from infrastructure_layer import rest_functions


# User Handling Methods


def add_user(user_name, user_password):
    data = {
        "user_name": user_name,
        "user_password": user_password
    }
    response = rest_functions.post('/users/add_user', data)
    return response


def get_user(user_name):
    data = {
        "user_name": user_name
    }
    response = rest_functions.get('/users/get_user', data)
    return response


def add_friend(user_name, user_password, friend_name):
    data = {
        "user_name": user_name,
        "user_password": user_password,
        "friend_name": friend_name
    }
    response = rest_functions.put('/users/add_friend', data)
    return response


def add_playlist(user_name, user_password, playlist_name):
    data = {
        "user_name": user_name,
        "user_password": user_password,
        "playlist_name": playlist_name
    }
    response = rest_functions.post('/users/add_playlist', data)
    return response


def add_song(song_genre, song_year, song_performer, song_title):
    data = {
        "song_genre": song_genre,
        "song_year": song_year,
        "song_performer": song_performer,
        "song_title": song_title
    }
    response = rest_functions.post('/songs/add_song', data)
    return response


def get_song(song_title):
    data = {
        "song_title": song_title
    }
    response = rest_functions.get('/songs/get_song', data)
    return response


def song_upvote(user_name, user_password, playlist_name, song_title):
    data = {
        "user_name": user_name,
        "user_password": user_password,
        "playlist_name": playlist_name,
        "song_title": song_title
    }
    response = rest_functions.put('/songs/upvote', data)
    return response


def song_downvote(user_name, user_password, playlist_name, song_title):
    data = {
        "user_name": user_name,
        "user_password": user_password,
        "playlist_name": playlist_name,
        "song_title": song_title
    }
    response = rest_functions.put('/songs/downvote', data)
    return response


def add_song_to_playlist(user_name, user_password, playlist_name, song_title):
    data = {
        "user_name": user_name,
        "user_password": user_password,
        "playlist_name": playlist_name,
        "song_title": song_title
    }
    response = rest_functions.post('/playlists/add_song', data)
    return response


def get_playlist(user_name, user_password, playlist_name):
    data = {
        "user_name": user_name,
        "user_password": user_password,
        "playlist_name": playlist_name,
    }
    response = rest_functions.get('/users/get_playlist', data)
    return response


def get_song_by_rank(rank, op):
    data = {
        "rank": rank,
        "op": op
    }
    response = rest_functions.get('/songs/ranked_songs', data)
    return response


def change_user_password(user_name, user_password, user_new_password):
    data = {
        "user_name": user_name,
        "user_password": user_password,
        "user_new_password": user_new_password,
    }
    response = rest_functions.put('/users/change_password', data)
    return response


# Admin functions


def delete_all_users():
    response = rest_functions.delete('/admin/delete_all_users', "")
    return response


def delete_all_songs():
    response = rest_functions.delete('/admin/delete_all_songs', "")
    return response


def set_songs_into_the_db(song_list):
    response = rest_functions.post('/admin/set_songs', song_list)
    return response


def set_users_into_the_db(user_list):
    response = rest_functions.post('/admin/set_users', user_list)
    return response
