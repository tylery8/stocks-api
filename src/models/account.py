class Account:
    def __init__(self, account_id, watchlist=None):
        self.account_id = account_id
        self.watchlist = [] if watchlist is None else watchlist
