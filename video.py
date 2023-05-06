# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 10:51:28 2023
Modified on Thu May 6 2023
@author: Erdi YALÇIN
"""
# Yüklenecek olan kütüphaneler
# pip install moviepy
import os
import re
import traceback
import urllib.request
from moviepy.editor import VideoFileClip, AudioFileClip, VideoClip
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import threading
# Bu video regexi ile video urlsi kontrol edilecek ve doğruysa indirme işlemi başlayacak
VideoUrlRegex = re.compile(r'^https://[a-z0-9.-]+\.edu\.tr/playback/presentation/[\d.]+/[-a-zA-Z0-9]+-\d+$') # Video Url Regex 

def download_files():
    link = link_entry.get()

    try:
        # Video urlsi doğruysa indirme işlemi başlayacak
        if VideoUrlRegex.match(link) is None:
            messagebox.showerror("Invalid URL", "Geçersiz URL")
            return
        
        # Butonu kilitle ve kullanıcıya işlemin başladığını göster
        download_button.configure(state="disabled")
        download_button.update()
        
        # video ve ses dosya yollarının ayarlanması
        versiyon = "2.3/"
        url = link.replace("playback/", "").replace(versiyon, "")
        videoUrl = url + "/deskshare/deskshare.mp4"
        sesUrl = url + "/video/webcams.mp4"
        # Dosyaların indirilmesi ve kaydedilmesi
        urllib.request.urlretrieve(videoUrl, "video.mp4", report_hook)
        print("Video İndirildi")
        # Dosyaların indirilmesi ve kaydedilmesi
        urllib.request.urlretrieve(sesUrl, "ses.mp4", report_hook)
        print("Ses Dosyası İndirildi")

        messagebox.showinfo("Download Completed", "Dosyalar Başarıyla İndirildi")

        # Video dosyasını yükle
        video = VideoFileClip("video.mp4")
        # Ses dosyasını yükle
        ses = AudioFileClip("ses.mp4")

        print("Video Birleştiriliyor")
        # Video ve ses dosyalarını birleştir
        video_with_audio: VideoClip = video.set_audio(ses)
        print("Video Kaydediliyor")
        # Birleştirilmiş dosyayı kaydet
        save_file_path = filedialog.asksaveasfilename(defaultextension=".mp4")

        # Kullanıcıya işlemin başladığı bilgisini ver
        messagebox.showinfo(
            "Video İşlemi Başladı", "Video İşlemi Başladı Lütfen Bekleyiniz"
        )
        # progress barı sahte bir şekilde çalıştır ve kullanıcıya işlemin başladığını göster
        progress_bar.configure(mode="indeterminate")
        progress_bar.pack(pady=10)
        # daha hızlı bir şekilde ilerlemesi için progress barı başlat
        progress_bar.start(10)

        t = threading.Thread(
            target=write_file,
            args=(video_with_audio, save_file_path, video, ses), # İşlem parametreleri 
            daemon=True, # Arayüz kapatıldığında threadi sonlandır 
        ) # İşlemi başka bir threadde çalıştır ve arayüzün donmasını engelle 
        t.start() 

        # Videoyu kaydet

        # Kullanıcıya işlemin tamamlandığı bilgisini ver

    except:
        messagebox.showerror("Download Error", "Dosyaları İndirirken Bir Hata Oluştu")
        traceback.print_exc()  # Hata mesajını yazdırır ve hatanın nerede olduğunu gösterir
        download_button.configure(state="normal") # Butonu tekrar aktif hale getirir
        download_button.update() # Butonu tekrar aktif hale getirir
        

def write_file(video_file: VideoClip, save_file_path: str, video, ses):
    video_file.write_videofile(save_file_path,logger=None)
    progress_bar.stop()
    messagebox.showinfo(
        "Video İşlemi Tamamlandı",
        "Video İşlemi Tamamlandı Lütfen Kaydedilen Dosyayı Kontrol Ediniz",
    )
    print("Video Kaydedildi")
    # Dosyaları sil
    video.close()  # Video dosyasını kapatır
    ses.close()  # Ses dosyasını kapatır
    video_file.close()  # Birleştirilmiş dosyayı kapatır
    os.remove("video.mp4")  # Video dosyasını siler
    os.remove("ses.mp4")  # Ses dosyasını siler
    print("Geçici Dosyalar Silindi")
    progress_bar.configure(mode="determinate")
    progress_bar["value"] = 100
    root.update_idletasks()
    download_button.configure(state="normal")
    download_button.update()
    

def report_hook(count, block_size, total_size):
    progress = int(count * block_size * 100 / total_size)
    progress_bar["value"] = progress
    root.update_idletasks()


# Arayüzün oluşturulması ve ayarlanması
root = tk.Tk()  # Arayüzün oluşturulması
root.title("Video İndirici")  # Arayüzün başlığı
link_label = ttk.Label(root, text="Ders Linki:")  # Arayüzdeki yazı
link_label.pack(pady=5)  # Arayüzdeki yazının konumu
# Arayüzdeki yazı alanı
link_entry = ttk.Entry(root, width=50)  # Arayüzdeki yazı alanının boyutu ve konumu
link_entry.pack(pady=5)  # Arayüzdeki yazı alanının konumu

# Arayüzdeki buton ve konumu
download_button = ttk.Button(
    root, text="Dosyaları İndir", command=download_files
)  # Arayüzdeki butonun konumu ve komutu
download_button.pack(pady=10)  # Arayüzdeki butonun konumu

progress_bar = ttk.Progressbar(
    root, orient=tk.HORIZONTAL, length=300, mode="determinate"
)
progress_bar.pack(pady=10)

root.mainloop()  # Arayüzün çalıştırılması
