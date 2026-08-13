# Imagem, voz e biometria — o que protege e o que expõe

> Pesquisa de **13/08/2026**. Lei e súmula foram conferidas na fonte primária
> (Planalto e STJ), não citadas de memória. O acórdão brasileiro sobre voz
> clonada por IA foi lido na íntegra, não por resumo.
>
> **Isto não é parecer jurídico.** É um mapa do terreno para decidir o que
> perguntar no briefing e o que colocar no contrato — e para saber quando
> chamar advogado.

Documento irmão: `docs/research/2026-08-13-formularios-por-servico/07-producao-com-ia.md`,
que trata de rotulagem, política de plataforma e licenciamento de ferramenta.
Aqui o assunto é outro: **de quem é a responsabilidade e o que precisa estar
escrito.**

---

## 1. Resposta direta

- **Uma autorização de imagem antiga quase certamente NÃO cobre alteração por
  IA.** Não é opinião isolada: o direito brasileiro manda interpretar
  restritivamente esse tipo de negócio, e a regra é que **cada modalidade de
  uso é independente das outras** — o que não foi escrito, não está autorizado.
  Um contrato que libera "editar e modificar" libera cortar, colorizar, montar.
  Não libera **fabricar uma cena que a pessoa nunca gravou**. (§3)

- **A voz é protegida, e com nome e sobrenome na Constituição.** O art. 5º,
  XXVIII, "a" cita literalmente "a reprodução da imagem e voz humanas", e o
  art. 20 do Código Civil protege "a transmissão da palavra". Voz não é um
  apêndice da imagem — é um direito próprio, que exige autorização própria. (§2)

- **Existe caso brasileiro sobre clone de voz por IA, e nele "foi a IA que fez"
  não foi defesa — foi agravante.** No TJSP, um shopping alegou que a voz do
  comercial era sintética (voz "Antônio", do Microsoft Azure). O tribunal mandou
  fazer perícia assim mesmo: *"o uso de Inteligência Artificial, por si só, não
  elimina — bem pelo contrário, agrava — o risco de utilização indevida de
  direitos de terceiros."* E listou, entre o que seria apurado, **"quem foi
  contratado para produzi-la, se houve algum tipo de verificação prévia"** — ou
  seja, **a produtora entra na conta, e o que a defende é ter verificado antes,
  por escrito.** É o único caso que achei, e é decisão de processo, não
  condenação final. (§2, §5)

- **Rosto filmado não é automaticamente "dado sensível" — mas criar avatar e
  clonar voz provavelmente é.** A LGPD diz "dado biométrico" **sem definir o
  termo, e a ANPD também não define**: conferi o Glossário oficial da autoridade
  (atualizado em julho/2026) e **não há verbete de biometria, reconhecimento
  facial nem IA**. Na ausência de definição, a leitura defensável é a do GDPR —
  biométrico é o dado que passa por *processamento técnico específico* que
  permite identificar unicamente alguém. Filmar um rosto é dado pessoal comum;
  **extrair as características daquele rosto e daquela voz para gerar falas
  novas é exatamente esse processamento.** Aí entra o art. 11: consentimento
  **específico e destacado**, e **sem a opção de legítimo interesse**. (§4)

- **Na produção ela é operadora, e a ANPD diz que isso protege bastante.** A
  marca decide a finalidade, logo é controladora. O guia oficial da ANPD (v2.0,
  item 60) afirma que **"em regra a responsabilidade é do controlador"** e que a
  equiparação do operador ao controlador é **"uma excepcionalidade"**. A exceção
  tem duas portas (art. 42, §1º, I): descumprir a lei, ou não seguir instrução
  **lícita**. Traduzindo: **enquanto ela seguir instrução lícita e documentada,
  o risco é do cliente.** O escudo não é o rótulo — é a instrução por escrito
  mais a verificação registrada. (§5)

- **No portfólio ela não é operadora — é controladora.** Quem decide exibir os
  vídeos no site dela para vender serviço é ela. E o site hoje publica **78
  nomes próprios de pessoas** ao lado do rosto delas. Isso é tratamento de dado
  pessoal por conta própria, sem nenhuma autorização escrita para esse uso
  específico. **"Mas já está público" não resolve** — o STJ já decidiu que estar
  acessível na internet não presume domínio público nem autoriza reuso. A boa
  notícia: **não existe jurisprudência brasileira de produtora processada por
  portfólio**, o cenário realista é notificação, não ação, e a ordem de grandeza
  de condenação em caso análogo foi **R$ 3.000**. (§6)

- **Autorização genérica é nula por texto expresso de lei.** LGPD, art. 8º,
  §4º: *"as autorizações genéricas para o tratamento de dados pessoais serão
  nulas."* No eixo do direito de imagem ela não é nula, mas é **encolhida** pelo
  juiz ao prazo, à praça e à finalidade originais. Como avatar e clone caem nos
  dois eixos, a autorização genérica **não serve em nenhum dos dois**. (§3)

- **O contrato-padrão do mercado publicitário brasileiro já resolve isso — a
  favor dela.** O modelo ABAP/APRO autoriza "montagem, cortes e reproduções"
  (verbos de edição, não de geração) e diz que **"qualquer utilização não
  prevista neste contrato" depende de expressa anuência**. E, nesse mesmo padrão,
  quem contrata o direito de imagem é **a agência por conta do anunciante**, não
  a produtora — com **taxa de 40%** se a produtora assumir esse serviço. Ela não
  está pedindo favor: está pedindo o padrão do setor. (§3, §7)

---

## 2. Direito de imagem e voz — a base

Quatro camadas se somam. Todas conferidas na fonte.

### Constituição Federal

**Art. 5º, X** — o alicerce:

> "são invioláveis a intimidade, a vida privada, a honra e a imagem das
> pessoas, assegurado o direito a indenização pelo dano material ou moral
> decorrente de sua violação"

**Art. 5º, XXVIII, "a"** — o dispositivo que quase ninguém cita, e que resolve
a dúvida sobre voz:

> "são assegurados, nos termos da lei: a) a proteção às participações
> individuais em obras coletivas e à reprodução da imagem **e voz humanas**,
> inclusive nas atividades desportivas"

A voz está no texto constitucional, ao lado da imagem, e no capítulo de obras
coletivas — que é exatamente o caso de uma produção audiovisual.

### Código Civil

**Art. 20** — o artigo operacional:

> "Salvo se autorizadas, ou se necessárias à administração da justiça ou à
> manutenção da ordem pública, a divulgação de escritos, **a transmissão da
> palavra**, ou a publicação, a exposição ou a utilização da imagem de uma
> pessoa poderão ser proibidas, a seu requerimento e sem prejuízo da
> indenização que couber, se lhe atingirem a honra, a boa fama ou a
> respeitabilidade, **ou se se destinarem a fins comerciais**."

Dois pontos que mudam a leitura do dia a dia:

1. **"A transmissão da palavra"** é a voz. Está no mesmo artigo da imagem, com
   a mesma proteção.
2. **"Ou se se destinarem a fins comerciais"** é uma condição *alternativa*, não
   cumulativa. Não precisa ofender a honra de ninguém. Se o uso é comercial e
   não foi autorizado, já basta. Todo trabalho de marca é uso comercial.

**Art. 11** — por que "assinou uma vez, resolvido para sempre" não funciona:

> "Com exceção dos casos previstos em lei, os direitos da personalidade são
> intransmissíveis e irrenunciáveis, não podendo o seu exercício sofrer
> limitação voluntária."

Imagem e voz não são vendidas como se vende um bem: elas são **autorizadas**,
dentro de limites. É a razão técnica pela qual autorização eterna e irrestrita
é juridicamente frágil.

**Art. 12** — a pessoa pode exigir que o uso **cesse**, além de pedir perdas e
danos. Não é só dinheiro: é tirar do ar.

**Art. 186 e 927** — quem causa dano repara. E o art. 927, parágrafo único,
prevê reparação **independentemente de culpa** quando "a atividade normalmente
desenvolvida pelo autor do dano implicar, por sua natureza, risco para os
direitos de outrem" — argumento que já aparece em artigos sobre IA, embora eu
não tenha achado decisão aplicando isso a produção com IA.

**Art. 934** — a base legal do direito de regresso: quem paga por dano causado
por outro **pode cobrar de volta de quem causou**. É o artigo que sustenta a
cláusula do §7.

### Súmula 403 do STJ — texto confirmado no original

Li o PDF oficial do STJ. O enunciado é:

> **SÚMULA N. 403**
> "Independe de prova do prejuízo a indenização pela publicação não autorizada
> de imagem de pessoa com fins econômicos ou comerciais."

Dados do enunciado, do próprio documento:

| | |
|---|---|
| Órgão | **Segunda Seção**, em 28.10.2009 |
| Publicação | **DJe 24.11.2009**, ed. 486 |
| Referências | CF/1988, art. 5º, V e X · CC/1916, art. 159 · CC/2002, arts. 186 e 927 |
| Precedentes | EREsp 230.268-SP · REsp 85.905-RJ · REsp 138.883-PE · REsp 207.165-SP · REsp 267.529-RJ · REsp 270.730-RJ · REsp 331.517-GO · REsp 1.053.534-RN · REsp 1.082.878-RJ |

**O que isso significa na prática.** A pessoa que aparece não precisa provar
que sofreu, que perdeu dinheiro, que passou vergonha. Provado o uso comercial
sem autorização, o dano é presumido (*in re ipsa*) e a indenização é devida. O
ônus vira todo do lado de quem publicou.

Uma ressalva honesta: a Súmula 403 **não é absoluta**. A jurisprudência a
afasta em algumas situações — imagem ligada a fato histórico de repercussão
social, e a tese do "mero coadjuvante" (pessoa que aparece incidentalmente, não
como elemento central). Nada disso socorre um avatar ou um protagonista de
campanha, que são o oposto de incidental.

### Lei de Direitos Autorais (9.610/98) — a camada que quase sempre esquecem

Não é a lei da imagem, mas ela governa a **obra** e o **intérprete**, e é dela
que vem o raciocínio decisivo do §3:

**Art. 4º** — a regra de ouro:

> "Interpretam-se restritivamente os negócios jurídicos sobre os direitos
> autorais."

**Art. 49** — limites da cessão. Dois incisos são diretamente úteis:

> "V - a cessão só se operará para **modalidades de utilização já existentes à
> data do contrato**;
> VI - não havendo especificações quanto à modalidade de utilização, o contrato
> será interpretado restritivamente, entendendo-se como limitada apenas a uma
> que seja aquela indispensável ao cumprimento da finalidade do contrato."

**Art. 50, §2º** — o que é essencial num instrumento de cessão:

> "Constarão do instrumento de cessão como elementos essenciais seu objeto e as
> **condições de exercício do direito quanto a tempo, lugar e preço**."

Tempo, lugar e preço. É a origem da tríade **prazo, praça e finalidade** que o
mercado usa.

### A voz clonada por IA — o único caso brasileiro que encontrei

**Apelação Cível nº 1119021-41.2023.8.26.0100** — TJSP, 6ª Câmara de Direito
Privado, relator Des. **José Carlos Costa Netto**, julgado em **31/10/2024**,
votação unânime. Li o acórdão inteiro (9 páginas).

**O caso.** Um locutor (Igor Lott Zeger Belkind) processou a Associação dos
Lojistas do Shopping Jardim Anália Franco alegando que sua voz foi usada sem
autorização numa campanha publicitária no YouTube. Juntou ata notarial
atestando a semelhança das vozes. **A defesa do shopping foi dizer que a voz
era gerada por IA** — apresentou declaração do contratado que fez a propaganda,
afirmando ter usado a ferramenta "Microsoft Azure" para gerar uma voz
artificial, chamada no aplicativo de "Antônio". A sentença de 1º grau aceitou
essa defesa e julgou improcedente.

**O que o tribunal decidiu.** Anulou a sentença por cerceamento de defesa e
determinou perícia. Trechos literais da ementa:

> "Apelada que comprovou ter utilizado voz gerada por Inteligência Artificial –
> Tecnologias de IA generativa que se servem de bancos de dados prévios –
> **Possibilidade de cometimento de plágio e violação a direitos da
> personalidade ao utilizar-se de IA generativa – Dever de cuidado –
> Responsabilidade do usuário do software de IA, bem como do desenvolvedor** –
> Recorrência das ações que apenas comprova que a IA está gerando voz similar à
> do autor, não afastando a probabilidade de se tratar rigorosamente da mesma
> voz – Necessidade de realização de prova pericial – Sentença anulada –
> Recurso provido."

E do corpo do voto:

> "Em suma, vê-se que o uso de Inteligência Artificial, por si só, não elimina —
> bem pelo contrário, agrava — o risco de utilização indevida de direitos de
> terceiros."

> "Não se pode excluir, portanto, a possibilidade de que, ao realizar o uso de
> voz gerada por um software, tenha a ré infringido **o dever de cuidado**
> quanto à utilização da PIA, sendo responsável por este motivo, pela reparação
> dos danos gerados."

E o trecho que importa mais para ela — o que o tribunal disse que será apurado:

> "Apenas então será possível às partes discutir, por meio das provas, **como
> foi gerada a PIA, quem foi contratado para produzi-la, se houve algum tipo de
> verificação prévia**, para analisar também as circunstâncias da
> responsabilidade, a gravidade da conduta, e assim determinar a
> responsabilidade e a indenização."

**Leitura para o negócio dela — quatro conclusões:**

1. Usar **voz sintética de catálogo**, de ferramenta grande e legítima, **não
   encerra a discussão**. O shopping usou uma voz pronta da Microsoft e ainda
   assim foi para perícia.
2. O tribunal criou, na prática, um **dever de cuidado** de quem usa a
   ferramenta — não só de quem a desenvolve.
3. **"Quem foi contratado para produzi-la"** é pergunta expressa do processo. A
   produtora é parte do exame, não espectadora.
4. **"Se houve algum tipo de verificação prévia"** é a outra pergunta expressa.
   Isso transforma o formulário de briefing de burocracia em **prova**. Um
   briefing respondido e arquivado é literalmente o documento que responde a
   essa pergunta a favor dela.

**Status:** é decisão **processual** (anulou sentença, mandou instruir). Não
achei o desfecho do mérito. Não use como "o STJ decidiu que" — não decidiu, e
não é o STJ.

### O precedente do CONAR — e por que ele é a melhor notícia do documento

**Volkswagen / Elis Regina (2023)** é o precedente institucional brasileiro mais
relevante sobre IA e imagem — e é **autorregulatório, não judicial**. A VW
ressuscitou digitalmente Elis Regina num comercial de aniversário. O CONAR
instaurou processo ético e **arquivou por unanimidade**.

Os três fundamentos do arquivamento formam, na prática, um **roteiro de
conformidade**:

1. **Houve consentimento de quem titulariza o direito** — os herdeiros
   autorizaram;
2. **O uso foi coerente com a pessoa real** — Elis aparecia "fazendo algo que
   fazia em vida", não dizendo coisas que jamais diria;
3. **O uso de IA estava evidente na peça** — houve transparência.

**Consentimento + coerência + transparência.** É praticamente o mesmo tripé do
art. 50 do AI Act europeu e do "reasonably specific description" da SAG-AFTRA —
três sistemas chegando ao mesmo lugar. E é acionável: se o projeto dela passa
nesses três testes, ela está no lado certo do único precedente brasileiro
favorável que existe.

Uma nuance que vale reter para o negócio: o teste 2 (coerência) é o que separa
"avatar da porta-voz da marca dizendo o que ela diria" de "fabricar uma
declaração". A primeira coisa é o serviço dela. A segunda é o problema.

### O que a lei estrangeira já resolveu (e que aqui ainda não)

Não vale como lei no Brasil, mas mostra para onde a régua está indo — e serve
para negociar com cliente internacional. O documento 07 cobre o eixo de
**rotulagem**; aqui o eixo é **consentimento**:

