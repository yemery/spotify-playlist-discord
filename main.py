from db import get_db_connection
from utils import get_playlist_info
# import schedule



# checking if new tracks been added to any playlist in db
def check_new_tracks():
    try:
        db = get_db_connection()
        playlists= db["playlists"].find()
        for playlist in playlists:
            playlist_id = playlist.get("id")
            playlist_data = get_playlist_info(playlist_id)
            if playlist_data.get("total_tracks") > playlist.get("total_tracks"):
                print(f"New tracks added to {playlist_data.get('name')} playlist")
                # update the db with the new tracks
                db["playlists"].update_one({"id": playlist_id}, {"$set": {"total_tracks": playlist_data.get("total_tracks")}})
            else:
                print(f"No new tracks added to {playlist_data.get('name')} playlist")
        
            
        
            
    except Exception as e:
        print("Error in checking new tracks")
        print(e)




check_new_tracks()