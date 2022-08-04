import pytest
import json
from logic_layer import api_calls


@pytest.mark.song
@pytest.mark.parametrize(("song_genre", "song_year", "song_performer", "song_name"),
                         [("a", "1", "c", "d"),
                          ("bob", "1970", "reggae", "is this love")])
def test_add_songs(song_genre, song_year, song_performer, song_name, delete_songs):
    assert delete_songs.status_code == 200, f"Bad Response"
    add_songs_response = api_calls.add_song(song_genre, song_year, song_performer, song_name)
    assert add_songs_response.status_code == 200, f"Error: add songs responded {add_songs_response.status_code}" \
                                                  f"for lligal input"
    get_song_response = api_calls.get_song(song_name)
    assert get_song_response.status_code == 200, f"Error: get songs responded {add_songs_response.status_code}" \
                                                 f"after adding the song"


@pytest.mark.song
@pytest.mark.xfail
@pytest.mark.parametrize(("song_genre", "song_year", "song_performer", "song_name"),
                         [("", "1970", "reggae", "is this love"),
                          ("bob", "", "reggae", "is this love"),
                          ("bob", "1970", "", "is this love"),
                          ("bob", "1970", "reggae", ""),
                          ])
def test_add_songs_empty_fields(song_genre, song_year, song_performer, song_name, delete_songs):
    assert delete_songs.status_code == 200, f"Bad Response"
    add_songs_response = api_calls.add_song(song_genre, song_year, song_performer, song_name)
    assert add_songs_response.status_code == 200, f"Error: add songs responded {add_songs_response.status_code}" \
                                                  f"for lligal input"
    get_song_response = api_calls.get_song(song_name)
    assert get_song_response.status_code != 200, f"Error: get songs responded {add_songs_response.status_code}" \
                                                 f"after adding a song with an empty field"


@pytest.mark.song
@pytest.mark.xfail
@pytest.mark.parametrize(("song_genre", "song_year", "song_performer", "song_name"),
                         [("bob", "#$%^&", "reggae", "is this love"),
                          ("bob", "george bush", "reggae", "is this love"),
                          ])
def test_add_songs_illegal_year(song_genre, song_year, song_performer, song_name, delete_songs):
    assert delete_songs.status_code == 200, f"Bad Response"
    add_songs_response = api_calls.add_song(song_genre, song_year, song_performer, song_name)
    assert add_songs_response.status_code == 200, f"Error: add songs responded {add_songs_response.status_code}" \
                                                  f"for lligal input"
    get_song_response = api_calls.get_song(song_name)
    assert get_song_response.status_code != 200, f"Error: get songs responded {add_songs_response.status_code}" \
                                                 f"after adding a song with illegal year field"


@pytest.mark.song
@pytest.mark.xfail
@pytest.mark.parametrize(("song_genre", "song_year", "song_performer", "song_name"),
                         [("a", "1", "c", "d"),
                          ("bob", "1970", "reggae", "is this love")])
def test_add_same_songs_twice(song_genre, song_year, song_performer, song_name, delete_songs):
    assert delete_songs.status_code == 200, f"Bad Response"
    add_first_songs_response = api_calls.add_song(song_genre, song_year, song_performer, song_name)
    assert add_first_songs_response.status_code == 200, f"Error: add songs responded " \
                                                        f"{add_first_songs_response.status_code}" \
                                                        f"for lligal input"
    add_second_songs_response = api_calls.add_song(song_genre, song_year, song_performer, song_name)
    assert add_second_songs_response.status_code != 200, f"Error: add songs responded " \
                                                         f"{add_second_songs_response.status_code}" \
                                                         f"for adding an  identical song"


@pytest.mark.song
@pytest.mark.parametrize(("song_genre", "song_year", "song_performer", "song_name"),
                         [("a", "1", "c", "d"),
                          ("bob", "1970", "reggae", "is this love")])
