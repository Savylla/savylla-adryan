# Formulário de briefing — consolidado

Documento de decisão. Reúne as 9 pesquisas desta pasta num único desenho,
já com as escolhas travadas pela Savylla em 13/08/2026.

Os relatórios individuais continuam sendo a fonte: cada campo aqui tem um "de onde
vem" apontando para o arquivo que o justifica. **Este documento corta muito** — os 7
relatórios somam ~110 campos, e o que cabe num formulário que o cliente termina são
~14. O que ficou de fora não foi descartado: virou pergunta da primeira resposta dela.

---

## 1. Decisões travadas

| Decisão | Escolha | Consequência |
|---|---|---|
| Plataforma | **HTML nativo no site**, envio pelo FormSubmit que já roda no `index.html` | Zero fornecedor novo, zero custo, identidade visual preservada. A lógica condicional vira JS a escrever e manter. |
| Arquitetura | **Um formulário só**, `briefing.html`, que se adapta ao serviço | Um tronco, sete blocos. Atende quem combina frentes. Link por serviço: `briefing.html?servico=filmmaker` chega com a caixa marcada. |
| Verba | **Campo aberto, opcional**, sem faixas | Nenhum número parte do site. Respeita a regra de preço nunca aparecer. |
| Upload | **Não existe.** Todo material é campo de link | Restrição do site estático — decisão técnica, não de produto. |
| Passos | **3**, num único `<form>` com fieldsets escondidos | Se o JS falhar, degrada para um formulário longo que ainda envia. |
| Contato | **No fim** | Em site estático nada é gravado antes do envio; pedir contato antes não recupera abandono. |

### A discordância que a pesquisa não resolveu

O relatório de UX recomendou **faixas** de verba; quatro relatórios de serviço
recomendaram **texto livre**. A Savylla decidiu por texto livre. O argumento que
sustenta a decisão, do relatório de Direção de Arte: *faixas prontas publicam a
escada de preço dela na página, em formato de menu* — o que colide frontalmente com
a regra do site.

O custo aceito: menos gente responde um campo aberto do que um radio. Se depois de
uns meses o campo vier vazio quase sempre, a alternativa é movê-lo para o e-mail de
retorno — não transformá-lo em faixas.

---

## 2. Contagem honesta

*Atualizada em 13/08/2026, depois da pesquisa de conformidade.*

| Bloco | Obrigatórios | Condicionais | Opcionais |
|---|---|---|---|
| Tronco (todo cliente vê) | 10 | 3 | 4 |
| Bloco do serviço | 6 a 7 | varia | varia |
| **Total por cliente** | **16 a 17** | **3+** | **4+** |

**A tensão, dita com todas as letras.** A pesquisa de UX pedia no máximo 14 campos, 10
obrigatórios. A pesquisa de conformidade acrescentou 3 campos ao tronco (T9 promovido a
obrigatório, T9a e T14) e 3 ao bloco de IA. **O formulário passou do teto de
conversão.**

Três coisas seguram o estrago, e vale conferi-las na implementação:

1. **Os campos jurídicos novos são quase todos condicionais.** T9a e T14 só aparecem
   quando há pessoa real em cena. Projeto de produto, still de catálogo ou pós-produção
   de material sem gente **não vê nenhum dos dois**.
2. **São todos de clique**, não de digitação — três radios e um checkbox. O relatório de
   Direção de Arte já tinha notado: um formulário de 16 campos onde 12 são cliques
   termina; um de 10 campos onde 8 são caixas de texto, não.
3. **O trade-off foi escolhido, não sofrido.** Perder alguns leads no formulário custa
   menos que uma notificação por uso de imagem — e o caso do TJSP mostra que o que
   defende a produtora é justamente a verificação prévia registrada.

Se na prática a conversão cair demais, o corte deve sair de **T5a** (data travada) ou
**T2** (link da marca), que são conveniência. Nunca de T9a ou T14.

Isso está **acima** do teto de 10 obrigatórios que o relatório de UX recomendou, e a
escolha é consciente: este é um formulário de orçamento, onde qualidade de lead vale
mais que volume, e a finalidade declarada é *responder com proposta em uma rodada*.
Cada campo abaixo passou pela régua: **muda preço, prazo, formato ou risco — ou sai.**

O que segura a queda de conversão: 3 passos curtos, maioria de cliques e não de
digitação, zero jargão, e condicionais que escondem o que não se aplica.

**Quem marca 3 ou mais frentes** não vê 3 blocos somados (viraria 30 campos): vê um
bloco combinado com o mínimo de cada, e a proposta abre com uma conversa. Regra do
relatório de UX, adotada.

---

## 3. O tronco

Vale para todo mundo. Microcopy pronta para colar.

### Passo 1 — O que você precisa

**T1. Frentes de trabalho** · checkbox múltiplo · **obrigatório** (mínimo 1)

> **De que você precisa?**
> Marque quantas quiser — dá para combinar.
> ☐ Conteúdo para Redes Sociais ☐ Direção de Creators ☐ Filmmaker
> ☐ Pós-produção ☐ Fotografia ☐ Direção de Arte ☐ Produção com IA
> ☐ Ainda não sei — me ajuda a definir

A última caixa é a que segura quem não conhece o nome do serviço. E é resposta
valiosa por si: indica cliente que precisa de conversa, não de orçamento.
*De onde vem: 00-ux-e-conversao.*

**T2. Marca ou empresa** · texto + URL · **obrigatório**

> **Qual a marca ou empresa?**
> Se tiver site ou Instagram, cola aqui — eu dou uma olhada antes de responder.
> *(Se for projeto pessoal ou ainda sem nome, escreve só o nome do projeto.)*

O link substitui cinco perguntas de contexto: ela vê sozinha o mercado, o padrão
visual atual e o nível de acabamento esperado.
*De onde vem: 06-direcao-de-arte, 01-conteudo-redes-sociais, 05-fotografia.*

**T3. A ideia** · textarea 3–4 linhas · **obrigatório**

> **Me conta a ideia.**
> Do jeito que você contaria por áudio. Não precisa escrever briefing — três ou
> quatro linhas bastam.

