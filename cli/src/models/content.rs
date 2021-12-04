use std::fmt::Debug;

use crate::models::collections::ContentCollection;
use prettytable::{Row, Table};

/// The core interface that all types of Datafy content responses must conform to
#[typetag::serde(tag = "content")]
pub trait Content {
    /// Formats the members of a Content struct as a `PrettyTable` Row
    ///
    /// # Args
    ///
    /// * `idx` - A usize reference representing the index of this particular struct in a collection
    ///
    /// # Returns
    ///
    /// * A `PrettyTable` Row of the struct data
    fn as_row(&self, idx: usize) -> Row;
}

impl Debug for dyn Content {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        // TODO: Implement a more useful debug
        write!(f, "<Content>")
    }
}

/// Constructs a `PrettyTable` from the data in a `ContentCollection` which can
/// then be displayed to a terminal
///
/// # Args
///
/// * `content` - A collection of content to display
///
/// # Returns
///
/// * `table` - The pretty formatted table of the collection
fn generate_table(content: ContentCollection) -> Table {
    let mut table = Table::new();
    table.add_row(Row::from_iter(content.item_headers));
    content
        .items
        .iter()
        .enumerate()
        .map(|(idx, item)| item.as_row(idx))
        .for_each(|row| {
            table.add_row(row);
        });

    table
}

/// Displays a table containing the data in a `ContentCollection` to stdout
///
/// # Args
///
/// * `content` - A collection of content to display
pub fn display(content: ContentCollection) {
    generate_table(content).printstd();
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
pub async fn retrieve_content(
    endpoint: &str,
) -> Result<ContentCollection, Box<dyn std::error::Error>> {
    let resp = reqwest::get(endpoint)
        .await?
        .json::<ContentCollection>()
        .await?;
    Ok(resp)
}
