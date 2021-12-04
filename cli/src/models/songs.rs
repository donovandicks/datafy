use crate::models::content::Content;
use prettytable::Row;
use serde::{Deserialize, Serialize};

#[derive(Deserialize, Debug, Serialize)]
/// The song model returned from the Datafy backend API
pub struct Song {
    /// The name of the song
    name: String,

    /// The name of the artists performing the song
    artists: Vec<String>,

    /// The popularity of the song from 0 to 100
    popularity: u8,

    /// The album from which the song is
    album: String,

    /// The date when the song was first released
    release_date: String,

    /// The Spotify ID of the song
    id: String,
}

#[typetag::serde]
impl Content for Song {
    fn as_row(&self, idx: usize) -> Row {
        row!(
            idx + 1,
            &self.name,
            &self.artists.join(", "),
            &self.popularity,
            &self.album,
            &self.release_date,
            &self.id
        )
    }
}
