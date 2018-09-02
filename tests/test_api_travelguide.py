import os
import tempfile
import urllib.parse

import pytest

from app import app as travelguide


@pytest.fixture
def client():
    db_fd, travelguide.app.config['DATABASE'] = tempfile.mkstemp()
    travelguide.app.config['TESTING'] = True
    # travelguide.app.config[]
    client = travelguide.app.test_client()

    # with travelguide.app.app_context():
    #     travelguide.init_db()

    yield client

    os.close(db_fd)
    os.unlink(travelguide.app.config['DATABASE'])


def test_get_towns(client):
    rv = client.get('/api_v1.0/get_towns')
    assert rv.status_code == 200

# def test_post_towns(client):
#     params = {"name": "Testing2"}
#     url = '/api_v1.0/create_town?' + urllib.parse.urlencode(params)
#     rv = client.post(url)
#     assert rv.status_code == 201
