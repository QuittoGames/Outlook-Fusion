"""
Tool - Utilitários Globais
Funções auxiliares para sistema, módulos e validações
"""
import os
import platform
import re
from dataclasses import dataclass
from data import data
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class tool:
    """Classe de utilitários globais"""
    
    # ═══════════════════════════════════════════════════════════════
    # SISTEMA
    # ═══════════════════════════════════════════════════════════════
    
    @staticmethod
    def clear_screen():
        """Limpa a tela do terminal"""
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')
    
    @staticmethod
    def get_platform() -> str:
        """Retorna o sistema operacional atual"""
        return platform.system()
    
    # ═══════════════════════════════════════════════════════════════
    # MÓDULOS
    # ═══════════════════════════════════════════════════════════════

    @staticmethod
    async def verify_modules():
        """Verifica e instala dependências do requirements.txt"""
        try:
            req_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "requirements", "requirements.txt"))
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_path], check=True)
        except Exception as E:
            print(f"[ERROR] Erro na verificação de módulos: {E}")
            return
        
    @staticmethod
    async def add_path_modules(data_local: data):
        """Adiciona caminhos de módulos locais ao sys.path"""
        if data_local.modules_local is None:
            return
        try:
            for module in data_local.modules_local:
                module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), module))
                sys.path.append(module_path)
                if data_local.Debug:
                    print(f"[DEBUG] Module loaded: {module}")
            return
        except Exception as E:
            print(f"[ERROR] Erro ao adicionar caminhos: {E}")
            return
    
    # ═══════════════════════════════════════════════════════════════
    # FORMATAÇÃO DE DATA/HORA - RFC3339/ISO8601
    # ═══════════════════════════════════════════════════════════════
    
    @staticmethod
    def format_offset(dt: datetime) -> str:
        """Formata o offset de timezone: -0300 → -03:00"""
        offset = dt.strftime("%z")
        return f"{offset[:3]}:{offset[3:]}" if offset else "+00:00"
    
    @staticmethod
    def to_rfc3339(dt: datetime) -> str:
        """
        Converte datetime para RFC3339/ISO8601
        Formato: 2026-02-04T15:30:00-03:00
        """
        if dt.tzinfo is None:
            dt = dt.astimezone()
        offset = tool.format_offset(dt)
        return dt.strftime(f"%Y-%m-%dT%H:%M:%S{offset}")
    
    @staticmethod
    def now_rfc3339() -> str:
        """Retorna data/hora atual em RFC3339"""
        return tool.to_rfc3339(datetime.now().astimezone())
    
    @staticmethod
    def now_plus_hours_rfc3339(hours: int = 2) -> str:
        """Retorna data/hora atual + N horas em RFC3339"""
        dt = datetime.now().astimezone() + timedelta(hours=hours)
        return tool.to_rfc3339(dt)
    
    @staticmethod
    def format_friendly(iso_str: str) -> str:
        """
        Formata ISO8601 para exibição amigável
        Ex: 2026-02-03T14:30:00-03:00 → 14:30 • 03/02
        """
        try:
            dt = datetime.fromisoformat(iso_str)
            return dt.strftime("%H:%M • %d/%m")
        except:
            return iso_str
    
    @staticmethod
    def format_with_friendly(iso_str: str) -> str:
        """
        Retorna ISO com versão amigável
        Ex: 2026-02-03T14:30:00-03:00 (14:30 • 03/02)
        """
        friendly = tool.format_friendly(iso_str)
        return f"{iso_str} ({friendly})"
    
    # ═══════════════════════════════════════════════════════════════
    # REGEX PATTERNS PARA PARSING DE DATA/HORA
    # ═══════════════════════════════════════════════════════════════
    
    # RFC3339 completo: 2026-02-04T15:30:00-03:00
    REGEX_RFC3339 = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$')
    
    # ISO com T mas sem offset: 2026-02-04T15:30:00 ou 2026-02-04T15:30
    REGEX_ISO_NO_OFFSET = re.compile(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?)Z?$')
    
    # Apenas hora: "14" ou "9"
    REGEX_HOUR_ONLY = re.compile(r'^(\d{1,2})$')
    
    # Hora e minuto: "14:00" ou "9:30"
    REGEX_HOUR_MINUTE = re.compile(r'^(\d{1,2}):(\d{2})$')
    
    # Data BR com hora: "05/02 14:00" ou "05/02 14"
    REGEX_DATE_BR_TIME = re.compile(r'^(\d{1,2})/(\d{1,2})\s+(\d{1,2})(?::(\d{2}))?$')
    
    # Data BR completa com hora: "05/02/2026 14:00"
    REGEX_DATE_BR_FULL_TIME = re.compile(r'^(\d{1,2})/(\d{1,2})/(\d{4})\s+(\d{1,2})(?::(\d{2}))?$')
    
    # Data ISO com espaço: "2026-02-05 14:00"
    REGEX_DATE_ISO_SPACE = re.compile(r'^(\d{4})-(\d{2})-(\d{2})\s+(\d{1,2})(?::(\d{2}))?$')
    
    @staticmethod
    def parse_user_datetime(user_input: str, base_date: str = None) -> str:
        """
        Transforma input do usuário em RFC3339/ISO8601
        Usa regex para parsing preciso.
        
        Args:
            user_input: Input do usuário
            base_date: Data base RFC3339 para usar quando só hora é informada
                      (útil para término de eventos)
        
        Aceita:
        - "14" ou "9" -> hora (usa base_date ou hoje)
        - "14:00" ou "9:30" -> hora:minuto (usa base_date ou hoje)
        - "05/02 14:00" ou "05/02 14" -> dia/mês deste ano
        - "05/02/2026 14:00" -> data completa BR
        - "2026-02-05 14:00" -> formato ISO com espaço
        - RFC3339/ISO8601 completo (mantém como está)
        """
        if not user_input:
            return ""
        
        user_input = user_input.strip()
        
        # Determina a data base (para quando só hora é informada)
        if base_date:
            try:
                base_dt = datetime.fromisoformat(base_date)
            except:
                base_dt = datetime.now().astimezone()
        else:
            base_dt = datetime.now().astimezone()
        
        # 1. RFC3339 completo - retorna direto
        if tool.REGEX_RFC3339.match(user_input):
            return user_input
        
        # 2. ISO com T mas sem offset
        match = tool.REGEX_ISO_NO_OFFSET.match(user_input)
        if match:
            try:
                dt = datetime.fromisoformat(user_input.replace('Z', '+00:00'))
                return tool.to_rfc3339(dt.astimezone())
            except:
                pass
        
        # 3. Apenas hora: "14" ou "9"
        match = tool.REGEX_HOUR_ONLY.match(user_input)
        if match:
            hour = int(match.group(1))
            if 0 <= hour <= 23:
                dt = base_dt.replace(hour=hour, minute=0, second=0, microsecond=0)
                return tool.to_rfc3339(dt)
        
        # 4. Hora e minuto: "14:00" ou "9:30"
        match = tool.REGEX_HOUR_MINUTE.match(user_input)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                dt = base_dt.replace(hour=hour, minute=minute, second=0, microsecond=0)
                return tool.to_rfc3339(dt)
        
        # 5. Data BR com hora: "05/02 14:00" ou "05/02 14"
        match = tool.REGEX_DATE_BR_TIME.match(user_input)
        if match:
            day = int(match.group(1))
            month = int(match.group(2))
            hour = int(match.group(3))
            minute = int(match.group(4)) if match.group(4) else 0
            year = base_dt.year
            try:
                dt = datetime(year, month, day, hour, minute, 0).astimezone()
                return tool.to_rfc3339(dt)
            except:
                pass
        
        # 6. Data BR completa: "05/02/2026 14:00"
        match = tool.REGEX_DATE_BR_FULL_TIME.match(user_input)
        if match:
            day = int(match.group(1))
            month = int(match.group(2))
            year = int(match.group(3))
            hour = int(match.group(4))
            minute = int(match.group(5)) if match.group(5) else 0
            try:
                dt = datetime(year, month, day, hour, minute, 0).astimezone()
                return tool.to_rfc3339(dt)
            except:
                pass
        
        # 7. Data ISO com espaço: "2026-02-05 14:00"
        match = tool.REGEX_DATE_ISO_SPACE.match(user_input)
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            hour = int(match.group(4))
            minute = int(match.group(5)) if match.group(5) else 0
            try:
                dt = datetime(year, month, day, hour, minute, 0).astimezone()
                return tool.to_rfc3339(dt)
            except:
                pass
        
        # Se não reconhecer, retorna o input original
        return user_input
    
    # ═══════════════════════════════════════════════════════════════
    # VALIDAÇÕES
    # ═══════════════════════════════════════════════════════════════
    
    @staticmethod
    def is_valid_iso(date_str: str) -> bool:
        """Verifica se a string é um ISO8601/RFC3339 válido"""
        try:
            datetime.fromisoformat(date_str)
            return True
        except:
            return False
    
    @staticmethod
    def clean_friendly_format(value: str) -> str:
        """Remove formato amigável: '2026-02-04T15:00 (15:00 • 04/02)' → '2026-02-04T15:00'"""
        if value and "(" in value:
            return value.split(" (")[0]
        return value
    
    @staticmethod
    def ensure_end_after_start(date_start: str, date_end: str) -> str:
        """
        Garante que a data de término seja após a data de início.
        Se o término for antes ou igual ao início, ajusta para o dia seguinte.
        
        Args:
            date_start: Data de início em RFC3339
            date_end: Data de término em RFC3339
            
        Returns:
            Data de término ajustada se necessário
        """
        try:
            start_dt = datetime.fromisoformat(date_start)
            end_dt = datetime.fromisoformat(date_end)
            
            # Se término <= início, adiciona 1 dia ao término
            if end_dt <= start_dt:
                end_dt = end_dt + timedelta(days=1)
                return tool.to_rfc3339(end_dt)
            
            return date_end
        except:
            return date_end
    
    @staticmethod
    def validate_date_range(date_start: str, date_end: str) -> tuple[bool, str]:
        """
        Valida se o range de datas é válido.
        
        Returns:
            (is_valid, error_message)
        """
        try:
            start_dt = datetime.fromisoformat(date_start)
            end_dt = datetime.fromisoformat(date_end)
            
            if end_dt <= start_dt:
                return False, "Data de término deve ser após a data de início"
            
            return True, ""
        except Exception as e:
            return False, f"Erro ao validar datas: {e}"