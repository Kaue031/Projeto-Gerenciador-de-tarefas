# Gerenciador de Tarefas (CRUD) — Documentação de implementação

Este README descreve passo a passo **como o gerenciador de tarefas foi construído** (arquivos, rotas, banco de dados, e estrutura de commits). Está em português e foi pensado para explicar claramente o que foi feito em cada etapa/commit.

---

## Visão geral do projeto

- **Tecnologias:** Python 3 + Flask, SQLite (sqlite3), HTML (Jinja2 templates), CSS simples.
- **Estrutura de pastas:**
  ```
  gerenciador_tarefas/
  ├─ app.py
  ├─ db.py
  ├─ requirements.txt
  ├─ README.md
  ├─ templates/
  │  ├─ base.html
  │  ├─ index.html
  │  ├─ add.html
  │  ├─ task.html
  │  └─ edit.html
  ├─ static/
  │  └─ style.css
  └─ .github/workflows/ci.yml
  ```

---

## Passo a passo — como o projeto foi desenvolvido (10 commits)

### Commit 1 — app inicial (Flask mínimo)
- Arquivo: `app.py`
- O que foi feito:
  - Criado um app Flask mínimo (`Flask(__name__)`).
  - Rota `/` que renderiza a lista de tarefas (inicialmente em memória).
- Objetivo: ter a aplicação rodando e uma página inicial mínima.

### Commit 2 — templates iniciais
- Arquivos: `templates/base.html`, `templates/index.html`
- O que foi feito:
  - `base.html` define o layout básico (head, link para CSS, container).
  - `index.html` extende `base.html` e lista tarefas.
- Objetivo: separar layout e conteúdo usando Jinja2.

### Commit 3 — rota e formulário para criar tarefas
- Arquivos: `templates/add.html`, atualização em `app.py`
- O que foi feito:
  - Adicionada rota `/add` com formulário para título e descrição.
  - Rota `/create` (`POST`) que recebe o form e adiciona a tarefa (inicialmente em memória).
- Objetivo: permitir criação de tarefas via interface.

### Commit 4 — estilização básica
- Arquivo: `static/style.css`
- O que foi feito:
  - CSS simples para visual limpo (container central, botões, formulários).
- Objetivo: deixar a interface apresentável.

### Commit 5 — página de detalhes da tarefa
- Arquivos: `templates/task.html`, atualização em `templates/index.html`, `app.py`
- O que foi feito:
  - Rota `/task/<id>` para exibir detalhes (título + descrição).
  - Links na lista para acessar a página de detalhe.
- Objetivo: ver a tarefa completa e ter ações futuras (editar/excluir).

### Commit 6 — persistência com SQLite
- Arquivos: `db.py`, ajustes em `app.py`
- O que foi feito:
  - Criado `db.py` com `get_conn()` e `init_db()` usando `sqlite3`.
  - Estrutura da tabela `tasks` (id, title, desc).
  - `app.py` atualizado para inicializar o DB (`db.init_db()`).
- Objetivo: salvar tarefas entre reinícios (persistência).

### Commit 7 — CRUD com DB (create + read)
- Arquivo: `app.py` (ajustado para usar SQLite)
- O que foi feito:
  - Implementadas consultas para listar tarefas (`SELECT id, title FROM tasks`).
  - `create()` agora insere no banco (`INSERT INTO tasks`).
  - `task_detail()` busca a tarefa por `id`.
- Objetivo: formalizar create e read usando SQLite.

### Commit 8 — Update e Delete (editar e excluir)
- Arquivos: `app.py`, `templates/edit.html`
- O que foi feito:
  - Rotas: `/edit/<id>` (GET), `/update/<id>` (POST), `/delete/<id>` (POST).
  - `edit.html` permite alterar título e descrição; `delete` remove do banco.
- Objetivo: completar o CRUD.

### Commit 9 — arquivos auxiliares
- Arquivos: `requirements.txt`, `README.md` (versão inicial)
- O que foi feito:
  - Adicionado `requirements.txt` (Flask).
  - README com instruções básicas.
- Objetivo: preparar para execução local e documentação.

### Commit 10 — GitHub Actions workflow
- Arquivo: `.github/workflows/ci.yml`
- O que foi feito:
  - Workflow que instala dependências e executa um *smoke test* (importa Flask, importa `app` e checa `GET /` com `app.test_client()`).
- Objetivo: rodar checagens automáticas em push/pull_request.

---

## Como o código funciona — explicação rápida das principais partes

### app.py
- Define o objeto `app = Flask(__name__)`.
- Inicializa o banco chamando `db.init_db()`.
- Rotas principais:
  - `GET /` — lista de tarefas (consulta `tasks` no DB).
  - `GET /add` — formulário para criar tarefa.
  - `POST /create` — insere tarefa no DB.
  - `GET /task/<id>` — mostra detalhe da tarefa.
  - `GET /edit/<id>` — mostra formulário de edição.
  - `POST /update/<id>` — atualiza a tarefa.
  - `POST /delete/<id>` — exclui a tarefa.
- Uso de `redirect(url_for(...))` para navegação pós-form.

### db.py
- `get_conn()` — abre conexão SQLite com `row_factory=sqlite3.Row`.
- `init_db()` — cria tabela `tasks` caso não exista.

### Templates (Jinja2)
- `base.html` — layout base e link para CSS.
- `index.html` — itera sobre `tasks` e exibe links `ver`/`editar`.
- `add.html` / `edit.html` — formulários para criar/editar.
- `task.html` — detalhamento com botão de excluir.

---

## Como rodar localmente (resumo rápido)
1. Criar e ativar venv:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # mac/linux
   # PowerShell (Windows):
   # .\venv\Scripts\Activate.ps1
   ```
2. Instalar dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Rodar:
   ```bash
   python app.py
   ```
4. Abrir `http://127.0.0.1:5000` no navegador.

---

## Notas de desenvolvimento e sugestões de melhorias
- **Validações:** atualmente só valida título obrigatório; adicionar validação adicional e mensagens de erro.
- **Autenticação:** pode-se adicionar login para multiusuário.
- **Front-end:** usar framework (Bootstrap, Tailwind) para UI mais rica.
- **Testes:** adicionar testes com `pytest` e fixtures para banco temporário (SQLite in-memory).
- **CI:** workflow atual faz smoke test; expandir para rodar `pytest`, linters (flake8), e checks de segurança.

---

## Contato / Créditos
- Projeto gerado e organizado conforme solicitado — preparado para 10 commits distintos e com workflow pronto para GitHub Actions.
- Se quiser, posso gerar também um script `create_commits_and_push.sh` para automatizar a criação dos 10 commits e o push para seu repositório remoto.
