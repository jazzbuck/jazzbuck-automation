import requests as re
import dataclasses
import datetime
from typing import Tuple


@dataclasses.dataclass
class ObsidianWebhookConnection:

    url: str

    def send_markdown_to_obsidian(
        self,
        target_path: str,
        markdown: str,
    ) -> None:
        """
        Sends markdown to target path in obsidian vault using webhooks.
        """

        params = {"path": target_path}
        headers = {"Content-Type": "text/plain"}

        r = re.post(
            self.url,
            params=params,
            data=markdown,
            headers=headers,
        )

        r.close()


def make_to_do_markdown(subject: str, body: str) -> Tuple[str, str]:
    subject = "".join(x for x in subject if x.isalnum())
    subject = "".join(x for x in subject.title() if not x.isspace())
    date_formatted = format(datetime.datetime.now(), "%Y%m%d%H%M")
    title = date_formatted + "-" + subject
    body = f"""---
id: {date_formatted}
aliases: ["to-do: {subject}"]
---
#todo

# {subject}

{body}
"""

    return title, body


def make_reading_inbox_markdown(
    title: str,
    author: str,
    url: str,
) -> Tuple[str, str]:
    """ """
    pass
