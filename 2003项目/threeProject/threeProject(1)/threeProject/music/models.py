from django.db import models


# Create your models here.
class Music(models.Model):
    music_name = models.CharField('歌曲', max_length=200)
    singer_name = models.CharField('歌手', max_length=200)
    play_url = models.CharField('播放链接', max_length=500)
    wyy_music_id = models.IntegerField('某云歌曲id', default=0)
