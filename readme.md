# 🏛️ Sistema de Gestão Jurídica - Vanessa Alves

Sistema completo de gestão para escritórios de advocacia com recursos avançados de automação, IA e integração.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Ativo-success.svg)

---

## 📋 **Índice**

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Módulos](#módulos)
- [Requisitos](#requisitos)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## 🎯 **Sobre o Projeto**

Sistema profissional desenvolvido para advocacia, com foco em:
- **Automação** de tarefas repetitivas
- **Inteligência Artificial** para análise jurídica
- **Gestão completa** de clientes e processos
- **Importação automática** de documentos
- **Geração de petições** personalizadas

---

## ✨ **Funcionalidades**

### 🔹 **Sistema Base**
- ✅ Cadastro completo de clientes
- ✅ Gestão de processos por área do direito
- ✅ Importação automática de PDFs e DOCX
- ✅ Detecção inteligente de nomes das partes
- ✅ Geração automática de petições
- ✅ Busca avançada em tempo real
- ✅ Backup automático de dados
- ✅ Interface moderna e intuitiva

### 🔹 **Módulos Avançados**

#### 📅 **Controle de Prazos**
- Calendário jurídico integrado
- Contagem automática de prazos
- Alertas por email antes do vencimento
- Consideração de feriados forenses
- Dashboard de prazos críticos

#### 🤖 **Assistente IA Jurídico**
- Chat integrado com IA
- Análise de documentos
- Sugestão de teses e argumentos
- Revisão automática de petições
- Pesquisa jurídica assistida

#### 🔍 **Jurisprudência**
- Busca em tribunais (STF, STJ, TJs)
- Download e organização de decisões
- Biblioteca de precedentes
- Marcação de favoritos
- Exportação de pesquisas

#### 📰 **Monitor DJe**
- Consulta automática de publicações
- Download de intimações
- Alertas de movimentações
- Histórico de publicações

#### 📊 **Dashboard Avançado**
- Gráficos e estatísticas
- Relatórios personalizados
- Taxa de sucesso por área
- Exportação em PDF/Excel
- Análise de desempenho

---

## 🔧 **Instalação**

### **Pré-requisitos**
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### **Passo a Passo**

1. **Clone o repositório:**
```bash
git clone https://github.com/SEU_USUARIO/vanessa-alves-juridico.git
cd vanessa-alves-juridico
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute o sistema:**
```bash
python sistema_principal.py
```

---

## 📖 **Como Usar**

### **Cadastro de Clientes**
1. Acesse a aba **"👤 Cliente"**
2. Preencha os dados do cliente
3. Clique em **"💾 SALVAR CLIENTE"**

### **Importação Automática**
1. Vá para **"📤 Importar"**
2. Selecione arquivos PDF ou DOCX
3. Sistema detecta automaticamente os nomes
4. Escolha quem é o cliente
5. Processo importado e vinculado!

### **Geração de Petições**
1. Acesse **"📄 Petição"**
2. Digite CPF do cliente e nº do processo
3. Clique em **"GERAR PETIÇÃO"**
4. Documento criado automaticamente!

---

## 🧩 **Módulos**

### **Sistema Principal** (`sistema_principal.py`)
Sistema base com todas as funcionalidades essenciais.

### **Controle de Prazos** (`modulo_prazos.py`)
Gestão completa de prazos processuais com alertas.

### **Assistente IA** (`modulo_ai_assistente.py`)
ChatBot jurídico integrado com análise de documentos.

### **Jurisprudência** (`modulo_jurisprudencia.py`)
Busca e organização de decisões judiciais.

### **Monitor DJe** (`modulo_dje.py`)
Acompanhamento de publicações oficiais.

### **Dashboard** (`modulo_dashboard.py`)
Estatísticas e relatórios avançados.

---

## 📦 **Requisitos**

Principais bibliotecas utilizadas:

```
customtkinter==5.2.0
python-docx==0.8.11
PyPDF2==3.0.1
requests==2.31.0
beautifulsoup4==4.12.2
matplotlib==3.7.1
pandas==2.0.3
openpyxl==3.1.2
```

Veja o arquivo completo em [`requirements.txt`](requirements.txt)

---

## 🎨 **Screenshots**

### Tela Principal
![Sistema Principal](https://via.placeholder.com/800x500?text=Sistema+Principal)

### Importação Automática
![Importação](https://via.placeholder.com/800x500?text=Importação+Automática)

### Geração de Petições
![Petições](https://via.placeholder.com/800x500?text=Geração+de+Petições)

---

## 🤝 **Contribuição**

Contribuições são bem-vindas! Siga os passos:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

---

## 📝 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📧 **Contato**

**Vanessa Alves Advocacia**
- Website: [em desenvolvimento]
- Email: contato@vanessaalves.adv.br
- LinkedIn: [Vanessa Alves]

---

## 🙏 **Agradecimentos**

- CustomTkinter pela biblioteca de interface moderna
- Comunidade Python Brasil
- Todos os contribuidores do projeto

---

## 📊 **Estatísticas do Projeto**

![GitHub stars](https://img.shields.io/github/stars/SEU_USUARIO/vanessa-alves-juridico?style=social)
![GitHub forks](https://img.shields.io/github/forks/SEU_USUARIO/vanessa-alves-juridico?style=social)
![GitHub issues](https://img.shields.io/github/issues/SEU_USUARIO/vanessa-alves-juridico)

---

## 🔄 **Roadmap**

- [x] Sistema base de gestão
- [x] Importação automática
- [x] Geração de petições
- [ ] Integração com PJe
- [ ] App mobile
- [ ] API REST
- [ ] Sistema de autenticação
- [ ] Multi-usuário

---

## 💡 **Dicas de Uso**

### Para melhor desempenho:
- Use arquivos DOCX para importação rápida
- Mantenha backups regulares
- Revise dados importados antes de usar
- Configure alertas de prazos

### Atalhos úteis:
- `Ctrl + F` - Busca rápida
- `Ctrl + N` - Novo cliente
- `Ctrl + P` - Gerar petição

---

**Desenvolvido com ❤️ para advocacia moderna**
