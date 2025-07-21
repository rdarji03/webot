from fastapi import APIRouter
from app.schemas.web_crawl_schema import WebsiteCreate
from app.services.scraperService import store_website

router = APIRouter()


@router.post('/scrap')
async def start_web_scrap(website_data: WebsiteCreate):
    data = website_data.dict(by_alias=True)
    result = await store_website(data)  # ✅ yeh sahi hai
    return {"message": "Website data received", "data": result}
