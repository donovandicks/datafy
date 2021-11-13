use prettytable::{Row, Table};

struct Artist {
    name: String,
}

impl Artist {
    fn as_row(&self) -> Row {
        row!(&self.name)
    }
}

struct ArtistCollection {
    items: Vec<Artist>,
}

struct Artists {
    data: ArtistCollection,
}

impl Artists {
    fn display(&self) {
        let mut table = Table::new();
        let rows: Vec<Row> = self.data.items.iter().map(|item| item.as_row()).collect();
        for row in rows.iter() {
            table.add_row(row.to_owned());
        }
        table.printstd();
    }
}

pub fn display_artists() {
    let artists = Artists {
        data: ArtistCollection {
            items: vec![Artist {
                name: String::from("Archie Shepp"),
            }],
        },
    };

    artists.display();
}
