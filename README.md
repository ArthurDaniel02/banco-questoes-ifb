# ⚙️ API - Sistema de Banco de Questões IFB 🎓

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.2%2B-green.svg?logo=Django)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Render](https://img.shields.io/badge/Render-Deploy-black?logo=render)](https://render.com/)

Uma API RESTful desenvolvida para gerenciar o Sistema de Banco de Questões, projeto integrante da residência tecnológica do IFB - Campus São Sebastião.

## 🚀 Live Demo
> **Acesse a API em produção:** [https://api-banco-questoes.onrender.com/api/docs/](https://api-banco-questoes.onrender.com/api/docs/)

---

## 📑 Sumário
- [Visão Geral](#-visão-geral)
- [Problema que Resolve](#-problema-que-resolve)
- [Público-Alvo e Níveis de Acesso](#-público-alvo-e-níveis-de-acesso-rbac)
- [Funcionalidades e Roadmap](#-funcionalidades-e-roadmap)
- [Pacotes Utilizados](#-pacotes-utilizados)
- [Documentação da API (Endpoints)](#-documentação-da-api)
- [Como Rodar Localmente](#-como-rodar-localmente)
- [Deploy (Produção)](#-deploy-produção)

---

## 🔭 Visão Geral
Este repositório contém o código-fonte do backend (API) que alimenta a interface do frontend do Banco de Questões. O sistema é responsável pela regra de negócio, persistência de dados, rotas de segurança e integração com Inteligência Artificial (Gemini) para geração automatizada de questões em múltiplos formatos.

## 🎯 Problema que Resolve
A elaboração e gestão de questões avaliativas é um processo demorado e suscetível a repetições. O sistema centraliza o acervo da instituição, permite a categorização inteligente por tags e níveis de dificuldade, aplica controle de "frescor" (evitando o reuso frequente da mesma questão) e agiliza o trabalho docente através da geração de rascunhos de questões via IA.

## 👥 Público-Alvo e Níveis de Acesso (RBAC)
O sistema foi projetado para atender o corpo docente e a gestão pedagógica, dividindo-se em:
* **Docentes:** Podem criar questões abertas e fechadas, gerenciar suas alternativas, gerar rascunhos com IA e visualizar o banco.
* **Coordenadores:** Possuem privilégios administrativos. Podem cadastrar novos docentes, excluí-los e realizar todas as ações de gestão do banco.

## ✨ Funcionalidades e Roadmap
O desenvolvimento está dividido nas seguintes etapas:
- [x] Modelagem do banco de dados (Categorias, Tags, Questões, Alternativas, Perfis e Histórico).
- [x] Desenvolvimento dos Endpoints REST (CRUD) e validação de regras de negócio estritas.
- [x] Sistema de Autenticação (JWT) e Autorização/Níveis de Acesso (RBAC).
- [x] Sistema de Filtros de busca (por tag, categoria e autor).
- [x] Integração com IA Generativa (Gemini 1.5) para criação automatizada de questões em lote.

---

## 🛠️ Pacotes Utilizados

| Pacote | Função / Descrição |
|--------|--------------------|
| `django` | Framework web principal |
| `djangorestframework` | Toolkit para construção da API REST |
| `djangorestframework-simplejwt` | Autenticação e segurança via JSON Web Tokens (JWT) |
| `django-filter` | Sistema de buscas e filtros dinâmicos nas rotas |
| `drf-spectacular` | Documentação interativa automática (Swagger UI) |
| `google-genai` | Integração com a API do Google Gemini para geração de questões |
| `gunicorn` & `whitenoise` | Servidor WSGI e gerenciador de estáticos para ambiente de produção |

---

## 📚 Documentação da API

A documentação interativa completa (com Schemas e testes em tempo real) está disponível na rota `/api/docs/` utilizando o Swagger UI.

### 🔐 Como Autenticar
1. Vá até a rota `POST /api/login/` e insira seu usuário e senha.
2. Copie o token retornado no campo `access`.
3. Clique no botão **Authorize** no topo do Swagger, cole o token e aplique.

### 📍 Endpoints Principais

| Categoria | Método | Endpoint | Descrição | Acesso |
|-----------|--------|----------|-----------|--------|
| **Autenticação** | POST | `/api/login/` | Gera os tokens JWT de acesso | Público |
| **Autenticação** | POST | `/api/login/refresh/` | Renova o token expirado | Público |
| **Usuários** | GET/POST | `/api/usuarios/` | Gerenciamento de docentes | Coordenador |
| **Questões** | GET/POST | `/api/questoes/` | Lista, filtra e cria questões | Docente |
| **Questões (IA)** | POST | `/api/questoes-gerar-ia/` | Gera 10 questões inéditas via Gemini | Docente |
| **Histórico** | POST | `/api/questoes/{id}/registrar_uso/`| Registra log de exportação (frescor) | Docente |
| **Alternativas** | GET/POST | `/api/alternativas/` | Gerencia as alternativas de uma questão | Docente |
| **Categorias** | GET/POST | `/api/categorias/` | CRUD de categorias de disciplinas | Docente* |
| **Tags** | GET/POST | `/api/tags/` | CRUD de tags de conteúdo | Docente |

*(Nota: Rotas com `GET/POST` também possuem suporte a `PUT`, `PATCH` e `DELETE` fornecendo o `{id}` do recurso).*

---

## 🚀 Como Rodar Localmente

### Pré-requisitos
* Python 3.12
* Git

### Passo a Passo de Instalação
```bash
1. **Clone o repositório e acesse a pasta:**
git clone [https://github.com/ArthurDaniel02/banco-questoes-ifb](https://github.com/ArthurDaniel02/banco-questoes-ifb)
cd banco-questoes-ifb

2. **Crie e ative o ambiente virtual:**
```bash
python -m venv venv
# Windows: .\venv\Scripts\Activate.ps1
# Linux/Mac: source venv/bin/activate

3. Instale as dependências:
```bash
pip install -r requirements.txt

4. Variáveis de Ambiente:
Crie um arquivo .env na raiz do projeto (opcional localmente) ou defina a chave da API do Gemini diretamente no sistema para testar a geração de questões.

5. Crie o banco de dados e o superusuário:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

6.Execute o servidor local:
```bash
python manage.py runserver
Acesse localmente em: http://127.0.0.1:8000/api/docs/

☁️ Deploy (Produção)
A API está hospedada na plataforma Render.com, utilizando variáveis de ambiente para proteção de chaves e banco de dados PostgreSQL.

Root Directory: bancoquestoes

Build Command: sh build.sh (Executa instalações, coleta de estáticos e migrações do banco)

Start Command: gunicorn bancoquestoes.wsgi:application