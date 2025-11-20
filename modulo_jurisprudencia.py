"""
MÓDULO DE BUSCA DE JURISPRUDÊNCIA
Pesquisa em tribunais e organização de decisões
"""

import customtkinter as ctk
import tkinter.messagebox as msg
from datetime import datetime
import json
import os
import webbrowser

from config import *

try:
    import requests
    from bs4 import BeautifulSoup
    SCRAPING_DISPONIVEL = True
except ImportError:
    SCRAPING_DISPONIVEL = False

class BuscaJurisprudencia(ctk.CTkToplevel):
    """Janela de Busca de Jurisprudência"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("🔍 Busca de Jurisprudência")
        self.geometry("1400x850")
        self.configure(fg_color=COR_FUNDO)
        
        self.arquivo_biblioteca = "jurisprudencia.json"
        self.biblioteca = self.carregar_biblioteca()
        
        self.criar_interface()
    
    def criar_interface(self):
        """Cria interface de busca"""
        
        # Header
        frame_header = ctk.CTkFrame(self, fg_color=COR_CARD, height=110, corner_radius=0)
        frame_header.pack(fill="x")
        frame_header.pack_propagate(False)
        
        ctk.CTkLabel(
            frame_header,
            text="🔍 PESQUISA DE JURISPRUDÊNCIA",
            font=("Montserrat", 26, "bold"),
            text_color=COR_OURO
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            frame_header,
            text="Busque decisões em tribunais brasileiros",
            font=("Arial", 12),
            text_color="#888888"
        ).pack(pady=(0, 20))
        
        # Container principal
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Painel de busca (topo)
        self.criar_painel_busca(container)
        
        # Área de resultados (centro)
        frame_resultados = ctk.CTkFrame(container, fg_color=COR_CARD, corner_radius=15)
        frame_resultados.pack(fill="both", expand=True, pady=(10, 0))
        
        # Tabs para resultados e biblioteca
        self.tabs = ctk.CTkTabview(frame_resultados, fg_color=COR_CARD)
        self.tabs.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.tabs.add("🔍 Resultados")
        self.tabs.add("📚 Minha Biblioteca")
        
        # Scroll para resultados
        self.scroll_resultados = ctk.CTkScrollableFrame(
            self.tabs.tab("🔍 Resultados"),
            fg_color="transparent"
        )
        self.scroll_resultados.pack(fill="both", expand=True)
        
        # Scroll para biblioteca
        self.scroll_biblioteca = ctk.CTkScrollableFrame(
            self.tabs.tab("📚 Minha Biblioteca"),
            fg_color="transparent"
        )
        self.scroll_biblioteca.pack(fill="both", expand=True)
        
        # Mensagem inicial
        self.mostrar_mensagem_inicial()
        self.atualizar_biblioteca()
    
    def criar_painel_busca(self, parent):
        """Cria painel de busca"""
        
        frame_busca = ctk.CTkFrame(parent, fg_color=COR_CARD, corner_radius=15, height=200)
        frame_busca.pack(fill="x")
        frame_busca.pack_propagate(False)
        
        # Termo de busca
        ctk.CTkLabel(
            frame_busca,
            text="🔍 Termo de Busca:",
            font=("Arial", 14, "bold"),
            text_color=COR_OURO
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.entry_busca = ctk.CTkEntry(
            frame_busca,
            placeholder_text="Ex: horas extras adicional noturno",
            height=45,
            font=("Arial", 13)
        )
        self.entry_busca.pack(fill="x", padx=20, pady=(0, 15))
        
        # Frame de opções
        frame_opcoes = ctk.CTkFrame(frame_busca, fg_color="transparent")
        frame_opcoes.pack(fill="x", padx=20)
        
        # Tribunal
        frame_tribunal = ctk.CTkFrame(frame_opcoes, fg_color="transparent")
        frame_tribunal.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            frame_tribunal,
            text="Tribunal:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(0, 5))
        
        self.combo_tribunal = ctk.CTkComboBox(
            frame_tribunal,
            values=["Todos", "STF", "STJ", "TST", "TRT", "TJ-SP", "TJ-RJ", "TJ-MG"],
            height=38
        )
        self.combo_tribunal.set("Todos")
        self.combo_tribunal.pack(fill="x")
        
        # Área do direito
        frame_area = ctk.CTkFrame(frame_opcoes, fg_color="transparent")
        frame_area.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            frame_area,
            text="Área do Direito:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(0, 5))
        
        self.combo_area = ctk.CTkComboBox(
            frame_area,
            values=["Todas"] + AREAS_DIREITO,
            height=38
        )
        self.combo_area.set("Todas")
        self.combo_area.pack(fill="x")
        
        # Botão buscar
        frame_btn = ctk.CTkFrame(frame_opcoes, fg_color="transparent", width=150)
        frame_btn.pack(side="left", fill="y")
        frame_btn.pack_propagate(False)
        
        ctk.CTkButton(
            frame_btn,
            text="🔍 BUSCAR",
            command=self.realizar_busca,
            fg_color=COR_OURO_ESCURO,
            hover_color=COR_OURO,
            height=63,
            font=("Arial", 14, "bold")
        ).pack(fill="both", pady=(18, 0))
    
    def mostrar_mensagem_inicial(self):
        """Mostra mensagem inicial"""
        for widget in self.scroll_resultados.winfo_children():
            widget.destroy()
        
        frame_msg = ctk.CTkFrame(self.scroll_resultados, fg_color="transparent")
        frame_msg.pack(expand=True, pady=100)
        
        ctk.CTkLabel(
            frame_msg,
            text="🔍",
            font=("Arial", 80),
            text_color="#888888"
        ).pack()
        
        ctk.CTkLabel(
            frame_msg,
            text="Digite um termo e clique em BUSCAR",
            font=("Arial", 16),
            text_color="#888888"
        ).pack(pady=10)
        
        ctk.CTkLabel(
            frame_msg,
            text="Exemplo: 'horas extras', 'guarda compartilhada', 'danos morais'",
            font=("Arial", 12),
            text_color="#666666"
        ).pack()
    
    def realizar_busca(self):
        """Realiza busca de jurisprudência"""
        termo = self.entry_busca.get().strip()
        tribunal = self.combo_tribunal.get()
        area = self.combo_area.get()
        
        if not termo:
            msg.showerror("Erro", "Digite um termo para buscar!")
            return
        
        # Limpar resultados anteriores
        for widget in self.scroll_resultados.winfo_children():
            widget.destroy()
        
        # Mostrar "buscando..."
        frame_loading = ctk.CTkFrame(self.scroll_resultados, fg_color="transparent")
        frame_loading.pack(expand=True, pady=50)
        
        ctk.CTkLabel(
            frame_loading,
            text="🔄 Buscando...",
            font=("Arial", 18, "bold"),
            text_color=COR_OURO
        ).pack()
        
        self.update()
        
        # Buscar (simulado por enquanto)
        resultados = self.buscar_simulado(termo, tribunal, area)
        
        # Remover loading
        frame_loading.destroy()
        
        # Exibir resultados
        if not resultados:
            ctk.CTkLabel(
                self.scroll_resultados,
                text="😕 Nenhum resultado encontrado",
                font=("Arial", 16),
                text_color="#888888"
            ).pack(pady=50)
            return
        
        # Cabeçalho de resultados
        frame_header_res = ctk.CTkFrame(self.scroll_resultados, fg_color="#1a4d1a", corner_radius=10)
        frame_header_res.pack(fill="x", padx=20, pady=(10, 20))
        
        ctk.CTkLabel(
            frame_header_res,
            text=f"✅ {len(resultados)} resultado(s) encontrado(s) para '{termo}'",
            font=("Arial", 14, "bold"),
            text_color="#90EE90"
        ).pack(padx=15, pady=12)
        
        # Exibir cada resultado
        for resultado in resultados:
            self.criar_card_resultado(resultado)
    
    def buscar_simulado(self, termo, tribunal, area):
        """Busca simulada (exemplo)"""
        
        # Dados de exemplo
        exemplos = [
            {
                "titulo": "HORAS EXTRAS. ADICIONAL NOTURNO. PROCEDÊNCIA.",
                "tribunal": "TST",
                "processo": "RR-12345-20.2023.5.01.0001",
                "data": "15/10/2024",
                "ementa": "RECURSO DE REVISTA. HORAS EXTRAS E ADICIONAL NOTURNO. Comprovada a prestação "
                         "habitual de horas extras e trabalho noturno sem a devida contraprestação. "
                         "Recurso conhecido e provido.",
                "area": "Trabalhista",
                "relevancia": 95
            },
            {
                "titulo": "DANO MORAL. CONFIGURAÇÃO. QUANTUM INDENIZATÓRIO.",
                "tribunal": "STJ",
                "processo": "REsp 1.234.567",
                "data": "20/09/2024",
                "ementa": "RESPONSABILIDADE CIVIL. DANO MORAL. Caracterizado o dano moral pela "
                         "conduta ilícita que afetou a honra e dignidade do autor. Quantum fixado "
                         "em R$ 50.000,00.",
                "area": "Cível",
                "relevancia": 88
            },
            {
                "titulo": "GUARDA COMPARTILHADA. MELHOR INTERESSE DA CRIANÇA.",
                "tribunal": "STJ",
                "processo": "REsp 987.654",
                "data": "10/11/2024",
                "ementa": "DIREITO DE FAMÍLIA. GUARDA COMPARTILHADA. Não havendo impedimento grave, "
                         "deve prevalecer a guarda compartilhada, conforme Lei 13.058/2014, "
                         "atendendo ao melhor interesse da criança.",
                "area": "Família",
                "relevancia": 92
            }
        ]
        
        # Filtrar por área se especificado
        if area != "Todas":
            exemplos = [e for e in exemplos if e["area"] == area]
        
        # Filtrar por tribunal se especificado
        if tribunal != "Todos":
            exemplos = [e for e in exemplos if e["tribunal"] == tribunal]
        
        # Simular busca por termo (case insensitive)
        termo_lower = termo.lower()
        resultados = []
        
        for exemplo in exemplos:
            texto_completo = (exemplo["titulo"] + " " + exemplo["ementa"]).lower()
            if any(palavra in texto_completo for palavra in termo_lower.split()):
                resultados.append(exemplo)
        
        return resultados
    
    def criar_card_resultado(self, resultado):
        """Cria card de resultado"""
        
        frame_card = ctk.CTkFrame(self.scroll_resultados, fg_color="#1a1a1a", corner_radius=12)
        frame_card.pack(fill="x", padx=20, pady=10)
        
        # Header do card
        frame_header = ctk.CTkFrame(frame_card, fg_color="transparent")
        frame_header.pack(fill="x", padx=15, pady=(15, 10))
        
        # Relevância
        cor_relevancia = "#00ff00" if resultado["relevancia"] >= 90 else "#FFD700" if resultado["relevancia"] >= 80 else "#FFA500"
        
        ctk.CTkLabel(
            frame_header,
            text=f"⭐ {resultado['relevancia']}%",
            font=("Arial", 11, "bold"),
            text_color=cor_relevancia
        ).pack(side="left", padx=(0, 10))
        
        # Tribunal e área
        ctk.CTkLabel(
            frame_header,
            text=f"{resultado['tribunal']} | {resultado['area']}",
            font=("Arial", 11, "bold"),
            text_color=COR_OURO
        ).pack(side="left")
        
        # Data
        ctk.CTkLabel(
            frame_header,
            text=resultado['data'],
            font=("Arial", 10),
            text_color="#888888"
        ).pack(side="right")
        
        # Título
        ctk.CTkLabel(
            frame_card,
            text=resultado['titulo'],
            font=("Arial", 14, "bold"),
            text_color="#FFFFFF",
            wraplength=1200,
            justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 10))
        
        # Processo
        ctk.CTkLabel(
            frame_card,
            text=f"📋 Processo: {resultado['processo']}",
            font=("Arial", 11),
            text_color="#CCCCCC"
        ).pack(anchor="w", padx=15)
        
        # Ementa
        frame_ementa = ctk.CTkFrame(frame_card, fg_color="#0a0a0a", corner_radius=8)
        frame_ementa.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            frame_ementa,
            text=resultado['ementa'],
            font=("Arial", 11),
            text_color="#AAAAAA",
            wraplength=1150,
            justify="left"
        ).pack(padx=12, pady=12)
        
        # Botões de ação
        frame_btns = ctk.CTkFrame(frame_card, fg_color="transparent")
        frame_btns.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkButton(
            frame_btns,
            text="⭐ Salvar na Biblioteca",
            command=lambda: self.salvar_na_biblioteca(resultado),
            fg_color=COR_OURO_ESCURO,
            hover_color=COR_OURO,
            width=180,
            height=35
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            frame_btns,
            text="🔗 Abrir no Tribunal",
            command=lambda: self.abrir_no_tribunal(resultado),
            fg_color="#4169E1",
            hover_color="#5a7fda",
            width=180,
            height=35
        ).pack(side="left")
    
    def salvar_na_biblioteca(self, resultado):
        """Salva decisão na biblioteca pessoal"""
        
        # Verificar se já existe
        for item in self.biblioteca:
            if item.get("processo") == resultado["processo"]:
                msg.showinfo("Info", "Esta decisão já está na sua biblioteca!")
                return
        
        # Adicionar tags e observações
        resultado["data_salvo"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        resultado["tags"] = [resultado["area"], resultado["tribunal"]]
        resultado["observacoes"] = ""
        
        self.biblioteca.append(resultado)
        self.salvar_biblioteca()
        
        msg.showinfo("Sucesso", "✅ Decisão salva na sua biblioteca!")
        self.atualizar_biblioteca()
    
    def abrir_no_tribunal(self, resultado):
        """Abre decisão no site do tribunal"""
        
        urls = {
            "STF": "https://portal.stf.jus.br/jurisprudencia/",
            "STJ": "https://www.stj.jus.br/sites/portalp/Jurisprudencia",
            "TST": "https://www.tst.jus.br/jurisprudencia"
        }
        
        tribunal = resultado["tribunal"]
        url = urls.get(tribunal, "https://www.google.com/search?q=" + resultado["processo"])
        
        webbrowser.open(url)
    
    def atualizar_biblioteca(self):
        """Atualiza exibição da biblioteca"""
        
        for widget in self.scroll_biblioteca.winfo_children():
            widget.destroy()
        
        if not self.biblioteca:
            ctk.CTkLabel(
                self.scroll_biblioteca,
                text="📚 Sua biblioteca está vazia\n\nSalve decisões relevantes para consultá-las depois!",
                font=("Arial", 14),
                text_color="#888888"
            ).pack(pady=100)
            return
        
        # Ordenar por data (mais recentes primeiro)
        self.biblioteca.sort(key=lambda x: x.get("data_salvo", ""), reverse=True)
        
        # Exibir cada item
        for item in self.biblioteca:
            frame_item = ctk.CTkFrame(self.scroll_biblioteca, fg_color="#1a1a1a", corner_radius=10)
            frame_item.pack(fill="x", padx=20, pady=10)
            
            # Título
            ctk.CTkLabel(
                frame_item,
                text=item['titulo'],
                font=("Arial", 13, "bold"),
                text_color="#FFFFFF",
                wraplength=1100,
                justify="left"
            ).pack(anchor="w", padx=15, pady=(15, 5))
            
            # Info
            info_text = f"📋 {item['processo']} | {item['tribunal']} | {item['area']}"
            ctk.CTkLabel(
                frame_item,
                text=info_text,
                font=("Arial", 11),
                text_color="#CCCCCC"
            ).pack(anchor="w", padx=15, pady=(0, 10))
            
            # Botão remover
            def remover_item(processo=item['processo']):
                if msg.askyesno("Confirmar", "Remover esta decisão da biblioteca?"):
                    self.biblioteca = [i for i in self.biblioteca if i["processo"] != processo]
                    self.salvar_biblioteca()
                    self.atualizar_biblioteca()
            
            ctk.CTkButton(
                frame_item,
                text="🗑️ Remover",
                command=remover_item,
                fg_color="#8B0000",
                hover_color="#A52A2A",
                width=100,
                height=30
            ).pack(anchor="e", padx=15, pady=(0, 15))
    
    def carregar_biblioteca(self):
        """Carrega biblioteca salva"""
        if os.path.exists(self.arquivo_biblioteca):
            try:
                with open(self.arquivo_biblioteca, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def salvar_biblioteca(self):
        """Salva biblioteca"""
        try:
            with open(self.arquivo_biblioteca, "w", encoding="utf-8") as f:
                json.dump(self.biblioteca, f, indent=4, ensure_ascii=False)
        except Exception as e:
            msg.showerror("Erro", f"Erro ao salvar biblioteca: {str(e)}")

def abrir_busca_jurisprudencia(parent):
    """Abre janela de busca de jurisprudência"""
    if not SCRAPING_DISPONIVEL:
        resposta = msg.askyesno(
            "Bibliotecas Não Instaladas",
            "Para busca automática, instale:\n\n"
            "pip install requests beautifulsoup4\n\n"
            "Deseja abrir mesmo assim? (busca simulada)"
        )
        if not resposta:
            return
    
    janela = BuscaJurisprudencia(parent)
    janela.grab_set()
