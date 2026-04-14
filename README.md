 # WatchParty

A real-time web application that allows multiple users to watch YouTube videos together in sync with live chat.

---

## Features

-  Synchronized YouTube playback
-  Real-time chat using WebSockets
-  User authentication (Login/Register)
-  Create & join private rooms
-  Dark mode UI

---

##  Tech Stack

- **Backend:** Django, Django Channels
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** PostgreSQL
- **WebSockets:** Daphne (ASGI server)

---

## Installation (Local Setup)

```bash
git clone https://github.com/Mayanknegi24/Get2Gather.git
cd watchparty
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

## Acknowledgements
Django Documentation
YouTube Iframe API
