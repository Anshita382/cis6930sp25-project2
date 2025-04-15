import requests

def test_coref_api():
    url = "http://gpu002.cm.cluster:65535/resolve_coref"
    text = "John said he would help Mary. She was grateful."
    response = requests.post(url, headers={"Content-Type": "application/json"}, json={"text": text})
    data = response.json()

    assert "coreference_mapping" in data
    assert isinstance(data["coreference_mapping"], list)
