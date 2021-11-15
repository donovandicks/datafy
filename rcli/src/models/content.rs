use prettytable::Row;
use serde::de::DeserializeOwned;

/// The core interface that all types of Datafy content responses must conform to
pub trait Content {
    /// Formats the members of a Content struct as a PrettyTable Row
    ///
    /// # Args
    ///
    /// * `idx` - A usize reference representing the index of this particular struct in a collection
    ///
    /// # Returns
    ///
    /// * A PrettyTable Row of the struct data
    fn as_row(&self, idx: &usize) -> Row;
}

/// An interface for a generic collection of Content objects
pub trait ContentCollection {
    /// Displays the contents of the collection in the terminal as a PrettyTable Table
    fn display(&self);
}

/// Retrieves content of type `T` from the Datafy backend
///
/// # Args
///
/// * `endpoint` - A str reference that serves as the API endpoint from which to request data
///
/// # Returns
///
/// * A `Result` containing either the data retrieved from the API or an error
///     received when making the request
pub async fn retrieve_content<T>(endpoint: &str) -> Result<T, Box<dyn std::error::Error>>
where
    T: ContentCollection + DeserializeOwned,
{
    let resp = reqwest::get(endpoint).await?.json::<T>().await?;
    Ok(resp)
}
