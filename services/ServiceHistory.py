import datetime

from pydantic import BaseModel


class HistoryBaseModel(BaseModel):
    id_emp: str
    date_: datetime.datetime | None = None


class ServiceHistory:
    pass
