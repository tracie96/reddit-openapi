import requests

def test_get_news_check_status_code_equals_200():
    response = requests.get("http://127.0.0.1:8000/news")
    assert response.status_code == 200

def test_get_query_endpoint():
    response = requests.get("http://127.0.0.1:8000/news?query=bitcoin")
    assert response.status_code == 200


def test_get_content_type_equals_json():
    response = requests.get("http://127.0.0.1:8000/news")
    assert response.headers["Content-Type"] == "application/json"

def test_check_if_value_contain_bitcoin():
    response = requests.get("http://127.0.0.1:8000/news/?query=bitcoin")
    print(response.json())
    for res in response.json():
        assert "bitcoin" in res['headline']