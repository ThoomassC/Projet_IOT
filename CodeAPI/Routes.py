import requests

def post_Datas():
    return requests.post("http://localhost:5000/get_datas/").json()
