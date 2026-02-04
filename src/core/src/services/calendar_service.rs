use clap::Parser;
use serde_json::json;
use chrono::{DateTime, FixedOffset};
use crate::api_controller::APIController;

#[derive(Parser, Debug)]
#[command(name = "Outlook Fusion", version = "0.1", about = "Cria eventos no Outlook Calendar via CLI")]
pub struct CalendarService {
    /// Assunto do evento
    #[arg(short, long)]
    subject: String,

    #[arg(short,long)]
    descr: Option<String>,

    /// Conteúdo do evento
    #[arg(short, long)]
    content: String,

    /// Data de início ISO8601 (ex: 2026-02-01T14:00:00)
    #[arg(long)]
    date_start: String,

    /// Data de término ISO8601 (ex: 2026-02-01T15:00:00)
    #[arg(long)]
    date_end: String,

    /// Timezone (ex: America/Sao_Paulo)
    #[arg(short, long, default_value = "America/Sao_Paulo")]
    timezone: String,

    /// Local do evento
    #[arg(short, long, default_value = "Online")]
    location: String,
}

impl CalendarService {
    pub async fn add_event(&self, token: &str) -> Result<(), Box<dyn std::error::Error>> {
        print!("trafor data");
        let start: DateTime<FixedOffset> = DateTime::parse_from_rfc3339(&self.date_start)
            .expect("Data de início inválida");
        let end: DateTime<FixedOffset> = DateTime::parse_from_rfc3339(&self.date_end)
            .expect("Data de término inválida");

        if start > end {
            return Err("Start date cannot be after end date".into());
        }
        
        let mut description = String::new();

        if let Some(some_desc) = &self.descr {
            description = some_desc.clone();
        }

        print!("build json");
        let body = json!({
            "subject": self.subject,
            "body": { "contentType": "HTML", "content": description },
            "start": {
                "dateTime": start.to_rfc3339(),
                "timeZone": self.timezone
            },
            "end": {
                "dateTime": end.to_rfc3339(),
                "timeZone": self.timezone
            },
            "location": {
                "displayName": self.location
            }
        });

        APIController::add_calendar(token, "https://graph.microsoft.com/v1.0/me/events", &body).await?;
        print!("send");

        Ok(())
    }
}