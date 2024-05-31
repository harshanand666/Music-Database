# Overview
This is a simple Dash based web app used to query a music database. The database was built using [Spotify's top 10000 songs dataset](https://www.kaggle.com/datasets/joebeachcapital/top-10000-spotify-songs-1960-now) with a few complex queries. The frontend was built using the Dash framework and the database was built using MySQL.

# Database Design
The database has the following entities and relationships, as well as the supported queries: 

## Entities
1. Songs (TrackID, TrackName, Duration)
2. Artists (ArtistID, ArtistName, Nationality)
3. Genres (GenreID, GenreName, Origin)
4. Record Labels (LabelID, LabelName, Address, PhoneNumber)
5. Albums (AlbumID, AlbumName, ReleaseDate)
6. Streaming Platforms (PlatformID, PlatformName, SubscriptionFee, TotalSubscribers)

## Relationships
1. Compose (Artists, Songs)
2. Has (Artists, Albums) - identifying relationship
3. Streams (Platforms, Songs)
4. Belongs to (Genres, Songs)
5. Produces (Labels, Songs)
6. Comprises (Albums, Songs)

## Queries
1. List the number of songs by each artist with a duration of less than 5 minutes
2. List record labels ordered by the number of streams of all produced songs in descending
order
3. List the top 10 artists with the greatest number of songs in descending order
4. List the number of albums recorded each year by a particular artist
5. List the artist and album for which there are no songs with more than 200000 streams
6. List the genres sorted by the average number of streams per song in that genre
7. List the number of songs per genre grouped by artist
8. List the number of albums where number of songs are greater than 10 for a given genre
9. List the number of songs for an artist on different streaming platforms along with their
average duration and number of streams
10. List the number of albums released each year sorted in ascending order
11. List the 5 youngest artists with greater than 15 songs and greater than 2 albums

## ER Diagram
![ER Diagram](https://github.com/harshanand666/Music-Database/blob/main/ER_Diagram.png)

## Relational Schema
![Relational Schema](https://github.com/harshanand666/Music-Database/blob/main/Relational_Schema.png)

## Data
The following dataset from Kaggle was used to get the majority of the attributes:
[Spotify's top 10000 songs dataset](https://www.kaggle.com/datasets/joebeachcapital/top-10000-spotify-songs-1960-now).
Attributes covered in the dataset:
- Songs: TrackName, Duration, ReleaseDate 
- Artists: ArtistID, ArtistName
- Albums: AlbumID, AlbumName, ReleaseDate 
- Streams: NumberOfStreams
- Record Labels: LabelName 
- Genres: Name

Randomly generated attributes:
- Artists: DOB, Nationality
- Albums: ReleaseDate
- Genres: Origin
- Record Labels: Address, PhoneNumber
- Streaming Platforms: PlatformName, SubscriptionFee, TotalSubscribers

# Usage
- A MySQL server is required to run the code. Both the insertion script as well as the app.py script require setting the correct config (username and password) before running them to ensure all commands are executed correctly.
- The [create_tables.sql](https://github.com/harshanand666/Music-Database/blob/main/create_tables.sql) file contains the SQL commands to create the necessary tables.
- The [insert_data.py](https://github.com/harshanand666/Music-Database/blob/main/insert_data.py) script reads in the dataset (named as data.csv in the same folder), generates the required random attributes, and inserts all the records into the corresponding tables. This needs to be run once.
- The [app.py](https://github.com/harshanand666/Music-Database/blob/main/app.py) script runs the Dash app and allows the user to execute the abovementioned queries.