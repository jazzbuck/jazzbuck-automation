import argparse
import os
import pathlib

parser = argparse.ArgumentParser(
    prog="archive-obsidian-inboxes",
    description="Moves all files from target folder with target hashtag to target archive folder",
)

parser.add_argument(
    "--inbox",
    "-i",
    type=str,
    required=True,
)

parser.add_argument(
    "--archive",
    "-a",
    type=str,
    required=True,
)

parser.add_argument(
    "--hashtag",
    "-t",
    type=str,
    required=True,
)

args = parser.parse_args()

if __name__ == "__main__":

    inbox_folder = pathlib.Path(args.inbox)
    archive_folder = pathlib.Path(args.archive).absolute()
    hashtag = args.hashtag

    for file in inbox_folder.iterdir():
        if file.is_file() and (file.suffix == ".md"):
            with open(file, "r") as r:
                contents = r.read()

            if (f"#{hashtag} " in contents) or (f"#{hashtag}\n" in contents):
                filename = file.name
                target = archive_folder / filename
                file.rename(target)
