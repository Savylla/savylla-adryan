# AGENTS.md — Site Savylla Adryan

As instruções deste projeto vivem em [`.claude/CLAUDE.md`](.claude/CLAUDE.md).
Leia aquele arquivo: ele descreve o site, o mapa de diretórios, como o deploy no
GitHub Pages funciona e qual sistema está instalado.

Resumo do essencial:

- Site estático, sem build step. `index.html`, `servicos.html`, `style.css`,
  `script.js`, `servicos.js` e `assets/` são o site; os `.py` e `.json` da raiz são
  o pipeline de vídeos, não conteúdo publicado.
- O deploy monta o artefato por lista de inclusão e só dispara quando um arquivo do
  site muda. Alterações em `.claude/` ou `.sinkra/` não publicam nada.
- Escreva em português, com acentuação correta.
- `push`, PR e release são exclusivos do `@devops`.

O AIOX legacy (`.aiox-core/`, agentes por arquivo em `.codex/`, `.gemini/`, `.kimi/`,
`.antigravity/`, `.cursor/`) foi aposentado em 11/08/2026. O sistema atual é o
SINKRA-OS 3.1.9 com o AIOX Cockpit — as skills e os agentes vêm de `.claude/skills/`,
`.claude/agents/` e da camada global em `~/.claude/skills`.
