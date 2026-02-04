use clap::Subcommand;
use crate::services::calendar_service::CalendarService;

#[derive(Subcommand)]
pub enum Commands {
    Create(CalendarService),
}
