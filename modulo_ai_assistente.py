"""
MÓDULO DE ASSISTENTE IA JURÍDICO
ChatBot integrado com análise de documentos e sugestões
"""

import customtkinter as ctk
import tkinter.messagebox as msg
from datetime import datetime
import json
import os
from tkinter import filedialog

from config import *

# Verificar se API está disponível
try:
    import requests
    REQUESTS_DISPONIVEL = True
except ImportError:
    REQUESTS_DISPONIVEL = False

class AssistenteIA(ctk.CTkToplevel):
    """Janela do Assistente IA Jurídico"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("🤖 Assistente IA Jurídico")
        self.geometry("1200x800")
        self.configure(fg_color=COR_FUNDO)
        
        self.historico = []
        self.arquivo_historico = "historico_ia.json"
        self.carregar_historico()
        
        self.criar_interface()
    
    def criar_interface(self):
        """Cria interface do assistente"""
        
        # Header
        frame_header = ctk.CTkFrame(self, fg_color=COR_CARD, height=100, corner_radius=0)
        frame_header.pack(fill="x")
        frame_header.pack_propagate(False)
        
        ctk.CTkLabel(
            frame_header,
            text="🤖 ASSISTENTE IA JURÍDICO",
            font=("Montserrat", 26, "bold"),
            text_color=COR_OURO
        ).pack(side="left", padx=30, pady=30)
        
        ctk.CTkLabel(
            frame_header,
            text="Análise jurídica • Sugestões de teses • Revisão de peças",
            font=("Arial", 12),
            text_color="#888888"
        ).pack(side="left", padx=(0, 30))
        
        # Container principal
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Painel esquerdo - Menu de opções
        frame_menu = ctk.CTkFrame(container, fg_color=COR_CARD, corner_radius=15, width=300)
        frame_menu.pack(side="left", fill="y", padx=(0, 10))
        frame_menu.pack_propagate(False)
        
        self.criar_menu(frame_menu)
        
        # Painel central - Chat
        frame_chat = ctk.CTkFrame(container, fg_color=COR_CARD, corner_radius=15)
        frame_chat.pack(side="left", fill="both", expand=True)
        
        self.criar_area_chat(frame_chat)
    
    def criar_menu(self, parent):
        """Cria menu de opções"""
        
        ctk.CTkLabel(
            parent,
            text="⚙️ FUNCIONALIDADES",
            font=("Arial", 16, "bold"),
            text_color=COR_OURO
        ).pack(pady=20)
        
        opcoes = [
            ("💬 Chat Livre", self.modo_chat_livre),
            ("📄 Analisar Documento", self.modo_analise_doc),
            ("⚖️ Sugerir Teses", self.modo_sugerir_teses),
            ("✍️ Revisar Petição", self.modo_revisar_peticao),
            ("📚 Pesquisa Jurídica", self.modo_pesquisa),
            ("🎯 Modelo de Peça", self.modo_modelo_peca),
            ("📊 Análise de Caso", self.modo_analise_caso),
            ("🗑️ Limpar Histórico", self.limpar_historico)
        ]
        
        for texto, comando in opcoes:
            ctk.CTkButton(
                parent,
                text=texto,
                command=comando,
                fg_color="transparent",
                hover_color=COR_OURO_ESCURO,
                anchor="w",
                height=45,
                font=("Arial", 13)
            ).pack(fill="x", padx=15, pady=5)
        
        # Informações
        frame_info = ctk.CTkFrame(parent, fg_color="#1a4d1a", corner_radius=10)
        frame_info.pack(fill="x", padx=15, pady=20, side="bottom")
        
        info_text = "ℹ️ SOBRE O ASSISTENTE\n\n"
        info_text += "Este assistente utiliza IA para:\n"
        info_text += "• Responder dúvidas jurídicas\n"
        info_text += "• Analisar documentos\n"
        info_text += "• Sugerir argumentos\n"
        info_text += "• Revisar peças processuais\n"
        info_text += "• Pesquisar jurisprudência"
        
        ctk.CTkLabel(
            frame_info,
            text=info_text,
            font=("Arial", 10),
            justify="left",
            text_color="#90EE90"
        ).pack(padx=10, pady=10)
    
    def criar_area_chat(self, parent):
        """Cria área de chat"""
        
        # Área de mensagens
        self.chat_display = ctk.CTkTextbox(
            parent,
            font=("Arial", 12),
            wrap="word",
            fg_color="#0a0a0a"
        )
        self.chat_display.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Mensagem inicial
        self.adicionar_mensagem_sistema(
            "👋 Olá! Sou seu assistente jurídico virtual.\n\n"
            "Como posso ajudá-lo hoje?\n\n"
            "💡 Dica: Selecione uma funcionalidade no menu à esquerda ou digite sua pergunta abaixo."
        )
        
        # Frame de entrada
        frame_input = ctk.CTkFrame(parent, fg_color="transparent")
        frame_input.pack(fill="x", padx=15, pady=(0, 15))
        
        # Campo de entrada
        self.entry_mensagem = ctk.CTkTextbox(
            frame_input,
            height=80,
            font=("Arial", 12),
            wrap="word"
        )
        self.entry_mensagem.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Botões
        frame_btns = ctk.CTkFrame(frame_input, fg_color="transparent", width=120)
        frame_btns.pack(side="left", fill="y")
        frame_btns.pack_propagate(False)
        
        ctk.CTkButton(
            frame_btns,
            text="📎",
            command=self.anexar_arquivo,
            fg_color=COR_CARD,
            hover_color=COR_OURO_ESCURO,
            width=50,
            height=35,
            font=("Arial", 16)
        ).pack(pady=(0, 5))
        
        ctk.CTkButton(
            frame_btns,
            text="Enviar ➤",
            command=self.enviar_mensagem,
            fg_color=COR_OURO_ESCURO,
            hover_color=COR_OURO,
            height=40,
            font=("Arial", 13, "bold")
        ).pack()
        
        # Bind Enter para enviar
        self.entry_mensagem.bind("<Control-Return>", lambda e: self.enviar_mensagem())
    
    def adicionar_mensagem_sistema(self, texto):
        """Adiciona mensagem do sistema"""
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_display.insert("end", f"\n🤖 ASSISTENTE [{timestamp}]\n", "sistema")
        self.chat_display.insert("end", f"{texto}\n", "msg_sistema")
        self.chat_display.insert("end", "\n" + "─"*80 + "\n")
        
        # Configurar tags
        self.chat_display.tag_config("sistema", foreground=COR_OURO, font=("Arial", 11, "bold"))
        self.chat_display.tag_config("msg_sistema", foreground="#FFFFFF")
        
        self.chat_display.see("end")
    
    def adicionar_mensagem_usuario(self, texto):
        """Adiciona mensagem do usuário"""
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_display.insert("end", f"\n👤 VOCÊ [{timestamp}]\n", "usuario")
        self.chat_display.insert("end", f"{texto}\n", "msg_usuario")
        
        self.chat_display.tag_config("usuario", foreground="#4169E1", font=("Arial", 11, "bold"))
        self.chat_display.tag_config("msg_usuario", foreground="#CCCCCC")
        
        self.chat_display.see("end")
    
    def enviar_mensagem(self):
        """Envia mensagem do usuário"""
        mensagem = self.entry_mensagem.get("1.0", "end").strip()
        
        if not mensagem:
            return
        
        # Adicionar mensagem do usuário
        self.adicionar_mensagem_usuario(mensagem)
        
        # Limpar campo
        self.entry_mensagem.delete("1.0", "end")
        
        # Processar resposta
        self.processar_mensagem(mensagem)
        
        # Salvar no histórico
        self.historico.append({
            "tipo": "usuario",
            "mensagem": mensagem,
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })
        self.salvar_historico()
    
    def processar_mensagem(self, mensagem):
        """Processa mensagem e gera resposta"""
        
        # Simular "digitando..."
        self.chat_display.insert("end", "\n🤖 digitando...\n", "digitando")
        self.chat_display.tag_config("digitando", foreground="#888888", font=("Arial", 10, "italic"))
        self.chat_display.see("end")
        self.update()
        
        # Gerar resposta baseada em palavras-chave
        resposta = self.gerar_resposta_local(mensagem)
        
        # Remover "digitando..."
        conteudo = self.chat_display.get("1.0", "end")
        linhas = conteudo.split("\n")
        if "digitando..." in linhas[-2]:
            self.chat_display.delete("end-2l", "end-1l")
        
        # Adicionar resposta
        self.adicionar_mensagem_sistema(resposta)
        
        # Salvar no histórico
        self.historico.append({
            "tipo": "assistente",
            "mensagem": resposta,
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })
        self.salvar_historico()
    
    def gerar_resposta_local(self, mensagem):
        """Gera resposta baseada em palavras-chave"""
        
        msg_lower = mensagem.lower()
        
        # Detectar área do direito
        if any(palavra in msg_lower for palavra in ["trabalhista", "trabalho", "emprego", "fgts", "rescisão"]):
            return self.resposta_trabalhista()
        
        elif any(palavra in msg_lower for palavra in ["família", "divórcio", "guarda", "alimentos", "pensão"]):
            return self.resposta_familia()
        
        elif any(palavra in msg_lower for palavra in ["prazo", "dias úteis", "vencimento", "quando vence"]):
            return self.resposta_prazos()
        
        elif any(palavra in msg_lower for palavra in ["petição", "como fazer", "modelo", "elaborar"]):
            return self.resposta_peticao()
        
        elif any(palavra in msg_lower for palavra in ["jurisprudência", "decisão", "precedente", "súmula"]):
            return self.resposta_jurisprudencia()
        
        elif any(palavra in msg_lower for palavra in ["recurso", "apelação", "agravo"]):
            return self.resposta_recursos()
        
        else:
            return self.resposta_generica()
    
    def resposta_trabalhista(self):
        return """📋 **DIREITO DO TRABALHO**

