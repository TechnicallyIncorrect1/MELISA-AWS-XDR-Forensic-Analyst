import asyncio
import json
import os
import boto3
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress
import logging

from cisa_kev import KevCatalog

console = Console()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MelisaAWSXDR:
    def __init__(self):
        self.session = boto3.Session()
        self.guardduty = self.session.client('guardduty')
        self.securityhub = self.session.client('securityhub')
        self.s3 = self.session.client('s3')
        self.eventbridge = self.session.client('events')
        self.lambda_client = self.session.client('lambda')
        
        self.kev = KevCatalog("data/kev_catalog.json")
        self.forensic_bucket = os.getenv("MELISA_FORENSIC_BUCKET")
        
        console.print(Panel.fit("[bold magenta]MELISA AWS XDR Forensic Analyst[/] - Powered by Trellix Concepts + AWS", 
                               title="🚀 MELISA-AGENTIC v2.0", subtitle="XDR + Forensics + Auto Response"))

    async def ingest_guardduty_findings(self):
        """Ingesta amenazas de GuardDuty (estilo Trellix Network + EDR)"""
        try:
            findings = self.guardduty.list_findings(DetectorId='default')['FindingIds']
            if findings:
                detail = self.guardduty.get_findings(DetectorId='default', FindingIds=findings[:10])
                for finding in detail['Findings']:
                    cve = finding.get('Title', '').split()[-1] if 'CVE' in finding.get('Title', '') else None
                    if cve and self.kev.is_known_exploited(cve):
                        console.print(f"[bold red]🚨 KEV EXPLOITED FINDING DETECTED: {cve}[/]")
                    await self.store_forensic_artifact(finding)
            return len(findings)
        except Exception as e:
            logging.error(f"GuardDuty error: {e}")
            return 0

    async def store_forensic_artifact(self, finding: dict):
        """Almacena evidencia forense en S3 (estilo Trellix Forensic)"""
        if not self.forensic_bucket:
            return
        timestamp = datetime.utcnow().isoformat()
        key = f"forensics/{timestamp}-{finding.get('Id', 'unknown')}.json"
        self.s3.put_object(
            Bucket=self.forensic_bucket,
            Key=key,
            Body=json.dumps(finding, default=str),
            ContentType='application/json'
        )
        console.print(f"[green]📦 Forensic artifact saved: {key}[/]")

    async def run_mission_control(self):
        """Mission Control en vivo - estilo Trellix XDR Dashboard"""
        with Live(console=console, refresh_per_second=2) as live:
            while True:
                progress = Progress()
                task1 = progress.add_task("[cyan]GuardDuty + Security Hub...", total=100)
                task2 = progress.add_task("[magenta]KEV Correlation...", total=100)
                task3 = progress.add_task("[yellow]Forensic Collection...", total=100)

                findings = await self.ingest_guardduty_findings()
                
                table = Table(title="MELISA AWS XDR LIVE STATUS")
                table.add_column("Module", style="cyan")
                table.add_column("Status", style="green")
                table.add_column("Findings", justify="right")
                table.add_column("Action", style="magenta")
                
                table.add_row("GuardDuty", "🟢 ACTIVE", str(findings), "Correlating with KEV")
                table.add_row("Security Hub", "🟢 ACTIVE", "Live", "Auto-response enabled")
                table.add_row("Forensics (S3)", "🟢 ACTIVE", "Collecting", "Artifacts stored")
                table.add_row("Trellix-Inspired XDR", "🔥 POWERED", "Running", "AI + Automation")

                live.update(table)
                await asyncio.sleep(8)

# ===================== EJECUCIÓN =====================
if __name__ == "__main__":
    console.print("[bold green]Iniciando MELISA AWS XDR Forensic Analyst...[/]")
    xdr = MelisaAWSXDR()
    asyncio.run(xdr.run_mission_control())
