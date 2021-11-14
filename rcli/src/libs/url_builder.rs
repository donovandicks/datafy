use std::fmt::Display;

pub struct URLBuilder {
    base: String,
    resource: String,
    params: Vec<String>,
}

impl URLBuilder {
    pub fn new() -> URLBuilder {
        URLBuilder {
            base: String::from("http://0.0.0.0:5000"),
            resource: String::from(""),
            params: vec![],
        }
    }

    pub fn with_param<'a, T>(&'a mut self, key: &str, value: T) -> &'a mut URLBuilder
    where
        T: Display,
    {
        self.params.push(format!("{}={}", key, value));
        self
    }

    pub fn with_resource<'a>(&'a mut self, resource: &str) -> &'a mut URLBuilder {
        if self.resource.is_empty() {
            self.resource = String::from(resource);
        }

        self
    }

    pub fn build(&self) -> String {
        if self.resource.is_empty() {
            panic!("Endpoint resource not defined!")
        }

        format!("{}/{}?{}", self.base, self.resource, self.params.join("&"))
    }
}

#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    fn build_url_no_params() {
        let url = URLBuilder::new().with_resource("artists").build();
        assert_eq!(url, String::from("http://0.0.0.0:5000/artists?"))
    }

    #[test]
    fn build_url_one_param() {
        let url = URLBuilder::new()
            .with_resource("songs")
            .with_param("limit", 5)
            .build();
        assert_eq!(url, String::from("http://0.0.0.0:5000/songs?limit=5"))
    }

    #[test]
    fn build_url_two_params() {
        let url = URLBuilder::new()
            .with_resource("genres")
            .with_param("limit", 5)
            .with_param("time_range", "short_term")
            .build();
        assert_eq!(
            url,
            String::from("http://0.0.0.0:5000/genres?limit=5&time_range=short_term")
        )
    }

    #[test]
    fn build_url_param_list() {
        let url = URLBuilder::new()
            .with_resource("recommendations")
            .with_param("seed_artists", "ABC123,XYZ456")
            .build();
        assert_eq!(
            url,
            String::from("http://0.0.0.0:5000/recommendations?seed_artists=ABC123,XYZ456")
        )
    }
}
