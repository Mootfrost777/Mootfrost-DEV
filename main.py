from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn
import requests
import threading
import time


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static/templates")

repos = []


def load_projects():
    while True:
        try:
            resp = requests.get("https://api.github.com/users/Mootfrost777/repos").json()
            global repos
            repos.clear()
            for repo in resp:
                repos.append(Project(repo["name"], repo["description"], repo["html_url"]))
        except Exception as e:
            print(e)
        time.sleep(7200)


class Project:
    name: str
    description: str
    url: str

    def __init__(self, name, description, url):
        self.name = name
        self.description = description
        self.url = url


@app.get("/api/get_repos")
def get_repos():
    return repos


@app.get("/")
def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about")
def main_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/projects")
def main_page(request: Request):
    return templates.TemplateResponse("projects.html", {"request": request})


threading.Thread(target=load_projects).start()
uvicorn.run(app)
