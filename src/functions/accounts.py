from src.dynamo.accounts_client import ACCOUNTS_CLIENT
from src.ids.generators import generate_account_id
from src.models.account import Account
from src.exceptions import WatchlistLimitExceededException, IllegalAmountException, InsufficientFundsException,\
    RapidTradeException
from time import time as now


def create():
    account = Account(
        account_id=generate_account_id()
    )

    ACCOUNTS_CLIENT.put_item(account)

    return 201, account.__dict__


def read_watchlist(account_id):
    account = ACCOUNTS_CLIENT.get_item(account_id)

    return 200, sorted(account.watchlist, key=lambda stock: stock['symbol'])


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

    for stock in portfolio['stocks'].values():
        stock['trades'].sort(key=lambda trade: trade['time'], reverse=True)

    portfolio['stocks'] = sorted([{'symbol': k, **v} for k, v in portfolio['stocks'].items()],
                                 key=lambda stock: stock['symbol'])

    portfolio['trades'] = sorted([{'symbol': stock['symbol'], **trade}
                                  for stock in portfolio['stocks']
                                  for trade in stock['trades']],
                                 key=lambda trade: trade['time'],
                                 reverse=True)

    return 200, portfolio


def add_trade(account_id, symbol, time, price, amount, buy=True):
    if amount <= 0:
        raise IllegalAmountException("Amounts must be positive")

    shares = amount/price

    account = ACCOUNTS_CLIENT.get_item(account_id)

    if round(now() * 1000) - account.portfolio['last_action'] <= 5000:
        raise RapidTradeException('Please wait at least 5 seconds between actions')

    if buy:
        if amount > account.portfolio['cash']:
            raise InsufficientFundsException()
    else:
        if shares > account.portfolio['stocks'][symbol]['shares']:
            raise InsufficientFundsException()

    account.portfolio['cash'] -= (1 if buy else -1) * amount

    if symbol not in account.portfolio['stocks']:
        account.portfolio['stocks'][symbol] = {'shares': 0, 'trades': []}

    account.portfolio['stocks'][symbol]['shares'] += (1 if buy else -1) * shares
    account.portfolio['stocks'][symbol]['trades'].insert(0, {
        'time': time,
        'price': round(price, 3),
        'amount': round(amount, 2),
        'shares': round(shares, 10),
        'buy': buy
    })

    account.portfolio['last_action'] = round(now() * 1000)

    ACCOUNTS_CLIENT.put_item(account)

    return 200, account.portfolio['stocks'][symbol]['trades'][0]


def add_deposit(account_id, amount):
    if amount <= 0:
        raise IllegalAmountException("Deposits must be positive")

    account = ACCOUNTS_CLIENT.get_item(account_id)

    account.portfolio['deposit'] += amount
    account.portfolio['cash'] += amount

    ACCOUNTS_CLIENT.put_item(account)

    return 200, {'amount': amount}
