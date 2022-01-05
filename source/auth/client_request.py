import requests

data = {
    'key': 'value',
}
r = requests.post('http://0.0.0.0:13451/vote', json=data)
