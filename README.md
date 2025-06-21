📰 Feddit Sentiment Viewer
===========================

This app allows you to view and sort comments from a fake Reddit-style API (Feddit)
based on polarity (sentiment score between 0 and 1).

It includes:
- A FastAPI backend that fetches and analyses comments.
- A Streamlit frontend for interactively viewing and sorting the results.


🔧 Requirements
----------------
Install dependencies using:

    pip install -r requirements.txt


🚀 How to Run
--------------

1. Start the Feddit API
-------------------------
Make sure the fake Reddit API (Feddit) is running locally on port 8080.

If using Docker:

    docker compose -f <path-to-feddit-docker-compose.yml> up -d


2. Run the FastAPI App
------------------------

    python main.py

This exposes the following endpoints on localhost port 1234:

    POST /api/v1/comments_polarity/limit
    POST /api/v1/comments_polarity/with_time

These endpoints return comments with a predicted polarity.


3. Run the Streamlit Frontend
-------------------------------
    streamlit run feddit_streamlit.py --server.port 5678

This will open an interactive web UI in your browser.


🧠 How It Works
-----------------

FastAPI Endpoints:
- `/limit`: Fetch comments by subfeddit name and a number limit.
- `/with_time`: Fetch comments by subfeddit name and a date range.

Each comment is analysed using a placeholder `predict()` function that returns
a sentiment score between 0 and 1, a label either POSITIVE or NEGATIVE.


Streamlit App:
- Enter a subfeddit name.
- Choose a fetch mode: limit or time range.
- Results are displayed in a sortable table, ordered by polarity.
- Toggle between ascending and descending order.


🔍 Example Use
----------------
1. Open the Streamlit app.
2. Type in a feddit name like `Dully Topic 1`.
3. Select "By Limit", enter `10`, and click "Fetch Comments".
4. Comments will appear sorted by their predicted sentiment.


📁 Project Structure
---------------------
.
│   .gitignore
│   api.py
│   main.py
│   requirements.txt
│   streamlit_app.py
│   test.py
│   utils.py
│
├───.github
│   └───workflows
│           ci.yml
│
└───model
        utils.py
        __init__.py
