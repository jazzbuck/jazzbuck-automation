from jazzbuck_automation import *
import yaml
import argparse

parser = argparse.ArgumentParser(
    prog="email-todo-to-obsidian",
    description='Retrieves "todo" emails from account and sends to Obsidian',
)

parser.add_argument(
    "--secrets",
    "-s",
    type=str,
    required=True,
)

args = parser.parse_args()

if __name__ == "__main__":

    with open(args.secrets, "r") as r:
        secrets = yaml.safe_load(r)

    imap = connect_to_imap_server(
        username=secrets["email"]["username"],
        password=secrets["email"]["password"],
        imap_server=secrets["email"]["imap_server"],
    )

    list_of_messages = retrieve_latest_emails(
        imap,
        10,
        secrets["email"]["expected_sender"],
        keyword="todo",
    )

    list_of_markdown = write_todo_email_to_markdown(list_of_messages)

    obsidian = ObsidianWebhookConnection(secrets["obsidian"])

    if list_of_markdown:

        for doc in list_of_markdown:
            obsidian.send_markdown_to_obsidian(
                target_path=f"to-do-list/{doc[0]}.md",
                markdown=doc[1],
            )

        imap = connect_to_imap_server(
            username=secrets["email"]["username"],
            password=secrets["email"]["password"],
            imap_server=secrets["email"]["imap_server"],
        )

        archive_emails_from_inbox(
            imap,
            "todo",
        )
