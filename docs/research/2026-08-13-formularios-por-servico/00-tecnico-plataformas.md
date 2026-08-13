# Camada técnica — como o formulário roda neste site

> Pesquisa de 13/08/2026. Todo preço e limite abaixo tem data e fonte na seção 8.
> Onde não consegui confirmar na documentação oficial do fornecedor, está escrito
> **não confirmado** — e não é para tratar como fato.

---

## 1. O terreno (lido do código, não pesquisado)

### 1.1 A CSP literal, hoje

São **duas CSP diferentes**, uma por página, declaradas em `<meta http-equiv>` (não em
header HTTP — o GitHub Pages não deixa configurar header).

**`index.html`, linha 34** — transcrição literal:

```
default-src 'self';
script-src 'self';
style-src 'self' 'unsafe-inline';
img-src 'self' data: https://i.ytimg.com https://img.youtube.com;
media-src 'self' blob:;
font-src 'self';
connect-src 'self' https://formsubmit.co;
frame-src https://www.youtube-nocookie.com https://www.youtube.com https://www.instagram.com;
form-action https://formsubmit.co;
base-uri 'self';
object-src 'none';
upgrade-insecure-requests
```

**`servicos.html`, linha 35** — transcrição literal (mais fechada; o comentário no
código diz o porquê: *"esta página não tem vídeo embedado, nem formulário, nem player
do YouTube"*):

```
default-src 'self';
script-src 'self';
style-src 'self' 'unsafe-inline';
img-src 'self' data:;
media-src 'none';
font-src 'self';
connect-src 'self';
frame-src 'none';
form-action 'none';
base-uri 'self';
object-src 'none';
upgrade-insecure-requests
```

Diretiva por diretiva, o que hoje é permitido:

| Diretiva | `index.html` | `servicos.html` | Leitura |
|---|---|---|---|
| `default-src` | `'self'` | `'self'` | tudo que não tem diretiva própria só vem do próprio domínio |
| `script-src` | `'self'` | `'self'` | **nenhum JS de terceiro.** Nem inline, nem CDN. É por isso que a `lite-yt-embed.js` foi vendorizada em `assets/lib/` |
| `style-src` | `'self' 'unsafe-inline'` | idem | CSS próprio + `style=""` inline permitido; nenhum CSS externo |
| `img-src` | `'self' data:` + `i.ytimg.com` + `img.youtube.com` | `'self' data:` | thumbs do YouTube liberadas só no index |
| `media-src` | `'self' blob:` | `'none'` | mp4 externo bloqueado — a armadilha já conhecida do projeto |
| `font-src` | `'self'` | `'self'` | fonte só autohospedada. Google Fonts não carrega |
| `connect-src` | `'self'` + **`https://formsubmit.co`** | `'self'` | `fetch`/XHR: só o próprio domínio e o FormSubmit |
| `frame-src` | `youtube-nocookie.com`, `youtube.com`, `instagram.com` | **`'none'`** | **`servicos.html` não pode carregar iframe nenhum hoje** |
| `form-action` | **`https://formsubmit.co`** | **`'none'`** | destino de `<form action>`; `servicos.html` proíbe qualquer submit |
| `base-uri` | `'self'` | `'self'` | anti sequestro de base |
| `object-src` | `'none'` | `'none'` | sem plugin/embed |
| `upgrade-insecure-requests` | ativo | ativo | http → https |

**A descoberta que muda a conversa:** o site **já tem um formulário funcionando e já tem
um fornecedor liberado na CSP.** Não estamos partindo do zero.

### 1.2 O contato hoje

Existe **um** formulário no projeto (grep por `<form` retorna só ele): `index.html`
linhas 1195–1222, `id="contatoForm"`, seção `#contato`.

- Backend: **FormSubmit**, via token de "Invisible email".
  `script.js:3728` → `const FORMSUBMIT_TOKEN = '6c5430f84d0c32ffe3e7e326393fcb61';`
  O endereço de destino não existe em nenhum lugar do front-end — só o FormSubmit sabe.
- Campos: nome, email, assunto, mensagem. Mais os de controle: `_subject`, `_captcha=true`,
  `_template=table` e o honeypot `_honey` (input escondido por CSS inline).
- Envio: `fetch` para `https://formsubmit.co/ajax/{token}` (`script.js:3741–3786`), com
  `AbortController` de 15 s, estados anunciados em `aria-live`, e o `action` nativo
  preenchido em runtime como fallback (`script.js:3738`).
- Não há upload de arquivo. Não há lógica condicional. Não há mais nada.

**E-mail:** nunca aparece no HTML. É montado por JS só depois de um clique real —
`.email-revelar` no `#contato` e `.email-abrir` no footer (`script.js:3715–3722`),
via `data-user` + `data-dominio`. Anti-raspador deliberado.

**WhatsApp:** não existe no site. Nenhum `wa.me`.

**`servicos.html`:** **não tem CTA de conversão própria.** Os 7 blocos de serviço
terminam num link para o portfólio filtrado (`index.html?filtro=video#trabalhos` etc.),
e o CTA do rodapé da página manda para `index.html#contato` — o mesmo formulário
genérico de 4 campos, para os 7 serviços. É exatamente o buraco que esta pesquisa
existe para tapar.

### 1.3 O que o deploy publica, e o que precisa mudar

`.github/workflows/deploy-pages.yml` tem **duas listas** que precisam ser tocadas, e
esquecer uma delas produz sintomas diferentes:

**(a) `on.push.paths` (linhas 10–20)** — o gatilho. Hoje: `assets/**`, `index.html`,
`servicos.html`, `style.css`, `script.js`, `servicos.js`, `sitemap.xml`, `robots.txt`,
`.nojekyll`, o próprio workflow.
→ Um arquivo novo fora dessa lista: o push **não dispara deploy nenhum**. Sintoma:
commit feito, Actions em silêncio, site velho no ar. Parece cache; não é.

**(b) o `cp` do job de build (linhas 49–51)** — a lista de inclusão do artefato:

```
cp -r assets _site/
cp index.html servicos.html style.css script.js servicos.js sitemap.xml robots.txt .nojekyll _site/
```

→ Um arquivo novo fora desse `cp`: **o deploy roda verde e o arquivo simplesmente não
existe no ar** — 404. Pior sintoma dos dois, porque não há erro em lugar nenhum.
→ Um arquivo **da lista que desaparecer**: o `cp` falha e o deploy morre ali. É de
propósito (comentário nas linhas 44–47).

**Portanto, para publicar páginas novas de formulário** (digamos `briefing-pos-producao.html`
e um `briefing.js` e `briefing.css`), o mínimo é:

1. Acrescentar cada arquivo novo ao `on.push.paths`.
2. Acrescentar cada arquivo novo ao `cp` da linha 51.
3. Acrescentar as URLs novas ao `sitemap.xml` (não obrigatório para funcionar, mas o
   sitemap hoje só lista 2 URLs e ficaria mentindo).

Se em vez de 7 páginas o caminho for **um link para fora** (fornecedor hospedado), a
resposta é: **nenhuma das duas listas muda, e não há arquivo novo.** É a diferença
central entre as opções da seção 3.

### 1.4 O teto de 10 minutos

Confirmado tanto no comentário do workflow (linhas 3–5, 82–90) quanto na documentação
do GitHub: *"GitHub Pages deployments will timeout if they take longer than 10 minutes."*
O input `timeout` da `actions/deploy-pages` é cortado pelo `MAX_TIMEOUT` de 600000 ms da
própria action — os "30 min" que já estiveram escritos ali nunca existiram. Runs
históricos: 10m22s e 10m54s passaram raspando; 11m17s e 10m40s falharam.

**Implicação direta para esta decisão:** o custo de deploy é proporcional ao **peso do
artefato**, não ao número de arquivos HTML. 7 páginas HTML de texto são alguns dezenas de
KB — irrelevante. O que mataria o deploy seria pôr **assets pesados** (vídeo, imagem
grande) no `_site` por causa dos formulários. Ninguém precisa fazer isso.

---

## 2. Opções avaliadas

Legenda de "Mexe na CSP?": o que precisa ser **acrescentado** ao `<meta>` das páginas.

| Serviço | Como integra | Plano free (limites) | 1º plano pago | Upload de arquivo | Lógica condicional | Mexe na CSP? |
|---|---|---|---|---|---|---|
| **Tally** (embed) | `<iframe src="https://tally.so/embed/{id}">` + `https://tally.so/widgets/embed.js` | **formulários e respostas ilimitados** (uso justo: 50.000 resp./mês, 100 GB upload/mês, 500 GB total) | Pro **US$ 29/mês** mensal, **US$ 24/mês** anual | **sim, no free** — 10 MB/arquivo; nº de arquivos e armazenamento ilimitados; Pro remove o limite de 10 MB | **sim, no free**, sem limite de condições | **`frame-src https://tally.so`** (+ `script-src https://tally.so` só se quiser altura dinâmica) |
| **Tally** (link para fora) | `<a href="https://tally.so/r/{id}">` | idem | idem | idem | idem | **nada.** `navigate-to` foi removido da spec de CSP em set/2022 e nunca foi implementado — navegar para fora não é governado por CSP |
| **Fillout** | `<iframe src="https://forms.fillout.com/t/{id}">` + script `https://server.fillout.com/embed/v1/` | 1.000 respostas/mês | Starter **US$ 15/mês** (anual US$ 180) | sim, 20 MB (Free/Starter/Pro); "1 GB+" no Business | sim, no free | **`frame-src https://forms.fillout.com`** + **`script-src https://server.fillout.com`** (2 domínios) |
| **FormSubmit** *(já em uso)* | POST/`fetch` para `https://formsubmit.co/ajax/{token}` | submissões ilimitadas, formulários ilimitados; arquivos não retidos após 30 dias | não documentado (existe link "/services", sem preço publicado) | sim — exige `enctype="multipart/form-data"`, **10 MB para a soma de todos os arquivos** | **não tem** | **nada** — `connect-src` e `form-action` já liberam `formsubmit.co` no `index.html`. Em página nova, replicar as duas diretivas |
| **Google Forms** | `<iframe src="https://docs.google.com/forms/...">` | grátis, respostas ilimitadas | — | sim, **mas todo respondente é obrigado a fazer login numa conta Google, sem exceção nem contorno** | sim (pular para seção) | `frame-src https://docs.google.com` |
| **Web3Forms** | POST para `https://api.web3forms.com/submit` | 250 submissões/mês | não confirmado | **não no free** — upload é dos planos pagos | não confirmado | `connect-src https://api.web3forms.com` |
| **Formspree** | POST/`fetch` para `https://formspree.io/f/{id}` | 50 submissões/mês, arquivo de 30 dias | Personal **US$ 15/mês** (200 subm./mês, 1 GB de upload) — números de fonte secundária, a página oficial de preço é renderizada por JS e **não consegui confirmar na origem** | pago | não confirmado | `connect-src https://formspree.io` + `form-action` |
| **Typeform** | iframe | **10 respostas/mês** (caiu de 100 em fev/2026) | Basic US$ 25/mês (100 resp./mês) | — | sim | — |
| **Jotform** | iframe | 5 formulários, 100 submissões/mês, 100 MB de espaço, 500 submissões armazenadas no total | Bronze US$ 34/mês (anual) | sim | sim | — |
| **Cognito Forms** | iframe | 100 entradas/mês, 100 MB (fonte secundária) | Pro US$ 19/mês | sim | sim, no free | — |
| **Netlify Forms** | atributo `netlify` no HTML, detectado no build da Netlify | — | — | — | — | **inviável: exige que o site seja hospedado na Netlify.** O detector roda no build da Netlify; no GitHub Pages não existe |
| **Basin / Formcarry** | POST | não confirmado | não confirmado | não confirmado | não confirmado | `connect-src` do domínio |

### 2.1 O que sai da lista, e por quê

- **Typeform**: 10 respostas/mês no free. Sete briefings B2B estouram isso num mês bom.
  O plano que resolve custa mais que o Tally Pro e entrega menos.
- **Jotform**: 5 formulários no free e **precisamos de 7**. Já nasce pago.
- **Netlify Forms**: dependeria de trocar de hospedagem. Fora de escopo.
- **Web3Forms**: sem upload no free, e upload é requisito em 2 dos 7 serviços.
- **Google Forms**: o login obrigatório do Google no upload é fatal. Um diretor de marketing
  de agência que recebe o link no WhatsApp corporativo bate numa tela de login antes de ver
  o formulário. É a pior taxa de conclusão possível justamente no briefing mais valioso.
- **FormSubmit**: **não tem lógica condicional.** Ele é um encanamento de e-mail, não um
  construtor de formulário. Continua ótimo para o que faz hoje.

### 2.2 O ponto de CSP que quase todo mundo erra

Isto é o que decide a comparação, e vale escrever com precisão porque é
contraintuitivo e este projeto já se queimou com CSP antes:

**A CSP da página pai NÃO se aplica ao documento dentro de um iframe cross-origin.**
Confirmado na MDN: `frame-src` *"specifies valid sources for nested browsing contexts"* —
ela governa **se o iframe pode carregar**, e nada além disso. O documento dentro do
iframe é outro browsing context, com a CSP dele.

Consequência prática, para o caminho de embed:

- O upload do arquivo acontece **de dentro** do iframe → **não precisa de `connect-src`.**
- As fontes, o CSS e as imagens do formulário são carregados **de dentro** do iframe →
  **não precisa de `font-src`, `style-src` nem `img-src`.**
- O captcha do fornecedor roda **de dentro** do iframe → **não precisa liberar
  `challenges.cloudflare.com` nem `google.com/recaptcha`.**
- O `<form>` do fornecedor submete **de dentro** do iframe → **não precisa de `form-action`.**

Ou seja: embutir Tally por iframe custa **uma diretiva, um domínio**. Já um formulário
**nativo** na sua página que faz `fetch` para o fornecedor custa `connect-src` +
`form-action` + (se tiver captcha de terceiro) `script-src` + `frame-src` + `connect-src`
do captcha. **O iframe é o caminho de menor superfície de CSP, não o maior.** Contraria a
intuição, mas é assim que a spec funciona.

O único motivo para acrescentar `script-src https://tally.so` é o `embed.js`, e ele serve
para **uma coisa só**: redimensionar o iframe conforme a altura do conteúdo
(`dynamicHeight=1`), via `postMessage`. Sem ele o formulário funciona igual — só ganha
barra de rolagem interna. **Dá para começar sem o script**, com `height` fixo generoso,
e manter `script-src 'self'` intacto. Recomendo começar assim.

---

## 3. Recomendação

### Escolha principal: **Tally, embutido por iframe, uma página por serviço**

Sete páginas próprias no site (`briefing-pos-producao.html`, …), cada uma com o header e
o rodapé do site, o texto de abertura dela, e o formulário Tally correspondente dentro de
um iframe. A pessoa nunca sai de `savylla.github.io`.

**Por que Tally e não os outros:**

1. **É o único que entrega os três requisitos no plano gratuito**: 7 formulários (ilimitados),
   lógica condicional sem limite de condições, e upload de arquivo. Fillout cobra
   US$ 15/mês para tirar a marca; Jotform já barra em 5 formulários; Typeform em 10 respostas.
2. **Custa uma diretiva de CSP.** `frame-src https://tally.so`. Um domínio, um lugar.
3. **Webhook está no plano gratuito** — e webhook é o que faz a resposta chegar no ClickUp
   (seção 4). Nos concorrentes isso costuma ser feature paga.
4. **Campos ocultos por query string, no free** (`https://tally.so/r/nPA50m?name=Marie&ref=email`).
   Serve para marcar de qual página/serviço veio o preenchimento sem criar campo visível.
5. **Redirect on completion é gratuito** — no fim do briefing a pessoa volta para uma
   página de obrigado no próprio site.
6. **Formulário em múltiplas páginas e campos calculados estão no gratuito** — que é
   exatamente o que um briefing longo precisa para não parecer um paredão de 30 campos.
7. **Dados hospedados na União Europeia**, empresa europeia sujeita ao GDPR. Para LGPD
   (seção 6) é o cenário mais fácil de justificar entre os fornecedores avaliados.

**O que Tally não tem:** integração nativa com ClickUp. A lista oficial de integrações é
Notion, Slack, Airtable, Google Sheets, Zapier, Make, Coda, **Webhooks**, n8n, Linear,
Discord, Integrately, Pipedream, IFTTT e um servidor MCP. O caminho até o ClickUp passa
por webhook ou por script — é o assunto da seção 4, e não é problema, porque ela já tem
a infraestrutura Python para isso.

**O que se perde no plano gratuito** — três coisas, em ordem de importância real:

1. **Respostas parciais são pagas (Pro).** Quem começa um briefing longo e abandona no meio
   não deixa as **respostas** dele no plano gratuito. Ressalva da própria documentação:
   mesmo no Pro, elas **não disparam integração nem notificação por e-mail** e só saem em
   CSV manual — servem para diagnóstico, não para o fluxo do ClickUp.
   *Nuance que suaviza isso:* a API expõe `GET /forms/{formId}/analytics/drop-off`, que dá
   **em qual pergunta as pessoas desistem** sem ser um endpoint marcado como Pro. Ou seja,
   o *diagnóstico* de abandono provavelmente sai de graça pela API; o que o Pro compra é o
   **conteúdo** do que a pessoa chegou a escrever antes de sair. **Não consegui confirmar**
   se o endpoint de analytics responde em conta gratuita — vale testar antes de assinar.
2. **O selo "Made with Tally"** fica visível.
3. **Domínio próprio** (`forms.savylla.com.br`) é Pro — irrelevante no caminho de embed,
   porque a URL que a pessoa vê é a do site.

Remover os três custa **Pro: US$ 29/mês mensal ou US$ 24/mês no anual** — o mesmo plano que
tira o limite de 10 MB por arquivo. Minha leitura: **comece no gratuito.** O selo não custa
cliente. Assine o Pro quando um dos dois gatilhos acontecer: o limite de 10 MB atrapalhar
de verdade no manual de marca, ou ela querer saber **onde** as pessoas abandonam o briefing.
Aí os US$ 24 se pagam em decisão, não em cosmética.

**O que exatamente muda neste repositório:**

*(a) A CSP das páginas novas* — as 7 páginas de briefing começam com a CSP do
`servicos.html` e trocam **uma** diretiva:

```
frame-src 'none'    →    frame-src https://tally.so
```

Ficando (linha completa, pronta para colar no `<meta>` das páginas de briefing):

```
default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; media-src 'none'; font-src 'self'; connect-src 'self'; frame-src https://tally.so; form-action 'none'; base-uri 'self'; object-src 'none'; upgrade-insecure-requests
```

Repare no que **não** mudou: `script-src` segue `'self'`, `connect-src` segue `'self'`,
`form-action` segue `'none'`. Se depois quiser a altura dinâmica, e **só** nesse caso,
`script-src` passa a `'self' https://tally.so`.

*(b) O `servicos.html` e o `index.html`* — se os CTAs forem apenas links para as páginas
novas (`<a href="briefing-pos-producao.html">`), **a CSP dessas duas páginas não muda em
nada.** Link interno não envolve CSP. É o caminho que eu seguiria.

*(c) O workflow, nos dois lugares* — `on.push.paths` ganha as entradas novas, e o `cp` da
linha 51 ganha os mesmos arquivos:

```yaml
      - 'briefing-*.html'
      - 'politica-privacidade.html'
      - 'obrigado.html'
```

```
cp index.html servicos.html politica-privacidade.html obrigado.html briefing-conteudo-redes-sociais.html briefing-direcao-de-creators.html briefing-filmmaker.html briefing-pos-producao.html briefing-fotografia.html briefing-direcao-de-arte.html briefing-producao-com-ia.html style.css script.js servicos.js sitemap.xml robots.txt .nojekyll _site/
```

> Repare que no `cp` os 7 nomes estão **escritos por extenso**, e no `on.push.paths` usei
> glob. É de propósito, e a assimetria importa:
> - No **`on.push.paths`** o glob é seguro e desejável — ele só decide se o workflow dispara.
> - No **`cp`** o glob **destrói a garantia de fail-fast** que o comentário das linhas 44–47
>   promete de propósito. Com `cp briefing-*.html`, se um arquivo for renomeado ou apagado
>   por engano, o glob simplesmente casa com menos arquivos e o `cp` **retorna zero** — o
>   deploy sobe verde, com uma página a menos no ar, e ninguém é avisado. Com os nomes
>   literais, o `cp` falha e o deploy para ali, que é exatamente o comportamento que o
>   workflow escolheu ter. **Não troque os nomes literais por glob no `cp`.**

*(d) Arquivos novos no repo:*
- `briefing-conteudo-redes-sociais.html`, `briefing-direcao-de-creators.html`,
  `briefing-filmmaker.html`, `briefing-pos-producao.html`, `briefing-fotografia.html`,
  `briefing-direcao-de-arte.html`, `briefing-producao-com-ia.html`
- `politica-privacidade.html` (seção 6 explica por que ela é obrigatória)
- `obrigado.html` (destino do *redirect on completion*)
- CSS: **nada novo** — dá para reusar as classes de `style.css`. O iframe precisa de
  meia dúzia de linhas, que cabem no arquivo existente.
- JS: **nada novo obrigatório.** Se as páginas reusarem o header/overlay, elas carregam
  o `servicos.js` que já existe — ele só depende de `#header`, `#sideMenu`, `#navOverlay`,
  `#burgerBtn` e `[data-revelar]`. Replicar essa marcação é mais barato que escrever JS novo.
- `sitemap.xml`: +9 URLs.
- `servicos.html`: 7 CTAs novos, um por bloco de serviço. **Atenção:** o JSON-LD dessa
  página (linhas 52–69) é uma cópia paralela da copy — mexer no texto visível não atualiza
  ele, e ele engana o grep de verificação.

### Plano B: **Tally hospedado, link para fora** (`tally.so/r/{id}`)

Mesmo Tally, mesmos formulários, mesma conta, mesmo custo zero. A diferença é que o CTA
é `<a href="https://tally.so/r/xxxxx" target="_blank" rel="noopener">` em vez de uma
página com iframe.

**O que se ganha:** literalmente **zero** mexida em CSP (confirmado: `navigate-to` foi
removido da spec em set/2022 e nunca foi implementado em navegador nenhum), **zero**
arquivo novo, **zero** linha no workflow, **zero** risco de o deploy quebrar. É trocar 7
`<a href>` no `servicos.html`. Dá para estar no ar hoje.

**O que se perde, honestamente:**
- **A marca.** O formulário é uma página branca da Tally com o logo dela, não o
  `#0b1120` do site com a Instrument Serif. Num portfólio de audiovisual — onde o
  produto *é* acabamento visual — isso não é detalhe cosmético, é incoerência do
  próprio pitch. Dá para amenizar (a Tally deixa customizar cor e capa) mas não resolver.
- **A sensação de continuidade.** A URL muda de domínio no meio da conversão. Uma
  parcela das pessoas hesita ali.
- **O tracking.** Ver quantos abriram e quantos terminaram exige olhar dois painéis.
- **O SEO.** As 7 páginas de briefing seriam 7 páginas indexáveis do site, cada uma
  ranqueando para "briefing de pós-produção" e afins. O link para fora joga isso no lixo.

**Quando o plano B é a resposta certa:** se ela quiser validar **se as pessoas preenchem**
antes de investir em 7 páginas. É um bom teste de 2 semanas. E a migração depois é
indolor: os mesmos formulários Tally passam de link para iframe, sem refazer nada.

**Terceira via, para registro:** formulários **nativos** em HTML/JS com lógica condicional
escrita à mão, postando no FormSubmit que já está liberado na CSP. Custo zero, marca 100%
sob controle, nenhum domínio novo. Descartei porque: o upload do FormSubmit é **10 MB para
a soma de todos os arquivos** (não serve nem para um manual de marca decente), não há painel
de respostas, não há retomada de preenchimento, e manter a lógica condicional de 7
formulários longos à mão em JS é dívida técnica garantida — 7 formulários com ramificação
é exatamente o problema que um construtor de formulário resolve. Não vale o orgulho.

---

## 4. Onde cai a resposta

### 4.1 O obstáculo que elimina metade das opções

**Webhook exige um receptor HTTPS público. Ela não tem, e no GitHub Pages não pode ter.**

Isso é decisivo, porque "use o webhook" é a resposta padrão para "manda para o ClickUp" — e
aqui ela não funciona sozinha. Um webhook precisa de alguém escutando numa URL pública.
Site estático não escuta nada. Então o webhook obriga a contratar um intermediário na
nuvem (Zapier, Make, n8n Cloud, Pipedream) só para ter um endereço que recebe o POST.

**E é justamente aí que o caminho barato aparece: não use webhook. Use polling.**

A Tally tem **API REST pública de leitura**, e é isso que muda tudo:

```
GET https://api.tally.so/forms/{formId}/submissions
Authorization: Bearer <token>
```

Autenticação por Bearer token, **100 requisições por minuto**, com paginação. Há também
`GET /forms/{formId}/questions` (para mapear os campos), `GET /forms` e o bloco de
analytics — inclusive **`GET /forms/{formId}/analytics/drop-off`**, abandono por questão.
No índice oficial da API, a marca *"Requires a Pro subscription"* aparece **só** em
criar/atualizar/deletar workspace e gerenciar pastas — **não nos endpoints de submissions**.

Do outro lado, o ClickUp:

```
POST https://api.clickup.com/api/v2/list/{list_id}/task
Authorization: pk_...            (personal token; OAuth 2.0 também é suportado)
```

**Só o campo `name` é obrigatório.** Rate limit: **100 requisições por minuto por token no
Free Forever, Unlimited e Business** (1.000 no Business Plus, 10.000 no Enterprise);
excedente devolve HTTP 429 com os headers `X-RateLimit-Limit`, `-Remaining` e `-Reset`.

E para anexo (o manual de marca da Direção de Arte):

```
POST https://api.clickup.com/api/v2/task/{task_id}/attachment
Content-Type: multipart/form-data
```
A documentação recomenda migrar para a **V3 Attachments API**, que cobre tarefas e campos
personalizados do tipo File. **Não há limite de tamanho documentado** nessa página —
não confirmado.

### 4.2 O caminho recomendado

**Duas camadas, e a segunda é opcional até ela querer.**

**Camada 1 — a caixa de entrada, no dia zero: notificação por e-mail da Tally.**
Está no plano gratuito, chega na hora, não depende de script nenhum rodar, e não quebra se
ela estiver viajando. **Isto é o que garante que nenhum briefing se perde.** Ligue e esqueça.

Ao lado, ligue também a **integração nativa com Google Sheets** (gratuita) — uma planilha
por serviço, ou uma só com a coluna do serviço. Ela serve como registro durável e legível
sem depender da API. Custo: zero.

**Camada 2 — a tarefa no ClickUp: um script Python dela.**

Um script novo na raiz, no mesmo molde dos 43 que já existem:

1. `GET /forms/{formId}/submissions` para cada um dos 7 formulários, filtrando pelo que
   ainda não foi processado.
2. Monta o `name` da tarefa (`[Pós-produção] Nestlé — Fulano`) e a descrição com as
   respostas.
3. `POST /api/v2/list/{list_id}/task` na lista de briefings.
4. Se houver arquivo, `POST /api/v2/task/{task_id}/attachment`.
5. Grava o ID processado num JSON de estado.

**O passo 5 é o que importa, e ela já sabe disso melhor que ninguém.** O projeto tem
`upload_progress.json`, `youtube_results.json`, `audit_progress.json` — o padrão de
"controle de estado em JSON para não reprocessar" já é a arquitetura da casa. E a memória
do projeto registra que **três bugs de controle de estado no uploader do YouTube já
sumiram e duplicaram vídeos**. Aqui o sintoma equivalente é tarefa duplicada no ClickUp.
**Escreva o passo 5 primeiro, com o ID da submissão como chave de idempotência.**

**Custo total desse caminho: R$ 0,00.** Nenhuma assinatura, nenhum intermediário, nenhum
plano pago dos dois lados. Os dois rate limits (100/min em cada API) são folgadíssimos para
o volume de briefings de uma pessoa.

**Por que isto e não Zapier/Make/n8n:** porque o intermediário existe para resolver o
problema de "não tenho onde receber o webhook" — e o polling não tem esse problema. Ela
trocaria zero por uma assinatura mensal, um painel a mais para manter, **e uma terceira
transferência internacional para declarar na política de privacidade** (seção 6.4). Não
compensa. Se um dia ela quiser reação em tempo real em vez de um `cron` de 15 minutos, aí a
conversa muda — mas briefing de projeto não é evento de tempo real.

> O argumento acima é **arquitetural, não de preço**: ele vale mesmo que os planos
> gratuitos de Zapier, Make e n8n cobrissem o volume dela — porque o custo que importa é
> a peça a mais no caminho, não a mensalidade. **Os preços e limites atuais desses três
> não estão confirmados** nesta pesquisa (o orçamento de buscas da sessão acabou antes).
> Se alguém quiser reabrir a decisão, o dado que falta é esse; a conclusão não depende dele.

**Por que não o Form view nativo do ClickUp** (que resolveria a integração por definição):
duas objeções. A primeira é de CSP — embutir o formulário do ClickUp exigiria liberar o
domínio de compartilhamento dele em `frame-src`, e **não consegui confirmar qual é** (a
central de ajuda do ClickUp devolveu HTTP 403 nas tentativas). Não vou recomendar liberar um
domínio que não confirmei. A segunda é de produto: o formulário do ClickUp é uma ferramenta
interna de intake, não uma peça de conversão — e para um portfólio cujo produto é
acabamento visual, isso pesa.

### 4.3 A ordem de implantação que eu seguiria

| Etapa | O que faz | Custo | Quando |
|---|---|---|---|
| 1 | Formulários na Tally + notificação por e-mail ligada | R$ 0 | dia 1 — já é utilizável |
| 2 | Google Sheets ligado como registro | R$ 0 | dia 1, dois cliques |
| 3 | CTAs no `servicos.html` apontando para os formulários | R$ 0 | dia 1 |
| 4 | `politica-privacidade.html` publicada | R$ 0 | **antes** de divulgar (seção 6) |
| 5 | Script Python de sincronia com o ClickUp | R$ 0 | quando o volume incomodar |

A etapa 5 é a última de propósito. **Automatizar a criação de tarefa antes de saber quantos
briefings chegam por mês é otimizar o que ainda não existe.** Com 3 briefings/mês, copiar
e colar do e-mail para o ClickUp leva dois minutos e não erra. O script se paga quando o
volume passa disso — e a essa altura ela já vai saber quais campos realmente importam na
descrição da tarefa, o que torna o script melhor.

---

## 5. Upload de material bruto

**Recomendação: não peça upload direto. Peça link.** Para os dois serviços, com uma
exceção pequena.

### Pós-produção — material bruto, dezenas de GB

Upload direto está **fora de questão**, e não por preguiça — pelos números:

- **Tally free: 10 MB por arquivo.** Fim da conversa.
- **Tally Pro (US$ 29/mês): sem limite de tamanho por arquivo**, mas a política de uso
  justo trata **100 GB/mês de upload ou 500 GB de armazenamento total** como volume alto
  que dispara "contato para um plano sob medida". Dois projetos de pós por mês encostam
  nisso. Você estaria construindo em cima de um limite que vai ser renegociado.
- **Nenhum concorrente resolve**: Fillout 20 MB (1 GB+ só no Business, US$ 75/mês),
  Formspree 1 GB no plano de US$ 15, FormSubmit 10 MB no total.
- E há o problema mais bobo e mais real: **um upload de 40 GB por formulário web numa aba
  de navegador**. Uma queda de Wi-Fi, um notebook que dorme, e a pessoa recomeça. Nenhum
  desses fornecedores faz upload retomável de arquivo grande — não é o negócio deles.

**O que fazer:** campo de texto obrigatório, `type="url"`, rotulado sem ambiguidade —
*"Link do material bruto (Drive, WeTransfer, Frame.io, MASV)"* — e um campo de senha/código
de acesso ao lado, porque metade dos links vem protegido.

Isso não é uma concessão: **é o fluxo que o mercado de audiovisual já usa.** Ninguém
manda 40 GB de bruto por formulário. Manda link. Pedir de outro jeito sinalizaria
desconhecimento do ofício — o oposto do que a página de serviços está tentando comunicar.

Os números que sustentam a escolha, para ela poder orientar o cliente:

| Via | Limite / custo | Serve para bruto? |
|---|---|---|
| **Google Drive** | quota da conta do cliente | sim, e é o que a maioria já tem |
| **WeTransfer free** | **3 GB por transferência**, e até 10 transferências **ou** 3 GB no total numa janela móvel de 30 dias | só para material leve |
| **MASV** | **15 GB/mês grátis**, depois **US$ 0,25/GB** pago pelo remetente | sim — é a ferramenta do ramo |
| **Frame.io** | assinatura por membro (Team a partir de **US$ 25/membro/mês**), armazenamento por faixa, não por GB | sim, e já é usado no fluxo dela (existe receita de baixar bruto do frame.io no projeto) |

Uma nota que economiza dor de cabeça: **quem paga o MASV é quem recebe**, não quem envia.
Se ela quiser oferecer "manda por aqui" como conveniência, o custo é dela, a US$ 0,25/GB —
40 GB = US$ 10 por projeto. É defensável embutir isso no orçamento, mas é decisão de preço,
não técnica.

### Direção de Arte — manual de marca

Aqui **o upload direto vale a pena**, com uma ressalva. Um manual de marca é um PDF: os
enxutos ficam em 2–8 MB, mas um manual de agência com mockups fotográficos passa fácil de
10 MB, que é exatamente o teto do Tally free.

**Recomendação:** ofereça **os dois caminhos no mesmo formulário** — campo de upload
(*"até 10 MB"*, explícito) **e** campo de link, com a instrução de usar o link se o arquivo
for maior. Custa um campo a mais e elimina o beco sem saída em que a pessoa tenta enviar,
falha, e desiste no meio do briefing. É a diferença entre um formulário que funciona e um
que funciona só para quem tem sorte.

Se o limite de 10 MB começar a atrapalhar de verdade, **é aí que o Tally Pro se paga** —
ele existe para isso, não para tirar o selo.

---

## 6. LGPD e anti-spam

> Aviso: isto é pesquisa da letra da lei e dos regulamentos da ANPD, com os artigos
> transcritos. Não é parecer jurídico. Nos pontos em que a exigência formal é
> inatingível para uma profissional autônoma, digo isso em vez de fingir que dá.

### 6.1 Base legal: **legítimo interesse**, não consentimento

A intuição manda pôr um "aceito os termos" e dormir tranquila. É a escolha errada.

- **Consentimento (art. 7º, I)** joga o **ônus da prova** em você (art. 8º, §2º: *"Cabe ao
  controlador o ônus da prova de que o consentimento foi obtido em conformidade"*) e é
  **revogável a qualquer momento** (art. 8º, §5º) — se a pessoa revoga, você perde
  tecnicamente o direito de responder ao contato que **ela** iniciou. Absurdo prático.
- **Execução de contrato (art. 7º, V)** exige contrato *"do qual seja parte o titular"*.
  Quem preenche é o analista de marketing; o contrato é com a empresa dele. Funciona
  quando o contato é o próprio contratante; **fica frágil no B2B**, que é o caso aqui.
- **Legítimo interesse (art. 7º, IX)** é o que se sustenta em qualquer configuração. A
  finalidade cabe literalmente no **art. 10, I** (*"apoio e promoção de atividades do
  controlador"*), e o critério central da ANPD — **legítima expectativa** — é o mais fácil
  de defender que existe: **a pessoa preencheu o formulário pedindo para ser contatada.**

O que vem junto do legítimo interesse:
- **art. 10, §1º** — só o "estritamente necessário". Nome, e-mail, telefone, empresa e
  descrição do projeto passam. **CPF, CNPJ, endereço e data de nascimento não** — corte.
- **art. 10, §2º** — *"deverá adotar medidas para garantir a transparência"*. **É este
  dispositivo que obriga o aviso, e não um checkbox.**
- **art. 10, §3º** — a ANPD *pode* pedir relatório de impacto. Não é entregável prévio,
  é risco futuro. Por isso o item 7 da lista prática.
- **art. 7º, §6º** — dispensar o consentimento *"não desobriga (...) das demais
  obrigações"*. Sem caixa, mas **com** aviso.

**Regra de ouro:** responder ao contato → art. 7º, IX, **sem checkbox**. Mandar newsletter
depois → art. 7º, I, **checkbox separado e desmarcado**. Bases diferentes para finalidades
diferentes, no mesmo formulário.

### 6.2 O aviso de privacidade — art. 9º, item por item

O caput exige informação *"clara, adequada e **ostensiva**"*:

| Inciso | Exige | No caso dela |
|---|---|---|
| I | finalidade específica | "responder ao contato, orçar e negociar o projeto". Não vale "melhorar nossos serviços" |
| II | forma e **duração** | **é este inciso que obriga declarar o prazo de retenção** |
| III | identificação do controlador | nome civil completo + CNPJ se MEI/ME. "Savylla" sozinho não identifica |
| IV | contato do controlador | e-mail que funciona de verdade |
| V | uso compartilhado e finalidade | **nomear os terceiros**: o fornecedor do formulário, o provedor de e-mail, o captcha se houver |
| VI | responsabilidades dos agentes | ela = controladora; o fornecedor = operador, sob instrução dela |
| VII | direitos do art. 18, com **menção explícita** | "menção explícita" é literal: **listar os nove incisos**, não escrever "você tem os direitos da LGPD" |

### 6.3 Consentimento: quando sim, quando não

**Checkbox pré-marcado não vale.** Não há artigo com essas palavras, mas três convergem:
art. 8º caput (exige *"manifestação de vontade"* — caixa já marcada é inércia), art. 9º, §1º
(nulo se não apresentado *"de forma clara e **inequívoca**"*) e art. 8º, §3º (vedado
tratamento *"mediante vício de consentimento"*).

**Checkbox único juntando tudo também não vale.** O art. 8º, §4º é a norma decisiva:
*"O consentimento deverá referir-se a finalidades determinadas, e as **autorizações
genéricas** para o tratamento de dados pessoais **serão nulas**."* Aquele
"concordo com a política e aceito receber comunicações" é autorização genérica → nulo.
**Uma caixa por finalidade.**

### 6.4 A parte incômoda: transferência internacional

**Sim, usar Tally é transferência internacional** — e a Resolução CD/ANPD nº 19/2024
(DOU 23/08/2024) fecha qualquer escapatória: art. 3º, III define transferência como
*"transmite, compartilha ou **disponibiliza acesso**"*, e o art. 7º, parágrafo único diz que
a lei se aplica *"**independe do meio utilizado** (...), do país de sede dos agentes de
tratamento ou do país onde estejam localizados os dados"*.

O art. 9º do Regulamento exige **duas coisas cumulativas**: uma hipótese legal do art. 7º
**e** um mecanismo de transferência válido, que só pode ser (a) país com decisão de
adequação da ANPD, (b) cláusulas-padrão contratuais, ou (c) as hipóteses do art. 33 da
LGPD — **inclusive o inciso VIII, o consentimento específico e em destaque.**

**E aqui está o problema concreto, dito sem rodeio:**

- **Via (a) está vazia:** não há decisão de adequação publicada pela ANPD para nenhum país.
- **Via (b) está fechada na prática.** O art. 16 exige adoção *"**integral e sem alteração**"*
  do texto do Anexo II — que é um contrato bilateral **assinado por exportador e
  importador**. A Tally não vai assinar cláusulas da ANPD com uma autônoma brasileira. O
  DPA da Tally traz SCCs **só europeias** (*Decision (EU) 2021/914*), **sem uma linha sobre
  LGPD ou ANPD**. E o prazo de 12 meses para incorporar as cláusulas **venceu em
  23/08/2025** — já passou.
- **Via (c) é a única executável por uma pessoa só:** art. 33, VIII — *"consentimento
  específico e em destaque para a transferência, com informação prévia sobre o caráter
  internacional da operação, **distinguindo claramente esta de outras finalidades**"*.

**Não existe regime simplificado de pequeno porte para isto.** A Res. 19/2024 não menciona
pequeno porte em nenhum artigo. A Res. 2/2022 flexibiliza registro, encarregado e prazos —
**não toca em transferência internacional.**

**O que reduz o risco de fato:** a Tally é belga, com dados na União Europeia. O "país de
destino" que ela vai declarar é um país com regime equivalente. Isso não substitui o
mecanismo do art. 33, mas melhora muito a dosimetria (art. 52, §1º) se alguém reclamar. **É
mais um argumento técnico a favor da Tally sobre os fornecedores americanos** (Formspree,
Fillout, Web3Forms, FormSubmit — todos EUA), e não é um argumento pequeno.

O art. 17, §2º do Regulamento ainda exige **publicar no site**, em português e linguagem
simples, um documento sobre a transferência com seis itens — incluindo o **país de destino**
e o **direito de peticionar contra ela perante a ANPD**. O §3º autoriza expressamente que
isso viva **dentro da política de privacidade, em seção destacada.** É exatamente o que a
`politica-privacidade.html` vai fazer.

### 6.5 Encarregado (DPO): **ela não precisa nomear**

A Resolução CD/ANPD nº 2/2022 resolve isso, e é a melhor notícia desta seção:

- **art. 2º, I** inclui explicitamente *"**pessoas naturais** e entes privados
  despersonalizados"* na definição de agente de pequeno porte → profissional autônoma
  pessoa física está dentro.
- **art. 11** — *"Os agentes de tratamento de pequeno porte **não são obrigados a indicar o
  encarregado**"*.
- **art. 11, §1º** — mas **deve** *"disponibilizar um canal de comunicação com o titular"*.
  **O e-mail no site substitui o DPO, e isso é obrigatório, não opcional.**
- **art. 14, I** — prazo **em dobro** para atender pedidos de titulares.
- **art. 9º** — registro de operações do art. 37 pode ser **simplificado**.
- **art. 3º/4º** — ela perde o regime se fizer tratamento de alto risco. Um formulário de
  briefing B2B com 5 campos **não é**: o art. 4º exige cumulativamente critério geral
  (larga escala ou afetação significativa) **e** específico (tecnologia emergente,
  vigilância de zona pública, decisão automatizada, dado sensível/de criança/idoso).
  Nenhum se aplica. **Folga confortável.**
- **art. 6º** — a flexibilização *"não isenta (...) inclusive das bases legais e dos
  princípios"*. O aviso e a base legal continuam integralmente exigíveis.

### 6.6 Retenção

**Precisa declarar o prazo** (art. 9º, II) e **precisa eliminar** (arts. 15 e 16 — *"os
dados pessoais serão eliminados após o término de seu tratamento"*, com ressalva para
obrigação legal e para uso próprio **anonimizado**).

Detalhe fino que evita prometer o que não se pode cumprir: o direito de **eliminação** do
art. 18, VI é dos dados tratados **com consentimento**. Com base em legítimo interesse, o
que o titular exerce é **oposição** (art. 18, §2º) — que na prática dá no mesmo. Então não
escreva "deleto quando você pedir"; escreva "atendo pedidos de eliminação e de oposição".

### 6.7 O mínimo prático — 7 itens

1. **Enxugar os campos** (art. 6º, III + art. 10, §1º). Sem CPF, CNPJ, endereço.
2. **Texto abaixo do botão de enviar** — abaixo, não em tooltip, porque o art. 9º exige
   "ostensiva". Redação de partida:

   > Ao enviar, seus dados (nome, e-mail, telefone, empresa e a descrição do projeto)
   > serão usados por **[NOME CIVIL COMPLETO — CNPJ 00.000.000/0001-00]** apenas para
   > responder a este contato e negociar o projeto, com base no legítimo interesse
   > (art. 7º, IX, da LGPD). Não vendo nem cedo seus dados. Guardo por até 24 meses após o
   > último contato. Você pode pedir acesso, correção, eliminação ou se opor ao tratamento
   > a qualquer momento em **contato@…**. Detalhes na [Política de Privacidade].

3. **Uma caixa desmarcada só para marketing** — e **só se ela realmente for mandar
   newsletter**. Se não for, não coloque caixa nenhuma. Sem `checked`, sem `required`, e
   nunca juntando com "aceito a política".
4. **Uma caixa desmarcada e em destaque para a transferência internacional** — é o
   mecanismo do art. 33, VIII, e ele exige destaque e distinção das outras finalidades:
   *"Este formulário é operado pela Tally (Bélgica, União Europeia) e seus dados serão
   armazenados fora do Brasil. Concordo especificamente com essa transferência."*
5. **Um caminho alternativo sem formulário, visível ao lado:** *"Prefere não usar o
   formulário? Escreva direto para contato@…"*. Isto resolve **dois** problemas de uma vez:
   dá saída a quem não aceita o item 4, e é **o que sustenta a liberdade** do consentimento
   dele. Sem alternativa, um consentimento obrigatório não é livre. (Bônus: essa rota já
   existe no site — é o `#contato` do `index.html` com o FormSubmit.)
6. **`politica-privacidade.html`, em duas partes:**
   - os sete incisos do art. 9º, cada um com título próprio, e a lista **nominal** dos nove
     incisos do art. 18; mais a frase do art. 11, §1º da Res. 2/2022: *"Não indiquei
     encarregado, por ser agente de tratamento de pequeno porte (art. 11 da Resolução
     CD/ANPD nº 2/2022). O canal de atendimento aos titulares é contato@…"*;
   - **seção destacada "Transferência internacional de dados"** com os seis itens do
     art. 17, §2º, nomeando o país de destino e terminando com *"Você pode peticionar
     contra mim perante a ANPD (gov.br/anpd)."*
7. **Um arquivo privado de duas páginas, fora do site** (escrever, não publicar): o **teste
   de balanceamento** do legítimo interesse nas três fases da ANPD (finalidade /
   necessidade / balanceamento e salvaguardas) e o **registro simplificado** do art. 9º da
   Res. 2/2022. É o que ela mostra se pedirem, e é a diferença entre "não tinha nada" e
   "tinha e estava documentado" na dosimetria do art. 52, §1º.

**Fica de fora do mínimo:** DPO, RIPD, banner de cookies (o site não tem analytics nem
pixel de terceiro — a CSP não permitiria), e cláusulas-padrão assinadas — esta última
porque é **factualmente inatingível**, não porque seja dispensada.

### 6.8 Risco real de sanção: **baixo** — mas o risco que importa não é multa

As sanções do art. 52 vão de advertência a multa de **até 2% do faturamento no Brasil,
limitada a R$ 50 milhões por infração**, mais bloqueio, eliminação e suspensão. O §1º manda
aplicar *"de forma gradativa"*, pesando gravidade, **boa-fé**, condição econômica e adoção
de boas práticas.

O único caso pecuniário conhecido contra pequeno porte é a **Telekall Infoservice** (DOU
06/07/2023, processo 00261.000489/2022-62): **R$ 14.400 no total**. E o que a empresa fazia
era **vender listas de WhatsApp de eleitores para campanha eleitoral** — tratamento sem base
legal nenhuma. Não tem relação com responder o briefing de quem procurou você.

**Onde o risco realmente mora, em ordem de probabilidade:**

1. **Due diligence de cliente B2B.** Este é o risco material, e é comercial, não
   regulatório. Marca grande contratando freelancer manda checklist de LGPD de compras ou
   jurídico. **Não ter política de privacidade no site já custou contrato para muita gente.**
   A perda é imediata e silenciosa — ninguém explica que você foi cortada por isso. Para
   uma profissional que atende Nestlé e Carrefour, **é este item que justifica o trabalho
   da seção 6, não o medo de multa.**
2. **Reclamação de titular** (art. 18, §1º) — prazo curto para responder e provar base
   legal e canal. O item 7 é o seguro.
3. **Responsabilidade civil (art. 42)** — corre no Judiciário, independe da ANPD, e **não
   tem teto de 2%**.

### 6.9 Anti-spam: três fatos antes das opções

**Fato 1 — o GitHub Pages não consegue validar token de captcha.** Turnstile, reCAPTCHA e
hCaptcha só protegem quando o **servidor** chama o `siteverify` com o token. Site estático
não tem servidor. Widget na página sem validação no backend = o bot ignora o widget e faz
POST direto no endpoint. **Colar captcha próprio aqui é teatro de segurança**, a menos que
quem recebe o POST valide o token — ou seja, a menos que o fornecedor faça isso nativamente.

**Fato 2 — CSP é por documento** (o mesmo da seção 2.2): o captcha que roda dentro do
iframe do fornecedor é governado pela CSP **dele**.

**Fato 3 — `form-action` não herda de `default-src`.** Neste site a diretiva é declarada
explicitamente (`formsubmit.co` no index, `'none'` no serviços), então **este site já está
do lado seguro** — mas significa que qualquer POST para fornecedor novo exige tocar nela.

### 6.10 O quadro, e a recomendação

| Opção | Script de terceiro? | Domínios exatos na CSP | Grátis? | Manutenção |
|---|---|---|---|---|
| **Honeypot** | não | **nenhum** | sim | quase zero |
| **Captcha nativo do fornecedor** (dentro do iframe) | não, no **seu** documento | **nenhum** | sim | **nenhuma** |
| **Cloudflare Turnstile** | sim | `script-src` e `frame-src`: `https://challenges.cloudflare.com`; `connect-src 'self'` só em pre-clearance | Free: challenges ilimitados, 20 widgets, 10 hostnames/widget | baixa no widget, **mas exige backend** |
| **Google reCAPTCHA** | sim | **três diretivas**: `script-src` `https://www.google.com/recaptcha/` + `https://www.gstatic.com/recaptcha/`; `frame-src` `https://www.google.com/recaptcha/` + `https://recaptcha.google.com/recaptcha/`; `connect-src` `https://www.google.com/recaptcha/` | 1.000 req/s ou 1.000.000 chamadas/mês | **exige backend** |
| **hCaptcha** | sim | **quatro diretivas** (`script-src`, `frame-src`, `style-src`, `connect-src`), todas com `https://hcaptcha.com` **e `https://*.hcaptcha.com`** — a doc **proíbe** fixar subdomínio | Free $0, **volume não publicado** | **exige backend** |

**Recomendação: o reCAPTCHA nativo da Tally, ligado digitando `/recaptcha` no formulário.
Custo de CSP: zero. Custo em dinheiro: zero. Manutenção: nenhuma.**

Por que ganha, e por margem larga:
- **A Tally valida o token dela.** Mata o Fato 1 sem backend, sem Worker, sem chave, sem
  secret para rotacionar.
- **Nenhum domínio do Google entra na CSP deste site** — o reCAPTCHA carrega dentro do
  documento servido por `tally.so`, sob a CSP da Tally (Fato 2). O site continua com
  `script-src 'self'`.
- **Está no plano gratuito**, para todos os usuários.
- **Não acrescenta transferência internacional para declarar.** Turnstile (Cloudflare, EUA),
  reCAPTCHA direto (Google, EUA) e hCaptcha (EUA) cada um adicionaria **uma segunda**
  transferência internacional ao item 6.4 — sem nenhum ganho de segurança aproveitável num
  site estático.
- Detalhe de implementação da doc da Tally: **posicionar o reCAPTCHA imediatamente antes do
  botão de enviar.** Em formulário multipágina, se ele fica na primeira página a validação
  expira antes do fim — e num briefing longo isso quebraria o envio.
- Ela também tem, de graça e sem script: **prevenção de duplicata**, proteção por senha e
  fechamento do formulário.

**O que eu explicitamente não faria:** implementar Turnstile, reCAPTCHA ou hCaptcha por
conta própria neste site. Pagaria 2, 3 ou 4 diretivas de CSP (a do hCaptcha com wildcard de
subdomínio), pagaria uma transferência internacional extra para declarar, e **não teria
proteção real** sem montar backend. É o pior retorno das opções disponíveis — e num
repositório que já se queimou três vezes com CSP, é também o caminho mais provável de
quebrar algo em silêncio.

**Para o `#contato` do `index.html`, que fica como está:** ele já tem o honeypot `_honey` e
o `_captcha=true` do FormSubmit. Isso já é o arranjo correto — o captcha do FormSubmit roda
**na página de destino, no domínio dele, depois do POST**, fora da CSP do site. Não mexa.

---

## 7. Riscos e armadilhas

### CSP — o que quebra, e como o erro se apresenta

1. **Esquecer a CSP na página nova.** Se a página de briefing for criada copiando o
   `servicos.html`, ela vem com `frame-src 'none'` — e o iframe da Tally **não carrega,
   silenciosamente na tela**. A única pista é uma linha no console. Sintoma: retângulo
   branco/vazio onde deveria estar o formulário. **Teste obrigatório: abrir o console e
   confirmar zero violação de CSP antes de dar push.**
2. **Confundir onde a CSP se aplica.** Já expliquei na seção 2.2, mas o erro inverso
   também acontece: alguém vê o formulário funcionando e resolve "limpar" a CSP liberando
   `connect-src https://tally.so`, `font-src`, `img-src`… tudo desnecessário. Cada domínio
   a mais é superfície que não precisava existir. **Uma diretiva, um domínio.**
3. **O `embed.js` é opcional, e é a única coisa que toca `script-src`.** Se um dia o
   formulário aparecer com barra de rolagem interna e alguém "resolver" liberando
   `script-src https://tally.so`, ele está trocando `script-src 'self'` — a diretiva mais
   valiosa da CSP inteira, a que impede JS de terceiro no site — por conveniência de
   layout. Vale muito mais chutar `height` para 1800 px.
4. **Meta-CSP não tem relatório.** `<meta http-equiv>` não suporta `report-uri`/`report-to`
   de forma útil, e o GitHub Pages não deixa mandar header. Não existe telemetria de
   violação de CSP neste site. Toda validação é manual, no console, por página. Isso é
   estrutural — não tem como consertar sem sair do Pages.
5. **Precedente do projeto:** a CSP deste site **já quebrou funcionalidade três vezes**
   (mp4 externo bloqueado, `font-src 'self'` obrigando a autohospedar as fontes, e a
   `lite-yt-embed.js` que teve de ser patcheada localmente e cujos 2 patches quebram se
   alguém atualizar pelo upstream). O padrão é claro: **neste repositório, a CSP é a
   primeira suspeita quando algo "simplesmente não aparece".**

### Deploy — o teto de 10 minutos

6. **7 páginas HTML não ameaçam o teto.** São dezenas de KB de texto. O risco é indireto:
   páginas novas convidam a acrescentar **imagens** (capa do briefing, ícone de serviço).
   Cada asset novo entra no `_site` e conta. O comentário do workflow é explícito: *"Não
   adicione diretórios ao `_site` sem medir."* O job já imprime `du -sh _site` — use.
7. **A pior falha é a silenciosa.** Arquivo fora do `cp` da linha 51 = deploy verde,
   arquivo 404 no ar. Ninguém é avisado. Some com o `on.push.paths` também, e o deploy
   nem roda — o commit fica no repo, o site fica velho, e parece cache de 10 min do Pages.
   **Os dois lugares, sempre.**
8. **`cp` com glob mata a garantia de fail-fast** que o workflow escolheu de propósito.
   Liste os nomes por extenso no `cp` (glob no `on.push.paths` é seguro).
9. **A `politica-privacidade.html` é o arquivo mais fácil de esquecer nas duas listas** —
   e é o único cuja ausência tem consequência jurídica, não só estética. Se o link do
   formulário aponta para uma política que dá 404, ela está pior do que se não tivesse
   link nenhum: fica documentado que prometeu o aviso do art. 9º e não entregou.
   **Publique e abra a URL antes de divulgar qualquer formulário.**

### Fornecedor

10. **Dependência de terceiro numa etapa de conversão.** Tally fora do ar = 7 briefings
   fora do ar. Mitigação barata: manter o `#contato` do `index.html` (FormSubmit) intacto
   como rota alternativa. Ele já existe e já funciona; não desligue.
11. **"Respostas ilimitadas" tem letra miúda** — a política de uso justo (50.000 respostas,
    100 GB de upload, 500 GB de armazenamento por mês). Irrelevante para o volume dela,
    mas é a razão de a seção 5 recomendar link em vez de upload: é justamente o eixo de
    upload que encosta na letra miúda primeiro.
12. **O selo "Made with Tally" no plano gratuito** é uma decisão de posicionamento, não
    um bug. Assuma consciente.

### GitHub Pages

13. **Nada roda no servidor.** Nenhuma validação, nenhum segredo, nenhum token verificado.
    Confirmado na documentação: *"GitHub Pages sites shouldn't be used for sensitive
    transactions like sending passwords or credit card numbers"* — e o uso é proibido para
    *"facilitating commercial transactions or providing commercial software as a service"*.
    Um briefing de contato não é transação comercial; está tranquilo. Mas **qualquer**
    solução que dependa de verificar um token no servidor (captcha próprio, por exemplo)
    é impossível aqui por construção.
14. **Cotas:** repositório de origem com limite recomendado de 1 GB, site publicado **no
    máximo 1 GB**, banda **soft de 100 GB/mês**, e 10 builds/hora — este último **não se
    aplica** a quem publica por workflow próprio do Actions, que é o caso. Nenhuma dessas
    cotas é ameaçada por páginas de formulário.
15. **Cache de ~10 min no Pages** faz um deploy bem-sucedido parecer que não subiu. Validar
    na origem com `curl`, não no navegador.

---

## 8. Fontes

### Código do repositório (lido, não pesquisado)

| Arquivo | O que entregou |
|---|---|
| `index.html:34` | CSP literal do index, com `formsubmit.co` já liberado em `connect-src` e `form-action` |
| `index.html:1195–1222` | o único formulário do projeto: campos, honeypot `_honey`, `_captcha=true` |
| `servicos.html:35` | CSP do serviços, com `frame-src 'none'` e `form-action 'none'` |
| `servicos.html:52–69` | JSON-LD `OfferCatalog` — a cópia paralela da copy dos 7 serviços |
| `servicos.html:145–151, 431–444` | os 7 âncoras dos serviços e o CTA atual, que aponta para `index.html#contato` |
| `script.js:3715–3787` | e-mail montado por JS pós-clique, token do FormSubmit, `fetch` com `AbortController` de 15 s |
| `servicos.js` (inteiro) | dependências reais do JS da página interna: `#header`, `#sideMenu`, `#navOverlay`, `#burgerBtn`, `[data-revelar]` |
| `.github/workflows/deploy-pages.yml` | `on.push.paths` (10–20), `cp` de inclusão (49–51), e o histórico do teto de 10 min (3–5, 82–90) |
| `sitemap.xml` | só 2 URLs hoje |

### Documentação e preços pesquisados (todos consultados em 13/08/2026)

| URL | O que entregou |
|---|---|
| https://tally.so/pricing | planos e o que o Free inclui: formulários e submissões ilimitados, lógica condicional, webhooks, Google Sheets/Notion/Airtable/Zapier/Make, upload de 10 MB por arquivo. Pro adiciona remoção de marca, domínio próprio e upload sem limite |
| https://tally.so/help/plans-and-pricing | **preço literal: Pro US$ 29/mês, Business US$ 89/mês** (mensal). A página de preço mostra US$ 24 e US$ 74 na visão anual (2 meses de desconto) |
| https://tally.so/help/file-uploads | *"10MB for free"* por arquivo; Pro *"no limit to the file upload size"*; sem limite de nº de arquivos, de armazenamento total nem de tempo de retenção |
| https://tally.so/help/fair-use-policy | os números da letra miúda do "ilimitado": **50.000 submissões/mês, 100 GB de upload/mês ou 500 GB total, 50.000 e-mails/mês**; picos ok, 3–4 meses seguidos dispara contato |
| https://tally.so/widgets/embed.js | **o arquivo em si** — confirma que os únicos hosts que ele usa são `tally.so/embed/{id}` e `tally.so/popup/{id}`. Base do `frame-src https://tally.so` |
| https://tally.so/help/embed-your-form | confirma os 3 modos de embed (standard, popup, full page); **não publica o código literal** |
| https://tally.so/help/hidden-fields | formato literal da URL com query string: `https://tally.so/r/nPA50m?name=Marie&ref=email`. Confirma o padrão `tally.so/r/{id}` e que campos ocultos são gratuitos |
| https://tally.so/help/redirect-on-completion | *"Redirect on completion is free to use for all Tally users"*; dá para passar respostas na URL de destino |
| https://tally.so/features | confirma no gratuito: formulário multipágina, lógica condicional, campos calculados. **Lista oficial de integrações — ClickUp NÃO está nela**: Notion, Slack, Airtable, Google Sheets, Zapier, Make, Coda, Webhooks, n8n, Linear, Discord, Integrately, Pipedream, IFTTT, servidor MCP, Google Analytics. Barra de progresso e validação de resposta **não aparecem** na lista |
| https://tally.so/help/partial-submissions | **respostas parciais são exclusivas do Tally Pro**; e mesmo no Pro elas *"can't be synced to other applications using integrations and they won't trigger email notifications"* — só export manual em CSV |
| https://tally.so/help/gdpr · https://tally.so/help/privacy-policy | empresa europeia sujeita ao GDPR, dados na UE (servidores em Frankfurt segundo fonte secundária — **a região exata não está confirmada na página oficial**), criptografia em trânsito e em repouso, DPA aceito na criação da conta e fornecido a pedido |
| https://www.fillout.com/pricing | Free US$ 0 / Starter US$ 15 / Pro US$ 40 / Business US$ 75 mensais; 1.000 respostas/mês no Free; upload em todos os planos com 20 MB (Free/Starter/Pro) e "1 GB+" no Business; lógica condicional desde o Free; remoção total de marca a partir do Pro; webhooks e Sheets desde o Free. **ClickUp não é citado** |
| https://www.fillout.com/help/sharing (via busca) | os dois domínios do embed: iframe em `https://forms.fillout.com/t/{id}`, script em `https://server.fillout.com/embed/v1/` |
| https://formsubmit.co/documentation | *"the sum of each file size must not exceed the 10MB size limit"* com `enctype=multipart/form-data`; *"unlimited submissions from unlimited forms"*; endpoint AJAX `formsubmit.co/ajax/...`; honeypot `_honey`; **nenhum preço publicado**; `_webhook` existe |
| https://formsubmit.co/help | arquivos enviados não são retidos após 30 dias |
| https://web3forms.com/ (via busca; a página de preço devolveu HTTP 403) | 250 submissões/mês no free; **upload de arquivo só nos planos pagos**; endpoint `https://api.web3forms.com/submit` |
| https://formspree.io/pricing | **página renderizada por JS, não consegui ler na origem.** Os números (50 submissões/mês no free, Personal US$ 15/mês com 200 submissões e 1 GB de upload) vêm de fontes secundárias de 2026 e estão **não confirmados** |
| https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits | as cotas literais: repositório de origem com limite recomendado de 1 GB, site publicado *"no larger than 1 GB"*, *"soft bandwidth limit of 100 GB per month"*, *"soft limit of 10 builds per hour"* (que não se aplica a workflow próprio), proibição de *"facilitating commercial transactions or providing commercial software as a service"*, e *"shouldn't be used for sensitive transactions like sending passwords or credit card numbers"*. Também: **deploys estouram em 10 minutos** |
| https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-src | a base da seção 2.2: `frame-src` *"specifies valid sources for nested browsing contexts"* — governa se o iframe carrega, não os recursos dentro dele |
| https://github.com/w3c/webappsec-csp/issues/608 · https://github.com/mdn/content/issues/21114 | `navigate-to` **removido da spec de CSP em setembro de 2022** e nunca implementado em navegador nenhum → link para fora não é governado por CSP. Base do plano B |
| https://developers.cloudflare.com/turnstile/reference/content-security-policy/ | domínios literais do Turnstile: `script-src: https://challenges.cloudflare.com` e `frame-src: https://challenges.cloudflare.com`; alternativa recomendada por nonce/`strict-dynamic` |
| https://developers.google.com/recaptcha/docs/faq | domínios literais do reCAPTCHA: `script-src` `https://www.google.com/recaptcha/` + `https://www.gstatic.com/recaptcha/`; `frame-src` `https://www.google.com/recaptcha/` + `https://recaptcha.google.com/recaptcha/`; `connect-src` `https://www.google.com/recaptcha/`. Free até 1.000.000 chamadas/mês; Enterprise 10.000 avaliações/mês sem custo |
| https://wetransfer.com/help-center/subscriptions/plan-limits (via busca) | free: **3 GB por transferência**, até 10 transferências ou 3 GB numa janela móvel de 30 dias |
| https://masv.io/pricing · https://help.massive.io/en/free-tier-pay-as-you-go | **15 GB/mês grátis, depois US$ 0,25/GB**, pago por quem recebe |
| Frame.io (fontes secundárias de 2026) | Team a partir de **US$ 25/membro/mês**, até 15 membros; preço por faixa de armazenamento, não por GB. **Não confirmado na página oficial de preço** |
| Google Forms — upload (fontes secundárias de 2026, consistentes entre si) | upload **exige login em conta Google de todo respondente, sem exceção nem contorno dentro do Google Forms** |
| Typeform (fontes secundárias de 2026) | free caiu para **10 respostas/mês em fev/2026**; Basic US$ 25/mês com 100 respostas. O limite é teto rígido: ao bater, o formulário para de coletar |
| Jotform (fontes secundárias de 2026, incluindo páginas de ajuda da própria Jotform) | free: **5 formulários**, 100 submissões/mês, 1.000 visualizações/mês, 100 MB de espaço, 500 submissões armazenadas no total; pago a partir de US$ 34/mês no anual |
| Cognito Forms (fontes secundárias de 2026) | free: formulários ilimitados, **100 entradas/mês**, 100 MB; lógica condicional completa no free; Pro US$ 19/mês. **Não confirmado na página oficial** |
| Netlify Forms (fontes secundárias) | detecção do formulário acontece no build da Netlify → **exige hospedagem na Netlify**, inviável no GitHub Pages |

### APIs — Tally e ClickUp (consultadas em 13/08/2026)

| URL | O que entregou |
|---|---|
| https://developers.tally.so/api-reference/introduction | a API é REST pública, autenticação **Bearer token**, **100 requisições por minuto**; a própria doc sugere webhooks para não esbarrar no limite |
| https://developers.tally.so/llms.txt | o índice completo dos endpoints. Os que sustentam a seção 4: `GET /forms/{formId}/submissions`, `GET /forms/{formId}/submissions/{submissionId}`, `GET /forms/{formId}/questions`, `GET /forms/{formId}/analytics/drop-off`, e o CRUD de `/webhooks`. A marca *"Requires a Pro subscription"* aparece **só** em workspaces e folders — **não em submissions** |
| https://developer.clickup.com/reference/createtask | `POST /v2/list/{list_id}/task`; autenticação por **personal token (`Authorization: pk_...`)** ou OAuth 2.0; **só `name` é obrigatório** |
| https://developer.clickup.com/reference/createtaskattachment | `POST /v2/task/{task_id}/attachment`, `multipart/form-data`; a doc recomenda a **V3 Attachments API**; **limite de tamanho não documentado — não confirmado** |
| https://developer.clickup.com/docs/rate-limits | **100 req/min por token no Free Forever, Unlimited e Business**; 1.000 no Business Plus; 10.000 no Enterprise. Excedente = HTTP 429 com `X-RateLimit-Limit`/`-Remaining`/`-Reset` |
| https://help.clickup.com/ (Form view) | **HTTP 403 — não consegui ler.** Por isso o domínio de embed do formulário nativo do ClickUp está **não confirmado**, e a seção 4.2 se recusa a recomendar liberar um domínio não verificado na CSP |

### LGPD — lei, regulamentos e jurisprudência administrativa (consultados em 13/08/2026)

| URL | O que entregou |
|---|---|
| https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm | **texto integral da LGPD.** Base de tudo na seção 6: arts. 7º, 8º, 9º, 10, 15, 16, 18, 33–36, 41, 42 e 52, transcritos literalmente |
| https://www.in.gov.br/en/web/dou/-/resolucao-cd-anpd-n-19-de-23-de-agosto-de-2024-580095396 | **Resolução CD/ANPD nº 19/2024, DOU 23/08/2024, Edição 163, Seção 1, p. 123** — Regulamento de Transferência Internacional inteiro + Anexo II (as cláusulas-padrão). Arts. 3º, 7º, 9º, 16 e 17 transcritos. **Confirmado por leitura integral: nenhum artigo menciona agente de pequeno porte** |
| https://www.in.gov.br/en/web/dou/-/resolucao-cd-anpd-n-2-de-27-de-janeiro-de-2022-376562019 | **Resolução CD/ANPD nº 2/2022** — o regime de pequeno porte. Art. 2º, I (inclui pessoa natural), art. 11 e §1º (dispensa de encarregado + canal obrigatório), arts. 3º/4º (o que é alto risco), art. 9º (registro simplificado), art. 14, I (prazo em dobro), art. 6º (o que **não** é dispensado) |
| https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia_legitimo_interesse.pdf | **Guia Orientativo de Legítimo Interesse da ANPD**, publicado em 02/02/2024 — o teste de balanceamento em três fases (finalidade / necessidade / balanceamento e salvaguardas) e o critério de legítima expectativa. O PDF entregou só metadados; o conteúdo veio da análise do Data Privacy Brasil (https://www.dataprivacybr.org/guia-do-legitimo-interesse-orientacoes-da-anpd/) |
| https://www.mayerbrown.com/pt/insights/publications/2025/08/end-of-grace-period-implementation-of-brazils-standard-contractual-clauses-in-international-transfers-of-personal-data | confirma que o prazo de 12 meses do parágrafo único do art. 2º da Res. 19/2024 **venceu em 23/08/2025** |
| https://tally.so/help/data-processing-agreement | o DPA da Tally: traz SCCs **apenas europeias** (*Decision (EU) 2021/914*, Schedule II) e **nenhuma menção a LGPD, ANPD ou cláusulas-padrão brasileiras**. É o que fecha a via (b) do art. 9º, II do Regulamento |
| Caso Telekall Infoservice — https://www.jusbrasil.com.br/artigos/a-primeira-sancao-aplicada-pela-anpd-o-caso-telekall-infoservice/1893365255 | única sanção pecuniária conhecida contra microempresa: **R$ 14.400**, DOU 06/07/2023, processo SEI/ANPD 00261.000489/2022-62, por venda de listas de contatos de eleitores. A notícia oficial da ANPD devolveu HTTP 401 |
| Lei nº 15.352/2026 (ANPD como agência reguladora) e volume de processos sancionadores em 2026 | **fontes secundárias (Confidata, Instituto SIGILO, Turivius) — não confirmado em fonte oficial nem no DOU.** A direção da tendência é mais fiscalização; nada indica mudança de patamar para este porte e este tipo de dado |

### Anti-spam (consultados em 13/08/2026)

| URL | O que entregou |
|---|---|
| https://developers.cloudflare.com/turnstile/reference/content-security-policy/ | **página atualizada em 05/05/2026.** `script-src` e `frame-src` = `https://challenges.cloudflare.com`; `connect-src 'self'` **apenas** em modo pre-clearance; nonce/`strict-dynamic` recomendados. **Nota:** fontes de terceiros listam também `connect-src https://challenges.cloudflare.com`, que **não está na doc oficial** — não confirmado |
| https://developers.cloudflare.com/turnstile/plans/ | **página atualizada em 16/04/2026.** Free: *"Unlimited challenges"*, até 20 widgets, 10 hostnames por widget, 7 dias de analytics |
| https://developers.google.com/recaptcha/docs/faq | **página atualizada em 02/04/2026 UTC.** Os domínios das três diretivas + free tier de **1.000 req/s ou 1.000.000 chamadas/mês** + o comportamento de excedente: *"may fail open by returning a static score 0.9"* com *"Over free quota"* — degrada em silêncio. `style-src`: **não especificado, não confirmado** |
| https://docs.hcaptcha.com/ + https://docs.hcaptcha.com/configuration/ | **quatro diretivas** (`script-src`, `frame-src`, `style-src`, `connect-src`) com `https://hcaptcha.com` **e `https://*.hcaptcha.com`**, e o aviso literal: *"Please do not hard-code specific subdomains (...) asset subdomains used may vary over time or by region"* |
| https://www.hcaptcha.com/pricing | Free = **$0**, e declara conformidade com *"GDPR, CCPA, **LGPD**, PIPL"*. **Volume mensal do free: não publicado, não confirmado.** Pro: 100K evals + $0,99/1K, a $139/mês mensal ou $99/mês anual |
| https://tally.so/help/recaptcha | **reCAPTCHA v2 nativo, gratuito para todos os usuários**, inserido digitando `/recaptcha`; recomendação de posicionar **imediatamente antes do botão de enviar** — em formulário multipágina, colocado no começo, a validação **expira** |
| https://developers.tally.so/widgets/introduction | corrobora os hosts do embed: script `https://tally.so/widgets/embed.js`, iframe em `https://tally.so` |
| https://help.formspree.io/hc/en-us/articles/360017735154-How-to-prevent-spam | filtro de spam por machine learning, honeypot, **restrição de domínio** (só aceita POST dos domínios autorizados — custo zero de CSP e mata o POST direto) e regras custom no Business. Só o reCAPTCHA exige script de terceiro |
| Eficácia de honeypot (Clearout, Splitforms, Prospect Hub) | **blogs e fornecedores; os percentuais que circulam (~80% sozinho, >99% com time-trap) NÃO estão confirmados** em fonte oficial ou estudo revisado. O consenso qualitativo é convergente: pega bot burro, e bot moderno com navegador headless ignora o isco de propósito |
