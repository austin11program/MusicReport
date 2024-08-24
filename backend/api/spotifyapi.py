from dotenv import load_dotenv
import os
import base64
from requests import post,get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
     
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_song( song_name, num):
    url = "https://api.spotify.com/v1/search"
    global token
    headers = get_auth_header(token)
    query = f"?q={song_name}&type=track&limit={num}"
    query_url = url + query
    result = get(query_url, headers = headers)
    
    itemList = json.loads(result.content)    
    resultList = getSongResultList(itemList, "byName")
    return resultList

def searchSongId(ids):
    stringQ = ""
    for id in ids:
        stringQ = stringQ + "," + id
    url = "https://api.spotify.com/v1/tracks"
    global token
    headers = get_auth_header(token)
    query = f"?ids={stringQ}"
    query_url = url+ query
    result = get(query_url, headers = headers)
   
    itemList = json.loads(result.content)
    resultList = getSongResultList(itemList, "byId")
    return resultList

def getSongResultList(itemList, type):
    resultList = [] 
    
    list = itemList["tracks"] if "byId" == type else itemList["tracks"]["items"]
    
    for item in list:
        if item == None: 
            continue
        trackId = item["id"]
        songName = item["name"]
        artistName = item["album"]["artists"][0]["name"]
        artistId = item["album"]["artists"][0]["id"]
        albumName = item["album"]["name"]
        coverUrls = []
        for photo in item["album"]["images"]:
            coverUrls += [photo["url"]]
        previewUrl = item["preview_url"]
        albumId = item["album"]["id"]
        resultList += [{ "id": trackId,
                          "songName": songName,
                          "artistName": artistName,
                          "artistId" : artistId,
                          "albumName": albumName,
                          "coverUrls": coverUrls,
                          "previewUrl": previewUrl,
                          "albumId":albumId }]
    return resultList

def search_for_album(album_name, num):
    url = "https://api.spotify.com/v1/search"
    global token
    headers = get_auth_header(token)
    query = f"?q={album_name}&type=album&limit={num}"
    query_url = url + query
    result = get(query_url, headers = headers)
    
    itemList = json.loads(result.content)["albums"]["items"];
    max = json.loads(result.content)["albums"]["total"];
    num = max if max < num else num
    resultList = []
    for i in range(num):
        albumId = itemList[i]["id"]
        totalTracks = itemList[i]["total_tracks"]
        cover = itemList[i]["images"][0]["url"]
        name = itemList[i]["name"]
        releaseDate =itemList[i]["release_date"]
        artistId = itemList[i]["artists"][0]["id"]
        resultList += [{
                        "id" :albumId,
                        "name":name,
                        "cover":cover,
                        "totalTracks":totalTracks,
                        "releaseDate":releaseDate,
                        "artistId": artistId}]
    return resultList

def search_for_albumId(id):
    query_url = "https://api.spotify.com/v1/albums/" + id
    global token
    headers = get_auth_header(token)
    result = get(query_url, headers = headers)
    itemList = json.loads(result.content)
    
    resultList = []
    resultList += [{
                    "albumId" : itemList["id"],
                    "totalTracks":itemList["total_tracks"],
                    "cover":itemList["images"][0]["url"] ,
                    "name":itemList["name"],
                    "releaseDate":itemList["release_date"],
                    "artistId":itemList["artists"][0]["id"]}]
    return resultList

def search_for_artist(artist_name, num):
    url = "https://api.spotify.com/v1/search"
    global token
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit={num}"
    query_url = url + query
    result = get(query_url, headers = headers)
    itemList = json.loads(result.content)["artists"]["items"]
    max = json.loads(result.content)["artists"]["total"]
    num = max if max < num else num
    resultList = []
    for i in range(num):
        id = itemList[i]["id"]
        name = itemList[i]["name"]
        image = itemList[i]["images"][0]["url"]
        rank = itemList[i]["popularity"]
        resultList += [{
                        "id" :id,
                        "name":name,
                        "image":image,
                        "popularity": rank}]
    return resultList

def search_for_artistId(id):
    query_url = "https://api.spotify.com/v1/artists/"+id
    global token
    headers = get_auth_header(token)
    result = get(query_url, headers = headers)
    itemList = json.loads(result.content)
    resultList = []
    resultList += [{
                    "id" : itemList["id"],
                    "name":itemList["name"],
                    "image":itemList["images"][0]["url"],
                    "popularity": itemList["popularity"]}]
    return resultList



token = get_token()



