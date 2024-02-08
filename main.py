import json

import requests as req
from requests.exceptions import HTTPError

from wox import Wox


class Main(Wox):
    def query(self, input):
        return [
            {
                "Title": " " + input,
                "SubTitle": " Add Notion_DB",
                "IcoPath": "images\\icon.png",
                "JsonRPCAction": {
                    "method": "post_notion",
                    "parameters": ["{}".format(input)],
                    "dontHideAfterAction": False,
                },
            }
        ]

    def post_notion(self, user_input):
        file = open(".env")
        data = json.load(file)

        notion_token = data["token"]
        db_id = data["id"]
        file.close

        url = "https://api.notion.com/v1/pages"
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        body = {
            "parent": {"database_id": db_id},
            "properties": {
                "Name": {"title": [{"text": {"content": "{}".format(user_input)}}]}
            },
        }

        # req.request("POST", url=url, data=json.dumps(body), headers=headers)

        try:
            r = req.request("POST", url=url, data=json.dumps(body), headers=headers)
            # HTTPError occurs if status code is in the 400s or 500s
            r.raise_for_status()
            Wox.debug(self, "Posting Success")

        except HTTPError as e:
            raise Wox.debug(self, " Posting Failure\n" + str(e))


if __name__ == "__main__":
    Main()