| Norma | Status | O que importa |
|---|---|---|
| **ELVIS Act** (Tennessee, EUA) | **Lei, desde 01/07/2024** | Estende o direito de imagem à **voz**, e define voz como som identificável atribuível a alguém "**independentemente de conter a voz real ou uma simulação da voz**". Fecha exatamente a defesa que o shopping tentou no caso do TJSP |
| **California AB 2602** | **Lei, desde 01/01/2025** | Torna **inexequível** cláusula de réplica digital que **não traga "descrição razoavelmente específica" dos usos pretendidos** e tenha sido assinada sem advogado ou sindicato. É a consagração legal do "genérico não vale" |
| **California AB 1836** | **Lei, desde 01/01/2026** | Réplica digital de pessoa **falecida** exige consentimento prévio específico dos titulares |
| **EU AI Act, art. 50** | **Lei; obrigações desde 02/08/2026** | Quem implanta sistema que gera deepfake deve **divulgar que o conteúdo é artificial**, no máximo na primeira exposição. Exceção para obra evidentemente artística ou satírica |
| **NO FAKES Act** (EUA, federal) | **Projeto** — reintroduzido em 20/05/2026 | Criaria direito federal sobre réplicas digitais. **Quarta tentativa em cerca de três anos; nunca aprovado.** Não trate como lei |

E um caso estrangeiro que merece nota, por ser o inverso do vazio brasileiro:
**Arijit Singh v. Codible Ventures** (Índia, 2024) — tida como a primeira decisão
sobre síntese não autorizada de voz por IA generativa. Nos EUA, **Lehrman &
Sage v. Lovo** discute dubladores cujas gravações, licenciadas "para uso
interno", foram usadas além do escopo — **exatamente a hipótese de extrapolação
de finalidade** deste §3.

### O que existe de lei penal sobre IA (e que não se aplica a ela)

**Lei 15.123, de 24/04/2025** (conferida no Planalto) acrescentou parágrafo
único ao art. 147-B do Código Penal:

> "A pena é aumentada de metade se o crime é cometido mediante uso de
> inteligência artificial ou de qualquer outro recurso tecnológico que altere
> imagem ou som da vítima."

**Escopo estreito:** é aumento de pena no crime de **violência psicológica
contra a mulher**. Não é uma lei geral sobre imagem alterada por IA e nada tem
a ver com produção publicitária. Cito só para evitar que apareça em alguma
busca como se fosse "a lei brasileira de deepfake". Não é.

### E o Marco Legal da IA?

**Ainda não é lei.** Consultei a ficha de tramitação oficial da Câmara em
13/08/2026 e a situação do **PL 2338/2023** é literalmente:

> "Aguardando Parecer do(a) Relator(a) na Comissão Especial"

Aprovado no Senado em 10/12/2024, apresentado na Câmara em 17/03/2025,
despachado à Comissão Especial em 29/04/2025, regime de prioridade, sujeito à
apreciação do Plenário. **A votação de plenário anunciada para 27/05/2026 não
consta como realizada.** Isso fecha uma pendência que o documento 07 tinha
deixado em aberto: em agosto de 2026, **não há Marco Legal da IA em vigor no
Brasil**. Tudo que vale hoje é Constituição + Código Civil + LGPD + Lei de
Direitos Autorais.

---

## 3. A autorização antiga cobre alteração por IA?

### A resposta

**Não, na esmagadora maioria dos casos.** E o mais importante: **o cliente vai
achar que sim.** Essa distância entre o que ele acredita e o que o papel diz é
o risco número um do serviço de "expansão de plano" e "completar material
filmado".

### O raciocínio, em quatro passos

**Passo 1 — Interpretação restritiva é a regra, não a exceção.**
Lei 9.610/98, art. 4º: negócios sobre direitos autorais **interpretam-se
restritivamente**. Direito de imagem, sendo direito da personalidade
(irrenunciável, art. 11 do CC), recebe tratamento no mínimo tão restritivo. Na
dúvida, decide-se **contra** quem quer usar.

**Passo 2 — Cada modalidade de uso é independente.**
Este é o ponto técnico que fecha a questão, e ele está dito com todas as letras
no **Guia do produtor audiovisual da OAB-RJ** (Comissão de Direito Autoral,
Direitos Imateriais e Entretenimento):

> "Os negócios que envolvem direitos autorais são interpretados restritivamente,
> devendo os respectivos instrumentos contratuais regularem precisamente o
> acordo entre as partes, inclusive quanto à utilização da obra, tendo em vista
> que **as diversas modalidades de utilização são independentes entre si, não
> havendo abertura para presunções** no que concerne a cessão e licenciamento
> de direitos autorais e conexos."

"Não havendo abertura para presunções." Gerar uma performance nova por IA é uma
modalidade distinta de editar um material gravado. Se não está escrita, não está
presumida.

**Passo 3 — A lei veda cessão para modalidade que não existia.**
Lei 9.610/98, art. 49, V: *"a cessão só se operará para modalidades de
utilização já existentes à data do contrato."* Um contrato de 2019, 2021, até
2023 foi assinado num mundo em que gerar fala nova a partir do rosto de alguém
não era modalidade de uso disponível. O inciso VI reforça: sem especificação, o
contrato limita-se ao **indispensável à finalidade** dele.

**Passo 4 — A LGPD fecha por outro caminho.**
- Art. 6º, I (princípio da finalidade): tratamento para propósitos
  "específicos, explícitos e informados ao titular", **"sem possibilidade de
  tratamento posterior de forma incompatível com essas finalidades"**.
- Art. 8º, §4º: **"as autorizações genéricas para o tratamento de dados
  pessoais serão nulas."**
- Art. 9º, §2º: mudou a finalidade de forma incompatível com o consentimento
  original? O controlador **tem que informar antes**, e o titular pode revogar.

Gravar um depoimento para uma campanha e depois sintetizar falas novas com
aquele rosto é, no mínimo, finalidade nova. Provavelmente incompatível.

**Reforço de fato, não de direito:** os modelos de termo de autorização que
circulam no Brasil — inclusive os de universidades públicas e órgãos públicos —
**não têm cláusula de IA**. Se o padrão de mercado não tem, a chance de o
documento que o cliente guardou na gaveta ter é baixíssima.

### O contrato-padrão do mercado publicitário já responde a pergunta

Este é o achado mais prático da pesquisa, e ele dispensa discussão jurídica.

O **Manual de Produção do III Fórum da Produção Publicitária** (ABAP, APRO,
APROSOM, SIAESP, SINAPROSP) traz o *Contrato-Padrão de Concessão de Uso de
Imagem e/ou Som de Voz e/ou Nome do Ator ou Modelo* — cujo texto, segundo o
próprio manual, **não pode ser alterado**. É, com alta probabilidade, o contrato
que está por trás do material dos clientes dela. Cláusula IX, literal:

> "**9.1.** A CONTRATANTE fica autorizada a executar livremente a **montagem** do
> filme e das demais peças publicitárias referidas neste contrato, podendo
> realizar **cortes e reproduções** que sejam necessários, desde que não sejam
> prejudiciais à imagem do(a) CONTRATADO(A)/ANUENTE e que sejam utilizados
> **exclusivamente para os fins estabelecidos neste contrato**.
>
> **9.2.** Fica entendido que a presente autorização **não importa em qualquer
> cessão** de direitos de interpretação, de imagem, de som de voz ou de nome,
> **dependendo sempre de expressa anuência do(a) CONTRATADO(A)/ANUENTE qualquer
> utilização não prevista neste contrato**.
>
> **9.3.** Após o encerramento deste contrato ou de sua primeira renovação,
> **fica vedada à CONTRATANTE a veiculação do material produzido, a qualquer
> título ou pretexto** […] salvo com expressa autorização do(a)
> CONTRATADO(A)/ANUENTE."

**Leia os verbos do 9.1: montagem, cortes, reproduções.** São verbos de
**edição**. Nenhum é verbo de **geração**. Expandir plano, trocar cenário e criar
fala nova não estão ali.

E o **9.2 encerra o assunto por escrito**: qualquer utilização não prevista
**depende de expressa anuência**. Não é preciso invocar interpretação restritiva,
art. 49 nem LGPD — **o próprio contrato diz que o que não está previsto não está
autorizado.**

O 9.3 acrescenta o eixo do prazo: encerrado o contrato, a veiculação é **vedada**.

**Consequência para o dia a dia dela:** quando o cliente disser "temos o contrato
do ator", a pergunta certa não é "vocês têm?" — é **"o contrato prevê alteração
por IA?"**. Se for o padrão do setor, a resposta é não, e está escrito na
cláusula 9.2. Ela pode mostrar isso ao cliente sem parecer que está inventando
dificuldade.

Outras cláusulas do mesmo modelo, úteis para o eixo prazo/praça: a veiculação
vale pelo período fixado no quadro do contrato; a **renovação automática só vale
para contrato original de até 6 meses e uma única vez**; mídias e localidades
adicionais exigem **pagamento suplementar**; e os veículos "deverão ser descritos,
**um a um, de forma explícita**".

**Convergência internacional.** O documento 07 já registra o processo Rainbow
USA (jul/2026), em que se alega exatamente que a licença de talento não cobria
criar novas poses, figurino e composição por IA. E o padrão SAG-AFTRA exige
consentimento **separado, específico e por escrito** para réplica digital — se
bastasse o contrato de gravação, esse consentimento separado não existiria.
Não é lei no Brasil; é confirmação de que o mercado que mais lida com o
problema chegou à mesma conclusão.

### E se a autorização for genérica ou "por prazo indeterminado"?

Pergunta importante, e a resposta tem **duas metades diferentes** — é aqui que
muita gente erra ao generalizar.

**No eixo do direito de imagem: não é nula, é encolhida.** A tese que se repete
nas decisões é que autorização sem limite de duração **não vira autorização
perpétua**:

> "A autorização para uso de imagem concedida […] sem que tenha sido fixado um
> limite de duração, seja quantitativo, seja temporal, não autoriza o
> entendimento de que o uso da imagem seja permanente, **sob pena de
> considerá-la definitiva, vitalícia e geral, o que colide com a própria
> natureza personalíssima do direito**."

Ou seja: o juiz não rasga o documento — ele **reduz o alcance** ao prazo
razoável, à finalidade original e à praça contratada. E qualquer extrapolação
dos limites **objetivos** (onde veicula), **temporais** (por quanto tempo) ou
**subjetivos** (quem usa) gera dever de indenizar — com a Súmula 403 dispensando
prova de prejuízo.

**No eixo da LGPD: é nula, e ponto.** Art. 8º, §4º não deixa margem — "as
autorizações genéricas para o tratamento de dados pessoais **serão nulas**".

**Por que isso importa tanto para o caso dela.** Avatar e clone de voz caem nos
**dois eixos ao mesmo tempo**: são uso de imagem/voz *e* tratamento de dado
pessoal (provavelmente sensível). Então uma autorização genérica **não sustenta
o uso por IA em nenhum dos dois** — encolhe num, morre no outro. Não há
combinação em que ela sirva.

### O que precisa estar escrito

Uma autorização que realmente cobre produção com IA precisa responder, por
escrito e sem eufemismo, a **seis perguntas**:

| # | Pergunta | Por quê |
|---|---|---|
| 1 | **O quê** exatamente pode ser feito (inclusive gerar fala e cena novas) | Modalidade independente; sem isso, não está autorizado |
| 2 | **Para qual finalidade** — que campanha, que produto | Art. 6º, I da LGPD; finalidade específica |
| 3 | **Onde** (praça e mídia, com "mídia paga" dito com todas as letras) | Extrapolação de praça gera dever de indenizar |
| 4 | **Por quanto tempo**, com data de fim | Autorização sem prazo é o buraco clássico |
| 5 | **O que acontece com o modelo/avatar no fim** — apagar ou renovar | O avatar treinado é um ativo separado do vídeo |
| 6 | **Como a pessoa revoga**, e o que acontece se revogar | Art. 8º, §5º da LGPD; direito da personalidade |

### Uma cláusula real, publicada — e ela é de exclusão

Procurei cláusulas reais, não modelos genéricos. A mais completa que encontrei
**em português** vem da **GDA — Gestão dos Direitos dos Artistas** (entidade
portuguesa de gestão coletiva), no guia sobre IA de maio/2024. É uma cláusula de
**exclusão** — o artista proibindo o uso por IA — e serve como espelho: tudo que
ela proíbe é exatamente o que uma autorização precisa liberar expressamente.

> "As interpretações gravadas respeitantes ao presente contrato, bem como os
> direitos de personalidade do artista, incluindo sem limitação, a voz do
> artista, imagem, retrato ou qualquer outra característica […] **tal como
> ficaram ou com qualquer alteração posterior**, não podem ser reproduzidas,
> comunicadas ao público, publicadas, serem objeto de sampling e/ou utilizadas
> de qualquer forma para efeitos de **treino de tecnologias de inteligência
> artificial** para gerar imagens, vídeos e/ou sons, ou para avaliação e
> validação de modelos gerados por inteligência artificial […] incluindo mas não
> se limitando tecnologias capazes de **gerar interpretações no mesmo estilo ou
> género** que as interpretações gravadas […] bem como quaisquer outros
> desenvolvimentos tecnológicos que possam facilitar a **criação, modificação ou
> síntese** das interpretações gravadas pelo artista ou características,
> incluindo mas não se limitando a **geração de novas interpretações, imagens,
> vídeos e/ou sons sem intervenção humana**, do artista."

Repare na expressão **"tal como ficaram ou com qualquer alteração posterior"**.
É exatamente o gancho que fecha a brecha desta seção. Uma autorização séria
precisa do movimento inverso, e igualmente explícito.

O mesmo guia lista o que a autorização **afirmativa** precisa conter, e a lista
bate com a minha: formas de exploração visadas; **quem** pode usar (só o
produtor ou terceiros?); quais interpretações (atuais ou futuras); qual
característica (voz, imagem, retrato); **se vão ou não ser usadas para
aprendizagem de máquina**; duração, território e remuneração adequada. E
recomenda que a autorização para IA seja obtida **"em documento separado do
contrato original"** — a mesma conclusão a que a LGPD chega pelo art. 8º, §1º
("cláusula destacada") e a que a SAG-AFTRA chega pelo "separately signed rider".
**Três sistemas jurídicos diferentes, uma mesma recomendação: documento à
parte.**

### O contraexemplo brasileiro — como não fazer

O contrato do **BBB 26** virou caso público: autoriza a emissora a usar nome,
imagem e voz dos participantes "para alimentar sistemas de IA", **sem
remuneração específica e sem limitação de prazo ou território**, e — na análise
que li — aparece como **inciso de regulamento, sem destaque**.

É o retrato exato do que a LGPD fulmina: sem destaque (art. 8º, §1º) e com
finalidade indeterminada (art. 8º, §4º — **autorização genérica é nula**). Serve
como aviso: uma cláusula ampla demais não é uma cláusula forte — é uma cláusula
frágil, porque atrai nulidade.

### Redação sugerida

Duas cláusulas. A primeira é para **o termo assinado pela pessoa que aparece**.
A segunda é para **o contrato com o cliente** e está no §7.

> ⚠️ Texto de trabalho para levar a um advogado, não modelo pronto para assinar.
> Está redigido para ser **entendido pela pessoa que vai assinar** — o que, sob
> a LGPD, é requisito de validade, não estilo (art. 9º, §1º: consentimento é
> nulo se a informação não foi apresentada "de forma clara e inequívoca").

**Cláusula de autorização para uso por inteligência artificial**
*(cláusula destacada, em campo separado, com assinatura ou aceite próprio —
LGPD, art. 8º, §1º e art. 11, I)*

