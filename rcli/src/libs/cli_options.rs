use crate::libs::url_builder::URLBuilder;
use crate::models::collections::{
    ArtistCollection, GenreCollection, RecommendationCollection, SongCollection,
};
use crate::models::content::{retrieve_content, ContentCollection};
use dialoguer::{theme::ColorfulTheme, Confirm, Input, Select};

/// The possible CLI option variants
enum CLIOptions {
    /// The CLI options for the Artists resource
    ArtistOptions { limit: String, time_range: String },

    /// The CLI options for the Genres resource
    GenreOptions {
        limit: String,
        time_range: String,
        aggregate: String,
    },

    /// The CLI options for the Recommendations resource
    RecommendationOptions {
        seed_artists: String,
        seed_genres: String,
        seed_tracks: String,
    },

    /// The CLI options for the Songs resource
    SongOptions { limit: String, time_range: String },
}

/// Get the query `limit` parameter from the user. The value must be within the
/// bounds of u32
///
/// # Returns
///
/// * The limit formatted as a string
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

/// Get the query `time_range` parameter from the user.
///
/// The possible choices are below:
///
/// * `short_term` - the last 4 weeks
/// * `medium_term` - the last 6 months
/// * `long_term` - the last 3 years
///
/// # Returns
///
/// * The selected time_range
fn get_time_range() -> String {
    let choices = ["short_term", "medium_term", "long_term"];

    let index = Select::with_theme(&ColorfulTheme::default())
        .with_prompt("Time Range: ")
        .items(&choices)
        .default(1)
        .interact()
        .unwrap();

    String::from(choices[index])
}

/// Get the query `aggregate` parameter from the user
///
/// # Returns
///
/// * A string boolean
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

/// Get input item IDs from the user
///
/// # Returns
///
/// * The comma-separated string of the user-supplied IDs
fn get_item_ids(item: &str) -> String {
    let mut items = vec![];

    if !Confirm::with_theme(&ColorfulTheme::default())
        .with_prompt(format!("Would you like to enter {} IDs?", item))
        .default(false)
        .wait_for_newline(true)
        .interact()
        .unwrap()
    {
        return String::from("");
    }

    loop {
        let input: String = Input::with_theme(&ColorfulTheme::default())
            .with_prompt(format!("{} ID: ", item))
            .interact_text()
            .unwrap();

        items.push(input);

        if !Confirm::with_theme(&ColorfulTheme::default())
            .with_prompt(format!("Would you like to enter another {} ID?", item))
            .default(false)
            .wait_for_newline(true)
            .interact()
            .unwrap()
        {
            break;
        }
    }

    items.join(",")
}

/// Prompt the user for inputs appropriate for the artists endpoint
fn choose_artist_options() -> CLIOptions {
    CLIOptions::ArtistOptions {
        limit: get_limit(),
        time_range: get_time_range(),
    }
}

/// Prompt the user for inputs appropriate for the genres endpoint
fn choose_genre_options() -> CLIOptions {
    CLIOptions::GenreOptions {
        limit: get_limit(),
        time_range: get_time_range(),
        aggregate: get_aggregate(),
    }
}

/// Prompt the user for inputs appropriate for the recommendations endpoint
fn choose_rec_options() -> CLIOptions {
    CLIOptions::RecommendationOptions {
        seed_artists: get_item_ids("artist"),
        seed_genres: get_item_ids("genre"),
        seed_tracks: get_item_ids("track"),
    }
}

/// Prompt the user for inputs appropriate for the songs endpoint
fn choose_song_options() -> CLIOptions {
    CLIOptions::SongOptions {
        limit: get_limit(),
        time_range: get_time_range(),
    }
}

/// Fetches the appropriate content for the supplied resource and displays the
/// results in the terminal
///
/// # Args
///
/// * `resource` - A str reference for the API resource from which to get content
pub async fn fetch_content(resource: &str) {
    let resource_lower = resource.to_lowercase();
    let opts = match resource_lower.as_ref() {
        "artists" => choose_artist_options(),
        "genres" => choose_genre_options(),
        "recommendations" => choose_rec_options(),
        "songs" => choose_song_options(),
        _ => unimplemented!(),
    };

    match opts {
        CLIOptions::ArtistOptions { limit, time_range } => {
            let url = URLBuilder::new()
                .with_resource(resource_lower.as_ref())
                .with_param("limit", limit.as_ref())
                .with_param("time_range", time_range.to_lowercase().as_ref())
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
                .with_param("limit", limit.as_ref())
                .with_param("time_range", time_range.to_lowercase().as_ref())
                .with_param("aggregate", aggregate.as_ref())
                .build();

            retrieve_content::<GenreCollection>(&url)
                .await
                .unwrap()
                .display();
        }
        CLIOptions::SongOptions { limit, time_range } => {
            let url = URLBuilder::new()
                .with_resource(resource_lower.as_ref())
                .with_param("limit", limit.as_ref())
                .with_param("time_range", time_range.to_lowercase().as_ref())
                .build();

            retrieve_content::<SongCollection>(&url)
                .await
                .unwrap()
                .display();
        }
        CLIOptions::RecommendationOptions {
            seed_artists,
            seed_genres,
            seed_tracks,
        } => {
            let url = URLBuilder::new()
                .with_resource(resource_lower.as_ref())
                .with_param("seed_artists", seed_artists.as_ref())
                .with_param("seed_genres", seed_genres.as_ref())
                .with_param("seed_tracks", seed_tracks.as_ref())
                .build();

            retrieve_content::<RecommendationCollection>(&url)
                .await
                .unwrap()
                .display();
        }
    }
}
