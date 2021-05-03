from src.dynamo.accounts_client import ACCOUNTS_CLIENT
from src.ids.generators import generate_account_id
from src.models.account import Account
from src.exceptions import WatchlistLimitExceededException, IllegalAmountException, InsufficientFundsException


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

    stocks = {}
    for trade in portfolio['trades']:
        symbol = trade['symbol']
        if symbol not in stocks:
            stocks[symbol] = {'symbol': symbol, 'shares': 0, 'trades': []}

        stocks[symbol]['shares'] += (1 if trade['buy'] else -1) * trade['shares']
        stocks[symbol]['trades'].append(trade)

    portfolio['stocks'] = list(stocks.values())

    return 200, portfolio


def add_trade(account_id, symbol, time, price, amount, buy=True):
    if amount <= 0:
        raise IllegalAmountException("Amounts must be positive")

    account = ACCOUNTS_CLIENT.get_item(account_id)

    if buy and amount > account.portfolio['cash']:
        raise InsufficientFundsException()

    account.portfolio['cash'] -= (1 if buy else -1) * amount

    account.portfolio['trades'].insert(0, {
        'symbol': symbol,
        'time': time,
        'price': round(price, 3),
        'amount': round(amount, 2),
        'shares': round(amount/price, 10),
        'buy': buy
    })

    ACCOUNTS_CLIENT.put_item(account)

    return 200, account.portfolio['trades'][0]


def add_deposit(account_id, deposit):
    if deposit <= 0:
        raise IllegalAmountException("Deposits must be positive")

    account = ACCOUNTS_CLIENT.get_item(account_id)

    account.portfolio['deposit'] += deposit
    account.portfolio['cash'] += deposit

    ACCOUNTS_CLIENT.put_item(account)

    return 200, {'deposit': deposit}
