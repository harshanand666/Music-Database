import pandas as pd
import mysql.connector
import random

# Password for sql server
PASSWORD = ""

# Create connection to database
my_connection = mysql.connector.connect(
    user="root", password=PASSWORD, host="localhost", database="MusicTest"
)

cursor_object = my_connection.cursor()

# Read in data
df = pd.read_csv("./data.csv")


# Helper function to output random date for Date of birth
def generate_random_dob(start="1950-01-01", end="2000-01-01"):
    return pd.to_datetime(random.choice(pd.date_range(start=start, end=end)))


# Helper function to generate random release data
def generate_random_release(start="2000-01-01", end="2020-01-01"):
    return pd.to_datetime(random.choice(pd.date_range(start=start, end=end)))


# Helper function to generate random phone number
def generate_random_phone_number():
    area_code = random.randint(100, 999)
    central_office_code = random.randint(100, 999)
    line_number = random.randint(1000, 9999)
    return f"({area_code}) {central_office_code}-{line_number}"


# Mock addresses for record labels
addresses = [
    "1234 Elm Street, Springfield, IL 62704",
    "5678 Maple Avenue, Metropolis, NY 10001",
    "9101 Oak Lane, Gotham, NJ 07030",
    "1122 Pine Drive, Smallville, KS 66002",
    "1314 Birch Boulevard, Star City, CA 90210",
    "1516 Cedar Circle, Central City, CO 80022",
    "1718 Redwood Road, Coast City, OR 97330",
    "1920 Willow Way, Keystone, FL 33556",
    "2122 Aspen Avenue, Blüdhaven, TX 75001",
    "2324 Spruce Street, Fawcett City, WA 98001",
]

# Mock streaming platforms
music_streaming_platforms = [
    "Spotify",
    "Apple Music",
    "Amazon Music",
    "YouTube Music",
    "Tidal",
    "Pandora",
    "Deezer",
    "SoundCloud",
    "iHeartRadio",
    "Napster",
    "Google Play Music",
    "Qobuz",
    "Bandcamp",
    "Audiomack",
    "Anghami",
    "JioSaavn",
    "Wynk Music",
    "Gaana",
    "Tencent Music",
    "KKBOX",
]

# Populate Artists Table
artist_ids = {}
i = 1
for _, artist in df[["Artist Name(s)"]].drop_duplicates().iterrows():
    artist_name = str(artist.values[0]).split(",")[0]
    artist_ids[artist_name] = i
    dob = generate_random_dob()
    country = random.choice(["USA", "UK", "France", "Germany", "Brazil"])
    query = "insert into Artists values (%s, %s, %s, %s)"
    values = [i, artist_name, dob, country]
    cursor_object.execute(query, values)
    i += 1

# Populate Albums Table
album_ids = {}
i = 1
for _, row in (
    df[
        [
            "Album Name",
            "Album Artist Name(s)",
        ]
    ]
    .drop_duplicates()
    .dropna()
    .iterrows()
):
    album_name = row["Album Name"]
    artist_name = str(row["Album Artist Name(s)"]).split(",")[0]
    release_date = generate_random_release()

    album_ids[album_name] = i
    artist_id = artist_ids.get(artist_name)
    if not artist_id:
        continue
    query = "insert into Albums values (%s, %s, %s, %s)"
    values = [i, artist_id, album_name, release_date]
    try:
        cursor_object.execute(query, values)
    except:
        pass
    i += 1

# Populate Genres Table
genre_ids = {}
i = 1
for _, row in df[["Artist Genres"]].drop_duplicates().dropna().iterrows():

    genre = str(row["Artist Genres"]).split(",")[0]

    if genre in genre_ids or not genre or genre == "":
        continue
    genre_ids[genre] = i
    country = random.choice(["USA", "UK", "France", "Germany", "Brazil"])
    query = "insert into Genres values (%s, %s, %s)"
    values = [i, genre, country]
    cursor_object.execute(query, values)
    i += 1

# Populate RecordLabels Table
label_ids = {}
i = 1
for _, row in df[["Label"]].drop_duplicates().dropna().iterrows():

    label = str(row["Label"]).split(",")[0]
    label_ids[label] = i
    address = random.choice(addresses)
    phone = generate_random_phone_number()
    query = "insert into RecordLabels values (%s, %s, %s, %s)"
    values = [i, label, phone, address]
    cursor_object.execute(query, values)
    i += 1

# Populate StreamingPlatforms Table
platform_ids = {}
i = 1
for platform in music_streaming_platforms:
    platform_ids[platform] = i
    subs = random.randint(1000000, 100000000)
    sub_fee = round(random.uniform(5.99, 14.99), 2)
    query = "insert into StreamingPlatforms values (%s, %s, %s, %s)"
    values = [i, platform, subs, sub_fee]
    cursor_object.execute(query, values)
    i += 1

# Populate Songs Table
song_ids = {}
i = 1
for _, row in (
    df[
        [
            "Track Duration (ms)",
            "Track Name",
            "Album Name",
            "Artist Name(s)",
            "Artist Genres",
            "Label",
        ]
    ]
    .drop_duplicates()
    .dropna()
    .iterrows()
):

    duration = round(float(row["Track Duration (ms)"]) / 1000)
    name = row["Track Name"]

    album_id = album_ids.get(row["Album Name"])
    artist_id = artist_ids.get(str(row["Artist Name(s)"]).split(",")[0])
    genre_id = genre_ids.get(str(row["Artist Genres"]).split(",")[0])
    label_id = label_ids.get(row["Label"])

    if not album_id or not artist_id or not genre_id or not label_id:
        continue
    song_ids[name] = i

    query = "insert into Songs values (%s, %s, %s, %s, %s, %s, %s)"
    values = [i, duration, name, genre_id, label_id, album_id, artist_id]
    cursor_object.execute(query, values)
    i += 1

# Populate Streams Table
for song_id in song_ids.values():
    for platform_id in platform_ids.values():
        streams = random.randint(100000, 10000000)
        query = "insert into Streams values (%s, %s, %s)"
        values = [platform_id, song_id, streams]
        cursor_object.execute(query, values)

# Populate Compose Table
query = "SELECT TrackID, ArtistID FROM Songs;"
cursor_object.execute(query)
mapping = cursor_object.fetchall()
for vals in mapping:
    query = "insert into Compose values (%s, %s)"
    values = [vals[1], vals[0]]
    cursor_object.execute(query, values)

# Commit all changes to database
my_connection.commit()
