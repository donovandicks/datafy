use prettytable::Row;
use serde::de::DeserializeOwned;

pub trait Content {
    fn as_row(&self, idx: &usize) -> Row;
}

pub trait ContentCollection {
    fn display(&self);
}

pub async fn retrieve_content<T>(endpoint: &str) -> Result<T, Box<dyn std::error::Error>>
where
    T: ContentCollection + DeserializeOwned,
{
    let resp = reqwest::get(endpoint).await?.json::<T>().await?;
    Ok(resp)
}
