# SupportBase — contexto fixo para o Claude Code

## Sobre o projeto
Base de conhecimento de suporte técnico (problemas, categorias, atalhos de texto).
Começou desktop (Flet), migrou para web. Projeto solo, feito para aprender e para portfólio.

## Stack
- Backend: Python + FastAPI, PostgreSQL 16 em Docker, psycopg2 direto (SEM ORM)
- Conexão: `config.py` cria um `conn` global com `RealDictCursor` (as linhas vêm como dict)
- Frontend: ainda não iniciado. Será React depois do backend, com CORS no FastAPI
- Bancos: `supportbase_test` (testes, carregado por `.env.test` no `conftest.py`) e `supportbase_prod`
- Ambiente do dev: CachyOS (Arch), Fish shell, VSCode, DBeaver, Docker. O banco roda no homelab, o host vem do `.env`

## Estrutura
- `main.py` — app FastAPI, chama `createTables()` e inclui os routers
- `config.py` — conexão com o banco
- `database/tables.py` — criação das tabelas
- `functions/support/` — services de `problems`, `categories`, `problems_categories`
- `functions/copy/shortcut.py` — service de atalhos
- `functions/photo/` — validação e compressão de imagem (Pillow)
- `functions/transcript/` — transcrição com faster-whisper
- `routes/` — um router por recurso, que só valida a entrada (Pydantic) e chama o service
- `requirements/` — `base.txt`, `arch.txt`, `dev.txt`

## Multi-tenant
- Tabelas `empresa` e `usuario` existem. `empresa_id` (NOT NULL, FK, ON DELETE RESTRICT) está em `problems`, `categories`, `problems_categories`, `shortcuts` e `settings`
- Todo service filtra por `empresa_id`
- `empresa_id` NUNCA entra no `SET` de um UPDATE, só no `WHERE`
- Atalhos (`shortcuts`) são pessoais: têm `usuario_id` (NOT NULL, FK) e os UNIQUE são `(short_cut_key, usuario_id)` e `(position, usuario_id)`.
  `usuario_id` é o último parâmetro das funções de `functions/copy/shortcut.py`, e as consultas filtram por `empresa_id` e `usuario_id`
- `settings` é por empresa, com PK composta `(empresa_id, setting_key)`
- `categories` tem `UNIQUE (name, empresa_id)`
- `database/tables.py` está alinhado com os bancos: um banco criado do zero sai idêntico ao `supportbase_test` e ao `supportbase_prod`.
  `empresa` e `usuario` são criadas antes das tabelas que as referenciam

## Convenções do backend
- Placeholders do PostgreSQL são `%s`. Nunca f-string com valor vindo do usuário.
  F-string só para trechos fixos escolhidos por whitelist (ex.: ORDER BY)
- Colunas em snake_case
- `RETURNING id` + `fetchone()` no INSERT (não existe `cursor.lastrowid` no psycopg2)
- `COALESCE` nos UPDATEs parciais (PATCH), para atualizar só os campos enviados
- Padrão dos services: `with conn.cursor()` + `try/except`, `conn.commit()` nas escritas,
  `conn.rollback()` no erro, `print(error)` para debug
- Retorno de erro: `{"success": False, "errorMessage": "..."}`. Retorno de sucesso: `{"success": True, ...}`.
  Alguns services ainda retornam `rowcount` ou a linha direto: isso está na lista de padronização
- Soft delete (coluna `ativo`) em `problems` e `categories`. Hard delete em `shortcuts` e `problems_categories`
- Nas rotas, parâmetros sem valor padrão vêm antes dos com padrão
- A ORDEM dos parâmetros varia entre os services (ex.: `list_categories(empresa_id, incluir_inativo)`,
  `listProblemsByDate(ordemEscolhida, empresa_id, incluir_inativo)`). Conferir sempre a assinatura
  do service antes de escrever a chamada na rota

