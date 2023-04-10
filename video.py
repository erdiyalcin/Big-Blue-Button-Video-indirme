# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 10:51:28 2023

@author: Erdi YALÇIN
"""
# Yüklenecek olan kütüphaneler
# pip install moviepy
import urllib.request
from moviepy.editor import VideoFileClip, AudioFileClip


link = "https://-----------/playback/presentation/2.3/------------------------------------------------"
dersinAdi = 'Python'
dersinHaftasi = "1"

#video ve ses dosya yollarının ayarlanması
versiyon = "2.3/"
url = link.replace("playback/","").replace(versiyon,"")
videoUrl = url + '/deskshare/deskshare.mp4'
sesUrl = url + '/video/webcams.mp4'


urllib.request.urlretrieve(videoUrl, 'video.mp4')
print("Video İndirildi")

urllib.request.urlretrieve(sesUrl, 'ses.mp4')
print("Ses Dosyası İndirildi")

# Video dosyasını yükle
video = VideoFileClip("video.mp4")
# Ses dosyasını yükle
ses = AudioFileClip("ses.mp4")

print("Video Birleştiriliyor")
# Video ve ses dosyalarını birleştir
video_with_audio = video.set_audio(ses)
print("Video Kaydediliyor")
# Birleştirilmiş dosyayı kaydet
video_with_audio.write_videofile(dersinAdi + "_" + dersinHaftasi + ".mp4")
print("Video Birleştirildi")
