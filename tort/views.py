from tortoise import Tortoise, run_async
# from tort.app.models import *
from app.models import *

async def get_data():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']},
    )

    await Tortoise.generate_schemas()

    artists = await Artists.get_or_none()[1:2]
    print(type(artists))
    print(artists.name, artists.year1, artists.year2, artists.country, artists.city)

    albums = await Albums.get_or_none()[0:1]
    print(albums.title, albums.release, albums.genre)

run_async(get_data())