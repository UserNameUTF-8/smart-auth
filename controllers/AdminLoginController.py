import datetime
from datetime import timedelta
from typing import Annotated

import repos.CRUDAdmins
from BaseModels import ResponseAdmin
from fastapi import HTTPException, Depends, APIRouter, Form
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from Utils import Utils
from services.ServiceAdmin import getAdminByMail
from jose import jwt, JWTError

from services.ServiceAdminLogin import oauth2_scheme, SECRET_KEY, ALGORITHM, create_access_token

log_ = APIRouter(prefix='/admin')


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
    except JWTError:
        raise credentials_exception

    admin__ = getAdminByMail(email)

    if admin__ is None:
        raise credentials_exception

    return admin__


@log_.post("/login")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    try:

        admin_: ResponseAdmin = getAdminByMail(form_data.username)

    except repos.CRUDAdmins.AdminNotFoundError as e:
        raise HTTPException(detail=e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if not admin_:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if admin_.admin_password != Utils.sha256(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid admin name or password'
        )
    access_token_expires = timedelta(days=10)  # valid 10 days
    access_token = create_access_token(
        data={"sub": admin_.admin_email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer",
            "exp_time": datetime.datetime.now() + access_token_expires}


@log_.post('/current-admin', response_model=ResponseAdmin)
def get_current_admin(current_user: Annotated[ResponseAdmin, Depends(get_current_user)]):
    return current_user
