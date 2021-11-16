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

async fn display_content<T>(url: &str)
where
    T: ContentCollection + DeserializeOwned,
{
    retrieve_content::<T>(url).await.unwrap().display();
}

async fn fetch_artists(builder: &mut URLBuilder, limit: &str, time_range: &str) {
    let url = builder
        .with_param("limit", limit)
        .with_param("time_range", time_range)
        .build();

    display_content::<ArtistCollection>(&url).await;
}

async fn fetch_genres(builder: &mut URLBuilder, limit: &str, time_range: &str, aggregate: &str) {
    let url = builder
        .with_param("limit", limit)
        .with_param("time_range", time_range)
        .with_param("aggregate", aggregate)
        .build();

    display_content::<GenreCollection>(&url).await;
}

async fn fetch_songs(builder: &mut URLBuilder, limit: &str, time_range: &str) {
    let url = builder
        .with_param("limit", limit)
        .with_param("time_range", time_range)
        .build();

    display_content::<SongCollection>(&url).await;
}

async fn fetch_recs(
    builder: &mut URLBuilder,
    seed_artists: &str,
    seed_genres: &str,
    seed_tracks: &str,
) {
    let url = builder
        .with_param("seed_artists", seed_artists)
        .with_param("seed_genres", seed_genres)
        .with_param("seed_tracks", seed_tracks)
        .build();

    display_content::<RecommendationCollection>(&url).await;
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

    // Temp var raw_builder necessary to avoid E0716 where the temp value is dropped
    // before it is referenced later
    let mut raw_builder: URLBuilder = URLBuilder::new();
    let builder = raw_builder.with_resource(&resource_lower);

    match opts {
        CLIOptions::Artist { limit, time_range } => {
            fetch_artists(builder, &limit, &time_range.to_lowercase()).await;
        }

        CLIOptions::Genre {
            limit,
            time_range,
            aggregate,
        } => {
            fetch_genres(builder, &limit, &time_range.to_lowercase(), &aggregate).await;
        }

        CLIOptions::Song { limit, time_range } => {
            fetch_songs(builder, &limit, &time_range.to_lowercase()).await;
        }

        CLIOptions::Recommendation {
            seed_artists,
            seed_genres,
            seed_tracks,
        } => {
            fetch_recs(builder, &seed_artists, &seed_genres, &seed_tracks).await;
        }
    }
}
