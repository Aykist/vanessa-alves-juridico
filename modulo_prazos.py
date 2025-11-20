"""
MÓDULO DE GESTÃO DE PRAZOS
Sistema de controle de prazos processuais com alertas
"""

import customtkinter as ctk
import tkinter.messagebox as msg
from datetime import datetime, timedelta
import json
import os
from tkinter import ttk

# Configurações
COR_OURO = "#d4af37"
COR_OURO_ESCURO = "#b8860b"
COR_FUNDO = "#1a1a1a"
COR_CARD = "#2b2b2b"
ARQUIVO_PRAZOS = "prazos.json"

# Feriados nacionais 2025
FERIADOS_2025 = [
    "01/01/2025",  # Ano Novo
    "03/03/2025",  # Carnaval
    "04/03/2025",  # Carnaval
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

def carregar_prazos():
    """Carrega prazos salvos"""
    if os.path.exists(ARQUIVO_PRAZOS):
        try:
            with open(ARQUIVO_PRAZOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"prazos": []}
    return {"prazos": []}

def salvar_prazos(dados):
    """Salva prazos no arquivo"""
    try:
        with open(ARQUIVO_PRAZOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        msg.showerror("Erro", f"Erro ao salvar prazos: {str(e)}")
        return False

def eh_dia_util(data):
    """Verifica se a data é dia útil"""
    # Se for sábado (5) ou domingo (6)
    if data.weekday() >= 5:
        return False
    
    # Se for feriado
    data_str = data.strftime("%d/%m/%Y")
    if data_str in FERIADOS_2025:
        return False
    
    return True

def proximo_dia_util(data):
    """Retorna o próximo dia útil"""
    while not eh_dia_util(data):
        data += timedelta(days=1)
    return data

def calcular_prazo(data_inicial, dias_uteis):
    """Calcula prazo considerando apenas dias úteis"""
    data_atual = data_inicial
    dias_contados = 0
    
    while dias_contados < dias_uteis:
        data_atual += timedelta(days=1)
        if eh_dia_util(data_atual):
            dias_contados += 1
    
    return data_atual

def dias_restantes(data_vencimento):
    """Calcula dias restantes até o vencimento"""
    hoje = datetime.now().date()
    venc = datetime.strptime(data_vencimento, "%d/%m/%Y").date()
    
    dias = 0
    data_atual = hoje
    
    while data_atual < venc:
        if eh_dia_util(data_atual):
            dias += 1
        data_atual += timedelta(days=1)
    
    return dias

def cor_por_urgencia(dias):
    """Retorna cor baseada na urgência"""
    if dias < 0:
        return "#FF0000"  # Vermelho - Vencido
    elif dias <= 3:
        return "#FF6B6B"  # Vermelho claro - Crítico
    elif dias <= 7:
        return "#FFA500"  # Laranja - Urgente
    elif dias <= 15:
        return "#FFD700"  # Amarelo - Atenção
    else:
        return "#90EE90"  # Verde - Tranquilo

class JanelaPrazos(ctk.CTkToplevel):
    """Janela de Gestão de Prazos"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("📅 Gestão de Prazos Processuais")
        self.geometry("1200x700")
        self.configure(fg_color=COR_FUNDO)
        
        self.dados_prazos = carregar_prazos()
        
        self.criar_interface()
        self.atualizar_lista()
    
    def criar_interface(self):
        """Cria a interface da janela"""
        
        # Header
        frame_header = ctk.CTkFrame(self, fg_color=COR_CARD, corner_radius=0, height=80)
        frame_header.pack(fill="x", pady=(0, 20))
        frame_header.pack_propagate(False)
        
        ctk.CTkLabel(
            frame_header,
            text="📅 GESTÃO DE PRAZOS PROCESSUAIS",
            font=("Montserrat", 24, "bold"),
            text_color=COR_OURO
        ).pack(pady=20)
        
        # Container principal
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Painel esquerdo - Formulário
        frame_form = ctk.CTkFrame(container, fg_color=COR_CARD, corner_radius=15, width=400)
        frame_form.pack(side="left", fill="both", padx=(0, 10), pady=0)
        frame_form.pack_propagate(False)
        
        ctk.CTkLabel(
            frame_form,
            text="➕ ADICIONAR PRAZO",
            font=("Arial", 16, "bold"),
            text_color=COR_OURO
        ).pack(pady=15)
        
        # Campos do formulário
        self.criar_formulario(frame_form)
        
        # Painel direito - Lista de prazos
        frame_lista = ctk.CTkFrame(container, fg_color=COR_CARD, corner_radius=15)
        frame_lista.pack(side="left", fill="both", expand=True, pady=0)
        
        ctk.CTkLabel(
            frame_lista,
            text="📋 PRAZOS ATIVOS",
            font=("Arial", 16, "bold"),
            text_color=COR_OURO
        ).pack(pady=15)
        
        # Scroll para lista
        self.scroll_prazos = ctk.CTkScrollableFrame(
            frame_lista,
            fg_color="transparent"
        )
        self.scroll_prazos.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    
    def criar_formulario(self, parent):
        """Cria formulário de cadastro"""
        
        form = ctk.CTkFrame(parent, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=20)
        
        # Processo
        ctk.CTkLabel(form, text="Número do Processo:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 5))
        self.entry_processo = ctk.CTkEntry(form, height=35)
        self.entry_processo.pack(fill="x", pady=(0, 10))
        
        # Tipo de prazo
        ctk.CTkLabel(form, text="Tipo de Prazo:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 5))
        self.combo_tipo = ctk.CTkComboBox(
            form,
            values=[
                "Contestação",
                "Recurso",
                "Apelação",
                "Manifestação",
                "Cumprimento de Sentença",
                "Apresentação de Documentos",
                "Resposta",
                "Impugnação",
                "Outro"
            ],
            height=35
        )
        self.combo_tipo.set("Contestação")
        self.combo_tipo.pack(fill="x", pady=(0, 10))
        
        # Frame para cálculo
        frame_calculo = ctk.CTkFrame(form, fg_color="#1a4d1a", corner_radius=10)
        frame_calculo.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            frame_calculo,
            text="⚖️ Calculadora de Prazo",
            font=("Arial", 12, "bold")
        ).pack(pady=(10, 5))
        
        # Data inicial
        ctk.CTkLabel(frame_calculo, text="Data da Intimação:", font=("Arial", 11)).pack(anchor="w", padx=15, pady=(5, 2))
        self.entry_data_inicial = ctk.CTkEntry(frame_calculo, placeholder_text="DD/MM/AAAA", height=32)
        self.entry_data_inicial.pack(fill="x", padx=15, pady=(0, 5))
        
        # Dias úteis
        ctk.CTkLabel(frame_calculo, text="Quantidade de Dias Úteis:", font=("Arial", 11)).pack(anchor="w", padx=15, pady=(5, 2))
        self.entry_dias = ctk.CTkEntry(frame_calculo, placeholder_text="Ex: 15", height=32)
        self.entry_dias.pack(fill="x", padx=15, pady=(0, 10))
        
        # Botão calcular
        ctk.CTkButton(
            frame_calculo,
            text="🧮 CALCULAR VENCIMENTO",
            command=self.calcular_vencimento,
            fg_color=COR_OURO_ESCURO,
            hover_color=COR_OURO,
            height=35
        ).pack(fill="x", padx=15, pady=(0, 10))
        
        # Data de vencimento calculada
        ctk.CTkLabel(form, text="Data de Vencimento:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 5))
        self.entry_vencimento = ctk.CTkEntry(form, height=35)
        self.entry_vencimento.pack(fill="x", pady=(0, 10))
        
        # Descrição
        ctk.CTkLabel(form, text="Observações:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 5))
        self.text_obs = ctk.CTkTextbox(form, height=80)
        self.text_obs.pack(fill="x", pady=(0, 15))
        
        # Botões
        frame_btns = ctk.CTkFrame(form, fg_color="transparent")
        frame_btns.pack(fill="x", pady=10)
        
        ctk.CTkButton(
            frame_btns,
            text="💾 SALVAR PRAZO",
            command=self.salvar_prazo,
            fg_color="#228B22",
            hover_color="#32CD32",
            height=45,
            font=("Arial", 13, "bold")
        ).pack(fill="x", pady=(0, 5))
        
        ctk.CTkButton(
            frame_btns,
            text="🗑️ LIMPAR",
            command=self.limpar_form,
            fg_color="#8B0000",
            hover_color="#A52A2A",
            height=40
        ).pack(fill="x")
    
    def calcular_vencimento(self):
        """Calcula data de vencimento"""
        try:
            data_inicial_str = self.entry_data_inicial.get().strip()
            dias_str = self.entry_dias.get().strip()
            
            if not data_inicial_str or not dias_str:
                msg.showerror("Erro", "Preencha a data inicial e quantidade de dias!")
                return
            
            data_inicial = datetime.strptime(data_inicial_str, "%d/%m/%Y")
            dias_uteis = int(dias_str)
            
            data_vencimento = calcular_prazo(data_inicial, dias_uteis)
            
            self.entry_vencimento.delete(0, "end")
            self.entry_vencimento.insert(0, data_vencimento.strftime("%d/%m/%Y"))
            
            msg.showinfo(
                "Cálculo Concluído",
                f"✅ Prazo de {dias_uteis} dias úteis\n"
                f"📅 Vence em: {data_vencimento.strftime('%d/%m/%Y')} ({data_vencimento.strftime('%A')})"
            )
            
        except ValueError:
            msg.showerror("Erro", "Data inválida! Use o formato DD/MM/AAAA")
        except Exception as e:
            msg.showerror("Erro", f"Erro ao calcular: {str(e)}")
    
    def salvar_prazo(self):
        """Salva novo prazo"""
        processo = self.entry_processo.get().strip()
        tipo = self.combo_tipo.get()
        vencimento = self.entry_vencimento.get().strip()
        obs = self.text_obs.get("1.0", "end").strip()
        
        if not processo or not vencimento:
            msg.showerror("Erro", "Preencha processo e data de vencimento!")
            return
        
        # Validar data
        try:
            datetime.strptime(vencimento, "%d/%m/%Y")
        except:
            msg.showerror("Erro", "Data de vencimento inválida!")
            return
        
        prazo = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "processo": processo,
            "tipo": tipo,
            "vencimento": vencimento,
            "observacoes": obs,
            "data_cadastro": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "status": "ativo"
        }
        
        self.dados_prazos["prazos"].append(prazo)
        
        if salvar_prazos(self.dados_prazos):
            msg.showinfo("Sucesso", "✅ Prazo cadastrado com sucesso!")
            self.limpar_form()
            self.atualizar_lista()
    
    def limpar_form(self):
        """Limpa formulário"""
        self.entry_processo.delete(0, "end")
        self.entry_data_inicial.delete(0, "end")
        self.entry_dias.delete(0, "end")
        self.entry_vencimento.delete(0, "end")
        self.text_obs.delete("1.0", "end")
        self.combo_tipo.set("Contestação")
    
    def atualizar_lista(self):
        """Atualiza lista de prazos"""
        for widget in self.scroll_prazos.winfo_children():
            widget.destroy()
        
        prazos_ativos = [p for p in self.dados_prazos["prazos"] if p["status"] == "ativo"]
        
        if not prazos_ativos:
            ctk.CTkLabel(
                self.scroll_prazos,
                text="📭 Nenhum prazo cadastrado",
                font=("Arial", 14),
                text_color="#888888"
            ).pack(pady=50)
            return
        
        # Ordenar por vencimento
        prazos_ativos.sort(key=lambda x: datetime.strptime(x["vencimento"], "%d/%m/%Y"))
        
        for prazo in prazos_ativos:
            dias = dias_restantes(prazo["vencimento"])
            cor = cor_por_urgencia(dias)
            
            frame_prazo = ctk.CTkFrame(self.scroll_prazos, fg_color="#1a1a1a", corner_radius=10)
            frame_prazo.pack(fill="x", pady=5, padx=10)
            
            # Header do prazo
            frame_header = ctk.CTkFrame(frame_prazo, fg_color="transparent")
            frame_header.pack(fill="x", padx=15, pady=10)
            
            # Urgência
            if dias < 0:
                urgencia_text = f"⚠️ VENCIDO HÁ {abs(dias)} DIAS"
            elif dias == 0:
                urgencia_text = "🔴 VENCE HOJE!"
            elif dias == 1:
                urgencia_text = "🟠 VENCE AMANHÃ"
            else:
                urgencia_text = f"🟢 {dias} dias úteis restantes"
            
            ctk.CTkLabel(
                frame_header,
                text=urgencia_text,
                font=("Arial", 13, "bold"),
                text_color=cor
            ).pack(side="left")
            
            # Botão concluir
            def concluir_prazo(prazo_id=prazo["id"]):
                if msg.askyesno("Confirmar", "Marcar este prazo como concluído?"):
                    for p in self.dados_prazos["prazos"]:
                        if p["id"] == prazo_id:
                            p["status"] = "concluido"
                            break
                    salvar_prazos(self.dados_prazos)
                    self.atualizar_lista()
            
            ctk.CTkButton(
                frame_header,
                text="✅ Concluir",
                command=concluir_prazo,
                fg_color="#228B22",
                hover_color="#32CD32",
                width=100,
                height=30
            ).pack(side="right", padx=5)
            
            # Botão excluir
            def excluir_prazo(prazo_id=prazo["id"]):
                if msg.askyesno("Confirmar", "Excluir este prazo?"):
                    self.dados_prazos["prazos"] = [
                        p for p in self.dados_prazos["prazos"] 
                        if p["id"] != prazo_id
                    ]
                    salvar_prazos(self.dados_prazos)
                    self.atualizar_lista()
            
            ctk.CTkButton(
                frame_header,
                text="🗑️",
                command=excluir_prazo,
                fg_color="#8B0000",
                hover_color="#A52A2A",
                width=40,
                height=30
            ).pack(side="right")
            
            # Informações do prazo
            frame_info = ctk.CTkFrame(frame_prazo, fg_color="transparent")
            frame_info.pack(fill="x", padx=15, pady=(0, 10))
            
            info_text = f"📋 {prazo['processo']} | {prazo['tipo']}\n"
            info_text += f"📅 Vencimento: {prazo['vencimento']}\n"
            if prazo.get('observacoes'):
                info_text += f"📝 {prazo['observacoes']}"
            
            ctk.CTkLabel(
                frame_info,
                text=info_text,
                font=("Arial", 11),
                text_color="#CCCCCC",
                justify="left"
            ).pack(anchor="w")

def abrir_gestao_prazos(parent):
    """Abre janela de gestão de prazos"""
    janela = JanelaPrazos(parent)
    janela.grab_set()
