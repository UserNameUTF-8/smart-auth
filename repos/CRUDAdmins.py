import datetime

from BaseModels import UpdateAdminBaseModel, ResponseAdmin, AdminBaseModel
from Utils import MailExists, Utils
from sqlalchemy import Delete, Update
from database.Admin import Admin
from database.maindb import session


class ArgumentError(RuntimeError):
    def __init__(self, mess):
        self.message = mess
        super().__init__(self.message)


class AdminNotFoundError(RuntimeError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class CRDAdmins:
    """
        ALL YOU NEED TO UPDATE DELETE CREATE READ FROM ADMINS
        TEMPLATE
        ADD ADMIN => VOID | ARGUMENT ERROR
        GET ADMIN BY ID => ADMIN | EXCEPTION ADMIN NOT FOUND
        GET ADMIN BY MAIL => ADMIN | EXCEPTION ADMIN NOT FOUND
        GET ALL ADMINS => LIST ADMINS | []
        GET ADMINS BY FULL NAME => LIST ADMINS | []
    """

    """
        ALL REQUESTS OF UPDATE AND DELETE SHOULD BE AUTHENTICATED
        WE DON'T HAVE TO CHECK FOR IF THE ADMIN EXISTS OR NOT
    """

    def __init__(self):
        self.__query = session.query(Admin)

    @staticmethod
    def datavalidation(fullname, password, email, ip=None):
        if (type(fullname) is not str or type(password) is not str or type(email) is not str or
                (ip is not None and type(ip) is not str)):
            raise ArgumentError('Parameters must be a Char-sequence')

        if len(fullname) > 60:
            raise ArgumentError('Admin Name Too Long')

        if len(email) > 60:
            raise ArgumentError('Admin Email Too Long')

        if len(fullname) < 3:
            raise ArgumentError('Admin Name Too Short')

        if len(email) < 4 or email.find('@') == -1:
            raise ArgumentError('Invalid Email')

    @staticmethod
    def addAdmin(admin__: AdminBaseModel):
        CRDAdmins.datavalidation(admin__.admin_fullname, admin__.admin_password, admin__.admin_email)
        exist = True
        try:
            CRDAdmins.getAdminByMail(admin__.admin_email)
        except AdminNotFoundError:
            exist = False

        if exist:
            raise MailExists
        hashed_password = Utils.sha256(admin__.admin_password)

        new_admin = Admin(fullname=admin__.admin_fullname, email=admin__.admin_email, password=hashed_password,
                          ip=admin__.admin_ip)
        session.add(new_admin)
        session.commit()

    @staticmethod
    def getAllAdmins():
        return session.query(Admin).all()

    @staticmethod
    def getAdminByMail(email: str):
        if type(email) is not str or len(email) > 60 or email.find('@') == -1:
            raise ArgumentError('Invalid Email')

        admin__ = session.query(Admin).filter(Admin.admin_email == email).first()

        if admin__ is None:
            raise AdminNotFoundError(f'Admin With Mail {email} Not Exists')

        return admin__

    @staticmethod
    def getAdminById(id_: int):
        if type(id_) is not int:
            raise ArgumentError('id Should be of Type Integer')

        admin__: Admin = session.query(Admin).filter(Admin.admin_id == id_).first()

        if admin__ is None:
            raise AdminNotFoundError(f'Admin With Id {id_} Not Found')

        return admin__

    def getAdminBy(self):
        return self

    def created_at(self, datatime_: datetime.datetime):
        self.__query = self.__query.filter(Admin.created_at == datatime_)
        return self

    def updated_at(self, datetime_: datetime.datetime):
        self.__query = self.__query.filter(Admin.updated_at == datetime_)
        return self

    def fullName(self, name: str):
        self.__query = self.__query.filter(Admin.admin_fullname == name)
        return self

    def ip(self, ipaddress: str):
        self.__query = self.__query.filter(Admin.admin_ip == ipaddress)
        return self

    def isActive(self):
        self.__query = self.__query.filter(Admin.is_active)
        return self

    def countChangePassword(self, number: int):
        self.__query = self.__query.filter(Admin.change_password_count == number)
        return self

    def isVerifiedMail(self):
        self.__query = self.__query.filter(Admin.is_mail_correct)
        return self

    def all_(self):
        adminList = self.__query.all()
        self.__query = session.query(Admin)
        return adminList

    @staticmethod
    def deleteAdminById(id_: int):
        session.execute(Delete(Admin).where(Admin.admin_ip == id_))
        session.commit()

    @staticmethod
    def updateAdmin(fields_to_update: UpdateAdminBaseModel):
        if fields_to_update.admin_ip is None and fields_to_update.admin_name is None:
            raise ArgumentError("Empty Body Bad Request")

        statement = Update(Admin).where(Admin.admin_id == fields_to_update.admin_id)

        if fields_to_update.admin_ip is not None:
            statement = statement.values(admin_ip=fields_to_update.admin_ip)

        if fields_to_update.admin_name is not None:
            statement = statement.values(admin_fullname=fields_to_update.admin_name)

        session.execute(statement)
        session.commit()
        return ResponseAdmin(**session.query(Admin).where(Admin.admin_id == fields_to_update.admin_id).first().__dict__)

    @staticmethod
    def updatePassword(pass_up: UpdateAdminBaseModel):
        if pass_up.admin_password is None:
            raise AdminNotFoundError("Bad Request Not Pass Not Found")

        query = Update(Admin).where(Admin.admin_id == pass_up.admin_id).values(
            {Admin.admin_password: Utils.sha256(pass_up.admin_password)})
        session.execute(query)
        session.commit()

        return session.query(Admin).where(Admin.admin_id == pass_up.admin_id).first()


if __name__ == '__main__':
    pass
