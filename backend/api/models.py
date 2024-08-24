from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import Signal



# Create your models here.

# Artist: 
# Album : Many to One (artist) ; 
# Track : Many to One (album) ; Many to One (artist)

class ArtistInfo(models.Model):
    id = models.CharField(max_length=100,primary_key=True)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    rank = models.IntegerField(null= True, blank= True)
    
    def __str__(self):
        return self.name

    def artistReport(self,report,term):
        rank = self.artistranking_set.filter(report=report, term=term).get()
        return { "name" : self.name, "image": self.image, "rank":rank.ordering, "term":term}

    
class AlbumInfo(models.Model):
    id = models.CharField(max_length=100,primary_key=True)
    name = models.CharField(max_length=100)
    cover = models.CharField(max_length=100)
    totalTracks = models.IntegerField()
    releaseDate = models.CharField(max_length=100)
    artistId = models.ForeignKey(ArtistInfo, null=True, blank=True,related_name='albums', on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class TrackInfo(models.Model):
    id = models.CharField(max_length=100,primary_key=True)
    songName = models.CharField(max_length=100)
    artistName = models.CharField(max_length=100)
    artistId = models.ForeignKey(ArtistInfo,null=True, blank=True,related_name='songs', on_delete=models.SET_NULL)
    albumName = models.CharField(max_length=100)
    coverUrls = models.JSONField(blank=True, null=True)
    previewUrl =models.CharField(max_length=100,blank=True, null=True)
    albumId = models.ForeignKey(AlbumInfo,null=True, blank=True,related_name='albums', on_delete=models.SET_NULL)

    def __str__(self):
        return self.songName
    
    def trackReport(self,report,term):
        rank = self.trackranking_set.filter(report=report, term=term).get()
        return { "name" : self.songName, "artist": self.artistName, "image": self.coverUrls[0], "rank":rank.ordering, "term":term}

class ReportDesign(models.Model):
    color = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    currentSongTerm = models.CharField(max_length=100)
    currentArtistTerm = models.CharField(max_length=100)
    image = models.CharField(max_length=100,null=True,blank=True)
    imagetext = models.CharField(max_length=100,null=True,blank=True)
    
    @property
    def data(self):
        return {"color":self.color, "name":self.name, "songTerm":self.currentSongTerm, "artistTerm":self.currentArtistTerm, "image":self.image, 'imagetext':self.imagetext}
    
class UserInfo(models.Model):
    displayName = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    id = models.CharField(max_length=100, primary_key=True)
    
class MusicReport(models.Model):
    belongsTo = models.ForeignKey(UserInfo, related_name="reports",null=True, on_delete=models.CASCADE)
    dateCreated = models.CharField(max_length=100,null = True)

    name = models.CharField(max_length=100)
    shortTermSongs = models.ManyToManyField('TrackInfo',related_name='sSongs', blank = True)
    mediumTermSongs = models.ManyToManyField('TrackInfo',related_name='mSongs', blank = True)
    longTermSongs = models.ManyToManyField('TrackInfo',related_name='lSongs', blank = True)
    shortTermArtists = models.ManyToManyField('ArtistInfo',related_name='sArtists', blank=True)
    mediumTermArtists = models.ManyToManyField('ArtistInfo',related_name='mArtists', blank=True)
    longTermArtists = models.ManyToManyField('ArtistInfo',related_name='lArtists', blank=True)
    
    design = models.OneToOneField(ReportDesign, on_delete=models.CASCADE)
    
    def songDisplay(self):
        songList = []
        long = [ song.trackReport(report=self,term="long_term") for song in self.longTermSongs.all()]
        medium = [ song.trackReport(report=self,term="medium_term") for song in self.mediumTermSongs.all()]
        short = [ song.trackReport(report=self,term="short_term") for song in self.shortTermSongs.all()]
        songList = short + medium + long
        return songList

    def artistDisplay(self):
        artistList = []
        long = [ artist.artistReport(report=self,term="long_term") for artist in self.longTermArtists.all()]
        medium = [ artist.artistReport(report=self,term="medium_term") for artist in self.mediumTermArtists.all()]
        short = [ artist.artistReport(report=self,term="short_term") for artist in self.shortTermArtists.all()]
        artistList = short + medium + long
        return artistList
     
class ArtistRanking(models.Model):
    ordering = models.IntegerField()
    term = models.CharField(max_length=100)
    report = models.ForeignKey(MusicReport, on_delete=models.CASCADE)
    artist= models.ForeignKey(ArtistInfo, on_delete=models.CASCADE)
    
class TrackRanking(models.Model):
    ordering = models.IntegerField()
    term = models.CharField(max_length=100)
    report = models.ForeignKey(MusicReport, on_delete=models.CASCADE)
    track = models.ForeignKey(TrackInfo, on_delete=models.CASCADE)


@receiver(post_save, sender=MusicReport)
def create_design(sender, instance, created, **kwargs):
    if created:
        design = ReportDesign.objects.create(
            color="orange",
            name=instance.name,
            currentSongTerm="short_term",
            currentArtistTerm="short_term",
        )
        # Associate the new design with the MusicReport instance
        instance.design = design
        instance.save()


def save_user_data(instance,name,userInfo):
    newReport = MusicReport(name=name)
    newReport.save()
    newReport.design.image = userInfo.image
    newReport.design.imagetext = userInfo.displayName
    newReport.design.save()
    newReport.belongsTo =userInfo
    newReport.dateCreated = instance.dateCreated
    newReport.shortTermArtists.set(instance.shortTermArtists.all())
    newReport.mediumTermArtists.set(instance.mediumTermArtists.all())
    newReport.longTermArtists.set(instance.longTermArtists.all())
    newReport.shortTermSongs.set(instance.shortTermSongs.all())
    newReport.mediumTermSongs.set(instance.mediumTermSongs.all())
    newReport.longTermSongs.set(instance.longTermSongs.all())
    newReport.save()
    return newReport
    


