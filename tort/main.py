from typing import List
from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError
# import crud
import schemas
from models import ArtistPydantic, Artist, ArtistInPydantic, ArtistPydanticList, Album, AlbumPydantic

app = FastAPI()

@app.post('/')  # test
async def get_schemas():
    print(f"{ArtistPydantic.schema()}\n{'*'*20}")
    artist = await Artist.create(name="Queen", country="GB", active=True)
    artist_schema = await ArtistInPydantic.from_tortoise_orm(artist)
    print(artist_schema.json())
    return artist_schema.json()


@app.post('/test_create')  # test
async def create_users():
    await Artist.create(name="Queen", country="GB", active=True)
    await Artist.create(name="Beatles", country="GB", active=False)
    await Artist.create(name="Лещенко", country="Россия", active=True)
    artist_schema = await ArtistPydanticList.from_queryset(Artist.all())
    print(artist_schema.dict())
    print(artist_schema.json())
    return artist_schema.json()


@app.get("/", response_model=ArtistPydantic)  # test
async def get_users_list():
    artists = await ArtistPydantic.from_queryset_single(Artist.get(id=3))
    print(artists.json())
    return artists


@app.get("/artists", response_model=List[ArtistPydantic])
async def get_artists():
    return await ArtistPydantic.from_queryset(Artist.all())


@app.post("/artists", response_model=ArtistPydantic)
async def create_artist(artist: ArtistInPydantic):
    artist_obj = await Artist.create(**artist.dict(exclude_unset=True))
    return await ArtistPydantic.from_tortoise_orm(artist_obj)


@app.get(
    "/artist/{artist_id}", response_model=ArtistPydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_artist(artist_id: int):
    return await ArtistPydantic.from_queryset_single(Artist.get(id=artist_id))


@app.post(
    "/artist/{artist_id}", response_model=ArtistPydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_artist(artist_id: int, artist: ArtistInPydantic):
    await Artist.filter(id=artist_id).update(**artist.dict(exclude_unset=True))
    return await ArtistPydantic.from_queryset_single(Artist.get(id=artist_id))


@app.delete("/artist/{artist_id}", response_model=schemas.Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_artist(artist_id: int):
    deleted_count = await Artist.filter(id=artist_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Artist {artist_id} not found")
    return schemas.Status(message=f"Deleted artist {artist_id}")

register_tortoise(
    app,
    db_url="sqlite://sql_app.db",
    modules={"models": ["models"], "aerich.models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
