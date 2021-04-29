from src.exceptions import UsernameDoesNotExistException, IncorrectUsernamePasswordException, UsernameTakenException
from src.dynamo.logins_client import LOGINS_CLIENT
from src.models.login import Login
from src.functions import accounts


def read(username, password):
    login = LOGINS_CLIENT.get_item(username)

    if not login:
        raise UsernameDoesNotExistException(username=username)

    if encrypt_password(password) != login.password:
        raise IncorrectUsernamePasswordException()

    return 200, login.__dict__


def create(username, password):
    login = LOGINS_CLIENT.get_item(username)

    if login:
        raise UsernameTakenException(username=username)

    login = Login(
        username=username,
        password=encrypt_password(password),
        account_id=accounts.create()[1]['account_id']
    )

    LOGINS_CLIENT.put_item(login)

    return 200, login.__dict__


def encrypt_password(password):
    return password + '_enc'
