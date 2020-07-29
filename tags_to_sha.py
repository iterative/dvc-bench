import os
from contextlib import contextmanager

from asv.config import Config
from git import Repo


@contextmanager
def dvc_git_repo():
    repo = Repo(Config.load("asv.conf.json").project)
    yield repo
    repo.close()


def convert_to_sha(tags_filename="tags.txt", hashes_filename="hashes.txt"):
    tags = []
    with open(tags_filename, "r") as fobj:
        tags.extend([l.strip() for l in fobj.readlines()])

    with dvc_git_repo() as repo:
        hashes = [repo.commit(t).hexsha + os.linesep for t in tags]

    with open(hashes_filename, "w") as fobj:
        fobj.writelines(hashes)


if __name__ == "__main__":
    convert_to_sha()
