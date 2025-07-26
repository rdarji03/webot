from app.models.web_crawl import WebScrawl
from app.models.web_page import WebPage
from app.config import db
from uuid import uuid4

website_collection = db['crawl_website']
website_page_collection = db['website_pages']


async def store_website(url: str):
    crawl_id = uuid4()
    isExsitedWebsite = await website_collection.find_one({'website_name': url})

    if isExsitedWebsite:
        return {
            "status": True,
            "message": "Website already present",
            "data": {
                "website": isExsitedWebsite["website_name"],
                "id": str(isExsitedWebsite["_id"])
            }
        }

    data = WebScrawl(
        website_name=url,
        crawl_id=str(crawl_id)
    )

    response = await website_collection.insert_one(data.dict())

    return {
        "status": True,
        "message": "Website stored successfully",
        "data": {
            "website": data.website_name,
            "crawl_id": str(crawl_id),
            "id": str(response.inserted_id)
        }
    }


async def store_pages(website_id, page,content):
    data = WebPage(
        website_id= website_id,
        page= page,
        content=content
    )
    await website_page_collection.insert_one(data.dict())

    return {
        "status": True,
        "message": "Website stored successfully",
        "data": {
           
        }
    }