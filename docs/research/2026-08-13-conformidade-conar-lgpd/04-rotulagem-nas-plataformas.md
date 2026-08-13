# Rotulagem de IA nas plataformas — o que é obrigatório e o que é automático

> Pesquisa executada em **13/08/2026**. Todas as afirmações abaixo vêm de página oficial de
> plataforma, de regulador ou de fornecedor de ferramenta. Onde só existe notícia ou blog, está
> marcado como **não confirmado**. Política de plataforma muda rápido — reconferir a cada trimestre.

---

## 1. Resposta direta

**A afirmação da pesquisa anterior — "YouTube, TikTok e Meta rotulam sozinhos, declare o cliente
ou não" — se sustenta em parte, e está exagerada exatamente no caso que mais interessa à
Savylla: vídeo com avatar digital publicado no Instagram.**

O que é verdade:

- **YouTube** aplica rótulo por conta própria em três situações declaradas na política: conteúdo
  feito com as ferramentas de IA generativa do próprio YouTube, conteúdo que chega **com metadado
  C2PA**, e conteúdo que os sistemas do YouTube detectam como gerado/alterado por IA.
- **TikTok** aplica rótulo AIGC automaticamente quando lê **Content Credentials (C2PA)** no
  arquivo, e a política diz explicitamente que conteúdo não rotulado "pode ser removido,
  restringido **ou rotulado pela nossa equipe**".
- **LinkedIn** exibe o selo "CR" (Content Credentials) automaticamente quando o arquivo carrega
  metadado C2PA.

Onde a afirmação é **imprecisa ou falsa**:

1. **Meta é o furo.** A posição oficial da Meta, publicada em 06/02/2024 e ainda atualizada em
   01/04/2025 sem correção nesse ponto, é que para **vídeo fotorrealista e áudio realista** de
   outras empresas ela **ainda não consegue detectar os sinais**: *"we can't yet detect those
   signals and label this content from other companies"*. Por isso a Meta **exige que a pessoa
   declare**, com penalidade se não declarar: *"We'll require people to use this disclosure and
   label tool when they post organic content with a photorealistic video or realistic-sounding
   audio"*. A rotulagem automática confirmada da Meta é sobretudo em **imagem** (via C2PA, IPTC e
   marca d'água invisível). **Não encontrei nenhuma página oficial da Meta afirmando que hoje ela
   detecta vídeo de IA de terceiros no feed orgânico.** Ou seja: no Instagram, para o vídeo de
   avatar da Savylla, o rótulo tende a depender de quem publica — o cliente.
2. **O gatilho não é "detecção mágica", é metadado.** O rótulo aparece sozinho porque a
   *ferramenta* gravou uma credencial C2PA no arquivo, não porque a plataforma "olhou o vídeo e
   percebeu". Se o metadado for perdido numa reexportação, o rótulo automático pode simplesmente
   não aparecer. A detecção por modelo próprio existe (YouTube cita), mas é o menos previsível
   dos três caminhos.
3. **A obrigação primária continua sendo declarar.** YouTube e TikTok não tratam a rotulagem
   automática como substituto: os dois exigem a declaração do criador quando o conteúdo é
   realista, e os dois preveem punição para quem não declara. Dizer ao cliente "não precisa se
   preocupar, a plataforma resolve" seria errado — a responsabilidade é de quem publica.
4. **Nem tudo que a Savylla faz exige rótulo.** O YouTube isenta **explicitamente** clonar a
   própria voz para narração ou dublagem, e o TikTok isenta narração TTS genérica que não imite
   voz de pessoa conhecida. Expansão de plano e correção de cor também caem em "edições
   inconsequentes" na maioria das políticas.

**Tradução prática:** o rótulo aparece sozinho com frequência, mas não sempre, não em todas as
plataformas e não no Instagram para vídeo. O campo do formulário está certo em avisar que às
vezes não é escolha; está errado se der a entender que a plataforma sempre resolve.

---

## 2. Tabela por plataforma