Principais pontos a considerar em ações trabalhistas:

🔹 **Vínculo Empregatício:**
- Requisitos: pessoalidade, não eventualidade, onerosidade e subordinação
- Prazo prescricional: 5 anos da extinção do contrato

🔹 **Verbas Rescisórias:**
- Saldo de salário
- Aviso prévio (trabalhado ou indenizado)
- 13º salário proporcional
- Férias vencidas e proporcionais + 1/3
- FGTS + 40% (dispensa sem justa causa)

🔹 **Horas Extras:**
- Adicional mínimo de 50%
- Domingos e feriados: 100%
- Reflexos em: DSR, 13º, férias, FGTS

💡 **Dica:** Sempre anexe documentos como CTPS, contracheques, comprovantes de pagamento e testemunhas."""
    
    def resposta_familia(self):
        return """👨‍👩‍👧 **DIREITO DE FAMÍLIA**

Aspectos importantes em ações de família:

🔹 **Guarda de Filhos:**
- Preferência pela guarda compartilhada (Lei 13.058/2014)
- Interesse superior da criança
- Direito de convivência

🔹 **Pensão Alimentícia:**
- Baseada no binômio necessidade-possibilidade
- Percentual comum: 30% dos rendimentos líquidos
- Pode incluir: alimentação, educação, saúde, lazer

