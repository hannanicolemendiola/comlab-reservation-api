from flask import Flask, jsonify, request

app = Flask(__name__)

reservations = [
    {
        "id": 1,
        "requester_name": "John",
        "laboratory": "Computer Lab 1",
        "date": "2026-11-20",
        "start_time": "09:00",
        "end_time": "11:00",
        "purpose": "Programming practice"
    },
    {
        "id": 2,
        "requester_name": "Jane",
        "laboratory": "Computer Lab 2",
        "date": "2026-11-21",
        "start_time": "13:00",
        "end_time": "15:00",
        "purpose": "Web development"
    }
]


def is_valid_reservation(data):
    required_fields = [
        "requester_name",
        "laboratory",
        "date",
        "start_time",
        "end_time",
        "purpose"
    ]

    return all(
        field in data and data[field]
        for field in required_fields
    )


def has_schedule_conflict(data, ignore_id=None):
    for reservation in reservations:
        if ignore_id is not None and reservation["id"] == ignore_id:
            continue

        if (
            reservation["laboratory"] == data["laboratory"]
            and reservation["date"] == data["date"]
        ):
            if (
                data["start_time"] < reservation["end_time"]
                and data["end_time"] > reservation["start_time"]
            ):
                return True

    return False


@app.route("/reservations", methods=["GET"])
def get_reservations():
    return jsonify({"reservations": reservations}), 200


@app.route("/reservations/<int:reservation_id>", methods=["GET"])
def get_reservation(reservation_id):
    for reservation in reservations:
        if reservation["id"] == reservation_id:
            return jsonify(reservation), 200

    return jsonify({
        "error": "Reservation ID not found"
    }), 404


@app.route("/reservations", methods=["POST"])
def create_reservation():
    data = request.get_json()

    if not data or not is_valid_reservation(data):
        return jsonify({
            "error": "Invalid input"
        }), 400

    if data["start_time"] >= data["end_time"]:
        return jsonify({
            "error": "Invalid input"
        }), 400

    if has_schedule_conflict(data):
        return jsonify({
            "error": "Schedule conflict"
        }), 400

    new_id = max(
        [reservation["id"] for reservation in reservations],
        default=0
    ) + 1

    new_reservation = {
        "id": new_id,
        "requester_name": data["requester_name"],
        "laboratory": data["laboratory"],
        "date": data["date"],
        "start_time": data["start_time"],
        "end_time": data["end_time"],
        "purpose": data["purpose"]
    }

    reservations.append(new_reservation)

    return jsonify(new_reservation), 201


@app.route("/reservations/<int:reservation_id>", methods=["PUT"])
def update_reservation(reservation_id):
    data = request.get_json()

    reservation = None

    for item in reservations:
        if item["id"] == reservation_id:
            reservation = item
            break

    if reservation is None:
        return jsonify({
            "error": "Reservation ID not found"
        }), 404

    if not data or not is_valid_reservation(data):
        return jsonify({
            "error": "Invalid input"
        }), 400

    if data["start_time"] >= data["end_time"]:
        return jsonify({
            "error": "Invalid input"
        }), 400

    if has_schedule_conflict(data, ignore_id=reservation_id):
        return jsonify({
            "error": "Schedule conflict"
        }), 400

    reservation["requester_name"] = data["requester_name"]
    reservation["laboratory"] = data["laboratory"]
    reservation["date"] = data["date"]
    reservation["start_time"] = data["start_time"]
    reservation["end_time"] = data["end_time"]
    reservation["purpose"] = data["purpose"]

    return jsonify(reservation), 200


@app.route("/reservations/<int:reservation_id>", methods=["DELETE"])
def delete_reservation(reservation_id):
    for index, reservation in enumerate(reservations):
        if reservation["id"] == reservation_id:
            deleted_reservation = reservations.pop(index)
            return jsonify(deleted_reservation), 200

    return jsonify({
        "error": "Reservation ID not found"
    }), 404


if __name__ == "__main__":
    app.run(debug=True)