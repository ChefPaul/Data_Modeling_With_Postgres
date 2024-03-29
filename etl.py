import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Processes song and artist data
    Args:
        cur: connection cursor
        filepath: path to data files

    Returns: Inserts song and artist data into database
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    songs_col = ['song_id', 'title', 'artist_id', 'year', 'duration']
    song_data = df[songs_col].values.tolist()[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artists_col = ['artist_id', 'title', 'artist_location', 'artist_latitude', 'artist_longitude']
    artist_data = df[artists_col].values.tolist()[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Processes user log data
    Args:
        cur: connecion cursor
        filepath: path to data files
    Returns: Inserts user log data into database
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'])
    
    # insert time data records
    # use pandas datetime (dt) to convert timestamps to different date formats
    time_data = (t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame({'start_time': time_data[0],
                        'hour': time_data[1],
                        'day': time_data[2],
                        'week': time_data[3],
                        'month': time_data[4],
                        'year': time_data[5],
                        'weekday': time_data[6]})

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_col = ['userId', 'firstName', 'lastName', 'gender', 'level']
    user_df = df[user_col]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [index, pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Processes all data files
    Args:
        cur: connection cursor
        conn: connection to database
        filepath: path to data files
        func: function to process data
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
