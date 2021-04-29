class Account:
    def __init__(self, account_id, apikey=None, watchlist=None):
        self.account_id = account_id
        self.apikey = apikey
        self.watchlist = [] if watchlist is None else watchlist
