from .models import TrackInfo, ArtistInfo, AlbumInfo, MusicReport, ArtistRanking, TrackRanking,ReportDesign, save_user_data,UserInfo

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from time import gmtime, strftime
from django.shortcuts import render
from django.db import connections
from django.db.utils import OperationalError


from .populateDatabase import fillMusicReport
from .spotifyapi import search_for_artist,search_for_album, search_for_song
from .userSpotify import authRequest, myTopStats, getToken,getUserProfile

# Create your views here
# source venv/bin/activate
    
def login(request):
    try:
        auth_url = authRequest() 
        return JsonResponse({'auth_url': auth_url}) 
    except Exception as e:
        print(f"Error in login view: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
def getTokenEnd(request):
    try:
        code = request.GET.get('code')
        if code:
            getToken(code)
            return JsonResponse({'success': True, 'status_code': 200})
        else:
            return JsonResponse({'error': 'No code provided'}, status=400)
    except Exception as e:
        print(f"Error in getTokenEnd view: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def getStats(request):
    if request.method == 'GET':
        userResult = getUserProfile()
        try:
            UserData = UserInfo.objects.get(id=userResult["id"])
        except UserInfo.DoesNotExist:
            UserData = UserInfo(displayName=userResult["displayName"],
                            image=userResult["image"],
                            email=userResult["email"],
                            id=userResult["id"],
                            demo='user')
            UserData.save()
            
        name = UserData.id + "_USER_DATA%"
        try:
            card = MusicReport.objects.filter(demo="user").get(name=name, dateCreated=strftime("%Y-%m-%d", gmtime()))
        except MusicReport.DoesNotExist:
            card = MusicReport(name=name)
            card.save()
            card.design.image = UserData.image
            card.design.imagetext = UserData.displayName
            card.design.save()
            card.belongsTo = UserData
            card.dateCreated = strftime("%Y-%m-%d", gmtime())
            card.demo="user"
            longTermSongs = myTopStats("tracks", "long_term")
            longTermArtists = myTopStats("artists", "long_term")
            fillMusicReport(card, longTermArtists, longTermSongs, "long_term")
            mediumTermSongs = myTopStats("tracks", "medium_term")
            mediumTermArtists = myTopStats("artists", "medium_term")
            fillMusicReport(card, mediumTermArtists, mediumTermSongs, "medium_term")
            shortTermSongs = myTopStats("tracks", "short_term")
            shortTermArtists = myTopStats("artists", "short_term")
            fillMusicReport(card, shortTermArtists, shortTermSongs, "short_term")
            card.save()
        
        currentName = request.GET.get("name")
        try:
            MusicReport.objects.filter(demo="user").get(name=currentName)
        except MusicReport.DoesNotExist:
            save_user_data(card,currentName,UserData,"demo") 
        
        artistData = card.artistDisplay()
        songData = card.songDisplay()
        return JsonResponse({'success': 200, "name": currentName, "artists": artistData, "songs": songData, "userId":UserData.id})
   
    return JsonResponse({'error': 'No code provided'}, status=400)


def setSongRange(request):
    if request.method == 'GET':
        range = request.GET.get("range")
        name = request.GET.get("name")
        id = request.GET.get("userId")
        demo = request.GET.get("demo")
        card = MusicReport.objects.filter(demo=demo).get(name=name,belongsTo__id=id)
        card.design.currentSongTerm = range
        card.design.save()
        
        dataCard = MusicReport.objects.filter(demo=demo).filter(name=id+"_USER_DATA%").filter(dateCreated=strftime("%Y-%m-%d", gmtime())).first()
        checkimagetext(dataCard, card.design.image, card,range, "songs")
        
        return JsonResponse({'success': 200, 'design':card.design.data})
    return JsonResponse({'error': 500})  


# copy over the funcaitonlay for all the other stuff
def checkimagetext(dataCard, image,card,term,type): # image is current one
    found = False
    if(type == "songs"):
        if term == "long_term":
            for song in dataCard.longTermSongs.all():
                if song.songName == card.design.image :
                    return
        elif term == "medium_term":
            for song in dataCard.mediumTermSongs.all():
                if song.songName == card.design.image :
                    return
        else: 
            for song in dataCard.shortTermSongs.all():
                if song.songName == card.design.image :
                    return
        targetSong = dataCard.trackranking_set.all().filter(term=term).order_by('ordering').first().track
        card.design.image = targetSong.coverUrls[0]
        card.design.imagetext = targetSong.songName
        card.design.save()
    else:
        if term == "long_term":
            for artist in dataCard.mediumTermArtists.all():
                if artist.name == card.design.image :
                    return
        elif term == "medium_term":
            for artist in dataCard.mediumTermArtists.all():
                if artist.name == card.design.image :
                    return
        else: 
            for artist in dataCard.shortTermArtists.all():
                if artist.name == card.design.image :
                    return
        targetArtist = dataCard.artistranking_set.all().filter(term=term).order_by('ordering').first().artist
        card.design.image = targetArtist.image
        card.design.imagetext = targetArtist.name
        card.design.save()

def setArtistRange(request):
    if request.method == 'GET':
        range = request.GET.get("range")
        name = request.GET.get("name")
        id = request.GET.get("userId")
        demo = request.GET.get("demo")
        card = MusicReport.objects.filter(demo=demo).get(name=name,belongsTo__id=id)
        card.design.currentArtistTerm = range
        card.design.save()
        
        dataCard = MusicReport.objects.filter(demo=demo).filter(name=id+"_USER_DATA%").filter(dateCreated=strftime("%Y-%m-%d", gmtime())).first()
        checkimagetext(dataCard, card.design.image, card,range, "artists")
        
        return JsonResponse({'success': 200})
    return JsonResponse({'error': 500}) 

def getResults(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        id = request.GET.get("userId")
        demo = request.GET.get("demo")
        queryResult = MusicReport.objects.filter(demo=demo).filter(name__icontains=name,belongsTo__id=id).exclude(name__endswith="_USER_DATA%")[:10]
        result = [{"name":query.name} for query in queryResult]
        return JsonResponse({'success': 200,'results':result})  
    return JsonResponse({'error': 500})  

def getCard(request):
    if request.method == 'GET':
        demoMode = request.GET.get("demo") == 'true'
        dbAlias = 'demo' if demoMode else 'default'
        name = request.GET.get("name")
        user_id = request.GET.get("userId")
        demo=request.GET.get('demo')
        try:
                card = MusicReport.objects.filter(demo=demo).get(name=name, belongsTo__id=user_id)
                return JsonResponse({
                    'success': 200,
                    'name': card.name,
                    'design': card.design.data,
                    'artistTime': card.design.currentArtistTerm,
                    'songTime': card.design.currentSongTerm
                })
        except MusicReport.DoesNotExist:
            return JsonResponse({'error': 500})
        except OperationalError:
            return JsonResponse({'error': 500, 'message': 'Database error'})
        
    return JsonResponse({'error': 405, 'message': 'Method not allowed'})
        
        
def deleteCurrentCard(request):
    if request.method == 'GET':
        demo = request.GET.get("demo")
        if(MusicReport.objects.filter(demo=demo).exclude(name__endswith="_USER_DATA%").count() == 1):
            return JsonResponse({'error': 400})  
        name = request.GET.get("name")
        id = request.GET.get("userId")
        card = MusicReport.objects.filter(demo=demo).exclude(name=name,belongsTo__id=id).exclude(name__endswith="_USER_DATA%").first()
        try:
            MusicReport.objects.filter(demo=demo).exclude(name__endswith="_USER_DATA%").get(name=name,belongsTo__id=id).design.delete()
        except MusicReport.DoesNotExist:
            return JsonResponse({'error': 500})  

        return JsonResponse({'success': 200, 'name':card.name, 'design':card.design.data, 'artistTime':card.design.currentArtistTerm, 'songTime':card.design.currentSongTerm})
    return JsonResponse({'error': 500})  

def createNewCard(request):
    if request.method == 'GET':
        name = request.GET.get("name")
        id = request.GET.get("userId")
        demo = request.GET.get("demo")
        if not name or not name.strip():
            return JsonResponse({'error': 'Name is required'}, status=400)
        try:
            MusicReport.objects.filter(demo=demo).get(name=name,belongsTo__id=id)
            return JsonResponse({'error': 500, 'name already exist':400})
        except MusicReport.DoesNotExist:
            pass
    
        userDataModel = MusicReport.objects.filter(demo=demo).get(name=id+"_USER_DATA%", dateCreated=strftime("%Y-%m-%d", gmtime()))
        UserData = UserInfo.objects.get(id=id)
        card = save_user_data(userDataModel, name,UserData, "user")

        return JsonResponse({'success': 200, 'name':card.name, 'design':card.design.data, 'artistTime':card.design.currentArtistTerm, 'songTime':card.design.currentSongTerm})
    return JsonResponse({'error': 500})  

def getimageresults(request):
    if request.method == 'GET':
        
        name = request.GET.get("name")
        id = request.GET.get("userId")
        songRange = request.GET.get("songRange")
        artistRange = request.GET.get("artistRange")
        demo = request.GET.get("demo")
        
        currentReport = MusicReport.objects.filter(demo=demo).get(name=name,belongsTo__id=id)
        results =[]
        if songRange =="short_term":
            results = [{"id": song.id, "image": song.coverUrls[0], "type":"songs"} for song in currentReport.shortTermSongs.all()]
        elif songRange =="medium_term":
            results = [{"id": song.id, "image": song.coverUrls[0], "type":"songs"} for song in currentReport.mediumTermSongs.all()]
        else:
            results = [{"id": song.id, "image": song.coverUrls[0], "type":"songs"} for song in currentReport.longTermSongs.all()]

        if artistRange =="short_term":
            results +=[{"id": artist.id, "image": artist.image, "type":"artists"} for artist in currentReport.shortTermArtists.all()]
        elif artistRange =="medium_term":
            results += [{"id": artist.id, "image": artist.image, "type":"artists"} for artist in currentReport.mediumTermArtists.all()]
        else:
            results += [{"id": artist.id, "image": artist.image, "type":"artists"} for artist in currentReport.longTermArtists.all()]
    
        userInfo = currentReport.belongsTo
        results += [{"id": userInfo.id, "image": userInfo.image, "type":"user"}]
        
        return JsonResponse({'success': 200, "data":results})
    return JsonResponse({'error': 500})  

def setdesignimage(request):
    if request.method == "GET":
        type = request.GET.get("type")
        id = request.GET.get("id")
        name = request.GET.get("name")
        userId = request.GET.get("userId")
        demo = request.GET.get("demo")

        targetImage = ""
        targetName = ""
        if type == 'songs':
            targetQuery = TrackInfo.objects.get(id=id)
            targetImage = targetQuery.coverUrls[0]
            targetName = "Personal favorite " + targetQuery.songName
        elif type == "artists":
            targetQuery = ArtistInfo.objects.get(id=id)
            targetImage = targetQuery.image
            targetName = "Personal favorite " + targetQuery.name
        else:
            targetQuery = UserInfo.objects.get(id=id)
            targetImage = targetQuery.image
            targetName = targetQuery.displayName
        
        targetDesign = MusicReport.objects.filter(demo=demo).get(name=name,belongsTo__id=userId).design
        targetDesign.image = targetImage
        targetDesign.imagetext = targetName
        targetDesign.save()
        return JsonResponse({'success': 200, 'design':targetDesign.data, "image":targetDesign.image})
    return JsonResponse({'error': 500})  

def deleteAll(request):
    ArtistInfo.objects.all().delete()
    TrackInfo.objects.all().delete()
    MusicReport.objects.all().delete()
    AlbumInfo.objects.all().delete()
    ArtistRanking.objects.all().delete()
    TrackRanking.objects.all().delete()
    ReportDesign.objects.all().delete()
    UserInfo.objects.all().delete()
    return JsonResponse({'success': 200})  


def backend_server_view(request):
    return render(request, 'index.html')

