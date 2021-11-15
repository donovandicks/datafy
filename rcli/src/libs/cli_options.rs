use crate::libs::url_builder::URLBuilder;
use crate::models::collections::{ArtistCollection, GenreCollection, SongCollection};
use crate::models::content::{retrieve_content, ContentCollection};
use dialoguer::{theme::ColorfulTheme, Input, Select};

enum CLIOptions {
    ArtistOptions {
        limit: String,
        time_range: String,
    },
    GenreOptions {
        limit: String,
        time_range: String,
        aggregate: String,
    },
    SongOptions {
        limit: String,
        time_range: String,
    },
}

fn get_limit() -> String {
    Input::with_theme(&ColorfulTheme::default())
        .with_prompt("Results Limit: ")
        .default(20.to_string())
        .validate_with(|input: &String| -> Result<(), &str> {
            match input.parse::<u32>() {
                Ok(_) => Ok(()),
                Err(_) => Err("Failed to parse limit. Value should be a positive integer."),
            }
        })
        .interact_text()
        .unwrap()
}

fn get_time_range() -> String {
    Input::with_theme(&ColorfulTheme::default())
        .with_prompt("Time Range: ")
        .default(String::from("medium_term"))
        .validate_with(|input: &String| -> Result<(), &str> {
            match input.to_lowercase().as_ref() {
                "short_term" | "medium_term" | "long_term" => Ok(()),
                _ => Err("Invalid term range. Value should be one of [short_term, medium_term, long_term]")
            }
        })
        .interact_text()
        .unwrap()
}

fn get_aggregate() -> String {
    let choices = ["true", "false"];
    let index = match Select::with_theme(&ColorfulTheme::default())
        .with_prompt("Aggregate Results: ")
        .items(&choices)
        .default(1)
        .interact()
    {
        Ok(index) => index,
        _ => panic!("Somehow received a value out of selection!"),
    };

    String::from(choices[index])
}

fn choose_artist_options() -> CLIOptions {
    CLIOptions::ArtistOptions {
        limit: get_limit(),
        time_range: get_time_range(),
    }
}

fn choose_song_options() -> CLIOptions {
    CLIOptions::SongOptions {
        limit: get_limit(),
        time_range: get_time_range(),
    }
}

fn choose_genre_options() -> CLIOptions {
    CLIOptions::GenreOptions {
        limit: get_limit(),
        time_range: get_time_range(),
        aggregate: get_aggregate(),
    }
}

pub async fn fetch_content(resource: &str) {
    let resource_lower = resource.to_lowercase();
    let opts = match resource_lower.as_ref() {
        "artists" => choose_artist_options(),
        "genres" => choose_genre_options(),
        "songs" => choose_song_options(),
        _ => unimplemented!(),
    };

    match opts {
        CLIOptions::ArtistOptions { limit, time_range } => {
            let url = URLBuilder::new()
                .with_resource(resource_lower.as_ref())
                .with_param("limit", limit)
                .with_param("time_range", time_range.to_lowercase())
                .build();

            retrieve_content::<ArtistCollection>(&url)
                .await
                .unwrap()
                .display();
        }
        CLIOptions::GenreOptions {
            limit,
            time_range,
            aggregate,
        } => {
            let url = URLBuilder::new()
                .with_resource(resource_lower.as_ref())
                .with_param("limit", limit)
                .with_param("time_range", time_range)
                .with_param("aggregate", aggregate)
                .build();

            retrieve_content::<GenreCollection>(&url)
                .await
                .unwrap()
                .display();
        }
        CLIOptions::SongOptions { limit, time_range } => {
            let url = URLBuilder::new()
                .with_resource(resource_lower.as_ref())
                .with_param("limit", limit)
                .with_param("time_range", time_range)
                .build();

            retrieve_content::<SongCollection>(&url)
                .await
                .unwrap()
                .display();
        }
    }
}
