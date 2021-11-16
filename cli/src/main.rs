mod libs;
mod models;

#[macro_use]
extern crate prettytable;
use crate::libs::processors::process_request;
use dialoguer::{theme::ColorfulTheme, Select};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    loop {
        let content_choices = ["Artists", "Genres", "Recommendations", "Songs", "Exit"];

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
            0 | 1 | 2 | 3 => process_request(content_choices[index]).await,
            _ => {
                println!("Goodbye!");
                break;
            }
        }
    }

    Ok(())
}
