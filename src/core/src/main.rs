mod api_controller;
mod services;
use dotenvy::dotenv;
use clap::Parser;
use services::calendar_service::CalendarService;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    dotenv().ok();
    let args = CalendarService::parse(); 
    let token = std::env::var("OUTLOOK_TOKEN").expect("[ERROR] OUTLOOK_TOKEN environment variable not found");

    args.add_event(&token).await?;
    Ok(())
}
