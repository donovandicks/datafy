CREATE TABLE album (
    album_id VARCHAR(80) PRIMARY KEY,
    album_name VARCHAR(240)
);
CREATE TABLE artist (
    artist_id VARCHAR(80) PRIMARY KEY,
    artist_name VARCHAR(240)
);
CREATE TABLE track (
    track_id VARCHAR(80) PRIMARY KEY,
    track_name VARCHAR(240),
    artist_id VARCHAR(80),
    album_id VARCHAR(80),
    popularity INTEGER,
    CONSTRAINT fk_artist FOREIGN KEY(artist_id) REFERENCES artist(artist_id),
    CONSTRAINT fk_album FOREIGN KEY(album_id) REFERENCES album(album_id)
);
CREATE TABLE playcount (
    track_id VARCHAR(80) PRIMARY KEY,
    last_played_timestamp BIGINT,
    total_play_count INTEGER,
    CONSTRAINT fk_track FOREIGN KEY(track_id) REFERENCES track(track_id)
);
CREATE TABLE trackdetail(
    track_id VARCHAR(80) PRIMARY KEY,
    acousticness DECIMAL(5),
    danceability DECIMAL(3),
    duration_ms INT,
    energy DECIMAL(3),
    instrumentalness DECIMAL(5),
    loudness DECIMAL(3),
    speechiness DECIMAL(4),
    tempo DECIMAL(3),
    valence DECIMAL(3),
    CONSTRAINT fk_track FOREIGN KEY(track_id) REFERENCES track(track_id)
);
