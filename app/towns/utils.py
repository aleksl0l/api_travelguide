from app.towns.models import Town


def map_town(town: Town) -> dict:
    return {
        'id_town': town.id_town,
        'name': town.name,
        'description': town.description,
        'url_photo': town.url_photo,
    }
