use clap::Parser;
use crate::enums::subcommands::Commands;

#[derive(Parser)]
#[command(name = "OutlookFusion", version = "0.2v")]
pub struct Cli {
    #[command(subcommand)]
    pub command: Commands,
}
