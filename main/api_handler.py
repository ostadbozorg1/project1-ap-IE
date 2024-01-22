from requests import Response, get, post


def _get_slots() -> dict[str, int]:
    responce: Response = get(url="http://localhost/slots")
    return responce.json()


def _reserve(id: str, amount: int):
    response: Response = post(
        url="http://localhost/reserve", json={"id": id, "reserved": amount})
    return response.json()["success"]


def get_reservation_amount(id: str) -> int:
    return _get_slots()[id]


def add_reservation_amount(id: str, amount: int):
    return _reserve(id=id, amount=-amount)


def make_reservation(id: str):
    return _reserve(id, 1)
