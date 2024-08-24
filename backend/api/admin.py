from django.contrib import admin
from .models import TrackInfo,AlbumInfo,ArtistInfo, MusicReport,ArtistRanking, TrackRanking, ReportDesign, UserInfo

# Register your models here.

@admin.register(TrackInfo)
class TrackInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'songName', 'artistName', 'artistId', 'albumName','coverUrls','previewUrl',"albumId")
    list_filter = (['albumName'])
    search_fields = ('songName','artistName')
    
@admin.register(AlbumInfo)
class AlbumInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cover', 'totalTracks','releaseDate',"artistId")
    search_fields = (["name"])
    
@admin.register(ArtistInfo)
class ArtistInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image','rank')
    search_fields = (["name"])

    
@admin.register(MusicReport)
class MusicReportAdmin(admin.ModelAdmin):
    list_display=(['name','belongsTo','dateCreated'])
    
@admin.register(ArtistRanking)
class ArtistRankingAdmin(admin.ModelAdmin):
    list_display=(['ordering','term','report','artist'])
    
@admin.register(TrackRanking)
class TrackRankingAdmin(admin.ModelAdmin):
    list_display=(['ordering','term','report','track'])   
    
@admin.register(ReportDesign)
class ReportDesignAdmin(admin.ModelAdmin):
    list_display=(['color','name','imagetext', 'image', 'currentSongTerm','currentArtistTerm'])   
    
@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display=(['displayName','image','email','id'])   