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


def set_reservation_amount(id: str, amount: int):
    _reserve(id=id, amount=_get_slots()[id]-amount)
