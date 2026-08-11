# Site Savylla Adryan — instruções do projeto

Site pessoal estático (portfólio), publicado no GitHub Pages a partir de
`Savylla/savylla-adryan`. **Não há build step**: o HTML, o CSS e o JS da raiz são
servidos como estão.

## Mapa

| Caminho | O que é |
|---|---|
| `index.html`, `servicos.html`, `style.css`, `script.js`, `servicos.js` | o site |
| `assets/` | imagens, fontes autohospedadas, capas dos projetos |
| `*.py` na raiz (43 scripts) | pipeline de vídeos ClickUp → YouTube — ferramenta, não conteúdo do site |
| `*.json` na raiz | estado do pipeline de vídeos (`client_videos.json`, `youtube_results.json`, …) |
| `.github/workflows/deploy-pages.yml` | deploy no Pages |
| `docs/` | documentação |

## Deploy

O workflow monta `_site/` por **lista de inclusão**, não de exclusão — só entram os
arquivos do site. Se um arquivo da lista sumir, o `cp` falha e o deploy para ali,
de propósito.

O push só dispara o deploy quando muda um dos paths listados no `on.push.paths`.
Mexer em `.claude/`, `.sinkra/` ou nos scripts do pipeline **não** publica nada.

O job vive perto do teto de 10 minutos da `actions/deploy-pages` — o artefato
enxuto existe justamente para caber nele. Não adicione diretórios ao `_site` sem
medir.

## Sistema instalado

| Camada | Onde |
|---|---|
| **SINKRA-OS 3.1.9** | `.sinkra/`, skills `S01`–`S04`, `/sinkra-pipeline`, `/sinkra-create-skill`, `/sinkra-update`, `/pedro-advisor` |
| **AIOX Cockpit** | `.aiox/` (protocol v3), skills globais em `~/.claude/skills` |
| Agentes do bundle | `.claude/agents/` |
| Rules | `.claude/rules/` — carregadas automaticamente |

O **AIOX legacy foi aposentado em 11/08/2026**: `.aiox-core/`, `.claude/commands/AIOX/`,
`.claude/skills/AIOX/`, os hooks do projeto e os espelhos de IDE (`.codex/`, `.gemini/`,
`.kimi/`, `.antigravity/`, `.cursor/`) saíram do git e do disco. Referências a
`.aiox-core/development/…`, à Constitution antiga ou aos agentes por arquivo
(`@dev` → `.aiox-core/development/agents/dev.md`) são resquício — o histórico do git
guarda tudo, mas nada disso existe mais na árvore.

## Convenções

- Responda e escreva em **português**, com acentuação correta.
- Git: conventional commits. `push`, PR e release são exclusivos do `@devops`.
- Segredos ficam no `.env` (gitignorado); o `.env.example` documenta as chaves sem valores.
