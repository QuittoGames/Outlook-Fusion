"""
Data - Model/Configurações Globais
Contém constantes, configurações e dados da aplicação
Modify with IA
"""
from dataclasses import dataclass


@dataclass
class AppConfig:
    """Configurações da aplicação"""
    APP_NAME: str = "OUTLOOK FUSION"
    APP_DESCRIPTION: str = "Gerenciador de Calendário Outlook"
    VERSION: str = "0.1.0"
    TECH_STACK: str = "Rust + Python"


@dataclass 
class ThemeConfig:
    """Configurações de tema/cores"""
    PRIMARY: str = "#0078D4"      # Azul Outlook
    ACCENT: str = "#50E6FF"       # Azul claro
    SUCCESS: str = "green"
    WARNING: str = "yellow"
    ERROR: str = "red"
    TEXT_DIM: str = "bright_black"


@dataclass
class DefaultValues:
    """Valores padrão para eventos"""
    TIMEZONE: str = "America/Sao_Paulo"
    LOCATION: str = "Online"
    CONTENT: str = "No content"
    EVENT_DURATION_HOURS: int = 2


@dataclass
class data:
    """Configuração principal da aplicação"""
    modules_local: list = None
    Debug: bool = False
    
    # Instâncias de configuração
    app: AppConfig = None
    theme: ThemeConfig = None
    defaults: DefaultValues = None
    
    def __post_init__(self):
        if self.modules_local is None:
            self.modules_local = ["Service"]
        if self.app is None:
            self.app = AppConfig()
        if self.theme is None:
            self.theme = ThemeConfig()
        if self.defaults is None:
            self.defaults = DefaultValues()