> **AUTORIZAÇÃO ESPECÍFICA PARA USO DE IMAGEM E VOZ POR INTELIGÊNCIA ARTIFICIAL**
>
> Eu, [nome], [qualificação], autorizo de forma **específica, destacada e
> informada** que minha imagem, minha voz e minhas características faciais e
> vocais sejam usadas para as finalidades descritas abaixo, com uso de
> ferramentas de inteligência artificial, nos exatos limites aqui definidos.
>
> **1. O que estou autorizando.** Entendo e autorizo que, a partir do material
> gravado comigo, sejam usadas ferramentas de inteligência artificial para:
> *(marcar apenas o que se aplica)*
> ( ) alterar o cenário, o enquadramento ou a extensão das cenas em que eu
> apareço;
> ( ) **criar imagens minhas em situações, poses, cenários ou figurinos que eu
> não gravei**;
> ( ) **criar falas minhas que eu não pronunciei**, por síntese ou clonagem da
> minha voz;
> ( ) criar e usar um **avatar digital** com a minha aparência;
> ( ) gerar versões do material com a minha voz em outros idiomas.
>
> **2. Para quê.** Esta autorização vale exclusivamente para: [campanha /
> projeto / peça], do anunciante [marca]. **Não** vale para nenhuma outra
> campanha, produto ou anunciante, nem para treinar modelos de inteligência
> artificial para finalidades diferentes desta.
>
> **3. Onde.** O material poderá ser veiculado em: [listar mídias e
> territórios]. ( ) Inclui mídia paga / impulsionamento. ( ) Não inclui.
>
> **4. Por quanto tempo.** De [data] até **[data de término]**. Vencido o prazo,
> a veiculação cessa. Prorrogação depende de nova autorização minha, por
> escrito.
>
> **5. O que acontece no fim.** Encerrado o prazo, o avatar digital, o modelo de
> voz e os arquivos técnicos derivados da minha imagem e da minha voz serão
> **eliminados**, e me será confirmada a eliminação, salvo se eu autorizar por
> escrito a manutenção.
>
> **6. Se eu mudar de ideia.** Posso revogar esta autorização a qualquer momento,
> por escrito, de forma gratuita e sem precisar justificar. A revogação vale
> daqui para frente: o material já veiculado até a data da revogação fica
> ratificado, e a retirada do que estiver no ar será feita em até [X] dias.
>
> **7. Remuneração.** ( ) Sem remuneração específica. ( ) Mediante o valor de
> [R$ ...], pago em [condições].
>
> **8. Contato.** Para exercer qualquer direito relativo a esta autorização:
> [nome, e-mail].
>
> Local, data e assinatura.

Três observações sobre esse texto:

- **Os checkboxes não são enfeite.** Consentimento específico significa que a
  pessoa autoriza *aquilo*, não "uso de IA" em bloco. Uma pessoa pode aceitar
  expansão de cenário e recusar fala sintética — e isso é legítimo.
- **O item 5 é o mais esquecido do mercado.** O vídeo publicado e o modelo
  treinado são coisas diferentes. Sem cláusula de eliminação, o avatar
  sobrevive ao contrato.
- **O item 6 não é generosidade.** Direito da personalidade é irrenunciável
  (CC, art. 11); cláusula que proíbe revogar tende a não valer. Melhor
  disciplinar a revogação (prazo para retirar do ar) do que fingir que ela não
  existe.

---

## 4. LGPD e dado sensível

### Face e voz são dado pessoal sensível? Depende — e o "depende" importa

**O que a lei diz, literalmente** (art. 5º):

> "I - **dado pessoal**: informação relacionada a pessoa natural identificada ou
> identificável;
> II - **dado pessoal sensível**: dado pessoal sobre origem racial ou étnica,
> convicção religiosa, opinião política, filiação a sindicato ou a organização
> de caráter religioso, filosófico ou político, dado referente à saúde ou à vida
> sexual, **dado genético ou biométrico, quando vinculado a uma pessoa
> natural**"

Repare no que **não** está lá: a LGPD **não define** o que é "dado biométrico".
Diz que é sensível e para por aí.

**E a ANPD também não define — isso foi confirmado, não presumido.** Varri o
portal da ANPD. A autoridade mantém um **Glossário de Proteção de Dados Pessoais
e da Privacidade** cuja finalidade declarada é "sistematizar os principais
conceitos" da área, publicado em 23/05/2024 e **atualizado em 08/07/2026** — ou
seja, corrente. Nele:

- **não há verbete "dado biométrico"**;
- **não há verbete "biometria"**, "reconhecimento facial" nem "inteligência
  artificial";
- a única aparição da palavra "biométrico" no glossário inteiro está **dentro da
  transcrição literal do art. 5º, II da LGPD**, no verbete "Dado Pessoal
  Sensível".

A lista oficial de guias orientativos da ANPD confirma o mesmo vazio: há guias
sobre encarregado, legítimo interesse, poder público, cookies, pesquisa
acadêmica, segurança para pequeno porte, agentes de tratamento e contexto
eleitoral. **Não há guia sobre biometria, reconhecimento facial ou IA.**

Isso muda o status da questão: **não é uma lacuna da minha pesquisa, é uma
lacuna regulatória.** Em agosto de 2026, quem precisa decidir se um rosto
filmado é dado sensível **não tem resposta oficial da autoridade brasileira** —
e vai ter que decidir com base no texto da lei, na comparação com o GDPR e na
doutrina. É exatamente o que este documento faz abaixo, e é por isso que a
recomendação prática é adotar a hipótese conservadora onde o risco se concentra.

**Por que a simplificação circula tanto.** Muito material de mercado — inclusive
o documento 07 deste conjunto de pesquisas — afirma direto que "voz e traços
faciais são dados biométricos, categoria sensível". É uma simplificação. O
artigo do Migalhas usado como fonte lá diz algo mais contido: que imagem e voz,
"quando utilizadas para identificá-lo ou para inferir suas características,
constituem **dados pessoais**".

**A leitura mais defensável.** O GDPR europeu, que serviu de modelo para a
LGPD, define biométrico com um qualificador que a LGPD deixou de fora (art.
4(14)):

> "personal data resulting from **specific technical processing** relating to
> the physical, physiological or behavioural characteristics of a natural
> person, **which allow or confirm the unique identification** of that natural
> person, such as facial images or dactyloscopic data"

Traduzindo o critério: não é a foto que é biométrica — é o **processamento
técnico específico** que extrai daquela foto uma representação capaz de
identificar unicamente a pessoa. Filmar o rosto de alguém gera dado pessoal.
Extrair um modelo daquele rosto gera dado biométrico.

**Aplicado ao trabalho dela — e é aqui que a distinção deixa de ser acadêmica:**

| O que ela faz | Provável enquadramento | Regime |
|---|---|---|
| Filma uma pessoa; edita, corta, colore | Dado pessoal **comum** | Art. 7º — bases mais flexíveis |
| Expande o plano, troca o cenário, sem tocar em rosto ou voz | Dado pessoal **comum** | Art. 7º |
| **Cria avatar digital a partir do rosto de alguém** | Dado **biométrico → sensível** | **Art. 11** |
| **Clona a voz de alguém** | Dado **biométrico → sensível** | **Art. 11** |
| **Sintetiza falas novas com o rosto da pessoa** | Dado **biométrico → sensível** | **Art. 11** |

Criar avatar e clonar voz **são**, por definição, "processamento técnico
específico" das características físicas de alguém. É difícil sustentar que não
sejam biométricos. **Então o serviço "Produção com IA" é precisamente a
atividade dela que cai no regime mais pesado da LGPD** — enquanto filmagem
comum não cai.

Uma nota de cautela na direção contrária: como a LGPD **omitiu** o qualificador
do GDPR, há leitura de que no Brasil qualquer foto ou vídeo de rosto já seria
biométrico. Se essa leitura prevalecer, o regime severo alcança também a
filmagem comum e o portfólio. Para decidir, vale trabalhar com a hipótese mais
conservadora nos casos de avatar e clone — que é onde o risco se concentra de
qualquer forma.

### O segundo caminho: imagem e áudio que *revelam* dado sensível

Há uma via de entrada no art. 11 que não passa por biometria nenhuma, e é a
ANPD quem a usa. No caso Meta (tratamento de dados de usuários para treinar IA
generativa), a autoridade registrou:

> "o tratamento indiscriminado de fotografias, imagens, vídeos e gravações de
> áudios, especialmente por meio do uso de sistemas de inteligência artificial,
> **pode revelar vinculações políticas, religiosas, sindicais e sexuais dos
> titulares, que já se caracterizam, de imediato, como dados pessoais
> sensíveis**, conforme definição do art. 5º, inciso II, da LGPD."

Repare no raciocínio: não é "o rosto é biométrico" — é "**o conteúdo da imagem
revela** categoria sensível". Um vídeo pode mostrar a pessoa numa igreja, num
ato sindical, num evento político. Isso reforça o art. 11, §1º da própria LGPD,
que estende o regime "a qualquer tratamento de dados pessoais que **revele**
dados pessoais sensíveis e que possa causar dano ao titular".

**É um segundo caminho, independente do primeiro.** Para o caso dela, importa
menos no avatar (onde a via biométrica já resolve) e mais no **portfólio**, onde
um único vídeo de conteúdo religioso, político ou sindical muda o regime
daquela peça — e derruba o legítimo interesse como base (§6).

### O que a ANPD já decidiu sobre IA generativa

Dois pontos confirmados em documento oficial, e os dois são úteis.

**1. Legítimo interesse não serve para dado sensível — dito pela ANPD, não só
pela doutrina.** No Voto nº 23/2024 do Conselho Diretor (caso Meta), item 4.54:

> "Em primeiro lugar, é importante reforçar que **a hipótese legal do legítimo
> interesse não se aplica ao tratamento de dados pessoais sensíveis**, conforme
> estabelecido pela LGPD […]"

O mesmo voto avisa que a decisão **não** legitima o uso de legítimo interesse
para treinar IA em geral (itens 4.17 e 4.60). E o processo principal do caso
Meta (nº 00261.004509/2024-36) **segue em andamento, sem decisão final e sem
sanção**, quase dois anos depois. Quem disser que "a ANPD liberou" está errado.

**2. A ANPD já disse que o titular não espera que material antigo vire treino de
IA.** Voto nº 11/2024, item 4.28 — e esta frase é diretamente transportável para
o §3 deste documento:

> "…é razoável supor que, a princípio, **não há a expectativa de que *todas*
> essas informações, inclusive as compartilhadas muitos anos atrás, sejam
> utilizadas para treinar sistemas de IA, que sequer estavam implementados
> quando as informações foram compartilhadas**."

É o argumento da "modalidade que não existia à data do contrato" (§3, passo 3),
dito pela autoridade brasileira de proteção de dados, com todas as letras. **Se
alguém questionar a tese central deste documento, esta é a citação a mostrar.**

O mesmo voto (item 4.56) antecipou o risco de deepfake: "há, ainda, o risco de
produção de conteúdos sintéticos com base nos dados pessoais tratados, a exemplo
de deepfakes, que podem expor e atingir negativamente a reputação dos titulares".

### O regime do art. 11 — o que muda

Texto literal do que interessa:

> "Art. 11. O tratamento de dados pessoais sensíveis somente poderá ocorrer nas
> seguintes hipóteses:
> I - quando o titular ou seu responsável legal consentir, de forma
> **específica e destacada**, para **finalidades específicas**;"

O art. 11 tem uma lista **fechada** e bem mais curta que a do art. 7º. E o que
some dela é justamente o que o mercado mais usa:

- **Não existe "legítimo interesse" para dado sensível.** O art. 7º, IX,
  permite; o art. 11 não repete. Some a base mais confortável.
- **Não existe "execução de contrato".** O art. 7º, V, permite; o art. 11 não
  tem equivalente. Ou seja: **"está no contrato da campanha" não é base legal
  para criar um avatar de alguém.**

Na prática, para avatar e clone de voz sobra **uma** base viável: consentimento
específico e destacado do titular. As outras hipóteses do art. 11, II
(obrigação legal, política pública, pesquisa, exercício de direito em processo,
proteção da vida, tutela da saúde, prevenção à fraude) não descrevem produção
publicitária.

**"Específico e destacado" traduzido:**

- **Específico** = para *esta* finalidade. Reforçado pelo art. 8º, §4º
  (autorização genérica é **nula**).
- **Destacado** = art. 8º, §1º — "cláusula destacada das demais cláusulas
  contratuais". Não pode estar escondido no meio de um contrato de prestação de
  serviço ou num parágrafo de termo de uso. Campo separado, visível, com aceite
  próprio.
- **Provável** = art. 8º, §2º: **"Cabe ao controlador o ônus da prova de que o
  consentimento foi obtido em conformidade."** Quem tem que provar é quem usou.
  Guardar o documento é parte do dever, não zelo extra.

**A ANPD explicou o que "destacada" significa na prática.** A orientação está num
lugar inesperado — o guia sobre cookies (v1.0, out/2022) — mas o trecho é geral e
trata expressamente de dado sensível:

> "No caso de coleta de dados sensíveis com base no consentimento […] é
> necessário que, adicionalmente, o consentimento seja obtido por **forma
> específica e destacada**, conforme preconiza o art. 11, I, da LGPD. Em relação
> à forma destacada, recomenda-se que a autorização […] conste **separadamente
> do texto principal** ou, ainda, que se usem recursos para evidenciá-lo, de modo
> a **indicar quais dados sensíveis serão coletados e para qual finalidade
> específica** serão utilizados."

E, no mesmo guia, duas frases que valem para qualquer termo de autorização:

> "**Qualquer alteração das premissas adotadas para a obtenção do consentimento
> macula a hipótese legal adotada, exigindo novo consentimento** pelo titular de
> dados, ou a utilização de outra hipótese legal…"

> "o consentimento deve ser inequívoco, o que demanda […] uma manifestação de
> vontade clara e positiva do titular, **não se admitindo a sua inferência ou a
> obtenção de forma tácita ou a partir de uma omissão**."

**Traduzindo para o termo do §3:** documento separado (ou campo claramente
apartado), dizendo **quais** características serão usadas e **para qual
finalidade**, com marcação ativa da pessoa — nada de checkbox pré-marcado, nada
de "quem não se manifestar concorda". E se a finalidade mudar no meio do
caminho, **precisa de consentimento novo** — não serve "avisar depois".

**Convergência prática:** é exatamente o que as ferramentas já exigem. O
documento 07 registra que o HeyGen pede **vídeo de consentimento gravado pela
própria pessoa**, lendo uma declaração. Isso não é capricho do fornecedor — é a
forma de produzir prova de consentimento específico e destacado. A exigência
comercial e a exigência legal apontam para o mesmo lugar.

### Sanções

Art. 52: advertência; **multa de até 2% do faturamento no Brasil, limitada a
R$ 50 milhões por infração**; multa diária; publicização da infração; bloqueio
e **eliminação dos dados**; suspensão do banco de dados ou da atividade de
tratamento por até 6 meses; proibição parcial ou total de tratar dados.

Para uma profissional autônoma, os itens que doem não são só os financeiros:
**eliminação dos dados** e **publicização da infração** atingem o acervo e a
reputação — que são o ativo dela.

---

## 5. Controlador ou operador — de quem é a responsabilidade

**Esta é a seção mais importante do documento.**

### O critério

As definições, literais (LGPD, art. 5º):

> "VI - **controlador**: pessoa natural ou jurídica, de direito público ou
> privado, a quem competem **as decisões referentes ao tratamento** de dados
> pessoais;
> VII - **operador**: pessoa natural ou jurídica, de direito público ou privado,
> que realiza o tratamento de dados pessoais **em nome do controlador**"

O critério é **quem decide**, não quem executa. Reforçado pelo art. 39: *"O
operador deverá realizar o tratamento segundo as instruções fornecidas pelo
controlador."*

**A ANPD tem um guia sobre isso e ele responde ao caso dela de forma quase
literal.** O *Guia Orientativo para Definições dos Agentes de Tratamento de
Dados Pessoais e do Encarregado*, **versão 2.0 (abril/2022)**, item 9 — e repare
que o item trata **especificamente de pessoa natural**, que é exatamente a
situação de uma autônoma:

