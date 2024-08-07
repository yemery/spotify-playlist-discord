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
            new_tracks = pd.DataFrame(playlist_data.get("tracks", {}).get("items", []))
            print(old_tracks)
            print(new_tracks)
            # indexing by name to compare the two dataframes its in track name level i'll use addded at till find optimizd sol to access to it directly in one line
            old_tracks.set_index(
                old_tracks["track"].apply(lambda x: x.get("id")), inplace=True
            )  # lamda for each row in the dataframe to get the track id
            new_tracks.set_index(
                new_tracks["track"].apply(lambda x: x.get("id")), inplace=True
            )

            # check if new tracks been added or track been removed
            added = new_tracks[~new_tracks.index.isin(old_tracks.index)]
            removed = old_tracks[~old_tracks.index.isin(new_tracks.index)]

            if added is None:
                added_tracks = added.to_dict("records")
            if removed is None:
                removed_tracks = removed.to_dict("records")

            try:
                db["playlists"].update_one(
                {"id": playlist_id},
                {
                    "$set": {
                        "total_tracks": playlist_data.get("total_tracks"),
                        "tracks": playlist_data.get("tracks"),
                    }
                },
            )
                print("Playlist updated successfully")
            except Exception as e:
                print("Error in updating playlist")
                print(e)
        

            # print("added")
            # print(added)
            # # test converting dataframe to list of dicts
            # print("list of dict")
            # # print(added.values.tolist())
            # print(added.to_dict("records"))

            # print("removed")
            # print(removed)
            # limit of api is 100 songs well use offset and next to get all songs

            # # update the db with the new tracks
            # db["playlists"].update_one({"id": playlist_id}, {"$set": {"total_tracks": playlist_data.get("total_tracks")}})

    except Exception as e:
        print("Error in checking new tracks")
        print(e)


if __name__ == "__main__":
    check_new_tracks()
    # schedule.every(10).seconds.do(check_new_tracks)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
