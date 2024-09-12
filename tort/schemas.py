from typing import List
from pydantic import BaseModel
from tortoise.contrib.pydantic.base import PydanticModel, PydanticListModel


class AlbumBase(PydanticModel):
    title: str
    lable: str = None
    release: int
    genre: str = None
    price: int


class AlbumCreate(AlbumBase):
    pass


class Album(AlbumBase):
    id: int
    art: int

    class Config:
        orm_mode = True


class ArtistBase(PydanticModel):
    name: str
    country: str = None
    city: str = None
    year1: int
    year2: int


class ArtistCreate(ArtistBase):
    active: bool = True

    class Config:
        orm_mode = True


class ArtistInDB(ArtistBase):
    id: int


class Artist(ArtistBase):
    id: int
    albums: List[Album] = []

    class Config:
        orm_mode = True


class AlbumUser(AlbumBase):
    id: int
    art: ArtistInDB


class Status(BaseModel):
    message: str