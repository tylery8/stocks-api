from src.exceptions import UsernameDoesNotExistException, IncorrectUsernamePasswordException, UsernameTakenException
from src.dynamo.logins_client import LOGINS_CLIENT
from src.models.login import Login
from src.functions import accounts
from hashlib import sha256


def read(username, password):
    login = LOGINS_CLIENT.get_item(username)

    if not login:
        raise UsernameDoesNotExistException(username=username)

    if encrypt_password(password) != login.encrypted_password:
        raise IncorrectUsernamePasswordException()

    return 200, login.__dict__


def create(username, password, apikey=None):
    login = LOGINS_CLIENT.get_item(username)

    if login:
        raise UsernameTakenException(username=username)

    login = Login(
        username=username,
        encrypted_password=encrypt_password(password),
        account_id=accounts.create()[1]['account_id'],
        apikey=apikey
    )

    LOGINS_CLIENT.put_item(login)

    return 200, login.__dict__


def encrypt_password(password):
    return sha256(password.encode()).hexdigest()