Campo aberto único do tronco. Substitui objetivo, público-alvo e mensagem-chave em
caixas separadas, que é onde os modelos de mercado ficam longos e vazios.
*Convergência dos 7 relatórios.*

### Passo 2 — Como é o projeto

**T4. Onde vai rodar** · checkbox múltiplo · **obrigatório**

> **Onde isso vai aparecer?**
> Marque tudo que já é certo — é o que define formato, tamanho e quantidade de entrega.
> ☐ Instagram / TikTok ☐ YouTube ☐ LinkedIn ☐ Site ou e-commerce
> ☐ Anúncio pago (impulsionado) ☐ Impresso, PDV ou evento
> ☐ Uso interno / apresentação ☐ Ainda não sei

**T4a. Por quanto tempo e onde** · select duplo · **obrigatório, condicional**
*(só aparece se marcar "anúncio pago" ou "impresso, PDV ou evento")*

> **Por quanto tempo isso vai ficar no ar, e só na internet ou também fora dela?**
> Tempo: ○ até 3 meses ○ 6 meses ○ 1 ano ○ sem prazo definido ○ não sei
> Onde: ○ uma cidade ou região ○ Brasil todo ○ fora do Brasil também ○ não sei

Este par de campos é o que mais aparece nas sete pesquisas, por motivos diferentes
que chegam no mesmo lugar: a Lei 9.610/98 exige **tempo e lugar** no instrumento de
cessão (fotografia e design), e o guia APRO trata a veiculação como a **segunda face
do contrato**, com prazo próprio e renovação (audiovisual). Perguntado em português
de negócio, sem as palavras "licença" ou "cessão".
*De onde vem: 05-fotografia, 06-direcao-de-arte, 01-conteudo-redes-sociais, 03-filmmaker.*

**→ Aqui entra o BLOCO DO SERVIÇO (seção 4).**

**T5. Quando precisa estar pronto** · select · **obrigatório**

> **Para quando?**
> ○ Até 1 semana ○ 2 a 4 semanas ○ 1 a 2 meses ○ Mais de 2 meses
> ○ Sem data definida ainda

Select e não campo de data: a maioria não tem data exata e date picker no celular é
tortura. "Sem data definida" evita resposta inventada — e é sinal de lead menos maduro.

**T5a. Essa data é travada?** · radio · **obrigatório**

> ○ Travada — tem lançamento, evento ou feira em cima
> ○ Tenho uma preferência, mas dá para conversar

Separar desejo de compromisso. Urgência é fator de preço em todas as fontes de
precificação levantadas; sem esse campo, toda data vira urgência.
*De onde vem: 06-direcao-de-arte.*

**T6. Quem dá o ok final** · radio · **obrigatório**

> **Quem dá a palavra final?**
> ○ Sou eu ○ Eu e mais uma pessoa ○ Passa por um time ou comitê
> ○ Passa pelo jurídico ○ Ainda não está definido
> *Quanto mais gente aprova, mais rodadas o projeto pede. Prefiro já contar isso na proposta.*

**Convergência unânime: os 7 relatórios pediram este campo.** É proxy direto de
rodadas de revisão (o padrão de mercado é 2 a 3 inclusas) e é qualificação: mostra se
quem preenche decide. "Ainda não está definido" é o sinal mais forte de todos — a
proposta pode incluir definir o decisor como primeira etapa.

**T7. Já existe algo pronto?** · textarea + links · *opcional*

> **Já existe roteiro, manual de marca, referência ou material bruto?** *(opcional)*
> Cola links aqui. Arquivo grande, manda o link do Drive ou WeTransfer.

### Passo 3 — Fechamento

**T8. Verba** · texto livre · *opcional*

> **Já existe verba definida?** *(opcional)*
> Se puder me dizer a ordem de grandeza, eu já monto a proposta dentro dela — em vez
> de te mandar algo fora da realidade. Se ainda não tem, escreve "ainda não" que eu
> proponho os caminhos.

Texto livre, sem número sugerido, sem faixa. Ver seção 1.

**T9. Posso usar no meu portfólio?** · radio · **obrigatório**

> **Posso mostrar esse trabalho depois?**
> ○ Sim, quando estiver publicado ○ Sim, mas me avise antes
> ○ Só com aprovação de vocês por escrito ○ Não, é confidencial
> *Meu portfólio é como novos clientes me encontram. Combinar isso agora evita ter
> que perguntar depois — e se for confidencial, tudo bem, é só me dizer.*

Nasceu na pesquisa de fotografia e vale para as sete frentes: **este site é o motor
comercial dela** — 540 vídeos e 63 marcas viraram portfólio. Descobrir NDA depois de
fechar é tarde, e sigilo é variável de preço.
*De onde vem: 05-fotografia, 03-imagem-voz-e-biometria §8.*

> ⚠️ **Promovido a obrigatório em 13/08/2026.** A pesquisa de imagem e voz classificou
> a ausência deste campo como *"a omissão mais cara do conjunto"*: o formulário inteiro
> cuidava da produção e nada cuidava do direito dela de **mostrar o resultado**.

**T9a. A autorização de quem aparece cobre o portfólio?** · radio · **obrigatório, condicional**
*(só aparece se houver pessoa real em cena e T9 ≠ "não, é confidencial")*

> **A autorização assinada por quem aparece cobre mostrar o vídeo no portfólio de
> quem produziu?**
> ○ Sim ○ Não ○ Não sei
> *Pergunto porque a autorização costuma valer para a campanha de vocês, não para o
> site de quem produziu. Se não cobrir, é uma linha a mais no termo — resolve em um
> minuto agora, e não resolve depois.*

**O campo que ataca o problema dos três polos.** O contrato entre ela e a marca **não
vincula a pessoa filmada**: por mais cláusula que o cliente assine, quem autoriza o uso
da própria imagem é quem aparece. Sem tocar no termo do talento, o portfólio continua
exposto. Hoje o site publica **84 nomes próprios** no campo `talento`, ao lado dos
rostos, sem autorização escrita para esse uso específico.
*De onde vem: 03-imagem-voz-e-biometria §6 e §8.*

**T10. Nome** · texto · **obrigatório** · `autocomplete="name"`
**T11. E-mail** · e-mail · **obrigatório** · `autocomplete="email"` · `inputmode="email"`
> *É por aqui que eu mando a proposta.*

