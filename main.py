import json

import requests

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

        requests.request("POST", url=url, data=json.dumps(body), headers=headers)


if __name__ == "__main__":
    Main()
