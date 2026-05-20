# backup/backup-strategy.md
## Backup Strategy

- Daily full backups (S3 + local)
- Hourly incremental backups
- Retention: 30 days
- Automated with Velero (Kubernetes) + AWS Backup
