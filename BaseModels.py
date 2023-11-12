from pydantic import BaseModel
import datetime


class AdminBaseModel(BaseModel):
    """
    :admin_fullname
    :admin_password
    :admin_email
    :admin_ip optional
    """
    admin_fullname: str
    admin_password: str
    admin_email: str
    admin_ip: str | None = None


class ResponseAdmin(BaseModel):
    admin_id: int
    admin_fullname: str
    admin_password: str
    admin_email: str
    admin_ip: str | None = None
    change_password_count: int
    is_mail_correct: bool
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime | None


class UpdateAdminBaseModel(BaseModel):
    """
        WITH ID SHOULD HAVE AT LEAST ONE PARAM
    """
    admin_id: int
    admin_name: str | None = None
    admin_ip: str | None = None
    admin_password: str | None = None
