from api.models import ArtistInfo, AlbumInfo, TrackInfo, MusicReport, ArtistRanking,TrackRanking,ReportDesign
from .spotifyapi import search_for_artistId, search_for_albumId
from .userSpotify import myTopStats

def fillArtist(resultList):
        # Populate the database
        modelList = []
        for artist_data in resultList:
            artist = ArtistInfo(
                id=artist_data.get("id"),
                name=artist_data.get("name"),
                image=artist_data.get("image"),
                rank = artist_data.get("popularity"),
                )
            artist.save()
            modelList.append(artist)
        return modelList
            
def createArtist(model_data):
        if len(ArtistInfo.objects.filter(id=model_data.get("artistId"))) == 0 :
            resultList = search_for_artistId(model_data.get("artistId"))
            for artist_data in resultList:
                artist = ArtistInfo(
                    id=artist_data.get("id"),
                    name=artist_data.get("name"),
                    image=artist_data.get("image"),
                    
                    ) 
                artist.save()
        return ArtistInfo.objects.filter(id=model_data.get("artistId")).first()
            
def fillAlbums(resultList):
        # Populate the database
        for album_data in resultList:
            Artist = createArtist(album_data)
            album = AlbumInfo(
                id=album_data.get("id"),
                name=album_data.get("name"),
                cover=album_data.get("cover"),
                totalTracks=album_data.get("totalTracks"),
                releaseDate = album_data.get("releaseDate"),
                artistId = Artist
                )
            album.save()
 
def createAlbum(model_data):
        if len(AlbumInfo.objects.filter(id=model_data.get("albumId"))) == 0 :
            resultList = search_for_albumId(model_data.get("albumId"))
            for album_data in resultList:
                    Artist = createArtist(album_data)
                    album = AlbumInfo(
                        id=album_data.get("id"),
                        name=album_data.get("name"),
                        cover=album_data.get("cover"),
                        totalTracks=album_data.get("totalTracks"),
                        releaseDate = album_data.get("releaseDate"),
                    
                        artistId = Artist
                    )
                    album.save()

        return AlbumInfo.objects.filter(id=model_data.get("albumId")).first()
    # trying to find matching alblum with the ablum object not string
    
def fillTracks(resultList):
        # Populate the database
        modelList =[]
        for track_data in resultList:
            Artist = createArtist(track_data)
            Album = createAlbum(track_data)
            
            if Album != None:
                track = TrackInfo(
                    id=track_data.get("id"),
                    songName=track_data.get("songName"),
                    artistName=track_data.get("artistName"),
                    artistId=Artist,
                    albumName=track_data.get("albumName"),
                    coverUrls = track_data.get("coverUrls"),
                    previewUrl = track_data.get("previewUrl"),
                    albumId = Album
                    )
            else: 
                track = TrackInfo(
                    id=track_data.get("id"),
                    songName=track_data.get("songName"),
                    artistName=track_data.get("artistName"),
                    artistId=Artist,
                    albumName=track_data.get("albumName"),
                    coverUrls = track_data.get("coverUrls"),
                    previewUrl = track_data.get("previewUrl"),
                    )
            track.save()
            modelList.append(track)
        return modelList
        

def fillMusicReport(card, artistList, songList, range):
    
    if(range == "short_term"):    
        card.shortTermSongs.set(fillTracks(songList))
        card.shortTermArtists.set(fillArtist(artistList))
        rankings = [
            ArtistRanking(report=card, artist=ArtistInfo.objects.get(id=artist['id']), ordering=artist["order"],term=artist["term"])
            for artist in artistList
        ]
        ArtistRanking.objects.bulk_create(rankings)
        rankings = [
            TrackRanking(report=card, track=TrackInfo.objects.get(id=song['id']), ordering=song["order"],term=song["term"])
            for song in songList
        ]
        TrackRanking.objects.bulk_create(rankings)        
    elif(range=="medium_term"):
        card.mediumTermSongs.set(fillTracks(songList))
        card.mediumTermArtists.set(fillArtist(artistList))
        rankings = [
            ArtistRanking(report=card, artist=ArtistInfo.objects.get(id=artist['id']), ordering=artist["order"],term=artist["term"])
            for artist in artistList
        ]
        ArtistRanking.objects.bulk_create(rankings)
        rankings = [
            TrackRanking(report=card, track=TrackInfo.objects.get(id=song['id']), ordering=song["order"],term=song["term"])
            for song in songList
        ]
        TrackRanking.objects.bulk_create(rankings)  
    else:
        card.longTermSongs.set(fillTracks(songList))
        card.longTermArtists.set(fillArtist(artistList))
        rankings = [
            ArtistRanking(report=card, artist=ArtistInfo.objects.get(id=artist['id']), ordering=artist["order"],term=artist["term"])
            for artist in artistList
        ]
        ArtistRanking.objects.bulk_create(rankings)
        rankings = [
            TrackRanking(report=card, track=TrackInfo.objects.get(id=song['id']), ordering=song["order"],term=song["term"])
            for song in songList
        ]
        TrackRanking.objects.bulk_create(rankings)  
    card.save()
    
    