def test_get_song(song_genre, song_year, song_performer, song_name, delete_songs):
    assert delete_songs.status_code == 200, f"Bad Response"
    add_songs_response = api_calls.add_song(song_genre, song_year, song_performer, song_name)
    assert add_songs_response.status_code == 200, f"Error: add songs responded {add_songs_response.status_code}" \
                                                  f"for lligal input"
    get_song_response = api_calls.get_song(song_name)
    assert get_song_response.status_code == 200, f"Error: get songs responded {add_songs_response.status_code}" \
                                                 f"after adding the song"
    json_format = json.loads(get_song_response.text)
    assert json_format["data"]["title"] == song_name, f"Error: song name {json_format[song_name]} is different" \
                                                      f" than the song" \
                                                      f" name that was added"


@pytest.mark.song
@pytest.mark.xfail
def test_get_nonexistent_song(delete_songs):
    assert delete_songs.status_code == 200, f"Bad Response"
    get_song_response = api_calls.get_song("song_name")
    assert get_song_response.status_code != 200, "Error: get song response for an un nonexistent song is 200"


@pytest.mark.playlist
@pytest.mark.song
@pytest.mark.parametrize(("song_genre", "song_year", "song_performer", "song_name"),
                         [("a", "1", "c", "d"),
                          ("bob", "1970", "reggae", "is this love")])
def test_add_song_to_playlist(song_genre, song_year, song_performer, song_name, delete_songs, delete_users):
    assert delete_songs.status_code == 200, "Bad response"
    assert delete_users.status_code == 200, "Bad response"
    add_songs_response = api_calls.add_song(song_genre, song_year, song_performer, song_name)
    assert add_songs_response.status_code == 200, f"Error: add songs responded {add_songs_response.status_code}" \
                                                  f"for lligal input"
    add_user_response = api_calls.add_user("User1", "User1")
    assert add_user_response.status_code == 200, "Bad response"
    add_playlist_response = api_calls.add_playlist("User1", "User1", "playlist")
    assert add_playlist_response.status_code == 200, f'Error: Adding playlist to user responded 200'
    add_song_to_playlist_response = api_calls.add_song_to_playlist("User1", "User1", "playlist", song_name)
    assert add_song_to_playlist_response.status_code == 200, "Error: add song to playlist bad response for lligal input"
    get_playlist_response = api_calls.get_playlist("User1", "User1", "playlist")
    assert get_playlist_response.status_code == 200, "Bad response"
    json_format = json.loads(get_playlist_response.text)
    json_format["data"][0]["title"] == song_name, f"Error: song name in playlist is different than input"


@pytest.mark.playlist
@pytest.mark.song
@pytest.mark.xfail
def test_add_nonexistent_song_to_playlist(delete_songs, delete_users):
    assert delete_songs.status_code == 200, "Bad response"
    assert delete_users.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user("User1", "User1")
    assert add_user_response.status_code == 200, "Bad response"
    add_playlist_response = api_calls.add_playlist("User1", "User1", "playlist")
    assert add_playlist_response.status_code == 200, f'Error: Adding playlist to user responded 200'
    add_song_to_playlist_response = api_calls.add_song_to_playlist("User1", "User1", "playlist", "song_name")
    assert add_song_to_playlist_response.status_code != 200, "Error: add song to playlist is 200 for an " \
                                                             "non nonexistent song"


@pytest.mark.playlist
@pytest.mark.song
@pytest.mark.xfail
@pytest.mark.parametrize(("song_genre", "song_year", "song_performer", "song_name"),
                         [("a", "1", "c", "d"),
                          ("bob", "1970", "reggae", "is this love")])
