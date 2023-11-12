import datetime

from BaseModels import ResponseAdmin, UpdateAdminBaseModel, AdminBaseModel
from repos.CRUDAdmins import CRDAdmins
from database.Admin import Admin


def getAllAdmins() -> list[ResponseAdmin]:
    response: list[Admin] = CRDAdmins.getAllAdmins()

    def returnE(admin: Admin):
        return ResponseAdmin(**admin.__dict__)

    map_ = map(returnE, response)

    return list(map_)


def getAdminById(id_: int):
    return ResponseAdmin(**CRDAdmins.getAdminById(id_).__dict__)


def getAdminByMail(mail: str):
    return ResponseAdmin(**CRDAdmins.getAdminByMail(mail).__dict__)


def addAdmin(new_admin: AdminBaseModel):
    return CRDAdmins.addAdmin(new_admin)


def updateAdmin(adminToUpdate: UpdateAdminBaseModel):
    return CRDAdmins.updateAdmin(adminToUpdate)


def updateAdminPass(adminPassToUpdate: UpdateAdminBaseModel):
    return CRDAdmins.updatePassword(adminPassToUpdate)


if __name__ == '__main__':
    """
        simple example
    """
