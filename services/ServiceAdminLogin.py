from datetime import datetime, timedelta
from jose import jwt
from database.Employer import Employer
from BaseModels import AdminBaseModel

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from repos.CRUDAdmins import CRDAdmins

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def getAdminByMail_(mail: str):
    user: Employer = CRDAdmins.getAdminByMail(mail)  # get user or throw exception if not exist
    return AdminBaseModel(**user.__dict__)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=10)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


if __name__ == '__main__':
    print(getAdminByMail_('essid10110@gmail.com'))
