from src.dynamo.accounts_client import ACCOUNTS_CLIENT
from src.ids.generators import generate_account_id
from src.models.account import Account
from src.exceptions import WatchlistLimitExceededException, IllegalAmountException
from time import time


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

    portfolio['cash'] = portfolio['deposit'] - sum(trade['cost'] for trade in portfolio['trades'])

    portfolio['trades'] = [{
        'symbol': trade['symbol'],
        'time': trade['time'],
        'price': trade['price'],
        'shares': abs(trade['cost'])/trade['price'],
        'amount': abs(trade['cost']),
        'buy': trade['cost'] >= 0
    } for trade in portfolio['trades']]

    stocks = {}
    for trade in portfolio['trades']:
        symbol = trade['symbol']
        if symbol not in stocks:
            stocks[symbol] = {'symbol': symbol, 'shares': 0, 'trades': []}

        stocks[symbol]['shares'] += trade['shares']
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
        'price': round(float(price) * 1000)/1000,
        'cost': (1 if buy else -1) * round(float(amount) * 100)/100
    })

    ACCOUNTS_CLIENT.put_item(account)

    return 200, account.portfolio['trades']


def set_deposit(account_id, deposit):
    if deposit <= 0:
        raise IllegalAmountException("Deposits must be positive")

    account = ACCOUNTS_CLIENT.get_item(account_id)

    if account.portfolio['deposit'] != deposit:
        account.portfolio['deposit'] = deposit
        ACCOUNTS_CLIENT.put_item(account)

    return 200, account.portfolio['deposit']