| Plataforma | Declaração obrigatória? | Rótulo automático? | Como detecta | Onde aparece | Regra para anúncio | Fonte + data de acesso |
|---|---|---|---|---|---|---|
| **YouTube** | **Sim**, quando o conteúdo é realista: faz pessoa real dizer/fazer o que não fez, altera cena/lugar real, ou gera cena realista que não ocorreu. Isento: voz própria clonada para dublagem, filtro de beleza, cor, upscaling, legenda, conteúdo fantasioso | **Sim**, em 3 casos: ferramentas GenAI do YouTube, arquivo **com metadado C2PA**, ou detecção pelos sistemas do YouTube | C2PA + classificadores próprios + origem na própria ferramenta | Descrição expandida sempre; **no player** quando é fotorrealista | Sem regra de IA para anúncio comum. Para **anúncio eleitoral**, o Google exige marcar "Altered or synthetic content" nas configurações da campanha e gera aviso in-ad em alguns formatos | support.google.com/youtube/answer/14328491 · support.google.com/adspolicy/answer/6014595 — acesso 13/08/2026 |
| **TikTok** | **Sim**. "Exigimos que os criadores rotulem conteúdo gerado por IA ou significativamente editado que mostre cenas ou pessoas com aparência realista". Isento: cor/enquadramento/corte, estilo artístico (anime), TTS genérica que não imita voz conhecida | **Sim.** Efeitos de IA do TikTok são rotulados sozinhos; e o TikTok **lê Content Credentials (C2PA)** para "reconhecer e rotular AIGC instantaneamente". Além disso: conteúdo sem rótulo "pode ser removido, restringido **ou rotulado pela nossa equipe**" | C2PA (desde 09/05/2024) + moderação + origem na própria ferramenta | Rótulo AIGC no post (o criador também pode usar legenda, sticker ou marca d'água própria) | Não confirmei política de IA específica para TikTok Ads em fonte oficial | Community Guidelines, seção "Edited Media and AI-Generated Content (AIGC)", **efetivas 13/09/2025** · newsroom.tiktok.com 09/05/2024 · tiktok.com/transparency — acesso 13/08/2026 |
| **Meta (Instagram / Facebook)** | **Sim para vídeo e áudio.** A Meta exige que a pessoa use a ferramenta de declaração ao postar **vídeo fotorrealista ou áudio realista** criado/alterado digitalmente, e "pode aplicar penalidades" se não usar | **Parcialmente.** Automático confirmado sobretudo em **imagem**. Para vídeo/áudio de outras empresas, a Meta declara que **ainda não consegue detectar** os sinais | C2PA, metadado IPTC e marca d'água invisível — quando presentes na imagem | Rótulo "AI info" no post; em edição leve, o rótulo vai para o menu de três pontinhos | **Anúncio comum: não há exigência de divulgação de IA** nos Advertising Standards. **Anúncio de tema social, eleitoral ou político: divulgação obrigatória**; a partir de **01/06/2026** a Meta usa detecção automatizada para identificar mídia feita com IA de terceiros e mostra "AI info" no "Sobre este anúncio" | about.fb.com 06/02/2024 (atualizado 01/04/2025) e 05/04/2024 · transparency.meta.com Community Standards → Misinformation (atualizado 07/04/2025) · transparency.meta.com/policies/ad-standards/SIEP-advertising/SIEP — acesso 13/08/2026 |
| **LinkedIn** | **Sim, em caso restrito.** As Professional Community Policies dizem: *"Do not share synthetic or manipulated media that depicts a person saying something they did not say or doing something they did not do without clearly disclosing the fake or altered nature of the material."* Não há dever geral de rotular todo uso de IA | **Sim, mas só via C2PA.** O LinkedIn não roda detector próprio de IA: ele lê o metadado C2PA do arquivo e mostra o selo "CR" | Exclusivamente Content Credentials (C2PA) | Selo "CR" no canto da mídia in-stream; ao clicar, abre o painel com a ferramenta que criou e se houve IA | Não encontrei política de IA específica para LinkedIn Ads | linkedin.com/legal/professional-community-policies (sem data de revisão na página; rodapé "LinkedIn © 2026") · anúncio C2PA de 05/2024 — acesso 13/08/2026 |
| **Google Ads** | Só para **anúncio eleitoral**: "Advertisers must disclose all election ads that contain synthetic or digitally altered content", via checkbox "Altered or synthetic content". Isento: redimensionar, cortar, correção de cor/brilho, correção de defeito | Google gera o aviso in-ad em Feeds e Shorts no celular e em In-stream; nos demais formatos o anunciante é responsável por exibir o aviso | Declaração do anunciante | Aviso in-ad | Aviso prévio de pelo menos 7 dias antes de suspensão. Fora de eleição, a política de **Deturpação** proíbe "manipular mídia para enganar, fraudar ou induzir a erro" — é proibição, **não** um caminho de divulgação | support.google.com/adspolicy/answer/6014595 e /6020955 — acesso 13/08/2026 |

---

## 3. O mecanismo: C2PA e Content Credentials

**O que é.** C2PA (Coalition for Content Provenance and Authenticity) é um padrão aberto que grava
um manifesto assinado criptograficamente dentro do próprio arquivo — o "Content Credential". O
site oficial descreve como *"like a nutrition label for digital content"*: registra que ferramenta
criou o arquivo, quando, e que edições vieram depois. O comitê diretor inclui Adobe, Amazon, BBC,
Google, **Meta**, Microsoft, OpenAI, Sony, **TikTok** e Truepic (c2pa.org, atualizado 08/01/2026).

**Por que o rótulo aparece "sozinho".** A cadeia é esta, e ela tem três elos que podem quebrar:

1. A ferramenta de IA grava a credencial C2PA no arquivo na hora de gerar.
2. O arquivo chega à plataforma **com o metadado intacto**.
3. A plataforma lê o metadado no upload e aplica o rótulo.

Nenhuma das três plataformas "assiste ao vídeo e reconhece IA" como caminho principal — a
detecção por classificador próprio existe (o YouTube cita, a Meta cita para imagem), mas é o
caminho menos previsível. **O caminho previsível é o metadado.**

**O que remove o metadado.** O FAQ oficial do C2PA reconhece que *"C2PA Manifests are typically
embedded in the asset, they can be separated"* — ou seja, a credencial pode ser destacada do
arquivo. Na prática, qualquer reexportação num editor que não preserve C2PA, qualquer conversão de
container, um screenshot ou uma regravação de tela quebram o elo 2. Foi por isso que o padrão
criou as **Durable Content Credentials**: *"soft bindings — such as invisible watermarking or
fingerprinting — that can help rediscover the associated Content Credential even if it's removed
from the file"*.

**O que preserva.** Marca d'água invisível é mais resistente que metadado. O SynthID da Google
DeepMind, usado pela ElevenLabs, sobrevive segundo a própria ElevenLabs mesmo quando os clipes são
*"trimmed, sped up, stripped of metadata, or converted into a different file type"*. Ou seja: em
áudio, limpar o metadado não apaga a marca.

**Consequência para o briefing.** Não dá para prometer ao cliente que o vídeo *não* vai aparecer
rotulado, e também não dá para prometer que *vai*. O que dá para dizer com precisão é: o arquivo
sai da produção marcado, e a plataforma decide.

---

## 4. As ferramentas dela

| Ferramenta | Embute credencial/marca? | Dá para remover? | Fonte + data |
|---|---|---|---|
| **Runway** | **Sim.** "We do this by adding invisible watermarks to every Runway generation, thereby retaining evidence in the metadata that it is AI-generated." Runway declara ter adotado o padrão C2PA | Não há caminho oferecido pela ferramenta. O texto oficial não trata de remoção | runway.com/research/foundations-for-safe-generative-media, 07/10/2024 — acesso 13/08/2026 |
| **Synthesia** | **Sim, por padrão.** "relevant videos you generate with Synthesia carry C2PA-compliant provenance signals that mark them as AI-generated, with no setup required from you". Separadamente, existe um **rótulo visível "AI-generated"** opcional, que o admin do workspace pode ligar para todos os vídeos ou o usuário pode ligar por cena (Editor → Media → AI Labels; aparece no canto superior direito). Vídeos de plano gratuito já saem com marca d'água | O rótulo **visível** é opcional e você escolhe. A credencial **C2PA é automática e não é opcional**. A Acceptable Use Policy proíbe expressamente: *"Removing, deactivating or disabling any 'watermarks' or other mechanisms of the Services that are designed to help validate provenance or differentiate between human-generated and AI-generated content"* | help.synthesia.io, artigo sobre o Article 50 (atualizado 13/08/2026) · synthesia.io/legal/acceptable-use-policy (atualizada 23/02/2024) · synthesia.io/legal/ai-governance-practices (09/2024) — acesso 13/08/2026 |
| **ElevenLabs** | **Sim.** Marca d'água **SynthID** embutida no áudio, começando em 25/06/2026 pelo Text to Speech de usuários gratuitos e "we will expand coverage to all ElevenLabs audio generations over the coming weeks" (post atualizado em 09/08/2026). Também oferece o AI Speech Classifier e cita suporte a C2PA na página de Safety | A página oficial **não menciona opção de opt-out**. E a marca sobrevive a corte, mudança de velocidade, remoção de metadado e conversão de formato | elevenlabs.io/blog/synthid (25/06/2026, atualizado 09/08/2026) · elevenlabs.io/safety — acesso 13/08/2026 |
| **HeyGen** | **Não confirmado.** A página oficial de ética diz apenas que a HeyGen é *"a member of the Content Authenticity Initiative"* — **não afirma** que embute C2PA nos exports. Não encontrei nenhuma página oficial da HeyGen dizendo que o vídeo exportado carrega Content Credentials ou marca d'água invisível. A marca d'água **visível** com o logo HeyGen é padrão e sai nos planos pagos com um toggle | A marca **visível** sai: "Toggle off the watermark option at the bottom left of the menu". Sobre marca invisível, a documentação oficial é silenciosa | heygen.com/ethics (statement efetivo 13/11/2023, rodapé © 2026) · help.heygen.com, artigo "How to Remove the HeyGen Watermark" — acesso 13/08/2026 |

**Leitura para o cliente:** com **Runway, Synthesia e ElevenLabs**, o arquivo sai marcado e o
cliente **não tem escolha real** sobre a marca técnica — só sobre o rótulo visível na tela (e, no
caso da Synthesia, o contrato proíbe tentar remover a marca). Com **HeyGen**, não há confirmação
oficial de marca invisível, então o resultado é imprevisível — não prometa nada.

---

## 5. Se rodar fora do Brasil

### Vigente a partir de 02/08/2026 — já valendo hoje

**União Europeia — AI Act, Artigo 50 (Regulamento UE 2024/1689).** Aplica-se **desde 02/08/2026**,
confirmado pelo FAQ oficial da Comissão Europeia (publicado em 24/07/2026). Duas obrigações
distintas, e elas caem em pessoas diferentes:

- **Art. 50(2) — marcação legível por máquina** é dever do **provedor** do sistema de IA (Runway,
  Synthesia, ElevenLabs), não da Savylla nem do cliente. *"os outputs do sistema de IA são
  marcados em formato legível por máquina e detectáveis como artificialmente gerados ou
  manipulados"*.
- **Art. 50(4) — divulgação visível de deepfake** é dever do **deployer**, isto é, **de quem
  publica**. Precisa ser *"clear and distinguishable"* e mostrada no **primeiro contato** do
  espectador com o conteúdo, por meio *"understandable and perceivable by natural persons (e.g.
  with visible or audible labels)"*.
