import sqlite3
from datetime import datetime
import os


DATABASE = "database/bookings.db"


# ---------------- DATABASE ----------------

def get_connection():

    os.makedirs("database", exist_ok=True)

    return sqlite3.connect(DATABASE)



def init_database():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        date TEXT NOT NULL,

        time TEXT NOT NULL,

        email TEXT NOT NULL,

        UNIQUE(date,time)

    )
    """)


    conn.commit()
    conn.close()



init_database()



# ---------------- MOCK CALENDAR ----------------


available_slots = {

    "2026-07-15": [
        "10:00",
        "11:00",
        "15:00"
    ],

    "2026-07-16": [
        "09:00",
        "14:00",
        "16:00"
    ],

    "2026-07-17": [
        "10:30",
        "13:30",
        "17:00"
    ]

}



# ---------------- CHECK AVAILABILITY ----------------


def check_availability(date):


    if date not in available_slots:

        return {

            "available":False,

            "slots":[]

        }



    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(
        """
        SELECT time FROM bookings
        WHERE date=?
        """,
        (date,)
    )


    booked_times = [

        row[0]

        for row in cursor.fetchall()

    ]


    conn.close()



    free_slots = [

        slot

        for slot in available_slots[date]

        if slot not in booked_times

    ]



    return {

        "available":len(free_slots)>0,

        "slots":free_slots

    }




# ---------------- RESERVE SLOT ----------------


def reserve_slot(date,time,email):


    conn = get_connection()

    cursor = conn.cursor()



    try:

        cursor.execute(
        """
        INSERT INTO bookings(date,time,email)

        VALUES(?,?,?)

        """,

        (
            date,
            time,
            email
        )

        )


        conn.commit()



        booking = {

            "date":date,

            "time":time,

            "email":email

        }



        return {

            "status":"success",

            "booking":booking

        }



    except sqlite3.IntegrityError:


        return {

            "status":"failed",

            "message":
            "This slot is already booked."

        }



    finally:

        conn.close()




# ---------------- NOTIFICATION ----------------


def send_booking_notification(email,details):


    print(
f"""
=========================
NOTIFICATION SENT
=========================

Recipient:
{email}

Appointment:
{details}

Status:
Confirmed

=========================
"""
    )


    return {

        "status":"sent"

    }




# ---------------- HISTORY ----------------


def get_all_bookings():


    conn=get_connection()

    cursor=conn.cursor()



    cursor.execute(
    """
    SELECT date,time,email
    FROM bookings
    ORDER BY id DESC
    """
    )


    rows=cursor.fetchall()



    conn.close()



    return [

        {

            "date":row[0],

            "time":row[1],

            "email":row[2]

        }

        for row in rows

    ]