🔹 **Divórcio:**
- Não há mais prazo de separação
- Partilha de bens conforme regime de casamento
- União estável segue regras similares

💡 **Dica:** Reúna documentos financeiros de ambas as partes e comprovantes de gastos com os filhos."""
    
    def resposta_prazos(self):
        return """⏰ **GESTÃO DE PRAZOS**

Regras essenciais sobre prazos processuais:

🔹 **Contagem:**
- Exclui-se o dia do início
- Inclui-se o dia do vencimento
- Considera apenas dias úteis
- Prorroga se vencer em feriado/fim de semana

🔹 **Principais Prazos:**
- Contestação: 15 dias
- Apelação: 15 dias
- Agravo de Instrumento: 15 dias
- Embargos de Declaração: 5 dias
- Recurso Ordinário (TST): 8 dias

🔹 **Atenção:**
- Use sempre o módulo de Prazos do sistema
- Configure alertas antecipados
- Considere feriados locais

💡 **Dica:** Use nossa calculadora de prazos no menu 📅 Gestão de Prazos!"""
    
    def resposta_peticao(self):
        return """✍️ **ELABORAÇÃO DE PETIÇÕES**

Estrutura básica de uma petição inicial:

📝 **Elementos Essenciais:**

1. **Endereçamento:** Juízo competente
2. **Qualificação das Partes:** Autor e Réu completos
3. **Dos Fatos:** Narrativa clara e cronológica
4. **Do Direito:** Fundamentação legal
5. **Dos Pedidos:** Claros, específicos e possíveis
6. **Valor da Causa:** Estimativa dos pedidos
7. **Provas:** Rol de testemunhas e documentos
8. **Requerimentos Finais:** Citação, procedência, etc.

💡 **Dica:** Use o gerador automático de petições no sistema! Vá em 📄 Petição e o sistema cria o modelo para você."""
    
    def resposta_jurisprudencia(self):
        return """📚 **PESQUISA DE JURISPRUDÊNCIA**

Principais fontes de pesquisa:

🔍 **Tribunais Superiores:**
- STF: portal.stf.jus.br/jurisprudencia
- STJ: www.stj.jus.br/sites/portalp/Jurisprudencia
- TST: www.tst.jus.br/jurisprudencia

🔍 **Tribunais Estaduais:**
- Consulte o site do TJ do seu estado
- Use palavras-chave específicas
- Filtre por data e órgão julgador

📋 **Súmulas Importantes:**
- Súmulas vinculantes (STF)
- Súmulas da jurisprudência dominante
- Teses de repercussão geral

💡 **Em breve:** Módulo de busca automática integrado ao sistema!"""
    
    def resposta_recursos(self):
        return """⚖️ **RECURSOS PROCESSUAIS**

Principais recursos e prazos:

📌 **Apelação (15 dias):**
- Contra sentença
- Efeito devolutivo e suspensivo (regra)

📌 **Agravo de Instrumento (15 dias):**
- Contra decisões interlocutórias
- Rol taxativo do CPC, art. 1015

