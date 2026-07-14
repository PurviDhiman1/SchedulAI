from tools import (
    check_availability,
    reserve_slot,
    send_booking_notification,
)

from datetime import datetime, timedelta
import re


# Temporary conversation memory
booking_context = {}



# ---------------- DATE NORMALIZATION ----------------


def normalize_date(text):

    text = text.lower()


    if "tomorrow" in text:

        return (
            datetime.today() + timedelta(days=1)
        ).strftime("%Y-%m-%d")


    match = re.search(
        r"\d{4}-\d{2}-\d{2}",
        text
    )


    if match:

        return match.group()


    return None




# ---------------- TRIAGE AGENT ----------------


def triage_agent(user_message):

    text = user_message.lower()


    booking_keywords = [
        "book",
        "appointment",
        "schedule",
        "meeting",
        "slot",
        "availability",
        "reserve"
    ]


    # Continue ongoing booking conversation

    if (
        "date" in booking_context
        or "time" in booking_context
        or "waiting" in booking_context
    ):

        return {
            "route": "booking"
        }



    if any(
        word in text
        for word in booking_keywords
    ):

        return {
            "route": "booking"
        }



    if (
        "previous" in text
        or "history" in text
        or "booking" in text
    ):

        return {
            "route": "history"
        }



    return {
        "route": "general"
    }





# ---------------- BOOKING SPECIALIST ----------------



def booking_specialist(user_message):


    text = user_message.lower()



    # -------- DATE --------

    date = normalize_date(text)


    if date:

        booking_context["date"] = date




    # -------- EMAIL --------


    email_match = re.search(
        r"[\w\.-]+@[\w\.-]+",
        text
    )


    if email_match:

        booking_context["email"] = (
            email_match.group()
        )





    # -------- TIME --------


    time_match = re.search(
        r"\b\d{1,2}:\d{2}\b",
        text
    )


    if time_match:

        booking_context["time"] = (
            time_match.group()
        )





    # -------- CHECK DATE --------


    if "date" not in booking_context:

        return (
            "Please provide a date "
            "(example: tomorrow)"
        )





    # -------- SHOW AVAILABLE SLOTS --------


    if "time" not in booking_context:


        availability = check_availability(
            booking_context["date"]
        )


        if availability["available"]:


            booking_context["waiting"] = True


            return (

                f"Available slots on "
                f"{booking_context['date']}: "
                f"{', '.join(availability['slots'])}\n\n"

                "Please provide your preferred time and email."

            )



        else:

            return (
                "No slots available for this date."
            )






    # -------- ASK EMAIL --------


    if "email" not in booking_context:


        return (
            "Please provide your email."
        )






    # -------- FINAL BOOKING --------


    result = reserve_slot(

        booking_context["date"],

        booking_context["time"],

        booking_context["email"]

    )




    # -------- SLOT CONFLICT --------


    if result["status"] == "failed":


        alternatives = check_availability(
            booking_context["date"]
        )


        return (

            "❌ This slot is already booked.\n\n"

            "Available alternatives: "

            +
            ", ".join(
                alternatives["slots"]
            )

        )






    # -------- NOTIFICATION --------


    send_booking_notification(

        booking_context["email"],

        result["booking"]

    )





    booking = result["booking"]




    response = (

        "✅ Booking Confirmed\n\n"

        f"📅 Date: {booking['date']}\n"

        f"⏰ Time: {booking['time']}\n\n"

        "🔔 Notification sent successfully"

    )




    # Clear after successful booking

    booking_context.clear()



    return response