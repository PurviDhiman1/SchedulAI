import streamlit as st
from graph import run_scheduler
from tools import get_all_bookings, available_slots


# ---------------- CONFIG ----------------

st.set_page_config(
    page_title="SchedulAI",
    page_icon="📅",
    layout="wide"
)


# ---------------- STYLE ----------------

st.markdown(
"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');


*{
    font-family:Inter, sans-serif;
}


.stApp{
    background:
    linear-gradient(
        135deg,
        #f8fafc,
        #eef2ff
    );
}


/* remove branding */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}


/* Hero */

.hero{

text-align:center;
padding:30px;

}


.hero h1{

font-size:55px;
font-weight:800;
letter-spacing:-3px;
color:#111827;

}


.hero p{

font-size:20px;
color:#6b7280;

}


/* Cards */

.card{

background:white;
padding:25px;
border-radius:24px;

box-shadow:
0 10px 30px rgba(0,0,0,0.06);

border:1px solid #e5e7eb;

}


/* metrics */

.metric-title{

color:#6b7280;
font-size:14px;

}


.metric-value{

font-size:35px;
font-weight:700;
color:#111827;

}



/* chat */

[data-testid="stChatMessage"]{

background:white;
border-radius:18px;
padding:12px;

box-shadow:
0 5px 20px rgba(0,0,0,0.05);

}


[data-testid="stChatInput"]{

border-radius:20px;

}


</style>

""",
unsafe_allow_html=True
)



# ---------------- HERO ----------------


st.markdown(
"""
<div class="hero">

<h1>
📅 SchedulAI
</h1>

<p>
AI powered multi-agent scheduling assistant
</p>

</div>

""",
unsafe_allow_html=True
)



# ---------------- METRICS ----------------


bookings = get_all_bookings()


total_bookings = len(bookings)


from tools import check_availability


total_slots = 0

for date in available_slots:

    result = check_availability(date)

    total_slots += len(result["slots"])



c1,c2,c3 = st.columns(3)


with c1:

    st.markdown(
    f"""
    <div class="card">

    <div class="metric-title">
    📅 Total Bookings
    </div>

    <div class="metric-value">
    {total_bookings}
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )



with c2:

    st.markdown(
    f"""
    <div class="card">

    <div class="metric-title">
    🕒 Available Slots
    </div>

    <div class="metric-value">
    {total_slots}
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )



with c3:

    st.markdown(
    """
    <div class="card">

    <div class="metric-title">
    🤖 Agents Status
    </div>

    <div class="metric-value">
    🟢 Active
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )



st.write("")



# ---------------- WORKFLOW ----------------


st.markdown(
"""
<div class="card">

<h2>
🤖 AI Workflow
</h2>


<p>
User Request → Triage Agent → Booking Specialist → Calendar Tools → Confirmation
</p>


</div>

""",
unsafe_allow_html=True
)



st.write("")



# ---------------- BOOKINGS ----------------


if bookings:

    st.markdown(
    """
    <div class="card">

    <h2>
    📌 Upcoming Appointments
    </h2>

    </div>
    """,
    unsafe_allow_html=True
    )


    for booking in bookings[-3:]:

        st.markdown(
        f"""
        <div class="card">

        📅 <b>{booking['date']}</b>

        <br>

        ⏰ {booking['time']}

        <br><br>

        Status:
        ✅ Confirmed

        </div>
        """,
        unsafe_allow_html=True
        )



# ---------------- CHAT ----------------


st.markdown(
"""
<div class="card">

<h2>
💬 Conversation
</h2>

</div>
""",
unsafe_allow_html=True
)



if "messages" not in st.session_state:

    st.session_state.messages=[]



for role,msg in st.session_state.messages:

    with st.chat_message(role):

        st.write(msg)



user_input = st.chat_input(
    "Ask SchedulAI to book an appointment..."
)



if user_input:


    st.session_state.messages.append(
        ("user",user_input)
    )


    response = run_scheduler(
    user_input,
    st.session_state.get(
        "thread_id",
        "schedulai_user_001"
    )
)


    st.session_state.messages.append(
        ("assistant",response)
    )


    st.rerun()