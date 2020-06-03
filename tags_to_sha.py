import os

from git import Repo


def convert_to_sha(tags_filename="tags.txt", hashes_filename="hashes.txt"):
    tags = []
    with open(tags_filename, "r") as fobj:
        tags.extend([l.strip() for l in fobj.readlines()])

    git_repo = Repo("dvc")
    hashes = [git_repo.commit(t).hexsha + os.linesep for t in tags]

    with open(hashes_filename, "w") as fobj:
        fobj.writelines(hashes)


if __name__ == "__main__":
    convert_to_sha()
