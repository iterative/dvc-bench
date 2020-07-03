import calendar
import datetime
import os
import time

import feedparser


def get_entries_since(feed_url, days=1):
    d = feedparser.parse(feed_url)

    current_time = int(time.time())
    delta_time = datetime.timedelta(days=days).total_seconds()

    new_feed_entries = []
    for entry in d["entries"]:
        updated_time = calendar.timegm(entry["updated_parsed"])
        if current_time - updated_time <= delta_time:
            new_feed_entries.append(entry)

    return new_feed_entries


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
    entries = get_entries_since(feed, 1)
    prepare_issue_file(entries)
