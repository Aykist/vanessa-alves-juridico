"""
MÓDULO DE DASHBOARD AVANÇADO
Estatísticas, gráficos e relatórios
"""

import customtkinter as ctk
import tkinter.messagebox as msg
from datetime import datetime, timedelta
import json
import os

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib
    matplotlib.use('TkAgg')
    MATPLOTLIB_DISPONIVEL = True
except ImportError:
    MATPLOTLIB_DISPONIVEL = False

from config import *

class DashboardAvancado(ctk.CTkToplevel):
    """Janela de Dashboard com estatísticas"""
    
    def __init__(self, parent, dados):
        super().__init__(parent)
        
        self.title("📊 Dashboard & Estatísticas")
        self.geometry("1400x800")
        self.configure(fg_color=COR_FUNDO)
        
        self.dados = dados
        self.criar_interface()
        self.calcular_estatisticas()
    
    def criar_interface(self):
        """Cria interface do dashboard"""
        
        # Header
        frame_header = ctk.CTkFrame(self, fg_color=COR_CARD, height=100, corner_radius=0)
        frame_header.pack(fill="x")
        frame_header.pack_propagate(False)
        
        ctk.CTkLabel(
            frame_header,
            text="📊 DASHBOARD EXECUTIVO",
            font=("Montserrat", 28, "bold"),
            text_color=COR_OURO
        ).pack(pady=30)
        
        # Scroll container
        self.scroll_main = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_main.pack(fill="both", expand=True, padx=20, pady=20)
    
    def calcular_estatisticas(self):
        """Calcula e exibe estatísticas"""
        
        # Limpar conteúdo anterior
        for widget in self.scroll_main.winfo_children():
            widget.destroy()
        
        clientes = self.dados.get("clientes", {})
        
        # ========== CARDS DE RESUMO ==========
        frame_cards = ctk.CTkFrame(self.scroll_main, fg_color="transparent")
        frame_cards.pack(fill="x", pady=(0, 20))
        
        # Total de clientes
        total_clientes = len(clientes)
        self.criar_card_metrica(
            frame_cards,
            "👥 CLIENTES",
            str(total_clientes),
            "Total cadastrados",
            COR_OURO
        ).pack(side="left", padx=10, expand=True, fill="both")
        
        # Total de processos
        total_processos = sum(len(c.get("processos", [])) for c in clientes.values())
        self.criar_card_metrica(
            frame_cards,
            "⚖️ PROCESSOS",
            str(total_processos),
            "Total em andamento",
            "#4169E1"
        ).pack(side="left", padx=10, expand=True, fill="both")
        
        # Média de processos por cliente
        media = round(total_processos / total_clientes, 1) if total_clientes > 0 else 0
        self.criar_card_metrica(
            frame_cards,
            "📊 MÉDIA",
            str(media),
            "Processos por cliente",
            "#32CD32"
        ).pack(side="left", padx=10, expand=True, fill="both")
        
        # Processos recentes (últimos 30 dias)
        processos_recentes = self.contar_processos_recentes(clientes, 30)
        self.criar_card_metrica(
            frame_cards,
            "📅 RECENTES",
            str(processos_recentes),
            "Últimos 30 dias",
            "#FF6347"
        ).pack(side="left", padx=10, expand=True, fill="both")
        
        # ========== GRÁFICOS ==========
        if MATPLOTLIB_DISPONIVEL and total_processos > 0:
            self.criar_secao_graficos(clientes)
        
        # ========== ESTATÍSTICAS POR ÁREA ==========
        self.criar_estatisticas_areas(clientes)
        
        # ========== CLIENTES TOP ==========
        self.criar_top_clientes(clientes)
        
        # ========== ATIVIDADE MENSAL ==========
        self.criar_atividade_mensal(clientes)
    
    def criar_card_metrica(self, parent, titulo, valor, subtitulo, cor):
        """Cria card de métrica"""
        card = ctk.CTkFrame(parent, fg_color=COR_CARD, corner_radius=15, height=120)
        card.pack_propagate(False)
        
        ctk.CTkLabel(
            card,
            text=titulo,
            font=("Arial", 13, "bold"),
            text_color="#888888"
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            card,
            text=valor,
            font=("Arial", 36, "bold"),
            text_color=cor
        ).pack()
        
        ctk.CTkLabel(
            card,
            text=subtitulo,
            font=("Arial", 11),
            text_color="#666666"
        ).pack(pady=(5, 15))
        
        return card
    
    def criar_secao_graficos(self, clientes):
        """Cria seção de gráficos"""
        frame_graficos = ctk.CTkFrame(self.scroll_main, fg_color=COR_CARD, corner_radius=15)
        frame_graficos.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            frame_graficos,
            text="📈 GRÁFICOS ESTATÍSTICOS",
            font=("Arial", 18, "bold"),
            text_color=COR_OURO
        ).pack(pady=15)
        
        # Container para gráficos
        frame_plots = ctk.CTkFrame(frame_graficos, fg_color="transparent")
        frame_plots.pack(fill="x", padx=20, pady=(0, 20))
        
        # Gráfico de processos por área
        self.criar_grafico_areas(frame_plots, clientes)
    
    def criar_grafico_areas(self, parent, clientes):
        """Cria gráfico de pizza com processos por área"""
        # Contar processos por área
        areas_count = {}
        for cliente in clientes.values():
            for processo in cliente.get("processos", []):
                area = processo.get("area", "Não especificado")
                areas_count[area] = areas_count.get(area, 0) + 1
        
        if not areas_count:
            return
        
        # Criar gráfico
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='#1a1a1a')
        ax.set_facecolor('#1a1a1a')
        
        cores = ['#d4af37', '#4169E1', '#32CD32', '#FF6347', '#9370DB', '#20B2AA']
        
        wedges, texts, autotexts = ax.pie(
            areas_count.values(),
            labels=areas_count.keys(),
            autopct='%1.1f%%',
            colors=cores[:len(areas_count)],
            startangle=90,
            textprops={'color': 'white', 'fontsize': 10}
        )
        
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')
        
        ax.set_title('Processos por Área do Direito', color='white', fontsize=14, fontweight='bold', pad=20)
        
        # Adicionar ao tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
        
        plt.close(fig)
    
    def criar_estatisticas_areas(self, clientes):
        """Cria tabela de estatísticas por área"""
        frame_areas = ctk.CTkFrame(self.scroll_main, fg_color=COR_CARD, corner_radius=15)
        frame_areas.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            frame_areas,
            text="⚖️ ESTATÍSTICAS POR ÁREA DO DIREITO",
            font=("Arial", 18, "bold"),
            text_color=COR_OURO
        ).pack(pady=15)
        
        # Contar por área
        areas_count = {}
        for cliente in clientes.values():
            for processo in cliente.get("processos", []):
                area = processo.get("area", "Não especificado")
                areas_count[area] = areas_count.get(area, 0) + 1
        
        if not areas_count:
            ctk.CTkLabel(
                frame_areas,
                text="Nenhum processo cadastrado",
                text_color="#888888"
            ).pack(pady=20)
            return
        
        # Ordenar por quantidade
        areas_sorted = sorted(areas_count.items(), key=lambda x: x[1], reverse=True)
        
        # Criar tabela
        for area, count in areas_sorted:
            frame_row = ctk.CTkFrame(frame_areas, fg_color="#1a1a1a", corner_radius=8)
            frame_row.pack(fill="x", padx=20, pady=5)
            
            # Nome da área
            ctk.CTkLabel(
                frame_row,
                text=f"⚖️ {area}",
                font=("Arial", 13, "bold"),
                text_color="#FFFFFF"
            ).pack(side="left", padx=15, pady=10)
            
            # Quantidade
            ctk.CTkLabel(
                frame_row,
                text=f"{count} processo{'s' if count != 1 else ''}",
                font=("Arial", 12),
                text_color=COR_OURO
            ).pack(side="right", padx=15, pady=10)
        
        frame_areas.pack(pady=(0, 20))
    
    def criar_top_clientes(self, clientes):
        """Cria lista de clientes com mais processos"""
        frame_top = ctk.CTkFrame(self.scroll_main, fg_color=COR_CARD, corner_radius=15)
        frame_top.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            frame_top,
            text="🏆 TOP 10 CLIENTES (Mais Processos)",
            font=("Arial", 18, "bold"),
            text_color=COR_OURO
        ).pack(pady=15)
        
        # Criar lista de clientes com quantidade de processos
        clientes_list = []
        for cpf, cliente in clientes.items():
            num_processos = len(cliente.get("processos", []))
            if num_processos > 0:
                clientes_list.append((cliente.get("nome", "Sem nome"), num_processos, cpf))
        
        # Ordenar e pegar top 10
        clientes_list.sort(key=lambda x: x[1], reverse=True)
        top_10 = clientes_list[:10]
        
        if not top_10:
            ctk.CTkLabel(
                frame_top,
                text="Nenhum cliente com processos",
                text_color="#888888"
            ).pack(pady=20)
            return
        
        # Exibir top 10
        for i, (nome, num_proc, cpf) in enumerate(top_10, 1):
            frame_cliente = ctk.CTkFrame(frame_top, fg_color="#1a1a1a", corner_radius=8)
            frame_cliente.pack(fill="x", padx=20, pady=5)
            
            # Posição e medalha
            medalha = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}º"
            
            ctk.CTkLabel(
                frame_cliente,
                text=f"{medalha}  {nome}",
                font=("Arial", 13, "bold"),
                text_color="#FFFFFF"
            ).pack(side="left", padx=15, pady=10)
            
            ctk.CTkLabel(
                frame_cliente,
                text=f"{num_proc} processo{'s' if num_proc != 1 else ''}",
                font=("Arial", 12),
                text_color=COR_OURO
            ).pack(side="right", padx=15, pady=10)
        
        frame_top.pack(pady=(0, 20))
    
    def criar_atividade_mensal(self, clientes):
        """Cria resumo de atividade mensal"""
        frame_atividade = ctk.CTkFrame(self.scroll_main, fg_color=COR_CARD, corner_radius=15)
        frame_atividade.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            frame_atividade,
            text="📅 ATIVIDADE DOS ÚLTIMOS 6 MESES",
            font=("Arial", 18, "bold"),
            text_color=COR_OURO
        ).pack(pady=15)
        
        # Contar processos por mês
        hoje = datetime.now()
        meses_count = {}
        
        for i in range(6):
            mes_ref = hoje - timedelta(days=30*i)
            mes_nome = mes_ref.strftime("%B/%Y")
            meses_count[mes_nome] = 0
        
        for cliente in clientes.values():
            for processo in cliente.get("processos", []):
                data_cadastro = processo.get("data_cadastro", "")
                if data_cadastro:
                    try:
                        data = datetime.strptime(data_cadastro.split()[0], "%d/%m/%Y")
                        mes_proc = data.strftime("%B/%Y")
                        if mes_proc in meses_count:
                            meses_count[mes_proc] += 1
                    except:
                        pass
        
        # Exibir resumo
        for mes, count in meses_count.items():
            frame_mes = ctk.CTkFrame(frame_atividade, fg_color="#1a1a1a", corner_radius=8)
            frame_mes.pack(fill="x", padx=20, pady=5)
            
            ctk.CTkLabel(
                frame_mes,
                text=f"📅 {mes}",
                font=("Arial", 13),
                text_color="#FFFFFF"
            ).pack(side="left", padx=15, pady=10)
            
            ctk.CTkLabel(
                frame_mes,
                text=f"{count} novo{'s' if count != 1 else ''} processo{'s' if count != 1 else ''}",
                font=("Arial", 12),
                text_color=COR_OURO
            ).pack(side="right", padx=15, pady=10)
        
        frame_atividade.pack(pady=(0, 20))
    
    def contar_processos_recentes(self, clientes, dias):
        """Conta processos cadastrados nos últimos X dias"""
        hoje = datetime.now()
        limite = hoje - timedelta(days=dias)
        count = 0
        
        for cliente in clientes.values():
            for processo in cliente.get("processos", []):
                data_cadastro = processo.get("data_cadastro", "")
                if data_cadastro:
                    try:
                        data = datetime.strptime(data_cadastro.split()[0], "%d/%m/%Y")
                        if data >= limite:
                            count += 1
                    except:
                        pass
        
        return count

def abrir_dashboard(parent, dados):
    """Abre dashboard avançado"""
    if not MATPLOTLIB_DISPONIVEL:
        resposta = msg.askyesno(
            "Biblioteca Não Instalada",
            "Para exibir gráficos, instale matplotlib:\n\n"
            "pip install matplotlib\n\n"
            "Deseja abrir o dashboard mesmo assim?"
        )
        if not resposta:
            return
    
    janela = DashboardAvancado(parent, dados)
    janela.grab_set()
