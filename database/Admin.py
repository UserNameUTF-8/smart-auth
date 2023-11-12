from database.maindb import Base, engine
from sqlalchemy import Column, Integer, String, TEXT, Boolean, DateTime
import datetime


class Admin(Base):
    __tablename__ = "admins"
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    admin_fullname = Column(String(60), nullable=False)
    admin_email = Column(String(60), nullable=False, unique=True)
    admin_password = Column(TEXT, nullable=False)
    admin_ip = Column(String(16))
    change_password_count = Column(Integer, default=0)
    is_mail_correct = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())

    def __init__(self, fullname: str, email: str, password: str, ip: str | None = None):
        """
         4 params
            :param fullname: str
            :param email: str
            :param password: str
            :param ip: str optional
        """
        self.admin_fullname = fullname
        self.admin_email = email
        self.admin_password = password
        self.admin_ip = ip


if __name__ == '__main__':
    # Admin.__table__.drop(engine)
    # Base.metadata.create_all(bind=engine)
    pass