**T12. WhatsApp** · tel · *opcional* · `autocomplete="tel"` · `inputmode="tel"`
> *Se preferir que eu responda por aqui, é mais rápido.*

Opcional de propósito: telefone é campo de alto abandono, e no Brasil o WhatsApp é
onde a pessoa provavelmente prefere. Oferecer sem exigir pega os dois públicos.

**T13. Algo mais** · textarea · *opcional*
> **Quer me contar mais alguma coisa?**

Todo formulário com roteamento perde casos. É aqui que eles aparecem — e, segundo
três dos relatórios, é onde costuma aparecer algo caro.

**T14. Declaração** · checkbox · **obrigatório** *(só aparece se houver pessoa real em cena)*

> ☐ **Confirmo que as informações acima são verdadeiras e que, quando houver pessoas
> no material, os direitos de uso de imagem e voz estão em ordem do nosso lado.**
> *Isso vira parte da proposta. Não é pegadinha — é o que me permite tocar o projeto
> sem travar tudo em jurídico.*

**Perguntar gera informação; declarar gera prova.** É a diferença entre saber e poder
cobrar depois. O peso disso vem de um caso real: no TJSP, ao julgar um comercial com
voz sintética, o tribunal listou entre o que precisaria ser apurado **"quem foi
contratado para produzi-la, se houve algum tipo de verificação prévia"** — e registrou
que *"o uso de Inteligência Artificial, por si só, não elimina — bem pelo contrário,
agrava — o risco de utilização indevida de direitos de terceiros"*.

O que defende a produtora é **ter verificado antes, por escrito**. Este checkbox é esse
registro.
*De onde vem: 03-imagem-voz-e-biometria §2, §5 e §8.*

**Botão:**
> **Enviar briefing** — *Eu respondo em até 1 dia útil.*

O prazo fica **no botão**, não só na tela de obrigado: a pessoa decide enviar já
sabendo o que vem depois.

---

## 4. Os sete blocos de serviço

Entram entre T4a e T5. Cada bloco tem no máximo 7 campos.

### 4.1 Conteúdo para Redes Sociais — 6 campos

| # | Campo | Tipo | Microcopy | Por quê |
|---|---|---|---|---|
| A1 | Gravar ou já existe | radio | **"A gente vai gravar ou o material já existe?"** ○ Preciso gravar ○ Já tenho o bruto, quero só edição ○ Um pouco de cada | Bifurcação central do escopo. "Já tenho" é, na prática, Pós-produção. **Nenhum modelo de brief de redes sociais do mercado pergunta isso.** |
| A2 | Volume e ritmo | número + select | **"Quantos vídeos você imagina — e em que ritmo?"** ___ vídeos · por mês / no total · durante 1, 3, 6 meses ou projeto único | Eixo de escala do pacote. O select de período resolve, no mesmo campo, se é projeto único ou canal contínuo — que é outro tipo de contrato. |
| A3 | Onde grava e quantos dias | select + número | *(condicional: só se A1 ≠ "já tenho")* **"Onde a gente grava? E quantos dias de gravação você acha que dá?"** *Um dia bem aproveitado rende muito vídeo. Se não souber, deixa em branco que eu proponho.* | O eixo de custo mais pesado. **Uma diária rende de 10 a 30 entregas — o que precifica é a razão peças/diária, não o número de peças.** |
| A4 | Cidade | texto | *(condicional)* **"Em que cidade?"** | Deslocamento é linha separada de orçamento. |
| A5 | Quem aparece | radio | *(condicional)* **"Quem aparece na frente da câmera?"** ○ Ninguém, só produto/ambiente ○ Gente da empresa ○ Ator ou modelo ○ Um creator ○ Ainda não decidimos | Ativa o tripé de direitos da APRO (produtora + diretor + elenco) e a autorização de imagem. "Creator" sugere a frente 02. |
| A6 | Estratégia | radio | **"O que falar já está definido?"** ○ Temos o planejamento pronto ○ Temos ideias soltas ○ Preciso que você monte a estratégia | A estratégia está no escopo do serviço. Se o cliente já tem calendário, esse bloco sai da proposta. Diferença real de preço que **nenhum modelo de mercado captura**, porque todos assumem que a marca chega com a estratégia. |

**Cortado:** link do canal (absorvido em T2), manual de marca (só aparece se marcar
também Direção de Arte), redes específicas (T4 cobre).

### 4.2 Direção de Creators — 6 campos + 2 condicionais

| # | Campo | Tipo | Microcopy | Por quê |
|---|---|---|---|---|
| B1 | Setor regulado | select | **"A marca está em setor com regra de publicidade?"** Saúde/farma/suplemento · Alimento ou bebida · Bebida alcoólica · Financeiro/crédito · Apostas · Infantil · Nenhum desses · Não sei · *Pergunto porque muda o jeito de dirigir: em setor regulado a frase é a frase, e a gente ensaia para soar natural sem mudar palavra.* | **O campo mais importante do bloco.** Roteia todo o compliance e sinaliza o job de maior valor dela. |
| B1a | Jurídico | radio | *(condicional: se B1 ≠ "nenhum")* **"O texto já passou pelo jurídico?"** ○ Passou e não muda uma palavra ○ Passou, mas dá para ajustar com nova aprovação ○ Ainda não passou ○ Não tem jurídico envolvido | Peça aprovada em fluxo regulado fica travada e não muda sem novo ciclo. É o que define se o trabalho é "tirar naturalidade de texto imutável" — a especialidade que o site vende. |
| B1b | Restrições | textarea | *(condicional)* **"Tem palavra proibida, frase obrigatória ou coisa que não pode aparecer em cena?"** *Vale 'não pode dizer que cura', 'tem que ter a tarja', 'beba com moderação'.* | Descobrir em set custa a diária. |
| B2 | Quantos creators | select | **"Quantos creators entram nessa?"** 1 · 2 a 4 · 5 a 10 · mais de 10 · ainda não fechou | Multiplica preparação, set e trabalho de consistência. |
| B3 | Dias e horas | select duplo | **"Quantos dias de gravação, e quantas horas por dia?"** *Chute se precisar. Eu volto com o número certo na proposta.* | **A unidade de cobrança.** A tabela sindical remunera Diretor de Cena por bloco de tempo, base 8h/dia — não por vídeo. |
| B4 | Presencial ou remoto | radio | **"Eu vou estar no set ou entro por chamada?"** ○ Presencial ○ Remoto, entro por vídeo ○ Um pouco de cada · *Dirigir por chamada funciona e eu faço — só preciso de internet firme e um segundo aparelho do lado do creator.* | Deslocamento e hospedagem, ou requisito técnico do remoto. Linha de orçamento nos dois casos. (Cidade vem em campo condicional se presencial.) |
| B5 | Quem contrata o creator | radio | **"Quem contrata e paga o creator?"** ○ A marca ○ A agência ○ Ainda não definimos · *Só para eu saber com quem alinho agenda. Eu não entro no cachê do creator.* | **Se ninguém contratou, a data não é real.** Substitui todo o bloco de direitos/exclusividade do creator, que mexe no cachê dele e não na diária dela. |

