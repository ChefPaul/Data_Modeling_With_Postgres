# Data Modeling with Postgres
#### Data Engineering NanoDegree Project 1
The purpose of this project was to combine the theoretical concepts learned with the practical interactive lessons to create a database ingesting music data. Specifically, one for a startup called Sparkify, who wants to analyze the data they've been collecting on music streaming app. 

## Environment
Using a [Jupyter Notebook](https://jupyter.org/) environement to organize and create the project. 

## Libraries
Below are a list of the libraries used for the project.
```python
import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
```

## Package Contents
Within the package is a data folder with two subfolders, log_data and song_data, which house log data and song data in the JSON format. Additionally there are python files in the .py and .ipynb formats. 

The create_tables.py script drops and recreates the 'sparkifydb' database which is used through for testing and creating the etl process. This should be run after every iteration of change to ensure there are no duplicative processes running resulting in wrong data. 

The sql_queries.py contains all queries used to create tables and insert data into them. This file contains variables that are called upon throughout the etl process. 

The etl.ipynb is a step by step process on accessing and manipulating the raw data to prep for database ingestion. 

The test.ipynb contains the queries to select data from the tables to ensure the insert statements ran correctly. 

Finally, the etl.py file contains the whole process put together. Before running this script, the create_tables.py script should run to drop and recreate the 'sparkifydb' database. 

## Instructions
Run the create_tables.py script by creating a console editor and running

```bash
%run create_tables.py
```

Use the etl.ipynb to interact with the data and clean the data to match the format of the tables. For each insertion of data to the table, run the test.ipynb to make sure the data properly loaded. Complete the etl.ipynb and close the connection the the 'sparkifydb'.

Rerun the create_tables.py script to start with a clean database. 

Copy snippets of code from etl.ipynb into appropriate functions within etl.py script and save file. Run the etl.py script to load the data. 

```bash
%run etl.py
```

Once loaded, check the test.ipynb script to ensure data has been loaded into the tables. Close the kernal for the test.ipynb script.

## Roadmap
Next steps for improving the efficiency in data ingestion is to utilize the copy command, and create log files to log every step of the process. 

From an analytical standpoint, this database will be connected to a data visualization tool for analysis and story telling.

## License
[Udacity](https://www.udacity.com/)