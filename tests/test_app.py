import unittest
import os

os.environ['TESTING'] = 'true'

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert '<title>Jacky Lin</title>' in html
        assert '<img src="./static/img/logo.jpg">' in html

    def test_timeline(self):
        response = self.client.get('/api/timeline_post')
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # add timeline
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@gmail.com",
                                                                "content": "Hello World! I'm John"})
        assert response.status_code == 200
        assert response.is_json

        response = self.client.get('/api/timeline_post')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        json = response.get_json()
        assert "John Doe" in html
        assert "john@gmail.com" in html
        assert "Hello World! I'm John" in html
        assert len(json["timeline_posts"]) == 1

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post",
                                    data={"email": "john@gmail.com", "content": "Hello World! I'm John"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        self.assertEqual("Invalid name", html)
        # assert "Invalid name" in html

        # POST request missing content
        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe", "email": "john@gmail.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request missing content
        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe", "email": "", "content": "Hello World! I'm John"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