**Cortado:** métricas do creator, KPIs de mídia, hashtag/#publi (obrigação do
anunciante), direitos e exclusividade do creator.

### 4.3 Filmmaker — 7 campos

Exceção justificada ao teto de 6: o passo 3 é o **detector de limite do formato solo**,
e ele precisa dos três campos juntos para funcionar.

| # | Campo | Tipo | Microcopy | Por quê |
|---|---|---|---|---|
| C1 | Quantos dias | select | **"Quantos dias de gravação você imagina?"** 1 · 2 · 3 a 5 · mais de 5 · não sei | Unidade de preço do serviço. |
| C2 | Cidade e estado | texto | **"Em que cidade a gravação acontece?"** | Deslocamento, viabilidade de ida e volta, hospedagem acima de ~200 km. **O tempo de deslocamento conta dentro da diária** (tabela ASTIM/Sindcine). |
| C3 | Quantos lugares | select | **"São quantos lugares diferentes de gravação?"** 1 · 2 · 3 ou mais · ainda definindo → *(se ≠1)* **"Entram no mesmo dia ou em dias separados?"** | Duas locações num dia é jornada estourada; em dois dias é outra diária. |
| C4 | Tipo de gravação | select | **"Como é essa gravação, na prática?"** depoimento/entrevista · cena dirigida com roteiro · cobertura de evento · produto/mesa/detalhe · conteúdo com creator · mistura | Quatro operações diferentes com o mesmo nome. Define luz, som, setup — e se o formato solo atende. |
| C5 | Quem aparece | checkbox | **"Quem vai aparecer no vídeo?"** ninguém · pessoas da empresa · creator ou apresentador · atores contratados · figuração · não sei → *(se ator/figuração)* **"Quantas pessoas em cena?"** | Ator e figuração mudam o regime por via legal: DRT, AET, seguro, camarim. Não é só operacional. |
| C6 | Horário no dia | select | **"Quanto tempo a gravação deve ocupar no dia?"** até 4h · até 8h · vai passar de 8h · à noite ou madrugada · não sei | A régua da CCT é 8h; acima é hora extra de 50%/100%, depois das 22h é adicional noturno. **Sem esse campo, hora extra vira prejuízo silencioso.** |
| C7 | Precisa de algo além de mim | checkbox | **"Tem alguma coisa nessa lista que o projeto pede?"** drone · segunda câmera simultânea · maquiagem · teleprompter · estúdio alugado · trilha licenciada · arquivos brutos no fim · nada disso · não sei | Cada item é linha de orçamento ou licença própria. **Drone é serviço regulado — SISANT + SARPAS por operação.** |

**O detector.** Se marcar *atores* ou *figuração com mais de 3 pessoas*, **ou** *cena
dirigida* junto com *drone* ou *segunda câmera simultânea*, mostrar abaixo — como
informação, não erro:

> "Esse projeto provavelmente pede mais gente em set do que uma pessoa só. Eu continuo
> na direção e monto o time necessário — só já te aviso para a proposta não te surpreender."

Protege a promessa da página ("equipe reduzida") sem perder o lead. O teto documentado
do set solo é ~2 câmeras, 2 pessoas em cena, 3–5 luzes com som; acima disso o áudio
fica sem mão livre.

### 4.4 Pós-produção — 7 campos

| # | Campo | Tipo | Microcopy | Por quê |
|---|---|---|---|---|
| D1 | Natureza | select | **"Como é esse trabalho?"** um vídeo só · um lote · canal com publicação recorrente · acervo parado que quero destravar | Separa pontual de recorrência (contrato mensal) antes do valor. Se for recorrente, D2 vira "quantos por mês". |
| D2 | Quantos e que duração | texto guiado | **"Quantos vídeos precisam sair, e com que duração cada um?"** *Chute. "Uns 4 vídeos de 1 minuto" já me serve.* | Base do cálculo: ≈1h de trabalho por minuto finalizado, **em cada fase**. |
| D3 | Quanto material bruto | select + escape | **"Quanto material bruto você tem?"** até 1h · 1 a 5h · 5 a 20h · mais de 20h · **não sei, o link responde** · *Essa é a informação que mais muda o orçamento, então um chute honesto vale mais que um número redondo.* | Razão bruto:final é o **driver nº 1** de preço e prazo. |
| D4 | Estado do material | select | **"Em que estado está esse material?"** tudo bruto · os melhores trechos já marcados · tem roteiro ou ordem definida · existe um corte antigo para refazer | Define as horas de decupagem — é aqui que volume vira custo. |
| D5 | **Arquivo de amostra** | URL | **"Manda o link de UM arquivo bruto, do jeito que saiu da câmera."** *Só um clipe. Eu abro a ficha técnica dele e descubro sozinha o formato, a resolução e a taxa de quadros. Assim você não precisa procurar nada disso.* | **O campo mais valioso do formulário inteiro. Substitui 6 perguntas técnicas** que o cliente leigo erraria: codec, resolução, frame rate, log/RAW, peso por hora, câmera de origem. |
| D6 | Como chega | select + URL | **"Como você pretende me mandar?"** Drive · WeTransfer · Frame.io · MASV/Dropbox · disco físico · ainda não organizei · *WeTransfer grátis não passa de 3 GB, o que dá menos de 4 minutos de vídeo em qualidade alta.* | Viabilidade. **Validação inline:** se D3 ≥ 5h **e** D6 = WeTransfer, avisar na hora em vez de descobrir três e-mails depois. |
| D7 | O que entra no acabamento | multiselect | **"O que você quer que entre no acabamento?"** montagem · cor · motion/vinheta/cartelas · abertura, selos e tarjas · legenda · áudio e mixagem · entrega por plataforma · **não sei, me diga o que esse material precisa** | Motion e cor avançada são multiplicadores de tarifa, não adicionais. O escape evita que o cliente desmarque algo que o material exige. Legenda abre condicional de idioma — tradução é outra ordem de grandeza. |

