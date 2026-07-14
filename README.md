# 📅 SchedulAI

## AI-Powered Multi-Agent Appointment Scheduling Assistant

SchedulAI is a **multi-agent AI scheduling assistant** built using **LangGraph and Streamlit** that automates appointment booking workflows.

The system follows a state-based agent architecture where a **Triage Agent** analyzes user requests and routes scheduling tasks to a **Booking Specialist Agent**.

The Booking Specialist manages:

- Calendar availability checking
- Date and time validation
- Appointment reservation
- Conflict handling
- Notification simulation
- Booking history retrieval

This project demonstrates practical implementation of:

- AI Agent Orchestration
- LangGraph State Workflows
- Tool Execution
- Persistent Memory
- Automation Systems

---

# 🚀 Features

## 🤖 Multi-Agent AI Workflow

SchedulAI uses a LangGraph-based workflow:

```
User Request
      |
      ↓
Triage Agent
      |
      ├──────────────→ General Response
      |
      ↓
Booking Specialist
      |
      ↓
Calendar Tools
      |
      ├──────────────→ Check Availability
      |
      ├──────────────→ Reserve Slot
      |
      └──────────────→ Send Notification
      |
      ↓
Booking Confirmation
```

---

# 🤖 AI Agents

## 1. Triage Agent

The Triage Agent is responsible for understanding user intent.

Capabilities:

- Detects scheduling requests
- Handles general conversations
- Routes tasks to appropriate agents
- Maintains workflow direction

Example:

```
User:
Hello

Assistant:
Hello 👋

I am SchedulAI.
I can help you schedule and manage appointments.
```

---

## 2. Booking Specialist Agent

The Booking Specialist handles the complete scheduling process.

Responsibilities:

- Extract appointment date
- Validate available slots
- Collect missing information
- Reserve appointments
- Handle booking conflicts
- Trigger confirmation notifications

---

# 📅 Smart Scheduling

SchedulAI supports natural language scheduling.

Example:

```
Book tomorrow
```

The system automatically converts:

```
tomorrow
        ↓
YYYY-MM-DD
```

Example:

```
2026-07-15
```

Supported features:

✅ Date normalization  
✅ Time extraction  
✅ Email extraction  
✅ Slot validation  
✅ Booking confirmation  

---

# ⚡ Calendar Tool System

SchedulAI contains mocked but functional calendar tools.

## check_availability(date)

Checks available appointment slots.

Example:

```
Input:

2026-07-15


Output:

10:00
11:00
15:00
```

---

## reserve_slot(date, time, email)

Handles appointment booking.

Features:

- Validates requested slot
- Prevents duplicate booking
- Stores confirmed appointments
- Updates availability

---

## send_booking_notification(email, details)

Simulates external notification delivery.

Example:

```
Notification Sent Successfully

Email:
demo@gmail.com

Appointment:
2026-07-15
10:00
```

---

# 🧠 Memory & State Persistence

SchedulAI uses LangGraph state management.

Implemented using:

- LangGraph StateGraph
- SQLite checkpoint persistence
- Stateful workflow execution

The assistant can:

✅ Maintain booking context  
✅ Handle multi-step conversations  
✅ Retrieve previous bookings  
✅ Continue scheduling workflows  

Example:

```
User:

Book tomorrow


Assistant:

Available slots:

10:00
11:00
15:00


User:

I want 10:00


Assistant:

Please provide your email.


User:

demo@gmail.com


Assistant:

Booking Confirmed
```

---

# 🛡️ Validation & Error Handling

SchedulAI handles:

## Missing Date

```
Please provide a date.
```

---

## Missing Time

```
Please provide your preferred time.
```

---

## Missing Email

```
Please provide your email.
```

---

## Slot Conflict

Example:

```
User:

Book 10:00 tomorrow
```

Response:

```
❌ This slot is already booked.

Available alternatives:

11:00
15:00
```

---

# 🖥️ Application Dashboard

The Streamlit interface provides:

## Dashboard Features

- Total booking count
- Available slot tracking
- Agent status monitoring
- Upcoming appointments
- Interactive AI chat interface

---

# 💬 Example Conversation

```
User:

Book tomorrow


SchedulAI:

Available slots on 2026-07-15:

10:00, 11:00, 15:00


User:

I want 10:00


SchedulAI:

Please provide your email.


User:

my email is demo@gmail.com


SchedulAI:

✅ Booking Confirmed

📅 Date: 2026-07-15

⏰ Time: 10:00

🔔 Notification sent successfully
```

---

# 🏗️ Architecture

```
                 User
                  |
                  ↓
          Streamlit Interface
                  |
                  ↓
          LangGraph Workflow
                  |
        ----------------------
        |                    |
        ↓                    ↓
 Triage Agent       Booking Specialist
                            |
                            ↓
                    Calendar Tools
                            |
        --------------------------------
        |              |               |
        ↓              ↓               ↓
 Availability   Reservation    Notification
                            |
                            ↓
                    SQLite Database
```

---

# 🏗️ Tech Stack

## AI Framework

- LangGraph
- LangChain

## Backend

- Python
- SQLite

## Frontend

- Streamlit
- Custom CSS

## Libraries

- python-dotenv
- dateparser
- requests
- sqlalchemy
- langgraph-checkpoint-sqlite

---

# 📂 Project Structure

```
SchedulAI/

│
├── app.py
│     Streamlit user interface
│
├── graph.py
│     LangGraph workflow routing
│
├── agents.py
│     Triage Agent and Booking Specialist
│
├── tools.py
│     Calendar and notification tools
│
├── memory.py
│     Persistent memory configuration
│
├── database/
│     bookings.db
│
├── requirements.txt
│
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone <repository-url>

cd SchedulAI
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### macOS/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file:

```
GOOGLE_API_KEY=your_api_key_here
```

Never commit API keys to GitHub.

---

# ▶️ Run Application

Start Streamlit:

```bash
streamlit run app.py
```

Application URL:

```
http://localhost:8501
```

---

# 🧪 Testing Instructions

## Availability Test

Input:

```
Book tomorrow
```

---

## Booking Test

Input:

```
Book tomorrow
```

Then:

```
I want 10:00
```

Then:

```
my email is test@gmail.com
```

Expected:

```
✅ Booking Confirmed

Date:
2026-07-15

Time:
10:00

Notification sent successfully
```

---

## Previous Booking Test

Input:

```
What was my previous booking?
```

---

## Conflict Test

Book the same slot twice.

Expected:

```
❌ This slot is already booked.

Available alternatives:
Other available slots
```

---

# 🌐 Deployment

The application can be deployed using:

- Streamlit Community Cloud
- Render
- Hugging Face Spaces


Required secret:

```
GOOGLE_API_KEY=your_api_key_here
```

---

# 🔒 Security

Implemented:

✅ Environment-based secrets  
✅ API keys excluded from repository  
✅ Database operations isolated  
✅ Sensitive files ignored using `.gitignore`

---

# 🌟 Future Improvements

Future production enhancements:

- Real Google Calendar API integration
- Real email service integration
- WhatsApp notifications
- User authentication
- Multi-user calendars
- PostgreSQL deployment
- Cloud monitoring

---

# 👩‍💻 Author

## Purvi Dhiman

B.Tech Computer Science Engineering (AI/ML)

---

# 📌 Project Summary

SchedulAI demonstrates how autonomous AI agents can collaborate using LangGraph to automate real-world scheduling workflows.

The project combines:

- Agent orchestration
- State management
- Tool execution
- Validation logic
- Persistent memory
- Automation

to build an intelligent appointment scheduling assistant.