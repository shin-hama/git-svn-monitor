from datetime import datetime

from pydantic import BaseModel


class CommitInDB(BaseModel):
    author: str
    message: str
    repository_url: str
    ticket_id: int
    timestamp: datetime
    summary: str
