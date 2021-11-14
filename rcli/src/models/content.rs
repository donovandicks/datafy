use crate::libs::url_builder::URLBuilder;
use prettytable::Row;
use serde::de::DeserializeOwned;

pub trait Content {
    fn as_row(&self, idx: &usize) -> Row;
}

pub trait ContentCollection {
    fn display(&self);
}

async fn retrieve_content<T>(endpoint: &str) -> Result<T, Box<dyn std::error::Error>>
where
    T: ContentCollection + DeserializeOwned,
{
    let resp = reqwest::get(endpoint).await?.json::<T>().await?;
    Ok(resp)
}

pub async fn display_content<T>(resource: &str)
where
    T: ContentCollection + DeserializeOwned,
{
    let endpoint = URLBuilder::new().with_resource(resource).build();
    let content: T = retrieve_content(&endpoint).await.unwrap();
    content.display();
}
