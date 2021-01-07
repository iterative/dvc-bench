import os
from contextlib import contextmanager

from asv.config import Config
from git import Repo


@contextmanager
def dvc_git_repo():
    repo = Repo(Config.load("asv.conf.json").project)
    yield repo
    repo.close()


def convert_to_sha(
    tags_filename="revisions.txt", hashes_filename="hashes.txt"
):
    revs = []
    with open(tags_filename, "r") as fobj:
        revs.extend([l.strip() for l in fobj.readlines()])

    with dvc_git_repo() as repo:
        hashes = [repo.commit(r).hexsha + os.linesep for r in revs]

    with open(hashes_filename, "w") as fobj:
        fobj.writelines(hashes)


if __name__ == "__main__":
    convert_to_sha()
