mod libs;
mod models;

#[macro_use]
extern crate prettytable;
use dialoguer::{theme::ColorfulTheme, Select};
use models::collections::{ArtistCollection, GenreCollection, SongCollection};
use models::content::display_content;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    loop {
        let content_choices = ["Artists", "Songs", "Genres", "Exit"];

        let index = match Select::with_theme(&ColorfulTheme::default())
            .with_prompt("Select your desired content from the following options:")
            .items(&content_choices)
            .default(0)
            .interact()
        {
            Ok(index) => index,
            _ => continue,
        };

        match index {
            // TODO: These branch arms should point to other methods where the
            // user can select/input other parameters which are then passed to
            // the display content method
            0 => display_content::<ArtistCollection>("artists").await,
            1 => display_content::<SongCollection>("songs").await,
            2 => display_content::<GenreCollection>("genres").await,
            _ => {
                println!("Goodbye!");
                break;
            }
        }
    }

    Ok(())
}
