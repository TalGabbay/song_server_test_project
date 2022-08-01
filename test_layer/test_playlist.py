import pytest
import json
from src.logic_layer import api_calls


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


@pytest.mark.xfail
@pytest.mark.parametrize("user_name", ["tal", "Salomon", "lambda"])
def test_add_playlist_to_unexisting_user(user_name, delete_users):
    assert delete_users.status_code == 200, "Bad response"
    add_playlist_response = api_calls.add_playlist(user_name, "a", "Summer Vibes")
    assert add_playlist_response.status_code != 200, f'Error: Adding playlist to unexisting user responded 200'


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

