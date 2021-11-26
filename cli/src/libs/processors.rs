use crate::libs::{
    options::{
        choose_artist_opts, choose_genre_opts, choose_rec_opts, choose_song_opts, CLIOptions,
    },
    url_builder::URLBuilder,
};
use crate::models::{
    collections::{ArtistCollection, GenreCollection, RecommendationCollection, SongCollection},
    content::{retrieve_content, ContentCollection},
};
use std::boxed::Box;

/// Requests and returns a content collection from the backend
///
/// # Args
///
/// * `builder` - A reference to an instantiated `URLBuilder` that already contains
///     resource
/// * `opts` - A reference to a `CLIOption` variant that is populated with user input
///
/// # Returns
///
/// * A pointer to heap-allocated memory for an underlying content collection trait
///     object. The specific content collection is determined by the opts variant
///     but this is abstracted away.
async fn fetch_content(builder: &mut URLBuilder, opts: &CLIOptions) -> Box<dyn ContentCollection> {
    match opts {
        CLIOptions::Artist { limit, time_range } => Box::new(
            retrieve_content::<ArtistCollection>(
                &builder
                    .with_params(vec![("limit", limit), ("time_range", time_range)])
                    .build(),
            )
            .await
            .unwrap(),
        ),

        CLIOptions::Genre {
            limit,
            time_range,
            aggregate,
        } => Box::new(
            retrieve_content::<GenreCollection>(
                &builder
                    .with_params(vec![
                        ("limit", limit),
                        ("time_range", &time_range.to_lowercase()),
                        ("aggregate", aggregate),
                    ])
                    .build(),
            )
            .await
            .unwrap(),
        ),

        CLIOptions::Song { limit, time_range } => Box::new(
            retrieve_content::<SongCollection>(
                &builder
                    .with_params(vec![
                        ("limit", limit),
                        ("time_range", &time_range.to_lowercase()),
                    ])
                    .build(),
            )
            .await
            .unwrap(),
        ),

        CLIOptions::Recommendation {
            seed_artists,
            seed_genres,
            seed_tracks,
        } => Box::new(
            retrieve_content::<RecommendationCollection>(
                &builder
                    .with_params(vec![
                        ("seed_artists", seed_artists),
                        ("seed_genres", seed_genres),
                        ("seed_tracks", seed_tracks),
                    ])
                    .build(),
            )
            .await
            .unwrap(),
        ),
    }
}

/// Prompts the user for the appropriate options based on the given resource and
/// returns the appropriate `CLIOptions` enum variant with the users selections/input
///
/// # Args
///
/// * `resource` - A reference to the lowercased API resource
///
/// # Returns
///
/// * The `CLIOptions` variant appropriate for the given resource containing all
///     values supplied by the user
fn get_user_selections(resource: &str) -> CLIOptions {
    match resource {
        "artists" => choose_artist_opts(),
        "genres" => choose_genre_opts(),
        "recommendations" => choose_rec_opts(),
        "songs" => choose_song_opts(),
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

    fetch_content(builder, &opts).await.display();
}