def test_add_same_song_twice_to_playlist(song_genre, song_year, song_performer, song_name, delete_songs, delete_users):
    assert delete_songs.status_code == 200, "Bad response"
    assert delete_users.status_code == 200, "Bad response"
    add_songs_response = api_calls.add_song(song_genre, song_year, song_performer, song_name)
    assert add_songs_response.status_code == 200, f"Error: add songs responded {add_songs_response.status_code}" \
                                                  f"for lligal input"
    add_user_response = api_calls.add_user("User1", "User1")
    assert add_user_response.status_code == 200, "Bad response"
    add_playlist_response = api_calls.add_playlist("User1", "User1", "playlist")
    assert add_playlist_response.status_code == 200, f'Error: Adding playlist to user responded 200'
    add_song_to_playlist_response = api_calls.add_song_to_playlist("User1", "User1", "playlist", song_name)
    assert add_song_to_playlist_response.status_code == 200, "Error: add song to playlist bad response for lligal input"
    second_add_song_to_playlist_response = api_calls.add_song_to_playlist("User1", "User1", "playlist", song_name)
    assert second_add_song_to_playlist_response.status_code != 200, "Error: add an nonexistent song to playlist" \
                                                                    "responded 200"


@pytest.mark.playlist
@pytest.mark.song
@pytest.mark.xfail
def test_add_empty_song_to_playlist(delete_songs, delete_users):
    assert delete_songs.status_code == 200, "Bad response"
    assert delete_users.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user("User1", "User1")
    assert add_user_response.status_code == 200, "Bad response"
    add_playlist_response = api_calls.add_playlist("User1", "User1", "playlist")
    assert add_playlist_response.status_code == 200, f'Error: Adding playlist to user responded 200'
    add_song_to_playlist_response = api_calls.add_song_to_playlist("User1", "User1", "playlist", "")
    assert add_song_to_playlist_response.status_code != 200, "Error: add empty song to playlist" \
                                                             " response is 200"


@pytest.mark.song
@pytest.mark.parametrize(("song_genre", "song_year", "song_performer", "song_name"),
                         [("a", "1", "c", "d"),
                          ("bob", "1970", "reggae", "is this love")])
def test_songs_rate_starts_zero(song_genre, song_year, song_performer, song_name, delete_songs):
    assert delete_songs.status_code == 200, f"Bad Response"
    add_songs_response = api_calls.add_song(song_genre, song_year, song_performer, song_name)
    assert add_songs_response.status_code == 200, f"Error: bad response"
    get_song_response = api_calls.get_song(song_name)
    assert get_song_response.status_code == 200, f"Error: bad response"
    json_format = json.loads(get_song_response.text)
    rate = json_format["data"]["rating"]
    assert rate == 0, f"Error: new song rate {rate} is different than zero"


@pytest.mark.song
@pytest.mark.parametrize(("user_name", "user_password", "playlist", "song_title"),
                         [("Tal", "Gabbay", "play1", "kashmir"),
                          ("George", "Bush", "reggae", "is this love")])
def test_songs_upvote(user_name, user_password, playlist, song_title, delete_songs, delete_users):
    assert delete_songs.status_code == 200, f"Bad Response"
    assert delete_users.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user(user_name, user_password)
    assert add_user_response.status_code == 200, "Bad response"
    add_songs_response = api_calls.add_song("song_genre", "song_year", "song_performer", song_title)
    assert add_songs_response.status_code == 200, f"Error: bad response"
    add_playlist_response = api_calls.add_playlist(user_name, user_password, playlist)
    assert add_playlist_response.status_code == 200, f'Error: Adding playlist to user responded 200'
    song_upvote_response = api_calls.song_upvote(user_name, user_password, playlist, song_title)
    assert song_upvote_response.status_code == 200, f"Error: song upvote response is not 200 for correct input"
    get_song_response = api_calls.get_song(song_title)
    assert get_song_response.status_code == 200, f"Error: bad response"
    json_format = json.loads(get_song_response.text)
    rate = json_format["data"]["rating"]
    assert rate == 1, f"Error: new song rate {rate} is different than one after exactly one vote"


