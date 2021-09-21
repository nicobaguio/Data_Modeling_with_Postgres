import os
import glob
from dotenv import dotenv_values
from pandas.core.algorithms import isin
import psycopg2
import pandas as pd
# from sql_queries import *
from io import StringIO
import json

config = dict(dotenv_values(".env"))

def upload_data(cur, df, table):
    buffer = StringIO()
    if isinstance(df, pd.DataFrame):
        df.to_csv(buffer, header=False, index=False, sep="\t")
        buffer.seek(0)

        try:
            cur.copy_from(buffer, table, sep="\t", columns=tuple(df.columns), null="")
            print(f"Success: inserted data successfully into {table} table in database.")

        except:
            print(f"Error: copying data to {table} table in database.")

    else:
        print("Error: df is not a pandas dataframe.")

def process_songs(cur, df):
    # Process Songs Table
    songs_df = df[
        ['song_id', 'title', 'artist_id', 'year', 'duration']
    ].copy()

    # Process Artists Table
    artists_df = df[
        ['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']
    ].copy()

    artists_df.rename(columns={
        'artist_name': 'name',
        'artist_location': 'location',
        'artist_latitude': 'latitude',
        'artist_longitude': 'longitude',
    }, inplace=True)

    artists_df.drop_duplicates(subset='artist_id', inplace=True)

    # Upload to appropriate tables in database
    upload_data(cur, songs_df, 'songs')
    upload_data(cur, artists_df, 'artists')

def process_logs(cur, df):
    # filter by NextSong action
    next_songs_df = df.loc[df['page'] == 'NextSong'].copy()
    # next_songs_df.reset_index(drop=True, inplace=True)
    # Convert Time Stamp
    
    next_songs_df.loc[:,'ts_dt'] = next_songs_df['ts'].apply(
        pd.to_datetime, unit='ms', origin='unix'
    )

    # Process Time Table

    time_df = pd.DataFrame([{
        'start_time': v,
        'hour': v.hour,
        'day': v.day,
        'week': v.week,
        'month': v.month,
        'year': v.year
    } for _, v in next_songs_df['ts_dt'].items()])

    time_df.drop_duplicates(subset=['start_time'], inplace=True)

    # Process User Table
    user_df = next_songs_df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    
    user_df = user_df.rename(columns={
        'userId': 'user_id',
        'firstName': 'first_name',
        'lastName': 'last_name'
    })

    user_df = user_df.drop_duplicates('user_id')

    # Process Songplay Table
    
    pre_songplay_df = next_songs_df[
        ['ts_dt', 'userId', 'level', 'song', 'artist', 'sessionId', 'location', 'userAgent']
    ]

    cur.execute("SELECT artist_id, name FROM artists")
    artists_df = pd.DataFrame(cur.fetchall(), columns=['artist_id', 'name'])

    cur.execute("SELECT song_id, title FROM songs")
    songs_df = pd.DataFrame(cur.fetchall(), columns=['song_id', 'title'])

    first_merge_df = pd.merge(
        left=pre_songplay_df,
        right=artists_df,
        how='left',
        left_on='artist',
        right_on='name'
    )

    songplay_merged_df = pd.merge(
        left=first_merge_df,
        right=songs_df,
        how='left',
        left_on='song',
        right_on='title'
    )

    songplay_merged_df.drop(['name', 'title', 'song', 'artist'], axis=1, inplace=True)

    correct_order = ['ts_dt', 'userId', 'level', 'song_id', 'artist_id', 'sessionId', 'location', 'userAgent']

    songplays_df = songplay_merged_df[correct_order]
    songplays_df.rename(columns={
        'ts_dt': 'start_time',
        'userId': 'user_id',
        'sessionId': 'session_id',
        'userAgent': 'user_agent'
    }, inplace=True)

    # Upload to approriate table in database
    upload_data(cur, time_df, 'time')
    upload_data(cur, user_df, 'users')
    upload_data(cur, songplays_df, 'songplays')

def process_data(cur, conn, filepath, func):
    json_wildcard = os.path.join(filepath, "**", "*.json")
    files = glob.glob(json_wildcard, recursive=True)

    def process_json(fn):
        with open(fn) as f:
            data_list = [json.loads(line) for line in f]

        return data_list

    flat_files = [item for f in files for item in process_json(f)]

    df = pd.DataFrame(flat_files)
    
    func(cur, df)
    conn.commit()

def main():
    conn = psycopg2.connect(**config)
    cur = conn.cursor()
    
    process_data(cur, conn, filepath=os.path.join(".", "data", "song_data"), func=process_songs)
    process_data(cur, conn, filepath=os.path.join(".", "data", "log_data"), func=process_logs)

    conn.close()

if __name__ == "__main__":
    main()