# ⚙️ API - Sistema de Banco de Questões

Uma API RESTful desenvolvida para gerenciar o Sistema de Banco de Questões, projeto integrante da residência tecnológica do IFB - Campus São Sebastião.

## 📋 Sobre o Projeto
Este repositório contém o código-fonte do backend (API) que alimenta a interface do frontend, sendo responsável pela regra de negócio, persistência de dados, rotas de segurança (RBAC) e, futuramente, integração com Inteligência Artificial para geração de questões e motores de exportação multiformato.

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.x
* **Framework:** Django & Django REST Framework (DRF)
* **Banco de Dados:** SQLite (Desenvolvimento)
* **Autenticação:** JWT (JSON Web Tokens) via `djangorestframework-simplejwt`
* **Documentação da API:** Swagger UI via `drf-spectacular`
* **Integração IA:** *A decidir - ex: API da OpenAI ou Gemini*
* **Gerador de PDF/XML:** *A decidir*

## ✨ Funcionalidades e Roadmap
O desenvolvimento está dividido nas seguintes etapas (Quinzenas 1 a 6):

* [x] Modelagem do banco de dados (Categorias, Tags, Questões, Alternativas, Perfis, Histórico e Mídias).
* [x] Desenvolvimento dos Endpoints REST (CRUD) e validação de regras de negócio (5 alternativas).
* [x] Sistema de Autenticação (JWT) e Autorização/Níveis de Acesso (RBAC).
* [ ] Sistema de Filtros de busca (por tag, categoria e autor usando `django-filter`).
* [ ] Integração com IA Generativa para criação automatizada de questões.
* [ ] Motor de Exportação de arquivos (CSV, PDF formatado e XML padrão Moodle).

## 🚀 Como Rodar Localmente

### Pré-requisitos
* Python 3.10 ou superior
* Git

### Passo a Passo de Instalação

1. **Clone o repositório e acesse a pasta:**
```bash
git clone [https://github.com/ArthurDaniel02/banco-questoes-ifb](https://github.com/ArthurDaniel02/banco-questoes-ifb)
cd banco-questoes-ifb
Crie e ative o ambiente virtual:

PowerShell
python -m venv venv

# No Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# No Linux/Mac:
source venv/bin/activate
Instale as dependências:

PowerShell
pip install django djangorestframework djangorestframework-simplejwt django-filter drf-spectacular drf-spectacular[sidecar] Pillow
(Nota: futuramente adicionaremos um arquivo requirements.txt para facilitar este passo).

Crie o banco de dados e aplique as migrações:

PowerShell
python manage.py makemigrations
python manage.py migrate
Crie um usuário administrador:

PowerShell
python manage.py createsuperuser
Execute o servidor local:

PowerShell
python manage.py runserver
📚 Acessando a Documentação
Com o servidor rodando, você pode acessar a documentação interativa da API (Swagger) no seu navegador através do link:
👉 https://www.google.com/search?q=http://127.0.0.1:8000/api/docs/


Depois de colar e salvar, é só mandar aqueles comandinhos básicos para o GitHub que você mesmo lembrou:
```bash
git add README.md
git commit -m "docs: formata readme e atualiza checkboxes da sprint"
git push origin main