> "**pessoas naturais podem ser consideradas controladoras ou operadoras** de
> dados pessoais. Serão **controladoras quando atuarem de acordo com os próprios
> interesses, com poder de decisão sobre as finalidades e os elementos
> essenciais de tratamento**. Serão **operadoras quando atuarem de acordo com os
> interesses do controlador, sendo-lhes facultada apenas a definição de
> elementos não essenciais à finalidade do tratamento**. O operador deve ser uma
> entidade distinta do controlador, isto é, que não atua como profissional
> subordinado a este ou como membro de seus órgãos."

O critério fica preciso: **elementos essenciais** (finalidade, quais dados, por
quanto tempo, com quem compartilhar) → controlador. **Elementos não essenciais**
(qual software, qual método técnico, desde que a finalidade não mude) →
operador.

E o item 8 confirma que o papel **não é um rótulo fixo da pessoa**:

> "o agente de tratamento é definido **para cada operação de tratamento** de
> dados pessoais, portanto, **a mesma organização poderá ser controladora e
> operadora**, de acordo com sua atuação em diferentes operações de tratamento."

É a base oficial da tabela abaixo: ela muda de papel conforme a atividade, e
isso é o normal, não uma anomalia.

**Controladoria conjunta.** A LGPD não a define; o guia da ANPD a infere do
sistema (itens 40 a 44), buscando referência no art. 26 do RGPD e no EDPB:
ocorre quando há "participação conjunta" na determinação de "finalidades e
meios", por decisões **comuns ou convergentes**. Se as finalidades apenas se
complementam — uma serve à outra — a relação é controlador/operador.

> **Nota de peso das fontes:** o guia é expressamente **não vinculante** — a
> própria ANPD o descreve como "diretrizes não-vinculantes aos agentes de
> tratamento". Vale como interpretação oficial e boa defesa, não como norma.

### Aplicado ao caso concreto dela

A resposta não é única. **Ela muda de papel dependendo da atividade** — e é
isso que quase todo material de mercado erra ao responder "agência é operadora"
como se fosse regra geral.

| Atividade | Quem decide a finalidade | Papel dela |
|---|---|---|
| Produzir avatar da funcionária de uma marca, a pedido da marca | A marca (quer o vídeo, escolhe a pessoa, aprova o roteiro) | **Operadora** |
| Escolher qual ferramenta de IA usar, e com isso decidir se o dado vai para treino de terceiro | **Ela** | **Controladora** desse recorte, ou controladora conjunta |
| Guardar o material bruto e o modelo do avatar depois de entregue o projeto | **Ela**, se decidiu guardar por conta própria | **Controladora** |
| Exibir o trabalho no portfólio dela para captar cliente | **Ela**, por interesse próprio | **Controladora** (§6) |

**A regra geral: na produção contratada, ela é operadora.** A marca é
controladora. Isso é bom para ela.


**Antes dos furos, a boa notícia oficial.** O guia da ANPD (v2.0, item 60) diz
que a equiparação do operador ao controlador é **excepcional**, não a regra:

> "a responsabilidade solidária estabelecida pelo inciso I, § 1º do art. 42 da
> LGPD, prevista para os casos de danos causados em razão do tratamento
> irregular realizado por operador (por descumprir as obrigações da legislação
> ou por não observar as instruções do controlador), pode ser considerada como
> uma **excepcionalidade**, já que **em regra a responsabilidade é do
> controlador**. A princípio, essa é a única hipótese em que o operador é
> equiparado ao controlador."

Ou seja: enquanto ela **seguir instrução lícita e cumprir a lei**, a
responsabilidade é do cliente. O item 59 lembra a única obrigação que os dois
partilham sempre — **manter registro das operações de tratamento** (art. 37).
Isso reforça o conselho do §7: guardar briefing e termos não é zelo, é dever
legal dela mesmo como operadora.

Dito isso, há três furos — e todos são evitáveis.

**Furo 1 — o operador que erra vira controlador.** Art. 42, §1º, I, literal:

> "o operador responde **solidariamente** pelos danos causados pelo tratamento
> quando **descumprir as obrigações da legislação de proteção de dados** ou
> **quando não tiver seguido as instruções lícitas do controlador**, hipótese em
> que **o operador equipara-se ao controlador**"

Duas portas de entrada. A segunda é óbvia (fez diferente do combinado). **A
primeira é a perigosa: basta descumprir a lei.** Produzir um avatar sem
consentimento específico é descumprir a lei — mesmo que o cliente tenha mandado.
"O cliente pediu" não é, por si, salvo-conduto.

Repare também na palavra **"lícitas"**. Instrução ilícita não protege ninguém.
Se o cliente manda clonar a voz de alguém que não autorizou, cumprir a ordem
não a blinda: ela executou tratamento ilícito.

**Furo 2 — escolher a ferramenta é decidir os meios.** Quando ela decide subir
material numa plataforma cujos termos mandam o conteúdo para treino do modelo
(o documento 07 registra isso na Runway fora do Enterprise), essa decisão é
dela. É decisão sobre **meios essenciais** e sobre uma **nova finalidade**
(treinar modelo de terceiro) que o cliente pode nem conhecer. Aí ela deixa de
ser mera executora.

**Furo 3 — o direito de imagem não liga para LGPD.** Aqui está a armadilha
maior. A conversa controlador/operador resolve a **responsabilidade
administrativa perante a ANPD**. Não resolve a **ação de indenização por dano
moral** movida pela pessoa que apareceu no vídeo. Essa corre por outro trilho:
Constituição, art. 5º, X; Código Civil, arts. 20, 186 e 927; Súmula 403.

Nesse trilho, **quem produziu e quem veiculou podem ser acionados juntos**, e
a pessoa lesada escolhe contra quem litigar. Ser operadora sob a LGPD não é
defesa numa ação de direito de imagem. Foi exatamente o que se viu no caso do
TJSP: o tribunal disse que se vai apurar **"quem foi contratado para produzi-la,
se houve algum tipo de verificação prévia."**

### As consequências práticas

**1. O escudo dela não é o rótulo "operadora". É o par instrução + verificação.**
Duas coisas, por escrito:
- **instrução documentada do cliente** (o que ele pediu, com o que ele declarou
  ter); e
- **verificação prévia documentada** (o que ela perguntou e o que ele respondeu).

O briefing preenchido **é** a verificação prévia. Guardado com data, ele é a
resposta pronta à pergunta que o TJSP disse que seria feita.

