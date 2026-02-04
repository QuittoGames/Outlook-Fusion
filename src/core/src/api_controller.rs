use reqwest::{Client};
use serde_json::Value;

pub struct APIController;

impl APIController {
    pub async fn add_calendar(token: &str, url: &str, body: &Value) -> Result<(), reqwest::Error> {
        let debug: bool = false; // Local Debug Controler

        let client = Client::new();
        
        let response = client.post(url).bearer_auth(token).header("Content-Type", "application/json").json(body).send().await.unwrap();
        let status = response.status();
        let text = response.text().await?;

        if debug{
            println!("STATUS: {}", status);
            println!("RESPONSE: {}", text);

            if !status.is_success() {
                println!("Microsoft Graph error: {}", status);
            }
        }
      
        Ok(())
    }
}