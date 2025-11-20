"""
ARQUIVO DE CONFIGURAÇÃO CENTRAL
Sistema de Gestão Jurídica - Vanessa Alves
"""

import os
from datetime import datetime

# ==================== CORES E TEMAS ====================
COR_OURO = "#d4af37"
COR_OURO_ESCURO = "#b8860b"
COR_FUNDO = "#1a1a1a"
COR_CARD = "#2b2b2b"
COR_SUCESSO = "#228B22"
COR_ERRO = "#8B0000"
COR_AVISO = "#FFA500"

# ==================== ARQUIVOS DO SISTEMA ====================
ARQUIVO_DADOS = "VanessaAlves_Dados.json"
ARQUIVO_BACKUP = "VanessaAlves_Dados_backup.json"
ARQUIVO_PRAZOS = "prazos.json"
ARQUIVO_JURISPRUDENCIA = "jurisprudencia.json"
ARQUIVO_CONFIG_USER = "config_usuario.json"

# ==================== DIRETÓRIOS ====================
DIR_PETICOES = "Peticoes_Geradas"
DIR_DOCUMENTOS = "Documentos_Importados"
DIR_BACKUPS = "Backups"
DIR_RELATORIOS = "Relatorios"

# Criar diretórios se não existirem
for diretorio in [DIR_PETICOES, DIR_DOCUMENTOS, DIR_BACKUPS, DIR_RELATORIOS]:
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

# ==================== INFORMAÇÕES DO ESCRITÓRIO ====================
ESCRITORIO = {
    "nome": "VANESSA ALVES",
    "razao_social": "Vanessa Alves Advocacia",
    "especialidades": ["Trabalhista", "Família"],
    "slogan": "Advocacia Trabalhista & Direito de Família",
    "versao_sistema": "2.0"
}

# ==================== ÁREAS DO DIREITO ====================
AREAS_DIREITO = [
    "Trabalhista",
    "Família",
    "Cível",
    "Previdenciário",
    "Consumidor",
    "Criminal",
    "Tributário",
    "Empresarial"
]

# ==================== TEMPLATES DE PETIÇÃO ====================
TEMPLATES_PETICAO = {
    "Trabalhista": {
        "titulo": "RECLAMAÇÃO TRABALHISTA",
        "pedidos": [
            "Reconhecimento do vínculo empregatício",
            "Pagamento de verbas rescisórias",
            "FGTS e multa de 40%",
            "Horas extras e adicional noturno",
            "Aviso prévio indenizado",
            "Danos morais"
        ]
    },
    "Família": {
        "titulo": "AÇÃO DE FAMÍLIA",
        "pedidos": [
            "Regulamentação de guarda",
            "Fixação de alimentos",
            "Regime de visitas",
            "Partilha de bens",
            "Reconhecimento de união estável"
        ]
    },
    "Cível": {
        "titulo": "AÇÃO CÍVEL",
        "pedidos": [
            "Indenização por danos materiais",
            "Indenização por danos morais",
            "Cumprimento de obrigação",
            "Ressarcimento de valores"
        ]
    },
    "Previdenciário": {
        "titulo": "AÇÃO PREVIDENCIÁRIA",
        "pedidos": [
            "Concessão de benefício",
            "Revisão de benefício",
            "Restabelecimento de auxílio",
            "Aposentadoria por invalidez"
        ]
    },
    "Consumidor": {
        "titulo": "AÇÃO CONSUMERISTA",
        "pedidos": [
            "Restituição de valores pagos",
            "Danos morais",
            "Cumprimento de oferta",
            "Cancelamento de contrato"
        ]
    }
}

# ==================== TIPOS DE PRAZO ====================
TIPOS_PRAZO = [
    "Contestação (15 dias)",
    "Recurso Ordinário (8 dias)",
    "Apelação (15 dias)",
    "Agravo de Instrumento (15 dias)",
    "Embargos de Declaração (5 dias)",
    "Manifestação sobre Documentos (15 dias)",
    "Cumprimento de Sentença (15 dias)",
    "Apresentação de Documentos (Variável)",
    "Resposta à Reconvenção (15 dias)",
    "Impugnação (15 dias)",
    "Réplica (15 dias)",
    "Outro"
]

# ==================== FERIADOS NACIONAIS 2025 ====================
FERIADOS_NACIONAIS = [
    "01/01/2025",  # Ano Novo
    "03/03/2025",  # Carnaval (segunda)
    "04/03/2025",  # Carnaval (terça)
    "18/04/2025",  # Paixão de Cristo
    "21/04/2025",  # Tiradentes
    "01/05/2025",  # Dia do Trabalho
    "19/06/2025",  # Corpus Christi
    "07/09/2025",  # Independência
    "12/10/2025",  # Nossa Senhora Aparecida
    "02/11/2025",  # Finados
    "15/11/2025",  # Proclamação da República
    "20/11/2025",  # Consciência Negra
    "25/12/2025",  # Natal
]

