from fastapi import APIRouter, HTTPException, status

import repos.CRUDAdmins
from services.ServiceAdmin import getAllAdmins, getAdminById, getAdminByMail, AdminBaseModel, addAdmin, \
    UpdateAdminBaseModel, updateAdminPass, updateAdmin

AC = APIRouter(prefix='/admins')


@AC.get('/')
def get_all_admins():
    return getAllAdmins()


@AC.post('/')
def add_admin(admin_: AdminBaseModel):
    try:
        addAdmin(admin_)
    except repos.CRUDAdmins.MailExists as e:
        raise HTTPException(detail=e.args[0], status_code=status.HTTP_409_CONFLICT)

    return getAdminByMail(admin_.admin_email)


@AC.get('/{id_}')
def get_admin_by_id(id_: int):
    try:
        return getAdminById(id_)
    except repos.CRUDAdmins.AdminNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@AC.patch('/')
def update_admin(admin_update: UpdateAdminBaseModel):
    try:
        return updateAdmin(admin_update)
    except repos.CRUDAdmins.ArgumentError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@AC.get('/mail/')
def get_admin_by_mail(mail: str):
    res = None
    try:
        res = getAdminByMail(mail)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e)

    return res


@AC.put('/pass-update')
def update_pass(admin_pass_update: UpdateAdminBaseModel):
    return updateAdminPass(admin_pass_update)
