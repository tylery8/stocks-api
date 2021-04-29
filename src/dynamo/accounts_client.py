from src.dynamo.table import Client
from src.models.account import Account

ACCOUNTS_CLIENT = Client(Account, 'accounts', 'account_id')