- **Definição de deepfake** no FAQ da Comissão: três critérios cumulativos — alta semelhança com
  algo/alguém existente, retrata algo que existe ou poderia plausivelmente existir, e tem
  capacidade de enganar sobre a autenticidade. **Atenção:** a própria Synthesia alerta na
  documentação dela que *"a realistic AI presenter can fall within the visible-disclosure rules
  even if the avatar is not a real, identifiable person"*. Ou seja, avatar digital realista para
  público europeu provavelmente exige rótulo **visível**, não bastando o C2PA.
- **Exceção artística:** conteúdo que faz parte de obra *"evidently artistic, creative, satirical,
  fictional or analogous"* só precisa indicar a existência do material gerado, de forma que não
  atrapalhe a fruição da obra.
- **Prazo estendido:** sistemas colocados no mercado antes de 02/08/2026 têm até **02/12/2026**
  para cumprir integralmente a obrigação de marcação.
- **Retroatividade:** segundo a orientação europeia citada pela Synthesia, **não há obrigação de
  reetiquetar** conteúdo gerado antes de 02/08/2026.
- **Multa:** até €15 milhões ou 3% do faturamento global anual, o que for maior.

**Califórnia — AI Transparency Act (SB 942).** Também entra em vigor em **02/08/2026** (a data
original foi adiada pela AB 853, assinada em 13/10/2025). A obrigação recai sobre o **provedor**
de IA generativa com mais de 1 milhão de visitantes/usuários mensais: manter ferramenta gratuita
de detecção, oferecer opção de divulgação em manifesto, e aplicar divulgação latente de
proveniência. A Synthesia confirma na documentação oficial dela: *"The Act does not place
obligations on customers who generate videos"* — ou seja, **não recai sobre a Savylla nem sobre o
cliente**. Multa de US$ 5.000 por violação, por dia.

