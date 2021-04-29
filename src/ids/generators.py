from src.ids.utils import generate_id_for_table
from src.dynamo.accounts_client import ACCOUNTS_TABLE


def generate_account_id():
    return generate_id_for_table(table=ACCOUNTS_TABLE, length=15, prefix='A')
