use reqwest::{Client};
use serde_json::Value;

pub struct APIController;

impl APIController {
    pub async fn add_calendar(token: &str, url: &str, body: &Value) -> Result<(), reqwest::Error> {
        let client = Client::new();
        
        let _response = client.post(url).bearer_auth(token).json(body).send().await.unwrap();
        Ok(())
    }
}