### Réplica digital de performer nos EUA

Isso é o que morde quando a peça usa **avatar com rosto ou voz de pessoa real**:

- **Tennessee — ELVIS Act** (Ensuring Likeness Voice and Image Security), sancionada em
  21/03/2024, **em vigor desde 01/07/2024**. Proíbe usar nome, foto, voz ou imagem de alguém sem
  consentimento para publicidade, e proíbe distribuir tecnologia cujo propósito primário seja
  gerar réplica não autorizada de voz ou imagem.
- **Califórnia — AB 2602 e AB 1836**, sancionadas em 17/09/2024. A AB 2602 invalida cláusula
  contratual que autorize réplica digital sem consentimento informado e representação adequada do
  intérprete; a AB 1836 proíbe réplica digital de intérprete falecido sem consentimento do
  espólio. **As fontes secundárias divergem sobre a data exata de vigência da AB 1836** (01/01/2025
  vs 01/01/2026) — ver seção 8.

**Consequência para o briefing:** para peça que roda na Europa, o rótulo visível na tela deixa de
ser preferência do cliente e vira provável obrigação legal dele — e o campo do formulário deveria
saber disso. Para peça nos EUA com rosto ou voz de pessoa real, o que importa mais é o
**consentimento por escrito do intérprete**, não a rotulagem.

