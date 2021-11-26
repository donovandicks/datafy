use crate::libs::inputs::{get_aggregate, get_item_ids, get_limit, get_time_range};

/// The possible CLI option variants
pub enum CLIOptions {
    /// The CLI options for the Artists resource
    Artist { limit: String, time_range: String },

    /// The CLI options for the Genres resource
    Genre {
        limit: String,
        time_range: String,
        aggregate: String,
    },

    /// The CLI options for the Recommendations resource
    Recommendation {
        seed_artists: String,
        seed_genres: String,
        seed_tracks: String,
    },

    /// The CLI options for the Songs resource
    Song { limit: String, time_range: String },
}

/// Prompt the user for inputs appropriate for the artists endpoint
pub fn choose_artist_opts() -> CLIOptions {
    CLIOptions::Artist {
        limit: get_limit(),
        time_range: get_time_range(),
    }
}

/// Prompt the user for inputs appropriate for the genres endpoint
pub fn choose_genre_opts() -> CLIOptions {
    CLIOptions::Genre {
        limit: get_limit(),
        time_range: get_time_range(),
        aggregate: get_aggregate(),
    }
}

/// Prompt the user for inputs appropriate for the recommendations endpoint
pub fn choose_rec_opts() -> CLIOptions {
    let seed_artists = get_item_ids("artist");
    let seed_genres = get_item_ids("genre");
    let seed_tracks = get_item_ids("track");

    if seed_artists.is_empty() && seed_genres.is_empty() && seed_tracks.is_empty() {
        println!("Must supply at least one seed value!");
        choose_rec_opts()
    } else if seed_artists.len() + seed_genres.len() + seed_tracks.len() > 5 {
        println!("Must supply fewer than 5 total seed values!");
        choose_rec_opts()
    } else {
        CLIOptions::Recommendation {
            seed_artists: seed_artists.join(","),
            seed_genres: seed_genres.join(","),
            seed_tracks: seed_tracks.join(","),
        }
    }
}

/// Prompt the user for inputs appropriate for the songs endpoint
pub fn choose_song_opts() -> CLIOptions {
    CLIOptions::Song {
        limit: get_limit(),
        time_range: get_time_range(),
    }
}
