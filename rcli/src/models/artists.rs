use crate::models::content::Content;
use prettytable::Row;
use serde::Deserialize;

#[derive(Deserialize, Debug)]
pub struct Artist {
    name: String,
    popularity: u8,
    followers: u32,
    id: String,
}

impl Content for Artist {
    fn as_row(&self, idx: &usize) -> Row {
        row!(
            idx + 1,
            &self.name,
            &self.popularity,
            &self.followers,
            &self.id
        )
    }
}
