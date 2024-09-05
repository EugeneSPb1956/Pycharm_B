from tortoise import Tortoise, run_async
# from tort.app.models import *
from app.models import *

async def main():
    await Tortoise.init(
        # Здесь мы создаем ДБ SQLite DB - "db.sqlite3"
        db_url='sqlite://db.sqlite3',
        # Если модуль для моделей - __main__ то все модели для показа в нем
        # modules = {'models': ['__main__']},
        modules={'models': ['app.models']},
    )
    # Генерируем схемы
    await Tortoise.generate_schemas()


    artists = await Artists.get_or_none(id=1, name='Queen')
    print(artists, type(artists))
    if artists is not None:
        print('not none', artists, type(artists))
    else:
        print('none', artists, type(artists))
        artists = await Artists.create(
            name='Queen',
            country='GB',
            city='London',
            year1=1970,
            year2=1991,
        )

    print(artists.name)
    print(artists.name)

    albums = await Albums.create(
        title='Sheer Heart Attack',
        lable='EMI Elektra',
        release=1974,
        genre='Hard rock',
        price=499.99,
        artist='Queen',
        artists=artists,
    )

    # Получение объекта по полю
    artists = await Artists.get_or_none(id=1, name='Queen')
    print(artists)

    a_name = artists.name
    print(a_name)

    await Tortoise.close_connections()

if __name__ == '__main__':
    run_async(main())

