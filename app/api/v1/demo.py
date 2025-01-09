from typing import Union, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.common.response import R

demo_router = APIRouter()


class Demo(BaseModel):
    id: Optional[int] = None
    name: str
    description: str


datas: list[Demo] = [Demo(id=1, name="Item1", description="This is the first item")]


@demo_router.get("/demo")
def get_demo():
    return {"Hello": "World"}


@demo_router.get("/demo/{id}")
def get(id: int):
    for data in datas:
        if data.id == id:
            return R.ok(data.dict())


@demo_router.post("/demo")
def create_demo(demo: Demo):
    demo.id = len(datas) + 1
    datas.append(demo)
    return R.ok(demo.dict())
