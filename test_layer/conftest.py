import pytest
from src.logic_layer import api_calls


@pytest.fixture()
def delete_users():
    return api_calls.delete_all_users()