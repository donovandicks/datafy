use crate::models::content::Content;
use prettytable::Row;
use serde::Deserialize;

#[derive(Deserialize, Debug)]
pub struct Song {
    name: String,
    artists: Vec<String>,
    popularity: u8,
    album: String,
    release_date: String,
    id: String,
}

impl Content for Song {
    fn as_row(&self, idx: &usize) -> Row {
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
