mod libs;
mod models;

#[macro_use]
extern crate prettytable;
use dialoguer::{theme::ColorfulTheme, Select};
use libs::url_builder::build_url;
use models::artists::display_artists;

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
            0 => display_artists().await,
            1 | 2 => {
                println!("Selected {}", String::from(content_choices[index]));
                build_url();
                continue;
            }
            _ => {
                println!("Goodbye!");
                break;
            }
        }
    }

    Ok(())
}
