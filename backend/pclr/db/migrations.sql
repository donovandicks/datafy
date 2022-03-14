CREATE TABLE album (
    album_id VARCHAR(80) PRIMARY KEY,
    album_name VARCHAR(240)
);
CREATE TABLE artist (
    artist_id VARCHAR(80) PRIMARY KEY,
    artist_name varhcar(240)
);
CREATE TABLE track (
    track_id VARCHAR(80) PRIMARY KEY,
    track_name VARCHAR(240),
    artist_id VARCHAR(80),
    album_id VARCHAR(80),
    CONSTRAINT fk_artist FOREIGN KEY(artist_id) REFERENCES artist(artist_id),
    CONSTRAINT fk_album FOREIGN KEY(album_id) REFERENCES album(album_id)
);
CREATE TABLE play_count (
    track_id VARCHAR(80) PRIMARY KEY,
    last_played_timestamp BIGINT,
    total_play_count INTEGER,
    CONSTRAINT fk_track FOREIGN KEY(track_id) REFERENCES track(track_id)
);
