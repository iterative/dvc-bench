from collections import defaultdict
import csv
from typing import TextIO
from tabulate import tabulate
import argparse


def csv_to_md(file: TextIO) -> str:
    data = defaultdict(list)
    for row in csv.DictReader(file):
        for key, value in row.items():
            data[key].append(value)
    return tabulate(data, data.keys(), tablefmt="github")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert csv file to markdown table."
    )
    parser.add_argument("file", type=argparse.FileType("r"))
    parser.add_argument(
        "--wrap",
        action="store_true",
        default=False,
        help="Wrap in code blocks",
    )
    args = parser.parse_args()

    out = csv_to_md(args.file)
    if args.wrap:
        out = f"```\n{out}\n```"
    print(out)
