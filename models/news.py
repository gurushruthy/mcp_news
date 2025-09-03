from datetime import datetime
from pydantic import BaseModel

class NewsItem(BaseModel):
    id:str
    title:str
    description:str
    url:str
    source:str
    published_at:datetime
