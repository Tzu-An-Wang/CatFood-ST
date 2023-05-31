import datetime


def insert_data(db, username, rating, feedback):
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "datetime": time_now,
        "username": username,
        "rating": rating,
        "feedback": feedback,
    }
    db.collection("Reviews").document(time_now).set(data)
