from fastapi import FastAPI, Path
from typing_extensions import Annotated

from .models import Entity, Project

app = FastAPI()


class ProjectInput(Project):
    id: None = None


class EntityInput(Entity):
    id: None = None


@app.get("/projects/")
def list_project():
    return []


@app.post("/projects")
def create_project(obj: ProjectInput):
    return obj


@app.patch("/projects/{id}")
def patch_project():
    raise NotImplementedError()


@app.delete("/projects/{id}")
def delete_project():
    raise NotImplementedError()


@app.get("/projects/{project_id}/entities")
def list_entity():
    return []


@app.post("/projects/{project_id}/entities")
def create_entity(project_id: str, obj: EntityInput):
    return obj


@app.patch("/projects/{project_id}/entities/{entity_id}")
def patch_entity(project_id: str):
    raise NotImplementedError()


@app.delete("/projects/{project_id}/entities/{entity_id}")
def delete_entity(project_id: str, entity_id: str):
    raise NotImplementedError()
