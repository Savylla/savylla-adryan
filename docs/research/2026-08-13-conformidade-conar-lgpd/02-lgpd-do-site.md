# LGPD — o que este site precisa

> Pesquisa de 13/08/2026. Lei e resoluções lidas no original (Planalto e gov.br/anpd) —
> as URLs estão na seção 11. Onde não consegui confirmar, está escrito
> **não confirmado**, e não é para tratar como fato.
>
> Isto é pesquisa técnica, não parecer jurídico. Não sou advogada dela.

---

## 1. Diagnóstico do que existe hoje

Tudo nesta seção foi lido no código, não pesquisado.

### 1.1 O formulário que já está no ar

`index.html:1195–1222` — o `#contatoForm`. Quatro campos visíveis:

| Campo | `name` | Obrigatório |
|---|---|---|
| Seu nome | `nome` | sim |
| Seu email | `email` | sim |
| Assunto | `assunto` | não |
| Sua mensagem | `mensagem` | sim |

Mais quatro campos de controle do FormSubmit: `_subject`, `_captcha=true`,
`_template=table` e o honeypot `_honey`.

O envio é por `fetch` para `https://formsubmit.co/ajax/{token}` (`script.js:3756`), com
`AbortController` de 15 s. O `action` nativo é preenchido em runtime como fallback
(`script.js:3738`). O token é `FORMSUBMIT_TOKEN` em `script.js:3728` — recurso de
"Invisible email" do FormSubmit, então **o endereço de destino não existe em nenhum
ponto do front-end**. Só o FormSubmit sabe para onde encaminha.

**Nome, e-mail e mensagem são dado pessoal** (art. 5º, I: *"informação relacionada a
pessoa natural identificada ou identificável"*). Coletar, transmitir e armazenar é
tratamento (art. 5º, X). Ela é a **controladora** (art. 5º, VI). O FormSubmit é
**operador** (art. 5º, VII).

### 1.2 Tudo que sai do navegador do visitante para um terceiro

| Terceiro | Quando dispara | O que sai | Interação do visitante? |
|---|---|---|---|
| **GitHub Pages** (GitHub Inc., EUA) | toda visita | IP, user-agent, página pedida — logs de servidor | não |
| **Google** — `youtube.com`, `youtube-nocookie.com`, `i.ytimg.com`, `img.youtube.com` | **no carregamento da home** | IP + SNI do TLS, via 4 `<link rel="preconnect">` em `index.html:44–47` | **não** |
| **FormSubmit** | ao enviar o formulário | nome, e-mail, assunto, mensagem | sim |
| **YouTube** (`youtube-nocookie.com`) | ao abrir um projeto e tocar o vídeo | IP, user-agent, referer, cookies do YouTube | sim |
| **Google Ads** — `googleads.g.doubleclick.net`, `static.doubleclick.net` | ao interagir com o player | IP + SNI, via `preconnect` em `assets/lib/lite-yt-embed.js:118–119` | sim |
| **Meta / Instagram** | ao abrir um post do Instagram no player | IP, user-agent, referer, cookies da Meta | sim |

Dois detalhes que importam:

- **Os embeds de vídeo só nascem depois de um clique.** Não há nenhum `lite-youtube`
  no HTML estático (`grep -c` = 0); os elementos são criados por JS quando o modal
  abre (`script.js:2937, 2942, 3064, 3481`). Isso é bom, e é raro.
- **Mas os `preconnect` do `<head>` não esperam clique nenhum.** `index.html:44–47`
  abre conexão TCP+TLS com quatro hosts do Google em toda visita à home, antes de
  qualquer interação. `preconnect` não é só DNS: é handshake completo, e o IP do
  visitante chega ao Google. Essas quatro linhas são, hoje, o único vazamento de dado
  do visitante que acontece **sem ato nenhum dele**. E são largamente redundantes: a
  própria `lite-yt-embed.js` já faz o aquecimento sozinha, no `warmConnections()`
  (linhas 109–122), quando o player é tocado.
- Os dois `preconnect` para `doubleclick` vêm de fábrica na biblioteca, e o comentário
  do próprio autor, na linha 117, diz: *"Not certain if these ad related domains are in
  the critical path."* São domínios de publicidade do Google. Tirar as duas linhas é
  barato e não quebra nada.

### 1.3 O que o site **não** faz — e isso é uma vantagem grande

Procurei e não existe, em `index.html`, `servicos.html`, `script.js`, `servicos.js`
nem `style.css`:

- nenhum Google Analytics, `gtag`, Tag Manager, Meta Pixel, Hotjar, Clarity — **zero
  analytics**;
- nenhum `localStorage`, `sessionStorage` ou `document.cookie` — **o site não grava
  nada no navegador de ninguém**;
- nenhuma fonte de CDN. As fontes são autohospedadas em `assets/fonts/`, e a CSP está
  em `font-src 'self'`.

As duas CSP (`index.html:34`, `servicos.html:35`) são fechadas e explícitas. A de
serviços é mais restrita ainda (`form-action 'none'`, `frame-src 'none'`,
`connect-src 'self'`).

Isso significa que **ela não precisa de banner de cookies**. Não é um atalho: é que
não há cookie próprio nem cookie de terceiro sendo posto por decisão dela no
carregamento da página. Ver seção 4.

Um detalhe que poderia confundir: o `_captcha=true` em `index.html:1197` é um sinalizador
processado **do lado do FormSubmit**, não um script na página dela. Não há reCAPTCHA no
site — não existe `recaptcha`, `grecaptcha` nem `gstatic` em nenhum arquivo, e o
`script-src 'self'` da CSP bloquearia de qualquer forma. Nenhum script do Google roda
aqui.

### 1.4 Existe política de privacidade hoje? Não.

Procurei por `privacidade`, `privacy`, `cookie`, `LGPD`, `dados pessoais` nos cinco
arquivos do site. **Zero ocorrências.** Não há página, não há link no rodapé
(`index.html:1230–1236` lista Sobre, Marcas, Projetos, Serviços, Contato), não há uma
linha sequer perto do botão de enviar.

**Então, com todas as letras:** hoje já existe um formulário no ar coletando nome,
e-mail e mensagem de pessoas reais, transmitindo esses dados a um operador estrangeiro,
sem nenhuma informação ao titular. Isso é descumprimento do art. 9º da LGPD **agora**,
não quando o briefing entrar no ar. O briefing só aumenta o volume e a sensibilidade
do que é coletado — o problema de transparência já está instalado.

O art. 9º é direto:

> Art. 9º O titular tem direito ao acesso facilitado às informações sobre o tratamento
> de seus dados, que deverão ser disponibilizadas de forma clara, adequada e ostensiva
> acerca de, entre outras características previstas em regulamentação para o
> atendimento do princípio do livre acesso:
> I - finalidade específica do tratamento;
> II - forma e duração do tratamento, observados os segredos comercial e industrial;
> III - identificação do controlador;
> IV - informações de contato do controlador;
> V - informações acerca do uso compartilhado de dados pelo controlador e a finalidade;
> VI - responsabilidades dos agentes que realizarão o tratamento; e
> VII - direitos do titular, com menção explícita aos direitos contidos no art. 18 desta Lei.

E a LGPD se aplica a ela. O art. 4º, I tira da lei o tratamento *"realizado por pessoa
natural para fins exclusivamente particulares e não econômicos"* — um portfólio
profissional que capta cliente é econômico. O art. 3º confirma: a lei alcança
*"qualquer operação de tratamento realizada por pessoa natural"* quando feita no
território nacional.

---

## 2. A base legal

### 2.1 Recomendação: **art. 7º, V — não legítimo interesse**

A decisão que já estava tomada era usar **legítimo interesse** (art. 7º, IX). Pesquisei
e a recomendação é **trocar**. A base certa para o formulário de contato e para o
briefing é:

> Art. 7º, V — quando necessário para a execução de contrato ou de **procedimentos
> preliminares relacionados a contrato** do qual seja parte o titular, **a pedido do
> titular dos dados**.

Quatro razões, em ordem de peso.

**(a) É literalmente o que acontece.** Ninguém preenche um briefing de 14 campos por
acaso. A pessoa está pedindo um orçamento. Isso é procedimento preliminar a contrato,
a pedido do titular — o inciso V descreve o fato com precisão. Legítimo interesse
descreveria pior.

**(b) É o que destrava a transferência internacional — e legítimo interesse não
destrava.** Este é o ponto decisivo, e é técnico:

> Art. 33. A transferência internacional de dados pessoais somente é permitida nos
> seguintes casos: [...]
> IX - quando necessário para atender as hipóteses previstas nos **incisos II, V e VI
> do art. 7º** desta Lei.

O inciso **IX do art. 7º (legítimo interesse) não está nessa lista**. O inciso **V
está**. E a Resolução CD/ANPD nº 19/2024 reconhece o art. 33, IX como mecanismo válido
de transferência, no art. 9º, II, "c" do Regulamento anexo:

> Art. 9º A transferência internacional de dados somente poderá ser realizada [...]
> desde que amparada em: I - uma das hipóteses legais previstas no art. 7º ou no art. 11
> da Lei nº 13.709 [...]; e II - um dos seguintes mecanismos válidos [...]
> c) nas hipóteses previstas nos incisos II, "d", e III a IX do art. 33 da Lei nº 13.709.

Traduzindo para o caso dela:

- **Com art. 7º, V** → mecanismo de transferência = art. 33, IX → **não precisa de
  cláusula-padrão contratual, não precisa de contrato assinado com o FormSubmit.**
- **Com legítimo interesse** → o art. 33, IX não cobre → sobraria assinar as
  cláusulas-padrão da ANPD com o FormSubmit (art. 33, II, "b"), ou pedir consentimento
  específico e destacado só para a transferência (art. 33, VIII). Nenhuma das duas é
  viável (seção 5).

