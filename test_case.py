import pytest
import requests

URL = "https://poetrydb.org"


@pytest.mark.parametrize("param", [{ "endpoint": "author", "response": "{'authors': [", "code": 200 },
                                   { "endpoint": "title", "response": "{'titles': [", "code": 200 },
                                   { "endpoint": "invalid", "response": "Only author and title allowed.", "code": 200 }
])
def tests_poetry_author_and_title_endpoints(param):
    response = requests.get(f"{URL}/{param['endpoint']}")

    assert response.status_code == param["code"]
    assert param["response"] in str(response.json())


@pytest.mark.parametrize("param", [{ "author": "Alan Seeger", "response": "'author': 'Alan Seeger'", "code": 200 },
                                   { "author": "William Shakespeare", "response": "'author': 'William Shakespeare'", "code": 200 },
                                   { "author": "invalid", "response": "Not found", "code": 200 }
])
def tests_poetry_author_endpoint(param):
    response = requests.get(f"{URL}/author/{param['author']}")
    
    assert response.status_code == param["code"]
    assert param["response"] in str(response.json())


@pytest.mark.parametrize("param", [{ "title": '"All Is Vanity, Saith the Preacher"', "response": "'title': '\"All Is Vanity, Saith the Preacher\"'", "code": 200 },
                                   { "title": "Woods in Winter", "response": "'title': 'Woods in Winter'", "code": 200 },
                                   { "title": "invalid", "response": "Not found", "code": 200}
])
def tests_poetry_title_endpoint(param):
    response = requests.get(f"{URL}/title/{param['title']}")

    assert response.status_code == param["code"]
    assert param["response"] in str(response.json())


@pytest.mark.parametrize("param", [{ "author": "Ernest Dowson", "response": "[{'author': 'Ernest Dowson'}]", "code": 200 },
                                    { "author": "William Shakespeare", "response": "{'author': 'William Shakespeare'}", "code": 200 },
                                    { "author": "invalid", "response": "Not found", "code": 200 }
])
def tests_poetry_author_payload_response(param):
    response = requests.get(f"{URL}/author/{param['author']}:abs/author")

    assert response.status_code == param["code"]
    assert param["response"] in str(response.json())


@pytest.mark.parametrize("param", [{ "author": "Ernest Dowson", "response": "[{'title': \"The Moon Maiden's Song\", 'author': 'Ernest Dowson', 'linecount': '16'}]", "code": 200 },
                                   { "author": "Alan Seeger", "response": "{'title': 'I Have A Rendezvous With Death', 'author': 'Alan Seeger', 'linecount': '24'}", "code": 200 },
                                   { "author": "invalid", "response": "Not found", "code": 200 }
])
def tests_poetry_author_title_linecount(param):
    response = requests.get(f"{URL}/author/{param['author']}/author,title,linecount")

    assert response.status_code == param["code"]
    assert param["response"] in str(response.json())


@pytest.mark.parametrize("param", [{ "author": "Ernest Dowson", "response": "title\nThe Moon Maiden's Song\nauthor\nErnest Dowson\nlinecount\n16", "code": 200 },
                                   { "author": "Alan Seeger", "response": "title\nI Have A Rendezvous With Death\nauthor\nAlan Seeger\nlinecount\n24", "code": 200 },
                                   { "author": "invalid", "response": "Not found", "code": 200 }
])
def tests_poetry_author_title_linecount_text(param):
    response = requests.get(f"{URL}/author/{param['author']}/author,title,linecount.text")

    assert response.status_code == param["code"]
    assert param["response"] in str(response.text)
