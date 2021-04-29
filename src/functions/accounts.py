from src.dynamo.accounts_client import ACCOUNTS_CLIENT
from src.ids.generators import generate_account_id
from src.models.account import Account


def create():
    account = Account(
        account_id=generate_account_id()
    )

    ACCOUNTS_CLIENT.put_item(account)

    return 201, account.__dict__


def read_watchlist(account_id):
    account = ACCOUNTS_CLIENT.get_item(account_id)

    return 200, account.watchlist


def update_watchlist(account_id, watchlist):
    account = ACCOUNTS_CLIENT.get_item(account_id)

    if account.watchlist != watchlist:
        account.watchlist = watchlist
        ACCOUNTS_CLIENT.put_item(account)

    return 200, watchlist


def read_apikey(account_id):
    account = ACCOUNTS_CLIENT.get_item(account_id)

    return 200, account.apikey


def update_apikey(account_id, apikey):
    account = ACCOUNTS_CLIENT.get_item(account_id)

    if account.apikey != apikey:
        account.apikey = apikey
        ACCOUNTS_CLIENT.put_item(account)

    return 200, apikey
