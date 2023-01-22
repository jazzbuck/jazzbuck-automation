import requests as re
import json as json
from dataclasses import dataclass
import datetime
import time
import yaml


@dataclass
class PocketSession:
    """
    PocketSession stores state data about interaction with Pocket.
    """

    username: str
    consumer_key: str
    access_token: str

    def get_since(
        self,
        date: datetime.datetime = datetime.datetime.now() - datetime.timedelta(hours=1),
    ) -> None:
        """
        get_since retrieves saved items since datetime (by default 1 hour ago) and saves to payload
        """
        method_url = "https://getpocket.com/v3/get"
        consumer_key = self.consumer_key
        access_token = self.access_token

        headers = {"Content-Type": "application/json"}
        payload = {
            "consumer_key": consumer_key,
            "access_token": access_token,
            "since": time.mktime(date.timetuple()),
            "detailType": "simple",
        }

        r = re.post(method_url, data=json.dumps(payload), headers=headers)

        self.data = r.json()["list"]
        self.since = date

        r.close()

    def write_data(
        self,
        filename: str,
    ) -> None:
        """
        write data in class to filename
        """
        with open(filename, "w") as fp:
            json.dump(self.data, fp)


def write_pocket_data_to_markdown(
    pocket_dict: dict[str, dict],
) -> list[tuple[str, str]]:
    """
    Convenience function to write pocket data to markdown for Obsidian.
    """
    list_of_markdown = []

    if not (pocket_dict):
        return []

    if pocket_dict:

        for key, item in pocket_dict.items():

            match item:
                case item if "resolved_title" in item:
                    title = item["resolved_title"]
                case item if "given_title" in item:
                    title = item["given_title"]
                case _:
                    title = format(datetime.datetime.now(), "%Y%m%d%H%M")

            match item:
                case item if "time_added" in item:
                    time_added = datetime.datetime.utcfromtimestamp(
                        int(item["time_added"])
                    )
                case _:
                    time_added = datetime.datetime.now()
            time_added = format(time_added, "%Y%m%d%H%M")

            match item:
                case item if "resolved_url" in item:
                    url = item["resolved_url"]
                case _:
                    url = ""

            try:
                excerpt = item["excerpt"]
            except:
                excerpt = ""

            markdown = f"""---
id: {time_added}
aliases: ["{time_added}","{title}"]
---
#reading-inbox

# {title}

{url}

{excerpt}"""

            title = "".join(x for x in title.title() if not x.isspace())
            title = "".join(x for x in title if x.isalnum())
            title = time_added + "-" + title

            list_of_markdown.append((title, markdown))

    return list_of_markdown