**Condicional importante:** se D7 incluir áudio, ou se houver áudio em aparelho
separado, perguntar **"O som gravado no aparelho separado já está encaixado com a
imagem?"** — com timecode é um comando, sem é claquete por claquete.

**Cortado:** os 9 campos técnicos (substituídos por D5), proxies, LUT, objetivo/
público/funil (é briefing de acabamento, não de campanha), nº de rodadas desejadas
(T6 já responde).

### 4.5 Fotografia — 1 bifurcação + 6 campos

**E0. Tipo de foto** · radio · **obrigatório** — o único ponto de decisão:

> **O que você precisa fotografar?**
> ○ **Um evento** — festival, confraternização, congresso, ativação → caminho A
> ○ **O bastidor de uma produção** — making of, ensaio, set → caminho A
> ○ **Foto planejada de produto ou campanha** — still, catálogo, key visual → caminho B
> ○ **As duas coisas** → A e B

**Caminho A — cobertura (6 campos)**

| # | Campo | Microcopy | Por quê |
|---|---|---|---|
| EA1 | Data e local | **"Quando é? E onde — cidade e nome do espaço."** | Gate binário de agenda + deslocamento. |
| EA2 | Janela de cobertura | **"A cobertura precisa começar e terminar quando?"** das ___ às ___ | **Variável primária de preço.** Duas horas de coquetel e oito de congresso são orçamentos diferentes. |
| EA3 | Que evento e quanto público | textarea curto | Porte muda equipamento e logística. |
| EA4 | O que não pode faltar | textarea + link | **"Cronograma, discurso, premiação, foto oficial. Se tiver a programação em PDF, cola o link — funciona melhor que descrever."** | O shot list é o que evita "você não fotografou isso". |
| EA5 | Dois lugares ao mesmo tempo | radio | **"Vai ter coisa importante acontecendo em dois lugares ao mesmo tempo?"** | **Decide segundo fotógrafo** — a diferença entre cobrir tudo e escolher o que perder. |
| EA6 | Prévia | radio | **"Você precisa de foto ainda durante o evento?"** ○ sim, para postar na hora ○ no mesmo dia à noite ○ no dia seguinte ○ não, prefiro tudo tratado com calma · *Postar na hora muda a forma de trabalhar (edito em campo), então precisa estar combinado antes.* | **O campo de maior alavancagem do caminho A.** Prévia same-day tem adicional de 25–50% nas referências e já é oferta de prateleira de concorrente brasileiro. |
| EA7 | Autorização de imagem | radio | **"Quem cuida da autorização de uso de imagem dos convidados?"** ○ a gente coleta na inscrição ou entrada ○ ainda não pensamos nisso ○ não vai ter gente identificável · *Isso é da organização do evento, não minha — mas eu preciso saber para não te colocar num problema depois.* | LGPD. **O formulário não coleta autorização de ninguém — só pergunta quem se responsabiliza.** Coletar dado de terceiro num formulário de orçamento feriria minimização. |

*(São 7 — EA7 é curto e é proteção jurídica; mantido.)*

**Caminho B — still (6 campos)**

| # | Campo | Microcopy | Por quê |
|---|---|---|---|
| EB1 | Quantos itens | número | **"Quantos produtos ou itens diferentes vamos fotografar?"** | O SKU é a unidade de orçamento. |
| EB2 | Fotos por item | radio | **"Quantas fotos de cada um?"** 1 · 2–3 ângulos · 4–6 · não sei, me sugere | Segundo fator do volume. Junto com EB1, **a unidade real de orçamento**. |
| EB3 | Tipo de imagem | radio | **"Como você imagina as fotos?"** ○ fundo branco, tipo catálogo ○ cena montada, com clima de campanha ○ as duas | **A maior bifurcação de custo interna.** Não são o mesmo trabalho nem o mesmo dia. → se "cena montada", abre **"Quem providencia os objetos de cena?"** |
| EB4 | Pessoa na foto | radio | **"Vai ter gente na foto?"** ○ modelo ○ só mão ou parte do corpo ○ alguém da equipe de vocês ○ ninguém | Modelo é diária extra + termo de imagem. |
| EB5 | Onde e como o produto chega | radio + condicional | **"Onde vamos fotografar?"** estúdio · sua empresa · locação · você decide → *(se não for na empresa)* **"Como o produto chega até mim?"** *Me diz também se precisa voltar depois — e quando.* | Estúdio é diária extra. Logística de produto é o que atrasa a produção inteira quando fica para depois. |
| EB6 | Recorte e tratamento | radio duplo | **"Precisa do produto recortado, sem fundo?"** + **"Que nível de acabamento?"** ○ o padrão — cor, luz e limpeza, pronta para publicar ○ avançado — montagem, troca de fundo, retoque | Clipping path é serviço adicional, não "tratamento incluído". Separa a promessa do site do retoque avançado. |

### 4.6 Direção de Arte — 1 roteador + 5 comuns + caminho

**F0. Roteador** · radio · **obrigatório** — escrito como situação, não como nome de serviço:

> **O que você precisa resolver?**
> ○ **"Minha marca precisa de uma cara."** *Do zero, ou refazendo. Logo, cores, tipografia, e o manual para o time seguir.* → **A**
> ○ **"Tenho uma campanha e preciso do visual dela, em todos os lugares onde ela vai aparecer."** → **B**
> ○ **"Preciso de uma peça específica."** *Mídia kit, apresentação, folder, catálogo, embalagem.* → **C**
> ○ **"Tenho um time criando e preciso de alguém segurando o padrão visual."** → **D**
> ○ **"É mais de um desses, ou não sei encaixar."** → **B** + campo livre

