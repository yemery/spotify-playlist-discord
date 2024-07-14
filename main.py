from db import get_db_connection
from utils import get_playlist_info

# import schedule
import pandas as pd


# checking if new tracks been added to any playlist in db
def check_new_tracks():
    try:
        db = get_db_connection()
        playlists = db["playlists"].find()
        for playlist in playlists:
            print("*" * 50)
            playlist_id = playlist.get("id")
            playlist_data = get_playlist_info(playlist_id)
            print(playlist_data.get("tracks").get("total"))
            print(playlist.get("tracks").get("total"))
            # if playlist_data.get("total_tracks") > playlist.get("total_tracks"):
                # using pandas to check if new tracks been added or track been removed
                # get items from both old and new playlist
                # items= playlist_data.get('tracks', {}).get('items', [])
                # for i in items:
                #     print(i.get('track').get('name'))
            old_tracks = pd.DataFrame(playlist.get("tracks", {}).get("items", []))
            new_tracks = pd.DataFrame(
                playlist_data.get("tracks", {}).get("items", [])
            )
            print(old_tracks)
            print(new_tracks)
            # indexing by name to compare the two dataframes its in track name level i'll use addded at till find optimizd sol to access to it directly in one line
            old_tracks.set_index(old_tracks['track'].apply(lambda x: x.get('id')), inplace=True)
            new_tracks.set_index(new_tracks['track'].apply(lambda x: x.get('id')), inplace=True)
            
            # check if new tracks been added or track been removed
            added = new_tracks[~new_tracks.index.isin(old_tracks.index)]
            removed = old_tracks[~old_tracks.index.isin(new_tracks.index)]
            print(added)
            print(removed)
            # limit of api is 100 songs well use offset and next to get all songs
            
            
            

            # # update the db with the new tracks
            # db["playlists"].update_one({"id": playlist_id}, {"$set": {"total_tracks": playlist_data.get("total_tracks")}})
            

    except Exception as e:
        print("Error in checking new tracks")
        print(e)


check_new_tracks()
