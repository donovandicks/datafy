use crate::libs::{
    options::{
        choose_artist_options, choose_genre_options, choose_rec_options, choose_song_options,
        CLIOptions,
    },
    url_builder::URLBuilder,
};
use crate::models::{
    collections::{ArtistCollection, GenreCollection, RecommendationCollection, SongCollection},
    content::{retrieve_content, ContentCollection},
};
use serde::de::DeserializeOwned;
use std::boxed::Box;

async fn fetch_content<T>(url: &str) -> T
where
    T: ContentCollection + DeserializeOwned,
{
    retrieve_content::<T>(url).await.unwrap()
}

fn get_user_selections(resource: &str) -> CLIOptions {
    match resource {
        "artists" => choose_artist_options(),
        "genres" => choose_genre_options(),
        "recommendations" => choose_rec_options(),
        "songs" => choose_song_options(),
        _ => unimplemented!(),
    }
}

/// Fetches the appropriate content for the supplied resource and displays the
/// results in the terminal
///
/// # Args
///
/// * `resource` - A str reference for the API resource from which to get content
pub async fn process_request(resource: &str) {
    let resource_lower = resource.to_lowercase();
    let opts = get_user_selections(&resource_lower);

    // Temp var raw_builder necessary to avoid E0716 where the temp value is dropped
    // before it is referenced later
    let mut raw_builder: URLBuilder = URLBuilder::new();
    let builder = raw_builder.with_resource(&resource_lower);

    let content: Box<dyn ContentCollection> = match opts {
        CLIOptions::Artist { limit, time_range } => Box::new(
            fetch_content::<ArtistCollection>(
                &builder
                    .with_params(vec![("limit", &limit), ("time_range", &time_range)])
                    .build(),
            )
            .await,
        ),

        CLIOptions::Genre {
            limit,
            time_range,
            aggregate,
        } => Box::new(
            fetch_content::<GenreCollection>(
                &builder
                    .with_params(vec![
                        ("limit", &limit),
                        ("time_range", &time_range.to_lowercase()),
                        ("aggregate", &aggregate),
                    ])
                    .build(),
            )
            .await,
        ),

        CLIOptions::Song { limit, time_range } => Box::new(
            fetch_content::<SongCollection>(
                &builder
                    .with_params(vec![
                        ("limit", &limit),
                        ("time_range", &time_range.to_lowercase()),
                    ])
                    .build(),
            )
            .await,
        ),

        CLIOptions::Recommendation {
            seed_artists,
            seed_genres,
            seed_tracks,
        } => Box::new(
            fetch_content::<RecommendationCollection>(
                &builder
                    .with_params(vec![
                        ("seed_artists", &seed_artists),
                        ("seed_genres", &seed_genres),
                        ("seed_tracks", &seed_tracks),
                    ])
                    .build(),
            )
            .await,
        ),
    };

    content.display();
}
