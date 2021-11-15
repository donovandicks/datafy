use crate::libs::url_builder::URLBuilder;
use crate::models::collections::ArtistCollection;
use crate::models::content::{retrieve_content, ContentCollection};
use dialoguer::{theme::ColorfulTheme, Input};

enum CLIOptions {
    ArtistOptions { limit: String, time_range: String },
}

fn choose_artist_options() -> CLIOptions {
    let limit: String = Input::with_theme(&ColorfulTheme::default())
        .with_prompt("Results Limit: ")
        .default(20.to_string())
        .validate_with(|input: &String| -> Result<(), &str> {
            match input.parse::<u32>() {
                Ok(_) => Ok(()),
                Err(_) => Err("Failed to parse limit. Value should be a positive integer."),
            }
        })
        .interact_text()
        .unwrap();

    let time_range: String = Input::with_theme(&ColorfulTheme::default())
        .with_prompt("Time Range: ")
        .default(String::from("medium_term"))
        .validate_with(|input: &String| -> Result<(), &str> {
            match input.to_lowercase().as_ref() {
                "short_term" | "medium_term" | "long_term" => Ok(()),
                _ => Err("Invalid term range. Value should be one of [short_term, medium_term, long_term]")
            }
        })
        .interact_text()
        .unwrap();

    CLIOptions::ArtistOptions {
        limit: limit,
        time_range: time_range,
    }
}

pub async fn fetch_content(resource: &str) {
    let opts = match resource.to_lowercase().as_ref() {
        "artists" => choose_artist_options(),
        _ => unimplemented!(),
    };

    match opts {
        CLIOptions::ArtistOptions { limit, time_range } => {
            let url = URLBuilder::new()
                .with_resource(resource)
                .with_param("limit", limit)
                .with_param("time_range", time_range.to_lowercase())
                .build();

            retrieve_content::<ArtistCollection>(&url)
                .await
                .unwrap()
                .display();
        }
    }
}
