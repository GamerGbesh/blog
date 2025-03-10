from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import Content
import yt_dlp
import os
from pathlib import Path
import speech_recognition as sr



# Create your views here.
def home(request):
    blog = ""
    title = ""
    if request.method == "POST":
        url = request.POST.get("url")
        title, file = get_audio_title(url)
        blog = get_transcript(file)[0]
        Content(user=request.user, title=title, transcription=blog)
        Content.save()

    return render(request,"home.html", {"blog": blog, "title": title})


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return redirect("login")
    return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        form = forms.CustomUser(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username").lower()
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username.lower(), password=password)
            login(request, user)
            user = request.user
            return redirect("home")
        
    return render(request, "signup.html", {"form": forms.CustomUser})

def logout_user(request):
    logout(request)
    return redirect("home")

@login_required
def transcription(request):
    transcripts = Content.objects.filter(user=request.user)
    paginator = Paginator(transcripts, 10)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "transcription.html", {"page_obj": page_obj})


def get_audio_title(url):
    base_dir = Path(os.getcwd())
    download_folder = base_dir / "audios"
    if not download_folder.exists():
        download_folder.mkdir()
    ydl_opts = {
        "format":"bestaudio/best",
        "outtmpl":f"{download_folder}/output.%(ext)s",
        "postprocessors": [{
            "key":"FFmpegExtractAudio",
            "preferredcodec":"wav",
            "preferredquality": "192",
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        ydl.download([url])
    
    title = info["title"]
    file = download_folder / "output.wav"
    return title, file


def get_transcript(file):
    from key import CLIENT_KEY, CLIENT_ID
    gone = file
    file = str(file)
    r = sr.Recognizer()
    with sr.AudioFile(file) as src:
        audio_data = r.record(src)
        text = r.recognize_houndify(audio_data, CLIENT_ID, CLIENT_KEY)
    os.remove(gone)
    return text
    

def make_blog(text):
    pass
    