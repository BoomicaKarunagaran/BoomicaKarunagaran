#Libraries:
import googleapiclient.discovery
from googleapiclient.discovery import build
import mysql.connector
import isodate
from datetime import datetime
import streamlit as st
from googleapiclient.errors import HttpError
import pandas as pd

#API key connection:

def Api_connect():
    Api_Id="AIzaSyAvFAyaQCLZH7oA7h6iio_js7RpZXq8fTA"
    api_service_name = "youtube"
    api_version = "v3"
    youtube=build(api_service_name,api_version,developerKey=Api_Id)
    return youtube
youtube=Api_connect()

#fetching the channel id:
def get_channel_info(channel_id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    response = request.execute()
    data ={
        "channel_name":response['items'][0]['snippet']['title'],
        "channel_id":channel_id,
        "channel_dec":response['items'][0]['snippet']['description'],
        "channel_vc":response['items'][0]['statistics']['videoCount'],
        "channel_dec":response['items'][0]['snippet']['description'],
        "channel_pid":response['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
        "channel_subc":response['items'][0]['statistics']['subscriberCount']
        }
    return data

# channel_data=get_channel_info(channel_id)
# channel_data 


#To Fetch the video ids:
def get_video_ids(channel_id):
    video_ids=[]
    #get uploads playlist id
    response=youtube.channels().list(id=channel_id,
                                    part='contentDetails').execute()
    playlist_id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token=None

    while True:
        response1=youtube.playlistItems().list(playlistId=playlist_id,
                                            part='snippet',
                                            maxResults=50,
                                            pageToken=next_page_token).execute()
        for i in range(len(response1['items'])):
            video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token=response1.get('nextPageToken')

        if next_page_token is None:
            break
    return video_ids

    
    
# video_ids=get_video_ids('UCQqmjKQBKQkRbWbSntYJX0Q')
# video_ids    
    

#To fetch the video information:
def get_video_info(video_ids):import isodate
def duration_to_seconds(video_Duration):

    duration = isodate.parse_duration(video_Duration)
    hours = duration.days *24 + duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    seconds = duration.seconds % 60
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

def published_date(video_publisheddate):
    import isodate

    from datetime import datetime

    #ISO date string:
    iso_date_str="2024-05-24T18:11:59z"

    #step:1 parse the iso date str ing into a datetime object
    #note:The 'z' at the end of the ISO date string UTC time
    iso_date =datetime.fromisoformat(video_publisheddate.replace("Z","+00:00"))
    
    #step:2 format the datetime object to an SQL- compatible date string
    sql_date_str = iso_date.strftime('%Y -%m-%d %H:%M:%S')

    print("SQL-compatible date format:",sql_date_str)
    return sql_date_str


    video_data=[]
    for video_id in video_ids:
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()

        for item in response["items"]:
            print(item["statistics"])
            data=dict(Channel_Name = item['snippet']['channelTitle'],
                    Channel_Id = item['snippet']['channelId'],
                    Video_Id = item['id'],
                    Title = item['snippet']['title'],
                    Tags = item.get('tags'),
                    Description = item.get('description'),
                    vi_Publisheddate =published_date(item['snippet'].get('publishedAt')),
                    Duration = duration_to_seconds(item['contentDetails'].get('duration')),
                    views = item['statistics'].get('viewCount'),
                    Comments = item.get('CommentCount'),
                    Favourite_Count = item['statistics']['favoriteCount'],
                    Definition = item['contentDetails']['definition'],
                    Caption_status = item['contentDetails']['caption'],
                    )
            video_data.append(data)
    return video_data               

# video_data = get_video_info(video_ids)
# video_data



#To Fetch comment information:
from googleapiclient.errors import HttpError  # Import HttpError from googleapiclient.errors
# Function to fetch comment information
def get_comment_info(youtube, video_ids):
    comment_data = []
    try:
        for video_id in video_ids:
            try:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=50
                )
                response = request.execute()

                if 'items' in response and response['items']:
                    for item in response['items']:
                        data = {
                            'Comment_Id': item['snippet']['topLevelComment']['id'],
                            'Video_Id': item['snippet']['topLevelComment']['snippet']['videoId'],
                            'Comment_Text': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                            'Comment_Author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                            'Comment_Published': item['snippet']['topLevelComment']['snippet']['publishedAt']
                        }
                        comment_data.append(data)
                else:
                    
                    data = {
                        'Comment_Id': None,
                        'Video_Id': video_id,
                        'Comment_Text': 'No comments found',
                        'Comment_Author': 'N/A',
                        'Comment_Published': 'N/A'
                    }
                    comment_data.append(data)

            except HttpError as e:
                if e.resp.status == 403:
                    # Handle case where comments are disabled for the video ID
                    data = {
                        'Comment_Id': None,
                        'Video_Id': video_id,
                        'Comment_Text': 'Comments are disabled',
                        'Comment_Author': 'N/A',
                        'Comment_Published': 'N/A'
                    }
                    comment_data.append(data)
                else:
                    raise  # Re-raise the exception if it's not a 403 error

    except Exception as e:
        print(f"Error fetching comments: {str(e)}")

    return comment_data
# comment_data = get_comment_info(youtube,video_ids)
# comment_data


# To fetch the playlist details:
def get_playlist_details(channel_id):
        next_page_token=None
        All_data=[]
        while True:
                request=youtube.playlists().list( 
                        part='snippet,contentDetails', 
                        channelId=channel_id,                      
                        maxResults=50,
                        pageToken=next_page_token
                )
                response=request.execute()
        
                for item in response['items']:
                        data=dict(Playlist_Id=item['id'],
                               Title = item['snippet']['title'],
                               Channel_Id = item['snippet']['channelId'],
                               Channel_Name = item['snippet']['channelTitle'],
                               PublishedAt = item['snippet']['publishedAt'],
                               Video_Count= item['contentDetails']['itemCount'])
                        All_data.append(data)

                next_page_token=response.get('nextPageToken')
                if next_page_token is None:
                        break
        return All_data
# All_data=get_playlist_details('UCQqmjKQBKQkRbWbSntYJX0Q')
# All_data

#MySQL Connections:
import mysql.connector
#Connect to MYSQL server
mydb = mysql.connector.connect(

    host="127.0.0.1",
    user="root",
    password="pavi&boomi"
)
mycursor = mydb.cursor()
print(mydb)

#Create Database:
import mysql.connector
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="pavi&boomi"
)
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS mysqldatabase")

