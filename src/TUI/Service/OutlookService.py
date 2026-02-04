from dataclasses import dataclass
import subprocess
import os

@dataclass
class OutlookService:
    subject: str = ""
    descr: str = ""
    content: str = ""
    date_start: str = ""
    date_end: str = ""
    timezone: str = "America/Sao_Paulo"
    location: str = "Online"
    
    def run_outlookfusion(self) -> None:
        try:
            # Caminho relativo ao diretório do script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            core_dir = os.path.join(script_dir, "..", "..", "core")
            core_path = os.path.join(core_dir, "target", "debug", "core")
            
            cmd = [
                core_path,
                "create",
                "--subject", self.subject,
                "--content", self.content,
                "--date-start", self.date_start,
                "--date-end", self.date_end,
                "--timezone", self.timezone,
                "--location", self.location
            ]
            
            if self.descr:
                cmd.extend(["--descr", self.descr])
            
            # Executa no diretório do core para que o .env seja encontrado
            a = subprocess.run(cmd, check=True, cwd=core_dir,capture_output=True)
            print(a)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Erro ao executar OutlookFusionCLI: {e}")