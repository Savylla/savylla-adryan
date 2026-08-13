# Formulário — Pós-produção

Pesquisa de 13/08/2026 para o formulário de briefing do **Serviço 04 — Pós-produção**
(frente de acabamento independente: o cliente manda o bruto e recebe montado, tratado
e versionado).

Premissa do serviço: o orçamento **não** depende de uma ideia criativa a ser inventada
— depende quase inteiramente das **características do material que chega** e do
**número de coisas que saem**. O formulário é, por isso, o mais técnico dos sete. O
desafio central não é lembrar de perguntar, é perguntar de um jeito que um cliente
leigo consiga responder.

---

## 1. O que a pesquisa achou

### 1.1 Os modelos reais de briefing de edição convergem em ~10 blocos

O modelo mais completo que achei ([videoeditingcompany.com](https://videoeditingcompany.com/video-editing-brief-template/))
tem 10 seções, e as que interessam a uma frente de **acabamento** (não de campanha) são
quatro: *Platform & Technical Specifications* (plataforma, aspect ratios, duração alvo,
formato de arquivo, resolução, legendas, zona segura, frame da thumbnail), *Assets
Provided* (nomes e localização dos arquivos — "Google Drive link, Dropbox, Frame.io",
ativos de marca, música, voiceover, cortes anteriores), *Brand Guidelines* (cores,
tipografia, uso do logo, estilo de legenda, desenho do lower third) e *Stakeholders &
Approvals* (revisor primário, revisores adicionais, aprovador final, **limite de
revisões**).

Um segundo modelo, voltado a cliente final ([filefeedback.com](https://www.filefeedback.com/tools/client-video-brief-template)),
mostra o padrão que mais me convenceu: **quase todo campo técnico é fechado e inclui a
opção "Incerto"**. Legenda: `Não requerido | Queimadas no vídeo | Arquivo .SRT | Ambos |
Incerto`. Música: `Editor fornece de biblioteca licenciada | Cliente fornece a faixa |
Compositor/score customizado | Sem música | Incerto`. E há um campo que separa a frente
de serviço na origem: `Produção completa (gravação + edição) | Apenas edição | Misto |
Apenas animação | Incerto`.

O terceiro ([gigxomi.com](https://www.gigxomi.com/blog/video-editing-brief-template-what-to-include-before-assigning-work))
não dá checklist, mas dá três regras de processo que valem mais que campos: pedir **três
referências** (uma de ritmo, uma de tratamento visual, uma de legenda), ter **um
proprietário consolidado das aprovações** e deixar explícita "uma linha clara entre
revisões incluídas e novo escopo".

### 1.2 O que realmente determina o preço

**Volume de bruto é o driver número um, e é gritante.** A formulação mais direta que
achei: "um editor que recebe 2 horas de material para um vídeo de 3 minutos tem uma
carga de trabalho completamente diferente de um que recebe 40 horas"
([krock.io](https://krock.io/blog/stay-creative/how-much-video-editor-should-charge/)).
A razão bruto:final tem números de referência: ficção fica tipicamente entre **6:1 e
10:1**, animação perto de **1:1**, e documentário é o extremo — "frequentemente
excedendo 100:1" depois da migração para digital ([Wikipedia — Shooting ratio](https://en.wikipedia.org/wiki/Shooting_ratio)).
Uma escola de cinema recomenda ficção não passar de 10:1 e exemplifica: "60 minutos de
material que rendem um filme de 5 minutos são uma razão de 12:1"
([Cyber Film School](https://cyberfilmschool.com/post-production-rules-of-thumb/)).

**Tempo por minuto finalizado.** A mesma página dá a regra de bolso mais útil para
prazo: **1 hora de trabalho por minuto finalizado em cada fase** — rough cut, fine cut,
e som/música. Um filme de 90 minutos → 90h + 90h + 90h ≈ 270 horas. E a regra 60/40:
"60% dos recursos na produção, 40% na pós".

**Motion e cor são multiplicadores, não adicionais.** "Color grading avançado em
DaVinci, integração com Cinema 4D e motion graphics em After Effects... cada
especialidade que você adiciona é um multiplicador de tarifa" (krock.io). A beCreatives
lista no mesmo grupo de fatores o número de câmeras e fontes de material, mixagem de
áudio e compositing ([beCreatives](https://becreatives.co/video-editing-prices/)).

**Rodadas de revisão.** "A maioria das cotações inclui 2–3 rodadas de revisão. Se você
não definir isso de saída, o scope creep come sua margem" (krock.io).

**Urgência.** Duas fontes, dois números: 25–50% sobre a base para entrega em 48h ou no
mesmo dia (krock.io); 50–100% para entrega expressa em 24–48h, contra um padrão de 3–7
dias úteis (beCreatives).

**Versionamento e legenda são linha de custo própria.** Não achei uma porcentagem
confiável para "versão por aspect ratio" (a página que o resumo de busca atribuía isso
não confirma o número quando aberta — descartei). Para legenda, sim: os serviços
especializados cobram por minuto, e a diferença entre um SRT e um burn-in traduzido é de
ordem de grandeza — inglês a partir de £6/min e legenda traduzida a partir de £16/min
([Absolute Translations](https://www.absolutetranslations.com/subtitling-prices)),
US$ 1,99/minuto para caption automática revisada ([Rev](https://support.rev.com/hc/en-us/articles/18893487380365-Pricing)),
e burn-in cobrado à parte, "a partir de £80 por vídeo até 22 minutos, depois £3,50/min"
(Absolute Translations). Ou seja: **idioma e formato da legenda mudam o preço, não só
"tem legenda ou não"**.

### 1.3 A especificação técnica do material — e por que cada item muda o trabalho

**Codec e volume andam juntos.** Os números por hora de gravação em 4K:
ARRIRAW 4.6K ≈ **1,94 TB/hora**; ProRes HQ 4K ≈ **540 GB/hora**; ProRes 422 4K ≈
**315 GB/hora**; H.264/H.265 4K a 100 Mb/s ≈ **45 GB/hora**
([Tools for Film](https://www.toolsforfilm.com/blog/raw-prores-h265-storage-cost-comparison)).
A mesma página faz a inversão que importa: material leve **não** é material barato —
"a economia de US$ 250 em disco do H.265 é apagada por US$ 1.200+ em mão de obra de
transcode", porque codecs long-GOP exigem "transcode para um codec intermediário
(ProRes 422, DNxHD) antes de o grading começar", e esse transcode leva 4–12 horas num
longa. Por quê: no H.264/H.265 cada frame não é decodificável isoladamente — o decoder
tem que referenciar frames vizinhos, o que torna a reprodução em timeline caríssima em
4K. Em RAW/ProRes cada frame se basta.

**Log/RAW não é entregável, é ponto de partida.** Material log é gravado plano de
propósito e **exige** grading para virar imagem final; RAW guarda cada frame como um
conjunto de dados independente, o que dá precisão de exposição e balanço que um H.264 não
dá ([Artgrid](https://artgrid.io/insights/log-vs-raw/), [Pixflow](https://pixflow.net/blog/difference-between-raw-log-and-rec-709-camera-footage/)).
Consequência prática para o formulário: **se o material é log/RAW, "tratamento de cor"
deixa de ser opcional** — está no caminho crítico, não na lista de extras.

**Frame rate misturado é retrabalho silencioso.** Clipes de frame rates diferentes são
conformados ao frame rate da timeline — 23,98 / 29,97 / 30 / 50 / 59,94 / 60 fps todos
passam a tocar a 24 se a timeline for 24 ([manual do DaVinci Resolve](https://www.steakunderwater.com/VFXPedia/__man/Resolve18-6/DaVinciResolve18_Manual_files/part1321.htm)).
E colocar 24 fps numa timeline de 60 obriga a inventar 36 frames por segundo por
interpolação, com a cadência de repetição/descarte determinando se o movimento fica
suave ou trêmulo ([Frank Schrader](https://www.frankschrader.us/video-frame-rate-explained-different-frame-rate-on-timeline/)).
Um acervo juntado de várias gravações diferentes é exatamente o caso em que isso
aparece.

**Áudio gravado separado (dual system) é uma tarefa à parte.** Com timecode em comum
entre câmera e gravador (jam sync), um comando sincroniza a timeline inteira. Sem
timecode, sincroniza-se claquete por claquete alinhando o pico da onda — "um processo
um tanto tedioso" ([IFSS](https://ifsstech.wordpress.com/2008/07/03/dual-system-sound-sync-in-fcp/),
[Hollyland](https://store.hollyland.com/blogs/creator-hub/sync-audio-in-davinci-resolve)).
Pior: há uma armadilha de entrega documentada — se o cliente manda um projeto com sync
multicam **sem** os arquivos de áudio originais, "o novo editor não consegue ouvir nada"
([fórum Adobe](https://community.adobe.com/t5/premiere-pro-discussions/no-easy-solution-for-sending-proxy-only-project-to-an-editor-without-dual-system-sound-files/td-p/15263304)).

**Proxies.** Servem para circular o material antes/no lugar do original em alta, e o
requisito é rígido: **o proxy precisa ter o mesmo frame rate do clipe original** (a
resolução pode ser menor e o codec pode ser outro), e desalinhar isso produz erro de
sincronia de áudio no fim dos clipes longos ([Larry Jordan](https://larryjordan.com/articles/linking-media-to-proxies-created-outside-premiere-pro/),
[Frame.io — guia de proxies](https://blog.frame.io/2024/07/29/updated-guide-premiere-pro-proxies-and-proxy-workflows/)).

### 1.4 Como o material chega — e o que isso custa em dias

Os limites reais das opções que um cliente brasileiro vai propor:

| Via | Limite | Expira |
|---|---|---|
| WeTransfer grátis | **3 GB por transferência**, 10 transferências e 3 GB/mês, uso não comercial | 3 dias |
| SwissTransfer | 50 GB por transferência, sem conta | — |
| TransferNow | 5 GB, sem quota mensal | — |
| MASV | pacotes de tamanho ilimitado; 15 GB de crédito grátis/mês, US$ 0,25/GB depois | — |
| Frame.io | asset até 5 TB, mas **cap de 500 GB para arquivos de vídeo** | — |
| Google Drive | 5 TB por arquivo; 15 GB grátis de armazenamento | dá para definir expiração de acesso |

Fontes: [brault.app](https://brault.app/blog/file-transfer-and-sharing/wetransfer-free-limit/),
[MASV](https://masv.io/compare/wetransfer), [Frame.io — upload](https://help.frame.io/en/articles/9101026-uploading-your-media),
[filesize.org](https://filesize.org/limits/google-drive/).

O número que interessa: **3 GB do WeTransfer grátis dá menos de 4 minutos de ProRes 422
4K** (315 GB/hora). Um cliente que diz "eu te manda por WeTransfer" e tem 2 horas de
bruto ProRes está descrevendo algo que não vai acontecer. Daí a necessidade de cruzar
*volume* com *meio de envio* no mesmo formulário.

O fluxo canônico de pós ([MASV](https://masv.io/workflow/post-production)) é: data
management → edição → VFX → cor → som → entrega; recomenda **gerar proxies em H.264/H.265
ou ProRes para circular** antes de mover o original, cita Frame.io e Iconik como camada
de review, e lembra a regra dos três locais de backup. Entregáveis finais incluem
versões por aspect ratio (16×9, 9×16, 4×3, 1×1) — ou seja, versionamento é tratado como
etapa formal de entrega, não como favor.

### 1.5 Revisão e aprovação: como isso vira campo

As práticas concretas ([Cutjamm](https://www.cutjamm.com/blog/how-to-get-feedback-on-a-video)):
definir no contrato quantas rodadas estão incluídas; designar **um único decisor** para
aprovar o corte final; **instruir que tipo de feedback cabe em cada rodada** (no rough
cut: história e ritmo, não correção de cor); pedir notas com timestamp exato; dar ao
revisor 24–48h para responder para o projeto não empacar; e manter todo o feedback num
só lugar em vez de espalhado entre e-mail, WhatsApp e Drive. A gigxomi reforça a
separação entre "revisão criativa" e "defeito técnico" — só o segundo não conta como
rodada. Ferramentas de review dão comentário amarrado ao frame e controle de versão
([Markup.io](https://www.markup.io/blog/video-review/)).

O sintoma que justifica pedir a lista de aprovadores **antes** de começar: um estudo de
caso citado nos resultados de busca (não abri a página) afirma que times veem 3–4x mais
rodadas quando stakeholders externos entram na revisão depois da rodada 1
([PlayPause](https://playpause.io/blogs/video-review-and-approval-for-video-production-companies)).
Trato isso como indício, não como número.

### 1.6 Música e direitos

O padrão de campo já existe pronto e é fechado: `editor fornece de biblioteca licenciada
| cliente fornece a faixa | compositor/score customizado | sem música | incerto`
(filefeedback). O risco que o campo previne é concreto: no YouTube, quando o Content ID
reivindica um vídeo, o reclamante tem **30 dias** para liberar, manter a reivindicação,
pedir remoção ou deixar expirar ([Ajuda do YouTube — direitos musicais](https://support.google.com/youtube/answer/7071269?hl=pt)),
e faixas da Biblioteca de áudio sem restrição "não serão reivindicadas com o Content ID"
([Ajuda do YouTube — Biblioteca de áudio](https://support.google.com/youtube/answer/3376882?hl=pt-BR)).
Quando o material vem de fornecedor de estoque, é o fornecedor que ajuda a limpar a
reivindicação ([Microsoft/Clipchamp](https://support.microsoft.com/pt-br/topic/why-does-my-clipchamp-video-get-a-copyright-warning-on-youtube-or-other-sites-e3114010-710d-42ab-878b-86ef8e5c5429)).
Recomendação minha: perguntar também **se o vídeo vai rodar em mídia paga**, porque
licença de biblioteca para orgânico e para anúncio não são a mesma licença — isso é
conhecimento de mercado, não achado de fonte.

### 1.7 A saída para o cliente leigo: pedir arquivo, não especificação

Codec, resolução, frame rate, bit depth, espaço de cor e duração saem todos da **ficha
técnica de um único arquivo**, lida localmente por MediaInfo ou ffprobe
([MediaArea](https://mediaarea.net/en/MediaInfo)) — inclusive em leitores que rodam no
navegador sem subir o arquivo. Existe até app de celular para ler as propriedades de um
clipe ([smartfilming](https://smartfilming.blog/2020/06/16/26-checking-detailed-properties-of-video-clips-on-android-and-ios/)).

Conclusão de projeto (minha, apoiada nisso): **não perguntar codec. Pedir um arquivo de
amostra.** Um clipe bruto, do jeito que saiu da câmera, responde em 10 segundos o que
seis campos de dropdown responderiam errado.

---

## 2. O que é imprescindível saber para orçar este serviço

Em ordem de impacto no orçamento:

1. **Quantidade e duração do que sai** (nº de vídeos finais × duração de cada). É a base
   de tudo — a regra de 1h de trabalho por minuto finalizado por fase se aplica em cima
   deste número.
2. **Volume de material que entra** (horas ou GB). A razão bruto:final é o driver nº 1;
   2h e 40h de bruto para o mesmo entregável são dois serviços diferentes.
3. **Ponto de partida do material**: tudo bruto sem seleção · com os melhores trechos já
   marcados · com roteiro/ordem definida · corte antigo para refazer. Muda as horas de
   decupagem, que é onde o volume de bruto se converte em custo.
4. **Um arquivo de amostra**. Resolve codec, resolução, frame rate, log/RAW e peso por
   hora de uma vez — e o log/RAW promove o tratamento de cor de opcional a obrigatório.
5. **Se há áudio gravado em separado e se já está casado com a imagem.** Sincronia manual
   sem timecode é trabalho por take; e há o risco de o material chegar sem os arquivos de
   áudio originais.
6. **Nº de versões/formatos por plataforma** (16:9, 9:16, 1:1/4:5) e se há corte curto
   além do principal. Cada versão é entrega formal.
7. **O que entra no acabamento**: motion/vinheta/cartelas, cor, mixagem, masterização.
   Motion e cor avançada são multiplicadores de tarifa, não somas.
8. **Legenda: formato e idioma.** SRT, queimada, ou as duas; e se tem outro idioma —
   tradução é outra ordem de grandeza.
9. **Identidade do canal existe ou precisa ser criada?** "Aplicar abertura/selo/lower
   third" e "desenhar a cara do canal" são escopos distintos (o segundo encosta no
   Serviço 06).
10. **Música: quem fornece, e vai rodar em mídia paga?** Define risco de Content ID e
    tipo de licença.
11. **Prazo.** Urgência é 25–100% em cima da base conforme a fonte; sem data, some.
12. **Quantas pessoas revisam e quem dá a palavra final.** Determina quantas rodadas
    cabem no escopo — o item que mais destrói margem quando fica implícito.
13. **Como o material vai chegar.** Cruzado com o volume, diz se o envio é viável ou se
    o prazo começa uma semana depois.

---

## 3. Formulário proposto

**Formato:** 5 passos com barra de progresso. **18 campos obrigatórios** é muito para um
formulário público, então os 9 marcados com **★** formam o *núcleo mínimo*: se a pessoa
abandonar no meio, esses 9 já permitem responder com uma faixa de escopo e uma pergunta
única de follow-up. Sugiro que o formulário salve progresso e envie o parcial.

Onde há jargão inevitável, a explicação vai **dentro do campo**, em texto de apoio, e
todo campo técnico tem escape.

### Passo 1 — O que você precisa que volte pronto

| Campo | Tipo de input | Obrigatório? | Por que existe / o que destrava |
|---|---|---|---|
| ★ Natureza do trabalho | Select: `Um vídeo só` · `Um lote de vídeos` · `Canal com publicação recorrente` · `Acervo parado que quero destravar` | Sim | Separa projeto pontual de recorrência (contrato mensal) — muda a estrutura da proposta antes do valor |
| ★ Quantos vídeos e que duração | Texto curto guiado + campo numérico | Sim | Base de todo o cálculo de horas (≈1h de trabalho por minuto finalizado, por fase) |
| ★ Onde vai publicar | Multiselect: `YouTube` · `Instagram / TikTok` · `LinkedIn` · `Site ou landing page` · `Mídia paga (anúncio)` · `Uso interno` · `Telão de evento` · `Ainda não sei` | Sim | Define formatos de masterização, e "mídia paga" muda licença de música e nível de acabamento |
| Formatos de tela que precisa | Select: `Só um formato` · `Deitado + em pé (16:9 e 9:16)` · `Os três (deitado, em pé e quadrado)` · `Não sei, decida por mim` | Sim | Cada formato é uma entrega própria, não um export |
| Referências | Até 3 URLs | Não (recomendado) | Fixa o nível de acabamento esperado; os modelos recomendam 3 (ritmo, visual, legenda) |

**Microcopy**
- *Natureza:* "Como é esse trabalho?"
- *Quantidade:* "Quantos vídeos precisam sair, e com que duração cada um? — Chute se não tiver certeza. 'Uns 4 vídeos de 1 minuto' já me serve."
- *Onde publicar:* "Onde esses vídeos vão parar?"
- *Formatos:* "Precisa em mais de um formato de tela? — Deitado é o do YouTube, em pé é o do Reels e do TikTok. Cada formato é um corte próprio, não é só recortar a borda."
- *Referências:* "Tem algum vídeo que tenha o ritmo ou a cara que você quer? Cola até 3 links. — Pode ser de qualquer marca, inclusive concorrente."

### Passo 2 — O material que você vai mandar

| Campo | Tipo de input | Obrigatório? | Por que existe / o que destrava |
|---|---|---|---|
| ★ Quanto material você tem | Select de faixas em horas: `Até 1h` · `1 a 5h` · `5 a 20h` · `Mais de 20h` + campo alternativo em GB/TB + **`Não sei — o link responde`** | Sim | Razão bruto:final é o driver nº 1 de preço e de prazo |
| ★ Ponto de partida do material | Select: `Tudo bruto, nada selecionado` · `Os melhores trechos já estão marcados` · `Tem roteiro ou ordem definida` · `Existe um corte antigo para refazer` | Sim | Define as horas de decupagem — é aqui que volume de bruto vira custo |
| ★ Como o material chega + link | Select (`Google Drive` · `WeTransfer` · `Frame.io` · `MASV / Dropbox / outro` · `Disco físico` · `Ainda não organizei`) + campo de URL | Sim | Viabilidade: 3 GB do WeTransfer grátis dá <4 min de ProRes 4K. Cruzado com o volume, diz se o prazo começa hoje ou em uma semana |
| ★ Arquivo de amostra | URL de **um** arquivo bruto | Sim | **Substitui 6 campos técnicos.** A ficha técnica do arquivo entrega codec, resolução, frame rate, log/RAW e peso por hora |
| ★ O que vem junto com o vídeo | Multiselect: `Áudio gravado em aparelho separado` · `Logo, fontes e cores da marca` · `Roteiro ou texto` · `Trechos já escolhidos` · `Música` · `Legenda ou transcrição antiga` · `Só o vídeo, mais nada` · `Não sei o que tem` | Sim | Cada item ausente é trabalho a mais; áudio separado é tarefa própria |
| Esse áudio já está casado com a imagem? | Radio: `Sim, já está sincronizado` · `Não` · `Não sei` — **só aparece se marcou "áudio gravado em aparelho separado"** | Sim (condicional) | Com timecode, um comando resolve; sem, é claquete por claquete. E previne o caso do projeto entregue sem os arquivos de áudio originais |
| O material é de gravações diferentes? | Radio: `Uma gravação só` · `Várias, em datas/câmeras diferentes` · `Não sei` | Não | Material misturado costuma vir com frame rates diferentes, que precisam ser conformados antes da montagem |

**Microcopy**
- *Volume:* "Quanto material bruto você tem? — Em horas de gravação, ou em GB se souber. Não precisa ser exato: essa é a informação que mais muda o orçamento, então um chute honesto vale mais que um número redondo."
- *Ponto de partida:* "Em que estado está esse material?"
- *Como chega:* "Como você pretende me mandar? — Se já tem link, cola aqui. Se o material for grande, eu te indico o caminho — WeTransfer grátis não passa de 3 GB, o que dá menos de 4 minutos de vídeo em qualidade alta."
- *Amostra:* "Manda o link de **um** arquivo bruto, do jeito que saiu da câmera. — Só um clipe. Eu abro a ficha técnica dele e descubro sozinha o formato, a resolução e a taxa de quadros. Assim você não precisa procurar nada disso."
- *O que vem junto:* "O que mais existe além dos arquivos de vídeo?"
- *Áudio:* "O som gravado no aparelho separado já está encaixado com a imagem? — Se você não sabe, marca 'não sei': eu vejo na amostra. E se você for me mandar um projeto já montado, manda também os arquivos de áudio originais — sem eles o projeto abre muda."
- *Gravações diferentes:* "É uma gravação só ou material de várias? — Material de câmeras e datas diferentes quase sempre vem com taxas de quadros diferentes, e isso precisa ser acertado antes da montagem."

### Passo 3 — O acabamento

| Campo | Tipo de input | Obrigatório? | Por que existe / o que destrava |
|---|---|---|---|
| ★ O que entra no acabamento | Multiselect: `Montagem` · `Tratamento de cor` · `Motion, vinheta e cartelas` · `Abertura, selos e lower thirds` · `Legenda` · `Tratamento de áudio e mixagem` · `Entrega nos formatos de cada plataforma` · **`Não sei — me diga o que esse material precisa`** | Sim | Motion e cor avançada são multiplicadores de tarifa. O escape evita que o cliente desmarque algo que o material exige |
| ★ Legenda | Select: `Não precisa` · `Queimada no vídeo` · `Arquivo separado (.srt)` · `As duas coisas` · `Não sei` | Sim | Formato muda o trabalho; e o campo abre o de idioma |
| Em que idiomas | Multiselect / texto — **só aparece se legenda ≠ "Não precisa"** | Sim (condicional) | Tradução é outra ordem de grandeza (a partir de ~£16/min contra ~£6/min no idioma original) |
| ★ A cara do canal | Select: `Já existe manual de marca e pacote gráfico` · `Tem logo e cores, mas nada montado` · `Não tem nada — quero que crie` · `Não sei` | Sim | Separa "aplicar identidade" de "criar identidade" (o segundo encosta na Direção de Arte) |
| Música | Select: `Você escolhe de biblioteca licenciada` · `Eu forneço a faixa` · `Tenho trilha própria/compositor` · `Sem música` · `Não sei` | Sim | Define risco de Content ID: no YouTube o reclamante tem 30 dias para responder, e faixa de biblioteca livre não é reivindicada |
| Precisa receber o projeto aberto no final? | Radio: `Não, só os vídeos prontos` · `Sim, quero os arquivos do projeto` · `Não sei o que é isso` | Não | Entrega de projeto é escopo e organização extra — precisa estar dito antes, não depois |

**Microcopy**
- *Acabamento:* "O que você quer que entre no acabamento? — Marca tudo que faz sentido. Se estiver em dúvida, marca a última opção: eu olho o material e te digo o que ele pede."
- *Legenda:* "Precisa de legenda? — 'Queimada' é a que fica gravada na imagem, para quem assiste sem som. 'Arquivo separado' é o texto que o YouTube liga e desliga."
- *Idiomas:* "Em que idiomas?"
- *Cara do canal:* "Sua marca já tem uma cara definida para vídeo? — Abertura, selo, tarja com o nome de quem fala. Ter logo e cor não é a mesma coisa que ter isso montado."
- *Música:* "E a música, quem entra com ela?"
- *Projeto aberto:* "Você precisa receber o projeto de edição no final, além dos vídeos? — É o arquivo que abre no programa de edição, para outra pessoa continuar depois. Se você não sabe se precisa, provavelmente não precisa."

### Passo 4 — Prazo, revisão e aprovação

| Campo | Tipo de input | Obrigatório? | Por que existe / o que destrava |
|---|---|---|---|
| ★ Quando precisa estar pronto | Data + checkbox `Não tenho data fechada` | Sim | Urgência é 25–100% sobre a base dependendo da janela; e sem data o projeto não entra em fila |
| ★ Quem aprova | Texto curto (nome/função) + select de quantas pessoas revisam: `Só eu` · `2 ou 3` · `Mais de 3` · `Ainda não sei` | Sim | Aprovador único é a prática que segura o número de rodadas; mais aprovadores = mais rodadas, e isso precisa estar na proposta |
| Algo mais que eu deveria saber | Textarea | Não | Onde cabe o que nenhum campo previu (restrição jurídica, aparição de pessoa, embargo de data) |

**Microcopy**
- *Prazo:* "Quando isso precisa estar publicado?"
- *Aprovação:* "Quem dá a palavra final no corte? — E quantas pessoas vão opinar antes disso. Não é burocracia: com um aprovador, duas rodadas de ajuste resolvem; com cinco, o mesmo vídeo vira outro trabalho, e eu prefiro já contar isso na proposta."
- *Extra:* "Tem mais alguma coisa que eu deveria saber?"

### Passo 5 — Você

| Campo | Tipo de input | Obrigatório? | Por que existe |
|---|---|---|---|
| ★ Nome | Texto | Sim | Retorno |
| Marca ou empresa | Texto | Não | Contexto de porte e categoria |
| ★ E-mail | E-mail | Sim | Canal da proposta |
| WhatsApp | Telefone | Não | Onde a dúvida única de follow-up se resolve em 2 minutos |

### Lógica condicional — resumo

- `Idiomas da legenda` → só se **Legenda ≠ "Não precisa"**.
- `Áudio já sincronizado?` → só se **"O que vem junto"** inclui *áudio gravado em aparelho separado*.
- **Recomendação minha (sem fonte):** se **Volume ≥ 5h** e **Como chega = WeTransfer**,
  mostrar um aviso inline no próprio passo 2 ("por esse caminho não vai passar — eu te
  mando a alternativa"), em vez de descobrir isso três e-mails depois.
- **Recomendação minha:** se **Natureza = "Canal com publicação recorrente"**, trocar
  "Quantos vídeos" por "Quantos vídeos por mês" — o orçamento é mensal, não por peça.

---

## 4. O que NÃO perguntar (e por quê)

- **Codec, container, resolução, frame rate, bit depth, espaço de cor, LUT, câmera,
  bitrate.** Nove campos que o cliente leigo responde errado e o profissional acha
  desnecessários — porque todos saem da ficha técnica de um arquivo. Substituídos pelo
  campo de amostra. Se ela quiser precisão para clientes técnicos (produtoras), a saída é
  um campo opcional único de texto livre: "se você já sabe as especificações, cola aqui" —
  e não nove dropdowns.
- **"Você tem proxies?"** Fora que o termo não significa nada para 90% dos clientes, a
  resposta não muda o orçamento — muda o método de trabalho dela, e é decisão dela, não do
  cliente.
- **"Você tem LUT da câmera?"** Só faz sentido depois de saber que o material é log — e
  isso a amostra revela. Se revelar, é uma pergunta de e-mail, não de formulário.
- **Objetivo de marketing, público-alvo, funil, métrica de sucesso.** Os modelos de
  briefing incluem porque são briefings de *campanha*. Aqui o material já foi captado com
  um objetivo — perguntar de novo alonga o formulário sem mudar o escopo. A referência e a
  plataforma já entregam o tom necessário.
- **Faixa de orçamento.** Recomendação minha, alinhada à regra do site de preço nunca
  aparecer: pedir número de verba num formulário público inverte a lógica da proposta
  ("responder com uma proposta mais estruturada") e ancora a conversa antes de ela ver o
  material. Se ela quiser um sinal de porte, o campo `Natureza do trabalho` + `Quantos
  vídeos` já dão.
- **Nº de rodadas de revisão desejadas.** Isso é resposta dela na proposta, não pergunta
  ao cliente. O que se pergunta é **quantas pessoas aprovam** — daí ela dimensiona as
  rodadas.
- **Nomes de arquivo, estrutura de pastas, planilha de decupagem.** Vem depois do "sim",
  na abertura do projeto.
- **Software de edição usado antes.** Só importa se a resposta ao campo "precisa receber o
  projeto aberto" for sim — e nesse caso é conversa, não campo.

---

## 5. Fontes

**Modelos de briefing e intake**
- [videoeditingcompany.com — Video Editing Brief Template](https://videoeditingcompany.com/video-editing-brief-template/) — o modelo mais completo: 10 seções, com *Assets Provided* (link do Drive/Dropbox/Frame.io), *Brand Guidelines* (lower third, estilo de legenda) e limite de revisões.
- [filefeedback.com — Client Video Brief Template](https://www.filefeedback.com/tools/client-video-brief-template) — campos fechados com opção "Incerto" para legenda e música; separa "produção completa" de "apenas edição".
- [gigxomi.com — Video Editing Brief Template](https://www.gigxomi.com/blog/video-editing-brief-template-what-to-include-before-assigning-work) — as três regras de processo: 3 referências, aprovador consolidado, linha entre revisão incluída e novo escopo.

**O que determina preço e prazo**
- [krock.io — Video Editor Rates in 2026](https://krock.io/blog/stay-creative/how-much-video-editor-should-charge/) — a melhor formulação do volume de bruto (2h vs 40h para o mesmo vídeo); 2–3 rodadas incluídas; urgência 25–50%; motion/cor como multiplicador.
- [beCreatives — Video Editing Prices](https://becreatives.co/video-editing-prices/) — urgência 24–48h em +50–100% contra padrão de 3–7 dias úteis; nº de câmeras e fontes como fator.
- [Cyber Film School — Post Production Rules of Thumb](https://cyberfilmschool.com/post-production-rules-of-thumb/) — 1h de trabalho por minuto finalizado em cada fase; ficção até 10:1; regra 60/40 produção/pós.
- [Wikipedia — Shooting ratio](https://en.wikipedia.org/wiki/Shooting_ratio) — ficção 6:1–10:1, documentário frequentemente >100:1, animação ~1:1.

**Especificação técnica do material**
- [Tools for Film — RAW vs ProRes vs H.265 storage cost](https://www.toolsforfilm.com/blog/raw-prores-h265-storage-cost-comparison) — GB/hora por codec e o ponto-chave: material leve custa mais em mão de obra de transcode.
- [Artgrid — LOG vs RAW](https://artgrid.io/insights/log-vs-raw/) e [Pixflow — RAW, LOG e Rec.709](https://pixflow.net/blog/difference-between-raw-log-and-rec-709-camera-footage/) — por que log/RAW exige grading e não é entregável.
- [Manual do DaVinci Resolve — Mixed Frame Rates](https://www.steakunderwater.com/VFXPedia/__man/Resolve18-6/DaVinciResolve18_Manual_files/part1321.htm) e [Frank Schrader — frame rates numa timeline](https://www.frankschrader.us/video-frame-rate-explained-different-frame-rate-on-timeline/) — conformação ao frame rate da timeline e o custo de misturar.
- [IFSS — Dual System Sound Sync](https://ifsstech.wordpress.com/2008/07/03/dual-system-sound-sync-in-fcp/) e [Hollyland — sincronizar áudio no Resolve](https://store.hollyland.com/blogs/creator-hub/sync-audio-in-davinci-resolve) — timecode vs claquete/waveform.
- [Fórum Adobe — projeto proxy sem os arquivos de dual-system](https://community.adobe.com/t5/premiere-pro-discussions/no-easy-solution-for-sending-proxy-only-project-to-an-editor-without-dual-system-sound-files/td-p/15263304) — a armadilha do projeto que abre muda.
- [Larry Jordan — proxies criados fora do Premiere](https://larryjordan.com/articles/linking-media-to-proxies-created-outside-premiere-pro/) e [Frame.io — guia de proxies](https://blog.frame.io/2024/07/29/updated-guide-premiere-pro-proxies-and-proxy-workflows/) — o proxy tem que ter o mesmo frame rate.
- [MediaArea — MediaInfo](https://mediaarea.net/en/MediaInfo) e [smartfilming — propriedades de clipe no celular](https://smartfilming.blog/2020/06/16/26-checking-detailed-properties-of-video-clips-on-android-and-ios/) — a base do campo de amostra: a ficha técnica sai do arquivo.

**Entrega do material e limites de transferência**
- [brault.app — limite grátis do WeTransfer em 2026](https://brault.app/blog/file-transfer-and-sharing/wetransfer-free-limit/) — 3 GB/transferência, 10/mês, expira em 3 dias; alternativas com limites (SwissTransfer 50 GB, TransferNow 5 GB).
- [MASV vs WeTransfer](https://masv.io/compare/wetransfer) — pacotes ilimitados, 15 GB grátis/mês, US$ 0,25/GB.
- [Frame.io — Uploading your media](https://help.frame.io/en/articles/9101026-uploading-your-media) — asset até 5 TB, cap de 500 GB para vídeo.
- [filesize.org — limites do Google Drive](https://filesize.org/limits/google-drive/) — 5 TB por arquivo, 15 GB grátis.
- [MASV — Post-Production Workflow](https://masv.io/workflow/post-production) — fluxo canônico em 6 fases, proxies para circular, Frame.io/Iconik no review, versões por aspect ratio como entrega formal.

**Revisão e aprovação**
- [Cutjamm — How to get feedback on a video](https://www.cutjamm.com/blog/how-to-get-feedback-on-a-video) — rodadas no contrato, decisor único, tipo de feedback por rodada, timestamp, janela de 24–48h.
- [Markup.io — video review best practices](https://www.markup.io/blog/video-review/) — consolidação do feedback e comentário amarrado ao frame.
- [PlayPause — video review and approval](https://playpause.io/blogs/video-review-and-approval-for-video-production-companies) — indício (do resumo de busca, página não aberta) de 3–4x mais rodadas quando stakeholders externos entram depois da rodada 1.

**Legenda**
- [Absolute Translations — Subtitling Prices](https://www.absolutetranslations.com/subtitling-prices) — £6/min no idioma original, £16/min traduzido, burn-in a partir de £80 até 22 min + £3,50/min.
- [Rev — Pricing](https://support.rev.com/hc/en-us/articles/18893487380365-Pricing) — US$ 1,99/minuto para caption em inglês.

**Música e direitos**
- [Ajuda do YouTube — Gestão de direitos musicais](https://support.google.com/youtube/answer/7071269?hl=pt) — o reclamante tem 30 dias para liberar, manter, pedir remoção ou deixar expirar.
- [Ajuda do YouTube — Biblioteca de áudio](https://support.google.com/youtube/answer/3376882?hl=pt-BR) — faixas sem restrição não são reivindicadas pelo Content ID.
- [Microsoft/Clipchamp — aviso de direitos autorais](https://support.microsoft.com/pt-br/topic/why-does-my-clipchamp-video-get-a-copyright-warning-on-youtube-or-other-sites-e3114010-710d-42ab-878b-86ef8e5c5429) — quando a faixa vem de fornecedor de estoque, é ele que ajuda a limpar a reivindicação.

**Fonte consultada e descartada**
- [advids.co — social content video cost](https://advids.co/pricing/how-much-social-content-video-creation-cost) — o resumo de busca atribuía a esta página um "+15–25% por versão de aspect ratio"; ao abrir, a página **não** traz esse número. Descartado — não há porcentagem confiável de versionamento neste documento.