**Comuns aos quatro caminhos (5 campos):**

| # | Campo | Microcopy | Por quê |
|---|---|---|---|
| F1 | Manual de identidade | **"Você já tem manual de identidade?"** ○ sim, manual fechado (regras de uso, cores, tipografia) ○ tenho o logo e umas cores, mas nada escrito ○ não tenho nada ainda | **A pergunta que mais muda o trabalho.** Três estados, não dois — "tenho o logo em PNG" não é ter manual, e é o caso mais comum. Define criar sistema × aplicar sistema. |
| F2 | Material de marca | **"Se tem material de marca, joga aqui."** *Manual, logo em vetor, paleta, fontes. Link de pasta serve.* *(condicional: se F1 ≠ "não tenho nada")* | Vetor × PNG é diferença de horas. |
| F3 | **Formatos por peça** | **"Cada peça vai precisar de quantos formatos diferentes?"** *Um post pode virar 1:1, 4:5 e 9:16 — cada versão é uma arte.* 9:16 · 1:1 · 4:5 · 16:9 · vertical impresso · horizontal impresso | **O multiplicador silencioso — o campo mais importante do bloco.** "Um anúncio de rede social não é um entregável." Entregável vago é a principal fonte de scope creep. O texto de apoio ensina o cliente por que a pergunta existe, o que é o que faz ele responder de verdade. |
| F4 | Arquivos abertos | **"Depois de entregue, sua equipe vai precisar mexer nos arquivos?"** ○ sim, vamos adaptar e criar peças novas ○ não, só vou usar o que veio pronto ○ não sei ainda | Direitos e preço. Arquivo editável é extra na prática de mercado, e no Brasil o que não está escrito não foi cedido (art. 4º da 9.610). Perguntado como necessidade de negócio, não como cláusula. |
| F5 | Referências com o porquê | **"Manda 2 ou 3 referências visuais — e diz em uma linha o que te agradou em cada uma."** *O "o que te agradou" vale mais que o link.* | A instrução de justificar é deliberada: **referência sem motivo produz cópia; referência com motivo produz critério.** Substitui as perguntas abstratas de estilo dos questionários de branding. |

**Por caminho** (detalhe completo em `06-direcao-de-arte.md` §3):
- **A — identidade:** o que vai ganhar identidade (marca nova / refeita / canal / projeto) · o logo pode mudar? · nome definido e registrado? · aplicações obrigatórias na entrega
- **B — campanha:** do que é a campanha · a única coisa que a pessoa tem que lembrar · quais peças · já existe material visual ou a arte cria a imagem? · quem escreve os textos · por quanto tempo roda
- **C — peça avulsa / mídia kit:** que peça é · quantas páginas · **os números já existem?** · tem case com resultado real? · vai ter tabela de cotas? · PDF, link ou apresentação ao vivo
- **D — coordenação:** quem cria hoje · quantas pessoas · quantas peças por semana · existe padrão escrito? · **você quer que eu decida ou que eu opine?** · projeto fechado ou mensal

**Bloco impresso** *(condicional: se T4 incluir "impresso, PDV ou evento" ou se o
caminho C for material gráfico)* — 5 campos, **todos aceitam "ainda não sei" e nenhum
bloqueia o envio**, abrindo com:

> *"Impresso tem regra própria: o arquivo é fechado do jeito que a gráfica pede, e
> depois disso não dá para mudar. Cinco perguntas rápidas — se não souber, marque
> 'ainda não sei' e eu te ajudo a definir."*

Tamanho final (aberto e fechado, se dobra) · tiragem · já tem gráfica (+ gabarito) ·
papel e acabamento (verniz, relevo, corte especial mudam o arquivo) · **a data em que
a gráfica precisa receber o arquivo** — deliberadamente separada da data do T5.
Confundir as duas é o erro de cronograma mais comum em projeto com impresso.

### 4.7 Produção com IA — 6 campos + 2 blocos condicionais

Não existe modelo de mercado para este briefing: os guias de estúdio param em
"audiência, objetivo, plataforma". Este bloco é construção original — e é o de maior
risco jurídico dos sete.

| # | Campo | Microcopy | Por quê |
|---|---|---|---|
| G1 | O que a IA vai fazer | **"O que você imagina que a IA vai fazer aqui? Marque o que fizer sentido — se não souber, marque a última."** ☐ completar ou ampliar algo já filmado ☐ um apresentador ou porta-voz digital ☐ cenas criadas do zero ☐ versões em outros idiomas ☐ não sei, quero sua recomendação | **Roteador do bloco.** Define pipeline, custo e qual bloco de risco abrir. |
| G2 | Quantas peças e duração | número + select | Uma peça de 60s são 8–12 gerações, pelo limite de plano das ferramentas. |
| G3 | Regra interna sobre IA | **"Sua empresa tem alguma regra ou restrição sobre usar IA em material da marca?"** ○ não tem ○ tem, e é tranquilo ○ tem, e é restritiva — precisa aprovação ○ não sei, vou checar · *Pergunto no começo porque muita empresa grande tem política interna, e não vale a pena produzir algo que o jurídico de vocês não vai deixar publicar.* | **Descobrir isso no fim é perder o projeto inteiro.** |
| G4 | Material nas ferramentas | **"Posso usar o material de vocês dentro das ferramentas de IA?"** ○ sim ○ sim, com NDA assinado ○ não — precisa rodar sem enviar nosso material para fora ○ não sei · *Algumas ferramentas usam o que você envia para treinar os modelos delas. Existe caminho fechado para quando isso não pode acontecer.* | Fora do plano Enterprise, a Runway declara que input e output entram no treino, sem opt-out. Se o cliente não pode, o stack muda e o custo muda. |
| G5 | Rotulagem | **"Tudo bem o vídeo aparecer marcado como 'feito com IA'?"** ○ sim ○ preferimos que não ○ não pode de jeito nenhum ○ não sei · *As ferramentas de IA gravam uma marca invisível dentro do arquivo. YouTube, TikTok e LinkedIn leem essa marca e podem exibir o aviso sozinhos — nesses casos não é escolha nossa nem sua. No Instagram costuma depender de quem publica. E quando o vídeo mostra uma pessoa com aparência realista, YouTube e TikTok exigem que quem posta declare. Se isso for um problema para a marca, me diga agora: dá para desenhar a peça de um jeito que não caia na regra.* | **A pergunta certa não é "quer rotular?", é "está preparado para aparecer rotulado?"** ⚠️ Microcopy **corrigido em 13/08/2026** — a versão anterior dizia que Instagram rotula sozinho, e a política oficial da Meta diz o contrário: ela não detecta vídeo e áudio realistas de terceiros, e por isso **exige declaração de quem publica**. Ver `../2026-08-13-conformidade-conar-lgpd/04-rotulagem-nas-plataformas.md`. |
| G6 | O que precisa sair perfeito | **"Tem algo que precisa aparecer perfeito, sem margem para erro?"** ☐ embalagem, rótulo ou texto legível ☐ mão segurando o produto, em close ☐ o rosto de alguém que o público reconhece ☐ o produto exatamente como é na vida real ☐ nada disso, é mais atmosfera · *Essas quatro coisas são justamente onde a IA ainda escorrega. Se alguma for essencial, eu prefiro filmar aquele trecho e integrar — e te digo isso na proposta, não no meio do projeto.* | Traduz os limites técnicos de 2026 para linguagem de cliente. **É o campo que evita prometer o impossível.** |

