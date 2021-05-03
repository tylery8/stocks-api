class Account:
    def __init__(self, account_id, watchlist=None, portfolio=None):
        self.account_id = account_id
        self.watchlist = [] if watchlist is None else watchlist
        self.portfolio = {'deposit': 0, 'trades': []} if portfolio is None else portfolio
