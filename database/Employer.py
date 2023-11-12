from sqlalchemy import Integer, String, TEXT, BLOB, Column, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.maindb import Base, engine
import datetime


class Employer(Base):
    __tablename__ = "employers"
    emp_id = Column(Integer, primary_key=True, autoincrement=True)
    emp_fullname = Column(String(60), nullable=False)
    emp_email = Column(String(60), nullable=False, unique=True)
    emp_password = Column(TEXT, nullable=False)
    emp_ip = Column(String(16))
    change_password_count = Column(Integer, default=0)
    is_mail_correct = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    face_coding = Column(BLOB, nullable=False)

    auth_ = relationship("History", back_populates="employers")

    def __init__(self, fullname: str, email: str, password: str, emp_ip: str, face_coding: bytes):
        self.emp_fullname = fullname
        self.emp_email = email
        self.emp_password = password
        self.emp_ip = emp_ip,
        self.face_coding = face_coding


class EmpNotExistsError(RuntimeError):
    def __init__(self):
        super().__init__("Not Exists Employer")


"""
    HISTORY
"""


class History(Base):
    __tablename__ = 'history'
    date_auth = Column(DateTime, default=datetime.datetime.now(), primary_key=True)
    id_emp = Column(Integer, ForeignKey('employers.emp_id'), primary_key=True)
    employers = relationship("Employer", back_populates="auth_")

    def __init__(self, empId: int):
        self.id_emp = empId
        self.date_auth = datetime.datetime.now()


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