---

## 6. O que isso significa para o campo do formulário

### O microcopy atual

> "YouTube, TikTok e Instagram hoje colocam esse aviso por conta própria quando identificam IA —
> então em parte dos casos não é escolha nossa."

**Veredito: quase certo, com um erro específico e uma imprecisão de mecanismo.**

1. **Erro:** citar o **Instagram** ao lado de YouTube e TikTok como quem "coloca por conta
   própria". A posição oficial da Meta é que ela **ainda não detecta** vídeo de IA de outras
   empresas — a rotulagem automática dela é sobretudo em imagem, e para vídeo ela **exige que
   quem publica declare**. Na plataforma onde o cliente mais publica, o rótulo depende do cliente,
   não da plataforma.
2. **Imprecisão:** "quando identificam IA" sugere que a plataforma analisa o vídeo. O que
   acontece é mais simples e mais fácil de explicar: a ferramenta grava uma marca no arquivo e a
   plataforma lê essa marca.
3. **Falta o essencial:** o microcopy não diz que **declarar é obrigação de quem publica** quando
   o vídeo mostra uma pessoa realista. Isso é o dado que muda a decisão do cliente.

### Versão reescrita (sugestão)

> As ferramentas de IA gravam uma marca invisível dentro do arquivo. YouTube, TikTok e LinkedIn
> leem essa marca e podem exibir o aviso sozinhos — nesses casos não é escolha nossa nem sua.
> No Instagram costuma depender de quem publica. E quando o vídeo mostra uma pessoa com aparência
> realista, YouTube e TikTok exigem que quem posta declare. Se isso for um problema para a marca,
> me diga agora: dá para desenhar a peça de um jeito que não caia na regra.

### Versão curta, se o campo for apertado

