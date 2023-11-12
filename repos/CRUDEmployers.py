import datetime

from Utils import Utils
from sqlalchemy import Delete, Update
from database.Employer import Employer, History
from database.maindb import session
from services.ServiceEmployer import EmpBaseModel, EmpUpdateBaseModel


class EmpNotFoundError(RuntimeError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class MailExistsError(RuntimeError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class InValidArgumentError(RuntimeError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class CRUDEmployers:
    """
        all gets: all, id, mail, chaine
        delete: id
        update: modelUpdate :params fullname or emp_ip [rq]
        update: modelUpdate :params password [rq]

        create: EmpBaseModel: (fullname, password, mail, face coding) [req] and ip [op]
    """

    @staticmethod
    def dataValidation(fullname: str, email: str, password: str, ip: str | None = None):
        if len(fullname) < 3 or len(fullname) > 60 or len(email) > 60 or len(email) < 5 or len(password) < 6:
            raise InValidArgumentError("Invalid Length of Arguments")

        if email.find('@') == -1:
            raise InValidArgumentError("Invalid Email")

    @staticmethod
    def getAllEmployers():
        return session.query(Employer).all()

    @staticmethod
    def addEmployer(emp: EmpBaseModel):
        emailExists = True
        try:
            CRUDEmployers.getEmpByMail(emp.emp_email)
        except EmpNotFoundError:
            emailExists = False

        if emailExists:
            raise MailExistsError(f'Mail f{emp.emp_email} Exists')

        CRUDEmployers.dataValidation(emp.emp_fullname, emp.emp_email, emp.emp_password, emp.emp_ip)
        hashed_password = Utils.sha256(emp.emp_password)
        new_emp = Employer(emp.emp_fullname, emp.emp_email, hashed_password, emp.emp_ip, emp.emp_coding)
        session.add(new_emp)
        session.commit()

    @staticmethod
    def getEmpById(id_: int):
        if type(id_) is not int:
            raise InValidArgumentError('id should be int')
        emp = session.query(Employer).where(Employer.emp_ip == id_).first()
        if not emp:
            raise EmpNotFoundError(f'Employer with id {id} is not Exists')
        return emp

    @staticmethod
    def getEmpByMail(email: str):
        emp = session.query(Employer).where(Employer.emp_email == email).first()
        if emp is None:
            raise EmpNotFoundError(f'There is No Employer is Email {email}')
        return emp

    @staticmethod
    def deleteEmpById(id_: int):
        query = Delete(Employer).where(Employer.emp_id == id_)
        session.execute(query)
        session.commit()

    @staticmethod
    def updateEmp(emp_: EmpUpdateBaseModel):
        CRUDEmployers.getEmpById(emp_.emp_id)
        if emp_.emp_ip is None and emp_.emp_fullname is None:
            raise InValidArgumentError('No Specified Argument To Update')
        query = Update(Employer).where(Employer.emp_ip == emp_.emp_ip)

        if len(emp_.emp_fullname) > 60 or len(emp_.emp_fullname) < 3:
            raise InValidArgumentError('Invalid Employer Name')

        if emp_.emp_ip and len(emp_.emp_ip) > 16 or len(emp_.emp_ip) < 8:
            raise InValidArgumentError('Invalid Ip Address')

        if emp_.emp_fullname:
            query.values({Employer.emp_fullname: emp_.emp_fullname})

        if emp_.emp_ip:
            query.values({Employer.emp_ip: emp_.emp_ip})

        session.execute(query)
        session.commit()

    @staticmethod
    def updateEmpPass(modelWithPass: EmpUpdateBaseModel):
        if modelWithPass.emp_password is None:
            raise InValidArgumentError('Password not Exists ')

        if len(modelWithPass.emp_password) < 6:
            raise InValidArgumentError('Password Is Too Short')

        hashedPass = Utils.sha256(modelWithPass.emp_password)

        Update(Employer).values({Employer.emp_password: hashedPass}).where(Employer.emp_id == modelWithPass.emp_id)

        return "updated success"


class GetEmployersBy:
    def __init__(self):
        self.query = session.query(Employer)

    def created_at(self, datetime_: datetime.datetime):
        self.query = self.query.where(Employer.created_at == datetime_)
        return self

    def update_at(self, datetime_: datetime.datetime):
        self.query = self.query.where(Employer.updated_at == datetime_)
        return self

    def ipAddress(self, ip: str):
        self.query = self.query.where(Employer.emp_ip == ip)
        return self

    def isActive(self, isActive):
        self.query = self.query.where(Employer.is_active == isActive)
        return self

    def countChangePass(self, numberChange: int):
        self.query = self.query.where(Employer.change_password_count == numberChange)
        return self

    def fullName(self, name):
        self.query = self.query.where(Employer.emp_fullname == name)
        return self

    def all_(self) -> list[Employer]:
        list_ = self.query.all()
        self.query = session.query(Employer)
        return list_


if __name__ == '__main__':
    # newEmp = Employer(
    #     'Imed jbeli',
    #     'imed@go.com',
    #     "not hashed pass",
    #     "localhost",
    #     'noCoding'.encode()
    # )
    #
    new_history = History(1)
    session.add(new_history)
    session.commit()
