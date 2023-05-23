import tkinter as tk
import customtkinter as ctk
from pytube import YouTube
import requests
import API

result = []

# Functions
def startDownload():
    if link.get() == "":
        title.configure(text="Please Insert A Link")
        return
    try:
        ytObject = YouTube(link.get(), on_progress_callback=onProgress)
        video = ytObject.streams.get_highest_resolution()
        title.configure(text=ytObject.title)
        finishLabel.configure(text="")
        video.download()
        finishLabel.configure(text="Finished Downloading", text_color="green")
        link.delete(0, ctk.END)
    except:
        finishLabel.configure(text="Error Downloading", text_color="red")

def stopApp():
    app.destroy()

def onProgress(stream, chunk, bytes_remaining):
    size = stream.filesize
    bytesDownloaded = size - bytes_remaining
    percentageOfCompletion = bytesDownloaded / size * 100
    per = str(int(percentageOfCompletion))
    pPercentage.configure(text=per + "%")
    pPercentage.update()

    # Update Progress Bar
    progressBar.set(float(percentageOfCompletion) / 100)
    
def searchVideos():
    if link.get() == "":
        title.configure(text="Please Insert A Keyword")
        return
    url = "https://youtube-media-downloader.p.rapidapi.com/v2/search/videos"
    querystring = {"keyword":"","page":"1","limit":"10","type":"video"}
    headers = {
        "X-RapidAPI-Key": f"{API.apikey}",
        "X-RapidAPI-Host": "youtube-media-downloader.p.rapidapi.com"
    }
    querystring['keyword'] = link.get()
    response = requests.get(url, headers=headers, params=querystring)
    responseData = response.json().get('items')[:10]
    for res in responseData:
        result.append({'title': res.get('title'), 'url': "https://www.youtube.com/watch?v=" + res.get('id')})
    lst = []
    for res in result:
        lst.append(res.get('title')[:50])
    listMenu.configure(values=lst)
    listMenu.set("Select Video")

def optionMenu_callback(value):
    for res in result:
        if res.get('title')[:50] == value:
            link.delete(0, ctk.END)
            link.insert(0, res.get('url'))
            break

# System Settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# App Frame
app = ctk.CTk()
app.geometry("720x480")
app.title("YouTube Downloader")

# UI Elements
title = ctk.CTkLabel(app, text="Insert A Download Link", font=("Arial", 24))
title.pack(pady=10, padx=10)

# Link Input
url_var = tk.StringVar()
link = ctk.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack(pady=10, padx=10)
clear = ctk.CTkButton(app, text="Clear Input", width=100, height=40, command=lambda: link.delete(0, ctk.END))
clear.pack(pady=10, padx=10)

# Finished Downloading
finishLabel = ctk.CTkLabel(app, text="", font=("Arial", 24))
finishLabel.pack()

# Progress Bar
pPercentage = ctk.CTkLabel(app, text="0%", font=("Arial", 24))
pPercentage.pack()

progressBar = ctk.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(pady=10, padx=10)

# Search Button
search = ctk.CTkButton(app, text="Search", width=100, height=40, command=searchVideos)
search.pack(pady=10, padx=10)

# Search Result
listMenu = ctk.CTkOptionMenu(app, values=result, width=150, command=optionMenu_callback)
listMenu.set("Videos")
listMenu.pack(pady=10, padx=10)

# Download Button
download = ctk.CTkButton(app, text="Download", width=100, height=40, command=startDownload)
download.pack(pady=10, padx=1)

# Exit Button
exitButton = ctk.CTkButton(app, text="Exit", width=100, height=40, command=stopApp)
exitButton.pack(pady=10, padx=10)

# Run App
app.mainloop()