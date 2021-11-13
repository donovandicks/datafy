mod api_options;

use dialoguer::{theme::ColorfulTheme, Select};

fn main() {
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
            0 | 1 | 2 => println!("Selected {}", String::from(content_choices[index])),
            _ => {
                println!("Goodbye!");
                break;
            }
        };
    }
}
