import unittest

from database.maindb import session
from repos.CRUDAdmins import CRDAdmins
from repos.CRUDEmployers import CRUDEmployers
from database.Employer import Employer
from services.ServiceAdmin import AdminBaseModel


def insertEmp():
    session.add(new_emp)
    session.commit()


class MyTestCase(unittest.TestCase):
    pass


if __name__ == '__main__':
    insertEmp()
    unittest.main()
