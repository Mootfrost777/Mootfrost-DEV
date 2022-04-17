from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn
import requests
import time
import asyncio

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static/templates")


def load_projects():
    print("Loading projects...")
    try:
        repos = requests.get("https://api.github.com/users/Mootfrost777/repos").json()
        res = []
        for repo in repos:
            res.append(Project(repo["name"], repo["description"], repo["html_url"]))
        return res
    except:
        print("Error loading projects. API request failed.")
        return Project('Error', 'Error', 'Error')


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
    return load_projects()


@app.get("/")
def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about")
def main_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/projects")
def main_page(request: Request):
    return templates.TemplateResponse("projects.html", {"request": request})


uvicorn.run(app)
