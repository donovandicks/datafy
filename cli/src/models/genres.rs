use crate::models::content::Content;
use prettytable::Row;
use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct Genre {
    /// The name of the genre
    name: String,

    /// Number of times the genre appeared
    count: i32,
}

impl Content for Genre {
    fn as_row(&self, idx: usize) -> Row {
        row!(idx + 1, &self.name, &self.count,)
    }
}
