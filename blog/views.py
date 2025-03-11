from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from pathlib import Path
import yt_dlp
import os
import whisper
import ollama
import re

from . import forms
from .models import Content

def home(request):
    blog, title = "", ""

    if request.method == "POST":
        url = request.POST.get("url")
        if url:
            title, file = get_audio_title(url)
            transcript = get_transcript(file)
            blog = generate_blog(transcript)
            if request.user.is_authenticated:
                Content.objects.create(user=request.user, title=title, transcription=blog)

    return render(request,"home.html", {"blog": blog, "title": title})


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")
        return redirect("login")
    return render(request, "login.html")

def signup(request):
    form = forms.CustomUser(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        username = form.cleaned_data.get("username").lower()
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username.lower(), password=password)
        login(request, user)
        return redirect("home")
        
    return render(request, "signup.html", {"form": form})

def logout_user(request):
    logout(request)
    return redirect("home")

@login_required
def transcription(request):
    transcripts = Content.objects.filter(user=request.user).order_by("-created")
    paginator = Paginator(transcripts, 10)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    return render(request, "transcription.html", {"page_obj": page_obj})


@login_required
def blogs(request, id):
    blog = Content.objects.filter(user=request.user).get(id=id)
    return render(request, "blog.html", {"memo":blog})


def get_audio_title(url):
    base_dir = Path(os.getcwd())
    download_folder = base_dir / "audios"
    download_folder.mkdir(exist_ok=True)
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
        info = ydl.extract_info(url, download=True)
    
    title = info.get("title", "Unknown Title")
    file = download_folder / "output.wav"
    return title, file


def get_transcript(file):
    model = whisper.load_model("small")
    result = model.transcribe(str(file), verbose=True)
    os.remove(file)
    return result["text"]
    

def generate_blog(text):
    model = "deepseek-r1:latest"
    prompt = f"Make a very informative blog post about the following '{text}'."

    response = ollama.chat(model=model, messages=[{"role":"user", "content":prompt}])
    cleaned_text = re.split(r"<think>.+</think>", response["message"]["content"], flags=re.DOTALL)[1]
    cleaned_text = cleaned_text.replace("**", "").replace("###", "")
    return cleaned_text
    