@pytest.mark.song
@pytest.mark.xfail
@pytest.mark.parametrize(("user_name", "user_password", "playlist", "song_title"),
                         [("Tal", "Gabbay", "play1", "kashmir"),
                          ("George", "Bush", "reggae", "is this love")])
def test_songs_upvote_non_nonexistent_song(user_name, user_password, playlist, song_title, delete_songs, delete_users):
    assert delete_songs.status_code == 200, f"Bad Response"
    assert delete_users.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user(user_name, user_password)
    assert add_user_response.status_code == 200, "Bad response"
    add_playlist_response = api_calls.add_playlist(user_name, user_password, playlist)
    assert add_playlist_response.status_code == 200, f'Error: Adding playlist to user responded 200'
    song_upvote_response = api_calls.song_upvote(user_name, user_password, playlist, song_title)
    assert song_upvote_response.status_code != 200, f"Error: song upvote response 200 for non nonexistent song"


@pytest.mark.song
@pytest.mark.xfail
@pytest.mark.parametrize(("user_name", "user_password", "song_title"),
                         [("Tal", "Gabbay", "kashmir"),
                          ("George", "Bush", "is this love")])
def test_songs_upvote_not_on_playlist(user_name, user_password, song_title, delete_songs, delete_users):
    assert delete_songs.status_code == 200, f"Bad Response"
    assert delete_users.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user(user_name, user_password)
    assert add_user_response.status_code == 200, "Bad response"
    add_songs_response = api_calls.add_song("song_genre", "song_year", "song_performer", song_title)
    assert add_songs_response.status_code == 200, f"Error: bad response"
    song_upvote_response = api_calls.song_upvote(user_name, user_password, "", song_title)
    assert song_upvote_response.status_code != 200, f"Error: song upvote response is 200 although song is" \
                                                    f" not on any playlist"
    get_song_response = api_calls.get_song(song_title)
    assert get_song_response.status_code == 200, f"Error: bad response"
    json_format = json.loads(get_song_response.text)
    rate = json_format["data"]["rating"]
    assert rate == 0, f"Error: new song rate {rate} had been changed without being assigned to a playlist"


@pytest.mark.song
@pytest.mark.security
@pytest.mark.xfail
@pytest.mark.parametrize(("user_name", "user_password", "playlist", "song_title"),
                         [("Tal", "Gabbay", "play1", "kashmir"),
                          ("George", "Bush", "reggae", "is this love")])
def test_song_upvote_wrong_password(user_name, user_password, playlist, song_title, delete_songs, delete_users):
    assert delete_songs.status_code == 200, f"Bad Response"
    assert delete_users.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user(user_name, user_password)
    assert add_user_response.status_code == 200, "Bad response"
    add_songs_response = api_calls.add_song("song_genre", "song_year", "song_performer", song_title)
    assert add_songs_response.status_code == 200, f"Error: bad response"
    add_playlist_response = api_calls.add_playlist(user_name, user_password, playlist)
    assert add_playlist_response.status_code == 200, f'Error: Adding playlist to user responded 200'
    song_upvote_response = api_calls.song_upvote(user_name, "wrong_password", playlist, song_title)
    assert song_upvote_response.status_code != 200, f"Error: song upvote response 200 for voting " \
                                                    f"with incorrect password"
    get_song_response = api_calls.get_song(song_title)
    assert get_song_response.status_code == 200, f"Error: bad response"
    json_format = json.loads(get_song_response.text)
    rate = json_format["data"]["rating"]
    assert rate == 0, f"Error: new song rate {rate} change after upvote with incorrect password"


@pytest.mark.song
@pytest.mark.security
@pytest.mark.xfail
@pytest.mark.parametrize(("user_name", "user_password", "playlist", "song_title"),
                         [("Tal", "Gabbay", "play1", "kashmir"),
                          ("George", "Bush", "reggae", "is this love")])
