use crate::libs::{
    options::{
        choose_artist_opts, choose_genre_opts, choose_rec_opts, choose_song_opts, CLIOptions,
    },
    url_builder::URLBuilder,
};
use crate::models::content::{display, retrieve_content};

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
        "recs" => choose_rec_opts(),
        "songs" => choose_song_opts(),
        _ => unimplemented!(),
    }
}

/// Constructs the endpoint URL with all passed parameters
///
/// # Args
///
/// * `builder` - A mut ref to a `URLBuilder` instance that has been instantiated
///     with a resource
/// * `opts` - A ref to a `CLIOptions` enum variant containing the user defined
///     options which will be interpreted as query params in the URL
///
/// # Returns
///
/// * The constructed URL with resource and query params
fn build_url(builder: &mut URLBuilder, opts: &CLIOptions) -> String {
    match opts {
        CLIOptions::Artist { limit, time_range } => builder
            .with_params(vec![("limit", limit), ("time_range", time_range)])
            .build(),

        CLIOptions::Genre {
            limit,
            time_range,
            aggregate,
        } => builder
            .with_params(vec![
                ("limit", limit),
                ("time_range", &time_range.to_lowercase()),
                ("aggregate", aggregate),
            ])
            .build(),

        CLIOptions::Song { limit, time_range } => builder
            .with_params(vec![
                ("limit", limit),
                ("time_range", &time_range.to_lowercase()),
            ])
            .build(),

        CLIOptions::Recommendation {
            seed_artists,
            seed_genres,
            seed_tracks,
            limit,
        } => builder
            .with_params(vec![
                ("seed_artists", seed_artists),
                ("seed_genres", seed_genres),
                ("seed_tracks", seed_tracks),
                ("limit", limit),
            ])
            .build(),
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
    let endpoint = build_url(builder, &opts);
    let content = retrieve_content(endpoint.as_str()).await.unwrap();

    display(content);
}
