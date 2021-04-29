class StocksException(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status


class RoutingException(StocksException):
    def __init__(self):
        super().__init__(400, "Routing Exception. Path does not exist")


class UsernameDoesNotExistException(StocksException):
    def __init__(self, username):
        super().__init__(400, f"Username {username} does not exist")


class IncorrectUsernamePasswordException(StocksException):
    def __init__(self):
        super().__init__(400, "Incorrect username/password")


class UsernameTakenException(StocksException):
    def __init__(self, username):
        super().__init__(400, f"Username {username} is taken")
