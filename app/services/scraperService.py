from app.models.web_crawl import WebScrawl
from app.config import db
from uuid import uuid4
import subprocess

website_collection = db['crawl_website']


async def store_website(web_data):
    crawl_id = str(uuid4())
    data = WebScrawl(
        website_name=web_data['website'],
        crawl_id=crawl_id
    )

    # isExistWebsite = await website_collection.find_one({'website_name': data.website_name})
    # if isExistWebsite:
    #     return {
    #         "status": True,
    #         "message": "Website Already Present",
    #         "data": {
    #             "website": isExistWebsite["website_name"],
    #             "crawl_id": str(isExistWebsite["_id"])
    #         }
    #     }

    # web_crawl_data = await website_collection.insert_one(data.dict(by_alias=True))

    sub_process_res = subprocess.run(
        ['python',
         'app/subprocesses/run_scrapper.py',
         web_data['website'],
         ],
        capture_output=True,
        text=True
    )

    if sub_process_res.returncode == 0:
        return {
            "status": "success",
            # "website_id": str(web_crawl_data.inserted_id),
            "output": sub_process_res.stdout
        }
    else:
        return {
            "status": "error",
            # "website_id": str(web_crawl_data.inserted_id),
            "error": sub_process_res.stderr
        }