**2. Instrução ilícita tem que ser recusada, não executada.** Se o cliente
responde no briefing "não teve autorização assinada" e mesmo assim pede o
avatar, executar é o cenário do art. 42, §1º, I. Essa é a hora de parar — e a
resposta certa é oferecer o caminho (termo de autorização) em vez de tocar o
projeto. O documento 07 já prevê isso na microcopy ("eu já trabalho com um
modelo e te mando"): comercialmente é gentileza, juridicamente é proteção.

**3. Vale um contrato de operador.** Uma cláusula curta no contrato de
prestação registrando que ela atua **como operadora**, segundo instruções do
cliente, e que o cliente é o controlador. Não muda a realidade sozinha (o papel
decorre dos fatos, não do rótulo), mas alinha as expectativas e serve de prova
de quem decidia o quê.

**4. O regresso é o que sobra quando tudo dá errado.** Art. 42, §4º da LGPD:
*"Aquele que reparar o dano ao titular tem direito de regresso contra os demais
responsáveis, na medida de sua participação no evento danoso."* E Código Civil,
art. 934, na mesma linha. Se ela for acionada e pagar por falha de autorização
que era do cliente, pode cobrar dele. **Mas só na prática se houver cláusula e
prova de quem declarou o quê** — daí o §7.

**5. Não se blinda contra tudo.** Se ela mesma foi negligente — não perguntou,
não guardou, usou material que sabia ser problemático — nenhuma cláusula
resolve. O art. 43 só exclui responsabilidade em três hipóteses: não realizou o
tratamento, realizou mas sem violar a lei, ou o dano decorreu de culpa
exclusiva do titular ou de terceiro. A cláusula de regresso protege no cenário
"terceiro"; não protege no cenário "eu não perguntei".

---

## 6. O portfólio

### O que está no ar hoje

Levantei no próprio catálogo do site (`client_videos.json`):

| | |
|---|---|
| Vídeos publicados | **534** |
| Marcas | **46** |
| Registros cujo campo `talento` traz **nome próprio de pessoa** | **78** |

Os maiores blocos são Soldiers Nutrition (100), Raia (64), Drogasil (50),
Mercado Pago (48) e Magazine Luiza (37).

**Esses 78 nomes são o achado desta seção.** Não é só "vídeo com pessoa em
cena": é **nome próprio publicado ao lado do rosto**, num site público, com
finalidade comercial. Sob a LGPD isso é pessoa "identificada", não meramente
identificável — e o tratamento é dela, decidido por ela, para benefício dela.
**No portfólio ela é controladora**, com todos os deveres que isso traz:
finalidade, transparência, atendimento a pedido do titular, ônus da prova.

### A base legal para manter no ar

Avaliei quatro caminhos. Nenhum é confortável sozinho; combinados, dão um
terreno defensável.

**(a) A exceção de "fins artísticos" — não conte com ela.**
Art. 4º, II, "a": a LGPD não se aplica a tratamento "realizado para fins
**exclusivamente** jornalístico e artísticos". A palavra é *exclusivamente*. Um
portfólio existe para **vender serviço** — é finalidade comercial, ainda que o
conteúdo seja artístico. Na minha leitura essa exceção **não cobre** o
portfólio. Registro porque ela vai aparecer em qualquer busca sobre o tema, e é
uma pista falsa.

**(b) "Dados tornados manifestamente públicos pelo titular" — não se encaixa.**
Art. 7º, §4º dispensa consentimento "para os dados tornados manifestamente
públicos **pelo titular**". No caso dela, quem tornou público foi **a marca**,
não a pessoa filmada. O texto é específico quanto a quem publica. Além disso, o
§3º manda considerar "a finalidade, a boa-fé e o interesse público que
justificaram sua disponibilização" — a finalidade original era a campanha da
marca, não a captação de clientes da produtora. **Base fraca.**

Duas ressalvas que salvam parte dela: **(i)** onde o **creator repostou a peça no
próprio perfil**, aí sim foi o titular quem tornou público, e o §4º passa a ser
argumentável — isso é comum com creator, raro com funcionário de cliente e
figurante; **(ii)** mesmo quando se aplica, o §6º mantém **todos** os deveres e
**todos** os direitos do titular, inclusive o de pedir remoção. O §4º nunca é
escudo contra pedido de retirada. Serve como argumento **acessório e caso a
caso** — não sustenta um acervo de 534 vídeos.

**(c) Legítimo interesse (art. 7º, IX + art. 10) — a base mais viável.**
Art. 10, I admite expressamente "**apoio e promoção de atividades do
controlador**". Divulgar o próprio trabalho é literalmente promoção de
atividade — a hipótese está no texto da lei, não em analogia. Mas o art. 10
impõe condições: só os dados **estritamente necessários** (§1º), transparência
(§2º), e respeito às "legítimas expectativas" do titular.

Aplicando com honestidade: exibir o **vídeo** que já está público no canal da
marca cabe bem na expectativa legítima de quem participou de uma campanha
publicitária. **Publicar o nome próprio da pessoa junto**, num site que não é o
da marca, é mais difícil de justificar como "estritamente necessário" — o nome
do talento não é necessário para demonstrar a competência técnica dela.

**A ANPD tem guia sobre isso, e ele impõe uma condição que muda tudo.** O *Guia
Orientativo — Legítimo Interesse* (fev/2024) exige, entre os elementos da
legítima expectativa, que o titular tenha "**a possibilidade efetiva de se opor**
ao tratamento".

Traduzindo: legítimo interesse **não é um argumento que se usa em juízo depois**.
É um documento escrito **antes** (o teste de balanceamento, ou LIA), mais
transparência no site, mais um canal de oposição que funcione de verdade. **Sem
o canal de remoção, a base desmonta sozinha** — porque a própria base pressupõe
que a oposição seja possível.

E há um limite duro, dito pela própria ANPD (Voto 23/2024, item 4.54): **"a
hipótese legal do legítimo interesse não se aplica ao tratamento de dados
pessoais sensíveis"**. Se o material envolve avatar, voz clonada, ou conteúdo
que revele filiação religiosa, política ou sindical (§4), essa base **não está
disponível** — só consentimento. Na prática: esses vídeos precisam sair do
portfólio ou ganhar autorização própria.

**(d) A autorização original da campanha — depende, e provavelmente não cobre.**
Mesmo raciocínio do §3: interpretação restritiva, modalidades independentes. Uma
autorização para "veiculação da campanha X nas mídias da marca Y" não menciona
"exibição no portfólio do fornecedor". São **três desvios**, e cada um bastaria
sozinho:

1. **Agente diferente** — autorizou-se a marca (ou a agência), não a produtora.
2. **Finalidade diferente** — campanha publicitária ≠ material de captação
   comercial de uma prestadora.
3. **Prazo diferente** — campanha tem prazo de veiculação; portfólio é perpétuo.

Agravante prático: em publicidade, o contrato de elenco costuma ser **da agência
ou do anunciante com o talento**. A produtora frequentemente **não é parte e não
tem cópia do termo** — ou seja, ela não teria como provar o escopo da
autorização de 534 vídeos, mesmo querendo.

### O que a jurisprudência diz — e ela é específica

Três decisões mudam a análise. As duas primeiras são do STJ.

**"Já está público" não é licença — STJ, REsp 1.822.619** (3ª Turma, rel. Min.
Nancy Andrighi):

> "O fato de a fotografia estar acessível mediante pesquisa em mecanismo de busca
> disponibilizado na internet **não priva seu autor dos direitos** assegurados
> pela legislação de regência, tampouco autoriza a presunção de que ela esteja
> em domínio público"

Foi dito sobre direito autoral, mas a lógica — **disponibilidade não é
autorização** — transporta-se com facilidade para imagem. **É o precedente que
derruba diretamente a tese mais confortável dela.**

**A régua que salva — STJ, REsp 1.772.593** (3ª Turma, rel. Min. Nancy Andrighi,
16/06/2020). Torcedor filmado em estádio teve a imagem usada em campanha
publicitária de automóvel, sem autorização expressa. **Não houve dano moral**,
porque a imagem aparecia "no contexto da torcida, com várias outras pessoas",
**sem destaque individual**.

A régua é precisa e ela pode aplicar sozinha: **destaque individual é o divisor
de águas.** Um creator em close falando à câmera está no lado ruim da régua. Uma
pessoa ao fundo, não identificável, está no lado bom. Vale a pena passar o
acervo por essa lente — e os 78 nomes próprios estão, por definição, no lado
ruim, porque nomear alguém é o oposto de não destacar.

**O caso estruturalmente mais parecido — TJDFT, 5º Juizado Especial Cível de
Brasília, proc. 0708200-37.2020.8.07.0016.** Casa noturna publicou foto de uma
cliente no Instagram do próprio estabelecimento, sem consentimento. Resultado:
**remoção em 5 dias + R$ 3.000 de dano moral**, com base no art. 5º, V e X da CF
e art. 20 do CC. Fundamento decisivo: *"por se tratar de publicação com
finalidade de lucro, o pedido merece prosperar."*

É exatamente a estrutura do portfólio: **empresa publica imagem de pessoa em
canal próprio, para promover o próprio negócio.** Guarde a ordem de grandeza:
**R$ 3.000 por pessoa.** Baixo individualmente — relevante se escalar.

**E o que não existe:** não foi localizada **nenhuma decisão brasileira em que
fotógrafo ou produtora tenha sido processado por exibir trabalho de cliente em
portfólio.** Procuramos por várias formulações. Isso é informação útil: é um
risco reconhecido pela doutrina e pela prática contratual, mas com
**litigiosidade praticamente nula**. O cenário realista não é ação judicial — é
**notificação extrajudicial**, vinda de um creator que brigou com a marca, de um
funcionário demitido, ou do jurídico de um cliente. O custo real é remoção
urgente e desgaste, não condenação.

**Conclusão desta parte, sem enfeite.** O portfólio se sustenta hoje em
**legítimo interesse + material já publicado pelo cliente + ausência de destaque
individual na maior parte do acervo + baixo atrito real**. É uma posição
**razoável, não blindada**. Os dois elos fracos são a **exibição de nomes
próprios** e a inexistência de autorização escrita para uso em portfólio.

### Se a pessoa pedir remoção

**Resposta curta: tire do ar.** Discutir o direito dela é caro, lento e ruim de
reputação, e a chance de ganhar é baixa. Fundamentos que a pessoa tem:

- **Código Civil, art. 12**: pode exigir que **cesse** a lesão a direito da
  personalidade. Direito da personalidade é irrenunciável (art. 11) — o que
  torna a autorização de imagem, na leitura predominante, **revogável**.
- **LGPD, art. 18, IV**: eliminação de dados tratados em desconformidade;
  **art. 18, IX**: revogação do consentimento; **art. 18, §2º**: **direito de
  oposição** a tratamento feito com dispensa de consentimento — exatamente o
  caso de quem se apoia em legítimo interesse.
- **Art. 8º, §5º**: revogação a qualquer momento, "por procedimento **gratuito
  e facilitado**", ficando **ratificados os tratamentos já realizados**.

Esse último ponto é a boa notícia: **a revogação vale daqui pra frente.** Tirar
do ar quando pedirem não implica indenizar retroativamente pelo período em que
o material estava autorizado. O risco só vira caro se ela **resistir** ao
pedido — aí a exibição passa a ser não autorizada e a Súmula 403 volta a
morder.

Três notas técnicas que valem a pena:

- **Oposição tem um detalhe brasileiro.** O art. 18, §2º condiciona a oposição a
  "descumprimento ao disposto nesta Lei" — texto mais estreito que o europeu. Na
  prática vale pouco: como o guia da ANPD exige "possibilidade efetiva de se
  opor" para o legítimo interesse ser válido, **negar a oposição tende a criar
  justamente o descumprimento que a autoriza**. O círculo fecha contra quem
  resiste.
- **A revogabilidade não é ponto pacífico — é ponto latente.** A doutrina
  sustenta que a autorização é revogável, por ser direito da personalidade
  irrenunciável (CC, art. 11), e que **cláusula de renúncia ao direito de
  revogar é inválida**. Só que os contratos-padrão do setor usam
  sistematicamente "irrevogável e irretratável" (ver as cláusulas APRO abaixo).
  Ou seja: o mercado tenta blindar contratualmente algo que a doutrina diz não
  ser blindável. **Não localizamos acórdão do STJ decidindo expressamente a
  revogação de autorização de uso de imagem.** Trate como questão aberta.
- **Ela não tem direito a ser indenizada por quem revoga.** Procuramos e **não
  achamos fundamento no direito brasileiro** para isso. O modelo português
  prevê indenizar as expectativas do cessionário; o direito brasileiro **não tem
  dispositivo equivalente** — não importe o raciocínio de lá. Aliás, o único
  dispositivo próximo aponta ao contrário: a Lei 9.610/98, art. 24, §3º, manda
  que **o autor** indenize terceiros quando retira a obra de circulação.
  Conclusão prática: discutir a revogação é perder tempo e piorar a posição.

**O que fazer, concretamente:**
1. Ter **um canal visível** para pedir remoção (um e-mail no rodapé do site já
   resolve). O art. 8º, §5º pede procedimento "facilitado", e o art. 18, §5º diz
   que o atendimento é **sem custo** para o titular.
2. **Atender rápido e sem discussão**, e responder por escrito confirmando.
3. **Registrar** o pedido e o atendimento (prova de conformidade — art. 6º, X,
   responsabilização e prestação de contas).
4. Se o pedido chegar via cliente, atender igual.

### Material já publicado vs. inédito

Distinção prática, de risco muito diferente:

| Tipo | Risco | Recomendação |
|---|---|---|
| Peça **já veiculada** pelo cliente | Menor. Já é público, a pessoa sabe que foi ao ar, a expectativa legítima está formada | Base do portfólio. É o que ela já faz |
| Peça **aprovada mas nunca veiculada** | Médio. A pessoa autorizou a campanha que não saiu; pode nem saber que existe | Só com "de acordo" do cliente por escrito |
| **Making-of, bastidor, tomada descartada** | Alto. Ninguém autorizou aquilo especificamente; e frequentemente é o que o NDA protege | Não publicar sem autorização específica |
| **Material bruto** | Alto, em dois eixos: imagem e confidencialidade | Não publicar |
| Peça com **avatar ou voz clonada** | Alto. Dado sensível; legítimo interesse não serve | Só com consentimento específico |

Regra de bolso utilizável: **se o cliente publicou, ela pode mostrar; se o
cliente não publicou, ela precisa perguntar.** É também a regra que o mercado
recomenda: expor o trabalho **só depois de o cliente o ter feito, no tempo
dele** — antes disso, além do risco jurídico, há o risco de estragar o plano de
lançamento do cliente.

**O making-of merece um parágrafo próprio, porque é o pior dos dois mundos.**
Juridicamente é obra distinta, não coberta pelo termo de imagem da campanha, e
captura as pessoas em estado **não-performático** — sem maquiagem, errando a
fala, conversando entre tomadas. Nenhuma autorização de campanha alcança isso.
E é justamente o conteúdo que produtora nenhuma resiste a mostrar. O material
bruto é pior ainda: contém **tomadas descartadas**, e às vezes o motivo do
descarte é a própria pessoa em cena — o cenário clássico de dano moral com
destaque individual.

Do lado do direito autoral e do sigilo, há dois reforços: o art. 24, III da LDA
garante ao titular "o de **conservar a obra inédita**"; e a divulgação não
autorizada de informação confidencial obtida em relação contratual é tipificada
como **crime de concorrência desleal** na Lei 9.279/96 — responsabilidade que
**persiste depois de o contrato terminar**.

**Se o portfólio dela hoje tem só peça final já veiculada, ela está no melhor
quadrante possível desta matriz.** Vale confirmar isso antes de qualquer outra
providência — é a checagem mais rápida e a que mais tranquiliza.

### O que pedir por escrito

**Primeiro, a má notícia: uma cláusula só não resolve.** O portfólio de
publicidade tem **três polos** — a produtora, a marca e **a pessoa em cena, que
não assina o contrato entre as duas**. A marca não pode autorizar, em nome do
creator, um uso que ele nunca consentiu. Todos os modelos de contrato de
portfólio que encontramos são bilaterais, e por isso nenhum fecha o problema.
O único que reconhece isso abertamente é um modelo de fotografia que ressalva
que a cláusula "não se aplica a terceiros (convidados)".

Fechar de verdade exige **dois instrumentos**:

1. cláusula de portfólio no contrato **com a marca** — autoriza exibir a obra;
2. menção ao uso em portfólio do fornecedor **no termo assinado pela pessoa
   que aparece** — ou termo próprio.

O item 2 é o que praticamente ninguém faz. É de onde vem a exposição.

**Segundo, o padrão do setor é mais restritivo do que ela imagina.** No *Guia
Audiovisual vol. 7 — Contratos*, da **APRO com o SEBRAE** (modelos validados
pela ANCINE), a cláusula de portfólio aparece três vezes, sempre como **exceção
dentro da cláusula de confidencialidade**, e sempre com o mesmo recorte estreito:

> "[…] salvo mediante autorização prévia e expressa da Produtora, **com exceção
> expressa para a divulgação do vínculo profissional estabelecido no contrato em
> seu portfólio**."

Leia o que isso libera: apenas **dizer que trabalhou para X**. Não libera exibir
a obra. O padrão da indústria é, portanto, *mais* restritivo que a prática
corrente de portfólio.

E os termos de imagem dos mesmos modelos vão no sentido oposto — amplíssimos:

> "No termo deverá constar que a utilização da imagem e/ou som de voz, nome
> artístico e dados biográficos, será realizada em **caráter irrevogável e
> irretratável** e poderá ser fixada em qualquer suporte material existente,
> bem como produzida, explorada comercialmente e utilizada para publicidade e
> divulgação **da obra audiovisual**, no Brasil e no exterior […]"

Dois alertas sobre esse modelo: (i) o próprio guia diz que ele se destina a
**obra audiovisual NÃO publicitária** — publicidade tem regime próprio, com
convenções coletivas e prazos de veiculação, então **os modelos APRO não cobrem
o caso dela**; e (ii) mesmo esse termo autoriza divulgar **a obra**, nunca a
produtora. Nem o contrato de elenco mais amplo do setor autoriza portfólio de
fornecedor.

**Terceiro, a melhor redação genérica que encontramos** vem de um modelo de
contrato de fotografia — enumera canais, dispensa autorização caso a caso, cria
opt-out formalizado e precifica a exclusividade:

> "O CLIENTE autoriza expressamente o FOTÓGRAFO a utilizar as fotografias e
> vídeos do evento para fins de divulgação profissional, portfólio, redes
> sociais, site, materiais publicitários e participação em concursos
> fotográficos, sem necessidade de autorização prévia para cada uso e sem ônus
> para o FOTÓGRAFO."

Com base nesses três achados, a redação sugerida para o caso dela:

> **USO DO TRABALHO EM PORTFÓLIO**
>
> O CONTRATANTE autoriza a CONTRATADA a exibir o material produzido no âmbito
> deste contrato em seu portfólio profissional — site, redes sociais,
> apresentações comerciais e propostas — com finalidade exclusiva de
> demonstração da própria capacidade técnica, observado o seguinte:
>
> **(a)** a exibição fica limitada ao material **já divulgado publicamente pelo
> CONTRATANTE**. Material não veiculado, bastidor, making-of e material bruto só
> poderão ser exibidos mediante autorização específica e por escrito;
>
> **(b)** a autorização abrange a menção ao nome e à marca do CONTRATANTE
> exclusivamente para identificar a autoria do trabalho, **sem** sugerir
> patrocínio, endosso ou vínculo societário;
>
> **(c)** o CONTRATANTE **declara** que as pessoas que aparecem no material
> autorizaram o uso de sua imagem e voz, e que essa autorização **é compatível
> com a exibição em portfólio de fornecedor**;
>
> **(d)** a CONTRATADA **retirará o material do ar** em até [10] dias úteis
> contados de solicitação escrita do CONTRATANTE ou de qualquer pessoa retratada,
> sem necessidade de justificativa e sem qualquer ônus;
>
> **(e)** esta autorização vigora por prazo indeterminado e pode ser revogada
> pelo CONTRATANTE por escrito, na forma da alínea (d).

A alínea **(c)** é a que faz o trabalho pesado: transfere para o cliente a
declaração sobre a autorização das pessoas, o que ativa o regresso do §7. A
alínea **(d)** é o que evita litígio: quem tira do ar em 10 dias raramente é
processado.

**Duas medidas complementares, baratas:**

1. **Reconsiderar a exibição dos 78 nomes próprios.** Perguntar: o nome da
   pessoa é necessário para demonstrar a competência dela? Na maioria dos
   casos, não — o que vende é o vídeo e a marca. Remover ou reduzir os nomes
   é a maneira mais rápida de encolher a exposição, e é exatamente o que o art.
   10, §1º pede (só o estritamente necessário). Onde o nome **agrega** (talento
   conhecido), vale pedir o "de acordo".
   *Atenção operacional:* a memória do projeto registra que o campo `talento` é
   de **uso duplo** — em alguns projetos guarda nome de pessoa, em outros título
   de vídeo ou nome de produto. Qualquer limpeza precisa distinguir os dois, não
   varrer o campo inteiro.
2. **Publicar um aviso de privacidade curto** no site, com finalidade do
   tratamento e canal de contato. Atende os arts. 9º e 10, §2º (transparência) e
   custa um parágrafo.
3. **Escrever o teste de balanceamento (LIA), mesmo que curto.** Uma página
   registrando: qual a finalidade (divulgar o próprio trabalho), por que é
   legítima (art. 10, I), quais dados são estritamente necessários, por que o
   impacto é baixo (material já público no canal da marca) e como o titular se
   opõe. O guia da ANPD trata isso como parte da base legal, não como
   formalidade — **sem o documento, o legítimo interesse é uma alegação; com
   ele, é uma base.** É a medida de maior retorno por esforço deste documento
   inteiro.

**Um argumento extra, disponível mas não consolidado.** A Lei 9.610/98, art. 85,
diz que, "não havendo disposição em contrário", os co-autores da obra
audiovisual podem utilizar "**em gênero diverso**" a parte que constitua sua
contribuição pessoal. Um portfólio é, plausivelmente, gênero diverso da
veiculação publicitária. **Não encontramos jurisprudência aplicando o art. 85 a
portfólio** — registre como hipótese útil, não como tese firmada. E ele só
alcança quem for **co-autora** (pela lei, o roteirista e o diretor — art. 16),
o que em 534 vídeos certamente não é o caso em todos.

**E o limite de todos esses argumentos autorais:** mesmo que o direito autoral
cobrisse tudo, **não resolveria nada quanto à pessoa em cena.** Direito autoral
e direito de imagem são regimes independentes e paralelos. Ela pode ser 100%
titular da obra e ainda assim responder por dano moral ao creator filmado. O
próprio art. 46, I, "c" da LDA reconhece isso ao ressalvar a oposição do
retratado.

---

## 7. O que exigir do cliente por escrito

O objetivo aqui é um só: **mover o risco para quem tem a informação e o
poder de decisão.** Quem conhece a funcionária, quem contratou o ator, quem
guardou o termo assinado é o cliente. Ela não tem como verificar sozinha.

### Antes de tudo: a boa notícia que muda a negociação

Há uma crença comum — que eu mesmo carreguei até o meio desta pesquisa — de que
o ônus de obter a autorização de imagem é sempre da produtora. **Em publicidade,
é o contrário.** Vale corrigir com todas as letras, porque isso inverte a posição
dela na mesa de negociação.

O **Guia do produtor audiovisual da OAB-RJ** diz que cabe ao produtor "obter
autorização de uso de nome, voz e imagem" — e daí se conclui, naturalmente, que
o ônus é da produtora. **Mas esse guia trata de obra audiovisual em geral
(cinema, documentário), onde a produtora escala o elenco.** Publicidade tem
padrão próprio, e ele é o oposto.

O **Manual de Produção do III Fórum da Produção Publicitária** — o padrão
brasileiro do setor, assinado por **ABAP, APRO, APROSOM, SIAESP e SINAPROSP** —
diz, literalmente:

> "**2.1.3.** O anunciante é o **maior responsável** pelo uso dos materiais
> produzidos."

> "**2.2.4.** A agência de publicidade, **por conta e ordem de seu cliente
> anunciante, é a responsável direta pela contratação dos Direitos de Uso de
> Imagem** e/ou Som de Voz e/ou Nome do Ator ou Modelo […]"

> "**2.3.2.** [A agência/anunciante] é também responsável por **detalhar
> precisamente cada peça/material publicitário, praças/territórios, período e
> mídias** a serem contratadas […]"

**No mercado publicitário brasileiro, o default é a agência/anunciante — não a
produtora.** Ela não está nadando contra a corrente ao exigir isso do cliente:
está **pedindo o padrão do setor**.

E o manual precifica o desvio: *"Quando a contratação de prestação de serviços e
Concessão de Direitos de Imagem for realizada pela produtora, haverá uma **taxa
de serviços de 40%** sobre tais custos […]"*

Guarde esse número. Se o cliente empurrar a coleta de autorização para ela, **o
próprio padrão do setor diz que isso é serviço remunerado a 40%** — não é favor,
não é "já está no pacote". É o argumento comercial mais forte deste documento.

A ressalva honesta: se ela assume a contratação, **assume também o risco**. E há
responsabilidades que são dela de qualquer forma — o manual registra que a
produtora responde por multas de CRT/ANCINE e CONDECINE que podem chegar a
milhões, por liberar filme publicitário sem as formalidades.

### As declarações e garantias

> ⚠️ Texto de trabalho para levar a advogado.

> **DECLARAÇÕES E GARANTIAS DO CONTRATANTE**
>
> O CONTRATANTE declara e garante, sob sua exclusiva responsabilidade, que:
>
> **1. Titularidade.** É titular ou licenciado de todos os direitos sobre os
> materiais que fornecer à CONTRATADA — imagens, vídeos, áudios, marcas,
> músicas, textos e demais conteúdos — e que seu uso na forma contratada não
> viola direito de terceiro.
>
> **2. Autorização das pessoas retratadas.** Todas as pessoas que aparecem ou
> cuja voz é ouvida nos materiais fornecidos autorizaram, **por escrito**, o uso
> de sua imagem, nome e voz, em autorização **vigente** e **compatível** com o
> uso pretendido neste contrato quanto a **finalidade, prazo, território e
> mídia**, incluindo mídia paga quando aplicável.
>
> **3. Autorização específica para inteligência artificial.** Quando o objeto
> incluir criação de avatar digital, clonagem ou síntese de voz, ou geração de
> imagens ou falas que a pessoa não gravou, o CONTRATANTE declara possuir
> autorização **específica e destacada** de cada pessoa envolvida para esse uso,
> nos termos do art. 11, I da Lei 13.709/2018, e que essa autorização
> **contempla expressamente o uso por inteligência artificial** — não se
> tratando de autorização genérica de uso de imagem nem de autorização anterior
> à contratação que não mencione essa modalidade.
>
> **4. Papéis na LGPD.** Para os tratamentos realizados na execução deste
> contrato, o CONTRATANTE é **controlador** e a CONTRATADA atua como
> **operadora**, seguindo suas instruções documentadas. A CONTRATADA poderá
> **recusar** instrução que repute ilícita, sem que isso configure
> inadimplemento, mora ou motivo para rescisão por culpa.
>
> **5. Menores e pessoas em situação especial.** Havendo menor de 18 anos, o
> CONTRATANTE declara possuir autorização dos responsáveis legais e, quando
> exigível, o **alvará judicial** correspondente.
>
> **6. Exatidão do briefing.** As informações prestadas no formulário de
> briefing são verdadeiras e completas, e integram este contrato para todos os
> efeitos. O CONTRATANTE se obriga a **comunicar imediatamente** qualquer
> alteração — em especial revogação de autorização por pessoa retratada.
>
> **7. Aprovação do conteúdo.** A aprovação escrita das peças pelo CONTRATANTE
> implica sua concordância com o conteúdo final e com sua veiculação, sendo dele
> a responsabilidade pela decisão de publicar, pela conformidade publicitária
> (inclusive perante o CONAR) e pela rotulagem de conteúdo gerado por IA nas
> plataformas em que veicular.
>
> **8. Indenização e regresso.** O CONTRATANTE **manterá a CONTRATADA indene** e
> a **reembolsará integralmente** de qualquer perda, custo, despesa, honorário
> advocatício, condenação ou acordo decorrente de reclamação de terceiro
> fundada na falsidade, inexatidão ou descumprimento de qualquer declaração
> deste item — inclusive falta, insuficiência, vencimento ou revogação de
> autorização de uso de imagem ou voz. A CONTRATADA comunicará ao CONTRATANTE
> qualquer reclamação em até [5] dias úteis. **Este direito de regresso
> fundamenta-se no art. 934 do Código Civil e no art. 42, §4º da Lei
> 13.709/2018.**
>
> **9. Limite.** As garantias deste item não se aplicam na medida em que a perda
> decorra de culpa exclusiva da CONTRATADA.

### Por que cada peça existe

| Cláusula | O risco que ela endereça |
|---|---|
| 1 | Material de terceiro entregue pelo cliente (música, imagem de banco) |
| **2** | A base: extrapolação de prazo, praça e finalidade |
| **3** | **A mais importante.** Ataca exatamente o §3 — obriga o cliente a afirmar que a autorização cobre IA, e não uma genérica ou anterior |
| 4 | Fixa os papéis e — crucial — **cria o direito de recusar instrução ilícita** sem ser inadimplente. Sem isso, recusar vira quebra de contrato |
| 5 | Menor exige alvará judicial (Guia OAB-RJ). Erro caro e comum |
| **6** | **Transforma o briefing em documento contratual.** É o que dá valor jurídico ao formulário e materializa a "verificação prévia" que o TJSP disse que seria examinada |
| 7 | Move para o cliente a decisão de publicar, a conformidade publicitária e a rotulagem |
| **8** | O regresso. É o que faz as declarações valerem dinheiro em vez de serem enfeite |
| 9 | Honestidade: nenhuma cláusula cobre negligência própria (art. 43 da LGPD) |

### O hold harmless que o mercado brasileiro já usa

Não precisei inventar o modelo de indenização: **ele existe no padrão
publicitário brasileiro.** O Manual ABAP traz, no *Contrato de Locação e Licença
de Uso de Fotos*, esta cláusula — e ela é instrutiva nos dois sentidos:

> "**CLÁUSULA 3** – A CONTRATADA/FORNECEDORA se responsabiliza pela licença ora
> concedida à CONTRATANTE e por eventuais problemas decorrentes da utilização da
> obra […] problemas esses […] decorrentes de **pleitos judiciais ou
> extrajudiciais de terceiros**, no que tange aos direitos autorais, morais e
> patrimoniais, direitos conexos, **direitos de imagem de pessoas ali
> retratadas** […] **desde que utilizadas estritamente na forma estabelecida
> neste contrato**.
>
> **PARÁGRAFO ÚNICO** – A responsabilidade da CONTRATADA/FORNECEDORA é mantida
> mesmo se eventuais problemas forem promovidos contra a CONTRATANTE e/ou seu
> CLIENTE/ANUNCIANTE […] **remanescendo à CONTRATANTE, e/ou a seu
> CLIENTE/ANUNCIANTE, o direito de regresso**.
>
> **CLÁUSULA 4** – A CONTRATANTE **não poderá proceder as alterações na obra ora
> locada** para sua utilização nas peças publicitárias referidas neste contrato."

**Duas leituras críticas, e as duas trabalham a favor dela:**

1. **A garantia do fornecedor é condicionada** — "desde que utilizadas
   estritamente na forma estabelecida neste contrato". Se o cliente extrapolar —
   por exemplo, mandando alterar por IA algo licenciado apenas para veiculação —
   **a garantia cai e o risco volta para quem alterou**. Essa condicionante é a
   melhor amiga dela na redação: ela deve garantir o que entregou **nos exatos
   termos do briefing aprovado**, e não além.
2. **A Cláusula 4 é a proibição de alteração, por escrito, e é anterior à IA.**
   "Não poderá proceder as alterações na obra" alcança perfeitamente expandir
   plano, trocar cenário e sintetizar fala nova. O mercado já tinha a trava; a IA
   só a tornou urgente.

**Como ela usa isso.** Espelhar a estrutura: garantir o próprio trabalho **com a
mesma condicionante**, e acoplar a declaração do cliente do item 8 acima. O
resultado é simétrico e defensável — ela responde pelo que fez, o cliente
responde pelo que declarou.

### Duas medidas que não são cláusula

- **Guardar tudo, com data.** Briefing preenchido, e-mail de aprovação, termos
  recebidos. Sob o art. 8º, §2º da LGPD, o ônus da prova do consentimento é de
  quem trata. Arquivo organizado é meio de defesa.
- **Considerar seguro de Erros e Omissões (E&O).** O Guia do produtor
  audiovisual da OAB-RJ encerra seu checklist com exatamente esse item: *"Foi
  contratado o seguro de Erros e Omissões?"* É prática consolidada no
  audiovisual justamente para reclamação de imagem e direito autoral. **Não
  pesquisei disponibilidade nem custo para autônomo no Brasil** (§9) — mas é a
  única medida que cobre o cenário em que o cliente declarou algo falso **e**
  não tem como pagar o regresso.

---

## 8. Como isso vira campo de formulário

O documento 07 já desenhou o formulário de Produção com IA. Cruzando com esta
pesquisa: **a estrutura está certa e a maioria dos riscos está coberta.** O que
falta são cinco campos — e um deles é grave.

### O que já está coberto

| Campo do doc 07 | Risco | Situação |
|---|---|---|
| 2.3 "A autorização permite modificar com IA?" | Autorização antiga não cobre IA (§3) | ✅ **É o campo mais valioso do formulário.** Manter. E agora ele tem resposta pronta: se o cliente usou o contrato-padrão do setor, a **cláusula 9.2** já diz que uso não previsto depende de anuência expressa |
| 3.1 "A pessoa já sabe e concordou?" | Súmula 403; art. 11, I | ✅ Coberto |
| 3.2 "Existe documento assinado?" | Ônus da prova (art. 8º, §2º) | ✅ Coberto |
| 3.3 "A voz" | Voz é direito autônomo (CF art. 5º, XXVIII, "a") + dado biométrico | ✅ Coberto |
| 3.4 "Por quanto tempo e onde" | Prazo e praça (LDA art. 50, §2º) | ✅ Coberto |
| 4.2 "Onde o material pode rodar" | Escolha de ferramenta = decidir meios → controladoria (§5) | ✅ Coberto |

### O que falta

**Falta 1 — Portfólio. Nenhum campo pergunta isso. É a lacuna grave.**
O formulário inteiro cuida da produção e **nada** cuida do direito de ela
mostrar o resultado. Considerando que o portfólio dela tem 534 vídeos e 78
nomes próprios no ar (§6), é a omissão mais cara do conjunto.

> **Campo novo — "Posso mostrar esse trabalho depois?"**
> Opções: `Sim, quando estiver publicado` · `Sim, mas me avise antes` ·
> `Só com aprovação nossa por escrito` · `Não, é confidencial`
> Ajuda: *"Meu portfólio é como novos clientes me encontram. Combinar isso
> agora evita ter que perguntar depois — e se for confidencial, tudo bem, é só
> me dizer."*

> **Sub-campo condicional** (se houver pessoa real em cena e a resposta acima
> não for "não"): **"A autorização assinada por quem aparece cobre mostrar o
> vídeo no portfólio de fornecedor?"** → `Sim` · `Não` · `Não sei`
> Ajuda: *"Pergunto porque a autorização costuma valer para a campanha de
> vocês, não para o site de quem produziu. Se não cobrir, é uma linha a mais
> no termo — resolve em um minuto agora, e não resolve depois."*
>
> Este sub-campo é o que ataca o **problema dos três polos** (§6): o contrato
> entre ela e a marca não vincula a pessoa filmada. Sem tocar no termo do
> talento, o portfólio continua exposto por mais cláusulas que ela assine com o
> cliente.

**Falta 2 — Quem obtém o termo, se ele não existir.**
O 3.2 descobre que **não há** documento. Não define **quem resolve**. E como o
padrão do setor diz que isso é **serviço remunerado a 40%** quando cai na
produtora (§7), deixar em aberto é abrir mão de receita, não só de proteção.

> **Campo condicional** (aparece se 3.2 = "não tem nada" ou "só de boca"):
> **"Quem vai cuidar da autorização?"**
> Opções: `Nós cuidamos e te enviamos assinado` ·
> `Prefiro que você me mande o modelo e eu coleto` ·
> `Quero que você cuide disso (incluir no orçamento)` · `Não sei`
> Ajuda: *"Qualquer caminho serve — só preciso saber qual, porque muda o prazo
> e o escopo."*
>
> Note a terceira opção: ela **inclui no orçamento**, e isso é sustentado pelo
> padrão de mercado. Não é cobrança inventada.

**Falta 3 — Menor de idade.**
Menor exige autorização dos responsáveis e, quando aplicável, **alvará
judicial** (Guia OAB-RJ). Isso não é detalhe: é semanas de prazo.

> **Campo condicional** (se houver pessoa real): **"Alguma pessoa que aparece
> tem menos de 18 anos?"** → `Não` · `Sim` · `Não sei`
> Ajuda: *"Se tiver, o caminho é diferente e leva mais tempo — precisa de
> autorização dos pais e, em alguns casos, de autorização da Justiça."*

**Falta 4 — O que acontece com o avatar no fim.**
O 3.4 pergunta por quanto tempo o rosto pode ser usado. Não pergunta o destino
do **modelo treinado**, que é um ativo separado e sobrevive à campanha.

> **Sub-campo do 3.4:** **"Quando o prazo acabar, o que fazer com o avatar?"**
> Opções: `Apagar tudo` · `Guardar para usar de novo (renovando a autorização)` ·
> `Não sei`
> Ajuda: *"O avatar é um arquivo que continua existindo depois do vídeo pronto.
> Melhor combinar agora se ele fica guardado ou se some no fim."*

**Falta 5 — A declaração formal do cliente.**
Perguntar "existe autorização?" gera **informação**. Fazer o cliente **declarar**
gera **prova**. É a diferença entre saber e poder cobrar depois. O §7, cláusula
6, transforma o briefing em documento contratual — mas isso só funciona se o
formulário disser isso na cara.

> **No fim do formulário, antes de enviar — checkbox obrigatório:**
> ☐ *"Confirmo que as informações acima são verdadeiras e que, quando houver
> pessoas no material, os direitos de uso de imagem e voz estão em ordem do
> nosso lado."*
> Ajuda: *"Isso vira parte da proposta. Não é pegadinha — é o que me permite
> tocar o projeto sem travar tudo em jurídico."*

### Um ajuste de redação

No 3.3 (voz), a ajuda diz: *"a lei brasileira trata voz como dado sensível."*
**Impreciso** (§4). Voz vira dado sensível quando é processada para identificar
ou replicar a pessoa — que é justamente o caso do clone, mas não de qualquer
gravação. E o fundamento mais forte e mais simples é outro: **a Constituição
cita a voz junto com a imagem**. Sugestão:

> *"Usar a voz da própria pessoa é possível e dá o melhor resultado, mas exige
> uma autorização separada da do rosto — a lei protege voz e imagem como coisas
> diferentes, e clonar uma voz é mais delicado do que gravar uma."*

### Uma nota sobre a ordem

O documento 07 põe o bloco de risco no Passo 3, depois de o cliente já ter
investido no preenchimento. **Do ponto de vista jurídico isso continua certo** —
o que importa é que as perguntas sejam feitas e registradas **antes de
orçar**, não que venham primeiro na tela. O que a pesquisa acrescenta é o
motivo: no caso do TJSP, o tribunal disse que se examinaria **"se houve algum
tipo de verificação prévia"**. Prévia à produção. O Passo 3 satisfaz isso.

---

## 9. O que eu NÃO consegui confirmar

- **A definição de "dado biométrico" pela ANPD — CONFIRMADO QUE NÃO EXISTE.**
  Esta era a maior lacuna do documento e ela **fechou, com resposta negativa**:
  varri o portal e o Glossário oficial da ANPD (atualizado em 08/07/2026) **não
  traz verbete de dado biométrico, biometria, reconhecimento facial nem
  inteligência artificial**, e a lista de guias orientativos não tem nenhum
  sobre esses temas (§4). Logo, a afirmação central do §4 — de que face e voz
  só viram sensível com processamento técnico de identificação — **continua
  apoiada na lei, no GDPR e na doutrina, e não em ato da ANPD, porque tal ato
  não existe.** Isso é diferente de "não consegui achar": eu procurei na fonte e
  o vazio é real. Consequência prática: **a questão é genuinamente incerta no
  Brasil**, e a decisão conservadora é a defensável.

- **Regulamento da ANPD sobre dados biométricos: não localizei nenhum**, e a
  ausência é coerente com o vazio do glossário. O documento 07 registrou que até
  março/2026 não havia, com previsão para 2026 — **em agosto de 2026 continuo
  sem encontrar.** Não descarto que exista consulta pública ou minuta em
  tramitação que eu não tenha alcançado.

- **O caso Grok — CONFIRMADO por pesquisa paralela em 13/08/2026.** Esta lacuna
  **fechou** depois que o documento foi escrito. A confirmação veio de uma
  pesquisa de apoio que alcançou o PDF do **Radar Tecnológico nº 6 — *Deepfakes***
  (ANPD, 2026, 163 p., ISBN 978-65-82658-05-1), onde a própria ANPD narra o ato,
  às p. 102-103, literalmente:

  > "Por fim, no dia 11 de fevereiro de 2026, as instituições envolvidas na
  > Recomendação Conjunta avaliaram como insuficientes as providências
  > informadas, e a ANPD expediu medida preventiva **com fundamento nos arts. 32,
  > III, e 35 do Regulamento de Fiscalização**, de modo a impedir que a
  > ferramenta de inteligência artificial Grok gere conteúdos que representem
  > crianças e adolescentes ou pessoas maiores de idade identificadas ou
  > identificáveis em contextos sexualizados ou erotizados, sem autorização."

  Documentos com número e link confirmados: **Nota Técnica nº 1/2026/FIS/CGF/ANPD**
  (doc. SEI 0239948, Processo nº 00261.000178/2026-27, de 20/01/2026), que
  *propõe* a medida, e a **Recomendação Conjunta ANPD + MPF + Senacon** de
  20/01/2026. **Continua não confirmado:** o número do despacho/voto que efetivou
  a medida, o Circuito Deliberativo e a publicação em DOU — o portal bloqueia
  busca automatizada. Não inventar esses números.

  **Consequência:** deepfake deixou de ser, para a ANPD, assunto apenas de
  estudo. Há ato de fiscalização concreto sobre geração de imagem e voz de
  pessoa identificável sem autorização. Isso **aumenta** o peso do §4.

- **O Guia de Agentes de Tratamento — RESOLVIDO.** Consegui o arquivo oficial da
  ANPD e li o texto da **versão 2.0 (abril/2022)**. As citações do §5 (itens 8,
  9, 59 e 60) vêm do documento, não de fonte secundária. **Ressalva de forma:** o
  PDF publicado pela ANPD é o arquivo do processo SEI nº 00261.000468/2021-66
  (Nota Técnica nº 10/2021/CGN/ANPD), que contém a proposta, a consulta pública
  e várias versões em sequência — inclusive minutas preliminares de 2021. **Eu
  extraí o texto do bloco da versão 2.0 final**, mas quem for citar em peça
  jurídica deve conferir a paginação na versão diagramada, porque a numeração
  dos itens varia entre as minutas (o mesmo trecho é item 59 numa versão e 60 em
  outra).

- **Se a autorização de uso de imagem é revogável — não há decisão do STJ
  localizada.** A doutrina sustenta que sim, e que renúncia ao direito de
  revogar é inválida; os contratos-padrão do setor dizem "irrevogável e
  irretratável". **É litígio latente, não questão resolvida** (§6).

- **Os precedentes do STJ (REsp 1.822.619 e REsp 1.772.593) foram confirmados
  pelas notícias oficiais do próprio STJ, não pela leitura dos acórdãos.** O
  caso do TJDFT (0708200-37.2020.8.07.0016) idem, pela notícia oficial do
  tribunal. As teses estão corretas; se forem citadas em peça jurídica, os
  inteiros teores precisam ser lidos.

- **O desfecho do caso do TJSP sobre voz clonada.** Li o acórdão que anulou a
  sentença e mandou fazer perícia (31/10/2024). **Não achei o resultado do
  mérito.** Não sei se houve condenação. Não use como precedente de condenação.

- **Outros casos brasileiros sobre clone de voz ou avatar por IA em contexto
  publicitário.** Achei **um** julgado, e ele é de segundo grau, sobre questão
  processual. Apareceram menções em resumos de busca a (i) um influenciador
  condenado a R$ 50 mil por clonar vozes de celebridades e (ii) uma tutela de
  urgência da 35ª Vara Cível de SP em jun/2025 com multa diária de R$ 50 mil por
  vídeos com voz e imagem de médico gerados por IA. **Não abri nem confirmei
  nenhum dos dois** e por isso não os usei na análise. **A jurisprudência
  brasileira sobre isso é praticamente inexistente — e essa escassez é, em si,
  um risco: não há como prever com segurança como um juiz decidirá.**

- **Caso brasileiro de fotógrafo ou produtora processado por usar trabalho de
  cliente em portfólio: procuramos por várias formulações e NÃO encontramos
  nenhum.** Registro como achado, não como lacuna: o risco é doutrinariamente
  reconhecido e contratualmente tratado, mas a litigiosidade é praticamente
  nula. Isso **não** significa que o uso seja lícito — significa que o cenário
  provável é notificação extrajudicial, não ação.

- **Cláusula brasileira autorizando uso por IA: não existe modelo consolidado.**
  Os termos que circulam no Brasil — universidades, órgãos públicos, escritórios
  — **não têm cláusula de IA**. A única cláusula real e completa que encontrei
  está em **português de Portugal** (GDA) e é de **exclusão**, não de
  autorização. O material brasileiro é analítico: diz o que a cláusula deve
  conter, não traz o texto. **As cláusulas dos §3, §6 e §7 deste documento foram
  redigidas a partir dos requisitos legais, não copiadas de um modelo
  existente.** Precisam de revisão de advogado.

- **Não li a decisão original do CONAR no caso Volkswagen / Elis Regina.**
  Trabalhei com notícias e análises convergentes. Os três fundamentos do
  arquivamento (§2) devem ser conferidos na decisão antes de virarem argumento
  formal.

- **Números de acórdão citados por artigos, não conferidos no STJ.** Alguns
  artigos citam REsp 1.384.424, REsp 1.243.699 e AgInt no REsp 2.040.356/SP a
  propósito de irrenunciabilidade da imagem. **Não abri nenhum deles** (o
  buscador do STJ é renderizado por JavaScript e não devolveu inteiro teor).
  Não use esses números sem conferir.

- **Um detalhe metodológico que vale registrar:** a pesquisa paralela feita para
  este documento concluiu que **não existe caso brasileiro sobre clone de voz por
  IA**. Eu encontrei um — o acórdão do TJSP do §2 — e o li na íntegra. A
  divergência mostra que o caso é obscuro o bastante para não aparecer em busca
  comum. Reforça o ponto: **a jurisprudência é rasa, e o pouco que existe é
  difícil de achar.**

- **Seguro de Erros e Omissões para autônomo no Brasil.** Recomendei porque o
  Guia da OAB-RJ o traz no checklist. **Não pesquisei se há seguradora que
  atenda profissional autônoma nem a que custo.** A busca esbarrou no limite de
  buscas da sessão.

- **A prática contratual do mercado publicitário brasileiro** (APRO, ABAP,
  sindicatos) sobre quem obtém a autorização. Trabalhei com o Guia da OAB-RJ,
  que é fonte sólida, e com modelos de contrato encontrados em busca. **Não abri
  documentos das associações setoriais.**

- **Se o campo `talento` do site é exibido ao público em todos os casos.** Contei
  78 nomes próprios **no arquivo de dados**. Confirmei pela memória do projeto
  que o campo é de uso duplo e alimenta a interface, mas **não verifiquei a
  renderização de cada um na página** — o número exato de nomes efetivamente
  visíveis pode ser menor.

---

## 10. Fontes

### Fontes primárias — lei em vigor (todas abertas e conferidas)

- [Constituição Federal — art. 5º](https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm) — incisos V, X (imagem, indenização) e **XXVIII, "a"** (reprodução da imagem **e voz** humanas). Planalto.
- [Código Civil, Lei 10.406/2002](https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm) — arts. 11, 12 (direitos da personalidade, cessação), **20** ("transmissão da palavra" e fins comerciais), 21, 186, 927 e **934** (regresso). Planalto.
- [LGPD, Lei 13.709/2018](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm) — arts. 4º (não aplicação), 5º (definições, incl. VI e VII), 6º (princípios), 7º, **8º** (§§1º a 5º — destaque, ônus da prova, nulidade da autorização genérica, revogação), 9º, 10, **11** (dado sensível), 16, 18, 39, **42** (§1º, I e §4º), 43, 44 e 52 (sanções). Planalto.
- [Lei de Direitos Autorais, Lei 9.610/98](https://www.planalto.gov.br/ccivil_03/leis/l9610.htm) — **art. 4º** (interpretação restritiva), 24 (direitos morais), **49, V e VI** (modalidades existentes à data do contrato) e **50, §2º** (tempo, lugar e preço). Planalto.
- [Lei 15.123/2025](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15123.htm) — aumento de pena com uso de IA no art. 147-B do Código Penal. **Escopo restrito a violência psicológica contra a mulher**; não é lei geral sobre IA. Planalto.

### Jurisprudência e súmula

- [STJ — Súmula 403, texto oficial (PDF)](https://www.stj.jus.br/docs_internet/revista/eletronica/stj-revista-sumulas-2014_38_capSumula403.pdf) — enunciado, referências e os 9 precedentes. Segunda Seção, 28.10.2009, DJe 24.11.2009.
- [TJSP — Apelação Cível 1119021-41.2023.8.26.0100, acórdão integral (PDF)](https://ioda.org.br/wp-content/uploads/2024/11/Inteligencia-Artificial-acordao.pdf) — **o único caso brasileiro sobre voz clonada por IA que encontrei.** 6ª Câm. Dir. Privado, rel. Des. José Carlos Costa Netto, 31/10/2024, v.u. Decisão processual (anula sentença, determina perícia).
- [IODA — ficha do caso](https://ioda.org.br/publicacoes/jurisprudencia-brasileira/inteligencia-artificial-e-o-uso-nao-autorizado-de-voz/) — contexto e partes.
- [STJ — REsp 1.822.619, 3ª Turma, rel. Min. Nancy Andrighi](https://www.stj.jus.br/sites/portalp/Paginas/Comunicacao/Noticias/Direito-autoral-deve-ser-respeitado-mesmo-que-foto-esteja-disponivel-na-internet.aspx) — **estar acessível na internet não presume domínio público.** Derruba a tese "já está público" (§6). Notícia oficial do STJ.
- [STJ — REsp 1.772.593, 3ª Turma, rel. Min. Nancy Andrighi, 16/06/2020](https://www.stj.jus.br/sites/portalp/Paginas/Comunicacao/Noticias/Para-Terceira-Turma--uso-publicitario-de-imagem-de-torcedor-em-estadio-nao-gerou-dano-moral.aspx) — torcedor em estádio; **sem destaque individual, sem dano moral.** A régua favorável do §6. Notícia oficial do STJ.
- [TJDFT — proc. 0708200-37.2020.8.07.0016, 5º Juizado Especial Cível de Brasília](https://www.tjdft.jus.br/institucional/imprensa/noticias/2020/agosto/publicacao-de-imagem-sem-autorizacao-de-cliente-gera-dever-indenizar) — casa noturna publicou foto de cliente no próprio Instagram: remoção em 5 dias + **R$ 3.000**. O caso estruturalmente mais próximo do portfólio. Notícia oficial do TJDFT.
- [TJDFT — proc. 0722772-72.2022.8.07.0001](https://www.tjdft.jus.br/institucional/imprensa/noticias/2023/julho/fotografa-nao-deve-ser-indenizada-por-fotos-de-cliente-publicadas-em-conta-pessoal) — fotógrafa × cliente: **o que não está no contrato, o juiz não presume.** Corta para os dois lados.
- [TJSP — uso indevido de imagens, 6ª Câm. Dir. Privado](https://www.tjsp.jus.br/Noticias/Noticia?codigoNoticia=38553) e [STJ — condenação da Oi por fotos em cartões telefônicos](https://www.stj.jus.br/sites/portalp/Paginas/Comunicacao/Noticias/14092020-Terceira-Turma-mantem-condenacao-da-Oi-por-uso-nao-autorizado-de-fotos-em-cartoes-telefonicos.aspx) — o vetor oposto: fotógrafos processando por uso da obra.

### Fontes setoriais — prática do audiovisual

- [OAB-RJ — Guia do produtor audiovisual (PDF, 80 p.)](https://www.oabrj.org.br/arquivos/files/CDADIE_guia_do_produtor_audiovisual_final_web.pdf) — Comissão de Direito Autoral, Direitos Imateriais e Entretenimento. **A fonte mais útil desta pesquisa depois da lei.** De onde vêm: "as diversas modalidades de utilização são independentes entre si, não havendo abertura para presunções"; o dever do produtor de obter autorização de nome, voz e imagem; o alvará judicial para menores; os elementos essenciais do contrato (objeto, prazo, preço, modalidades, territórios); e o checklist final, incluindo o seguro de Erros e Omissões.
- **[Manual de Produção do III Fórum da Produção Publicitária — ABAP, APRO, APROSOM, SIAESP, SINAPROSP (PDF)](https://www.abap.com.br/wp-content/uploads/2021/06/manual-de-producao-iii-forum-de-producao-publicitaria-1.pdf)** — **o padrão do mercado publicitário brasileiro, e a fonte mais decisiva do §3 e do §7.** De onde vêm: o Contrato-Padrão de Concessão de Uso de Imagem (cláusulas 9.1, 9.2 e 9.3 — "montagem, cortes e reproduções" e "qualquer utilização não prevista […] depende de expressa anuência"); os itens 2.1.3, 2.2.4 e 2.3.2 (**a agência, por conta do anunciante, é a responsável direta pela contratação dos direitos de imagem**); a taxa de 40% quando a produtora assume; e o hold harmless do Contrato de Locação e Licença de Uso de Fotos (cláusulas 3, parágrafo único e 4).
- [APRO — Guia de Boas Práticas para a contratação de serviços de produção publicitária (PDF)](https://apro.org.br/uploads/guia/Guia-Apro-0408.pdf) — responsabilidade em cascata: irregularidade do elenco reflete "ainda que indireta" na agência e no anunciante; direitos conexos e de personalidade do elenco exigem autorização expressa.
- **[GDA — Guia sobre Inteligência Artificial (Portugal, mai/2024, PDF)](https://www.gda.pt/wp-content/uploads/2024/05/GDA-AI-Guia.pdf)** — **a única cláusula real e completa sobre IA que encontrei em português**, transcrita no §3, mais o checklist do que a autorização afirmativa precisa conter e a recomendação de documento separado. Fonte portuguesa: **não é lei brasileira**, é referência de redação.
- APRO / SEBRAE — [Guia Audiovisual, vol. 7 — Contratos (2015), PDF integral](https://bibliotecas.sebrae.com.br/chronus/ARQUIVOS_CHRONUS/bds/bds.nsf/09640a8136324b820d6d5b4f92c33a56/$File/7673.pdf) ([ficha](https://bis.sebrae.com.br/bis/conteudoPublicacao.zhtml?id=7673) · [validação pela ANCINE](https://www.exibidor.com.br/noticias/mercado/3053-ancine-valida-modelos-de-contratos-da-apro-para-o-audiovisual)) — modelos referenciais do setor. Origem das cláusulas de portfólio transcritas no §6 (p. 40, 117 e 122), do termo de figuração "irrevogável e irretratável" (p. 66) e do contrato de elenco (p. 43). **Atenção: o guia declara que esses modelos são para obra audiovisual NÃO publicitária.**
### ANPD — documentos oficiais (orientativos não são vinculantes; votos e despachos são atos decisórios)

- **[ANPD — Guia Orientativo para Definições dos Agentes de Tratamento de Dados Pessoais e do Encarregado, v2.0 (abril/2022)](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-para-definicoes-dos-agentes-de-tratamento-de-dados-pessoais-e-do-encarregado)** · [PDF oficial](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/anonimizado___guia_de_agente_de_tratamento_e_encarregado_da_anpd_novo.pdf/@@display-file/file) — **lido no original**; base do §5. Item 8 (o papel é definido por operação, a mesma pessoa pode ser controladora e operadora); **item 9** (pessoa natural: controladora quando decide finalidades e **elementos essenciais**, operadora quando só define elementos **não essenciais**); item 59 (art. 37 — ambos mantêm registro das operações); **item 60** (a equiparação do operador ao controlador é **excepcionalidade**; "em regra a responsabilidade é do controlador"); itens 40-44 (controladoria conjunta, por decisões comuns ou convergentes). O documento é o arquivo do processo SEI nº 00261.000468/2021-66 (NT nº 10/2021/CGN/ANPD) e contém minutas anteriores — ver ressalva no §9. A própria ANPD o define como **"diretrizes não-vinculantes"**.
- **[ANPD — Glossário de Proteção de Dados Pessoais e da Privacidade](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/glossario-anpd)** — publicado em 23/05/2024, **modificado em 08/07/2026**. Usado no §4 como **prova de ausência**: nenhum verbete de dado biométrico, biometria, reconhecimento facial ou inteligência artificial; "biométrico" aparece uma única vez, dentro da transcrição do art. 5º, II da LGPD.
- [ANPD — índice de Materiais Educativos e Publicações](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes) — a lista completa de guias orientativos, conferida em 13/08/2026. **Nenhum sobre biometria ou IA.**
- [ANPD — Guia Orientativo: Legítimo Interesse (v1.0, fev/2024)](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia_orientativo_hipoteses_legais_tratamento_de_dados_pessoais_legitimo_interesse) · [PDF](https://www.gov.br/anpd/pt-br/documentos-e-publicacoes/guia_legitimo_interesse.pdf) · [análise do Data Privacy Brasil](https://www.dataprivacybr.org/guia-do-legitimo-interesse-orientacoes-da-anpd/) — base do §6: os quatro fatores da legítima expectativa (relação prévia; fonte e forma da coleta; contexto e período; finalidade e compatibilidade), a exigência de "possibilidade efetiva de se opor", e a régua de que "o que a LGPD exige não é o impacto zero". **O modelo de teste de balanceamento proposto não é de uso obrigatório.**
- [ANPD — Guia Orientativo: Cookies e proteção de dados pessoais (v1.0, out/2022, PDF)](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-cookies-e-protecao-de-dados-pessoais.pdf/@@display-file/file) — apesar do título, é **a fonte oficial mais completa da ANPD sobre os requisitos de validade do consentimento**, inclusive o que significa "específica e destacada" para dado sensível (§4). **Não há guia da ANPD dedicado a consentimento** — varredura do portal confirmou.
- **ANPD — caso Meta (treinamento de IA generativa com dados de usuários).** Processo principal **nº 00261.004509/2024-36**, instaurado de ofício em 28/06/2024, **em andamento, sem decisão final e sem sanção** (Painel da Fiscalização, dados de 11/03/2026). Atos: [Despacho Decisório nº 20/2024/PR/ANPD, DOU 02/07/2024](https://www.in.gov.br/web/dou/-/despacho-decisorio-n-20/2024/pr/anpd-569297245) (medida preventiva, multa diária de R$ 50 mil); [Voto nº 11/2024/DIR-MW/CD](https://www.gov.br/anpd/pt-br/assuntos/deliberacoes-do-conselho-diretor/circuitos-deliberativos-2024/cd-12-2024-votos.pdf/@@display-file/file) (itens 3.11, 4.28 e 4.56 — citados no §4); [Despacho Decisório nº 33/2024, DOU 30/08/2024](https://www.in.gov.br/web/dou/-/despacho-decisorio-n-33/2024/pr/anpd-581192714) e [Voto nº 23/2024/DIR-JR/CD](https://www.gov.br/anpd/pt-br/assuntos/deliberacoes-do-conselho-diretor/circuitos-deliberativos-2024/cd-18-2024-votos.pdf/@@display-file/file) (item 4.54 — legítimo interesse não se aplica a dado sensível; itens 4.17 e 4.60 — a suspensão da medida **não** legitima o uso de legítimo interesse para treinar IA).
- [ANPD — Painel da Fiscalização](https://www.gov.br/anpd/pt-br/assuntos/fiscalizacao/saiba-como_fiscalizamos) — base oficial usada para confirmar que o caso Meta segue em andamento e que não há processo sancionador contra a empresa.

### Modelos de cláusula de portfólio (prática de mercado, não fonte oficial)

- [GeraContratos — modelo de contrato de fotografia](https://geracontratos.com.br/modelo-contrato-fotografia) — a melhor redação genérica encontrada; transcrita no §6. Reconhece expressamente que **não alcança terceiros em cena**.
- [EPICS — contrato de vídeo para videomakers](https://www.epics.com.br/blog/contrato-de-video) e [Contrato Especialista — produção audiovisual](https://contrato-especialista.com/modelo-contrato-de-producao-audiovisual/) — cláusulas curtas de portfólio.
- [Moysés Remma — designers não precisam de autorização para expor trabalhos no portfólio](https://www.moysesremma.com.br/designers-nao-precisam-de-autorizacao-para-expor-trabalhos-no-portfolio/) — origem da regra "só depois de o cliente publicar, no tempo dele". Tese de direito moral do autor discutida e relativizada no §6.
- [ABRA — Contrato Padrão](https://abra.art.br/contrato-padrao/) — não aberto.

### Tramitação legislativa (não é lei)

- [Câmara dos Deputados — ficha de tramitação do PL 2338/2023](https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao=2487262) — consultada em 13/08/2026. Situação: **"Aguardando Parecer do(a) Relator(a) na Comissão Especial"**. Fecha a pendência deixada no documento 07.
- [Senado Federal — PL 2338/2023](https://www25.senado.leg.br/web/atividade/materias/-/materia/157233) — aprovação no Senado em 10/12/2024.

### CONAR — autorregulação (não é lei nem decisão judicial)

- [Migalhas — CONAR arquiva processo contra a Volkswagen pelo comercial com Elis Regina](https://www.migalhas.com.br/quentes/392385/conar-arquiva-processo-contra-volks-por-comercial-com-elis-regina) · [Olhar Digital](https://olhardigital.com.br/2023/08/24/pro/elis-regina-com-ia-conar-arquiva-processo-contra-propaganda-da-vw/) · [CAI OAB-PR](https://cai.oabpr.org.br/devidas-adequacoes-entre-o-direito-e-a-tecnologia-conar-arquiva-processo-contra-volkswagen/) — arquivamento por unanimidade (2023). Origem do tripé **consentimento + coerência + transparência** do §2. **Não li a decisão original do CONAR**, apenas as notícias e análises.

### Referência comparada (não é lei no Brasil)

- [GDPR, art. 4](https://gdpr-info.eu/art-4-gdpr/) — definição (14) de dado biométrico, com o qualificador "specific technical processing" / "unique identification" que a LGPD omitiu. Critério interpretativo do §4.
- **ELVIS Act (Tennessee)** — em vigor desde 01/07/2024; estende o direito de imagem à voz, incluindo **simulação** da voz. [Vanderbilt Law](https://law.vanderbilt.edu/why-tennessees-elvis-act-is-the-king-of-artificial-intelligence-protections/) · [Proskauer](https://www.proskauer.com/blog/the-king-is-back-in-the-digital-era-the-elvis-act-generative-ai-and-right-of-publicity)
- **California AB 2602** (Labor Code § 927), vigente desde 01/01/2025 — [texto oficial](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202320240AB2602) · [Proskauer](https://www.proskauer.com/blog/california-enacts-generative-ai-law-addressing-digital-replicas-of-performers). Torna inexequível cláusula de réplica digital sem "descrição razoavelmente específica" dos usos.
- **EU AI Act, art. 50** — obrigações de transparência de deepfake desde 02/08/2026. [artificialintelligenceact.eu](https://artificialintelligenceact.eu/article/50/) · [FAQ da Comissão Europeia](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act)
- **NO FAKES Act** — **projeto**, reintroduzido em 20/05/2026 como [S.4591](https://www.congress.gov/bill/119th-congress/senate-bill/4591/text) / [H.R.8915](https://www.congress.gov/bill/119th-congress/house-bill/8915/text/ih). Quarta tentativa em cerca de três anos; **nunca aprovado**. O texto integral não foi aberto (congress.gov retornou 403).
- [SAG-AFTRA — 2025 Interactive Media Agreement](https://www.sagaftra.org/contracts-industry-resources/interactive/2025-interactive-media-video-game-agreement) e [recursos de IA do contrato 2023 TV/Theatrical](https://www.sagaftra.org/contracts-industry-resources/contracts/2023-tvtheatrical-contracts/artificial-intelligence-resources) · análise de [Frankfurt Kurnit](https://technologylaw.fkks.com/post/102mewu/inside-the-new-sag-aftra-interactive-media-agreement-new-standards-for-ai-and-di) — **acordo coletivo, não lei**: consentimento separado, escrito, "razoavelmente específico", vedado consentimento em branco, e **o consentimento se invalida se o uso deixar de corresponder à descrição dada**.
- [WIPO Magazine — Arijit Singh v. Codible Ventures (Índia, 2024)](https://www.wipo.int/pt/web/wipo-magazine/articles/ai-voice-cloning-how-a-bollywood-veteran-set-a-legal-precedent-73631) — decisão sobre síntese não autorizada de voz por IA generativa.

### Entendimento de escritório e doutrina (não é lei nem jurisprudência)

- [Migalhas — IA e apropriação: proteção da imagem, voz e LGPD para atores no Brasil](https://www.migalhas.com.br/depeso/444941/ia-e-apropriacao-protecao-da-imagem-voz-e-lgpd-para-atores-no-brasil) — Jessica Marcelli de Oliveira Campos, 27/11/2025. Fonte citada no doc 07; aberta e conferida aqui. Diz que imagem e voz "constituem **dados pessoais**" — formulação mais contida do que "dado sensível", o que motivou a correção do §4.
- [Baril Advogados — manipulação de imagens com IA: riscos aos direitos de imagem e voz](https://www.bariladvogados.com.br/post/manipula%C3%A7%C3%A3o-de-imagens-com-ia-riscos-aos-direitos-de-imagem-e-voz-na-publicidade-e-entretenimento) — "a criação de avatar ou 'réplica digital' também requer autorização". Não traz redação de cláusula.
- [Peduti Advogados — abrangência da proteção ao direito de voz](https://blog.peduti.com.br/protecao-ao-direito-de-voz/) — base legal da voz: CF art. 5º, XXVIII, "a"; CC art. 20; LDA art. 90.
- [Legale — uso comercial não autorizado e Súmula 403](https://legale.com.br/blog/direito-de-imagem-uso-comercial-nao-autorizado-e-sumula-403/) — dano presumido (*in re ipsa*).
- [Dizer o Direito — a Súmula 403 não se aplica a fato histórico de repercussão social](https://buscadordizerodireito.com.br/jurisprudencia/5390/a-sumula-403-do-stj-nao-se-aplica-para-divulgacao-de-imagem-vinculada-a-fato-historico-de-repercussao-social) — limite da súmula.
- [Estratégia Carreira Jurídica — mitigação da Súmula 403 e a tese do mero coadjuvante](https://cj.estrategia.com/portal/direito-imagem-mitigacao-sumula-403-stj/) — o outro limite.
- [Blog As Claras — fotografia é dado pessoal sensível?](https://blog.asclaras.com.br/2022/09/28/mas-afinal-fotografia-e-dado-pessoal-sensivel/) e [TechCompliance — dados biométricos e LGPD](https://techcompliance.org/dados-biometricos/) — a distinção entre imagem bruta e template biométrico, e a ausência de definição técnica na LGPD.
- [Meio & Mensagem — o papel das agências em relação à LGPD](https://www.meioemensagem.com.br/opiniao/o-papel-das-agencias-em-relacao-a-lgpd) — no mercado de comunicação, marcas tendem a ser controladoras e agências operadoras, com corresponsabilidade conforme a relação.
- [Migalhas — LGPD e os agentes de tratamento](https://www.migalhas.com.br/depeso/372430/lgpd-e-os-agentes-de-tratamento) e [Tripla — controladoria conjunta e suboperador](https://blog.tripla.com.br/anpd-proximos-passos-definicao-de-controladoria-conjunta-e-suboperador/) — critérios de controladoria conjunta atribuídos ao guia da ANPD. **Fontes secundárias; o guia oficial não foi aberto** (§9).
- Schenini Moreira, André de Oliveira. [A exceção dos dados pessoais tornados manifestamente públicos pelo titular na LGPD](https://www.migalhas.com.br/depeso/293745/a-excecao-dos-dados-pessoais-tornados-manifestamente-publicos-pelo-titular-na-lgpd). Migalhas, 07/01/2019 — a hipótese do art. 7º, §4º pressupõe que **o próprio titular** publicou. Base do §6(b).
- [DP Especialista — direitos de uso de imagem do empregado pela empresa](https://dpespecialista.com.br/2025/08/05/direitos-de-uso-de-imagem-do-empregado-pela-empresa-consideracoes/), 05/08/2025 — interpretação restritiva do consentimento do retratado: não se estende a outros meios, finalidades ou momento diverso do pactuado.
- Cesa e Silva, Thaís. [A Revogação da Limitação ao Direito à Imagem](https://julgar.pt/wp-content/uploads/2021/10/20211026-JULGAR-Revoga%C3%A7%C3%A3o-da-Limita%C3%A7%C3%A3o-ao-Direito-%C3%A0-Imagem-Thai%CC%81s-Cesa-e-Silva-1.pdf). Revista JULGAR, out/2021 — estudo comparado luso-brasileiro sobre revogabilidade. **PDF não aberto integralmente.**
- [Migalhas — proteção de dados pessoais no uso de imagem e voz](https://www.migalhas.com.br/depeso/394075/protecao-de-dados-pessoais-no-uso-de-imagem-e-voz) (Bechara, Moraes e Izidoro, 26/09/2023) e [Migalhas — o direito à imagem e seus contornos na jurisprudência](https://www.migalhas.com.br/depeso/330606/o-direito-a-imagem-e-seus-contornos-na-jurisprudencia) (jul/2020).

### Fonte interna do projeto

- `docs/research/2026-08-13-formularios-por-servico/07-producao-com-ia.md` — rotulagem por plataforma, licenciamento de ferramentas (HeyGen, Synthesia, ElevenLabs, Runway), SAG-AFTRA, caso Rainbow USA e o desenho atual do formulário, cujos campos o §8 revisa.
- `client_videos.json` (raiz do repositório) — origem da contagem de 534 vídeos, 46 marcas e 78 registros com nome próprio de pessoa.

---

### Ressalvas honestas

- **Não sou advogado e isto não é parecer.** As cláusulas dos §3, §6 e §7 são
  textos de trabalho construídos a partir dos requisitos legais conferidos na
  fonte. Precisam de revisão profissional antes de ir para um contrato.
- **A maior fragilidade desta pesquisa é a ausência da ANPD** (§9). Onde a
  posição oficial faltou, eu disse que faltou, em vez de preencher com
  suposição.
- **A jurisprudência brasileira sobre IA e direito de imagem é rasa.** Um caso,
  de segundo grau, processual. Qualquer afirmação categórica sobre "como os
  tribunais decidem" seria invenção. O que existe hoje é a aplicação da lei
  geral a uma tecnologia nova — com a incerteza que isso carrega.
- **O ponto mais acionável do documento não é jurídico, é operacional:** o
  briefing preenchido e arquivado responde, a favor dela, exatamente a pergunta
  que o TJSP disse que seria feita — *"se houve algum tipo de verificação
  prévia"*. Fazer as perguntas certas antes de orçar deixou de ser bom
  atendimento e virou defesa.
