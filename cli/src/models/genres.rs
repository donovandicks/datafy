use crate::models::content::Content;
use prettytable::Row;
use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
pub struct Genre {
    /// The name of the genre
    name: String,

    /// Number of times the genre appeared
    count: i32,
}

#[typetag::serde]
impl Content for Genre {
    fn as_row(&self, idx: usize) -> Row {
        row!(idx + 1, &self.name, &self.count,)
    }
}