def test_song_upvote_wrong_user_name(user_name, user_password, playlist, song_title, delete_songs, delete_users):
    assert delete_songs.status_code == 200, f"Bad Response"
    assert delete_users.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user(user_name, user_password)
    assert add_user_response.status_code == 200, "Bad response"
    add_songs_response = api_calls.add_song("song_genre", "song_year", "song_performer", song_title)
    assert add_songs_response.status_code == 200, f"Error: bad response"
    add_playlist_response = api_calls.add_playlist(user_name, user_password, playlist)
    assert add_playlist_response.status_code == 200, f'Error: Adding playlist to user responded 200'
    song_upvote_response = api_calls.song_upvote("wrong_user_name", user_password, playlist, song_title)
    assert song_upvote_response.status_code != 200, f"Error: song upvote response 200 for voting " \
                                                    f"with wrong_user_named"
    get_song_response = api_calls.get_song(song_title)
    assert get_song_response.status_code == 200, f"Error: bad response"
    json_format = json.loads(get_song_response.text)
    rate = json_format["data"]["rating"]
    assert rate == 0, f"Error: new song rate {rate} change after upvote with wrong_user_name"


@pytest.mark.song
@pytest.mark.xfail
@pytest.mark.parametrize(("user_name", "user_password", "playlist", "song_title"),
                         [("Tal", "Gabbay", "play1", "kashmir"),
                          ("George", "Bush", "reggae", "is this love")])
def test_songs_upvote_twice_same_user(user_name, user_password, playlist, song_title, delete_songs, delete_users):
    assert delete_songs.status_code == 200, f"Bad Response"
    assert delete_users.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user(user_name, user_password)
    assert add_user_response.status_code == 200, "Bad response"
    add_songs_response = api_calls.add_song("song_genre", "song_year", "song_performer", song_title)
    assert add_songs_response.status_code == 200, f"Error: bad response"
    add_playlist_response = api_calls.add_playlist(user_name, user_password, playlist)
    assert add_playlist_response.status_code == 200, f'Error: Adding playlist to user responded 200'
    song_upvote_response = api_calls.song_upvote(user_name, user_password, playlist, song_title)
    assert song_upvote_response.status_code == 200, f"Error: song upvote response is not 200 for correct input"
    second_song_upvote_response = api_calls.song_upvote(user_name, user_password, playlist, song_title)
    assert second_song_upvote_response.status_code != 200, f"Error: second song upvote with the same user response is" \
                                                           f" 200"
    get_song_response = api_calls.get_song(song_title)
    assert get_song_response.status_code == 200, f"Error: bad response"
    json_format = json.loads(get_song_response.text)
    rate = json_format["data"]["rating"]
    assert rate == 1, f"Error: new song rate {rate} had changed after voting for the second time with the same user"


@pytest.mark.song
@pytest.mark.parametrize(("user_name", "user_password", "playlist", "song_title"),
                         [("Tal", "Gabbay", "play1", "kashmir"),
                          ("George", "Bush", "reggae", "is this love")])
def test_songs_downvote(user_name, user_password, playlist, song_title, delete_songs, delete_users):
    assert delete_songs.status_code == 200, f"Bad Response"
    assert delete_users.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user(user_name, user_password)
    assert add_user_response.status_code == 200, "Bad response"
    add_songs_response = api_calls.add_song("song_genre", "song_year", "song_performer", song_title)
    assert add_songs_response.status_code == 200, f"Error: bad response"
    add_playlist_response = api_calls.add_playlist(user_name, user_password, playlist)
    assert add_playlist_response.status_code == 200, f'Error: Adding playlist to user responded 200'
    song_upvote_response = api_calls.song_upvote(user_name, user_password, playlist, song_title)
    assert song_upvote_response.status_code == 200, f"Error: song upvote response is not 200 for correct input"
    song_downvote_response = api_calls.song_downvote(user_name, user_password, playlist, song_title)
    assert song_downvote_response.status_code == 200, f"Error: song downvote response is not 200 for correct input"
    get_song_response = api_calls.get_song(song_title)
    assert get_song_response.status_code == 200, f"Error: bad response"
    json_format = json.loads(get_song_response.text)
    rate = json_format["data"]["rating"]
    assert rate == 0, f"Error: Initial rate had stayed the same after downvote function"


