from src.dynamo.accounts_client import ACCOUNTS_CLIENT
from src.ids.generators import generate_account_id
from src.models.account import Account
from src.exceptions import WatchlistLimitExceededException, IllegalAmountException
from time import time
from decimal import Decimal


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
    if len(watchlist) > 8:
        raise WatchlistLimitExceededException(8)

    account = ACCOUNTS_CLIENT.get_item(account_id)

    if account.watchlist != watchlist:
        account.watchlist = watchlist
        ACCOUNTS_CLIENT.put_item(account)

    return 200, account.watchlist


def read_portfolio(account_id):
    account = ACCOUNTS_CLIENT.get_item(account_id)

    portfolio = account.portfolio

    portfolio['cash'] = portfolio['deposit'] - sum(
        (1 if trade['buy'] else -1) * trade['amount'] for trade in portfolio['trades']
    )

    stocks = {}
    for trade in portfolio['trades']:
        symbol = trade['symbol']
        if symbol not in stocks:
            stocks[symbol] = {'symbol': symbol, 'shares': 0, 'trades': []}

        stocks[symbol]['shares'] += (1 if trade['buy'] else -1) * trade['shares']
        stocks[symbol]['trades'].append(trade)

    portfolio['stocks'] = list(stocks.values())

    return 200, portfolio


def add_trade(account_id, symbol, price, amount, buy=True):
    if amount <= 0:
        raise IllegalAmountException("Amounts must be positive")

    account = ACCOUNTS_CLIENT.get_item(account_id)

    account.portfolio['trades'].insert(0, {
        'symbol': symbol,
        'time': round(time() * 1000),
        'price': Decimal(str(round(price, 3))),
        'amount': Decimal(str(round(amount, 2))),
        'shares': Decimal(str(round(amount/price, 10))),
        'buy': buy
    })

    ACCOUNTS_CLIENT.put_item(account)

    return 200, account.portfolio['trades'][0]


def set_deposit(account_id, deposit):
    if deposit <= 0:
        raise IllegalAmountException("Deposits must be positive")

    account = ACCOUNTS_CLIENT.get_item(account_id)

    if account.portfolio['deposit'] != deposit:
        account.portfolio['deposit'] = deposit
        ACCOUNTS_CLIENT.put_item(account)

    return 200, account.portfolio['deposit']