## Regras de trabalho (valem para toda tarefa)
- NÃO executar nada que altere o banco (ALTER, DROP, DELETE, INSERT, UPDATE) sem me mostrar os comandos e esperar minha confirmação
- `CREATE TABLE IF NOT EXISTS` não altera tabela existente: mudança de schema exige ALTER/DROP, nos DOIS bancos (test e prod)
- Depois de qualquer mudança de schema, verificar com `\d <tabela>` nos dois bancos
- NÃO criar nem alterar testes, a menos que eu peça. Eu escrevo os testes unitários
- NÃO alterar nada fora do escopo pedido. Se encontrar outro problema, listar no final em vez de corrigir
- Mudanças pequenas e incrementais, sem refatoração grande nem abstração prematura (YAGNI).
  Não criar camadas, classes ou arquivos novos sem necessidade
- Não adicionar dependências sem avisar
- Não commitar sem eu pedir
- Ao terminar, mostrar o `git diff` e explicar o PORQUÊ das decisões, não só o que mudou. Eu estou aprendendo e vou revisar
- Se eu pedir só uma explicação ou análise, não escrever código

## Como se comunicar comigo
- Português, direto, sem enrolação
- Comentários no código em português, explicando o raciocínio (é o estilo do projeto)
- Prefiro terminal e comandos que eu consiga entender e reproduzir

## Estado atual e pendências
Concluído: fase multi-tenant nas rotas e no schema. Todas as rotas recebem `empresa_id`, os 4 routers têm tags,
os dois bancos foram migrados e existe uma empresa e um usuário de teste nos dois (a senha é texto puro até o bcrypt entrar).

Próxima tarefa: `rollback()` no `except` de `validatePosition`, `listshortcutByPosition` e `listShortcutByDate`
(`functions/copy/shortcut.py`). Sem ele, um erro deixa a conexão global em "transaction aborted" e todas as requisições seguintes falham.

Pendências conhecidas (não mexer sem eu pedir):
- Unicidade ignorando a caixa: "Rede" e "rede" valem como nomes diferentes na mesma empresa.
  Opção recomendada: índice único sobre `lower(name)` + `empresa_id` (`CREATE UNIQUE INDEX`, no lugar do UNIQUE inline).
  Decidir se `short_cut_key` segue a mesma regra e se o `strip()` fica no service ou no Pydantic
- Categoria inativada continua ocupando o nome (o UNIQUE não olha `ativo`). Resolve com a rota de reativação
- FK composta em `problems_categories`: nada impede vincular problema de uma empresa a categoria de outra.
  Proposta: `UNIQUE (id, empresa_id)` em `problems` e `categories` + FKs compostas `(problem_id, empresa_id)` e `(category_id, empresa_id)`.
  A PK de `problems_categories` continua sem `empresa_id`
- `list_problems_categories` filtra só `problems_categories.empresa_id`, não `categories.empresa_id` (a FK composta resolve)
- Nada garante que o `usuario_id` de um atalho pertence ao `empresa_id` dele (mesma ideia da FK composta)
- `empresa_id` e `usuario_id` chegam do cliente sem autenticação, o que é esperado até entrar o JWT
- `body_create_shortcut.phrase` é Optional na rota, mas o service rejeita vazio e o banco tem NOT NULL
- Mensagem de erro genérica quando o banco bloqueia duplicata (falta tratar `UniqueViolation`)
- Faltam CRUDs de `empresa` e `usuario`
- A empresa de teste está no `supportbase_prod` (CNPJ `00000000000000`): apagar ou trocar antes de qualquer uso real

Backlog, baixa prioridade:
- Rota de upload de foto: `corruption_data()` -> `formats()` -> `decreaseQuality()`, checando `success` em cada etapa
- `delete_category` deve bloquear se houver problemas ATIVOS vinculados
- VARCHAR(n) no banco e `Field(max_length=...)` no Pydantic
- Tratar `UniqueViolation` e `ForeignKeyViolation` do psycopg2
- Padronizar retornos e mapear status HTTP (404 etc.)
- Rota de reativação (inverso do soft delete)

Roadmap: testes dos services, React, e por último JWT + bcrypt + connection pool
(rate limiting e scan de segurança só antes de expor na internet).