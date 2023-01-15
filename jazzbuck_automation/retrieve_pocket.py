import requests as re
import json as json
from dataclasses import dataclass
import datetime
import time
import webbrowser
from typing import Tuple


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
            "detailType": "complete",
        }

        r = re.post(method_url, data=json.dumps(payload), headers=headers)

        self.data = r.json()["list"]

    def write_data(
        self,
        filename: str,
    ) -> None:
        """
        write data in class to filename
        """
        with open(filename, "w") as fp:
            json.dump(self.data, fp)


def authenticate_pocket(
    consumer_key: str,
) -> Tuple[str, str]:
    """
    authenticates with pocket
    """
    method_url = "https://getpocket.com/v3/oauth/request"
    headers = {
        "Content-Type": "application/json",
        "X-Accept": "application/json",
        "charset": "UTF-8",
    }
    payload = {"consumer_key": consumer_key, "redirect_uri": "https://dis.repair"}
    r = re.post(method_url, data=json.dumps(payload), headers=headers)
    code = r.json()["code"]
    webbrowser.open(
        f"https://getpocket.com/auth/authorize?request_token={code}&redirect_uri=https://dis.repair"
    )
    input("Press any key to continue...")
    payload = {"consumer_key": consumer_key, "code": code}
    s = re.post(
        "https://getpocket.com/v3/oauth/authorize",
        data=json.dumps(payload),
        headers=headers,
    )
    access_token = s.json()["access_token"]
    username = s.json()["username"]

    return username, access_token
