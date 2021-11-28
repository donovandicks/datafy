use crate::models::content::Content;
use prettytable::Row;
use serde::Deserialize;

#[derive(Deserialize, Debug)]
/// The artist model returned from the Datafy backend API
pub struct Artist {
    /// The name of the artist
    name: String,

    /// The popularity of the artist from 0 to 100
    popularity: i8,

    /// The total number of followers that the artist has
    followers: i32,

    /// The Spotify ID of the artist
    id: String,
}

impl Content for Artist {
    fn as_row(&self, idx: usize) -> Row {
        row!(
            idx + 1,
            &self.name,
            &self.popularity,
            &self.followers,
            &self.id
        )
    }
}
