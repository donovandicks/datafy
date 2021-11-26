/// A data model for building URLs
pub struct URLBuilder {
    /// The base URL, e.g. `http://host:port`
    base: String,

    /// The resource endpoint to point to, e.g. `/` or `/songs`
    resource: String,

    /// A list of query parameters, which are strings e.g. `key=value`
    params: Vec<String>,
}

impl URLBuilder {
    /// Constructs a new instance of the `URLBuilder`
    ///
    /// # Returns
    ///
    /// * An instance of the `URLBuilder` with initialized members
    pub fn new() -> URLBuilder {
        URLBuilder {
            base: String::from("http://0.0.0.0:5000"),
            resource: String::from(""),
            params: vec![],
        }
    }

    /// Adds a parameter to the existing params list
    ///
    /// # Args
    ///
    /// * `key` - A str reference for the query parameter key
    /// * `value` - A str reference for the query parameter value
    ///
    /// # Returns
    ///
    /// * The current instance of the `URLBuilder`
    pub fn with_param<'a>(&'a mut self, key: &str, value: &str) -> &'a mut URLBuilder {
        if value.is_empty() {
            return self;
        }

        self.params.push(format!("{}={}", key, value));
        self
    }

    pub fn with_params<'a>(&'a mut self, params: Vec<(&str, &str)>) -> &'a mut URLBuilder {
        for (key, val) in params {
            self.with_param(key, val);
        }

        self
    }

    /// Sets a resource on the current `URLBuilder`
    ///
    /// Does **not** overwrite an existing resource
    ///
    /// # Args
    ///
    /// * `resource` - A str reference for the endpoint resource
    ///
    /// # Returns
    ///
    /// * The current instance of the `URLBuilder`
    pub fn with_resource<'a>(&'a mut self, resource: &str) -> &'a mut URLBuilder {
        if self.resource.is_empty() {
            self.resource = String::from(resource);
        }

        self
    }

    /// Construct the URL string with the data on the current `URLBuilder`
    ///
    /// # Returns
    ///
    /// * The formatted URL string
    ///
    /// # Panics
    ///
    /// If there is no resource defined on the `URLBuilder`
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
            .with_param("limit", "5")
            .build();
        assert_eq!(url, String::from("http://0.0.0.0:5000/songs?limit=5"))
    }

    #[test]
    fn build_url_two_params() {
        let url = URLBuilder::new()
            .with_resource("genres")
            .with_param("limit", "5")
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
