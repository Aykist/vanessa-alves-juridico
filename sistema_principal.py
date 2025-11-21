import customtkinter as ctk


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # === CONFIGURAÇÃO BÁSICA DA JANELA ===
        ctk.set_appearance_mode("dark")          # "dark", "light" ou "system"
        ctk.set_default_color_theme("blue")      # tema padrão

        self.title("Sistema Jurídico - Vanessa Alves")
        self.geometry("1100x650")
        self.minsize(900, 500)

        # Grade principal: 1 linha, 2 colunas (menu lateral + área de conteúdo)
        self.grid_columnconfigure(0, weight=0)   # menu lateral
        self.grid_columnconfigure(1, weight=1)   # conteúdo
        self.grid_rowconfigure(0, weight=1)

        # === MENU LATERAL ===
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)  # empurrar itens pra cima

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Vanessa Alves\nJurídico",
            font=ctk.CTkFont(size=18, weight="bold"),
            justify="center"
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_dashboard = ctk.CTkButton(
            self.sidebar_frame,
            text="Dashboard",
            command=lambda: self.mudar_pagina("dashboard")
        )
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        self.btn_clientes = ctk.CTkButton(
            self.sidebar_frame,
            text="Clientes",
            command=lambda: self.mudar_pagina("clientes")
        )
        self.btn_clientes.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.btn_processos = ctk.CTkButton(
            self.sidebar_frame,
            text="Processos",
            command=lambda: self.mudar_pagina("processos")
        )
        self.btn_processos.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        self.btn_juris = ctk.CTkButton(
            self.sidebar_frame,
            text="Jurisprudência",
            command=lambda: self.mudar_pagina("juris")
        )
        self.btn_juris.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        self.btn_chat_ia = ctk.CTkButton(
            self.sidebar_frame,
            text="Chatbot IA",
            command=lambda: self.mudar_pagina("chat_ia")
        )
        self.btn_chat_ia.grid(row=5, column=0, padx=20, pady=5, sticky="ew")

        # Botão de sair (parte de baixo)
        self.btn_sair = ctk.CTkButton(
            self.sidebar_frame,
            text="Sair",
            fg_color="#8b0000",
            hover_color="#a00000",
            command=self.fechar_sistema
        )
        self.btn_sair.grid(row=6, column=0, padx=20, pady=(40, 20), sticky="ew")

        # === ÁREA PRINCIPAL DE CONTEÚDO ===
        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Label inicial
        self.label_titulo = ctk.CTkLabel(
            self.content_frame,
            text="Dashboard - Sistema Jurídico",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label_titulo.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.label_descricao = ctk.CTkLabel(
            self.content_frame,
            text=(