mycursor.close()
mydb.close()

#Creating Tables and Inserting Data:
#Creating Channel Table:
import mysql.connector
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="pavi&boomi",
    database="mysqldatabase"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS  Channel_data(Channel_Name VARCHAR(255),Channel_ID VARCHAR(100) NOT NULL,Channel_description TEXT,Channel_video_count VARCHAR(100),Channel_playlist_ID VARCHAR(100),Channel_Subscription VARCHAR(100))")
mydb.commit()
mycursor.close()
mydb.close()  

#Inserting channel data:
# query= "INSERT INTO channel_data(Channel_Name, Channel_Id ,Channel_Description, Channel_video_count,Channel_playlist_ID,Channel_Subscription) VALUES (%s, %s, %s, %s,%s,%s)" 
# print(channel_data)
# val=list(channel_data.values())
# val
# print(values)
# mycursor.execute(query, values)
# mydb.commit()

#Create video table:
import mysql.connector
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="pavi&boomi",
    database="mysqldatabase"
)
mycursor = mydb.cursor()
mycursor.execute('''CREATE TABLE IF NOT EXISTS videodetails(
                        Channel_Name VARCHAR(100),
                        Channel_Id VARCHAR(100),
                        Video_Id VARCHAR(100) PRIMARY KEY,
                        Title VARCHAR(100),
                        Tags VARCHAR(255),
                        Description TEXT, 
                        video_Publisheddate VARCHAR(100), 
                        Video_Duration INT,
                        Views INT,
                        Comments INT, 
                        Favorite_count INT, 
                        Definition VARCHAR(100),
                        Caption_status VARCHAR(100))
                    ''')
mydb.commit()

#Insert video data:
# query = "INSERT INTO videodetails(Channel_Id, Channel_Name,Video_Id,Title,Tags,Description,vi_Publisheddate,Duration,views, Comments, Favorite_Count, Definition, Caption_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
# video_data= get_video_info(video_ids)
# video_data
# temp = []
# for i in video_data:
#     temp.append(tuple(i.values()))
# temp
# print(video_data)
# mycursor.executemany(query,temp)
# mydb.commit()

#Create comment Table:
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS Commentdetails (Comment_ID VARCHAR(100),
        Video_ID VARCHAR(100),
        Comment_text TEXT,
        Comment_Author VARCHAR(255),
        Comment_Published VARCHAR(255)
    )
