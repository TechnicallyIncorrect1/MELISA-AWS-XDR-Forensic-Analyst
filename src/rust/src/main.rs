use aws_sdk_s3::Client as S3Client;
use aws_sdk_guardduty::Client as GuardDutyClient;
use serde_json::Value;
use std::error::Error;
use chrono::Utc;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let config = aws_config::load_from_env().await;
    let s3 = S3Client::new(&config);
    let guardduty = GuardDutyClient::new(&config);

    println!("🔥 MELISA Rust Forensic Collector (Trellix + AWS) - Memory Safe");

    let findings = guardduty.list_findings()
        .detector_id("default")
        .send()
        .await?;

    for id in findings.finding_ids.unwrap_or_default() {
        let detail = guardduty.get_findings()
            .detector_id("default")
            .finding_ids(id)
            .send()
            .await?;

        if let Some(finding) = detail.findings {
            let timestamp = Utc::now().timestamp();
            let key = format!("forensics/{}-{}.json", timestamp, id);

            let body = serde_json::to_vec(&finding)?;

            s3.put_object()
                .bucket("melisa-forensic-bucket")
                .key(&key)
                .body(body.into())
                .send()
                .await?;

            println!("✅ Forensic artifact saved → {}", key);
        }
    }

    Ok(())
}
