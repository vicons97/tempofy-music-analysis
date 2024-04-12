import requests
import pandas as pd

def main():
    #CREDENTIALS:
    # User ingres his Spotify ID to acces his info.
    user_id = input("Enter Spotify ID: ")
    print("ID is:", user_id)
    #validation token, re-fresh it every 3600s
    token = 'HERE YOU WILL PUT YOUR ATHORIZATION TOKEN' #ATUO TOKEN

    #Request playlist's IDs
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists?limit=20"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    #Making of request
    response = requests.get(url, headers=headers)

    #Storing playlist with respective IDs
    # Here we transform the info from all the playlists for a better visualization
    playlist = response.json()
    ids_names = [(item["name"], item["id"]) for item in playlist["items"]]

    # We convert it to a DataFrame with index starting from 1 for better visualization
    ids_namesDF = pd.DataFrame(ids_names, columns=["Name", "ID"]).rename_axis("Index").reset_index()
    ids_namesDF["Index"] += 1  # Adding 1 to the index

    print(ids_namesDF)

    #Select specific ID  a from playlist

    option = int(input('which list you wish to check?: '))
    id_playlist_selecc = ids_names[option - 1][1]

    #HERE WE REQUEST TRACK´S ID
    params = {
        'fields': 'items(track(name,href,id,album(name,href)))',
        'limit': 50,
        'offset': 0
    }

    url = f'https://api.spotify.com/v1/playlists/{id_playlist_selecc}/tracks'

    #Second request of resources
    response2 = requests.get(url, headers=headers, params=params)
    tracks_json = response2.json()

    #Validation of success in request
    if response2.status_code == 200:
        #Storing of tracks from the response2
        tracks = tracks_json['items']
        count = 0
        #for loop to print the list of tracks
        for track in tracks:
            track_name = track['track']['name']
            track_id = track['track']['id']
            album_name = track['track']['album']['name']
            count += 1
            print(count, track_name)
            #print('Track ID:', track_id)
            #print('Album Name:', album_name)
            #print('---')
    else:
        print('Error:', tracks_json['error'])

    #here we store all id's for each track for leater use
    #also here we store all track's name for later use
    tracks_ids = response2.json()
    store_ids_tracks = [(item['track']["id"]) for item in tracks_ids["items"]]
    store_name_tracks = [(item['track']["name"]) for item in tracks_ids["items"]]


    #here we make a small transformation of the data to be one stringe divided by comas
    ids_string = ",".join(store_ids_tracks)
    names_string = ",".join(store_name_tracks)

    #Here we request values of tempos for each track and then store them in a csv
    ids_string = ','.join(store_ids_tracks)
    params = {
        'ids': ids_string
    }

    url = 'https://api.spotify.com/v1/audio-features'

    #Third request of resources
    response3 = requests.get(url, headers=headers, params=params)
    response_json = response3.json()

    #Validation of succes in request
    if response3.status_code == 200:
        audio_features = response_json['audio_features']

        # Here we create a list of dicts with the values of the features of each track.
        data = []
        for i, feature in enumerate(audio_features):
            track_name = store_name_tracks[i]
            track_id = feature['id']
            danceability = feature['danceability']
            energy = feature['energy']
            valence = feature['valence']
            tempo = feature['tempo']

            data.append({
                'Track': track_name,
                'ID': track_id,
                'Danceability': danceability,
                'Energy': energy,
                'Valence': valence,
                'Tempo': tempo
            })

        # Create DF based on the dict.
        df = pd.DataFrame(data)

        # Saving of DF in CSV file
        df.to_csv('audio_features.csv', index=False)

        print('CSV saved.')
    else:
        print('Error:', response_json['error'])

if __name__ == "__main__":
    main()
