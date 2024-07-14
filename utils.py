from config import *
import requests as req
import base64

# print (SPOTIPY_CLIENT_ID)

# print(SPOTIPY_CLIENT_ID,    SPOTIPY_CLIENT_SECRET)


def get_tokens():
    url = "https://accounts.spotify.com/api/token"
    auth_str = SPOTIPY_CLIENT_ID + ":" + SPOTIPY_CLIENT_SECRET

    auth_b64 = base64.b64encode(
        auth_str.encode("utf-8")
    ).decode()  # encode the string to bytes and then decode it to string
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + auth_b64,
    }
    data = {"grant_type": "client_credentials"}
    response = req.post(url, headers=headers, data=data)
    # refresh token
    # print( response.json().get("refresh_token"))
    # later ill add refresh token logic with access token
    return response.json().get("access_token")


# testing the function
# print(get_tokens())
# token = get_tokens()


def get_playlist_info(playlist_id):
    # print("entered")
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    # should send the token in the header as a bearer token and playlist id in the data
    headers = {"Authorization": "Bearer " + get_tokens()}
    response = req.get(url, headers=headers)
    # limit of tracks is 100 so i need to use offset and next to get all tracks
    # print(response.json().get("tracks").get("items"))
    # print(response.json().get("tracks").get("next"))
    # print(response.json().get("tracks").get("offset"))

    data = {
        "id": response.json().get("id"),
        "uri": response.json().get("uri"),
        "name": response.json().get("name"),
        # "description": response.json().get("description"),
        # "followers": response.json().get("followers").get("total"),
        "public": response.json().get("public"),
        "type": response.json().get("type"),
        "collaborative": response.json().get("collaborative"),
        "total_tracks": response.json().get("tracks").get("total"),
        "tracks": response.json().get("tracks"),
        "owner": response.json().get("owner").get("display_name"),
        # "image": response.json().get("images")[0].get("url")
        # tracks infos with added by and track name and artist name
    }
    # limit and offset to get all tracks in the playlist by resending the request with offset and next
    limit = 100
    offset = 0
    # print(response.json()["tracks"]['next'])
    next_page = response.json()["tracks"]['next']
    while True:
        if next_page is None:
            break
        else:
            # got only tracks in the playlist not the whole playist info
            next_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={offset}&limit={limit}'
            response = req.get(next_url, headers=headers)
           
            # update next_page to check if there is more pages
            next_page = response.json()["next"]
            
            # print("*" * 50,'next')
            # # print(response.json()["items"])
            
            if next_page is not None:
                # print(next_page)
                # print(len(data["tracks"]["items"]))
                data["tracks"]["items"].extend(response.json()['items'])
            offset += limit
                # print(len(data["tracks"]["items"]))
                
                # print(len(response.json()["tracks"]["items"]))

    # get total of tracks in the playlist
    # print(response.json()['tracks']['total'])
    # print("last check "*50)
    # print(len(data["tracks"]["items"]))
    # print(data["name"])
    # print(len(data['tracks']['items']))
    return data

    # return response.json()
    # print(response.json())
    print("finished")


# print(
#     get_playlist_info("5HrFvEtqcGW1LEv0G7GWi2")
# )  # testing the function with black playlist id

# track infos : added_by , track_name , artist_name , track_id , track_uri , track_href


def get_user_info(user_id):
    url = f"https://api.spotify.com/v1/users/{user_id}"
    headers = {"Authorization": "Bearer " + get_tokens()}
    response = req.get(url, headers=headers)
    data = {
        "id": response.json().get("id"),
        "uri": response.json().get("uri"),
        "name": response.json().get("display_name"),
        "followers": response.json().get("followers").get("total"),
        "image": response.json().get("images")[0].get("url"),
    }
    return data
