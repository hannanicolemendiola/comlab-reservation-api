import requests


BASE_URL = "http://127.0.0.1:5000"


def print_response(title, response):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)
    print("Status Code:", response.status_code)

    try:
        print("Response:")
        print(response.json())
    except ValueError:
        print(response.text)


response = requests.get(
    f"{BASE_URL}/reservations"
)

print_response(
    "GET ALL RESERVATIONS",
    response
)


response = requests.get(
    f"{BASE_URL}/reservations/1"
)

print_response(
    "GET RESERVATION BY ID",
    response
)


new_reservation = {
    "requester_name": "Alice",
    "laboratory": "Computer Lab 1",
    "date": "2026-11-22",
    "start_time": "09:00",
    "end_time": "11:00",
    "purpose": "API Testing"
}

response = requests.post(
    f"{BASE_URL}/reservations",
    json=new_reservation
)

print_response(
    "POST CREATE RESERVATION",
    response
)


updated_reservation = {
    "requester_name": "John Updated",
    "laboratory": "Computer Lab 1",
    "date": "2026-11-20",
    "start_time": "12:00",
    "end_time": "14:00",
    "purpose": "Updated programming practice"
}

response = requests.put(
    f"{BASE_URL}/reservations/1",
    json=updated_reservation
)

print_response(
    "PUT UPDATE RESERVATION",
    response
)


response = requests.delete(
    f"{BASE_URL}/reservations/1"
)

print_response(
    "DELETE RESERVATION",
    response
)