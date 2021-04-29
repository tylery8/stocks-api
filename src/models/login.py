class Login:
    def __init__(self, username, encrypted_password, account_id, apikey=None):
        self.username = username
        self.encrypted_password = encrypted_password
        self.account_id = account_id
        self.apikey = apikey
