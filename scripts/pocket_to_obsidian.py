from jazzbuck_automation import *
import datetime
import argparse


parser = argparse.ArgumentParser(
    prog="pocket-to-obsidian",
    description="Retrieves latest pocket files from API",
)

parser.add_argument(
    "--secrets",
    "-s",
    type=str,
    required=True,
)

args = parser.parse_args()

print(args.secrets)

if __name__ == "__main__":

    fmt = "%Y%m%d%H%M"

    with open(args.secrets, "r") as r:
        secrets = yaml.safe_load(r)

    pocket = PocketSession(
        username=secrets["pocket"]["username"],
        consumer_key=secrets["pocket"]["consumer_key"],
        access_token=secrets["pocket"]["token"],
    )

    now = datetime.datetime.now()

    try:
        with open("latest_pocket_read.txt", "r") as r:
            then = r.read().strip()
            then = datetime.datetime.strptime(then, fmt)
    except:
        then = now - datetime.timedelta(days=1)

    pocket.get_since(then)
    pocket.write_data("latest_pocket_data.json")

    list_of_markdown = write_pocket_data_to_markdown(pocket.data)

    obsidian = ObsidianWebhookConnection(secrets["obsidian"])

    if list_of_markdown:

        for doc in list_of_markdown:
            obsidian.send_markdown_to_obsidian(
                target_path=f"reading-inbox/{doc[0]}.md", markdown=doc[1]
            )
            obsidian.send_markdown_to_obsidian(
                target_path=f"reading-inbox.todotxt",
                markdown=f"\n(A) [[reading-inbox/{doc[0]}.md|{doc[0]}]]",
            )

    with open("latest_pocket_read.txt", "w") as w:
        w.write(format(now, fmt))
