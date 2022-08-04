import pytest
import json
from src.logic_layer import api_calls


@pytest.mark.playlist
@pytest.mark.parametrize("playlist", ["tal", "Salomon", "lambda"])
def test_add_playlist(playlist, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user("User1", "User1")
    assert add_user_response.status_code == 200, "Bad response"
    add_playlist_response = api_calls.add_playlist("User1", "User1", playlist)
    assert add_playlist_response.status_code == 200, f'Error: Adding playlist to user responded 200'
    get_user_response = api_calls.get_user("User1")
    assert get_user_response.status_code == 200, "Bad response"
    json_format = json.loads(get_user_response.text)
    assert json_format["data"]["playlists"][0] == playlist, f'Error: Playlist name {json_format["data"]["playlist"]}' \
                                                            f'is different then the given name {playlist}'


@pytest.mark.playlist
@pytest.mark.parametrize("playlist", ["tal", "Salomon", "lambda"])
def test_get_playlist(playlist, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user("User1", "User1")
    assert add_user_response.status_code == 200, "Bad response"
    add_playlist_response = api_calls.add_playlist("User1", "User1", playlist)
    assert add_playlist_response.status_code == 200, f'Error: Adding playlist to user responded 200'
    get_playlist_response = api_calls.get_playlist("User1", "User1", playlist)
    assert get_playlist_response.status_code == 200, f"Error: get playlist response: " \
                                                     f"{get_playlist_response.status_code} expected 200"


@pytest.mark.playlist
@pytest.mark.xfail
@pytest.mark.parametrize("playlist", ["tal", "Salomon", "lambda"])
def test_get_nonexistent_playlist(playlist, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user("User1", "User1")
    assert add_user_response.status_code == 200, "Bad response"
    get_playlist_response = api_calls.get_playlist("User1", "User1", playlist)
    assert get_playlist_response.status_code != 200, f"Error: get playlist responded 200 for an nonexistent playlist"


@pytest.mark.playlist
@pytest.mark.xfail
@pytest.mark.parametrize("playlist", ["tal", "Salomon", "lambda"])
def test_add_playlist_with_same_name(playlist, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user("User1", "User1")
    assert add_user_response.status_code == 200, "Bad response"
    add_playlist_response = api_calls.add_playlist("User1", "User1", playlist)
    assert add_playlist_response.status_code == 200, "Bad response"
    add_playlist_response = api_calls.add_playlist("User1", "User1", playlist)
    assert add_playlist_response.status_code != 200, "status code 200 for adding two playlists with the same name"


@pytest.mark.playlist
@pytest.mark.xfail
@pytest.mark.parametrize("user_name", ["tal", "Salomon", "lambda"])
def test_add_playlist_to_nonexistent_user(user_name, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    add_playlist_response = api_calls.add_playlist(user_name, "a", "Summer Vibes")
    assert add_playlist_response.status_code != 200, f'Error: Adding playlist to nonexistent user responded 200'


@pytest.mark.playlist
@pytest.mark.user
@pytest.mark.parametrize("playlist", ["tal", "Salomon", "lambda"])
def test_add_same_playlist_to_different_users(playlist, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user("User1", "User1")
    assert add_user_response.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user("User2", "User2")
    assert add_user_response.status_code == 200, "Bad response"
    add_playlist_response = api_calls.add_playlist("User1", "User1", playlist)
    assert add_playlist_response.status_code == 200, f'Error: Bad Response'
    add_playlist_response = api_calls.add_playlist("User2", "User2", playlist)
    assert add_playlist_response.status_code == 200, f'Error: Adding playlist with same name to different user responded' \
                                                     f'as error {add_playlist_response.status_code}'


@pytest.mark.playlist
@pytest.mark.security
@pytest.mark.parametrize("password", ["user1", " ", "uSER1"])
def add_playlist_using_wrong_password(password, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user("User1", "User1")
    assert add_user_response.status_code == 200, "Bad response"
    add_playlist_response = api_calls.add_playlist("User1", password, "playlist")
    assert add_playlist_response.status_code != 200, f'Error: adding a playlist to a user with wrong password'


@pytest.mark.playlist
@pytest.mark.user
@pytest.mark.parametrize("playlist", ["tal", "Salomon", "lambda"])
def get_another_users_playlist(playlist, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user("User1", "User1")
    assert add_user_response.status_code == 200, "Bad response"
    add_playlist_response = api_calls.add_playlist("User1", "User1", playlist)
    assert add_playlist_response.status_code == 200, f'Error: Bad Response'
    add_user_response = api_calls.add_user("User2", "User2")
    assert add_user_response.status_code == 200, "Bad response"
    get_playlist_response = api_calls.get_playlist("User2", "User2", playlist)
    assert get_playlist_response.status_code != 200 , f'Error: Getting user1 playlist using user2 credentials respnded' \
                                                      f'{get_playlist_response.status_code}'





