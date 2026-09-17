---
paths:
  - briefing.html
  - briefing.js
  - obrigado.html
  - servicos.html
  - sitemap.xml
  - .github/workflows/deploy-pages.yml
---

# O briefing não vai ao ar sem autorização nominal

O formulário de briefing (`briefing.html`, `briefing.js` e a página de retorno
`obrigado.html`) **não está aprovado pela dona do site**. Ela ainda vai mudar coisas
dentro dele. Até que autorize, esse material não pode chegar à produção.

Hoje ele está fora do ar por um motivo só: o workflow monta `_site/` por lista de
inclusão e essa lista não o menciona. Não existe nenhuma outra proteção — o
`briefing.html` carrega `<meta name="robots" content="index,follow">` e o `robots.txt`
permite tudo. Publicar é, portanto, um caminho de mão única: o Google indexa.

## A regra

**Nunca faça commit ou push de nada que exponha o briefing sem que a dona do site
tenha autorizado o briefing pelo nome, naquela conversa.**

Uma autorização genérica **não** serve. "pode dar push", "publica o site", "sobe as
correções" e "manda pra produção" autorizam o resto — nunca o briefing. A frase
precisa nomeá-lo: "publica o briefing", "pode subir o formulário de briefing".

## O que conta como expor o briefing

Qualquer um destes, isolado, já basta para vazá-lo:

| Alteração | Por que expõe |
|---|---|
| `briefing.html`, `briefing.js`, `obrigado.html` versionados | os arquivos em si |
| `deploy-pages.yml` com esses nomes no `cp` ou no `on.push.paths` | passa a copiá-los para `_site/` |
| `sitemap.xml` com a URL do briefing | anuncia a página ao Google |
| `servicos.html` com links `href="briefing.html..."` | 7 links visíveis no site |

Essas alterações já existem na árvore de trabalho, prontas e não commitadas. Elas
são trabalho legítimo, apenas não aprovado ainda — **não as reverta nem as apague**.
Deixe-as exatamente onde estão.

## Como publicar o resto com segurança

Faça `git add` nomeando os arquivos, um a um. Nunca `git add -A`, `git add .` nem
`git commit -a` neste repositório enquanto o briefing estiver pendente. Antes de
commitar, confira o que entrou:

```
git diff --cached --name-only
```

Se aparecer qualquer linha da tabela acima sem autorização nominal, desfaça o
staging e pergunte.

Depois do push, confirme que a produção continua limpa:

```
curl -s -o /dev/null -w "%{http_code}\n" https://savylla.github.io/savylla-adryan/briefing.html
curl -s https://savylla.github.io/savylla-adryan/servicos.html | grep -c briefing.html
```

O esperado é `404` e `0`. Qualquer outra coisa significa que o briefing vazou.

## Quando a autorização vier

Aí sim: commite os quatro itens da tabela juntos, e antes disso pergunte se o
`<meta name="robots">` do briefing deve continuar `index,follow` ou virar
`noindex,follow` como o do `obrigado.html` — um formulário de captação raramente
quer aparecer na busca.
