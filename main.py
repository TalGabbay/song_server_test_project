from logic_layer import api_calls
from src.logic_layer import helpers

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

print(r)
print(helpers.look_for_pattern("200", r))
