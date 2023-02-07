import requests

def get_Datas():
    return requests.get("http://localhost:5000/post_datas/").json()

def post_Datas():
    return requests.post("http://localhost:5000/get_datas/").json()