> A ferramenta grava uma marca invisível no arquivo, e algumas plataformas exibem o aviso sozinhas
> ao ler essa marca. Em outras, quem publica é que precisa declarar. Ou seja: nem sempre é escolha
> nossa — e é melhor combinar isso antes de produzir.

### Observação de escopo (vale acrescentar ao campo ou ao aviso vizinho)

Nem toda peça com IA cai na regra. Pelas políticas oficiais, **não exigem rótulo**: clonar a
própria voz para narração ou dublagem (isenção explícita do YouTube), narração TTS genérica que
não imita voz de pessoa conhecida (isenção explícita do TikTok), correção de cor, reenquadramento
e corte. **Exigem rótulo**: avatar ou rosto realista, troca de rosto, voz de IA que imita pessoa
real, e cena realista que não aconteceu.

---

## 7. O que ela deve avisar ao cliente na proposta

Quatro frases prontas, em linguagem de cliente:

1. "Os vídeos que eu entrego saem com uma marca técnica invisível dizendo que foram feitos com IA
   — isso vem das próprias ferramentas e não dá para desligar."
2. "Algumas plataformas leem essa marca e colocam o aviso 'feito com IA' automaticamente; no
   Instagram, normalmente é quem publica que precisa marcar."
3. "Quando o vídeo mostra uma pessoa com aparência realista, YouTube e TikTok exigem que quem
   posta declare — e a responsabilidade pela declaração é de vocês, que publicam. Não declarar
   pode custar remoção ou restrição do vídeo."
4. "Se a peça for rodar na Europa a partir de agosto de 2026, o aviso na tela deixa de ser
   preferência e passa a ser exigência legal para quem publica — melhor já desenhar assim."

---

## 8. O que eu NÃO consegui confirmar

- **Se a Meta passou a detectar vídeo de IA de terceiros no feed orgânico em 2025 ou 2026.** A
  declaração oficial mais recente que encontrei ("we can't yet detect those signals") é de
  06/02/2024, com atualização de página em 01/04/2025 que não corrigiu esse trecho. Vários blogs
  de 2026 afirmam que a Meta hoje rotula tudo sozinha, **mas nenhum aponta para página oficial da
  Meta que sustente isso** — tratei como não confirmado.
- **A página oficial de central de ajuda da Meta sobre o rótulo "AI info" no Instagram.** As URLs
  que tentei retornaram 404 ou página indisponível. Usei em substituição: about.fb.com (newsroom
  oficial), Transparency Center (Community Standards → Misinformation, e Ad Standards → SIEP) e
  meta.com/help sobre IA em anúncios.
- **Data de última revisão da página do YouTube** (support.google.com/youtube/answer/14328491) —
  a página não exibe data.
- **Data de revisão das Professional Community Policies do LinkedIn** — a página não exibe data.
- **Política de IA do TikTok Ads e do LinkedIn Ads.** Não localizei página oficial específica.
- **Se a HeyGen embute C2PA ou marca d'água invisível nos exports.** A única afirmação oficial que
  achei é filiação à Content Authenticity Initiative — o que **não** é o mesmo que embutir
  credencial. Um blog de terceiros afirma que a HeyGen "embeds invisible C2PA container metadata";
  não achei confirmação da HeyGen. **Recomendo teste empírico:** exportar um vídeo e abrir em
  verify.contentauthenticity.org.
