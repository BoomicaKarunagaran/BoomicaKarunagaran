DEMO VIDEO:https://screenrec.com/share/av5GnrI0cm
Overview:
This is the YouTube Data Harvesting and Warehousing Project which aims to extract data from a specific YouTube channel by using its Channel ID and store the extracted data in a SQL database. This is my intermediate level Python Project to harvest YouTube data using YouTube Data API and store the data in a SQL database as a data lake. After that the data is migrated from the data lake to a SQL database as tables and are displayed in the streamlit application. The main objective is to facilitate data analysis and reporting by systematically organizing and storing the channel's data. This project will demonstrate how to harvest and warehouse YouTube data using SQL, and Streamlit.

Project Approach:
1.	Set up a Streamlit app: Streamlit is a great choice for building data visualization and analysis tools quickly and easily. This application has a simple UI where users can enter a YouTube channel ID, view the channel details, and select channels to migrate to the data warehouse.

2.	Connect to the YouTube API: I have used the YouTube API to retrieve channel and video data. To create YouTube Api, I have used Google developer console.

3.	Migrate data to a SQL data warehouse: After collecting data from each channel, I have migrated it to a MYSQL data warehouse.

4.	Query the SQL data warehouse: I have used SQL queries to join the tables (channel, playlist, video, comment) in the MYSQL data warehouse and retrieve data for specific channels based on user input.

REQUIRED LIBRARIES:
1.googleapiclient. discovery
2. MySQL. Connector
3.streamlit


TOOLS USED:

1.PYTHON: Python is a powerful programming language renowned for being easy to learn and understand. Python is the primary language employed in this project for the development of the complete application, including data retrieval, processing, analysis, and visualization.

2.GOOGLE API CLIENT: The googleapiclient library in Python facilitates the communication with different Google APIs. Its primary purpose in this project is to interact with YouTube's Data API v3, allowing the retrieval of essential information like channel details, video specifics, and comments. By utilizing googleapiclient, developers can easily access and manipulate YouTube's extensive data resources through code.

3.MySQL: MySQL Database: MySQL is a Relational Database Management System (RDBMS) whereas the structured Query Language (SQL) is the language used for handling the RDBMS using commands i.e Creating, Inserting, Updating and Deleting the data from the databases.

4.STREAMLIT: Streamlit library was used to create a user-friendly UI that enables users to interact with the programme and carry out data retrieval and analysis operations

Installation:
To run this project, you need to install the following packages:
1.	pip install google-api-python-client
2.	pip install mysql_connector_python
3.	pip install pandas
4.	pip install streamlit


Tools Install:
1.	Virtual studio code.
2.	Python 3.11.0 or higher.
3.	MySQL.
4.	Youtube API key.

TECHNOLOGIES USED:
[Python](https://www.python.org/)
[MySQL](https://www.mysql.com/)
[YouTube Data API]
(https://developers.google.com/youtube/v3)
[Streamlit](https://docs.streamlit.io/library/api-reference)

