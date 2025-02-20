Create a web app that you can make a profile with username and password to save your settings.

To start The template will be filled in with my own personal settings for reference.

Users can change the settings to fit their lifestyle choice.

The app will include:
1. Affirmations
2. Personal Rules
3. Long term Goals
4. Inspirations
5. Study Guide
6. Ikigai Picture
7. Daily Checklist

Needs to have a simple and clean design.
Light and dark mode.
Notifications for daily checklist.

Will be using Javascript React for front end and Python Flask for back end. 

Eventually make a mobile version for IOS and Android and put it on the app stores.

First we will need a login / new user page
second a home screen 
tabs for the different pages
settings
light and dark mode button
log out


Running the virtual environment (backend).
1. cd S:\Learning\Python\Projects2025\personal-life-coach\main\backend
2. .\venv\Scripts\Activate
3. python app.py
4. API should be running at http://127.0.0.1:5000 or http://127.0.0.1:5000/tasks

Running psql from PostegreSQL bin folder (database).
1. & "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres
2. Password for user postgres:
3. \c task_manager
4. SELECT * FROM task;

Running the webpage (front end).
1. cd main
2. cd frontend
3. npm run dev
4. open http://localhost:5173/