@pytest.mark.song
@pytest.mark.xfail
@pytest.mark.parametrize(("user_name", "user_password", "playlist", "song_title"),
                         [("Tal", "Gabbay", "play1", "kashmir"),
                          ("George", "Bush", "reggae", "is this love")])
def test_songs_downvote_to_sub_zero(user_name, user_password, playlist, song_title, delete_songs, delete_users):
    assert delete_songs.status_code == 200, f"Bad Response"
    assert delete_users.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user(user_name, user_password)
    assert add_user_response.status_code == 200, "Bad response"
    add_songs_response = api_calls.add_song("song_genre", "song_year", "song_performer", song_title)
    assert add_songs_response.status_code == 200, f"Error: bad response"
    add_playlist_response = api_calls.add_playlist(user_name, user_password, playlist)
    assert add_playlist_response.status_code == 200, f'Error: Adding playlist to user responded 200'
    song_downvote_response = api_calls.song_downvote(user_name, user_password, playlist, song_title)
    assert song_downvote_response.status_code != 200, f"Error: song downvote response is 200 for downvoting a " \
                                                      f"rate that is equal to zero"
    get_song_response = api_calls.get_song(song_title)
    assert get_song_response.status_code == 200, f"Error: bad response"
    json_format = json.loads(get_song_response.text)
    rate = json_format["data"]["rating"]
    assert rate == 0, f"Error: Initial rate zero had changed to {rate} after downvote function"

# endregion

# Mirror all the tests for upvote.... too much black work ):


@pytest.mark.song
@pytest.mark.parametrize(("user_name", "user_password", "playlist", "song_title"),
                         [("Tal", "Gabbay", "play1", "kashmir"),
                          ("George", "Bush", "reggae", "is this love")])
def test_get_songs_by_rank(user_name, user_password, playlist, song_title, delete_songs, delete_users):
    assert delete_songs.status_code == 200, f"Bad Response"
    assert delete_users.status_code == 200, "Bad response"
    add_user_response = api_calls.add_user(user_name, user_password)
    assert add_user_response.status_code == 200, "Bad response"
    add_playlist_response = api_calls.add_playlist(user_name, user_password, playlist)
    assert add_playlist_response.status_code == 200, f'Error: Adding playlist to user responded 200'
    for i in range(1, 11):
        song_name_i = f"{i}+{song_title}"
        add_songs_response = api_calls.add_song("song_genre", "song_year", "song_performer", song_name_i)
        assert add_songs_response.status_code == 200, f"Error: bad response"
        add_song_to_playlist_response = api_calls.add_song_to_playlist(user_name, user_password, playlist, song_name_i)
        assert add_song_to_playlist_response.status_code == 200, f"Error: fail to add song {song_name_i} to playlist"
    for i in range(1, 4):
        song_name_i = f"{i}+{song_title}"
        song_upvote_response = api_calls.song_upvote(user_name, user_password, playlist, song_name_i)
        assert song_upvote_response.status_code == 200, f"Error: song upvote response is not 200 for correct input"
        get_song_response = api_calls.get_song(song_name_i)
    get_songs_by_rank_response = api_calls.get_song_by_rank(0, "eq")
    json_format = json.loads(get_songs_by_rank_response.text)
    assert len(json_format["data"]) == 7
    get_songs_by_rank_response = api_calls.get_song_by_rank(0, "greater")
    json_format = json.loads(get_songs_by_rank_response.text)
    assert len(json_format["data"]) == 3
    get_songs_by_rank_response = api_calls.get_song_by_rank(1, "less")
    json_format = json.loads(get_songs_by_rank_response.text)
    assert len(json_format["data"]) == 7