📌 **Embargos de Declaração (5 dias):**
- Omissão, contradição, obscuridade
- Interrompe prazo para outros recursos

📌 **Recurso Ordinário (8 dias - TST):**
- Específico da Justiça do Trabalho

💡 **Atenção:** Sempre verifique o tribunal e a matéria para determinar o recurso cabível!"""
    
    def resposta_generica(self):
        return """Entendo sua questão! 

Para melhor ajudá-lo, você pode:

🔹 Ser mais específico sobre a área do direito
🔹 Usar o menu à esquerda para funções específicas
🔹 Perguntar sobre: prazos, petições, jurisprudência, recursos

Exemplos de perguntas:
• "Como calcular prazo de contestação?"
• "Modelo de petição inicial trabalhista"
• "Quais documentos para ação de alimentos?"
• "Prazo para recurso de apelação"

Como posso ajudar especificamente?"""
    
    # ==================== MODOS ESPECIAIS ====================
    
    def modo_chat_livre(self):
        """Modo de chat livre"""
        self.adicionar_mensagem_sistema(
            "💬 Modo Chat Livre ativado!\n\n"
            "Faça qualquer pergunta jurídica e eu tentarei ajudar."
        )
    
    def modo_analise_doc(self):
        """Modo análise de documento"""
        self.adicionar_mensagem_sistema(
            "📄 Modo Análise de Documento\n\n"
            "Clique no botão 📎 para anexar um documento (PDF, DOCX) e eu farei uma análise jurídica."
        )
    
    def modo_sugerir_teses(self):
        """Modo sugestão de teses"""
        self.adicionar_mensagem_sistema(
            "⚖️ Modo Sugestão de Teses\n\n"
            "Descreva o caso e eu sugerirei possíveis teses jurídicas e argumentos."
        )
    
    def modo_revisar_peticao(self):
        """Modo revisão de petição"""
        self.adicionar_mensagem_sistema(
            "✍️ Modo Revisão de Petição\n\n"
            "Cole o texto da petição ou anexe o arquivo e eu farei uma revisão técnica e gramatical."
        )
    
    def modo_pesquisa(self):
        """Modo pesquisa jurídica"""
        self.adicionar_mensagem_sistema(
            "📚 Modo Pesquisa Jurídica\n\n"
            "Digite o tema ou palavras-chave e eu buscarei jurisprudência e legislação relevante."
        )
    
    def modo_modelo_peca(self):
        """Modo modelo de peça"""
        self.adicionar_mensagem_sistema(
            "🎯 Modo Modelo de Peça\n\n"
            "Qual tipo de peça processual você precisa? (Ex: contestação, apelação, embargos...)"
        )
    
    def modo_analise_caso(self):
        """Modo análise de caso"""
        self.adicionar_mensagem_sistema(
            "📊 Modo Análise de Caso\n\n"
            "Descreva o caso completo e eu farei uma análise de viabilidade, riscos e estratégias."
        )
    
    def anexar_arquivo(self):
        """Anexa arquivo para análise"""
        arquivo = filedialog.askopenfilename(
            title="Selecione o documento",
            filetypes=[
                ("Documentos", "*.pdf *.docx *.doc *.txt"),
                ("Todos", "*.*")
            ]
        )
        
        if arquivo:
            nome_arquivo = os.path.basename(arquivo)
            self.adicionar_mensagem_usuario(f"📎 Arquivo anexado: {nome_arquivo}")
            self.adicionar_mensagem_sistema(
                f"Recebi o arquivo '{nome_arquivo}'.\n\n"
                "📋 Análise disponível em breve! Esta funcionalidade requer integração com API de IA."
            )
    
    def limpar_historico(self):
        """Limpa histórico de chat"""
        if msg.askyesno("Confirmar", "Deseja limpar todo o histórico de conversas?"):
            self.chat_display.delete("1.0", "end")
            self.historico = []
            self.salvar_historico()
            self.adicionar_mensagem_sistema(
                "🗑️ Histórico limpo!\n\nComo posso ajudá-lo agora?"
            )
    
    # ==================== PERSISTÊNCIA ====================
    
    def carregar_historico(self):
        """Carrega histórico salvo"""
        if os.path.exists(self.arquivo_historico):
            try:
                with open(self.arquivo_historico, "r", encoding="utf-8") as f:
                    self.historico = json.load(f)
            except:
                self.historico = []
    
    def salvar_historico(self):
        """Salva histórico"""
        try:
            with open(self.arquivo_historico, "w", encoding="utf-8") as f:
                json.dump(self.historico, f, indent=4, ensure_ascii=False)
        except:
            pass

def abrir_assistente_ia(parent):
    """Abre assistente IA"""
    janela = AssistenteIA(parent)
    janela.grab_set()
