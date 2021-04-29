import json
from src.exceptions import StocksException, RoutingException
from src.functions import logins, accounts


def main(routeKey, headers, body='{}', **kwargs):
    method, path = routeKey.split(' ')
    path = path.split('/')
    path.append(method)

    kwargs = json.loads(body)
    if 'x-stocks-username' in headers:
        kwargs['username'] = headers['x-stocks-username']
    if 'x-stocks-password' in headers:
        kwargs['password'] = headers['x-stocks-password']
    if 'x-stocks-account' in headers:
        kwargs['account_id'] = headers['x-stocks-account']

    try:
        return route(path, **kwargs)
    except StocksException as se:
        return se.status, {'message': str(se)}


def route(path, **kwargs):
    if path[1] == 'logins':
        if path[2] == 'GET':
            return logins.read(**kwargs)
        if path[2] == 'POST':
            return logins.create(**kwargs)
    if path[1] == 'apikey':
        if path[2] == 'GET':
            return accounts.read_apikey(**kwargs)
        if path[2] == 'PUT':
            return accounts.update_apikey(**kwargs)
    if path[1] == 'watchlist':
        if path[2] == 'GET':
            return accounts.read_watchlist(**kwargs)
        if path[2] == 'PUT':
            return accounts.update_watchlist(**kwargs)

    raise RoutingException()
