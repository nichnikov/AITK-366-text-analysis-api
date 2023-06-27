from typing import List
from pydantic import BaseModel


class Parameters(BaseModel):
    stopwords_files: List[str]
    service_host: str
    service_port: int