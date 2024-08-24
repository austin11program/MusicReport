from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import requests

import urllib

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

REDIRECT_URI = "http://localhost:3000/musicreport"
AUTH_URL = "https://accounts.spotify.com/authorize"

userToken = ""


def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def authRequest():

            scope = 'user-read-private user-read-email user-top-read'
            params = {
                'client_id': client_id,
                'response_type': 'code',
                'scope': scope,
                'redirect_uri': REDIRECT_URI,
                'show_dialog': True
            }
            AUTH = "https://accounts.spotify.com/authorize"
            auth_url = f"{AUTH}?{urllib.parse.urlencode(params)}"
            return auth_url
   
def getToken(code):
    req_body ={
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri':REDIRECT_URI,
        'client_id':client_id,
        'client_secret':client_secret
    }
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    response = requests.post(TOKEN_URL, data = req_body)
    token_info = response.json()
    global userToken
    userToken = token_info["access_token"]
   

def myTopStats(type, timeRange):
    url = f"https://api.spotify.com/v1/me/top/{type}?time_range={timeRange}&limit=5"
    global userToken
    headers = {
        'Authorization': f"Bearer {userToken}"
    }
    result = get(url, headers=headers)
    itemList = result.json()
    return handleResult(type, itemList,timeRange)

def handleResult(type , itemList, timeRange):
    resultList = []
    if type == "tracks":
        for index, item in enumerate(itemList["items"]):
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
                            "albumId":albumId,
                            "order":(index+1),
                            "term":timeRange
                          }]
    elif type == 'artists':
        for index, item in enumerate(itemList["items"]):
            id = item["id"]
            name = item["name"]
            image = item['images'][0]['url']
            resultList += [{
                "id": id,
                "name":name,
                "image":image,
                "order":(index+1),
                "term":timeRange
            }]
    return(resultList)

def getUserProfile():
    url = f"https://api.spotify.com/v1/me"
    global userToken
    headers = {
        'Authorization': f"Bearer {userToken}"
    }
    result = get(url, headers=headers).json()
    
    largestImage = ''
    largestPixel = 0
    for image in result["images"]:
        if image["height"] > largestPixel:
            largestPixel=image["height"]
            largestImage=image['url']
    
    return {"displayName": result["display_name"], "image":largestImage, "email":result["email"], 'id':result["id"]}