Ou seja: a base legal que parecia a mais "confortável" é justamente a que quebra a
cadeia de conformidade da transferência internacional.

**(c) Legítimo interesse cobra documentação que ela não precisa produzir.** O Guia
Orientativo da ANPD sobre Legítimo Interesse (fev/2024) diz que o teste de
balanceamento é *"boa prática e medida recomendável para demonstrar o atendimento dos
requisitos para enquadramento no legítimo interesse"* e *"ferramenta essencial para
demonstrar a conformidade do tratamento de dados pessoais, nos termos do art. 6º, X
(princípio da responsabilização e prestação de contas) e do art. 37, da LGPD"*.

Não é uma formalidade obrigatória por si só — a ANPD diz expressamente que o modelo do
Anexo II *"não é de uso obrigatório"* e que *"em algumas circunstâncias, o teste pode
ser breve ou simplificado"*. Mas o ônus de provar existe, e recai sobre ela. Some-se
o art. 37 da LGPD, que manda manter registro das operações *"especialmente quando
baseado no legítimo interesse"*, e o art. 10, §2º, que exige *"medidas para garantir a
transparência do tratamento"*, e o art. 10, §3º, que autoriza a ANPD a pedir relatório
de impacto justamente de quem usa essa base. Trabalho a mais, para um resultado pior.

**(d) Consentimento também não é a melhor escolha aqui**, e a decisão de não usar
checkbox estava certa — só que pelo motivo errado. O Guia de Cookies da ANPD registra
que *"inexista hierarquia ou preferência entre as hipóteses legais previstas na LGPD"*,
mas também que o consentimento *"não é apropriado"* quando o tratamento é essencial
para prestar o serviço que o próprio titular pediu. Um briefing é exatamente isso.
Além disso, consentimento pode ser revogado a qualquer momento (art. 8º, §5º) e o ônus
de provar que foi obtido validamente é do controlador (art. 8º, §2º). Seria mais
obrigação, não menos.

### 2.2 O ponto onde o art. 7º, V acaba

O art. 7º, V cobre: receber o briefing, ler, responder, orçar, negociar, executar o
projeto e guardar o histórico do projeto contratado.

**Não cobre:** guardar o briefing de quem não fechou para mandar novidade depois,
montar mailing, disparar promoção. Isso não é procedimento preliminar de contrato —
já é prospecção. Para isso as opções são:

