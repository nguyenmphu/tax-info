from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder

from .crawl import get_tax_info_by_id

app = FastAPI()

@app.get('/api/search')
async def search(q: str):
    tax_info = await get_tax_info_by_id(q)
    if not tax_info:
        raise HTTPException(status_code=404, detail="Not found")
    return jsonable_encoder(tax_info)
