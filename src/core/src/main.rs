mod api_controller;
mod services;
mod cli;
mod enums;

use dotenvy::dotenv;
use clap::Parser;
use cli::cli::Cli;
use enums::subcommands::Commands;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();
    
    match cli.command {
        Commands::Create(calendar) => {
            dotenv().ok();
            let token = std::env::var("OUTLOOK_TOKEN").expect("[ERROR] OUTLOOK_TOKEN environment variable not found");
            calendar.add_event(&token).await.unwrap();
        }
    }
    Ok(())
}
