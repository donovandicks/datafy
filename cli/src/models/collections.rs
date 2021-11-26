use crate::models::artists::Artist;
use crate::models::content::{Content, ContentCollection};
use crate::models::recs::Recommendation;
use crate::models::songs::Song;
use prettytable::Table;
use serde::Deserialize;
use std::collections::HashMap;

#[derive(Deserialize, Debug)]
/// Model for data retrieved from the artists API endpoint
pub struct ArtistCollection {
    /// A list of Artist objects
    items: Vec<Artist>,
}

impl ContentCollection for ArtistCollection {
    fn display(&self) {
        let mut table = Table::new();
        table.add_row(row!("Rank", "Artist", "Popularity", "Followers", "ID"));
        self.items
            .iter()
            .enumerate()
            .map(|(idx, item)| item.as_row(idx))
            .for_each(|row| {
                table.add_row(row);
            });

        table.printstd();
    }
}

#[derive(Deserialize, Debug)]
/// Model for data retrieved from the artists API endpoint
pub struct SongCollection {
    /// A list of Song objects
    items: Vec<Song>,
}

impl ContentCollection for SongCollection {
    fn display(&self) {
        let mut table = Table::new();
        table.add_row(row!(
            "Rank",
            "Song",
            "Artists",
            "Popularity",
            "Album",
            "Release Date",
            "ID"
        ));
        self.items
            .iter()
            .enumerate()
            .map(|(idx, item)| item.as_row(idx))
            .for_each(|row| {
                table.add_row(row);
            });

        table.printstd();
    }
}

#[derive(Deserialize, Debug)]
/// Model for data retrieved from the genres API endpoint
pub struct GenreCollection {
    /// A map from genre name to count
    items: HashMap<String, u8>,
}

impl ContentCollection for GenreCollection {
    fn display(&self) {
        let mut table = Table::new();
        table.add_row(row!("Genre", "Count",));
        self.items
            .iter()
            .map(|(key, value)| row!(key, value))
            .for_each(|row| {
                table.add_row(row);
            });

        table.printstd();
    }
}

#[derive(Deserialize, Debug)]
/// Model for data retrieved from the genres API endpoint
pub struct RecommendationCollection {
    /// A list of Recommendation objects
    items: Vec<Recommendation>,
}

impl ContentCollection for RecommendationCollection {
    fn display(&self) {
        let mut table = Table::new();
        table.add_row(row!("Song", "Artists"));
        self.items
            .iter()
            .enumerate()
            .map(|(idx, item)| item.as_row(idx))
            .for_each(|row| {
                table.add_row(row);
            });

        table.printstd();
    }
}