**Bloco condicional — pessoas e direitos** *(só se G1 incluir apresentador/avatar)*:
a pessoa já sabe e concordou? · existe documento assinado? · e a voz? · por quanto
tempo e onde o rosto pode continuar sendo usado?

> Súmula 403 do STJ: uso comercial de imagem sem autorização gera **dano presumido**,
> sem precisar provar prejuízo. E as próprias ferramentas exigem: a HeyGen pede vídeo
> de consentimento gravado pela pessoa; a Synthesia proíbe avatar de catálogo em
> anúncio pago sem consentimento escrito.
>
> **Sobre a voz — redação corrigida em 13/08/2026.** A versão anterior dizia "a lei
> brasileira trata voz como dado sensível". É impreciso: voz vira dado sensível quando
> processada para identificar ou replicar a pessoa — o caso do clone, não o de qualquer
> gravação. E o fundamento mais forte é outro e mais simples: **a Constituição cita a
> voz junto com a imagem** (art. 5º, XXVIII, "a"). Microcopy novo:
>
> *"Usar a voz da própria pessoa é possível e dá o melhor resultado, mas exige uma
> autorização separada da do rosto — a lei protege voz e imagem como coisas diferentes,
> e clonar uma voz é mais delicado do que gravar uma."*
>
> Consequência prática do art. 11: para avatar de pessoa real e clone de voz,
> **legítimo interesse é indisponível**. A única base é **consentimento específico e
> destacado**, separado do texto principal.

**Três campos acrescentados em 13/08/2026** *(de `03-imagem-voz-e-biometria.md` §8)*:

| Campo | Quando aparece | Microcopy | Por quê |
|---|---|---|---|
| **Quem cuida da autorização** | se "não tem documento" ou "só de boca" | **"Quem vai cuidar da autorização?"** ○ Nós cuidamos e te enviamos assinado ○ Prefiro que você me mande o modelo e eu coleto ○ **Quero que você cuide disso (incluir no orçamento)** ○ Não sei · *Qualquer caminho serve — só preciso saber qual, porque muda o prazo e o escopo.* | Descobrir que **não há** documento sem definir **quem resolve** deixa o problema no ar. E a terceira opção é receita: no padrão ABAP/APRO, obter direito de imagem é **serviço remunerado a 40%** quando cai na produtora. Deixar em aberto é abrir mão de dinheiro, não só de proteção. |
| **Menor de idade** | se houver pessoa real em cena | **"Alguma pessoa que aparece tem menos de 18 anos?"** ○ Não ○ Sim ○ Não sei · *Se tiver, o caminho é diferente e leva mais tempo — precisa de autorização dos pais e, em alguns casos, de autorização da Justiça.* | Menor exige autorização dos responsáveis e, quando aplicável, **alvará judicial**. Não é detalhe: são semanas de prazo, e descobrir tarde inviabiliza a data. |
| **Destino do avatar** | sub-campo de 3.4 | **"Quando o prazo acabar, o que fazer com o avatar?"** ○ Apagar tudo ○ Guardar para usar de novo (renovando a autorização) ○ Não sei · *O avatar é um arquivo que continua existindo depois do vídeo pronto. Melhor combinar agora se ele fica guardado ou se some no fim.* | O 3.4 pergunta por quanto tempo o rosto pode ser usado, mas não o destino do **modelo treinado** — que é ativo separado e sobrevive à campanha. Sem isso, não existe saída limpa quando a pessoa sai da empresa. |

**Bloco condicional — material filmado** *(só se G1 incluir "completar algo já filmado")*:
tem os arquivos originais em boa qualidade? · aparece gente? · **a autorização que
essas pessoas assinaram permite modificar a imagem delas depois, inclusive com IA?**

> *"Essa é a pergunta que evita dor de cabeça: autorização de gravação antiga em geral
> libera editar, mas não libera criar imagem nova da pessoa. Se a resposta for 'não
> sei', eu te digo exatamente o que checar."*

**Este é o risco menos óbvio e mais provável do serviço** — há processo em curso
alegando exatamente isso — e ataca direto o item "expansão de plano", que é o mais
vendável dela.

---

## 5. O que precisa mudar no repositório

Nada disso está feito. É a lista para a fase de implementação.

