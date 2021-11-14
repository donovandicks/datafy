use crate::models::content::{Content, ContentCollection};
use prettytable::{Row, Table};
use serde::Deserialize;

#[derive(Deserialize, Debug)]
struct Artist {
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

#[derive(Deserialize, Debug)]
pub struct ArtistCollection {
    items: Vec<Artist>,
}

impl ContentCollection for ArtistCollection {
    fn display(&self) {
        let mut table = Table::new();
        table.add_row(row!("Rank", "Name", "Popularity", "Followers", "ID"));
        let rows: Vec<Row> = self
            .items
            .iter()
            .enumerate()
            .map(|(idx, item)| item.as_row(&idx))
            .collect();
        for row in rows.iter() {
            table.add_row(row.to_owned());
        }
        table.printstd();
    }
}

async fn retrieve_artists() -> Result<ArtistCollection, Box<dyn std::error::Error>> {
    let resp = reqwest::get("http://0.0.0.0:5000/artists?limit=5")
        .await?
        .json::<ArtistCollection>()
        .await?;

    println!("{:?}", resp);
    Ok(resp)
}

pub async fn display_artists() {
    let artists = retrieve_artists().await;
    artists.unwrap().display();
}
