<br />
<p align="center">
  <h3 align="center">Project: Data Modeling with Postgres</h3>

  <p align="center">
    Database and ETL pipeline in Postgres for a music streaming app's user activity data. 
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
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
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project was created as a project for the Data Engineering Nanodegree (Udacity).


### Built With

* Python

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* You must have the latest <a href="https://www.python.org/downloads/">Python version (3.9)</a> to run. Using older versions might cause instability in the performance of the module. 

### Installation


1. Clone the repo
   ```sh
   git clone https://github.com/nicobaguio/Data_Modeling_with_Postgres.git
   ```

2. Install packages
   ```sh
   pip install -r requirements.txt
   ```



<!-- USAGE EXAMPLES -->
## Usage
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


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.