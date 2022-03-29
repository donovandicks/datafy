CREATE TABLE playcount (
    track_id VARCHAR(80) PRIMARY KEY,
    last_played_timestamp BIGINT,
    total_play_count INTEGER
);

CREATE TABLE album (
  id VARCHAR(80) PRIMARY KEY,
  name VARCHAR(240)
);

CREATE TABLE artist (
  id VARCHAR(80) PRIMARY KEY,
  name VARCHAR(240)
);

CREATE TABLE track (
  id VARCHAR(80) PRIMARY KEY REFERENCES playcount (track_id),
  name VARCHAR(240),
  artist_id VARCHAR(80) REFERENCES artist (id),
  album_id VARCHAR(80) REFERENCES album (id),
  popularity INTEGER,
  acousticness DECIMAL(6, 5),
  danceability DECIMAL(4, 3),
  duration_ms INTEGER,
  energy DECIMAL(4, 3),
  instrumentalness DECIMAL(6, 5),
  loudness DECIMAL(6, 3),
  speechiness DECIMAL(5, 4),
  tempo DECIMAL(6, 3),
  valence DECIMAL(4, 3)
);
