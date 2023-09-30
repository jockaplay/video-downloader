from pytube import YouTube
from pytube.exceptions import RegexMatchError
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.editor as mp
import re
import os
import sys
import platform
import tkinter as tk
import tkinter.ttk as ttk
import threading


output = open("output.txt", "wt")
sys.stdout = output
sys.stderr = output
titulo = ""
path = f'C:/Users/{os.getlogin()}/Downloads' if platform.system() == 'Windows' else f'/home/{os.environ.get("USER")}/Downloads'


def download_video(link):
    global titulo
    try:
        yt = YouTube(link)
        titulo = yt.title
        ys = yt.streams.filter(only_audio=True).first()
        ys.download(path)
        video.reactivate(True)
    except RegexMatchError:
        video.reactivate(False)


def aside_video(link):
    do_threading = threading.Thread(
        target=lambda: download_video(link), name="downloading_video")
    do_threading.start()


def download_music(link):
    global titulo
    try:
        yt = YouTube(link)
        ys = yt.streams.filter(only_audio=True).first()
        ys.download(path)
        for file in os.listdir(path):
            if re.search('mp4', file):
                mp4_path = os.path.join(path, file)
                mp3_path = os.path.join(path, os.path.splitext(file)[0]+'.mp3')
                new_file = mp.AudioFileClip(mp4_path)
                new_file.write_audiofile(mp3_path)
                titulo = yt.streams[0].default_filename
                musica.reactivate(True)
    except RegexMatchError:
        musica.reactivate(False)


def aside_music(link):
    do_threading = threading.Thread(
        target=lambda: download_music(link), name="downloading_music")
    do_threading.start()


app = tk.Tk()
app.title("Baixar vídeo")
app.geometry('400x220')
app.resizable(False, False)


class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        tk.Frame(self).pack(pady=20)
        label2 = tk.Label(self, text="Selecione o formato").pack(pady=[0, 25])
        videoBtn = tk.Button(self, relief='flat', text="Vídeo", width=50, bg="#e2e2e2",
                             activebackground="#c2c2c2", command=lambda: changeScreen(self, video))
        videoBtn.pack(pady=1)
        musicaBtn = tk.Button(self, relief='flat', text="Música", width=50, bg="#e2e2e2",
                              activebackground="#c2c2c2", command=lambda: changeScreen(self, musica))
        musicaBtn.pack(pady=1)


class VideoFrame(ttk.Frame):
    def __init__(self, container, formato):
        super().__init__(container)
        tk.Frame(self).pack(pady=5)
        label = tk.Label(self, text="Insira o link do vídeo:" if formato ==
                         "video" else "Insira o link do música:").pack()
        linkInput = tk.Entry(self, width=50, relief="flat")
        linkInput.pack(ipadx=28, ipady=5, pady=[25, 1])
        self.baixarBtn = tk.Button(self, relief='flat', text="Baixar", width=50,
                                   bg="#e2e2e2", activebackground="#c2c2c2", command=lambda: go())
        self.baixarBtn.pack(pady=[25, 1])
        voltarBtn = tk.Button(self, relief='flat', text="Voltar", width=50, bg="#e2e2e2",
                              activebackground="#c2c2c2", command=lambda: changeScreen(self, main))
        voltarBtn.pack(pady=1)
        self.finishedLabel = tk.Label(
            self, text=f"")
        self.finishedLabel.pack(pady=[5, 0])

        def go():
            self.baixarBtn["state"] = "disabled"
            aside_video(linkInput.get()) if formato == "video" else aside_music(
                linkInput.get())

    def reactivate(self, success):
        self.baixarBtn["state"] = "normal"
        if success:
            self.finishedLabel.config(text=f'{titulo}\nSalvo em: {path}')
        else:
            self.finishedLabel.config(text=f'Este link é inválido.')


def changeScreen(exit, enter):
    enter.pack(padx=10)
    exit.pack_forget()


video = VideoFrame(app, "video")
musica = VideoFrame(app, "musica")
main = MainFrame(app)
main.pack(padx=10)
app.mainloop()