# ==================== SITES DE JURISPRUDÊNCIA ====================
SITES_JURISPRUDENCIA = {
    "STF": "https://portal.stf.jus.br/jurisprudencia/",
    "STJ": "https://www.stj.jus.br/sites/portalp/Jurisprudencia",
    "TST": "https://www.tst.jus.br/jurisprudencia",
    "TRT": "https://www.trt.jus.br/",
    "JusBrasil": "https://www.jusbrasil.com.br/jurisprudencia/"
}

# ==================== CONFIGURAÇÕES DE EMAIL ====================
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "use_tls": True,
    "remetente": "",  # Configurar pelo usuário
    "senha": ""  # Configurar pelo usuário
}

# ==================== MENSAGENS DO SISTEMA ====================
MENSAGENS = {
    "bem_vindo": "Bem-vindo ao Sistema de Gestão Jurídica!",
    "cliente_salvo": "✅ Cliente cadastrado com sucesso!",
    "processo_salvo": "✅ Processo cadastrado com sucesso!",
    "prazo_critico": "⚠️ ATENÇÃO: Você possui prazos críticos vencendo em breve!",
    "backup_realizado": "✅ Backup realizado com sucesso!",
    "erro_generico": "❌ Ocorreu um erro. Tente novamente.",
    "sem_dados": "📭 Nenhum registro encontrado."
}

# ==================== CONFIGURAÇÕES DE BUSCA ====================
BUSCA_CONFIG = {
    "max_resultados": 100,
    "timeout_requisicao": 10,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# ==================== CONFIGURAÇÕES DE RELATÓRIO ====================
RELATORIO_CONFIG = {
    "formato_padrao": "PDF",
    "incluir_logo": True,
    "incluir_rodape": True,
    "fonte": "Arial",
    "tamanho_fonte": 11
}

# ==================== LIMITES DO SISTEMA ====================
LIMITES = {
    "max_clientes": 10000,
    "max_processos_por_cliente": 500,
    "max_tamanho_arquivo": 50,  # MB
    "dias_backup_automatico": 7
}

# ==================== PADRÕES DE REGEX ====================
REGEX_PATTERNS = {
    "cpf": r"\d{3}\.?\d{3}\.?\d{3}-?\d{2}",
    "cnpj": r"\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}",
    "processo": r"\d{7}-?\d{2}\.?\d{4}\.?\d{1}\.?\d{2}\.?\d{4}",
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "telefone": r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}"
}

# ==================== ATALHOS DO TECLADO ====================
ATALHOS = {
    "novo_cliente": "Ctrl+N",
    "novo_processo": "Ctrl+P",
    "buscar": "Ctrl+F",
    "salvar": "Ctrl+S",
    "gerar_peticao": "Ctrl+G",
    "abrir_prazos": "Ctrl+R"
}

# ==================== LOG DO SISTEMA ====================
LOG_CONFIG = {
    "ativar_log": True,
    "nivel": "INFO",  # DEBUG, INFO, WARNING, ERROR
    "arquivo_log": "sistema.log",
    "max_tamanho_mb": 10
}

# ==================== FUNCÕES AUXILIARES ====================
def get_data_atual():
    """Retorna data atual formatada"""
    return datetime.now().strftime("%d/%m/%Y")

def get_hora_atual():
    """Retorna hora atual formatada"""
    return datetime.now().strftime("%H:%M:%S")

def get_timestamp():
    """Retorna timestamp completo"""
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def get_versao():
    """Retorna versão do sistema"""
    return ESCRITORIO["versao_sistema"]

def get_nome_escritorio():
    """Retorna nome do escritório"""
    return ESCRITORIO["nome"]

# ==================== INFORMAÇÕES DE DEPURAÇÃO ====================
if __name__ == "__main__":
    print("=" * 60)
    print(f"🏛️  {ESCRITORIO['razao_social']}")
    print(f"📋 Sistema de Gestão Jurídica v{ESCRITORIO['versao_sistema']}")
    print("=" * 60)
    print(f"\n📁 Arquivos configurados:")
    print(f"   - Dados: {ARQUIVO_DADOS}")
    print(f"   - Prazos: {ARQUIVO_PRAZOS}")
    print(f"   - Backup: {ARQUIVO_BACKUP}")
    print(f"\n📂 Diretórios:")
    print(f"   - Petições: {DIR_PETICOES}")
    print(f"   - Documentos: {DIR_DOCUMENTOS}")
    print(f"   - Backups: {DIR_BACKUPS}")
    print(f"   - Relatórios: {DIR_RELATORIOS}")
    print(f"\n⚖️  Áreas do Direito: {len(AREAS_DIREITO)}")
    print(f"📅 Feriados cadastrados: {len(FERIADOS_NACIONAIS)}")
    print(f"🔍 Sites de jurisprudência: {len(SITES_JURISPRUDENCIA)}")
    print(f"\n✅ Configuração carregada com sucesso!")
    print("=" * 60)
