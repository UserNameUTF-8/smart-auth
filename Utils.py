import datetime
import hashlib
from database.maindb import session


class MailExists(RuntimeError):

    def __init__(self):
        super().__init__("Mail Exists")


class Utils:

    @staticmethod
    def sha256(pass_: str):
        hasher_ = hashlib.sha256()
        hasher_.update(pass_.encode())
        return hasher_.hexdigest()


if __name__ == '__main__':
    print(Utils.sha256("Hello World"))