| # | Onde | O quê |
|---|---|---|
| 1 | `briefing.html` (novo) | A página. Um `<form>`, três fieldsets, campos escondidos do FormSubmit no mesmo padrão do `index.html`. |
| 2 | CSP do `briefing.html` | Precisa nascer com `connect-src 'self' https://formsubmit.co` e `form-action https://formsubmit.co`. **A CSP de `servicos.html` está em `form-action 'none'`** — se o formulário for embutido ali em vez de página própria, o envio falha silenciosamente no navegador. |
| 3 | `script.js` ou `briefing.js` | A lógica condicional (mostrar/esconder), a validação inline, a navegação entre passos e o honeypot. Progressive enhancement: sem JS, o formulário continua enviando. |
| 4 | `obrigado.html` (novo) | Destino do `_next`. Com o prazo de 1 dia útil repetido. |
| 5 | `politica-privacidade.html` (novo) | Exigência de LGPD, ver seção 6. |
| 6 | `.github/workflows/deploy-pages.yml` | **Dois lugares:** o `on.push.paths` (esquecer = o deploy nem dispara) e o `cp` da lista de inclusão (esquecer = deploy verde com 404 no ar). Nomes por extenso, não glob — o glob destrói o fail-fast que o workflow tem de propósito. |
| 7 | `servicos.html` | Os 7 links `servico__link` ganham um irmão: "Fazer o briefing" → `briefing.html?servico=<slug>`. |
| 8 | `style.css` | Estilo dos campos. Não existe formulário estilizado além do `#contatoForm`. |

**Fase 2, opcional:** o briefing virar tarefa no ClickUp. A API é gratuita em qualquer
plano (`POST /api/v2/list/{list_id}/task`, só `name` é obrigatório, token `pk_` que ela
já tem, 100 req/min). O caminho pode ser o `_webhook` do FormSubmit apontando para um
receptor, ou um script Python no padrão dos 43 que já existem. Fica para depois: não
bloqueia nada.

> ⚠️ **CORRIGIDO em 13/08/2026.** A versão anterior deste parágrafo afirmava que o
> FormSubmit não tem API de leitura. **Tem** — e armazena as submissões por 30 dias.
> A mesma pesquisa levantou o perfil do fornecedor: Devro LABS, Sri Lanka; único
> documento jurídico é um PDF de duas páginas de 2019, sem menção a retenção, LGPD ou
> subprocessadores; cadeia Sri Lanka → Cloudflare → OVH Canadá; CORS aberto sobre um
> token público. Não é impeditivo para um formulário de contato, mas **merece uma
> segunda olhada antes de o briefing passar a carregar informação comercial sensível
> de clientes grandes** (verba, lançamento não anunciado, material sob NDA).

---

## 6. LGPD e anti-spam

> ⚠️ **CORRIGIDO em 13/08/2026** pela pesquisa `../2026-08-13-conformidade-conar-lgpd/02-lgpd-do-site.md`.
> A recomendação original aqui era legítimo interesse (art. 7º, IX). **Está errada**:
> o art. 33, IX só autoriza transferência internacional para as hipóteses dos incisos
> **II, V e VI** — legítimo interesse não está na lista, e o FormSubmit fica fora do
> Brasil. Com o inciso IX seria preciso assinar as cláusulas-padrão da ANPD
> (Res. 19/2024) com o fornecedor, o que é inviável para uma autônoma.

**Base legal: art. 7º, V — procedimentos preliminares a contrato, a pedido do
titular** — **sem checkbox de consentimento**. Encaixa no que o formulário é de fato
(a pessoa pede um orçamento), abre o mecanismo de transferência internacional do
art. 33, IX sem nada a assinar, e dispensa o teste de balanceamento que o legítimo
interesse exigiria. Consentimento continua descartado: jogaria o ônus da prova nela e
seria revogável a qualquer momento.

O que é obrigatório: **aviso de privacidade** acessível a partir do formulário (o que
é coletado, para quê, por quanto tempo, com quem é compartilhado) e um **canal de
contato** para titular. Ela **não precisa de DPO** (Res. ANPD 2/2022, art. 11, agente
de pequeno porte).

**Anti-spam: honeypot + tempo mínimo de preenchimento.** Sem CAPTCHA — em site
estático não há backend para validar o token, então CAPTCHA próprio seria teatro. E o
`_captcha` do FormSubmit deve ser desligado explicitamente.

---

## 7. O que ficou em aberto

1. **A copy de rotulagem de IA precisa de olhar jurídico.** O Guia do CONAR não foi
   lido no original — duas leituras de escritórios convergem que não há obrigação de
   rotular, uma terceira diverge. E o PL 2338 está em tramitação, com status de
   agosto/2026 não confirmado.
2. **O multiplicador por formato em Direção de Arte não tem fonte pública.** Nenhuma
   referência publica número. O valor é dela.
3. **As estatísticas de conversão dos relatórios não batem entre si.** Três pesquisas
   trouxeram números de fontes diferentes para "campos × abandono". O relatório de UX
   marcou parte como folclore de mercado. Nenhuma decisão deste documento depende
   desses números — o dimensionamento saiu do conteúdo, não do benchmark.
4. **Pendência fora deste escopo:** o JSON-LD de `servicos.html` ainda descreve os
   serviços com a redação anterior ao commit `847de0c`.

---

## 8. Índice dos relatórios

| Arquivo | O que tem lá que não coube aqui |
|---|---|
| `00-ux-e-conversao.md` | Evidência sobre número de campos, multi-step, barra de progresso, padrões de rótulo/validação/acessibilidade, mobile, tela de confirmação |
| `00-tecnico-plataformas.md` | CSP transcrita e explicada, comparação completa de fornecedores com preço, caminho até o ClickUp, limites de upload, LGPD detalhada |
| `01-conteudo-redes-sociais.md` | Guia APRO+ABA, razão peças/diária, o tripé de direitos |
| `02-direcao-de-creators.md` | CCT e remuneração por bloco de tempo, fluxo de aprovação em setor regulado, direção remota |
| `03-filmmaker.md` | CCT SATED-SP/SIAESP, tabela ASTIM/Sindcine, teto documentado do set solo, regulação de drone |
| `04-pos-producao.md` | Razão bruto:final, horas por fase, limites de transferência, rodadas de revisão |
| `05-fotografia.md` | Lei 9.610 aplicada a licenciamento de imagem, model release, LGPD em evento, prévia same-day |
| `06-direcao-de-arte.md` | Crítica ao questionário de branding padrão, art. 50 §2º, bloco impresso completo, os 4 caminhos detalhados |
| `07-producao-com-ia.md` | Súmula 403, consentimento para avatar, disclosure por plataforma, termos de uso das ferramentas, limites técnicos de 2026 |
