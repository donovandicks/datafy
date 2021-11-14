use crate::models::artists::Artist;
use crate::models::content::{Content, ContentCollection};
use crate::models::songs::Song;
use prettytable::{Row, Table};
use serde::Deserialize;
use std::collections::HashMap;

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

#[derive(Deserialize, Debug)]
pub struct SongCollection {
    items: Vec<Song>,
}

impl ContentCollection for SongCollection {
    fn display(&self) {
        let mut table = Table::new();
        table.add_row(row!(
            "Rank",
            "Name",
            "Artists",
            "Popularity",
            "Album",
            "Release Date",
            "ID"
        ));
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

#[derive(Deserialize, Debug)]
pub struct GenreCollection {
    items: HashMap<String, u8>,
}

impl ContentCollection for GenreCollection {
    fn display(&self) {
        let mut table = Table::new();
        table.add_row(row!("Genre", "Count",));
        let rows: Vec<Row> = self
            .items
            .iter()
            .map(|(key, value)| row!(key, value))
            .collect();
        for row in rows.iter() {
            table.add_row(row.to_owned());
        }
        table.printstd();
    }
}
