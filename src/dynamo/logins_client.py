from src.dynamo.table import Client
from src.models.login import Login


LOGINS_CLIENT = Client(Login, 'logins', 'username')
