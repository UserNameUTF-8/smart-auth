from pydantic import BaseModel


class EmpBaseModel(BaseModel):
    """
    :emp_fullname
    :emp_password
    :emp_email
    :emp_coding
    :emp_ip optional
    """
    emp_fullname: str
    emp_password: str
    emp_email: str
    emp_coding: bytes
    emp_ip: str | None = None


class EmpUpdateBaseModel(BaseModel):
    emp_id: int
    emp_fullname: str | None = None
    emp_password: str | None = None
    emp_ip: str | None = None