''')
mydb.commit()
#Insert comment data:
# query = "INSERT INTO commentdetails (Comment_ID, Video_ID, Comment_text, Comment_Author, Comment_Published) VALUES (%s, %s, %s, %s, %s)"
# try:
#     comment_values = [(comment['Comment_Id'], comment['Video_Id'], comment['Comment_Text'], comment['Comment_Author'], comment['Comment_Published']) for comment in comment_data]
#     comment_data
#     temp = []
#     for i in comment_data:
#         temp.append(tuple(i.values()))
#     temp    
#     mycursor.executemany(query, comment_values)
#     mydb.commit()
#     print(mycursor.rowcount, "records inserted successfully into commentdetails table")
# except mysql.connector.Error as error:
#     print(f"Error inserting records: {error}")
# finally:
#     mycursor.close()
#     mydb.close()


# Streamlit UI configuration
st.set_page_config(page_title="YOUTUBETUBE DATA HARVESTING AND WAREHOUSING", layout="wide")

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="pavi&boomi",
    database="mysqldatabase"

)
mycursor = mydb.cursor()

def run_query(query):
    mycursor.execute(query)
    result = mycursor.fetchall()
    columns = [i[0] for i in mycursor.description]
    return pd.DataFrame(result, columns=columns)


st.sidebar.header("NAVIGATION")
section = st.sidebar.selectbox("SELECT SECTION", ["HOME", "DATA COLLECTION", "DATA ANALYSIS"])

if section == "HOME":
    st.markdown("Welcome to the YouTube Data Analysis App!")
    st.markdown("Use the sidebar to navigate through different sections of the app.")

# Assuming necessary imports and setup for Streamlit, MySQL, and YouTube API are done correctly

def main():
    if section == "DATA COLLECTION":
        st.header("DATA COLLECTION")
        st.markdown("Enter the YouTube Channel ID to collect and store data.")
        
        channel_id = st.text_input("Enter YouTube Channel ID:")
        if st.button("Collect and Store Data"):
            st.success("Data for channel ID collected and stored successfully.")
            channel_details=get_channel_info(channel_id)
            video_ids = get_video_ids(channel_id)
            video_data = get_video_info(video_ids)
            comment_data = get_comment_info(youtube,video_ids)
            # Insert channel data into database
            query= "INSERT IGNORE INTO channel_data(Channel_Name, Channel_Id ,Channel_Description, Channel_video_count,Channel_playlist_ID,Channel_Subscription) VALUES(%s,%s,%s,%s,%s,%s)" 
            channel_values = list(channel_details.values())
            mycursor.execute(query,channel_values)
            mydb.commit()
            # Insert video data into database
            if video_data:
                video_query = "INSERT IGNORE INTO videodetails (Channel_Id, Channel_Name, Video_Id, Title, Tags, Description, video_Publisheddate,video_Duration, views, Comments, Favourite_Count, Definition, Caption_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                video_values = [(item['Channel_Id'], item['Channel_Name'], item['Video_Id'], item['Title'], item['Tags'], item['Description'], item['video_Publisheddate'], item['video_Duration'], item['views'], item['Comments'], item['Favourite_Count'], item['Definition'], item['Caption_status']) for item in video_data]
                mycursor.executemany(video_query, video_values)
                mydb.commit()
                st.write(f"{len(video_data)} video records inserted successfully.")
            # Insert comment data into database
            query = "INSERT IGNORE INTO commentdetails (Comment_ID, Video_ID, Comment_text, Comment_Author, Comment_Published)VALUES(%s,%s,%s,%s,%s)"
            comment_values = [(comment['Comment_Id'], comment['Video_Id'], comment['Comment_Text'], comment['Comment_Author'], comment['Comment_Published']) for comment in comment_data]
            mycursor.executemany(query, comment_values)
            mydb.commit()
            # Display channel data if available
            if channel_details:
                st.write("Channel Data:")
                st.write(channel_details)

if __name__ == "__main__":
    main()

#DATA ANALYSIS:    
if section == "DATA ANALYSIS":
    st.header("DATA ANALYSIS")

    
    questions = [
         "What are the names of all the videos and their corresponding channels?",
        
        "Which channels have the most number of videos, and how many videos do they have?",
         
        "What are the top 10 most viewed videos and their respective channels?",

        "How many comments were made on each video, and what are their corresponding video names?",

        "Which videos have the highest number of likes, and what are their corresponding channel names?",

        "What is the total number of views for each channel, and what are their corresponding channel names?",

        "What are the names of all the channels that have published videos in the year 2022?",

        "What is the average duration of all videos in each channel, and what are their corresponding channel names?",

        "Which videos have the highest number of comments, and what are their corresponding channel names?",
        
    ]
    query = ""
    selected_question = st.selectbox("Select a Question to Query", questions)
    # Function to execute SQL queries and return the results as a DataFrame

        
    if st.button("Run Query"):
            if selected_question == questions[0]:
                query = "SELECT Title AS Video_Name, Channel_Name FROM videodetails"
            elif selected_question == questions[1]:
                query = "SELECT Channel_Name, COUNT(Video_Id) AS Number_of_Videos FROM videodetails GROUP BY Channel_Name ORDER BY Number_of_Videos DESC"
            elif selected_question == questions[2]:
                query = "SELECT Title AS Video_Name, Channel_Name, Views FROM videodetails ORDER BY Views DESC LIMIT 10"
            elif selected_question == questions[3]:
                query = "SELECT Title AS Video_Name, Comments FROM videodetails"
            elif selected_question == questions[4]:
                query = "SELECT Title AS Video_Name, Channel_Name, Likes FROM videodetails ORDER BY Likes DESC LIMIT 10"
            elif selected_question == questions[5]:
                query = "SELECT Channel_Name, SUM(Views) AS Total_Views FROM videodetails GROUP BY Channel_Name"
            elif selected_question == questions[6]:
                query = "SELECT Channel_Name FROM videodetails WHERE video_Publisheddate LIKE '2022%' GROUP BY Channel_Name"
            elif selected_question == questions[7]:
                query = "SELECT Channel_Name, AVG(Video_duration) AS Average_Duration FROM videodetails GROUP BY Channel_Name"
            elif selected_question == questions[8]:
                query = "SELECT Title AS Video_Name, Channel_Name, Comments FROM videodetails ORDER BY Comments DESC LIMIT 10"
            else:
                query = ""

            if query:
                result_df = run_query(query)
                st.write(result_df)
            else:
                st.error("Invalid query selected. Please try again.")



   