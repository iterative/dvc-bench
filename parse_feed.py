import datetime
import os
import re
import time

import feedparser
from revs_to_sha import dvc_git_repo


def get_commits_from_link(link):
    pattern = re.compile("commits=[0-9a-f]{40}-[0-9a-f]{40}")
    pattern_single = re.compile("commits=[0-9a-f]{40}")

    if pattern.search(link):
        (result,) = pattern.findall(link)
        return result.replace("commits=", "").split("-")
    elif pattern_single.search(link):
        (result,) = pattern_single.findall(link)
        return [result.replace("commits=", "")]
    raise Exception("Could not find commits in regression link!")


def latest_commit_time(revs):
    commit_times = []
    with dvc_git_repo() as repo:
        for r in revs:
            commit_times.append(repo.commit(r).committed_date)

    return sorted(commit_times)[-1]


def get_new_regressions(feed_url, days=1):
    d = feedparser.parse(feed_url)

    current_time = int(time.time())
    delta_time = int(datetime.timedelta(days=days).total_seconds())

    new_regressions = []
    for entry in d["entries"]:
        revs = get_commits_from_link(entry["link"])
        commit_time = latest_commit_time(revs)
        if current_time - commit_time <= delta_time:
            new_regressions.append(entry)

    return new_regressions


def prepare_issue_file(entries):
    if not entries:
        return

    path = os.path.join(".github", "ISSUE_TEMPLATE.md")

    lines = [
        "---",
        "title: \"[regression] check report {{ date | date('DD MM YYYY') }}\"",
        "assignees: pared",
        "labels: performance",
        "---",
    ]
    for index, e in enumerate(entries):
        lines.append(f"- [ ] {index+1}. [{e['title']}]({e['link']})")

    lines = map(lambda l: f"{l}{os.linesep}", lines)
    with open(path, "w") as fobj:
        fobj.writelines(lines)


if __name__ == "__main__":
    feed = "https://iterative.github.io/dvc-bench/regressions.xml"
    entries = get_new_regressions(feed)
    prepare_issue_file(entries)