1. **Não fazer.** É a recomendação. Apagar no prazo da seção 8 e pronto.
2. Se um dia quiser fazer: um checkbox **opcional e desmarcado** ("quero receber
   novidades"), que é consentimento (art. 7º, I), com descadastramento fácil. Um
   checkbox opcional não contamina o resto do formulário.
3. Legítimo interesse com teste de balanceamento documentado — o art. 10, I admite
   *"apoio e promoção de atividades do controlador"*. Possível, mas é o caminho caro.

A coerência importa: se ela usar os dados para mailing, o argumento do art. 7º, V cai —
e junto cai o mecanismo de transferência internacional do art. 33, IX.

### 2.3 O que precisa estar documentado

Pouca coisa, e nada disso vai para o site — é arquivo dela:

- **Registro simplificado das operações** (art. 37 da LGPD, em forma simplificada pelo
  art. 9º da Res. 2/2022). A ANPD publica um modelo pronto de ROPA para pequeno porte,
  em Excel e PDF (seção 11).
- **Uma folha registrando a análise do art. 4º do Regulamento da Res. 19/2024**: que
  há transferência internacional, que a hipótese legal é o art. 7º, V, e que o
  mecanismo é o art. 33, IX. É o Regulamento que joga essa verificação no colo do
  controlador. Cabe em cinco linhas.
- **Política simplificada de segurança** (art. 13 da Res. 2/2022) — facultada em
  formato simplificado, considerando *"os custos de implementação, bem como a
  estrutura, a escala e o volume das operações"*.

---

## 3. O mínimo obrigatório

| # | O que tem que existir | Onde a lei exige |
|---|---|---|
| 1 | **Aviso de privacidade** publicado e acessível, com os 7 itens do art. 9º | LGPD art. 9º, I–VII; Res. CD/ANPD 2/2022, art. 7º |
| 2 | **Canal de comunicação com o titular**, divulgado | Res. CD/ANPD 2/2022, art. 11, §1º; Res. CD/ANPD 18/2024, art. 3º, §3º |
| 3 | **Atender os direitos do titular** quando pedidos | LGPD art. 18, I–IX |
| 4 | **Informar a transferência internacional** — que os dados passam por serviço fora do Brasil, qual país, por quê | LGPD art. 9º, V; e o roteiro do art. 17, §2º do Reg. da Res. 19/2024 |
| 5 | **Registro das operações de tratamento** (arquivo dela, não do site) | LGPD art. 37; simplificado pelo art. 9º da Res. 2/2022 |
| 6 | **Coletar só o necessário** — não pedir campo que ela não usa | LGPD art. 6º, III (necessidade) |
| 7 | **Eliminar quando a finalidade acabar** | LGPD arts. 15 e 16 |
| 8 | **Medidas de segurança** proporcionais | LGPD art. 6º, VII e art. 46; simplificado pelo art. 13 da Res. 2/2022 |
| 9 | **Saber o que fazer se vazar** — comunicar ANPD e titular | LGPD art. 48; Res. CD/ANPD 15/2024; prazo em dobro pelo art. 14, II da Res. 2/2022 |

Sobre o item 1, um ponto que costuma ser mal entendido: **o pequeno porte NÃO está
dispensado do aviso de privacidade.** O art. 7º da Res. 2/2022 é explícito — os agentes
de pequeno porte *"devem disponibilizar informações sobre o tratamento de dados
pessoais e atender às requisições dos titulares em conformidade com o disposto nos
arts. 9º e 18 da LGPD"*, podendo escolher o meio (eletrônico, impresso ou outro). A
flexibilização é de **forma**, não de **conteúdo**.

Sobre o item 2: como ela é dispensada de encarregado (seção 4), o canal substitui o
DPO. Na prática, **um endereço de e-mail publicado no aviso de privacidade cumpre isso**.

Sobre o item 3, os direitos que ela precisa saber atender (art. 18): confirmação de que
existe tratamento, acesso, correção, anonimização/bloqueio/eliminação, portabilidade,
eliminação dos dados tratados com consentimento, informação sobre com quem
compartilhou, e revogação de consentimento. Na escala dela, quase todo pedido vai ser
"apaga meus dados" ou "o que você tem sobre mim" — e a resposta é procurar no Gmail e
responder.

---

## 4. O que ela **não** precisa

Ela se enquadra como **agente de tratamento de pequeno porte**. O art. 2º, I do
Regulamento da Res. CD/ANPD nº 2/2022 inclui, com todas as letras, *"pessoas naturais
[...] que realizam tratamento de dados pessoais, assumindo obrigações típicas de
controlador ou de operador"*.

E ela não cai em nenhuma exclusão do art. 3º, que só desenquadra quem: (I) faz
tratamento de alto risco; (II) tem receita bruta acima do limite da LC 123/2006; ou
(III) pertence a grupo econômico acima desse limite. Sobre o alto risco, o art. 4º
exige **cumulativamente** um critério geral (larga escala, ou afetar significativamente
direitos fundamentais) **e** um específico (tecnologia emergente, vigilância de zonas
públicas, decisão automatizada, dado sensível, dado de criança/idoso etc.). Um
formulário de briefing de audiovisual não atende nem o geral.

Com isso, a Res. 2/2022 dispensa ou flexibiliza:

| Artigo | O que ela ganha |
|---|---|
| **Art. 9º** | Registro das operações do art. 37 pode ser **simplificado**, e *"a ANPD fornecerá modelo"* — e forneceu (ROPA em xlsx e pdf) |
| **Art. 11** | **Não precisa indicar encarregado/DPO.** §1º: basta disponibilizar canal de comunicação com o titular |
| **Art. 11, §2º** | Se ela quiser indicar um encarregado mesmo assim, isso conta como **política de boas práticas e governança** para o art. 52, §1º, IX — atenuante em eventual sanção |
| **Art. 13** | **Política simplificada** de segurança da informação, considerando custos, estrutura e escala (§1º) |
| **Art. 14** | **Prazo em dobro** para atender solicitações de titulares e para comunicar incidente de segurança |
| **Art. 15** | Até **15 dias** para fornecer a declaração simplificada do art. 19, I da LGPD |

A dispensa de encarregado continua valendo depois do novo regulamento do encarregado:
a Res. CD/ANPD nº 18/2024, art. 3º, §3º, remete de volta — *"Os Agentes de Tratamento
de Pequeno Porte dispensados de indicar encarregado devem disponibilizar um canal de
comunicação com o titular de dados, nos termos do art. 11 do Regulamento [...] aprovado
pela Resolução CD/ANPD nº 2, de 27 de janeiro de 2022"*.

Além disso, **ela não precisa**:

- **Banner de cookies.** O site não grava cookie nem storage nenhum (seção 1.3), e os
  conteúdos incorporados de YouTube e Instagram só carregam depois de um clique
  deliberado. Se um dia ela adicionar analytics, muda: o Guia de Cookies da ANPD
  classifica *"medir o desempenho da página"* e *"exibir anúncios ou outros conteúdos
  incorporados"* como cookies **não necessários**, e diz que *"o recurso ao
  consentimento será mais apropriado quando a coleta de informações for realizada por
  cookies não necessários"*. Ou seja: **botar Google Analytics neste site cria a
  obrigação de banner que hoje não existe.** É uma decisão com custo de conformidade,
  não só técnica.
- **Relatório de Impacto (RIPD).** Só se a ANPD determinar (art. 38), ou pedir por
  causa de legítimo interesse (art. 10, §3º) — mais um motivo para não usar essa base.
- **Teste de balanceamento (LIA)**, se adotar o art. 7º, V como recomendado.
- **Cadastro em nada.** Não existe registro de controladores na ANPD.
- **Advogado, DPO terceirizado ou consultoria.** Nada na lei exige.

Duas ressalvas honestas: o art. 6º da Res. 2/2022 avisa que a dispensa *"não isenta os
agentes de tratamento de pequeno porte do cumprimento dos demais dispositivos da LGPD,
inclusive das bases legais e dos princípios"*. E o art. 16 permite à ANPD determinar,
caso a caso, o cumprimento das obrigações dispensadas.

---

## 5. O problema do FormSubmit

### 5.1 O enquadramento

O FormSubmit recebe os dados **em nome dela** e faz uma coisa só com eles: encaminhar.
Isso o torna **operador** (art. 5º, VII). Ela continua controladora e continua
responsável.

Se o FormSubmit está sediado fora do Brasil — e tudo indica que sim (seção 5.2) —
mandar os dados para ele é **transferência internacional**. O Regulamento da Res.
19/2024 define, no art. 3º, III, transferência como *"operação de tratamento por meio
da qual um agente de tratamento transmite, compartilha ou disponibiliza acesso a dados
pessoais a outro agente de tratamento"*, e o art. 5º fecha: *"A transferência
internacional de dados será caracterizada quando o exportador transferir dados pessoais
para o importador."*

### 5.2 Onde fica o FormSubmit — e é pior do que parecia

Este foi o achado mais desconfortável da pesquisa. **O FormSubmit não é uma empresa
americana.** E, a rigor, não dá para afirmar que seja uma empresa.

| O que | O que foi confirmado |
|---|---|
| Mantenedora | **Devro LABS** — rodapé literal de `formsubmit.co`, `/documentation` e `/help`: *"Copyright © 2026 Devro LABS \| Privacy"* |
| País | **Sri Lanka**. O registro RDAP público de `formsubmit.co` traz `"cc": "LK"`, região `"Southern"`. O perfil corporativo oficial da Devro LABS no LinkedIn declara sede em **Colombo, LK**, 2 a 10 funcionários, fundada em 2018 |
| Razão social, tipo societário, registro mercantil, endereço | **não confirmado.** Não existe em lugar nenhum do `formsubmit.co` nem do `devrolabs.com`. Todo o registro do domínio está `REDACTED FOR PRIVACY` |
| Documento jurídico | **um único PDF de 2 páginas**, `formsubmit.co/privacy.pdf`, intitulado *"Privacy Policies \| Terms of services"*, com data de vigência de **17 de janeiro de 2019**. Byte-idêntico em todas as capturas do Wayback Machine entre 2019 e 2025 — nunca foi revisado |
| DPA, cláusulas contratuais, contrato assinável | **não existem.** Não há `/terms`, `/dpa`, `/gdpr`, `/legal`. Não há cadastro, login nem clickwrap. O modelo é aceite tácito: *"By using the FormSubmit services you consent to the data practices described in this document"* |
| GDPR, LGPD, DPA no documento | **zero menções às três** |
| Subprocessadores no documento | **zero menções** |
| Retenção no documento jurídico | **zero menções** |

**Eles armazenam as submissões — não é só encaminhamento.** Isso contraria o que o
próprio PDF sugere (*"FormSubmit sends out the information over email"*). A
documentação técnica é explícita:

> *"We retain your form submissions for 30 days. Uploaded files won't retain or can't
> access through the API."* — `formsubmit.co/documentation`

E existe API de leitura pública: `GET /api/get-submissions/<apikey>` devolve o
histórico completo com `form_url`, `form_data` e `submitted_at`, limitada a 5 chamadas
por dia. A chave é obtida por `GET /api/get-apikey/<e-mail>` e enviada ao e-mail
cadastrado.

> **Correção a um documento interno:** o `00-CONSOLIDADO.md` e o `consolidado.html`
> desta pasta de pesquisa afirmam que *"o FormSubmit não tem API de leitura"*. **Está
> errado** — a API existe, é gratuita e devolve 30 dias de histórico. Isso muda o
> desenho proposto da integração com o ClickUp, e é uma informação de retenção que
> precisa entrar no aviso de privacidade.

**A cadeia de subprocessadores, nenhum deles declarado**, levantada por evidência
técnica (DNS, RDAP, cabeçalhos):

- **Cloudflare, Inc.** — registrador, DNS autoritativo, CDN/WAF e recebimento de e-mail
  (MX `route1/2/3.mx.cloudflare.net`);
- **OVH Hosting, Inc. (Montreal, Canadá)** — o host de envio de e-mail. O SPF aponta
  para `mail.safenote.co`, que resolve para `192.99.70.154`, alocado à OVH no ARIN;
- **Google** — reCAPTCHA (o `_captcha=true` que está no `index.html:1197`), Analytics e
  Fonts nas páginas deles.

Ou seja, uma mensagem enviada pelo formulário dela percorre, hoje:
**Sri Lanka → Cloudflare (global) → OVH no Canadá → Gmail (EUA)** — e nenhum desses
saltos está declarado em documento jurídico nenhum.

**Segurança: não há política, nem certificação, nem menção a criptografia.** Não existe
`/security`; o `/.well-known/security.txt` responde 404; não há SOC 2, ISO 27001,
pentest ou bug bounty declarados; os cabeçalhos não trazem HSTS, CSP nem
`Referrer-Policy`. E o endpoint AJAX responde `Access-Control-Allow-Origin: *` —
qualquer origem da internet pode postar no token dela, que é público por definição num
site estático (`script.js:3728`). Na prática, o único freio contra abuso é o reCAPTCHA
e o antispam deles. Isso é um problema de spam na caixa dela, não de vazamento dos
dados de quem preencheu — mas é bom saber que existe.

**O que isso significa para o art. 39 da LGPD.** O artigo manda que *"o operador deverá
realizar o tratamento segundo as instruções fornecidas pelo controlador, que verificará
a observância das próprias instruções"*. Não existe nenhum instrumento entre ela e o
FormSubmit que registre instrução nenhuma. Essa lacuna é real e não tem conserto pelo
lado do FormSubmit — só trocando de fornecedor (5.6) ou aceitando-a de forma
documentada e consciente (5.4 e 9).

### 5.3 Por que a rota das cláusulas-padrão não fecha

A rota "certinha" para operador estrangeiro seria uma destas:

1. **Decisão de adequação** (art. 33, I). Não serve: a ANPD só reconheceu **a União
   Europeia**, pela Resolução CD/ANPD nº 32, de 26 de janeiro de 2026. **Nenhum dos
   países do circuito real do FormSubmit — Sri Lanka, Estados Unidos ou Canadá — tem
   decisão de adequação.** A própria página de Transferência Internacional da ANPD
   registra que, fora a UE, nenhuma decisão sobre cláusulas específicas,
   cláusulas-padrão equivalentes ou normas corporativas globais foi proferida até hoje.

2. **Cláusulas-padrão contratuais** (art. 33, II, "b"). Não serve na prática. O art. 16
   do Regulamento exige *"a adoção integral e sem alteração do texto disponibilizado no
   Anexo II, mediante instrumento contratual firmado entre o exportador e o
   importador"*. Isso significa um contrato assinado entre ela e o FormSubmit, com o
   texto da ANPD, em português, inalterado. Não há com quem assinar: o serviço é
   gratuito, não tem cadastro nem login, não tem razão social publicada, e o único
   documento existente é um PDF de 2019 que ninguém assina (5.2). E o prazo já venceu:
   o art. 2º, parágrafo único da Resolução deu **12 meses contados da publicação** —
   publicada no DOU em 23/08/2024, com retificação em 18/08/2025.

3. **Cláusulas específicas ou normas corporativas globais** (art. 33, II, "a" e "c").
   Exigem aprovação prévia da ANPD, com processo instruído (arts. 21 a 30 do
   Regulamento). Fora de escala para ela por vários graus de magnitude.

4. **Consentimento específico e em destaque para a transferência** (art. 33, VIII).
   Funcionaria juridicamente, mas exige um checkbox só sobre transferência
   internacional, revogável, com ônus de prova dela — o oposto do que ela quer, e
   assustador no formulário.

### 5.4 A saída realista: art. 33, IX

A saída não é um jeitinho — está no texto da lei e é reconhecida pelo Regulamento.

> **LGPD, art. 33, IX** — quando necessário para atender as hipóteses previstas nos
> incisos II, V e VI do art. 7º desta Lei.
>
> **Reg. da Res. 19/2024, art. 9º, II, "c"** — [mecanismo válido:] nas hipóteses
> previstas nos incisos II, "d", e III a IX do art. 33 da Lei nº 13.709.
>
> **Reg. da Res. 19/2024, art. 1º, parágrafo único** — O disposto neste Regulamento não
> exclui a possibilidade da realização de transferência internacional de dados com base
> nos demais mecanismos previstos no art. 33 da Lei nº 13.709 [...] **que não dependam
> de regulamentação**, desde que atendidas as especificidades do caso concreto e os
> requisitos legais aplicáveis.

Encaixando: base legal art. 7º, V → transferência necessária para atender essa hipótese
→ art. 33, IX → mecanismo válido, **sem cláusula-padrão e sem contrato com o
FormSubmit**.

Três condições para esse encaixe se sustentar:

1. **A transferência tem que ser realmente necessária.** É: o formulário só entrega a
   mensagem porque o FormSubmit encaminha. Não há site estático em GitHub Pages que
   receba POST sozinho.
2. **Mínimo necessário.** O art. 9º, parágrafo único do Regulamento manda limitar a
   transferência ao mínimo. Tradução prática: não pedir campo que ela não vai usar.
   Um briefing de 14 campos precisa passar por essa peneira antes de ir ao ar.
3. **Coerência de finalidade.** Se ela usar os dados para mailing, sai do art. 7º, V e
   perde o art. 33, IX junto.

E o art. 4º do Regulamento diz de quem é o dever de verificar isso: *"Cabe ao
controlador verificar [...] se a operação de tratamento: I - caracteriza transferência
internacional de dados; II - submete-se à legislação nacional [...]; e III - está
amparada em hipótese legal e em mecanismo de transferência internacional válidos."*
Dela. Por isso a folha de cinco linhas da seção 2.3.

### 5.5 Um roteiro pronto do que publicar sobre a transferência

O art. 17, §2º do Regulamento está no capítulo das cláusulas-padrão — então, no
caminho do art. 33, IX, ele **não é obrigatório**. Mas é o melhor roteiro oficial que
existe do que dizer ao titular sobre uma transferência internacional, e o §3º permite
integrá-lo *"de forma destacada e de fácil acesso, à Política de Privacidade"*. Ele
manda informar, em português e linguagem simples:

> I - a forma, a duração e a finalidade específica da transferência internacional;
> II - o país de destino dos dados transferidos; III - a identificação e os contatos do
> controlador; IV - o uso compartilhado de dados pelo controlador e a finalidade;
> V - as responsabilidades dos agentes que realizarão o tratamento e as medidas de
> segurança adotadas; e VI - os direitos do titular e os meios para o seu exercício,
> incluindo canal de fácil acesso e o direito de peticionar contra o controlador perante
> a ANPD.

O texto da seção 6 já cobre todos os seis.

### 5.6 Alternativas com sede no Brasil

Resumo honesto: **não existe um "FormSubmit brasileiro".** Nenhum serviço nacional
oferece endpoint POST pronto e gratuito para formulário de site estático. As buscas por
alternativa nacional retornam ou tutoriais usando o próprio FormSubmit, ou
concorrentes igualmente estrangeiros (Formspree, Formcarry, Getform, FormKeep,
StaticForms).

O que existe, verificado em fonte primária:

| Serviço | Empresa BR | CNPJ | Dados no Brasil | Contrato de operador em PT-BR | Preço | Serve? |
|---|---|---|---|---|---|---|
| **KingHost** (grupo LWSA) | sim | 02.351.877/0010-43 | **sim** — *"servidores 100% no Brasil"* | sim | R$ 10–20/mês | sim, via PHP |
| **Locaweb Cloud** | sim | 02.351.877/0001-52 | **sim** — datacenter no Brasil | sim | R$ 20–320/mês | sim, via VM |
| **Azion** | sim | 12.447.998/0001-56 | **não garantido** — *"Data may be processed in globally distributed data centers"* | **sim, e publica as cláusulas-padrão da ANPD em português** | franquia mensal generosa | sim, via Edge Function |
| **Magalu Cloud** | sim | não confirmado | **sim** — regiões `br-se1` e `br-ne1` | não confirmado | não publicado | só via VM (não tem serverless) |
| **RD Station** | sim | 13.021.784/0001-86 | **não** — *"Califórnia e Iowa, nos Estados Unidos"* | sim, DPA explícito e lista de suboperadores | R$ 50–1.699/mês | parcialmente |
| **Umbler** | sim | 30.655.874/0001-48 | não confirmado | não confirmado | R$ 24–270/mês | sim, via PHP |
| **Pipefy** | **não** — Delaware, EUA | — | — | — | — | **descartar** |

Três leituras:

- **Se o objetivo for fechar os três requisitos — empresa brasileira, dados no Brasil e
  contrato de operador — o arranjo mais barato é KingHost (~R$ 10/mês) com um
  `contato.php` de umas 30 linhas** recebendo o POST vindo do GitHub Pages, com
  `Access-Control-Allow-Origin` restrito ao domínio dela, honeypot e limite de taxa. O
  custo real não é o dinheiro: é que o site deixa de ser 100% estático na prática, e
  passa a existir código de servidor para ela manter. Contra o princípio que rege este
  projeto.
- **Se o objetivo for apenas ter um operador com CNPJ acionável no Brasil** (o buraco
  do art. 39 apontado em 5.2), sem se importar com onde o dado é processado, a **Azion**
  resolve com menos trabalho — é a única que publica as cláusulas-padrão da ANPD em
  português e se declara operadora.
- **Não existe opção gratuita brasileira.** O piso realista é R$ 10/mês.

Recomendação: **não trocar agora.** A saída do art. 33, IX (5.4) é juridicamente
suficiente, e trocar de fornecedor introduz código de servidor, custo mensal e uma
superfície nova de manutenção para resolver um risco que, no porte dela, é baixo
(seção 9). Vale reavaliar se um dia o volume crescer, se ela passar a coletar dado
sensível, ou se um cliente corporativo exigir contrato de tratamento — aí a Azion ou a
KingHost entram.

**Lacunas desta pesquisa:** UOL Host, Mandaê e Zeev não foram investigados; a
confirmação literal de que a Azion Functions expõe endpoint HTTP com Fetch API e o CNPJ
da Magalu Cloud em fonte primária ficaram **não confirmados** (o orçamento de buscas da
sessão esgotou).

### 5.7 Uma coisa que ela pode fazer hoje, de graça

O GitHub Pages é operador estrangeiro do mesmo jeito, e recebe o IP de **todo**
visitante — não só de quem envia formulário. Trocar de hospedagem por causa disso seria
desproporcional. Mas os quatro `preconnect` do `index.html:44–47` entregam o IP do
visitante ao Google **antes de qualquer clique**, sem necessidade nenhuma, e são
redundantes com o `warmConnections()` da própria biblioteca. Tirar essas quatro linhas
e as duas de `doubleclick` em `lite-yt-embed.js:118–119` é a única coisa nesta pesquisa
que **reduz coleta de fato**, em vez de só documentá-la. Custa seis linhas.

---

## 6. Texto pronto do aviso de privacidade

Para virar `politica-privacidade.html`. Os únicos marcadores são os dois dados que só
ela tem: `[E-MAIL]` e, se ela tiver MEI, `[CNPJ]` (se não tiver, é só apagar a linha).

---

### Política de Privacidade

**Última atualização: [DATA DE PUBLICAÇÃO]**

Este site é meu portfólio profissional. Se você me mandou uma mensagem ou preencheu um
briefing, alguns dados seus passaram por aqui. Esta página explica quais, para quê, por
quanto tempo, e como pedir que eu apague.

Está escrito em português normal de propósito.

#### Quem sou eu

Savylla Adryan, profissional autônoma de audiovisual, no Rio de Janeiro, RJ.
[CNPJ — só se ela tiver MEI; se não tiver, apagar esta linha inteira]

Sou a **controladora** dos dados tratados neste site — quem decide o que é coletado e
por quê. É comigo que você fala sobre eles.

**Contato para qualquer assunto de dados pessoais: [E-MAIL]**

Este é o canal oficial. Não tenho encarregado (DPO) designado, porque a lei dispensa
disso quem é agente de tratamento de pequeno porte, como eu — Resolução CD/ANPD nº
2/2022, art. 11. Em lugar do encarregado, existe este e-mail, e ele funciona.

#### O que eu coleto

**No formulário de contato:** seu nome, seu e-mail, o assunto e a mensagem.

**No formulário de briefing:** seu nome, e-mail, WhatsApp, marca ou empresa, a descrição
do projeto, o prazo, a verba pretendida e os links de material que você me mandar.

Nada além disso. Não peço documento, não peço endereço, não peço data de nascimento.

**Só coleto quando você preenche e envia.** Não há formulário que salve enquanto você
digita.

#### Para que eu uso

Para uma coisa: **responder você e tocar o projeto.** Ler o que você precisa, tirar
dúvida, montar orçamento, negociar, e, se a gente fechar, produzir.

Não uso para mais nada. Não mando newsletter. Não faço disparo em massa. Não vendo,
não alugo e não passo seus dados para ninguém comprar.

#### Com que base legal

Com base no **art. 7º, inciso V da LGPD** (Lei 13.709/2018): tratamento necessário para
a execução de contrato ou de procedimentos preliminares relacionados a contrato, **a
pedido do titular**.

Em português: você me procurou pedindo um orçamento. Tratar seus dados para responder
é parte de atender esse pedido. É por isso que não tem caixinha de "eu concordo" — não
porque eu pulei a etapa, mas porque a base legal aqui não é consentimento.

#### Por onde seus dados passam

Preciso ser honesta sobre isto, porque envolve empresas fora do Brasil.

**FormSubmit** — é o serviço que recebe o formulário e me encaminha por e-mail. Um
site estático como este não consegue receber mensagem sozinho; sem esse intermediário,
o formulário não existe. Ele atua como **operador**: trata os dados em meu nome e só
para encaminhar. É mantido pela Devro LABS, com sede no **Sri Lanka**, e a
infraestrutura dele passa por **Cloudflare** e por um servidor de e-mail no **Canadá**.
O FormSubmit guarda uma cópia da submissão por **30 dias** e depois descarta.

**Google (Gmail)** — é onde a mensagem chega e fica guardada comigo. Estados Unidos.

**GitHub Pages** — é onde este site está hospedado. Como qualquer hospedagem, os
servidores registram o endereço de IP e o navegador de quem acessa, em logs técnicos.
Isso vale para toda visita, mesmo sem preencher nada. Estados Unidos.

**YouTube e Instagram** — os vídeos e posts do portfólio ficam nessas plataformas e só
são carregados **depois que você clica** para assistir. Quando você clica, seu
navegador se conecta ao YouTube ou ao Instagram, e essas empresas passam a enxergar seu
acesso, sob as políticas de privacidade delas. Se você não clicar em nenhum vídeo, isso
não acontece.

**WhatsApp** — se você me passou seu número no briefing, é bem provável que a gente
continue a conversa por lá, porque é como eu trabalho. Nesse caso, o histórico da nossa
conversa fica no WhatsApp, que é da Meta, sob as regras deles. Se você preferir tratar
tudo por e-mail, é só me dizer.

**Sobre a transferência internacional:** nenhum desses países tem decisão de adequação
reconhecida pela ANPD — hoje só a União Europeia tem. A transferência é feita com
fundamento no **art. 33, inciso IX da LGPD**, que a permite quando ela é necessária
para atender às hipóteses do art. 7º, V — exatamente o caso aqui: sem esse envio, a sua
mensagem não chega até mim. Limito essa transferência ao mínimo necessário: só vai o
que você escreveu no formulário, nada além.

#### Cookies

**Este site não usa cookies.** Não tenho Google Analytics, não tenho pixel do
Facebook, não tenho nenhuma ferramenta de rastreamento ou medição. O site também não
guarda nada na memória do seu navegador.

As únicas exceções são os players de vídeo do YouTube e do Instagram: se você clicar
para assistir, essas plataformas podem gravar cookies próprios delas no seu navegador.
Isso é decisão delas, sob as políticas delas — e só acontece se você clicar.

#### Por quanto tempo eu guardo

| O que | Quanto tempo |
|---|---|
| Mensagem do formulário de contato que não virou projeto | 6 meses depois da última resposta |
| Briefing de projeto que não fechou | 12 meses depois da última conversa |
| Dados de projeto que fechou | 5 anos depois de entregue |

O prazo de 5 anos existe porque, depois de um trabalho contratado, ainda posso precisar
comprovar o que foi combinado — nota fiscal, cobrança, ou defesa em alguma discussão.
Passado o prazo, eu apago.

Se você pedir para apagar antes, eu apago antes. Ver logo abaixo.

#### Seus direitos

A LGPD, no art. 18, te dá o direito de, a qualquer momento, me pedir:

- **confirmação** de que eu tenho dados seus;
- **acesso** a esses dados;
- **correção** do que estiver errado, incompleto ou desatualizado;
- **anonimização, bloqueio ou eliminação** de dado desnecessário ou excessivo;
- **portabilidade** dos dados para outro fornecedor;
- **eliminação** dos dados;
- **informação** sobre com quem eu compartilhei;
- **oposição** ao tratamento, se você achar que ele está em desacordo com a lei.

**Como pedir:** manda um e-mail para **[E-MAIL]** dizendo o que você quer. Não precisa
de formulário, nem de linguagem formal, nem de justificativa. "Apaga meus dados" basta.

**É de graça**, sempre.

**Prazo:** respondo o mais rápido que der. Para pedidos de acesso, a lei me dá até 15
dias (art. 19, I da LGPD combinado com o art. 15 da Resolução CD/ANPD nº 2/2022). Como
agente de tratamento de pequeno porte, tenho prazo em dobro nos demais casos (art. 14
da mesma Resolução) — mas na prática eu respondo bem antes disso.

Uma ressalva sincera: se você me pedir para apagar tudo no meio de um projeto em
andamento, eu vou apagar, mas provavelmente não vou conseguir continuar o trabalho.
A gente conversa antes.

#### Segurança

O que eu faço, na prática: o site inteiro roda em HTTPS; as mensagens chegam numa conta
de e-mail com verificação em duas etapas; e sou a única pessoa com acesso a elas.

Nenhuma medida é infalível. Se acontecer um incidente de segurança que possa causar
risco relevante a você, eu comunico você e a ANPD, como manda o art. 48 da LGPD.

#### Se você não ficar satisfeita

Fala comigo primeiro, em **[E-MAIL]** — quase tudo se resolve aí.

Se não resolver, você tem o direito de reclamar diretamente à **Autoridade Nacional de
Proteção de Dados (ANPD)**, em **gov.br/anpd**. Esse direito está no art. 18, §1º da
LGPD e não depende de nada que eu diga.

#### Mudanças nesta página

Se eu mudar alguma coisa aqui, a data lá em cima muda junto. Se a mudança for
significativa, aviso quem estiver com projeto em andamento.

---

## 7. Microcopy do formulário

**Debaixo do botão de envio** (uma linha, cinza, tamanho pequeno):

> Seus dados são usados só para eu responder e tocar o projeto. Nada de newsletter.
> [Como eu trato seus dados](politica-privacidade.html)

Alternativa mais curta, se a primeira ficar comprida no mobile:

> Uso seus dados só para responder você. [Política de privacidade](politica-privacidade.html)

**No rodapé, ao lado dos outros links** (`index.html:1230–1236` e o mesmo bloco em
`servicos.html`):

> Privacidade

**Na página `obrigado.html`**, uma linha discreta ao pé:

> Se quiser que eu apague o que você mandou, é só escrever para [E-MAIL].

**No aviso de privacidade, no bloco do canal do titular** — já está redigido na
seção 6, mas isolado para facilitar o copy-paste:

> **Contato para qualquer assunto de dados pessoais: [E-MAIL]**
> Manda um e-mail dizendo o que você quer. Não precisa de formulário nem de
> justificativa. "Apaga meus dados" basta. É de graça, sempre.

Três coisas que **não** devem entrar nesse microcopy: a palavra "consentimento" (não é
a base legal usada), a expressão "ao enviar você concorda com" (isso simula
consentimento onde ele não existe, e piora a situação jurídica em vez de melhorar), e
qualquer checkbox obrigatório de aceite (com base no art. 7º, V ele é desnecessário e
atrapalha a conversão).

---

## 8. Retenção: quanto tempo guardar o quê

A LGPD **não fixa prazo em número**. O que ela fixa é o gatilho:

> Art. 15. O término do tratamento de dados pessoais ocorrerá nas seguintes hipóteses:
> I - verificação de que a finalidade foi alcançada ou de que os dados deixaram de ser
> necessários ou pertinentes ao alcance da finalidade específica almejada; II - fim do
> período de tratamento; III - comunicação do titular [...]

> Art. 16. Os dados pessoais serão eliminados após o término de seu tratamento, no
> âmbito e nos limites técnicos das atividades, autorizada a conservação para as
> seguintes finalidades: I - cumprimento de obrigação legal ou regulatória pelo
> controlador; II - estudo por órgão de pesquisa [...]; III - transferência a terceiro
> [...]; ou IV - uso exclusivo do controlador, vedado seu acesso por terceiro, e desde
> que anonimizados os dados.

Repare no que **não** está na lista do art. 16: "guardar por via das dúvidas". Depois
que a finalidade acaba, a regra é eliminar.

Os prazos abaixo são **recomendação**, não texto de lei. Ela pode ajustar, desde que
escolha um número, escreva no aviso e cumpra.

| O que | Prazo sugerido | Por quê |
|---|---|---|
| Mensagem de contato que não virou nada | **6 meses** após a última resposta | a finalidade (responder) já se esgotou; 6 meses cobrem a pessoa que some e volta |
| Briefing de quem não fechou | **12 meses** após a última conversa | projeto de audiovisual que "morreu" costuma voltar dentro de um ciclo anual; passou disso, virou prospecção — e prospecção não cabe no art. 7º, V |
| Projeto que fechou | **5 anos** após a entrega | conservação para exercício regular de direitos: comprovar o que foi combinado, cobrar, ou se defender. Cai no art. 16, I combinado com o art. 7º, VI. **O número 5 não vem da LGPD** — vem do prazo geral de cobrança de dívida em instrumento particular do Código Civil (art. 206, §5º, I). Se ela preferir 3 anos, também é defensável |
| Pedido de eliminação do titular | **imediato**, na prática em dias | art. 15, III e art. 18, IV/VI |

**Onde apagar de verdade.** Este é o detalhe operacional que costuma furar:

1. **O Gmail é o banco de dados real.** "Apagar o briefing" significa apagar o e-mail
   **e esvaziar a lixeira** do Gmail, que retém itens excluídos por um período próprio.
2. **O FormSubmit guarda uma cópia por 30 dias.** Isso está na documentação técnica
   deles, não no documento jurídico (seção 5.2), e é acessível por API. Ela não tem
   como apagar essa cópia antecipadamente — não há painel nem endpoint de exclusão.
   Se um titular pedir eliminação nos primeiros 30 dias, o correto é apagar o que está
   sob controle dela e informar, com honestidade, que a cópia do operador expira em até
   30 dias da submissão. O aviso da seção 6 já declara esse prazo, o que evita a
   surpresa.
3. **A conversa no WhatsApp também é dado.** Se o projeto migrou para o WhatsApp, o
   histórico lá tem os mesmos dados. Apagar de um lado só não é apagar.
4. **Backups e exportações.** Se ela tiver o hábito de exportar e-mails ou usar cliente
   local, o dado está lá também.

Uma rotina de 15 minutos, duas vezes por ano, buscando por remetente e data no Gmail,
resolve praticamente tudo isso.

### Sobre o WhatsApp

Ela responde cliente por WhatsApp, e o briefing vai coletar o número. Isso muda três
coisas, nenhuma delas dramática:

1. **O número de WhatsApp é dado pessoal** como qualquer outro. Entra no aviso de
   privacidade (já entrou, seção 6) e no mesmo regime de retenção.
2. **A conversa é um banco de dados que ela controla.** Briefing detalhado, verba,
   contrato — muita coisa acaba morando lá. Quando ela apagar os dados de alguém,
   precisa lembrar do WhatsApp.
3. **O WhatsApp é mais uma empresa estrangeira no circuito.** O WhatsApp LLC é
   controlador dos dados dos próprios usuários — a ANPD já se manifestou sobre isso
   ao analisar a política de privacidade da plataforma e o compartilhamento com a
   Meta. Não é ela quem responde pelo que a Meta faz com os dados de conta de usuário.
   Ela responde pelo conteúdo da conversa que ela mesma conduz e guarda.

Recomendação prática: usar o WhatsApp normalmente, mencioná-lo no aviso de privacidade
como canal de atendimento (já mencionado, via campo do briefing), e não fazer disparo
em lista. Disparo em lista é outro tratamento, com outra finalidade, e sai do art. 7º, V.

---

## 9. Risco real, dimensionado

Resumo em uma frase: **o risco de multa contra ela é, na prática, próximo de zero — e o
que o torna não-nulo não é errar no formulário, é ignorar a ANPD.**

### 9.1 O que a ANPD de fato já fez

A ANPD pode sancionar desde 01/08/2021. De lá até hoje (13/08/2026), pela própria
página oficial de Decisões em Processos Sancionadores, ela **concluiu 9 processos
administrativos sancionadores**. Um foi arquivado; oito viraram sanção:

| Sancionado | Data | Sanção |
|---|---|---|
| **Telekall Inforservice** (microempresa) | 06/07/2023 | advertência + **multa de R$ 14.400** |
| Jardim Botânico do RJ | 06/10/2023 | **arquivado** |
| IAMSPE (SP) | 06/10/2023 | advertência + medida corretiva |
| Secretaria de Saúde de Santa Catarina | 18/10/2023 | 2 advertências + medida corretiva |
| Secretaria de Educação do DF | 31/01/2024 | 4 advertências |
| **INSS** | 01/02/2024 | publicização da infração + medida corretiva |
| Secretaria de Desenv. Social de PE | 25/04/2024 | advertência + medidas corretivas |
| Ministério da Saúde | 09/08/2024 | advertências + medidas corretivas |
| Ministério da Saúde | 06/11/2024 | advertências + medidas corretivas |

**Em cinco anos de poder sancionatório, a ANPD aplicou exatamente uma multa pecuniária:
R$ 14.400, contra a Telekall, em 2023.** Não é retórica — é o resultado de varredura no
DOU filtrando por órgão e pelos termos "multa", "advertência" e "sancionador".

Há uma razão estrutural: **oito dos nove alvos são do setor público, e a LGPD proíbe
multar o poder público.** O art. 52, §3º só autoriza contra órgãos públicos as sanções
dos incisos I, IV, V, VI, X, XI e XII — multa (II e III) está fora.

E o volume põe isso em escala. A ANPD recebeu 768 requerimentos em 2021, 1.047 em 2022,
1.137 em 2023 e 4.029 em 2024 — quase **7 mil requerimentos acumulados**, contra
**9 processos concluídos e 1 multa**.

### 9.2 Existe caso contra alguém do porte dela? Não.

Não há **nenhuma** sanção da ANPD contra pessoa física autônoma, MEI ou site pessoal.
As listas oficiais de processos sancionadores, fiscalização e monitoramento são
compostas por órgãos públicos (INSS, Ministério da Saúde, secretarias estaduais) e por
empresas grandes: Meta, Google, OpenAI, TikTok, X, Telegram, Uber, iFood, Serasa,
bancos, varejistas e clubes de futebol da Série A.

O caso mais próximo de "agente pequeno" é justamente a Telekall — e vale entender por
que ela foi punida, porque isso desenha o contorno do risco real. A Telekall era uma
microempresa que **vendia lista de contatos de WhatsApp de eleitores** para campanha
eleitoral, e **não respondeu à ANPD**. As duas multas de R$ 7.200 foram por tratar
dados sem base legal (art. 7º) e por obstruir a fiscalização (art. 5º do Regulamento de
Fiscalização). A falta de encarregado (art. 41) rendeu só advertência.

Ou seja: não foi punida por ter formulário sem política de privacidade. Foi punida por
comercializar dados de terceiros e por ignorar a autoridade.

### 9.3 Como um processo nasce — e quantos avisos vêm antes

A norma é a **Resolução CD/ANPD nº 1, de 28 de outubro de 2021** (Regulamento do
Processo de Fiscalização e do Processo Administrativo Sancionador), alterada pela
Resolução nº 4/2023. Pontos que importam:

- **A fiscalização tem quatro modos** (art. 15): monitoramento, orientação, prevenção e
  — só então — repressão.
- **Denúncia isolada normalmente não vira processo.** Os arts. 24 a 26 determinam que
  *"os requerimentos serão analisados de forma agregada"*; análise individualizada é
  excepcional e exige decisão motivada.
- **Antes de qualquer sanção existem medidas que não são sanção** (arts. 29 a 32):
  aviso, solicitação de regularização, plano de conformidade. Cabe também termo de
  ajustamento de conduta (art. 43).
- **Se virar processo, há auto de infração e 10 dias úteis de defesa** (arts. 45 a 47).

E a frase mais importante desta seção inteira está escrita pela própria ANPD, na página
oficial de fiscalização:

> *"até o momento, todos os processos sancionadores conduzidos pela ANPD, sem exceção,
> foram instaurados em decorrência de postura não colaborativa do regulado."*

### 9.4 Se o pior acontecesse, quanto seria

Existe regulamento de dosimetria: **Resolução CD/ANPD nº 4, de 24 de fevereiro de
2023**. Para pessoa natural:

- **A base de cálculo não é o faturamento dela** — o art. 11, §1º, IV, "d" define, para
  pessoa natural, o *"somatório dos rendimentos recebidos referentes a atividades de
  tratamento de dados pessoais"*. No caso dela, isso é próximo de nada: ela não ganha
  dinheiro tratando dados, ganha filmando.
- **Pisos do Apêndice II, Tabela 1, para pessoa natural:** infração leve **R$ 1.000**,
  média **R$ 2.000**, grave **R$ 4.000**.
- **Advertência é a regra** para infração leve ou média sem reincidência (art. 9º). A
  multa só entra quando (i) o infrator não atendeu medida preventiva ou corretiva,
  (ii) a infração é grave, ou (iii) nenhuma outra sanção serve (art. 10).
- **Atenuantes que ela alcança sem esforço** (art. 13): **−75%** se cessar a infração
  antes mesmo do procedimento preparatório; **−20%** por política de boas práticas e
  governança; **−5%** por cooperação e boa-fé. Somam.
- **Pequeno porte ganha prazo em dobro para pagar** (art. 17, §2º) — e essa é a única
  menção a pequeno porte em todo o regulamento de dosimetria. **Não existe faixa de
  multa reduzida específica para pequeno porte.** A atenuação vem por outra via: o
  critério legal de *"condição econômica do infrator"* (art. 52, §1º, IV da LGPD), a
  base de cálculo por rendimentos e os pisos menores da Tabela 1.
- O art. 27 permite à ANPD **afastar a metodologia** quando o resultado for
  desproporcional.

Sobre o teto de R$ 50 milhões do art. 52, II: ele é irrelevante aqui. A multa é *"de até
2% do faturamento da pessoa jurídica de direito privado"*, e o limite de R$ 50 milhões é
um teto, não um valor. Para pessoa natural sem rendimento de tratamento de dados, o
número que importa é o piso de R$ 1.000 a R$ 4.000.

### 9.5 O que efetivamente move a agulha

Três comportamentos tiram um caso da estatística e o colocam em processo:

1. **Tratar dados sem base legal declarada.** A Res. 4/2023, art. 8º, classifica isso
   como infração **grave** — e infração grave dispensa a escada e vai direto para
   multa (art. 10). É exatamente o que o item 2 do checklist resolve.
2. **Fazer marketing ou comércio com dados de terceiros.** Foi o que derrubou a
   Telekall.
3. **Não responder a um ofício da ANPD.** É infração autônoma (art. 5º do Regulamento
   de Fiscalização) e valeu metade da multa da Telekall. Se algum dia chegar um e-mail
   da ANPD, responder é a única coisa que ela precisa acertar.

### 9.6 O veredito honesto

**Não é "você vai ser multada".** A ANPD nunca sancionou ninguém do porte dela, nunca
multou pessoa física, e declara por escrito que só processa quem não colabora. O rito
tem aviso, pedido de regularização e plano de conformidade antes de qualquer auto de
infração. Com quase 7 mil requerimentos e 9 processos, a probabilidade estatística de
um portfólio individual virar processo é desprezível.

**E também não é "não precisa se preocupar".** O risco relevante não é a ANPD — é mais
mundano: um cliente corporativo que peça a política de privacidade antes de fechar
contrato e não a encontre; um titular irritado que pede exclusão e não recebe resposta,
porque não existe canal; e o fato, incômodo, de que **hoje já existe coleta acontecendo
sem aviso** — o que é descumprimento do art. 9º agora, mesmo que ninguém esteja
olhando.

O trabalho para sair dessa situação é de uma tarde: uma página HTML, um link no rodapé,
uma linha embaixo do botão e duas entradas num workflow. O custo de fazer é tão baixo
que discutir probabilidade de multa é quase acadêmico — a razão para fazer é que é
barato e correto, não que a ANPD esteja vindo.

---

## 10. Checklist de implementação

Em ordem. Os quatro primeiros resolvem o essencial e cabem em uma tarde.

1. **Decidir e anotar o e-mail do canal do titular.** Pode ser o mesmo Gmail que já
   recebe o formulário. Só precisa ser um endereço que ela lê. Sem isso, nada abaixo
   funciona. E confirmar para onde o `FORMSUBMIT_TOKEN` encaminha hoje — isso não está
   no código, só o FormSubmit sabe (seção 5.1).

   **Ligar a verificação em duas etapas nessa conta de e-mail, se ainda não estiver.**
   O aviso de privacidade da seção 6 afirma que ela existe. Uma declaração de segurança
   falsa é pior do que nenhuma: vira prova contra ela se houver incidente. Ou liga, ou
   apaga a frase.

2. **Criar `politica-privacidade.html`** com o texto da seção 6, substituindo `[E-MAIL]`,
   `[DATA DE PUBLICAÇÃO]` e `[CNPJ]` (ou apagando a linha do CNPJ). Usar o mesmo
   cabeçalho, rodapé e CSS das outras páginas. A CSP dessa página pode ser a mais
   fechada do site — copiar a de `servicos.html:35`, que já está em `frame-src 'none'`
   e `form-action 'none'`, porque a página não tem vídeo nem formulário.

3. **Registrar `politica-privacidade.html` no workflow de deploy — em dois lugares.**
   O `.github/workflows/deploy-pages.yml` monta o artefato por **lista de inclusão**, e
   a página nova precisa entrar nas duas listas:
   - no `on.push.paths` (linhas 10–20), senão editar a política **não dispara deploy
     nenhum** e a alteração fica só no repositório;
   - na linha do `cp` que monta o `_site` (linha 51), senão o arquivo **não vai para o
     ar** — e, pior, se for adicionado ao `paths` mas não ao `cp`, o site publica sem
     ela em silêncio.

   Este é o passo mais fácil de esquecer e o mais silencioso quando falha. O comentário
   do próprio workflow avisa: *"Se algum arquivo da lista desaparecer, o cp falha e o
   deploy para aqui."*

4. **Adicionar o link "Privacidade" no rodapé** do `index.html` (bloco
   `footer__nav`, linhas 1230–1236) e no rodapé equivalente do `servicos.html`.

5. **Adicionar a linha de microcopy** (seção 7) logo abaixo do botão do `#contatoForm`
   em `index.html:1219`.

6. **Remover os quatro `preconnect` do `index.html:44–47`.** São conexões a servidores
   do Google disparadas em toda visita, sem interação, e redundantes com o
   `warmConnections()` da `lite-yt-embed.js`. Medir o LCP antes e depois — se piorar
   de forma perceptível, manter só o `youtube-nocookie.com` e declarar isso no aviso.

7. **Remover as duas linhas de `doubleclick` em `assets/lib/lite-yt-embed.js:118–119`.**
   O próprio comentário do upstream, na linha 117, admite que não sabe se são
   necessárias. Registrar essa remoção junto dos dois patches locais que a biblioteca
   já carrega, para não voltarem numa atualização.

8. **Preencher o registro simplificado de operações** com o modelo ROPA da ANPD para
   pequeno porte (link na seção 11). Duas linhas: "formulário de contato" e "formulário
   de briefing". Guardar fora do repositório público — é documento dela, não conteúdo
   do site. Sugestão: junto do `.env`, na pasta gitignorada.

9. **Escrever a folha de meia página do art. 4º do Reg. da Res. 19/2024**: existe
   transferência internacional, hipótese legal é o art. 7º, V, mecanismo é o art. 33,
   IX, e a transferência é necessária porque um site estático não recebe POST sozinho.
   Mesmo lugar do item 8.

10. **Peneirar os 14 campos do briefing pelo princípio da necessidade** (art. 6º, III e
    art. 9º, parágrafo único do Reg. da Res. 19/2024) antes de publicar. Para cada
    campo, a pergunta é: se ela não responder, eu deixo de conseguir orçar? Se não
    deixo, o campo é opcional ou sai.

11. **Ao publicar o `briefing.html`**, repetir nele o link para a política e a linha de
    microcopy, e incluir a página nas **duas** listas do workflow (item 3). A CSP dele precisa
    nascer com `connect-src 'self' https://formsubmit.co` e
    `form-action https://formsubmit.co` — a de `servicos.html` está em
    `form-action 'none'` e faria o envio falhar em silêncio.

12. **Marcar duas datas no calendário por ano** para a limpeza de retenção descrita na
    seção 8: Gmail (incluindo lixeira) e WhatsApp.

13. **Se um dia ela quiser analytics:** reler a seção 4 antes. Analytics cria a
    obrigação de banner de consentimento que hoje ela não tem. Se for indispensável,
    procurar opção sem cookie e sem identificação individual — mas isso é outra
    pesquisa, e não confirmei nenhuma ferramenta específica aqui.

---

## 11. Fontes

### Lei

| Fonte | O que confirma |
|---|---|
| [Lei nº 13.709/2018 (LGPD) — Planalto](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm) | texto integral. Arts. 3º, 4º, 5º, 6º, 7º, 9º, 10, 15, 16, 18, 19, 33 a 37, 41, 48 e 52 lidos no original e citados literalmente neste documento |

Dispositivos usados, para conferência rápida: **art. 3º** (aplicação territorial);
**art. 4º, I** (exclusão de uso particular e não econômico); **art. 5º, I/VI/VII/X**
(dado pessoal, controlador, operador, tratamento); **art. 6º, III/VI/VII/X**
(necessidade, transparência, segurança, responsabilização); **art. 7º, I/V/IX** (bases
legais); **art. 9º, I–VII** (informação ao titular); **art. 10, §§1º a 3º** (legítimo
interesse — o artigo tem três parágrafos, não quatro); **arts. 15 e 16** (término e
eliminação); **art. 18, I–IX e §§1º a 5º** (direitos); **art. 19, I** (declaração
simplificada); **art. 33, I/II/VIII/IX** (transferência internacional); **arts. 34 a
36**; **art. 37** (registro de operações); **art. 41** (encarregado); **art. 52**
(sanções).

### Resoluções da ANPD (todas lidas no original)

| Fonte | O que confirma |
|---|---|
| [Resolução CD/ANPD nº 2, de 27/01/2022 — agentes de pequeno porte](https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no-2-de-27-de-janeiro-de-2022) | art. 2º, I (pessoas naturais entram); art. 3º (exclusões); art. 4º (alto risco, critérios cumulativos); art. 7º (**não** dispensa o art. 9º da LGPD); art. 9º (registro simplificado); art. 11 e §§ (dispensa de encarregado, canal obrigatório, boas práticas); art. 13 (política simplificada); art. 14 (prazo em dobro); art. 15 (15 dias); art. 6º e 16 (limites da dispensa) |
| [Resolução CD/ANPD nº 19, de 23/08/2024 — transferência internacional e cláusulas-padrão](https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no-19-de-23-de-agosto-de-2024) | art. 1º da Resolução (regula o art. 33, **I e II** apenas); art. 2º, par. único (prazo de 12 meses); Anexo I art. 1º par. único, art. 3º, art. 4º, art. 5º, art. 6º, art. 9º, art. 16, art. 17. Publicada no DOU de 23/08/2024, com retificação de 18/08/2025 |
| [Resolução CD/ANPD nº 18, de 16/07/2024 — atuação do encarregado (DOU)](https://www.in.gov.br/en/web/dou/-/resolucao-cd/anpd-n-18-de-16-de-julho-de-2024-572632074) | art. 3º, §3º: preserva expressamente a dispensa do pequeno porte, remetendo ao art. 11 da Res. 2/2022; arts. 8º e 9º (divulgação da identidade e contato do encarregado, para quem tem) |
| [Resolução CD/ANPD nº 1, de 28/10/2021 — Regulamento do Processo de Fiscalização e do Processo Administrativo Sancionador](https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no1-2021) | art. 5º (não responder à ANPD é infração autônoma); art. 15 (quatro modos de fiscalização); arts. 24–26 (requerimentos analisados *"de forma agregada"*); arts. 29–32 (orientação e prevenção antes da repressão); art. 43 (TAC); arts. 45–47 (auto de infração, 10 dias úteis de defesa). Alterada pela Res. 4/2023 |
| [Resolução CD/ANPD nº 4, de 24/02/2023 — Regulamento de Dosimetria e Aplicação de Sanções Administrativas](https://www.in.gov.br/en/web/dou/-/resolucao-cd/anpd-n-4-de-24-de-fevereiro-de-2023-466146077) · [versão certificada em PDF, com os Apêndices](https://dspace.mj.gov.br/bitstream/1/9179/1/RES_ANPD_2023_4.pdf) | art. 8º (leve/média/grave; tratar sem base legal é grave); art. 9º (advertência é a regra); art. 10 (quando cabe multa); art. 11, §1º, IV, "d" (base de cálculo para pessoa natural); art. 12 (agravantes); art. 13 (atenuantes de −75% a −5%); art. 17, §2º (prazo em dobro para pequeno porte pagar); art. 27 (afastar a metodologia). **Apêndice II, Tabela 1** (pisos para pessoa natural: R$ 1.000 / 2.000 / 4.000) só existe no PDF certificado — o HTML do DOU omite os apêndices |
| [Resolução CD/ANPD nº 15, de 24/04/2024 — Comunicação de Incidente de Segurança](https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd) | existência e ementa confirmadas na lista oficial |
| [Resolução CD/ANPD nº 32, de 26/01/2026 — adequação da União Europeia](https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd) | *"Dispõe sobre o reconhecimento da União Europeia como organismo internacional com grau de proteção de dados pessoais adequado"*. É a única decisão de adequação existente |
| [Lista oficial de regulamentações da ANPD](https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd) | conferência dos números e datas de todas as resoluções acima |

### Guias e materiais oficiais da ANPD

| Fonte | O que confirma |
|---|---|
| [Guia Orientativo — Hipóteses legais de tratamento: Legítimo Interesse (fev/2024, 53 p.)](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia_legitimo_interesse.pdf) | teste de balanceamento é *"boa prática e medida recomendável"* e *"ferramenta essencial para demonstrar a conformidade"* (art. 6º, X e art. 37); o modelo do Anexo II *"não é de uso obrigatório"*; o teste *"pode ser breve ou simplificado"* em baixo impacto; reforço de transparência e de registro no legítimo interesse (art. 10, §§1º e 2º) |
| [Guia Orientativo — Cookies e Proteção de Dados Pessoais (out/2022, 40 p.)](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-cookies-e-protecao-de-dados-pessoais.pdf) | classificação de cookies necessários x não necessários; *"exibir anúncios ou outros conteúdos incorporados"* é não necessário; *"inexiste hierarquia ou preferência entre as hipóteses legais"*; consentimento *"não é apropriado"* para o que é essencial ao serviço pedido; diferença entre banner e política de cookies |
| [Guia + Checklist + modelo de ROPA para agentes de tratamento de pequeno porte](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-sobre-seguranca-da-informacao-para-agentes-de-tratamento-de-pequeno-porte) | a ANPD publica modelo pronto de registro de operações (xlsx e pdf) e checklist de segurança para pequeno porte — é o material que atende ao art. 9º, par. único da Res. 2/2022 |
| [Transferência Internacional de Dados — ANPD](https://www.gov.br/anpd/pt-br/assuntos/assuntos-internacionais/transferencia-internacional-de-dados) | a UE é o único reconhecimento de adequação; **os EUA não têm decisão de adequação**; nenhuma cláusula específica, cláusula-padrão equivalente ou norma corporativa global foi aprovada até hoje |
| [ANPD — análise do compartilhamento de dados entre WhatsApp e Meta](https://www.gov.br/anpd/pt-br/assuntos/noticias/anpd-conclui-a-analise-sobre-compartilhamento-de-dados-pessoais-entre-whatsapp-e-meta) | o WhatsApp LLC é controlador dos dados dos usuários da plataforma; a Meta atua ora como operadora, ora como controladora |

### Fiscalização e sanções (fontes oficiais)

| Fonte | O que confirma |
|---|---|
| [ANPD — Decisões em Processos Sancionadores](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/decisoes-em-processos-sancionadores) | a lista completa dos 9 processos concluídos e seus desfechos |
| [ANPD — Saiba como fiscalizamos](https://www.gov.br/anpd/pt-br/assuntos/fiscalizacao-2/atividades-fiscalizatorias) | *"até o momento, todos os processos sancionadores conduzidos pela ANPD, sem exceção, foram instaurados em decorrência de postura não colaborativa do regulado"*; o rito de 7 etapas; o volume de requerimentos por ano |
| [Despacho da ANPD no DOU de 06/07/2023 — caso Telekall](https://www.in.gov.br/web/dou/-/despacho-494550988) | a **única multa** da história da ANPD: advertência pelo art. 41 + R$ 7.200 pelo art. 7º + R$ 7.200 pelo art. 5º do Reg. de Fiscalização = **R$ 14.400**, contra uma microempresa |
| [Despacho no DOU — INSS, 01/02/2024](https://www.in.gov.br/web/dou/-/despacho-decisorio-n-1/2024/fis/cgf-540637061) | publicização da infração, agravada por descumprimento de medida preventiva |
| [Despacho no DOU — Meta Platforms, 02/07/2024](https://www.in.gov.br/web/dou/-/despacho-decisorio-n-20/2024/pr/anpd-569297245) | multa diária de R$ 50.000 — mas é astreinte de medida preventiva, não sanção de processo sancionador |

> Nota de honestidade sobre um dado que circula: a versão de que cada multa da Telekall
> corresponderia a "2% do faturamento da microempresa" aparece em blogs, mas **não está
> no texto do despacho publicado no DOU**. Não confirmado.

### FormSubmit e alternativas (fontes primárias)

| Fonte | O que confirma |
|---|---|
| [formsubmit.co/privacy.pdf](https://formsubmit.co/privacy.pdf) | o **único** documento jurídico do serviço: 2 páginas, *"Privacy Policies \| Terms of services"*, vigência de 17/01/2019. Sem menção a retenção, subprocessadores, GDPR, LGPD, DPA, lei aplicável, foro ou nome de empresa |
| [formsubmit.co/documentation](https://formsubmit.co/documentation) | *"We retain your form submissions for 30 days. Uploaded files won't retain or can't access through the API."*; limite de 10 MB somados; `_webhook` |
| [formsubmit.co/help](https://formsubmit.co/help) | retenção de 30 dias; reCAPTCHA, honeypot `_honey`, `_blacklist`; "Invisible emails" |
| [formsubmit.co/api-documentation](https://formsubmit.co/api-documentation) | a API de leitura existe: `get-apikey` e `get-submissions`, 5 chamadas/dia |
| [RDAP de `formsubmit.co`](https://rdap.registry.co/co/domain/formsubmit.co) | país do registrante `"cc": "LK"` (Sri Lanka), região Southern; domínio criado em 29/11/2018; registrador Cloudflare; demais campos `REDACTED FOR PRIVACY` |
| [Devro LABS no LinkedIn](https://www.linkedin.com/company/devrolabs) | sede em Colombo, Sri Lanka; 2–10 funcionários; fundada em 2018 |
| [devrolabs.com/company](https://devrolabs.com/company) | *"we keep our products for free and no paid package included"*; nenhum endereço |
| [RDAP ARIN de 192.99.70.154](https://rdap.arin.net/registry/ip/192.99.70.154) | o IP do SMTP (`mail.safenote.co`, do SPF) pertence a OVH Hosting, Inc., Montreal, Canadá |
| [king.host/hospedagem-de-sites](https://king.host/hospedagem-de-sites) | *"com servidores 100% no Brasil"*; CNPJ 02.351.877/0010-43 no rodapé |
| [Contrato de cliente da Azion](https://www.azion.com/pt-br/documentacao/contratos/contrato-de-cliente/) e [cláusulas ANPD](https://www.azion.com/pt-br/documentacao/anpd/operator-operador/) | CNPJ 12.447.998/0001-56, Porto Alegre/RS; declara-se operadora; publica as cláusulas-padrão da ANPD em português |
| [Política de privacidade da RD Station](https://legal.rdstation.com/pt-BR/privacy-policy/) e [DPA](https://www.rdstation.com/legal-e-privacidade/dpa/) | DPA explícito com lista de suboperadores, **mas** *"Os data centers estão localizados, especificamente nos estados da Califórnia e Iowa, nos Estados Unidos"* |
| [Termos do Pipefy](https://www.pipefy.com/legal-portal/terms-and-conditions/) | *"Pipefy, Inc., a foreign company duly incorporated under the laws of the State of Delaware"* — não é empresa brasileira |

### Código lido neste repositório

| Arquivo e linha | O que mostra |
|---|---|
| `index.html:34` | CSP da home, com `formsubmit.co` liberado em `connect-src` e `form-action` |
| `index.html:44–47` | os quatro `preconnect` para hosts do Google, disparados no carregamento |
| `index.html:1195–1222` | o `#contatoForm`: 4 campos visíveis, `_subject`, `_captcha`, `_template`, honeypot `_honey` |
| `index.html:1230–1236` | `footer__nav` — onde entra o link "Privacidade" |
| `servicos.html:35` | CSP mais fechada, com `form-action 'none'` e `frame-src 'none'` |
| `script.js:3728` | `FORMSUBMIT_TOKEN` — o destino não existe no front-end |
| `script.js:3738, 3756` | `action` de fallback e o `fetch` para `formsubmit.co/ajax/` |
| `script.js:2937, 2942, 3064, 3481` | os `lite-youtube` nascem por JS, só quando o modal abre |
| `script.js:2496` | monta a URL de embed do Instagram |
| `assets/lib/lite-yt-embed.js:109–122` | `warmConnections()`, incluindo os dois `preconnect` para `doubleclick` nas linhas 118–119 |
| `assets/fonts/` | fontes autohospedadas — nenhuma CDN |
| `.github/workflows/deploy-pages.yml:10–20, 51` | as duas listas de inclusão: `on.push.paths` e o `cp` que monta o `_site` |

### O que **não** consegui confirmar

Nada abaixo deve ser tratado como fato.

- **Razão social, tipo societário, número de registro e endereço do FormSubmit / Devro
  LABS.** O país (Sri Lanka) está sustentado por dois indícios independentes, mas a
  pessoa jurídica em si não foi confirmada. Um perfil no Gust apareceu na busca
  listando o status como "Not Incorporated", mas a página retorna HTTP 403 e não pôde
  ser verificada.
- **Por quanto tempo o FormSubmit mantém no servidor os anexos** antes de descartar. A
  documentação só diz que não são retidos no arquivo consultável pela API.
- **Para qual e-mail o token `FORMSUBMIT_TOKEN` encaminha.** Por desenho do recurso
  "Invisible email", isso não existe no front-end. O `index.html:1178` e `:1241`
  expõem `savyllaadryan` + `gmail.com` como contato público, mas **não confirmei** que
  seja o mesmo destino do formulário. Ela precisa confirmar antes de escrever o
  endereço no aviso de privacidade.
- **CNPJ da Magalu Cloud em fonte primária**, e a confirmação literal de que a Azion
  Functions expõe endpoint HTTP com Fetch API.
- **UOL Host, Mandaê e Zeev** não foram investigados como alternativas.
- **Se a Resolução CD/ANPD nº 15/2024 (incidentes) fixa prazo específico em número** —
  li a ementa na lista oficial, mas não abri o texto integral. O que está confirmado é
  que a Res. 2/2022, art. 14, II dá prazo em dobro ao pequeno porte.
- **Se existe modelo oficial da ANPD de aviso de privacidade** pronto para copiar. A
  ANPD publica modelo de ROPA e checklist de segurança para pequeno porte, mas não
  encontrei um template de política de privacidade. O texto da seção 6 foi escrito a
  partir dos requisitos do art. 9º da LGPD e do roteiro do art. 17, §2º do Regulamento
  da Res. 19/2024, não copiado de um modelo oficial.
- **O prazo de 5 anos da seção 8 não vem da LGPD.** É uma recomendação prática ancorada
  no prazo geral de cobrança de dívida líquida em instrumento particular do Código
  Civil (art. 206, §5º, I). A LGPD não fixa prazo numérico de retenção para nada disso.
