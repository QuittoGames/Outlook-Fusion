"""
UIService - Serviço de Interface do Usuário
Responsável por componentes visuais e inputs estilizados
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.align import Align
from rich.table import Table
from data import data, ThemeConfig, AppConfig, DefaultValues
from tool import tool


@dataclass
class UIService:
    """Serviço de UI com componentes visuais"""
    
    config: data = None
    console: Console = None
    
    # Atalhos para configs
    theme: ThemeConfig = None
    app: AppConfig = None
    defaults: DefaultValues = None
    
    def __post_init__(self):
        if self.config is None:
            self.config = data()
        if self.console is None:
            self.console = Console()
        
        # Atalhos para facilitar acesso
        self.theme = self.config.theme
        self.app = self.config.app
        self.defaults = self.config.defaults
    
    # ═══════════════════════════════════════════════════════════════
    # FORMATAÇÃO DE DATA - Delegates para tool
    # ═══════════════════════════════════════════════════════════════
    
    @staticmethod
    def get_current_datetime_iso() -> str:
        """Retorna data/hora atual em RFC3339"""
        return tool.now_rfc3339()
    
    @staticmethod
    def get_datetime_plus_hours_iso(hours: int = 2) -> str:
        """Retorna data/hora + N horas em RFC3339"""
        return tool.now_plus_hours_rfc3339(hours)
    
    @staticmethod
    def format_to_rfc3339(dt: datetime) -> str:
        """Formata datetime para RFC3339"""
        return tool.to_rfc3339(dt)
    
    @staticmethod
    def format_iso_friendly(iso_str: str) -> str:
        """Formata ISO para exibição amigável"""
        return tool.format_friendly(iso_str)
    
    @staticmethod
    def format_iso_with_friendly(iso_str: str) -> str:
        """Retorna ISO com versão amigável"""
        return tool.format_with_friendly(iso_str)
    
    @staticmethod
    def transform_to_iso(user_input: str, base_date: str = None) -> str:
        """Transforma input do usuário em RFC3339"""
        return tool.parse_user_datetime(user_input, base_date)
    
    # ═══════════════════════════════════════════════════════════════
    # COMPONENTES VISUAIS - BANNER, INPUTS, PAINÉIS
    # ═══════════════════════════════════════════════════════════════
    
    def show_banner(self):
        """Banner de apresentação do app usando configs"""
        self.console.clear()
        self.console.print()
        
        banner = Text()
        banner.append("╔═══════════════════════════════════════╗\n", style=f"bold {self.theme.PRIMARY}")
        banner.append("║                                       ║\n", style=f"bold {self.theme.PRIMARY}")
        banner.append("║      ", style=f"bold {self.theme.PRIMARY}")
        banner.append(f"  {self.app.APP_NAME}", style="bold white")
        banner.append("               ║\n", style=f"bold {self.theme.PRIMARY}")
        banner.append("║   ", style=f"bold {self.theme.PRIMARY}")
        banner.append(self.app.APP_DESCRIPTION, style=f"italic {self.theme.ACCENT}")
        banner.append("    ║\n", style=f"bold {self.theme.PRIMARY}")
        banner.append("║                                       ║\n", style=f"bold {self.theme.PRIMARY}")
        banner.append("║       ", style=f"bold {self.theme.PRIMARY}")
        banner.append(f"v{self.app.VERSION}", style=self.theme.TEXT_DIM)
        banner.append(" • ", style=self.theme.TEXT_DIM)
        banner.append(self.app.TECH_STACK, style=self.theme.TEXT_DIM)
        banner.append("        ║\n", style=f"bold {self.theme.PRIMARY}")
        banner.append("║                                       ║\n", style=f"bold {self.theme.PRIMARY}")
        banner.append("╚═══════════════════════════════════════╝", style=f"bold {self.theme.PRIMARY}")
        
        self.console.print(Align.center(banner))
        self.console.print("\n")
    
    def show_separator(self, width: int = 45):
        """Exibe separador horizontal"""
        separator = Text("─" * width, style=self.theme.TEXT_DIM)
        self.console.print(Align.center(separator))
        self.console.print()
    
    def show_hint(self, text: str, icon: str = "💡"):
        """Exibe dica/hint para o usuário"""
        self.console.print(Align.center(Text(f"{icon} {text}", style=self.theme.TEXT_DIM)))
        self.console.print()
    
    def input_field(self, label: str, icon: str = "▸", default: str = None, 
                    optional: bool = False, transform: bool = False, base_date: str = None) -> str:
        """Campo de input estilizado e centralizado
        
        Args:
            label: Texto do campo
            icon: Ícone do campo
            default: Valor padrão
            optional: Se é opcional
            transform: Se deve transformar para RFC3339
            base_date: Data base para transformação (quando só hora é informada)
        """
        
        label_text = Text()
        label_text.append(f"{icon} ", style=f"bold {self.theme.ACCENT}")
        label_text.append(label, style="bold white")
        
        if optional:
            label_text.append(" ", style="white")
            label_text.append("(opcional)", style=self.theme.TEXT_DIM)
        
        if default:
            label_text.append(f" ", style="white")
            label_text.append(f"[{default}]", style=self.theme.TEXT_DIM)
        
        self.console.print(Align.center(label_text))
        self.console.print()
        
        prompt = Text("                         ▸ ", style=self.theme.ACCENT)
        self.console.print(prompt, end="")
        value = input().strip()
        self.console.print()
        
        if transform and value:
            value = self.transform_to_iso(value, base_date)
        
        return value if value else default if default else ""
    
    def show_success_panel(self, message: str, icon: str = ""):
        """Painel de sucesso"""
        panel = Panel(
            Align.center(Text.assemble(
                (f"{icon} ", f"bold {self.theme.SUCCESS}"),
                (message, f"bold {self.theme.SUCCESS}")
            )),
            border_style=self.theme.SUCCESS,
            box=box.HEAVY,
            width=50
        )
        self.console.print(Align.center(panel))
        self.console.print()
    
    def show_warning_panel(self, message: str, icon: str = ""):
        """Painel de aviso/cancelamento"""
        panel = Panel(
            Align.center(Text.assemble(
                (f"{icon} ", f"bold {self.theme.WARNING}"),
                (message, f"bold {self.theme.WARNING}")
            )),
            border_style=self.theme.WARNING,
            box=box.ROUNDED,
            width=50
        )
        self.console.print(Align.center(panel))
    
    def show_error_panel(self, message: str, icon: str = ""):
        """Painel de erro"""
        panel = Panel(
            Align.center(Text.assemble(
                (f"{icon} ", f"bold {self.theme.ERROR}"),
                (message, f"bold {self.theme.ERROR}")
            )),
            border_style=self.theme.ERROR,
            box=box.HEAVY,
            width=50
        )
        self.console.print(Align.center(panel))
        self.console.print()
    
    def show_info(self, lines: list[str]):
        """Exibe informações adicionais"""
        info = Text()
        for line in lines:
            info.append(f"  {line}\n", style=self.theme.TEXT_DIM)
        self.console.print(Align.center(info))
    
    def confirm_prompt(self, message: str = "Confirmar?", icon: str = "") -> bool:
        """Prompt de confirmação Y/n"""
        confirm_text = Text()
        confirm_text.append(f"{icon} ", style=f"bold {self.theme.ACCENT}")
        confirm_text.append(f" {message} ", style="bold white")
        confirm_text.append("[Y/n]", style=self.theme.TEXT_DIM)
        
        self.console.print(Align.center(confirm_text))
        self.console.print()
        
        response = input().strip().lower()
        self.console.print()
        
        return response in ['y', 'yes', '']
    
    def wait_for_exit(self):
        """Aguarda Enter para sair"""
        self.console.print("\n")
        self.console.print(Align.center(f"[{self.theme.TEXT_DIM}]Pressione Enter para sair...[/]"))
        input()
    
    def create_summary_table(self, title: str, fields: dict) -> Table:
        """Cria tabela de resumo estilizada"""
        table = Table(
            show_header=True,
            header_style=f"bold {self.theme.PRIMARY}",
            border_style=self.theme.ACCENT,
            box=box.ROUNDED,
            title=f"[bold white]{title}[/]",
            title_style=f"bold {self.theme.PRIMARY}",
            padding=(0, 2)
        )
        
        table.add_column("Campo", style=f"{self.theme.ACCENT}", width=15)
        table.add_column("Valor", style="white", width=40)
        
        for campo, valor in fields.items():
            if valor:
                table.add_row(f"  {campo}", valor)
        
        return table
    
    def show_table(self, table: Table):
        """Exibe tabela centralizada"""
        self.console.print(Align.center(table))
        self.console.print("\n")
