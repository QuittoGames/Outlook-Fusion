"""
Index - Ponto de Entrada da Aplicação TUI
Orquestra os serviços e fluxo principal
"""
import asyncio
from datetime import datetime, timedelta

from data import data
from tool import tool
from Service.OutlookService import OutlookService
from Service.UIService import UIService


# ═══════════════════════════════════════════════════════════════
# INICIALIZAÇÃO
# ═══════════════════════════════════════════════════════════════

data_local = data()
ui = UIService(config=data_local)


# ═══════════════════════════════════════════════════════════════
# FLUXO PRINCIPAL DA TUI
# ═══════════════════════════════════════════════════════════════

def Start():
    """TUI principal - terminal friendly com Nerd Fonts"""
    
    # Banner e separador
    ui.show_banner()
    ui.show_separator()
    
    # Coleta de dados básicos
    subject = ui.input_field("Assunto do Evento", "")
    descr = ui.input_field("Descrição", "", optional=True)
    content = ui.input_field("Conteúdo", "", default=data_local.defaults.CONTENT)
    
    # Input de horário com dica
    ui.show_hint("Formatos aceitos: 14:00, 14, 05/02 14:00, ISO8601", "⏱️")
    
    # Data de início
    default_start = tool.now_rfc3339()
    default_start_display = tool.format_with_friendly(default_start)
    date_start = ui.input_field("Data de Início", "", default=default_start_display, transform=True)
    date_start = tool.clean_friendly_format(date_start)
    
    # Calcula automaticamente 2h depois da data de início
    default_end = tool.now_plus_hours_rfc3339(data_local.defaults.EVENT_DURATION_HOURS)
    if date_start:
        try:
            start_dt = datetime.fromisoformat(date_start)
            default_end = tool.to_rfc3339(start_dt + timedelta(hours=data_local.defaults.EVENT_DURATION_HOURS))
        except:
            pass
    
    # Mostra que o término é calculado automaticamente
    ui.show_hint(f"Término = Início + {data_local.defaults.EVENT_DURATION_HOURS}h → {tool.format_friendly(default_end)}", "⏱️")
    
    # Data de término (usa date_start como base para quando só hora é informada)
    default_end_display = tool.format_with_friendly(default_end)
    date_end = ui.input_field("Data de Término", "", default=default_end_display, transform=True, base_date=date_start)
    date_end = tool.clean_friendly_format(date_end)
    
    # Garante que término seja após início (ajusta para dia seguinte se necessário)
    date_end = tool.ensure_end_after_start(date_start, date_end)
    
    # Timezone e localização
    tz = ui.input_field("Timezone", "", default=data_local.defaults.TIMEZONE)
    location = ui.input_field("Localização", "", default=data_local.defaults.LOCATION)
    
    # Resumo em tabela estilizada
    summary_fields = {
        "Assunto": subject,
        "Descrição": descr if descr else None,
        "Conteúdo": content,
        "Início": tool.format_friendly(date_start),
        "Término": tool.format_friendly(date_end),
        "Timezone": tz,
        "Local": location
    }
    
    summary_table = ui.create_summary_table(" Resumo do Evento", summary_fields)
    ui.show_table(summary_table)
    
    # Confirmação
    if ui.confirm_prompt("Confirmar criação do evento?", ""):
        # Criando evento
        with ui.console.status(f"[{ui.theme.ACCENT}] Criando evento...[/]", spinner="dots"):
            service = OutlookService(
                subject=subject,
                descr=descr,
                content=content,
                date_start=date_start,
                date_end=date_end,
                timezone=tz,
                location=location
            )
            service.run_outlookfusion()
        
        # Sucesso
        ui.show_success_panel("Evento criado com sucesso!", "")
        ui.show_info([
            "O evento foi adicionado ao seu calendário",
            "Você receberá notificações conforme configurado"
        ])
    else:
        # Cancelado
        ui.show_warning_panel("Operação cancelada", "")
    
    # Aguarda sair
    ui.wait_for_exit()


# ═══════════════════════════════════════════════════════════════
# INICIALIZAÇÃO ASSÍNCRONA
# ═══════════════════════════════════════════════════════════════

async def main():
    try:
        await tool.add_path_modules(data_local)
        if data_local.Debug:
            tool.verify_modules()
    except StopAsyncIteration as E:
        print(f"[ERROR] Erro StopAsycnInteration, Erro: {E}")

if __name__ == "__main__":
    asyncio.run(main())
    Start()