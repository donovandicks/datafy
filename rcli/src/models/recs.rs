use crate::models::content::Content;
use prettytable::Row;
use serde::Deserialize;

#[derive(Deserialize, Debug)]
/// The recommendation model returned from the Datafy backend API
pub struct Recommendation {
    /// The name of the recommended song
    song: String,

    /// The list of artists performing the recommended song
    artists: Vec<String>,
}

impl Content for Recommendation {
    fn as_row(&self, _idx: &usize) -> Row {
        row!(&self.song, &self.artists.join(", "),)
    }
}
