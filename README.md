<br />
<p align="center">
  <h2 align="center">Project: Data Modeling with Postgres</h3>

  <p align="center">
    Database and ETL pipeline in Postgres for a music streaming app's user activity data. 
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h1 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#introduction">Introduction</a></li>
        <li><a href="#schema">Schema</a></li>
        <li><a href="#files">Files</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
# About The Project

## Introduction
This project was created as a project for the Data Engineering Nanodegree (Udacity). In this project, we create data models from data collected from songs and user activity
on the new music streaming app built by a startup called Sparkify. Currently, the data resides in a directory of JSON logs on user activity on the app, as well as a directory
wit JSON metadata on the songs on their app.

## Schema

### Fact Table

#### Song Plays

user activity data related to song plays.

    songplay_id: primary key (unique identifier).
    start_time : timestamp of song play.
    user_id    : unique identifier for user.
    level      : whether the user has a free or paid account. 
    song_id    : unique identifier for the song that the user was listening to.
    artist_id  : unique identifier for the artist of the song.
    session_id : unique identifier for a user's session.
    location   : location at time of the session.
    user_agent : user agent used to access the app.

### Dimension Table

#### 1. Users

user data.

    user_id   : primary key (unique identifier).
    first_name: user's first name.
    last_name : user's last name.
    gender    : user's gender.
    level     : whether the user has a free or paid account.

#### 2. Songs

song data.

    song_id  : primary key (unique identifier).
    title    : song title.
    artist_id: unique identifier for the artist of the song.
    year     : year song was released.
    duration : duration of song, in seconds.

#### 3. Artists

artist data.

    artist_id: primary key (unique identifier).
    name     : artist's name
    location : artist's location
    latitude : artist's latitude
    longitude: artist's longitude

#### 4. Time

timestamps of user activity data broken down by unit.

    start_time: songplay start_time
    hour      : songplay hour
    day       : songplay day
    week      : songplay week
    month     : songplay month
    year      : songplay year

## Files

1. `create_tables.py` -- Python script that sets up the database based on the credentials specified in `.env`

2. `etl.ipynb` -- Jupyter Notebook for performing exploratory data analysis for creating the ETL pipeline.

3. `etl.py` -- Python script that performs the ETL (Extract, Transform, Load) process.

4. `sql_queries.py` -- contains sql queries for creating databases that are used in `create_tables.py` & `etl.py`.

<br>

# Getting Started

To get a local copy up and running follow these simple steps.

## Prerequisites

* You must have the latest <a href="https://www.python.org/downloads/">Python version (3.9.7)</a> to run. Using older versions might cause instability in the performance of the module. 

## Installation


1. Clone the repo
   ```sh
   git clone https://github.com/nicobaguio/Data_Modeling_with_Postgres.git
   ```

2. Install packages
   ```sh
   pip install -r requirements.txt
   ```



<!-- USAGE EXAMPLES -->
# Usage

To use the code:

1. Create a .env file that contains your database credentials.

    *.env*

        host=127.0.0.1
        dbname=sparkifydb
        user=student
        password=student



2. Create tables.

        py create_tables.py

3. Run ETL script

        py etl.py

    By default, the ETL scripts inserts data using the `COPY` SQL command. To insert data into the database individually (using the `INSERT INTO` SQL command), just add the `-i` or `--insert` flag ***AFTER the script***:

        py etl.py -i
        py etl.py --insert


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.