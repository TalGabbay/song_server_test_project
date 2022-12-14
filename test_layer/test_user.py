import pytest
import json
import re
from logic_layer import api_calls


@pytest.mark.user
@pytest.mark.parametrize("user_name", ["a",
                                       "A",
                                       "aaa",
                                       "Tal",
                                       "gabbay"])
def test_add_user(user_name, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    set_user = api_calls.add_user(user_name, "1")
    assert set_user.status_code == 200, f'Error: expected status code 200 returned {set_user.status_code}'
    user_response = api_calls.get_user(user_name)
    server_user_name = json.loads(user_response.text)['data']['user_name']
#    print(user_response.json()['data']['user_name'])
    assert server_user_name == user_name, f'Error: User name assertion fail expected {user_name} returned {server_user_name}'


@pytest.mark.user
@pytest.mark.xfail
@pytest.mark.parametrize("user_name", ["a",
                                       "A",
                                       "aaa",
                                       "Tal",
                                       "gabbay"])
def test_get_nonexistent_user(user_name, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    get_user_response = api_calls.get_user(user_name)
    assert get_user_response.status_code != 200, f'Error: get user returned status code 200 for unexciting user'


# cannot be tested because the get_unexisting user isn't working well
@pytest.mark.user
@pytest.mark.xfail
@pytest.mark.parametrize("user_name", ["a",
                                       "A",
                                       "aaa",
                                       "Tal",
                                       "gabbay"])
def test_delete_user(user_name, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    set_user = api_calls.add_user(user_name, "1")
    assert set_user.status_code == 200, f'Error: expected status code 200 returned {set_user.status_code}'
    get_user_response = api_calls.get_user(user_name)
    assert get_user_response.status_code == 200, f'Error: expected status code 200 returned {set_user.status_code}'
    delete_user_response = api_calls.delete_all_users()
    assert delete_user_response.status_code == 200, f'Error: expected status code 200 returned {set_user.status_code}'
    get_user_response = api_calls.get_user(user_name)
    assert get_user_response.status_code != 200, f'Error: getuser returned status code 200 after deletion'


@pytest.mark.user
@pytest.mark.xfail
@pytest.mark.parametrize("user_name", ["",
                                       "1",
                                       "*",
                                       "    "])
def test_add_illigal_user(user_name, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    set_user = api_calls.add_user(user_name, "1")
    assert set_user.status_code != 200, f'Error: system excepted {user_name} as user_name'


@pytest.mark.user
@pytest.mark.xfail
@pytest.mark.parametrize("user_name", ["Tal",
                                       "tal",
                                       "A",
                                       "eli anna",
                                       "@tal"])
def test_add_user_with_same_name(user_name, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    set_user = api_calls.add_user(user_name, "1")
    assert set_user.status_code == 200, f'Error: expected status code 200 returned {set_user.status_code}'
    set_user = api_calls.add_user(user_name, "1")
    assert set_user.status_code != 200, f'Error: expected error code for inserting two users with the same name' \
                                        f' returned {set_user.status_code}'


@pytest.mark.user
@pytest.mark.parametrize(("user_name1", "user_name2"),
                         [("Tal", "tal"),
                          ("a", "A"),
                          ("taL", "Tal")])
def test_add_user_with_almost_same_name(user_name1, user_name2, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    set_user_response = api_calls.add_user(user_name1, "1")
    assert set_user_response.status_code == 200, f'Error: expected status code 200 returned {set_user_response.status_code}'
    set_user_response = api_calls.add_user(user_name2, "1")
    assert set_user_response.status_code == 200, f'Error: expected 200 for inserting two users with the same name' \
                                                 f' but different Capital letters returned' \
                                                 f' {set_user_response.status_code}'


@pytest.mark.user
@pytest.mark.security
@pytest.mark.parametrize(("user_name", "password"),
                         [("Tal", "123"),
                          ("a", "A"),
                          ("taL", "@3445Tal")])
def test_get_user_password(user_name, password, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    set_user = api_calls.add_user(user_name, password)
    get_user = api_calls.get_user(user_name)
    match = re.search(password, get_user.text)
    assert not match, f'Error: get user response contains the user password {match.group(0)}'


@pytest.mark.user
@pytest.mark.security
@pytest.mark.xfail
@pytest.mark.parametrize(("user_name", "password"),
                         [("Tal", "123"),
                          ("a", "A"),
                          ("taL", "@3445Tal")])
def test_change_user_password_using_wrong_password(user_name, password, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    set_user = api_calls.add_user(user_name, password)
    assert set_user.status_code == 200, f'Error: expected status code 200 returned {set_user.status_code}'
    change_password_response = api_calls.change_user_password(user_name, "wrong password", "new password")
    assert change_password_response.status_code != 200, f'Error:changing users passport with a wrong password returned' \
                                                        f' status code 200'


@pytest.mark.user
@pytest.mark.security
@pytest.mark.parametrize(("user_name", "password", "new_password"),
                         [("Tal", "123", "321"),
                          ("a", "A", "567"),
                          ("taL", "@3445Tal", "kkk")])
def test_change_user_password(user_name, password, new_password, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    set_user = api_calls.add_user(user_name, password)
    assert set_user.status_code == 200, f'Error: expected status code 200 returned {set_user.status_code}'
    change_password_response = api_calls.change_user_password(user_name, password, new_password)
    assert change_password_response.status_code == 200, f'Error: expected status code 200 returned ' \
                                                        f'{change_password_response.status_code}'
    change_password_response = api_calls.change_user_password(user_name, new_password, password)
    assert change_password_response.status_code == 200, f'Error: status {change_password_response.status_code}' \
                                                        f' expected 200 using the new password after changing it'


@pytest.mark.user
@pytest.mark.security
@pytest.mark.xfail
@pytest.mark.parametrize(("user_name", "password", "new_password"),
                         [("Tal", "123", "321"),
                          ("a", "A", "567"),
                          ("taL", "@3445Tal", "kkk")])
def test_change_user_password_using_old_password(user_name, password, new_password, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    set_user = api_calls.add_user(user_name, password)
    assert set_user.status_code == 200, f'Error: expected status code 200 returned {set_user.status_code}'
    change_password_response = api_calls.change_user_password(user_name, password, new_password)
    assert change_password_response.status_code == 200, f'Error: expected status code 200 returned ' \
                                                        f'{change_password_response.status_code}'
    change_password_response = api_calls.change_user_password(user_name, password, new_password)
    assert change_password_response.status_code != 200, f'Error: status {change_password_response.status_code}' \
                                                        f' old password can still be used after changing passwords'


@pytest.mark.user
@pytest.mark.parametrize(("user1", "user2"),
                         [("Tal", "moses"),
                          ("a", "b"),
                          ("c", "Tcc")])
def test_add_friend(user1, user2, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    set_user1_response = api_calls.add_user(user1, "1")
    assert set_user1_response.status_code == 200, f'Error: expected status code 200 returned ' \
                                                  f'{set_user1_response.status_code}'
    set_user2_response = api_calls.add_user(user2, "1")
    assert set_user2_response.status_code == 200, f'Error: expected status code 200 returned ' \
                                                  f'{set_user2_response.status_code}'
    add_friend_response = api_calls.add_friend(user1, "1", user2)
    assert add_friend_response.status_code == 200, f'Error: adding friend expected status code 200 returned ' \
                                                   f'{set_user2_response.status_code}'
    get_user1_response = api_calls.get_user(user1)
    json_format = json.loads(get_user1_response.text)
    json_format["data"]["friends"]
    assert json_format["data"]["friends"][0] == user2, f'Error: get user response does not contains' \
                                                       f' the added friend {user2}'


@pytest.mark.user
@pytest.mark.xfail
@pytest.mark.parametrize("user_name", ["a",
                                       "A",
                                       "aaa",
                                       "Tal",
                                       "gabbay"])
def test_add_unexisting_friend(user_name, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    set_user1_response = api_calls.add_user(user_name, "1")
    assert set_user1_response.status_code == 200, f'Error: expected status code 200 returned ' \
                                                  f'{set_user1_response.status_code}'
    add_friend_response = api_calls.add_friend(user_name, "1", "user_friend")
    assert add_friend_response.status_code != 200, f'Error: adding nonexistent friend responded 200'


@pytest.mark.user
@pytest.mark.xfail
@pytest.mark.parametrize("user_name", ["aaa",
                                       "Tal",
                                       "gabbay"])
def test_add_friend_with_wrong_password(user_name, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    set_user1_response = api_calls.add_user(user_name, "1")
    assert set_user1_response.status_code == 200, f'Error: expected status code 200 returned ' \
                                                  f'{set_user1_response.status_code}'
    add_friend_response = api_calls.add_friend(user_name, " ", "user_friend")
    assert add_friend_response.status_code != 200, f'Error: adding a friend  with wrong password responded 200'
    get_user_response = api_calls.get_user(user_name)
    json_format = json.loads(get_user_response.text)
    get_user_json = json_format["data"]["friends"]
    assert get_user_json[0] == "user_friend", f'Error: get user response do not contains the added friend'
