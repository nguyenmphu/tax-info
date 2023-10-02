import json
import random
import string
from typing import Optional

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from .models import TaxInfo


RANDOM_CHARS = string.ascii_lowercase + string.digits

BASE_URL = 'https://masothue.com'
HEADERS = {
    'authority': 'masothue.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'dnt': '1',
    'origin': 'https://masothue.com',
    'referer': 'https://masothue.com/',
    'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43',
    'x-requested-with': 'XMLHttpRequest',
}


async def get_tax_info_by_id(id_: str) -> Optional[TaxInfo]:
    async with ClientSession() as session:
        session.headers.update(HEADERS)
        token = await __get_token(session)
        if token:
            url = await __get_tax_info_url(session, id_, token)
            return await __get_tax_info(session, url)


async def __get_token(session: ClientSession) -> Optional[str]:
    async with session.post(f'{BASE_URL}/Ajax/Token', data={'r': __random_word()}) as response:
        if response.status == 200:
            token = json.loads(await response.read()).get('token')
            return token


async def __get_tax_info_url(session: ClientSession, id_: str, token: str) -> Optional[str]:
    async with session.post(f'{BASE_URL}/Ajax/Search',
            data={
                'q': id_,
                'type': 'personal',
                'token': token,
            }
        ) as response:
        if response.status == 200:
            path = json.loads(await response.read()).get('url')
            if path:
                return f'{BASE_URL}{path}'      


async def __get_tax_info(session: ClientSession, url: str) -> Optional[TaxInfo]:
    async with session.get(url) as response:
        if response.status == 200:
            html = str((await response.read()).decode("utf-8"))
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find(class_='table-taxinfo')
            return TaxInfo(
                tax_id=table.find(itemprop='taxID').get_text().strip(),
                name=table.find('thead').get_text().strip(),
                address=table.find(itemprop='address').get_text().strip(),
            )


def __random_word():
    return ''.join(random.sample(RANDOM_CHARS, random.choice((5, 6, 7, 8, 9))))
