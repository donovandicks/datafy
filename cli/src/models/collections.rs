use serde::Deserialize;

use crate::models::content::Content;
use std::boxed::Box;

#[derive(Deserialize, Debug)]
pub struct ContentCollection {
    /// A list of Content objects
    pub(crate) items: Vec<Box<dyn Content>>,

    /// A list of data field descriptors
    pub(crate) item_headers: Vec<String>,

    /// Number of items in the collection
    pub(crate) count: i32,
}
