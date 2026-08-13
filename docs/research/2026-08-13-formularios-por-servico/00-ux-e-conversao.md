# Camada transversal — UX e conversão dos formulários

Pesquisa de 13/08/2026. Escopo: como os 7 formulários de briefing devem ser
estruturados, apresentados e operados. O **conteúdo** de cada um (quais perguntas)
é de outros sete levantamentos — aqui está o tronco.

Antes de tudo, quatro restrições reais do projeto que mudam as recomendações
(levantadas no código, não supostas):

1. **Não há build step.** O formulário vai ser HTML + JS de mão, servido como está.
2. **O `index.html` já envia por [FormSubmit](https://formsubmit.co)** — com
   `_honey` (honeypot), `_captcha=true`, `_template=table` e rótulo flutuante com
   `<label for>` de verdade. O tronco novo deve herdar esse padrão, não inventar outro.
3. **O `servicos.html` tem `form-action 'none'` e `connect-src 'self'` na CSP.**
   Do jeito que está, nenhum formulário envia nada de dentro dessa página. Isso
   precisa mudar de propósito, no arquivo onde o formulário morar.
4. **O deploy é lista de inclusão em dois lugares** (`on.push.paths` e o `cp` do
   `deploy-pages.yml`). Arquivo novo que não entre nas duas listas não publica — e
   se entrar só no `cp` e sumir, o deploy quebra de propósito.

A consequência mais importante da nº 1 e nº 2: **nada é capturado antes do submit.**
Não existe captura parcial, não existe "salvar rascunho no servidor". Isso decide
sozinho uma das perguntas de arquitetura (onde entram nome/e-mail) e vou usar isso lá.

---

## 1. O que a evidência realmente diz

### 1.1 Número de campos x conversão

**O que tem base.**

- **Baymard Institute** — o checkout médio em 2024 tem **11,3 campos** (era 11,8 em
  2021 e 12,7 em 2019), quando **8 bastariam**; **17% dos usuários já abandonaram
  por complexidade do checkout**. Base: mais de 200.000 horas de pesquisa de usabilidade
  ao longo de 10+ anos.
  [baymard.com/blog/checkout-flow-average-form-fields](https://baymard.com/blog/checkout-flow-average-form-fields)
  *Ressalva importante:* a própria página **não** publica o tamanho de amostra por
  número nem uma curva causal campo-a-campo. O dado é sobre **checkout de e-commerce**,
  não sobre briefing de serviço. Serve como disciplina ("corte o que não muda a entrega"),
  não como tabela de conversão para copiar.

- **Teste real e documentado do Marketo**, publicado pelo MarketingExperiments, com
  três variantes do mesmo formulário:

  | Campos | Conversão | Custo por lead |
  |---|---|---|
  | 5 | 13,4% | US$ 31,24 |
  | 7 (+ nº de funcionários, setor) | 12,0% | US$ 34,94 |
  | 9 (+ CRM, telefone comercial) | 10,0% | US$ 41,90 |

  [marketingexperiments.com/lead-generation/lead-generation-testing-form-field-length-reduces-cost-per-lead-by-10-66](https://marketingexperiments.com/lead-generation/lead-generation-testing-form-field-length-reduces-cost-per-lead-by-10-66)
  É o dado mais honesto que achei sobre campo de qualificação: cada par de campos
  extras custou ~1,4 ponto de conversão. Note que aqui o campo extra piorou **também**
  o custo por lead — mas o custo era mídia paga. No caso dela o custo é a hora dela
  escrevendo proposta. Volto nisso em 2.6.

- **Unbounce Conversion Benchmark Report** — metodologia pública: 41 mil landing pages,
  464 milhões de visitantes, 57 milhões de conversões, janela 23/07/2023 a 23/07/2024,
  páginas com menos de 50 visitantes excluídas, mediana geral de 6,6%.
  [unbounce.com/conversion-benchmark-report/methodology](https://unbounce.com/conversion-benchmark-report/methodology/)
  Isso dá uma régua de ordem de grandeza. Não dá curva por número de campos com
  metodologia aberta.

**O que é folclore de mercado — não use, e não deixe ninguém usar contra você:**

- **"Limitar a 3 campos garante no mínimo 25% de conversão."** Origem rastreada a um
  infográfico do QuickSprout. Não há estudo, amostra nem metodologia. "Garantir"
  conversão mínima é afirmação impossível.
- **"Reduzir de 4 para 3 campos aumenta 50%."** É um número da HubSpot de 2012 que
  virou citação circular. Nunca vi a metodologia publicada.
- **"Cada campo adicional derruba a conversão em 4,1%"** e a tabela
  **"23,1% com 3 campos → 17,0% com 5 → 11,4% com 7 → 6,9% com 10+"**. Aparecem
  idênticas em vários sites de 2026. Abri o principal deles e perguntei pela fonte:
  ele lista "HubSpot, Unbounce, WordStream, Baymard, Hotjar, FullStory, Contentsquare"
  em bloco, **sem um único link, nome de relatório, data ou tamanho de amostra**.
  [digitalapplied.com/blog/form-conversion-rate-benchmarks-2026-data-points](https://www.digitalapplied.com/blog/form-conversion-rate-benchmarks-2026-data-points)
  É estatística zumbi com cara de benchmark.
- **"Campo de orçamento derruba a conversão em 15,3%."** Ver 1.6.

**Conclusão utilizável:** existe efeito real de comprimento, a direção é confiável, e a
**magnitude publicada não é.** A régua defensável é a do Marketo: da ordem de
1 a 1,5 ponto de conversão por par de campos de qualificação. Isso é pouco o bastante
para justificar campos que realmente mudam a proposta, e caro o bastante para proibir
campo decorativo.

### 1.2 Formulário longo pode converter melhor quando o lead é qualificado?

Os dois lados, com o que cada um tem de evidência:

**A favor do curto (mais forte em dado).** O teste do Marketo acima. E o argumento
operacional: time de vendas qualifica melhor que campo de formulário, e o campo
"também espanta gente". Um caso muito citado é uma empresa de hospedagem que cortou
de 20 para 4 campos e teve +188% de leads
([cxl.com/blog/ab-testing-forms](https://cxl.com/blog/ab-testing-forms/)) — caso único,
sem metodologia, trate como anedota direcional.

**A favor do longo (mais fraco em dado, mais forte em lógica de negócio).** A CXL
registra explicitamente que **reduzir campos pode derrubar a qualidade do lead**, e
que perguntar orçamento é um jeito reconhecido de melhorar qualidade — mas apresenta
isso como prática de teste, não como resultado medido.
[cxl.com/blog/ab-testing-forms](https://cxl.com/blog/ab-testing-forms/)
A CXL também observa que testes de contagem de campos costumam dar lift significativo
**abaixo de 5%** — ou seja, o efeito é real e pequeno, e o ganho de qualidade pode
compensar facilmente.

**Onde o caso dela cai, e por quê isso importa.** A assimetria decisiva não está na
conversão, está no custo do lead ruim. Em lead gen paga, um lead ruim custa mídia. No
caso dela, um lead ruim custa **uma proposta artesanal escrita à mão** — a coisa mais
escassa que ela tem. A finalidade declarada é exatamente essa: "retornar o contato com
uma proposta mais estruturada". Então o formulário dela **legitimamente** pode ser mais
longo que o de um lead magnet, e a métrica que ela deve olhar não é taxa de envio, é
**propostas enviadas por hora de trabalho** e **taxa de fechamento**.

Sendo honesta: **não achei um estudo controlado que prove que formulário longo fecha
mais negócio em serviço criativo.** Isso é uma inferência de custo de oportunidade, não
um achado. Assumo a inferência e recomendo em cima dela, mas está marcada como
inferência.

### 1.3 Multi-step x página única

**O que circula é quase todo insustentável.** Os números famosos:
"+300%" (Venture Harbour), "+743%", "+214%" (Vendio), "11% → 46%" (BrokerNotes),
"+59,2%" (Conversion Fanatics/HubSpot). Nenhum publica metodologia, amostra ou
significância. E há uma prova direta de deriva: o **mesmo** teste da HubSpot aparece
como **"+59,2%"** em alguns sites e como **"86% de conversão maior"** no artigo da Zuko
([zuko.io/blog/single-page-or-multi-step-form](https://www.zuko.io/blog/single-page-or-multi-step-form)).
Quando o mesmo estudo tem dois números diferentes, o número não existe. Também abri o
artigo da Zuko esperando dado próprio — eles são uma empresa de form analytics — e
**eles não apresentam dado próprio**, só repassam terceiros.

**O que tem base de verdade** é a doutrina "**one thing per page**" do GOV.UK, formulada
por Caroline Jarrett em 2015 e sustentada por pesquisa de usuário contínua do governo
britânico. A razão publicada é o ponto forte, não um percentual:
usuários de baixa confiança acham mais fácil, **funciona melhor em mobile**, e
**lida melhor com erro, ramificação, loop e salvar progresso**.
[designnotes.blog.gov.uk/2015/07/03/one-thing-per-page](https://designnotes.blog.gov.uk/2015/07/03/one-thing-per-page/)
E a orientação explícita é: **comece separado e agrupe só quando a pesquisa mostrar que
agrupar ajuda** — não o contrário.

**Divulgação progressiva** (mostrar só o que é relevante agora) é princípio consolidado
da NN/g para carga cognitiva.
[nngroup.com/articles/progressive-disclosure](https://www.nngroup.com/articles/progressive-disclosure/)

**Barra de progresso e "endowed progress effect".** Aqui há estudo acadêmico de verdade:
Nunes & Drèze, *Journal of Consumer Research*, 2006. Lava-rápido, ~300 clientes,
dois cartões de fidelidade. Cartão A: 8 selos, começa em 0/8. Cartão B: 10 selos,
**2 já estampados**, começa em 2/10. O esforço real é idêntico — 8 lavagens.
Conclusão: **19% completaram o cartão A contra 34% o cartão B.**
[researchgate.net/publication/23547282](https://www.researchgate.net/publication/23547282_The_Endowed_Progress_Effect_How_Artificial_Advancement_Increases_Effort)
**Ressalva que ninguém faz:** isso é fidelidade de lava-rápido, não formulário web. O
mecanismo (progresso artificial aumenta esforço) transfere de forma plausível; a
**magnitude não transfere.** Use a técnica, não espere quase dobrar nada.

**Nome/e-mail no começo ou no fim?** Não achei experimento controlado limpo dos dois
lados — este é um ponto onde o mercado tem opinião e não tem dado. O que existe de dado
utilizável é indireto: no dataset da Zuko (mais de 100 milhões de sessões de formulário),
**campos pessoais são os que mais derrubam** — senha com ~10,5% de abandono médio no
campo, telefone com 6,3%, e completude desktop 55,5% contra mobile 47,5%.
[zuko.io/blog/zuko-benchmarking-data-how-does-your-form-compare](https://www.zuko.io/blog/zuko-benchmarking-data-how-does-your-form-compare)
Ou seja: o campo pessoal é caro. Onde colocar o caro é decisão de arquitetura, e eu
decido em 2.3 — com um argumento que vem do stack dela, não de benchmark.

### 1.4 Lógica condicional / perguntas ramificadas

Boa prática é consenso e tem fundamento: ramificar é divulgação progressiva aplicada, e
o GOV.UK cita "lidar melhor com ramificação" como uma das razões de separar por página.
Não há controvérsia aqui.

**O custo de manutenção é o que ninguém escreve, e no caso dela é concreto:**
sem build step, cada regra condicional é JS escrito à mão que precisa ficar em sincronia
com o HTML na mão, sem teste automatizado. Cada serviço novo, cada pergunta renomeada, é
uma chance de dessincronizar. E há uma armadilha técnica específica: **campo com
`required` dentro de bloco escondido torna o formulário impossível de enviar**, com o
navegador reclamando de um campo invisível. Regras práticas em 4.6.

### 1.5 Sete formulários separados x um com roteamento

Não achei estudo — isto é engenharia e SEO, não psicologia. Levantei o que decide:

- **SEO.** Hoje **não existe URL por serviço**: o `servicos.html` é *uma* página com
  sete âncoras (`#conteudo-redes-sociais`, `#direcao-de-creators`, `#filmmaker`,
  `#pos-producao`, `#fotografia`, `#direcao-de-arte`, `#producao-com-ia`) e um único
  `canonical`. Então "ganhar URL própria por serviço" não é preservar algo que existe —
  é criar sete páginas novas. E páginas de **formulário** são o pior candidato a
  ranquear: conteúdo fino, quase idêntico entre si (o tronco é o mesmo), competindo
  entre elas. Se algum dia ela quiser URL por serviço para SEO, o ativo certo é a
  **descrição** do serviço, não o formulário.
- **Manutenção.** Sete arquivos = sete cópias do tronco, sete CSPs, sete entradas na
  lista de inclusão do deploy, e sete lugares para esquecer de corrigir a mesma coisa.
- **O cliente que combina.** A própria página promete: *"Você contrata uma sozinha ou
  combina quantas o projeto pedir."* Sete formulários separados **quebram essa promessa
  na prática** — ou a pessoa preenche dois formulários e ela recebe dois e-mails
  desconexos, ou a pessoa desiste de dizer que quer dois.

Recomendação e justificativa completas em 2.1.

### 1.6 Perguntar verba/orçamento

**Contra, e o que vale de cada peça:**

- **"Campo de orçamento tem impacto de -15,3% na conversão, o pior de todos os campos
  testados."** Abri a fonte. Ela cita "estudo Formstack com 1.500 tomadores de decisão
  B2B (2025)", Forrester e Marketo, mas **não abre metodologia, controle nem como o
  -15,3% foi isolado**. [brixongroup.com/en/lead-forms-in-b2b...](https://brixongroup.com/en/lead-forms-in-b2b-the-perfect-balancing-act-between-data-depth-and-conversion-rate)
  Direção plausível (orçamento é campo sensível), **número não verificável — folclore.**
- **O teste do Marketo (1.1) é a evidência real contra**: campos de qualificação
  custaram conversão e custo por lead.
- **Baymard, sobre campos sensíveis em geral:** pesquisa de 2017 achou que **15% nunca
  fornecem telefone** e **35% nunca fornecem data de nascimento**. Prova que existe uma
  classe de campo que uma fatia do público simplesmente se recusa a preencher.
  [baymard.com/blog/required-optional-form-fields](https://baymard.com/blog/required-optional-form-fields)

**A favor:** a CXL recomenda explicitamente perguntar orçamento pretendido como forma
de melhorar qualidade de lead. [cxl.com/blog/ab-testing-forms](https://cxl.com/blog/ab-testing-forms/)
É recomendação de praticante, não resultado medido.

**O ponto que a pesquisa não cobre e que é o mais importante no caso dela:** o site
**nunca mostra preço**. Pedir a verba do cliente sem oferecer nenhuma referência de
preço é uma troca assimétrica, e é assim que a pergunta fica antipática. A literatura de
campo sensível trata do custo de *pedir*; ninguém testou o efeito de *pedir sem dar
nada em troca*. Minha decisão em 2.6 ataca exatamente essa assimetria.

### 1.7 Microcopy, rótulos e validação

Aqui a evidência é a mais sólida de toda a pesquisa.

- **Formulário que segue diretriz de usabilidade tem 78% de envio na primeira tentativa,
  contra 42% de formulário que não segue.** Estudo CHI de Seckler et al., citado pela
  NN/g. É o número mais forte que achei em toda a pesquisa e é sobre **conformidade
  geral**, não sobre contagem de campos.
  [nngroup.com/articles/web-form-design](https://www.nngroup.com/articles/web-form-design/)
  As 10 recomendações da NN/g, resumidas: seja curto; agrupe rótulo e campo; **coluna
  única**; sequência lógica; **evite placeholder**; case tipo e tamanho do campo com o
  input; **marque obrigatório e opcional**; explique formato **antes** do erro; nada de
  botão "limpar"; erro muito visível e que preserva o que a pessoa digitou.
- **Placeholder como rótulo é nocivo.** Dificulta lembrar o que vai no campo e revisar
  erro, e nem todo leitor de tela lê placeholder. Rótulo flutuante mitiga; rótulo **fora**
  do campo continua sendo o melhor.
  [nngroup.com/articles/form-design-placeholders](https://www.nngroup.com/articles/form-design-placeholders/)
- **Validação inline funciona, e o "quando" importa.** Estudo Wroblewski/Etre: +22% de
  sucesso, −22% de erros, +31% de satisfação, −42% de tempo, −47% de fixações oculares.
  **Melhor método: validar no `blur` (ao sair do campo)** para pergunta simples —
  7 a 10 segundos mais rápido. Validar **enquanto digita** só ajuda em campo complexo
  (usuário/senha), e com atraso. Validar **antes e enquanto** foi o pior: as pessoas
  chamaram de irritante.
  [alistapart.com/article/inline-validation-in-web-forms](https://alistapart.com/article/inline-validation-in-web-forms/)
  **Ressalva declarada pelo próprio autor: 22 participantes, resultado "indicativo, não
  definitivo".** Uso a direção (validar no blur), não os percentuais.
- **Obrigatório e opcional, os dois marcados.** Baymard: só **14% dos sites marcam os
  dois** (igual a 2016). 42% marcam só o obrigatório; 37% marcam só o opcional — e
  nesse último grupo **32% dos usuários batem em erro de validação**. Em teste,
  **44% dos usuários pararam completamente** no formulário de entrega da Amazon, e
  **22%** tentaram avançar sem preencher obrigatório na L.L. Bean, por falta de marcação.
  [baymard.com/blog/required-optional-form-fields](https://baymard.com/blog/required-optional-form-fields)
  A NN/g concorda e acrescenta: asterisco no **começo** do rótulo, em cor de bom
  contraste, e nunca confie em "todos os campos são obrigatórios salvo indicação" —
  ninguém lê instrução de formulário.
  [nngroup.com/articles/required-fields](https://www.nngroup.com/articles/required-fields/)
- **Acessibilidade — requisito, não enfeite.** WCAG 2.1 **1.3.5 Identify Input Purpose,
  nível AA**, exige `autocomplete` com token padronizado nos campos que coletam dado
  sobre a própria pessoa (nome, e-mail, telefone, endereço). Campo de busca ou dado de
  terceiro está fora do escopo.
  [dequeuniversity.com/resources/wcag2.1/1.3.5-identify-input-purpose](https://dequeuniversity.com/resources/wcag2.1/1.3.5-identify-input-purpose)
  O `index.html` **já faz isso** (`autocomplete="name"`, `autocomplete="email"`) — o
  tronco novo tem que manter.

### 1.8 Mobile

- **Completude é pior no celular: 47,5% contra 55,5% no desktop** (dataset Zuko).
  [zuko.io/blog/zuko-benchmarking-data-how-does-your-form-compare](https://www.zuko.io/blog/zuko-benchmarking-data-how-does-your-form-compare)
- **Teclado certo por tipo de campo é problema crônico e mensurável.** Baymard: dos 50
  maiores sites mobile, **60% erram ao menos 2 de 5 otimizações de teclado**, e o
  suporte a teclado dedicado subiu só de 40% (2013) para 46% (2015) — em teste, o
  resultado foi checkout "dominado por erro de validação" e até pedido enviado com dado
  errado. Casos concretos: HP com `str` autocorrigido para `ate` por não desligar
  autocorreção; Amazon exibindo teclado alfanumérico onde devia ser numérico.
  [baymard.com/blog/mobile-touch-keyboards](https://baymard.com/blog/mobile-touch-keyboards)
  Cheat sheet de combinação `type` + `inputmode` + `autocorrect` + `autocapitalize`:
  [baymard.com/labs/touch-keyboard-types](https://baymard.com/labs/touch-keyboard-types)
- **Contexto Brasil.** 92,9% dos domicílios têm rede móvel funcionando para internet ou
  telefonia em 2025 (IBGE/PNAD); nas classes D/E, o acesso à internet pelo celular foi
  de 48% (2017) para 78% (2025).
  [agenciadenoticias.ibge.gov.br](https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/47410-internet-chega-a-95-de-domicilios-do-pais-em-2025)
  · [mobiletime.com.br](https://www.mobiletime.com.br/noticias/05/01/2026/internet-movel-classesde/)
  Não achei número confiável do **share de tráfego web mobile especificamente do Brasil**
  — quem publica isso são agregadores sem metodologia. Trate "a maior parte do tráfego é
  mobile" como premissa razoável dela, não como dado que eu confirmei.
- **Salvar e continuar depois:** no stack estático, sem servidor, isso só existe como
  `localStorage`. Ver 4.7.

### 1.9 Depois do envio

Este é o tema **mais fraco em evidência** de toda a pesquisa. O que se acha sobre tela
de obrigado e e-mail automático é material de fornecedor de formulário, sem estudo:
"confirme o recebimento, informe o prazo estimado, dê próximo passo". Razoável,
não medido. Marco como boa prática sem base experimental.

**O que tem base de verdade é o prazo de resposta.** Oldroyd, McElheran & Elkington,
*Harvard Business Review*, março de 2011: **auditaram 2.241 empresas americanas**
medindo quanto cada uma levava para responder um lead de teste enviado pelo site.
Resultado: **37% responderam em até 1 hora, 16% entre 1 e 24 horas, 24% levaram mais de
24 horas e 23% nunca responderam.**
[hbr.org/2011/03/the-short-life-of-online-sales-leads](https://hbr.org/2011/03/the-short-life-of-online-sales-leads)
· [hbs.edu/faculty/Pages/item.aspx?num=39955](https://www.hbs.edu/faculty/Pages/item.aspx?num=39955)

**Cuidado com a parte que virou zumbi.** Os números "responder em 5 minutos torna 100x
mais provável o contato" e "depois de 5 minutos a chance de qualificar cai 80%" **não
são** da auditoria do HBR — vêm do dataset InsideSales/Lead Response Management e são
rotineiramente colados no crédito do HBR. A parte auditada e citável é a **distribuição
de tempo de resposta**, não o multiplicador.

O que é utilizável: **a régua do mercado é baixíssima.** Quase um quarto das empresas
nunca responde. Um prazo modesto e cumprido já é diferencial.

**WhatsApp como canal de retorno.** Pesquisa BCG em parceria com a Meta: 8 em cada 10
consumidores preferem falar com empresa por mensagem, e 89% das pessoas no Brasil usam
WhatsApp para falar com comércio ou prestador de serviço.
[agendor.com.br/blog/whatsapp-brasil](https://www.agendor.com.br/blog/whatsapp-brasil/)
**Ressalva séria: a Meta é co-autora do estudo, e a Meta é dona do WhatsApp.** Direção
confiável (no Brasil, mensagem ganha de e-mail para conversa comercial), magnitude é
material de marketing.

### 1.10 Anti-spam sem atrito

- **CAPTCHA tem custo humano medido, e é grande.** Bursztein et al., *IEEE Symposium on
  Security and Privacy*, 2010 — primeira avaliação em larga escala do lado humano:
  **mais de 318.000 CAPTCHAs de 21 esquemas populares** (13 de imagem, 8 de áudio).
  **Tempo médio de resolução de 9,8 a 28,4 segundos**; CAPTCHA de áudio é bem pior; e
  **não nativos em inglês são mais lentos e menos precisos** em esquemas centrados no
  inglês. Esse último ponto é diretamente relevante: o público dela é brasileiro.
  [web.stanford.edu/~jurafsky/burszstein_2010_captcha.pdf](https://web.stanford.edu/~jurafsky/burszstein_2010_captcha.pdf)
  · [ieeexplore.ieee.org/document/5504799](https://ieeexplore.ieee.org/document/5504799/)
- **Folclore a descartar:** "29% dos usuários abandonam ao ver CAPTCHA", "1,47% abandonam
  imediatamente", "CAPTCHA reduz 3-4% dos envios", "honeypot pega 80-90% dos bots",
  "78% dos bots preenchem todo campo que encontram (OWASP 2024)". Todos vêm de blogs de
  fornecedor de CAPTCHA — cada um com interesse comercial na resposta — e nenhum abre
  metodologia. Não achei estudo independente quantificando perda de conversão por CAPTCHA.
- **O que é defensável sem número:** honeypot tem custo de conversão estruturalmente
  zero porque o usuário legítimo nunca o vê. CAPTCHA visível tem custo maior que zero,
  e o estudo de 2010 dá a ordem de grandeza desse custo em segundos e em erro. Para o
  volume de um portfólio pessoal, gastar segundos de todo cliente legítimo para barrar
  spam que ela pode simplesmente deletar da caixa de entrada é troca ruim.

---

## 2. Decisões de arquitetura (com recomendação)

### 2.1 Sete formulários x um roteado → **UM formulário, com seleção de serviço no topo**

**Recomendação:** um arquivo, `briefing.html`, com o serviço escolhido por
**checkbox de múltipla escolha** no primeiro passo. Cada serviço ganha entrada própria
por query string — `briefing.html?servico=filmmaker` — que já chega com aquela caixa
marcada. Os sete CTAs do `servicos.html` apontam cada um para o seu link.

**Por quê:**

1. **A promessa da página exige.** O site diz que dá para combinar frentes. Checkbox
   múltiplo cumpre; sete formulários separados não — obrigariam a pessoa a preencher
   dois e ela a receber dois e-mails que não conversam.
2. **O argumento de SEO não existe aqui.** Hoje não há URL por serviço para preservar
   (uma página, sete âncoras, um canonical). Sete páginas de formulário seriam sete
   páginas de conteúdo fino quase idênticas competindo entre si — piora, não melhora.
   Se URL por serviço virar meta, o ativo a dividir é a **descrição**, nunca o formulário.
3. **Manutenção.** Um tronco, uma CSP, duas linhas na lista de inclusão do deploy. Sete
   arquivos seriam sete cópias do mesmo tronco para dessincronizar.
4. **Ela ganha o "?servico=" quase de graça** e a experiência ainda parece feita para
   aquele serviço, que é o benefício real que sete páginas prometiam.

**O que ela perde e como cobrir:** o link não fica bonito de ditar por telefone. Cubra
com um link curto no Instagram e um único `briefing.html` sem parâmetro, que abre com
nada marcado.

### 2.2 Multi-step x página única → **três passos, com degradação para página única**

**Recomendação:** três passos num único `<form>`:

- **Passo 1 — O que.** Quais frentes (checkbox múltiplo) + o projeto em uma frase.
- **Passo 2 — Detalhes.** O bloco específico dos serviços marcados. É aqui que entra o
  trabalho dos outros sete levantamentos.
- **Passo 3 — Prático.** Prazo, verba (opcional), como responder, e só então o contato.

**Por quê três, e não um nem "uma pergunta por página":**
- Um passo só empilha 14+ campos na tela do celular, onde a completude já é 8 pontos
  pior (Zuko). O motivo publicado do GOV.UK para separar é literalmente mobile, erro e
  ramificação — os três problemas dela.
- "Uma pergunta por página" viraria 15 toques em "Continuar". O GOV.UK diz para começar
  separado **e agrupar quando a pesquisa mostrar**; aqui o agrupamento é obvio porque as
  três fatias são cognitivamente distintas (o que você quer / como é / condições).
- Três passos permitem que a **ramificação tenha um só eixo** (passo 2 depende do passo 1)
  e nada mais. Isso é o que segura o custo de manutenção de 1.4.

**Regra técnica que não é opcional:** um único `<form>`, com os passos como `<fieldset>`
mostrados e escondidos por JS. Se o JS falhar — e num site sem build step, com CSP
`script-src 'self'`, isso é cenário real — a pessoa vê **um formulário longo que
funciona**, não uma página quebrada. Multi-step que só existe em JS transforma falha de
script em zero lead.

### 2.3 Onde entram nome e e-mail → **no fim, no passo 3**

**Recomendação:** contato é o último bloco, depois de prazo e verba.

**Por quê — e este é o argumento decisivo, que vem do stack e não de benchmark:** o
único motivo forte para pedir contato no começo é **salvar o abandono** — capturar
e-mail antes de a pessoa desistir. **No stack dela isso não existe.** Site estático,
FormSubmit, nada é gravado até o submit. Pedir contato primeiro não salva ninguém: só
gasta os campos mais caros (Zuko: campos pessoais lideram abandono; telefone 6,3%) no
momento em que a pessoa investiu menos e tem menos motivo para continuar.

Colocando no fim, o campo caro é pago quando o investimento já foi feito e o custo de
desistir é maior.

**Honestidade sobre isso:** é escolha raciocinada, não medida. Não achei experimento
limpo comparando ordem. Se ela quiser evidência própria depois, o teste é trivial:
trocar a ordem por um mês e comparar envios.

### 2.4 Barra de progresso → **sim, com progresso adiantado**

**Recomendação:** "Etapa 1 de 3" visível, com a barra já preenchida em torno de 15% no
passo 1 em vez de zero — a pessoa entra com progresso, não em branco. Passos clicáveis
para trás, e **o que foi digitado sobrevive ao voltar** (esse é o bug clássico; a própria
Zuko diz ter visto até 10% de ganho só corrigindo persistência entre passos).

**Por quê:** Nunes & Drèze, 19% → 34% de conclusão com dois selos de brinde, n≈300, JCR
2006. **Com a ressalva explícita:** o estudo é de fidelidade em lava-rápido. Aplique a
técnica; **não espere quase dobrar coisa alguma.** O ganho real aqui é o mais banal —
a pessoa saber quanto falta.

Nada de barra falsa que não corresponda aos passos reais. Três passos, três segmentos.

### 2.5 O cliente que quer combinar serviços → **checkbox múltiplo, com teto**

**Recomendação:** checkbox, não radio, não `<select>`. Microcopy espelhando a copy que
já está na página: *"Marque quantas quiser — dá para combinar."*

**E o teto, que é a parte que ninguém pensa:** se a pessoa marcar 3 frentes e o passo 2
empilhar os três blocos específicos, o formulário explode para 25+ campos. Regra:
**a partir de 3 serviços marcados, o passo 2 troca os blocos específicos por um bloco
único de escopo combinado** — 4 ou 5 perguntas amplas mais um campo de texto livre. Quem
quer três frentes tem projeto grande e vai conversar de verdade; o formulário só precisa
qualificar o suficiente para ela marcar a conversa.

Com 1 ou 2 serviços marcados, mostra os blocos específicos normalmente.

### 2.6 Campo de verba → **sim, mas opcional, em faixas, com saída explícita, no passo 3**

**Recomendação, exatamente assim:**

- **Opcional.** Nunca `required`. Verba obrigatória num site que não mostra preço é a
  combinação mais provável de perder um cliente bom.
- **Faixas, não campo aberto.** Faixa é mais fácil de responder, não expõe a pessoa, e
  — o ponto importante — **as faixas ensinam a ordem de grandeza.** É a única forma de
  ela devolver alguma referência de preço sem publicar tabela.
- **Com uma opção de fuga declarada:** "Ainda não sei / prefiro conversar". Sem ela, quem
  não quer responder abandona o formulário em vez de pular o campo.
- **No passo 3**, junto do prazo, que é o lugar de menor custo de abandono do fluxo.
- **Com microcopy que dá antes de pedir.** Não "Qual seu orçamento?" seco. Ver o texto
  exato em 3.

**Por quê, contra a evidência que diz para não pedir:** o "-15,3%" é folclore
(1.6). O teste real que existe (Marketo) mede custo em **mídia paga** — não é o custo
dela. O custo dela é hora escrevendo proposta artesanal, e a finalidade que ela mesma
declarou é proposta mais estruturada. Um campo opcional com fuga explícita tem custo
próximo de zero para quem não quer responder (pula um campo) e valor alto para quem
responde. É a assimetria certa.

**O que ela não deve fazer:** perguntar verba no passo 1. Ali é onde a pergunta soa como
porteiro cobrando pedágio.

### 2.7 Quantos campos no máximo → **tronco 8, específico 6, total ≤ 14; obrigatórios ≤ 10**

**Recomendação, e este é o número para passar aos sete pesquisadores:**

| Bloco | Máximo de campos | Máximo obrigatórios |
|---|---|---|
| Tronco (comum aos 7) | 8 | 6 |
| Específico por serviço | 6 | 4 |
| **Total, 1 serviço marcado** | **14** | **10** |
| Bloco combinado (3+ serviços) | 5 | 3 |

**Por quê 14 e não 8 (Baymard) nem 5 (Marketo):** o número da Baymard é de checkout, onde
o campo não muda o produto; o do Marketo é de lead magnet, onde o formulário não gera
entrega. No caso dela, o campo **muda a proposta**. A régua defensável do Marketo é
~1 a 1,5 ponto de conversão por par de campos de qualificação — a esse preço, 6 campos
que mudam preço, prazo ou formato se pagam; 6 campos de curiosidade, não.

**A regra de corte para os sete pesquisadores, em uma frase:** *toda pergunta tem que
mudar o preço, o prazo ou o formato da entrega.* Se não muda, corta ou vira opcional.
Se a resposta é sempre a mesma, ela já sabe — não pergunte.

---

## 3. Esqueleto comum aos 7 formulários

Este é o tronco. Os blocos específicos de cada serviço entram **no passo 2, entre 3.2 e
3.3**. Microcopy pronta para colar — em português, tom da casa (direto, sem corporativês).

### Passo 1 — O que você precisa

**1. Frentes de trabalho** · checkbox múltiplo · **obrigatório** (mínimo 1)

> **De que você precisa?**
> Marque quantas quiser — dá para combinar.
> ☐ Conteúdo para Redes Sociais ☐ Direção de Creators ☐ Filmmaker
> ☐ Pós-produção ☐ Fotografia ☐ Direção de Arte ☐ Produção com IA
> ☐ Ainda não sei — me ajuda a definir

A última caixa importa: sem ela, quem não sabe o nome do serviço que precisa vai embora.
Ela também é uma resposta valiosa — indica cliente que precisa de consultoria, não de
orçamento.

**2. O projeto em uma frase** · texto curto · **obrigatório**

> **Conte em uma frase o que você quer fazer.**
> Ex.: "lançamento de um sabor novo, 6 vídeos para Instagram e TikTok".

Pergunta de abertura fácil, sobre o assunto favorito da pessoa (o projeto dela). Nada de
dado pessoal aqui.

**3. Marca ou empresa** · texto curto · **opcional**

> **Marca ou empresa** *(opcional)*
> Se for projeto pessoal ou ainda sem nome, deixa em branco.

### Passo 2 — Como é o projeto

Aqui entram os **blocos específicos por serviço** (máx. 6 campos por serviço), ou o
**bloco combinado** se 3+ frentes estiverem marcadas.

Antes deles, dois campos do tronco:

**4. Onde isso vai ser publicado** · checkbox múltiplo · **obrigatório**

> **Onde o material vai rodar?**
> ☐ Instagram ☐ TikTok ☐ YouTube ☐ Site ☐ Anúncio pago
> ☐ Uso interno / evento ☐ Outro

Muda formato, proporção e quantidade de entrega — passa o teste de corte.

**5. Já existe algo pronto?** · texto livre curto · **opcional**

> **Já existe roteiro, manual de marca, referência ou material bruto?** *(opcional)*
> Cola links aqui. Se for arquivo grande, manda o link do Drive ou WeTransfer.

Ver 4.8 sobre por que é link e não upload.

### Passo 3 — Prazo, verba e contato

**6. Quando precisa estar pronto** · seleção · **obrigatório**

> **Para quando?**
> ○ Até 1 semana ○ 2 a 4 semanas ○ 1 a 2 meses ○ Mais de 2 meses
> ○ Sem data definida ainda

Seleção, não campo de data: a maioria não tem data exata, e campo de data no celular é
tortura. "Sem data definida" evita resposta inventada.

**7. Faixa de investimento** · seleção · **opcional**

> **Faixa de investimento** *(opcional)*
> Pergunto para já te mandar um escopo que cabe, em vez de um orçamento que não serve.
> ○ até R$ X ○ R$ X a Y ○ R$ Y a Z ○ acima de R$ Z
> ○ Ainda não sei — me manda opções

As faixas concretas quem define é ela; o desenho é que importa. A microcopy dá antes de
pedir: explica que a pergunta serve ao cliente. E a última opção é a saída sem custo.

**8. Nome** · texto · **obrigatório** · `autocomplete="name"`

> **Seu nome**

**9. E-mail** · e-mail · **obrigatório** · `autocomplete="email"` · `inputmode="email"`

> **Seu e-mail**
> É por aqui que eu mando a proposta.

**10. WhatsApp** · telefone · **opcional** · `autocomplete="tel"` · `inputmode="tel"`

> **WhatsApp** *(opcional)*
> Se preferir que eu responda por aqui, é mais rápido.

Opcional de propósito: telefone é campo de alto abandono (6,3%, Zuko), e no Brasil
WhatsApp é o canal que a pessoa provavelmente prefere. Oferecer sem exigir pega os dois
públicos.

**11. Como prefere que eu responda** · seleção · **opcional**

> **Como prefere que eu responda?**
> ○ E-mail ○ WhatsApp ○ Chamada de vídeo, se fizer sentido

Barato, e evita ela mandar e-mail para quem só olha WhatsApp.

**Botão de envio:**

> **Enviar briefing**
> Eu respondo em até 1 dia útil.

O prazo fica **no botão**, não só na tela de obrigado — a pessoa decide enviar sabendo o
que vai acontecer.

**Campos escondidos** (mesmo padrão do `index.html`):
`_subject` com o serviço no assunto, `_template=table`, `_autoresponse`, honeypot,
`_next` apontando para a tela de obrigado, e **`_captcha=false`** (ver 4.9).

---

## 4. Padrões de escrita e de interface

Base: as 10 recomendações da NN/g (78% x 42% de envio na primeira tentativa) e o que já
está certo no `index.html`.

### 4.1 Rótulos

- **Rótulo sempre visível, fora do campo ou flutuante.** Nunca placeholder como rótulo.
  O `index.html` já usa flutuante com `<label for>` de verdade + `placeholder=" "` —
  **mantenha esse padrão**, é a solução acessível.
- **Coluna única.** Sem duas colunas, sem exceção neste formulário.
- Rótulo em linguagem de cliente, não de produção. "Onde o material vai rodar", não
  "canais de distribuição".

### 4.2 Obrigatório e opcional — os dois marcados

Baymard: só 14% dos sites fazem isso, e quem marca só um dos dois gera erro em 32% dos
usuários. Então:

- Obrigatório: asterisco **antes** do rótulo, em cor com contraste real (não cinza claro),
  mais `required` e `aria-required="true"`.
- Opcional: a palavra **"(opcional)"** no fim do rótulo, visível.
- Uma legenda no topo do formulário explicando o asterisco — mas **sem depender dela**,
  porque ninguém lê instrução de formulário (NN/g).

### 4.3 Texto de ajuda

- Ajuda vai **antes** do campo, como texto permanente, não como mensagem de erro depois.
  A NN/g é explícita: explique o formato antes, em vez de corrigir depois.
- Amarrada por `aria-describedby` no input, para leitor de tela ler junto.
- Uma linha. Se precisa de duas, a pergunta está mal feita.

### 4.4 Validação

- **No `blur`** (ao sair do campo) para tudo. É o método que ganhou no estudo
  Wroblewski/Etre, com 7 a 10 segundos de vantagem.
- **Nunca "antes e enquanto"** — foi o pior do estudo, descrito como irritante.
- Nada de validar enquanto digita neste formulário: não há campo tipo senha/usuário que
  justifique.
- Sucesso não precisa de selo verde em todo campo. Ausência de erro basta.

### 4.5 Mensagens de erro

- Ao lado do campo, não no topo, e **nunca só cor** — texto + ícone + borda.
- **Preserva o que a pessoa digitou.** Nunca limpe o campo.
- Diga o que fazer, não o que houve: "Falta o @ no e-mail" em vez de "e-mail inválido".
- No submit com erro: **foco programático no primeiro campo inválido**, com
  `aria-invalid="true"` e `aria-describedby` apontando para a mensagem.
- Resumo de erro anunciado num `role="alert"`. O `index.html` já tem o padrão vizinho:
  `<p role="status" aria-live="polite">` para o status de envio — reuse.
- **Nada de botão "limpar"/"resetar"** (NN/g nº 9).

### 4.6 Acessibilidade e lógica condicional (as duas juntas, porque colidem)

- `<label for>` real em todo campo. `<fieldset>` + `<legend>` em todo grupo de
  checkbox/radio — inclusive na seleção de frentes.
- `autocomplete` com token WCAG 1.3.5 em nome, e-mail e telefone. É **nível AA**, e o
  `index.html` já cumpre.
- Navegação por teclado no multi-step: ao trocar de passo, **mova o foco para o título
  do novo passo** (`tabindex="-1"` + `.focus()`). Sem isso, o leitor de tela fica no
  botão de um passo que não existe mais. É o erro nº 1 de wizard acessível.
- Contraste de asterisco, mensagem de erro e texto de ajuda dentro do AA.
- **Bloco condicional escondido:** esconda o `<fieldset>` com o atributo `hidden` **e**
  ponha `disabled` nele. Duas razões, as duas concretas: `disabled` impede que valores
  de serviço desmarcado sejam enviados, e — **a armadilha** — campo com `required`
  dentro de bloco invisível **trava o envio do formulário**, com o navegador reclamando
  de um campo que ninguém vê. `disabled` no fieldset resolve os dois de uma vez.
- **Um só eixo de ramificação:** o passo 2 depende só de quais frentes foram marcadas no
  passo 1. **Proibido condicional dentro de condicional.** Sem build step e sem teste,
  ramificação de segundo nível é dívida que ela vai pagar sozinha às onze da noite.

### 4.7 Mobile

- **Teclado certo em cada campo** — 60% dos maiores sites erram isso (Baymard):
  - e-mail → `type="email"` `inputmode="email"` `autocapitalize="off"` `autocorrect="off"`
  - WhatsApp → `type="tel"` `inputmode="tel"`
  - nome → `type="text"` `autocapitalize="words"`
  - texto livre → `<textarea>`, sem desligar autocorreção
- Alvo de toque mínimo de 44 px em checkbox, radio e botão de avançar.
- Botão "Continuar" **fixo no rodapé** dentro do passo, não escondido depois de 12
  campos de rolagem.
- Evite `<select>` com muitas opções; radio em coluna é melhor no celular.
- **Salvar e continuar depois:** sem servidor, o único caminho é `localStorage` —
  gravar as respostas a cada mudança de passo e reoferecer ao voltar
  (*"Você tinha começado um briefing. Continuar de onde parou?"*). É umas 15 linhas de
  JS e resolve o caso real de quem preenche no celular e é interrompido. **Não grave
  nada em `localStorage` sem essa pergunta**, e limpe depois do envio.

### 4.8 Upload

**Recomendação: não faça upload de arquivo. Peça link.**

Motivos concretos, não estilísticos: o stack é estático — não há onde receber arquivo;
o FormSubmit tem limite de anexo; upload no celular é dos fluxos mais frágeis que
existem; e o material que ela precisa (bruto de vídeo, manual de marca) é grande demais
para anexo de qualquer jeito. O campo 5 do tronco pede link do Drive/WeTransfer, que é o
que o cliente dela já usa.

Se um dia precisar de imagem pequena, aí sim `accept` restrito e limite anunciado
**antes** do clique.

### 4.9 Anti-spam

**Recomendação: honeypot + tempo mínimo de preenchimento. Zero CAPTCHA visível.**

- **Desligue o `_captcha` do FormSubmit nesta página** (`value="false"`). Está `true` no
  `index.html` e, do lado do usuário, significa CAPTCHA depois do envio. O estudo de
  Bursztein mede 9,8 a 28,4 segundos de resolução, pior em áudio, e **pior ainda para
  não nativos em inglês** — o público dela é brasileiro. Gastar isso de todo cliente
  legítimo para barrar spam que ela deleta em dois segundos é troca ruim.
- **Honeypot** no padrão que já está no `index.html` (`_honey` com `display:none`).
  `display:none` remove o campo da árvore de acessibilidade, então leitor de tela não o
  vê — está correto. Reforce com `tabindex="-1"`, `aria-hidden="true"` e
  `autocomplete="off"`. **Cuidado real:** não dê ao honeypot nome que o autofill do
  navegador reconheça (`email`, `nome`, `telefone`) — o navegador preenche e o cliente
  legítimo é barrado.
- **Tempo mínimo:** guarde o timestamp de carregamento num campo escondido e descarte
  envio feito em menos de ~3 segundos. Bot preenche instantaneamente; humano não. Custo
  de conversão zero.
- **Se o spam furar** (só então): Cloudflare Turnstile, que é invisível na maior parte
  das vezes. Mas note: exige liberar o domínio da Cloudflare em `script-src` e
  `frame-src` da CSP — hoje é `script-src 'self'`. Não pague esse preço antes de ter o
  problema.

**Descarte os números que circulam** ("29% abandonam com CAPTCHA", "honeypot pega 80-90%"):
todos vêm de blog de fornecedor de CAPTCHA. A recomendação acima se sustenta pelo
raciocínio de custo, não por esses percentuais.

### 4.10 As duas coisas que quebram o deploy se ela esquecer

1. **CSP.** A página do formulário precisa de
   `form-action https://formsubmit.co` e `connect-src 'self' https://formsubmit.co`.
   Se o formulário for para dentro do `servicos.html`, que hoje tem `form-action 'none'`,
   **nada envia** e o erro só aparece no console.
2. **Lista de inclusão do deploy.** `briefing.html`, a tela de obrigado e o JS novo
   precisam entrar **nos dois lugares** do `deploy-pages.yml`: em `on.push.paths` (senão
   o push não dispara publicação) e no `cp` (senão não vão para o `_site`). E o `cp`
   falha de propósito se um arquivo listado sumir.

---

## 5. Depois do envio

Aviso de honestidade: como disse em 1.9, esta é a seção com **menos base experimental**.
O que existe sobre tela de obrigado é material de fornecedor. A parte com evidência de
verdade é o **prazo de resposta** (HBR, 2.241 empresas auditadas). Escrevi as
recomendações de forma que a parte forte carregue a fraca.

### 5.1 Tela de confirmação

**Página própria** (`obrigado.html`), não mensagem inline. Razão prática: o FormSubmit
manda o usuário para algum lugar depois do envio de qualquer forma — melhor que seja uma
página dela, com o `_next`. E dá URL para medir.

Três coisas, nessa ordem:

> **Recebi seu briefing.**
>
> Vou ler com calma e te responder **em até 1 dia útil**, com uma proposta de escopo —
> e não só um preço solto.
>
> Se for urgente, me chama no WhatsApp: [número]
>
> Enquanto isso, dá uma olhada nos [projetos] ou no [Instagram].

Por que assim: **confirma** (recebi), **datar** (1 dia útil), **dar saída** (WhatsApp para
quem tem pressa) e **ocupar a espera** (portfólio). A última linha é a única que é
palpite meu, não evidência.

**Não** repita o formulário nem mostre "sua mensagem foi enviada com sucesso" seco.

### 5.2 E-mail automático de recebimento

Use `_autoresponse` do FormSubmit. É estático — não personaliza. Então escreva genérico
e útil:

> Assunto: **Recebi seu briefing — Savylla Adryan**
>
> Oi! Seu briefing chegou.
>
> Vou responder em até 1 dia útil com uma proposta de escopo: o que eu faria, em quanto
> tempo e o investimento.
>
> Se algo mudou ou você esqueceu de contar alguma coisa, responde este e-mail — chega
> direto em mim.
>
> Se for urgente: [WhatsApp]
>
> Savylla Adryan · [site]

Serve a três funções: prova que o envio funcionou (o medo nº 1 de quem preenche
formulário), repete o prazo, e abre um canal de correção que evita que ela receba um
segundo briefing duplicado.

### 5.3 O prazo prometido

**Recomendação: prometa 1 dia útil. Responda no mesmo dia quando der.**

Por quê: a auditoria do HBR mostra que **23% das empresas simplesmente nunca respondem**
e 24% levam mais de 24 horas. A régua é baixíssima — prometer 1 dia útil e cumprir já
coloca ela na frente da maioria. E "1 dia útil" é uma promessa que uma pessoa autônoma
sozinha consegue honrar num dia de gravação; "responderei em minutos" não é.

**Não use** as frases de "5 minutos ou 100x menos chance" que circulam — 1.9 explica por
que aquele número não é do HBR e não deve embasar promessa dela.

A promessa aparece em **três lugares**, com o mesmo texto: no botão de envio, na tela de
obrigado e no e-mail automático. Prazo diferente em lugares diferentes destrói a
credibilidade dos três.

### 5.4 O que ela faz com a resposta

O formulário só vale se mudar o comportamento dela. Triagem em três linhas, na chegada:

1. **Marcou "ainda não sei" em serviço, ou "sem data definida" e sem faixa de verba** →
   isso não é proposta, é conversa. Responda oferecendo 20 minutos de chamada. Não gaste
   proposta artesanal aqui.
2. **Serviço claro + prazo + faixa de verba** → é proposta. Responda com **duas opções
   de escopo** (uma dentro da faixa, uma acima com o que a mais entrega), citando de
   volta as palavras que a pessoa usou no campo "o projeto em uma frase". Citar as
   palavras da própria pessoa é o que faz a proposta parecer feita para ela.
3. **Prazo "até 1 semana"** → responda primeiro, hoje, mesmo que só para dizer se cabe
   na agenda. Esses são os que somem se demorar.

E **duas medições**, porque sem elas ela não vai saber se o formulário funcionou. Uma
planilha simples com uma linha por briefing:

- **briefings recebidos → propostas enviadas → fechados** (a taxa que importa não é
  envio de formulário, é fechamento)
- **quantos vieram sem faixa de verba** — se for a maioria, o problema está nas faixas
  ou na microcopy do campo 7, não na existência dele.

Depois de uns 20 briefings ela tem dado próprio, que vale mais que qualquer benchmark
desta pesquisa.

---

## 6. Fontes

Marcadas por confiabilidade: **[A]** estudo com metodologia publicada · **[B]** pesquisa
de instituto sério com metodologia parcial · **[C]** praticante reputado, sem controle ·
**[D]** conteúdo de fornecedor / SEO, use só como pista · **[X]** folclore, não use.

**[A] Estudo acadêmico**
- [Nunes & Drèze — *The Endowed Progress Effect*, JCR 2006](https://www.researchgate.net/publication/23547282_The_Endowed_Progress_Effect_How_Artificial_Advancement_Increases_Effort) — o experimento do lava-rápido, ~300 clientes, 19% x 34% de conclusão. Sustenta a barra de progresso adiantada. Ressalva: não é formulário web; magnitude não transfere.
- [Bursztein et al. — *How Good Are Humans at Solving CAPTCHAs?*, IEEE S&P 2010 (PDF)](https://web.stanford.edu/~jurafsky/burszstein_2010_captcha.pdf) · [registro IEEE](https://ieeexplore.ieee.org/document/5504799/) — 318 mil CAPTCHAs, 21 esquemas; 9,8 a 28,4 s de resolução; não nativos em inglês mais lentos. Base do "sem CAPTCHA visível".
- [Oldroyd, McElheran & Elkington — *The Short Life of Online Sales Leads*, HBR 03/2011](https://hbr.org/2011/03/the-short-life-of-online-sales-leads) · [ficha HBS](https://www.hbs.edu/faculty/Pages/item.aspx?num=39955) — auditoria de 2.241 empresas: 37% em 1h, 24% acima de 24h, 23% nunca. Base do prazo de 1 dia útil. **Atenção:** os "5 minutos / 100x" que se atribuem a ele são de outro dataset (InsideSales/LRM).

**[B] Instituto de pesquisa**
- [NN/g — *Website Forms Usability: Top 10 Recommendations*](https://www.nngroup.com/articles/web-form-design/) — as 10 regras, e o número mais forte da pesquisa: **78% x 42%** de envio na primeira tentativa (estudo CHI, Seckler et al.). Base de toda a seção 4.
- [NN/g — *Placeholders in Form Fields Are Harmful*](https://www.nngroup.com/articles/form-design-placeholders/) — por que placeholder não é rótulo; rótulo flutuante como mitigação.
- [NN/g — *Marking Required Fields in Forms*](https://www.nngroup.com/articles/required-fields/) — asterisco no começo do rótulo, contraste, e "ninguém lê instrução de formulário".
- [NN/g — *Progressive Disclosure*](https://www.nngroup.com/articles/progressive-disclosure/) — fundamento dos blocos condicionais.
- [Baymard — *Required and Optional Fields* (só 14% marcam os dois)](https://baymard.com/blog/required-optional-form-fields) — 42% marcam só obrigatório, 37% só opcional (32% desses geram erro), 44% pararam na Amazon, 22% na L.L. Bean; e 15% nunca dão telefone / 35% nunca dão data de nascimento.
- [Baymard — *Minimize Form Fields* (checkout médio)](https://baymard.com/blog/checkout-flow-average-form-fields) — 11,3 campos em 2024 x 8 necessários; 17% abandonam por complexidade. Contexto é checkout, não briefing.
- [Baymard — *Touch Keyboards melhoraram só 9% desde 2013*](https://baymard.com/blog/mobile-touch-keyboards) — 60% dos 50 maiores erram 2 de 5 otimizações; casos HP e Amazon. Base de 4.7.
- [Baymard — *Touch Keyboard Types cheat sheet*](https://baymard.com/labs/touch-keyboard-types) — a tabela de `type`+`inputmode`+`autocorrect`+`autocapitalize` para copiar.
- [IBGE/PNAD — internet em 95% dos domicílios em 2025](https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/47410-internet-chega-a-95-de-domicilios-do-pais-em-2025) — 92,9% dos domicílios com rede móvel funcional. Contexto mobile Brasil.
- [MobileTime — internet móvel nas classes D/E](https://www.mobiletime.com.br/noticias/05/01/2026/internet-movel-classesde/) — 48% (2017) → 78% (2025) de acesso por celular.

**[B/C] Dado de plataforma, metodologia parcial**
- [Unbounce — metodologia do Conversion Benchmark Report](https://unbounce.com/conversion-benchmark-report/methodology/) — 41 mil páginas, 464 M visitantes, 57 M conversões, mediana 6,6%. A melhor metodologia aberta de benchmark que achei. Mas **não** dá curva por número de campos.
- [Zuko — dados de benchmarking de formulário](https://www.zuko.io/blog/zuko-benchmarking-data-how-does-your-form-compare) — 100 M+ sessões: completude 45%; desktop 55,5% x mobile 47,5%; senha 10,5% e telefone 6,3% de abandono no campo. Base do "campo pessoal é caro" e do argumento mobile.
- [MarketingExperiments — teste de comprimento de formulário do Marketo](https://marketingexperiments.com/lead-generation/lead-generation-testing-form-field-length-reduces-cost-per-lead-by-10-66) — 5/7/9 campos → 13,4%/12%/10% e CPL US$ 31,24/34,94/41,90. O teste real mais útil de toda a pesquisa; único que quantifica o preço de um campo de qualificação.

**[C] Praticante reputado**
- [Wroblewski/Etre — *Inline Validation in Web Forms* (A List Apart)](https://alistapart.com/article/inline-validation-in-web-forms/) · [resumo do autor](https://www.lukew.com/ff/entry.asp?883=) — +22% sucesso, −22% erro, −42% tempo; **e o achado que importa: validar no `blur` ganha**; "antes e enquanto" é o pior. **O autor declara: 22 participantes, "indicativo, não definitivo".** Use a direção, não os percentuais.
- [GOV.UK Design Notes — *One thing per page* (Caroline Jarrett, 2015)](https://designnotes.blog.gov.uk/2015/07/03/one-thing-per-page/) — a doutrina, e a razão publicada (mobile, erro, ramificação, salvar). Base da decisão de multi-step, sem depender de percentual nenhum.
- [Deque University — WCAG 2.1 §1.3.5 Identify Input Purpose](https://dequeuniversity.com/resources/wcag2.1/1.3.5-identify-input-purpose) — requisito AA de `autocomplete`. Não é opinião, é norma.
- [CXL — *5 A/B Tests for Opt-In Forms*](https://cxl.com/blog/ab-testing-forms/) — o lado "longo qualifica melhor", e a recomendação de perguntar orçamento. Prática, não resultado medido. Também traz o caso 20→4 campos / +188% (anedota).
- [BCG/Meta via Agendor — WhatsApp no Brasil](https://www.agendor.com.br/blog/whatsapp-brasil/) — 8 em 10 preferem mensagem; 89% usam WhatsApp com empresa. **Conflito de interesse declarado: a Meta é co-autora e dona do WhatsApp.** Direção sim, magnitude não.

**[D] Repassa terceiros, sem dado próprio**
- [Zuko — *Single page or multi-step form*](https://www.zuko.io/blog/single-page-or-multi-step-form) — abri esperando dado próprio de uma empresa de form analytics e **não há**: só repassa HubSpot, Conversion Fanatics e Venture Harbour. Útil só como prova de deriva: cita o teste da HubSpot como **"86%"** onde outros citam **"59,2%"**.
- [Venture Harbour — 5 estudos sobre comprimento de formulário](https://ventureharbour.com/how-form-length-impacts-conversion-rates/) — origem de vários "+300%" que circulam. Casos sem metodologia.

**[X] Folclore — identifiquei a origem ou a ausência dela**
- **"3 campos garantem 25% de conversão"** — infográfico do QuickSprout, sem estudo. "Garantir" conversão é impossível.
- **"4 → 3 campos = +50%"** — HubSpot 2012, metodologia nunca publicada, citação circular.
- **"−4,1% por campo"** e **"23,1% / 17,0% / 11,4% / 6,9% por número de campos"** — [digitalapplied.com](https://www.digitalapplied.com/blog/form-conversion-rate-benchmarks-2026-data-points): perguntei pela fonte, lista sete nomes em bloco **sem um link, relatório, data ou amostra**. Circula como benchmark em vários sites de 2026.
- **"Campo de orçamento = −15,3% de conversão"** — [brixongroup.com](https://brixongroup.com/en/lead-forms-in-b2b-the-perfect-balancing-act-between-data-depth-and-conversion-rate): cita Formstack/Forrester/Marketo sem abrir como o número foi isolado. Direção plausível, número não verificável.
- **"Multi-step converte +300% / +743% / +214% / +59,2% / +86% / +160%"** — todos de case de fornecedor sem metodologia, e com o mesmo estudo aparecendo com números diferentes.
- **"29% abandonam ao ver CAPTCHA"**, **"CAPTCHA reduz 3-4% dos envios"**, **"honeypot pega 80-90% dos bots"**, **"78% dos bots preenchem todo campo (OWASP 2024)"** — todos de blog de fornecedor de CAPTCHA, parte interessada, nenhum com metodologia. Não achei estudo independente de perda de conversão por CAPTCHA.

**Lacunas que eu não consegui fechar — assuma como não sabido, não como resolvido:**
1. Nenhum estudo controlado provando que formulário longo **fecha mais negócio** em serviço criativo. A recomendação de 2.2/2.7 é inferência de custo de oportunidade, marcada como tal.
2. Nenhum experimento limpo sobre **nome/e-mail no começo x no fim**. A decisão de 2.3 se sustenta numa característica do stack (não há captura parcial), não em benchmark.
3. Nenhum estudo sobre **tela de obrigado e e-mail de recebimento** — só material de fornecedor. Seção 5.1/5.2 é boa prática sem base experimental; o prazo (5.3) é a única parte com evidência.
4. Nenhum dado confiável de **share de tráfego mobile do Brasil**. Premissa razoável, não confirmada.