- **Se o rótulo de IA afeta alcance.** O YouTube afirma oficialmente que não ("Disclosing AI
  content won't limit a video's audience or impact its eligibility to earn money"). Encontrei
  afirmação equivalente atribuída ao TikTok, mas só em resumo de busca — não confirmei na página
  oficial. Da Meta, não achei declaração nenhuma.
- **Data exata de vigência da AB 1836 na Califórnia** — fontes jurídicas secundárias divergem
  entre 01/01/2025 e 01/01/2026. Não abri o texto oficial da lei.
- **Regra brasileira específica de rotulagem de IA em publicidade (CONAR / ANPD / PL 2338).** Não
  pesquisei — orçamento de buscas esgotado nesta sessão. **Fica como lacuna para a próxima
  rodada**, e é a mais relevante das lacunas, já que os clientes dela são brasileiros.

---

## 9. Fontes

Todas acessadas em **13/08/2026**.

**Plataformas**

| # | URL | O que entregou | Data da fonte |
|---|---|---|---|
| 1 | https://support.google.com/youtube/answer/14328491 | Política de divulgação de conteúdo alterado/sintético do YouTube: o que exige rótulo, as isenções (inclusive clonar a própria voz), onde o rótulo aparece, rotulagem automática (ferramentas próprias, C2PA, detecção) e penalidade | sem data na página |
| 2 | https://support.google.com/adspolicy/answer/6014595 | Política de Conteúdo político do Google Ads: divulgação obrigatória de conteúdo sintético em anúncio eleitoral, checkbox na campanha, formatos com aviso automático, isenções, aviso de 7 dias antes de suspensão. Confirmou que **não há** exigência de IA para anúncio não político | — |
| 3 | https://support.google.com/adspolicy/answer/6020955 | Política de Deturpação do Google Ads: "Manipulating media to deceive, defraud, or mislead others is not allowed" — proibição, sem via de divulgação | — |
| 4 | https://www.tiktok.com/community-guidelines/en/integrity-authenticity | **Texto oficial** da seção "Edited Media and AI-Generated Content (AIGC)": exigência de rótulo, lista do que exige divulgação, lista do que **não** exige (TTS genérica, estilo artístico, edições pequenas), lista do que é proibido, e "Unlabeled content may be removed, restricted, or labeled by our team" | efetivas 13/09/2025 |
| 5 | https://newsroom.tiktok.com/en-us/partnering-with-our-industry-to-advance-ai-transparency-and-literacy | TikTok lê Content Credentials no upload e auto-rotula AIGC de outras plataformas; promessa de anexar Content Credentials ao download | 09/05/2024 |
| 6 | https://www.tiktok.com/transparency/en/supporting-responsible-transparent-ai-generated-content/ | "we are members of the Coalition for Content Provenance and Authenticity (C2PA) and have adopted their Content Credentials, which enable our systems to instantly recognize and label AIGC" | — |
| 7 | https://newsroom.tiktok.com/en-us/new-labels-for-disclosing-ai-generated-content | Origem da exigência de rótulo e renomeação dos efeitos de IA do TikTok | 19/09/2023 |
| 8 | https://about.fb.com/news/2024/02/labeling-ai-generated-images-on-facebook-instagram-and-threads/ | **A fonte decisiva sobre a Meta:** C2PA e IPTC + marca d'água invisível em imagem; "we can't yet detect those signals" para vídeo/áudio de terceiros; exigência de declaração para vídeo fotorrealista e áudio realista, com penalidade | 06/02/2024, atualizado 01/04/2025 |
| 9 | https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/ | Evolução do rótulo "Made with AI" → "AI info" (01/07/2024) e movimento do rótulo para o menu em edição leve (12/09/2024); rótulo mais destacado em caso de alto risco de engano | 05/04/2024 |
| 10 | https://transparency.meta.com/policies/community-standards/misinformation/ | Regra de mídia manipulada: rótulo informativo (em vez de remoção) para mídia fotorrealista digitalmente criada/alterada com "particularly high risk of materially deceiving the public on a matter of public importance" | atualizado 07/04/2025 |
| 11 | https://transparency.meta.com/policies/ad-standards/SIEP-advertising/SIEP/ | Divulgação obrigatória de IA em anúncio de tema social/eleitoral/político; rejeição do anúncio e penalidade por reincidência; **detecção automatizada a partir de 01/06/2026** com "AI info" no "Sobre este anúncio" | — |
| 12 | https://transparency.meta.com/policies/ad-standards/ | Confirmou que **não existe** seção exigindo divulgação de IA em anúncio comum | — |
| 13 | https://www.meta.com/help/artificial-intelligence/355108217670024/ | Rótulo "AI info" em anúncios feitos com as ferramentas de IA **da própria Meta**; rollout gradual; rótulo ao lado de "Patrocinado" quando há humano fotorrealista gerado por IA | sem data |
| 14 | https://transparency.meta.com/governance/tracking-impact/labeling-ai-content/ | Confirmou início da rotulagem em 05/2024 e que a metodologia "is still evolving" — página de métricas, não de política | dados de 10/2024 |
| 15 | https://www.linkedin.com/legal/professional-community-policies | Única regra do LinkedIn sobre o tema: "Do not share synthetic or manipulated media that depicts a person saying something they did not say or doing something they did not do without clearly disclosing the fake or altered nature of the material" | sem data na página |

**Padrão técnico**

| # | URL | O que entregou | Data |
|---|---|---|---|
| 16 | https://c2pa.org/ | Definição de Content Credentials ("nutrition label for digital content") e composição do comitê diretor, incluindo Meta e TikTok | atualizado 08/01/2026 |
| 17 | https://c2pa.org/faqs/ | Manifestos C2PA "can be separated" do arquivo; Durable Content Credentials com soft binding (marca d'água invisível / fingerprint) para recuperar a credencial removida | ref. a 01/01/2026 |

**Ferramentas**

| # | URL | O que entregou | Data |
|---|---|---|---|
| 18 | https://runway.com/research/foundations-for-safe-generative-media | "adding invisible watermarks to every Runway generation"; adoção do C2PA | 07/10/2024 |
| 19 | https://help.synthesia.io/en/articles/16046624-what-does-the-eu-ai-act-article-50-mean-for-my-synthesia-videos | **A fonte mais completa da pesquisa.** C2PA automático em todo vídeo relevante; rótulo visível opcional e como ligá-lo; divisão provider × deployer no AI Act; datas 02/08/2026 e 02/12/2026; SB 942 não recai sobre o cliente; sem retroatividade; multas | atualizado 13/08/2026 |
| 20 | https://www.synthesia.io/legal/acceptable-use-policy | Proibição contratual de remover, desativar ou desabilitar marcas d'água e mecanismos de proveniência | 23/02/2024 |
| 21 | https://www.synthesia.io/legal/ai-governance-practices | Marcadores de áudio/vídeo opcionais para transparência sob o AI Act; vídeos freemium já saem com marca d'água | 09/2024 |
| 22 | https://elevenlabs.io/blog/synthid | SynthID em geração de áudio a partir de 25/06/2026, expandindo para todas as gerações; sobrevive a corte, mudança de velocidade, remoção de metadado e conversão de formato; sem menção a opt-out | 25/06/2026, atualizado 09/08/2026 |
| 23 | https://elevenlabs.io/safety | AI Speech Classifier e princípio "People should know when they're interacting with AI"; referência ao C2PA | sem data |
| 24 | https://www.heygen.com/ethics | Filiação à Content Authenticity Initiative — **sem** afirmação de que embute C2PA nos exports; consentimento expresso obrigatório para avatar de pessoa real | statement efetivo 13/11/2023 |
| 25 | https://www.heygen.com/moderation-policy | Consentimento explícito do "Actor" obrigatório para avatar customizado; direito do Actor de pedir remoção a qualquer momento | efetiva 25/07/2024 |
| 26 | https://help.heygen.com/en/articles/11057301-how-to-remove-the-heygen-watermark | Marca d'água visível padrão em todos os vídeos; toggle de remoção nos planos pagos; nada sobre marca invisível | sem data |

**Regulação**

| # | URL | O que entregou | Data |
|---|---|---|---|
| 27 | https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act | FAQ oficial da Comissão Europeia: obrigação de marcação legível por máquina (provedor) e divulgação visível de deepfake (deployer); definição de deepfake em 3 critérios; exceção artística; aplicação desde 02/08/2026 com prazo de 02/12/2026 | publicado 24/07/2026 |
| 28 | https://artificialintelligenceact.eu/article/50/ | Texto dos parágrafos 2 e 4 do Artigo 50 e data de aplicação | — |

**Fontes secundárias usadas apenas para localizar mudança (nunca como base de afirmação):**
searchengineland.com, socialmediatoday.com, fortune.com, nbcnews.com, mediapost.com,
manatt.com, proskauer.com, insideglobaltech.com (ELVIS Act e AB 2602/1836), e diversos blogs de
marketing de 2026 cujas afirmações sobre a Meta **não** foram confirmadas em fonte oficial.
