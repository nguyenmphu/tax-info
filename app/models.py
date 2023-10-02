from typing import Optional

from pydantic import BaseModel


class TaxInfo(BaseModel):
    tax_id: str
    name: str
    address: str
