from src.logic_layer import api_calls
import json
import re

api_calls.add_user('Tal Gabbay', 'tg')
r = api_calls.get_user('Tal Gabbay')

# api_calls.add_friend('Tal Gabbay', 'tg', 'Adam')
# api_calls.add_playlist('Tal Gabbay', 'tg', 'summer vibes')
# api_calls.add_song("Regge", '1970', "Bob Marly", "One Love")
# api_calls.get_song("One Love")
# api_calls.song_upvote('Tal Gabbay', 'tg', 'summer vibes', 'One Love')
# api_calls.song_downvote('Tal Gabbay', 'tg', 'summer vibes', 'One Love')
# api_calls.get_song("One Love")
# api_calls.add_song_to_playlist('Tal Gabbay', 'tg', 'summer vibes', 'One Love')
# api_calls.get_playlist('Tal Gabbay', 'tg', 'summer vibes')
# api_calls.get_song_by_rank('0', 'eq')
# api_calls.change_user_password('Tal Gabbay', '0', 'tg')
# api_calls.delete_all_songs()
# r1 = api_calls.delete_all_users()
# api_calls.set_songs_into_the_db()
# api_calls.set_users_into_the_db()




playlist = "ff"


def t_add_playlist(playlist):
    add_user_response = api_calls.add_user("User1", "User1")
    get_user_response = api_calls.get_user("User1")
    add_playlist_response = api_calls.add_friend("User1", "User1", playlist)
    json_format = json.loads(get_user_response.text)
    print(json_format["data"]["friends"][0])



t_add_playlist(playlist)