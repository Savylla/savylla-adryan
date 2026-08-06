/* ========================================
   SAVYLLA ADRYAN - Portfolio Audiovisual
   ======================================== */

// ----------------------------------------
// Dados dos projetos (reais)
// ----------------------------------------
const projetos = [
  {
    id: 68,
    nome: "Garagem Coletiva",
    categoria: "video",
    categoriaLabel: "Direção + Filmmaker",
    ano: "2017 - 2020",
    videoId: "",
    descricao: "Direção e Filmmaker nos projetos audiovisuais da Coletiva Garagem. Idealizado como um coletivo de produção audiovisual feito por e para mulheres que amam mulheres.",
    ficha: {
      "Função": "Direção e Filmmaker",
      "Marca": "Garagem Coletiva",
      "Projeto": "Produções Audiovisuais",
      "Tipo": "Coletivo Audiovisual",
      "Ano": "2017 - 2020"
    },
    videos: [
      { url: "assets/projetos/garagem-coletiva/video-1.mp4", direcao: true, talento: "Tendinite" },
      { url: "assets/projetos/garagem-coletiva/video-2.mp4", direcao: true, talento: "Conchinha" },
      { url: "assets/projetos/garagem-coletiva/video-3.mp4", direcao: true, talento: "O que é ser lésbica?" },
      { youtubeId: "Wp7oNIgtDow", direcao: true, talento: "Na Madruga Boladona" },
      { url: "assets/projetos/garagem-coletiva/video-5.mp4", direcao: true, talento: "Isopormácio" },
      { url: "assets/projetos/garagem-coletiva/video-6.mp4", direcao: true, talento: "Presente de Aniversário" },
      { url: "assets/projetos/garagem-coletiva/video-7.mp4", direcao: true, talento: "Miami Beach Gay Pride" }
    ],
    youtube: "https://www.youtube.com/@ColetivaGaragem",
    instagram: "https://www.instagram.com/coletivagaragem/",
    facebook: "https://www.facebook.com/coletivagaragem",
    galeria: []
  },
  {
    id: 67,
    nome: "Devassas",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2020",
    videoId: "",
    descricao: "Filmmaker na Campanha de divulgação da nova linha de roupas e estampas Devassas.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Devassas",
      "Projeto": "Campanha Nova Linha de Roupas e Estampas",
      "Tipo": "Campanha de Divulgação",
      "Ano": "2020"
    },
    videos: [
      { url: "assets/projetos/devassas/video-1.mp4", talento: "Devassas - Video 1" },
      { url: "assets/projetos/devassas/video-2.mp4", talento: "Devassas - Video 2" },
      { url: "assets/projetos/devassas/video-3.mp4", talento: "Devassas - Video 3" }
    ],
    instagram: "https://www.instagram.com/devassascom/",
    facebook: "https://www.facebook.com/devassascom",
    galeria: [
      "assets/projetos/devassas/foto-1.avif",
      "assets/projetos/devassas/foto-2.avif",
      "assets/projetos/devassas/foto-3.avif",
      "assets/projetos/devassas/foto-4.avif"
    ]
  },
  {
    id: 1,
    nome: "Dua Lipa - Radical Optimism",
    categoria: "design",
    categoriaLabel: "Design",
    ano: "2024",
    videoId: "",
    descricao: "Produção do material para a campanha de divulgação e lançamento no Brasil do álbum Radical Optimism da Dua Lipa.",
    ficha: {
      "Função": "Designer",
      "Marca": "Warner Music UK",
      "Projeto": "Álbum Radical Optimism - Dua Lipa",
      "Tipo": "Campanha de Divulgação",
      "Ano": "2024"
    },
    instagram: "https://www.instagram.com/dualipa/",
    youtube: "https://www.youtube.com/channel/UC-J-KZfRV8c13fOCkhXdLiQ",
    spotify: "https://open.spotify.com/intl-pt/artist/6M2wZ9GZgrQXHCFfjv46we?si=QVgMvEh-SYyEnA-C-a2EOA&nd=1&dlsi=e2ed800ec44c49d8",
    facebook: "https://www.facebook.com/DuaLipa",
    galeria: [
      "assets/projetos/warner-uk/foto-1.avif",
      "assets/projetos/warner-uk/foto-2.avif"
    ]
  },
  {
    id: 59,
    nome: "Warner Music Group",
    categoria: "fotografia",
    categoriaLabel: "Fotografia",
    ano: "2023",
    videoId: "",
    descricao: "Cobertura fotográfica da confraternização de fim de ano da Warner Music Brasil.",
    ficha: {
      "Função": "Fotógrafo",
      "Marca": "Warner Music Brasil",
      "Projeto": "Confraternização 2023",
      "Tipo": "Cobertura Fotográfica",
      "Ano": "2023"
    },
    youtube: "https://www.youtube.com/@warnermusicbrasil",
    instagram: "https://www.instagram.com/warnermusicbr/",
    tiktok: "https://www.tiktok.com/@warnermusicbr",
    galeria: [
      "assets/projetos/warner-confraternizacao/capa.avif",
      "assets/projetos/warner-confraternizacao/foto-1.avif",
      "assets/projetos/warner-confraternizacao/foto-2.avif",
      "assets/projetos/warner-confraternizacao/foto-3.avif",
      "assets/projetos/warner-confraternizacao/foto-4.avif",
      "assets/projetos/warner-confraternizacao/foto-5.avif"
    ]
  },
  {
    id: 62,
    nome: "#OrgulhoNãoPara Ambev",
    categoria: "design",
    categoriaLabel: "Design",
    ano: "2020",
    videoId: "",
    descricao: "Campanha de arrecadação através de twittada, a Ambev doou 1 real a cada tweet com a hashtag #OrgulhoNãoPara às ONGs Casinha, Casa 1 e Casarão Brasil. Somei nas artes de divulgação do projeto.",
    ficha: {
      "Função": "Designer",
      "Marca": "Casinha Acolhida / Ambev",
      "Projeto": "#OrgulhoNãoPara",
      "Tipo": "Campanha de Divulgação",
      "Ano": "2020"
    },
    website: "https://www.ambev.com.br/",
    website2: "https://www.b9.com.br/128294/ambev-lanca-manifesto-orgulhonaopara-com-rostos-iconicos-da-comunidade-lgbtqia-brasileira/",
    galeria: [
      "assets/projetos/orgulho-nao-para/capa.avif",
      "assets/projetos/orgulho-nao-para/foto-1.avif",
      "assets/projetos/orgulho-nao-para/foto-2.jpg"
    ]
  },
  {
    id: 61,
    nome: "Doritos Rainbow",
    categoria: "design",
    categoriaLabel: "Design",
    ano: "2020",
    videoId: "",
    descricao: "Campanha de criação da maior corrente de beijos pela internet. Cada beijo virtual enviado no site, a DORITOS®️ Rainbow doou R$1 real. Com meta de chegar em 1 milhão de beijos e reais! Auxiliei nas artes de divulgação do projeto.",
    ficha: {
      "Função": "Designer",
      "Marca": "Casinha Acolhida / Doritos",
      "Projeto": "Doritos Rainbow - 1Kiss1Donation",
      "Tipo": "Campanha de Divulgação",
      "Ano": "2020"
    },
    website: "https://www.doritos.com/",
    instagram: "https://www.instagram.com/doritosbrasil/",
    website2: "https://www.b9.com.br/127601/doritos-rainbow-lanca-campanha-1kiss1donation-com-meta-de-1-milhao-de-beijos-virtuais/",
    galeria: [
      "assets/projetos/doritos-rainbow/capa.avif",
      "assets/projetos/doritos-rainbow/foto-1.avif",
      "assets/projetos/doritos-rainbow/foto-2.png",
      "assets/projetos/doritos-rainbow/foto-3.jpg"
    ]
  },
  {
    id: 65,
    nome: "Linha Produções",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2020",
    videoId: "",
    descricao: "Filmmaker na Websérie Encontro com 8 Episódios em exibição no YouTube.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Linha Produções",
      "Projeto": "Websérie Encontro",
      "Tipo": "Websérie",
      "Ano": "2020"
    },
    youtube: "https://www.youtube.com/@LinhaProducoes",
    instagram: "https://www.instagram.com/linhaproducoes/",
    facebook: "https://www.facebook.com/linhaproducoesrj",
    galeria: [
      "assets/projetos/linha-producoes/capa.avif",
      "assets/projetos/linha-producoes/foto-1.avif"
    ],
    youtubePlaylist: "PLg-0c_LTgwGGwAkGWjSbzWnPkBktzEpg5"
  },
  {
    id: 66,
    nome: "Força da Terra",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2016",
    videoId: "",
    descricao: "Filmmaker no comercial de comemoração aos 20 anos da marca.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Força da Terra",
      "Projeto": "Comercial 20 Anos",
      "Tipo": "Comercial",
      "Ano": "2016"
    },
    videos: [
      { url: "assets/projetos/forca-da-terra/forca-da-terra-20-anos.mp4", talento: "Força da Terra 20 Anos" }
    ],
    website: "https://www.forcadaterra.com.br/",
    instagram: "https://www.instagram.com/forcadaterra/",
    facebook: "https://www.facebook.com/ForcaDaTerraCosmeticos",
    galeria: []
  },
  {
    id: 64,
    nome: "Doutora Drag",
    categoria: "video",
    categoriaLabel: "Edição de Vídeo",
    ano: "2020 - 2022",
    videoId: "",
    descricao: "Responsável pela edição dos vídeos do canal do Youtube \"Doutora Drag\", no período de 21/08/2020 à 09/02/2022 realizados pela Dimitra Vulcana. Com os roteiros de Danilo Carreiro.",
    ficha: {
      "Função": "Editor de Vídeo",
      "Marca": "Doutora Drag",
      "Projeto": "Canal Doutora Drag",
      "Tipo": "Edição de Vídeo",
      "Ano": "2020 - 2022"
    },
    youtube: "https://www.youtube.com/@DoutoraDrag",
    instagram: "https://www.instagram.com/dimitravulcana2/",
    galeria: [
      "assets/projetos/doutora-drag/capa.avif",
      "assets/projetos/doutora-drag/foto-1.avif",
      "assets/projetos/doutora-drag/foto-2.avif"
    ],
    youtubeGaleria: [
      "wX8OEUe6C4E",
      "i86cm9xpcYs"
    ]
  },
  {
    id: 63,
    nome: "Apsa",
    categoria: "design",
    categoriaLabel: "Design",
    ano: "2020",
    videoId: "",
    descricao: "Elaboração de projetos audiovisuais junto à equipe da agência Imaginatto, criação da identidade visual para o Instagram e Youtube e elaboração estratégica dos conteúdos.",
    ficha: {
      "Função": "Designer / Produtor Audiovisual",
      "Marca": "Apsa",
      "Projeto": "Identidade Visual e Conteúdo",
      "Tipo": "Design e Produção Audiovisual",
      "Ano": "2020"
    },
    website: "https://apsa.com.br/",
    instagram: "https://www.instagram.com/oficialapsa/",
    facebook: "https://www.facebook.com/oficialapsa",
    youtube: "https://www.youtube.com/watch?v=QBwiT53yL-k",
    galeria: [
      "assets/projetos/apsa/foto-2.avif"
    ],
    youtubeGaleria: [
      "QBwiT53yL-k"
    ]
  },
  {
    id: 60,
    nome: "Casinha Acolhida",
    categoria: "design",
    categoriaLabel: "Coordenação de Arte",
    ano: "2019 - 2023",
    videoId: "",
    descricao: "Participei da equipe de criação de conteúdo e produção de materiais gráficos pelo período de 2019 à 2023 atuando em diversas vertentes dos projetos da ONG, junto aos demais voluntários.",
    ficha: {
      "Função": "Coordenador de Arte",
      "Marca": "Casinha Acolhida",
      "Projeto": "Criação de Conteúdo e Materiais Gráficos",
      "Tipo": "Coordenação de Arte",
      "Ano": "2019 - 2023"
    },
    website: "https://casinha.ong/a-casinha/",
    instagram: "https://www.instagram.com/casinhaacolhida/",
    facebook: "https://www.facebook.com/casinhaacolhida",
    linkedin: "https://www.linkedin.com/company/casinhaacolhida/posts/?feedView=all",
    galeria: [
      "assets/projetos/casinha-acolhida/capa.avif",
      "assets/projetos/casinha-acolhida/foto-1.avif",
      "assets/projetos/casinha-acolhida/foto-2.avif",
      "assets/projetos/casinha-acolhida/foto-3.avif",
      "assets/projetos/casinha-acolhida/artes-3.avif",
      "assets/projetos/casinha-acolhida/artes-6.avif",
      "assets/projetos/casinha-acolhida/artes-7.avif",
      "assets/projetos/casinha-acolhida/batalha-lipsync-2_edited.avif",
      "assets/projetos/casinha-acolhida/casinha-de-portas-abertas-2_edited.avif",
      "assets/projetos/casinha-acolhida/casinha-de-portas-abertas-3.avif",
      "assets/projetos/casinha-acolhida/casinha-festa-de-5-anos.avif",
      "assets/projetos/casinha-acolhida/casinha-festa-de-5-anos-1.avif",
      "assets/projetos/casinha-acolhida/casinha-festa-de-5-anos-2.avif",
      "assets/projetos/casinha-acolhida/casinha-festa-de-5-anos-3.avif",
      "assets/projetos/casinha-acolhida/3198ad_696e96b8941e4aa687e7c2e0b29fcfd8~mv2.avif",
      "assets/projetos/casinha-acolhida/3198ad_790b43bfffe0436a9a49fbea2feba699~mv2.avif",
      "assets/projetos/casinha-acolhida/3198ad_8f87d29683534b3ba978c88d555aee5a~mv2.avif",
      "assets/projetos/casinha-acolhida/trapezio-cultural-2.avif",
      "assets/projetos/casinha-acolhida/trapezio-cultural-3.avif"
    ]
  },
  {
    id: 2,
    nome: "Alma Festival",
    categoria: "fotografia",
    categoriaLabel: "Fotografia",
    ano: "2024",
    videoId: "",
    descricao: "Junto à 4Fly, realizei fotos da área VIP do Alma Festival.",
    ficha: {
      "Função": "Fotógrafo",
      "Parceria": "4Fly",
      "Tipo": "Cobertura Fotográfica",
      "Área": "VIP",
      "Ano": "2024"
    },
    instagram: "https://www.instagram.com/almafestivalbr/",
    website: "https://4fly.pixieset.com/alma130724/album6/",
    galeria: [
      "assets/projetos/alma-festival/Savylla-Alma-3.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-6.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-9.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-11.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-12.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-15.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-16.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-19.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-20.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-23.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-24.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-25.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-26.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-27.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-29.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-34.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-36.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-38.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-39.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-40.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-41.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-44.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-46.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-48.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-53.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-54.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-56.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-61.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-62.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-63.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-64.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-65.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-66.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-67.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-68.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-70.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-80.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-81.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-82.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-85.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-90.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-92.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-93.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-95.jpg",
      "assets/projetos/alma-festival/Savylla-Alma-99.jpg"
    ]
  },
  {
    id: 3,
    nome: "Acampamento do Medo 1",
    categoria: "fotografia",
    categoriaLabel: "Fotografia + Edição",
    ano: "2024",
    videoId: "",
    descricao: "Captação e edição fotográfica do Making Of e material de divulgação da série Acampamento do Medo 1 para o canal do YouTube dos Irmãos Scribel.",
    ficha: {
      "Função": "Fotógrafo + Editor",
      "Marca": "Irmãos Scribel",
      "Projeto": "Acampamento do Medo 1",
      "Tipo": "Making Of + Divulgação",
      "Plataforma": "YouTube",
      "Ano": "2024"
    },
    instagram: "https://www.instagram.com/viniciusscribel/",
    instagram2: "https://www.instagram.com/gabrielscribel/",
    youtube: "https://www.youtube.com/c/Irm%C3%A3osScribel",
    youtubeVideo: "https://www.youtube.com/watch?v=CXS_WAV1x2g",
    tiktok: "https://www.tiktok.com/@irmaosscribel",
    galeria: [
      "assets/projetos/acampamento-medo-1/foto-1.avif",
      "assets/projetos/acampamento-medo-1/foto-2.avif",
      "assets/projetos/acampamento-medo-1/foto-3.avif",
      "assets/projetos/acampamento-medo-1/foto-4.avif",
      "assets/projetos/acampamento-medo-1/foto-5.avif"
    ]
  },
  {
    id: 58,
    nome: "Acampamento do Medo 2",
    categoria: "fotografia",
    categoriaLabel: "Fotografia + Edição",
    ano: "2024",
    videoId: "",
    descricao: "Captação e edição fotográfica do Making Of e material de divulgação do filme Acampamento do Medo 2 para o canal do YouTube dos Irmãos Scribel.",
    ficha: {
      "Função": "Fotógrafo + Editor",
      "Marca": "Irmãos Scribel",
      "Projeto": "Acampamento do Medo 2",
      "Tipo": "Making Of + Divulgação",
      "Plataforma": "YouTube",
      "Ano": "2024"
    },
    instagram: "https://www.instagram.com/viniciusscribel/",
    instagram2: "https://www.instagram.com/gabrielscribel/",
    youtube: "https://www.youtube.com/c/Irm%C3%A3osScribel",
    youtubeVideo: "https://www.youtube.com/watch?v=ZSXp56GNEc8",
    tiktok: "https://www.tiktok.com/@irmaosscribel",
    galeria: [
      "assets/projetos/acampamento-medo-2/foto-1.avif",
      "assets/projetos/acampamento-medo-2/foto-2.avif",
      "assets/projetos/acampamento-medo-2/foto-3.avif",
      "assets/projetos/acampamento-medo-2/foto-4.avif",
      "assets/projetos/acampamento-medo-2/foto-5.avif",
      "assets/projetos/acampamento-medo-2/foto-6.avif",
      "assets/projetos/acampamento-medo-2/foto-7.avif"
    ]
  },
  {
    id: 5,
    nome: "ONG Casinha Acolhida",
    categoria: "design",
    categoriaLabel: "Coordenação de Arte",
    ano: "2019 - 2024",
    videoId: "",
    descricao: "Realização da criação e produção dos materiais gráficos e físicos das diversas vertentes dos projetos da ONG, junto aos demais voluntários.",
    ficha: {
      "Função": "Coordenador de Arte",
      "Marca": "ONG Casinha Acolhida",
      "Tipo": "Materiais Gráficos e Físicos",
      "Período": "2019 - 2024",
      "Formato": "Voluntariado"
    },
    galeria: [
      "assets/projetos/casinha-acolhida-1.jpg",
      "assets/projetos/casinha-acolhida-2.jpg",
      "assets/projetos/casinha-acolhida-3.jpg"
    ]
  },
  {
    id: 6,
    nome: "Dalla Cervejaria",
    categoria: "video",
    categoriaLabel: "Som + Produção",
    ano: "2023",
    videoId: "",
    descricao: "Comercial para a chegada da cerveja Dalla no RJ. Com a Direção, Captação e Edição de Mariana Godois.",
    ficha: {
      "Função": "Captação de Som + Assistência de Produção",
      "Marca": "Dalla Cervejaria",
      "Direção": "Mariana Godois",
      "Tipo": "Comercial",
      "Locação": "Rio de Janeiro, RJ",
      "Ano": "2023"
    },
    galeria: [
      "assets/projetos/dalla-1.jpg",
      "assets/projetos/dalla-2.jpg"
    ]
  },
  {
    id: 7,
    nome: "BRAX Sports Assets",
    categoria: "video",
    categoriaLabel: "Captação de Som",
    ano: "2023",
    videoId: "",
    descricao: "Conteúdo de divulgação para promover o camarote Maracã Prime no jogo do Brasileirão (Flamengo x Fortaleza), atendendo à BRAX. Com Direção, Captação e Edição de Mariana Godois. Fotografia de Thaty Aguiar.",
    ficha: {
      "Função": "Captação de Som",
      "Marca": "BRAX Sports Assets",
      "Projeto": "Camarote Maracã Prime",
      "Direção": "Mariana Godois",
      "Fotografia": "Thaty Aguiar",
      "Tipo": "Conteúdo de Divulgação",
      "Ano": "2023"
    },
    galeria: [
      "assets/projetos/brax-1.jpg",
      "assets/projetos/brax-2.jpg"
    ]
  },
  {
    id: 9,
    nome: "Teçá Arte e Cultura",
    categoria: "motion",
    categoriaLabel: "Edição de Vídeo",
    ano: "2023",
    videoId: "",
    descricao: "Produção de Reels no Instagram para uso como vitrine virtual, sendo vídeos comerciais de agradecimento aos apoiadores do espetáculo teatral.",
    ficha: {
      "Função": "Editor de Vídeo",
      "Marca": "Teçá - Arte e Cultura",
      "Tipo": "Reels / Conteúdo Social",
      "Plataforma": "Instagram",
      "Ano": "2023"
    },
    galeria: [
      "assets/projetos/teca-1.jpg",
      "assets/projetos/teca-2.jpg"
    ]
  },
  {
    id: 10,
    nome: "Espetáculo Entretenimento",
    categoria: "video",
    categoriaLabel: "Produção de Campo",
    ano: "2023",
    videoId: "",
    descricao: "Cobrindo o desfile da rainha de bateria Kelly Jorge (locutora da rádio Tupí), na nova Intendente Magalhães pela G.R.E.S. Sereno de Campo Grande. Executando pela equipe do empresário Raphael Almeida. Com a produção executiva da Camille Aboud. Criação de Mídia Kit da Kelly Jorge e arte para divulgação.",
    ficha: {
      "Função": "Produção de Campo + Design",
      "Marca": "Espetáculo Entretenimento",
      "Artista": "Kelly Jorge",
      "Produção Executiva": "Camille Aboud",
      "Empresário": "Raphael Almeida",
      "Tipo": "Cobertura + Mídia Kit",
      "Ano": "2023"
    },
    galeria: [
      "assets/projetos/espetaculo-1.jpg",
      "assets/projetos/espetaculo-2.jpg"
    ]
  },
  {
    id: 11,
    nome: "Imaginatto",
    categoria: "video",
    categoriaLabel: "Videomaker + Design",
    ano: "2020 - 2023",
    videoId: "",
    descricao: "Produção remota de projetos audiovisuais junto à equipe da agência, elaborando identidade visual para os projetos das marcas e tendo participação na execução estratégica dos conteúdos focados em resultados de engajamento.",
    ficha: {
      "Função": "Videomaker e Designer",
      "Marca": "Agência Imaginatto",
      "Tipo": "Produção Audiovisual + Identidade Visual",
      "Formato": "Remoto",
      "Período": "2020 - 2023"
    },
    galeria: [
      "assets/projetos/imaginatto-1.jpg",
      "assets/projetos/imaginatto-2.jpg",
      "assets/projetos/imaginatto-3.jpg"
    ]
  },
  {
    id: 12,
    nome: "Doutora Drag",
    categoria: "motion",
    categoriaLabel: "Edição + Motion",
    ano: "2021 - 2022",
    videoId: "",
    descricao: "Edição para o canal do YouTube \"Doutora Drag\", realizado pela Dimitra Vulcana. Com roteiros de Danilo Carreiro, sincronizando a edição aos vídeos de intérprete de libras. Criação de vinhetas e nova identidade visual do canal.",
    ficha: {
      "Função": "Editor de Vídeo + Motion Designer",
      "Marca": "Doutora Drag / Dimitra Vulcana",
      "Roteiro": "Danilo Carreiro",
      "Plataforma": "YouTube",
      "Tipo": "Edição + Vinhetas + ID Visual",
      "Período": "2021 - 2022"
    },
    galeria: [
      "assets/projetos/doutora-drag-1.jpg",
      "assets/projetos/doutora-drag-2.jpg",
      "assets/projetos/doutora-drag-3.jpg"
    ]
  },
  {
    id: 13,
    nome: "Imagem Integrada",
    categoria: "motion",
    categoriaLabel: "Videomaker + Motion + Design",
    ano: "2021",
    videoId: "",
    descricao: "Produção de material para divulgação da clínica na Barra da Tijuca (RJ), para as redes sociais do cliente. Captação, edição e motion do comercial. Criação da identidade visual para a clínica Imagem Integrada, com o objetivo de comunicar e realizar de uma melhor maneira o contato com seus clientes através dos meios digitais e físicos.",
    ficha: {
      "Função": "Videomaker + Motion Designer + Designer",
      "Marca": "Clínica Imagem Integrada",
      "Tipo": "Comercial + Identidade Visual",
      "Locação": "Barra da Tijuca, RJ",
      "Ano": "2021"
    },
    galeria: [
      "assets/projetos/imagem-integrada-1.jpg",
      "assets/projetos/imagem-integrada-2.jpg",
      "assets/projetos/imagem-integrada-3.jpg"
    ]
  },
  {
    id: 14,
    nome: "Linha Produções",
    categoria: "video",
    categoriaLabel: "Câmera + Motion",
    ano: "2020",
    videoId: "",
    descricao: "Websérie Encontro da Linha Produções com 8 episódios em exibição no YouTube.",
    ficha: {
      "Função": "Câmera + Motion + Masterização",
      "Marca": "Linha Produções",
      "Tipo": "Websérie",
      "Episódios": "8",
      "Plataforma": "YouTube",
      "Ano": "2020"
    },
    galeria: [
      "assets/projetos/linha-producoes-1.jpg",
      "assets/projetos/linha-producoes-2.jpg"
    ]
  },
  {
    id: 15,
    nome: "Força da Terra",
    categoria: "video",
    categoriaLabel: "Videomaker",
    ano: "2020",
    videoId: "",
    descricao: "Produção do comercial de comemoração aos 20 anos da empresa.",
    ficha: {
      "Função": "Videomaker",
      "Marca": "Força da Terra",
      "Tipo": "Comercial Institucional",
      "Motivo": "Comemoração 20 anos",
      "Ano": "2020"
    },
    galeria: [
      "assets/projetos/forca-terra-1.jpg",
      "assets/projetos/forca-terra-2.jpg"
    ]
  },
  {
    id: 16,
    nome: "Devassas",
    categoria: "video",
    categoriaLabel: "Produção + Edição",
    ano: "2020",
    videoId: "",
    descricao: "Campanha de divulgação da nova linha de roupas e estampas da Devassas. Fotografia de Victor Vieira.",
    ficha: {
      "Função": "Assistência de Produção + Edição de Vídeo",
      "Marca": "Devassas",
      "Fotografia": "Victor Vieira",
      "Tipo": "Campanha de Moda",
      "Ano": "2020"
    },
    galeria: [
      "assets/projetos/devassas-1.jpg",
      "assets/projetos/devassas-2.jpg"
    ]
  },
  {
    id: 17,
    nome: "Coletiva Garagem",
    categoria: "video",
    categoriaLabel: "Direção + Videomaker + Design",
    ano: "2018 - 2020",
    videoId: "",
    descricao: "Produção de vídeo e arte (captação e edição) para os projetos e redes sociais da Coletiva Garagem. Idealizado como um coletivo de produção audiovisual feito por e para mulheres que amam mulheres.",
    ficha: {
      "Função": "Direção + Videomaker + Motion + Design",
      "Marca": "Coletiva Garagem",
      "Tipo": "Produção Audiovisual + Arte",
      "Formato": "Vídeo + Design",
      "Período": "2018 - 2020"
    },
    galeria: [
      "assets/projetos/coletiva-garagem-1.jpg",
      "assets/projetos/coletiva-garagem-2.jpg",
      "assets/projetos/coletiva-garagem-3.jpg"
    ]
  },
  {
    id: 18,
    nome: "Drogasil",
    categoria: "video",
    categoriaLabel: "Filmmaker + Direção",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo para TikTok da Drogasil com diversos creators, incluindo Daniela Castelo, Débora Melo, Julia Helen, Larissa Venturini, Yago Capita, Andrei Lamberg, Murilo Amorim, Thays Godinho Ribeiro, Anny Melo e Quéren Hapuque. Ampla série de produções entre fevereiro e agosto de 2025.",
    ficha: {
      "Função": "Filmmaker + Direção",
      "Marca": "Drogasil",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Período": "Fev - Ago 2025"
    },
    videos: [
      { youtubeId: "5rciUtPVuL0", direcao: true, talento: "Daniela Castelo" },
      { youtubeId: "iSFowsarqrQ", talento: "Débora Melo" },
      { youtubeId: "CfLLQlnjgkg", talento: "Débora Melo" },
      { youtubeId: "C_1KwT9qjWo", talento: "Daniela Castelo" },
      { youtubeId: "tTeTbjNalJY", talento: "Frederico Volkmann" },
      { youtubeId: "DlqE5_TP6L0", talento: "Frederico Volkmann" },
      { youtubeId: "Pwqr0TFxOAo", direcao: true, talento: "Quézia Castro" },
      { youtubeId: "MSv7PkJwgvU", direcao: true, talento: "Quézia Castro" },
      { youtubeId: "HN4I6uBSLuY", talento: "Clara Giffoni" },
      { youtubeId: "9jKktlUZVqc", talento: "Julia Helen" },
      { youtubeId: "X4SLuPfPzlQ", talento: "Julia Helen" },
      { youtubeId: "JAsHoP3Y214", talento: "Julia Helen" },
      { youtubeId: "VwR9ksjnl0w", talento: "Julia Helen" },
      { youtubeId: "ThbjiI7GgVI", direcao: true, talento: "Larissa Venturini" },
      { youtubeId: "4Uofj7ZBmtw", direcao: true, talento: "Larissa Venturini" },
      { youtubeId: "3vt2ctF6ZBg", direcao: true, talento: "Larissa Venturini" },
      { youtubeId: "Oo5AF_iUASU", direcao: true, talento: "Larissa Venturini" },
      { youtubeId: "bCQmkH50a8s", talento: "Yago Capita" },
      { youtubeId: "VUx0Rxx0_no", talento: "Andrei Lamberg" },
      { youtubeId: "ZCgxHei4D6I", talento: "Andrei Lamberg" },
      { youtubeId: "tMDNOb91s1Q", talento: "Andrei Lamberg" },
      { youtubeId: "fopYpuObULw", talento: "Murilo Amorim" },
      { youtubeId: "UbxUor7dgD4", talento: "Murilo Amorim" },
      { youtubeId: "PNNXRIiaq5U", talento: "Murilo Amorim" },
      { youtubeId: "3vRmgWKQ-KI", talento: "Murilo Amorim" },
      { youtubeId: "wTgDYMoxXkY", talento: "Thays Godinho Ribeiro" },
      { youtubeId: "NVcXhACOIx4", talento: "Thays Godinho Ribeiro" },
      { youtubeId: "GbXPStW3ICo", talento: "Thays Godinho Ribeiro" },
      { youtubeId: "WID5OYWU8xY", talento: "Thays Godinho Ribeiro" },
      { youtubeId: "wV5lv_6-grk", talento: "Anny Melo" },
      { youtubeId: "BJvLyfX2h5A", talento: "Anny Melo" },
      { youtubeId: "n9aPlT6_KqE", direcao: true, talento: "Quéren Hapuque" },
      { youtubeId: "9bpjUvES1K4", talento: "Anny Melo" },
      { youtubeId: "zyTZ9ZawHDQ", talento: "Anny Melo" },
      { youtubeId: "WzLgP64ctkw", direcao: true, talento: "Quéren Hapuque" },
      { youtubeId: "nxfehOV9_vE", direcao: true, talento: "Quéren Hapuque" },
      { youtubeId: "an_wiA3e7mU", direcao: true, talento: "Quéren Hapuque" },
      { youtubeId: "73HEDSjMaq0", talento: "Lívia Lima" },
      { youtubeId: "-WnlPFEMdFg", talento: "Lívia Lima" },
      { youtubeId: "O_Y6-vdgDDY", talento: "Frederico Volkmann" },
      { youtubeId: "_aTr2OMEiPs", talento: "Lívia Lima" },
      { youtubeId: "dpBXykL1CRM", talento: "Frederico Volkmann" },
      { youtubeId: "y5_iDsHXKRE", talento: "Frederico Volkmann" },
      { youtubeId: "gexMpN0aSZE", talento: "Lívia Lima" },
      { youtubeId: "cZurkdSZDec", talento: "Frederico Volkmann" },
      { youtubeId: "W2SpYLt4d9A", talento: "Yago Capita" },
      { youtubeId: "OIC_kkT4u-o", talento: "Yago Capita" },
      { youtubeId: "GL8dWgbun18", talento: "Yago Capita" },
      { youtubeId: "tx2GDqTC7r4", talento: "Yago Capita" },
      { youtubeId: "k58aVMVH9Sw", talento: "Carolina Cruz" }
    ],
    galeria: []
  },
  {
    id: 19,
    nome: "Mercado Pago",
    categoria: "video",
    categoriaLabel: "Filmmaker + Direção",
    ano: "2025",
    videoId: "",
    descricao: "Projetos extensos de filmagem e direção de conteúdo para TikTok do Mercado Pago, com diversos talentos e creators. Produções realizadas entre março e outubro de 2025.",
    ficha: {
      "Função": "Filmmaker + Direção",
      "Marca": "Mercado Pago",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Período": "Mar - Out 2025"
    },
    videos: [
      { youtubeId: "dxdNxe9Zzg4", direcao: true, talento: "Nalu Moura" },
      { youtubeId: "9iCdW6UJc-o", direcao: true, talento: "Nalu Moura" },
      { youtubeId: "zxeRSTxanAY", talento: "Nalu Moura" },
      { youtubeId: "d0qnoEjHgOM", talento: "Daniela Castelo" },
      { youtubeId: "m4u72jlB-Tw", talento: "Daniela Castelo" },
      { youtubeId: "-o7dERVmDUA", talento: "Daniela Castelo" },
      { youtubeId: "lXiBZ6NHzHM", talento: "Daniela Castelo" },
      { youtubeId: "ckrM_e-58Zs", direcao: true, talento: "Raphael Monteiro" },
      { youtubeId: "vEAYovMcRnM", talento: "Raphael Monteiro" },
      { youtubeId: "DoWeEwO9Eb8", talento: "Raphael Monteiro" },
      { youtubeId: "F4qxnn5gmHM", talento: "Raphael Monteiro" },
      { youtubeId: "FgF_fDoVYXk", talento: "Maria Souza" },
      { youtubeId: "W3cPrLIoQms", talento: "João Mendes" },
      { youtubeId: "og-ujl2b2X4", talento: "Maria Souza" },
      { youtubeId: "vVuiNZk6zKc", talento: "Maria Souza" },
      { youtubeId: "bMkx1BOe44U", talento: "João Mendes" },
      { youtubeId: "sYB5NegUsbk", talento: "João Mendes" },
      { youtubeId: "mKAlH0IPnYs", talento: "João Mendes" },
      { youtubeId: "hvzXSqK7ysk", talento: "Maria Souza" },
      { youtubeId: "oE_jYqTHzAU", talento: "Loretta Martins" },
      { youtubeId: "cBGTodEPCuU", talento: "Loretta Martins" },
      { youtubeId: "XuL7wexZg6g", talento: "Loretta Martins" },
      { youtubeId: "v6esQrHSqlU", talento: "Loretta Martins" },
      { youtubeId: "ez-at7lP7HY", talento: "Frederico Volkmann" },
      { youtubeId: "yVjto8K7BqQ", talento: "Frederico Volkmann" },
      { youtubeId: "RWnOjv4W9po", talento: "Frederico Volkmann" },
      { youtubeId: "TTP5YQles-k", talento: "Frederico Volkmann" },
      { youtubeId: "z490SYGwyBE", talento: "Renan Teiva" },
      { youtubeId: "rI1Avy1hz1c", talento: "Renan Teiva" },
      { youtubeId: "bhDld0yNZUw", talento: "Renan Teiva" },
      { youtubeId: "jInRNm1CRSw", talento: "Renan Teiva" },
      { youtubeId: "Od1BqBgoJ9c", talento: "Vitória Rodrigues" },
      { youtubeId: "6xUcrJaAO10", talento: "Raphael Monteiro" },
      { youtubeId: "mO27JR1aYGw", talento: "Raphael Monteiro" },
      { youtubeId: "0T9tXKLZG2I", talento: "Vitória Rodrigues" },
      { youtubeId: "dFBLa-oVYV0", talento: "Raphael Monteiro" },
      { youtubeId: "SfxQcOjKLU4", talento: "Vitória Rodrigues" },
      { youtubeId: "izoH41Te-Vw", talento: "Vitória Rodrigues" },
      { youtubeId: "xDe-4vMFMGM", talento: "Antônio Bastos" },
      { youtubeId: "-NSvoAL99pM", talento: "Marcelo Klein" },
      { youtubeId: "cwhzu-foUs0", talento: "Marcelo Klein" },
      { youtubeId: "NT3ixIxn9Fc", talento: "Antônio Bastos" },
      { youtubeId: "Y3Ha-wHWAiA", talento: "Antônio Bastos" },
      { youtubeId: "0UvgfcS8l34", talento: "Marcelo Klein" },
      { youtubeId: "TtfjanvFocw", talento: "Marcelo Klein" },
      { youtubeId: "ratqvzQX73Y", talento: "Antônio Bastos" },
      { youtubeId: "CVmumik2hnw", talento: "Daniela Castelo" },
      { youtubeId: "Mh_TPDkDH70", talento: "André Lemos" }
    ],
    galeria: []
  },
  {
    id: 20,
    nome: "Magazine Luiza",
    categoria: "video",
    categoriaLabel: "Filmmaker + Direção",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo para TikTok da Magazine Luiza, atendendo a campanhas de divulgação com múltiplos creators.",
    ficha: {
      "Função": "Filmmaker + Direção",
      "Marca": "Magazine Luiza",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "-f56zYQ3fDA", talento: "Letícia Machado" },
      { youtubeId: "6ZMZNKIWJ4c", direcao: true, talento: "Karol Alves" },
      { youtubeId: "Aq1O9dt5xWI", direcao: true, talento: "Julia Helen" },
      { youtubeId: "nmyY1x5cS_Y", direcao: true, talento: "Karol Alves" },
      { youtubeId: "o38LV90mbXA", direcao: true, talento: "Julia Helen" },
      { youtubeId: "ukGK-l6WyMU", direcao: true, talento: "Drico Alves" },
      { youtubeId: "Yzyqr_sNQNk", direcao: true, talento: "Drico Alves" },
      { youtubeId: "KVFNqq-0B6M", talento: "Drico Alves" },
      { youtubeId: "GQn-bgQy1XU", talento: "Samia Abreu" },
      { youtubeId: "uyJf71ov1Uo", talento: "Drico Alves" },
      { youtubeId: "NzpLW_es2JA", talento: "Samia Abreu" },
      { youtubeId: "k3ozkk3OZVM", talento: "Pedro Pires" },
      { youtubeId: "LoOTy7du6Iw", direcao: true, talento: "Bruna Noronha" },
      { youtubeId: "7Z1O-UByi_M", direcao: true, talento: "Bruna Noronha" },
      { youtubeId: "OqvXQHW-CTs", direcao: true, talento: "Bruna Noronha" },
      { youtubeId: "0PY15VxyeTU", direcao: true, talento: "Bruna Noronha" },
      { youtubeId: "5jbZ5utFLyY", talento: "Lara Gay" },
      { youtubeId: "d2t2Pi6X0XQ", talento: "Lara Gay" },
      { youtubeId: "WQqyTjkW67I", talento: "Lara Gay" },
      { youtubeId: "3-hSdScDuqM", talento: "Lara Gay" },
      { youtubeId: "cFIjWD32UB0", talento: "Quéren Hapuque" },
      { youtubeId: "872RY8rhtxw", talento: "Quéren Hapuque" },
      { youtubeId: "vPQww1qTQrs", talento: "Quéren Hapuque" },
      { youtubeId: "yDUXW76PUmk", talento: "Lara Gay" },
      { youtubeId: "aQG2M8aLwfA", talento: "Lara Gay" },
      { youtubeId: "ugzawOFiRLg", talento: "Lara Gay" },
      { youtubeId: "nrWPZMy85Ys", talento: "Lara Gay" },
      { youtubeId: "7G_XcintAnE", talento: "Lara Gay" },
      { youtubeId: "GbRmuDDoU9M", talento: "Lara Gay" },
      { youtubeId: "KS0rgWmvGzc", talento: "Lara Gay" },
      { youtubeId: "g-MEwRKpeT4", talento: "Lara Gay" }
    ],
    galeria: []
  },
  {
    id: 21,
    nome: "Raia",
    categoria: "video",
    categoriaLabel: "Filmmaker + Direção",
    ano: "2025",
    videoId: "",
    descricao: "Campanhas de conteúdo para TikTok da Raia com múltiplos criadores de conteúdo, entre março e agosto de 2025.",
    ficha: {
      "Função": "Filmmaker + Direção",
      "Marca": "Raia",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Período": "Mar - Ago 2025"
    },
    videos: [
      { youtubeId: "NEHleVfNaZQ", talento: "Loretta Martins" },
      { youtubeId: "Hef2F2YkWBY", talento: "Loretta Martins" },
      { youtubeId: "dmVpaBDXIqI", talento: "Frederico Volkmann" },
      { youtubeId: "bxIgQU1I9RE", talento: "Frederico Volkmann" },
      { youtubeId: "2dy78GzXYmI", direcao: true, talento: "Quézia Castro" },
      { youtubeId: "etwKYRii-PQ", direcao: true, talento: "Quézia Castro" },
      { youtubeId: "1joTeMnRzns", talento: "Ana Claudia Padilha" },
      { youtubeId: "PExvD8hVBlQ", talento: "Clara Giffoni" },
      { youtubeId: "gY-Qb8YOP1A", direcao: true, talento: "Frederico Volkmann" },
      { youtubeId: "STDiMaj-5hE", direcao: true, talento: "Frederico Volkmann" },
      { youtubeId: "433JzW9eKY0", direcao: true, talento: "Frederico Volkmann" },
      { youtubeId: "IsYjN2K7zkw", direcao: true, talento: "Frederico Volkmann" },
      { youtubeId: "3u9MuBy1MA8", talento: "Clara Giffoni" },
      { youtubeId: "LgtyB5yGwk0", direcao: true, talento: "Quézia Castro" },
      { youtubeId: "3JxtXPL1IkQ", direcao: true, talento: "Quézia Castro" },
      { youtubeId: "NrwwmOnYfUk", direcao: true, talento: "Quézia Castro" },
      { youtubeId: "9Kc2cyKRb7Q", direcao: true, talento: "Quézia Castro" },
      { youtubeId: "kGZHDLwl_5E", direcao: true, talento: "Frederico Volkmann" },
      { youtubeId: "E4wm7LWDHGA", direcao: true, talento: "Frederico Volkmann" },
      { youtubeId: "rEGK16dni-8", talento: "Frederico Volkmann" },
      { youtubeId: "kW0yqcZoiMs", direcao: true, talento: "Carol Gomes" },
      { youtubeId: "4gqaftd-Wno", talento: "Carol Gomes" },
      { youtubeId: "1Ptzf4q0f-0", talento: "Carol Gomes" },
      { youtubeId: "-m7qP5pd9xQ", talento: "Carol Gomes" },
      { youtubeId: "-SiLgbLMipY", talento: "Carolina Malagutti" },
      { youtubeId: "IdynLiO1-Dk", talento: "Carolina Malagutti" },
      { youtubeId: "879bcwYfPKg", talento: "Carolina Malagutti" },
      { youtubeId: "metF5HqeBy0", talento: "Carolina Malagutti" },
      { youtubeId: "DVo5UwG7zSU", talento: "Loretta Martins" },
      { youtubeId: "oSLYs1TB22A", talento: "Mariana Braga" },
      { youtubeId: "ZUQlSJj1fAE", talento: "Mariana Braga" },
      { youtubeId: "THQYuflaSYU", talento: "Mariana Braga" },
      { youtubeId: "PYQ-HQhlDFU", talento: "Andrei Lamberg" },
      { youtubeId: "3tsSZqYuNlQ", talento: "Mariana Braga" },
      { youtubeId: "9Bu4B6Vjcns", talento: "Julia Nogueira" },
      { youtubeId: "K-FR4hVqPRc", talento: "Julia Nogueira" },
      { youtubeId: "ud2cfUj3zzk", talento: "Rodrigo Rabello" },
      { youtubeId: "skn_frmGPg4", talento: "Rodrigo Rabello" },
      { youtubeId: "pipzmvZqiuU", talento: "Julia Nogueira" },
      { youtubeId: "mGz7jWVNDqw", talento: "Julia Nogueira" },
      { youtubeId: "QBQx_zq-m6w", talento: "Julia Nogueira" },
      { youtubeId: "13_ulJahCIA", talento: "Rodrigo Rabello" },
      { youtubeId: "6NqxW-978Y4", talento: "Rodrigo Rabello" },
      { youtubeId: "KnAVcVZXizM", talento: "Gabriel Peregrino" },
      { youtubeId: "3ZK9KNnVUuE", talento: "Karol Alves" },
      { youtubeId: "udU_zSYwp38", talento: "Gabriel Peregrino" },
      { youtubeId: "Wv1lnqe9b94", talento: "Karol Alves" },
      { youtubeId: "KkDAblY2_qM", talento: "Karol Alves" },
      { youtubeId: "Pa63ewjV_Ig", talento: "Gabriel Peregrino" },
      { youtubeId: "VJFGHtAWCWQ", talento: "Karol Alves" },
      { youtubeId: "58ygYoOz_y4", talento: "Gabriel Peregrino" },
      { youtubeId: "PfB7avwrrAs", talento: "Ismael Gotthardi" },
      { youtubeId: "P8DqRIRCrPE", talento: "Júlia Horta" },
      { youtubeId: "ga8O04wMf40", talento: "Ismael Gotthardi" },
      { youtubeId: "VcvxRWe8mkI", talento: "Júlia Horta" },
      { youtubeId: "4vFmVzr2fyM", talento: "Ismael Gotthardi" },
      { youtubeId: "KfAy2GJmw0I", talento: "Ismael Gotthardi" },
      { youtubeId: "69XENhu2ZLQ", talento: "Júlia Horta" },
      { youtubeId: "BVxlxR_CRKc", talento: "Júlia Horta" },
      { youtubeId: "JbdzrKKP6Qw", talento: "Lara Gay" },
      { youtubeId: "bM1w0WL-N4I", talento: "Lara Gay" },
      { youtubeId: "oOh-g3OiCWo", talento: "Lara Gay" },
      { youtubeId: "yypqTjCPpfs", talento: "Lara Gay" },
      { youtubeId: "DWEWlJZtEUY", talento: "Clara Giffoni" }
    ],
    galeria: []
  },
  {
    id: 22,
    nome: "Bradesco",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas digitais do Bradesco em plataforma TikTok.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Bradesco",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "M17yhOXbkcU", talento: "Pedro Zurawski" },
      { youtubeId: "I1PYDVfc2A4", talento: "Pedro Zurawski" },
      { youtubeId: "DDXT9lkQUK4", talento: "Pedro Zurawski" },
      { youtubeId: "1NCpqO2JDYA", talento: "Pedro Zurawski" },
      { youtubeId: "xiM6_X6yALw", talento: "Jorge Hissa" },
      { youtubeId: "EJCbUlPcEsw", talento: "Jorge Hissa" },
      { youtubeId: "R_eMeHFFFVM", talento: "Jorge Hissa" },
      { youtubeId: "UdgJsE0Lyu0", talento: "Pedro Ruivo" },
      { youtubeId: "2t6zKJiidyo", talento: "Jorge Hissa" },
      { youtubeId: "7F-XTs7O2VE", talento: "Pedro Ruivo" },
      { youtubeId: "SDL5JRfZU9o", talento: "Pedro Ruivo" }
    ],
    galeria: []
  },
  {
    id: 23,
    nome: "Netshoes",
    categoria: "video",
    categoriaLabel: "Filmmaker + Direção",
    ano: "2025",
    videoId: "",
    descricao: "Filmagem de conteúdo para TikTok da Netshoes com diversos talentos e creators.",
    ficha: {
      "Função": "Filmmaker + Direção",
      "Marca": "Netshoes",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "euSotih5hqs", direcao: true, talento: "Adam Pereira" },
      { youtubeId: "UOhP1uIfD3k", direcao: true, talento: "Lívia Lima" },
      { youtubeId: "7zsuUDj6fws", talento: "Mariana Braga" },
      { youtubeId: "TKbhu1ePwgA", talento: "Mariana Braga" },
      { youtubeId: "ph6-fETnA7g", talento: "Mariana Braga" },
      { youtubeId: "VX3XeDdLe4A", talento: "Mariana Braga" },
      { youtubeId: "2v7iO26xlTA", direcao: true, talento: "Ana Claudia Padilha" },
      { youtubeId: "ZkgDj_WIA8Y", direcao: true, talento: "Ana Claudia Padilha" },
      { youtubeId: "I5QmoGohwPI", direcao: true, talento: "Ana Claudia Padilha" },
      { youtubeId: "pI1O5y1Mxps", direcao: true, talento: "Ana Claudia Padilha" },
      { youtubeId: "5rYCACBOAYY", talento: "Frederico Volkmann" },
      { youtubeId: "vC3ObmufVpo", talento: "Frederico Volkmann" },
      { youtubeId: "uH4KK0HTjHI", talento: "Frederico Volkmann" },
      { youtubeId: "I3OYnOGyxJs", talento: "Frederico Volkmann" }
    ],
    galeria: []
  },
  {
    id: 24,
    nome: "LG",
    categoria: "video",
    categoriaLabel: "Filmmaker + Direção",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da LG em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker + Direção",
      "Marca": "LG",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "6HhYfAefd88", direcao: true, talento: "Karol Alves" },
      { youtubeId: "l5PiIUoa8Is", talento: "Clara Giffoni" },
      { youtubeId: "otPsDTAN-iM", direcao: true, talento: "Karol Alves" },
      { youtubeId: "36jEg7uyN4g", direcao: true, talento: "Karol Alves" },
      { youtubeId: "topA6s23vLk", direcao: true, talento: "Karol Alves" }
    ],
    galeria: []
  },
  {
    id: 25,
    nome: "Uber",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Conteúdo audiovisual para campanhas digitais da Uber em TikTok.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Uber",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "ZT8eawnV8p4", talento: "Juliana Da Silva" },
      { youtubeId: "P6SkAXCI41g", talento: "Juliana Da Silva" },
      { youtubeId: "zTDNCe8lSjs", talento: "Quéren Hapuque" },
      { youtubeId: "Y7AiWpRCHcA", talento: "Quéren Hapuque" },
      { youtubeId: "MvX5EXOkXqg", talento: "Quéren Hapuque" },
      { youtubeId: "ntZ5FZcphzM", talento: "Quéren Hapuque" }
    ],
    galeria: []
  },
  {
    id: 26,
    nome: "Carolina Herrera",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para a marca Carolina Herrera em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Carolina Herrera",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "S0j8u7mk5m0", talento: "Khiara" },
      { youtubeId: "qLu3vudI7As", talento: "Drico Alves" },
      { youtubeId: "7ASm4zJXidk", talento: "Diogo Malta" },
      { youtubeId: "cF1syOFPE7M", talento: "Diogo Malta" }
    ],
    galeria: []
  },
  {
    id: 27,
    nome: "Nestlé",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo para campanhas da Nestlé em plataformas de redes sociais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Nestlé",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais / Exibido no Cinema",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "RQiKHx6hAmI", talento: "Lucas Leal Souza" },
      { youtubeId: "zJKsB2zMy58", talento: "Lucas Leal Souza" },
      { youtubeId: "bAM16jswkMg", talento: "Lucas Leal Souza" },
      { youtubeId: "K9r_trZzBJ8", talento: "Alessandro Cerqueira" },
      { youtubeId: "YG6fXxkGmdM", talento: "Alessandro Cerqueira" },
      { youtubeId: "Zyl1AMK-wHs", talento: "Tati Infante" },
      { youtubeId: "6HoHOCyhWf4", talento: "Tati Infante" }
    ],
    galeria: []
  },
  {
    id: 28,
    nome: "Philips",
    categoria: "video",
    categoriaLabel: "Filmmaker + Direção",
    ano: "2025",
    videoId: "",
    descricao: "Conteúdo audiovisual para campanhas digitais da Philips em TikTok.",
    ficha: {
      "Função": "Filmmaker + Direção",
      "Marca": "Philips",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "TMiHks55BgA", direcao: true, talento: "Luiza Veloso" },
      { youtubeId: "OdCiyIQH-rE", direcao: true, talento: "Luiza Veloso" },
      { youtubeId: "rtLXU60r4Qc", talento: "Rodrigo Rabello" },
      { youtubeId: "8PUTeD8Aj5U", talento: "Rodrigo Rabello" }
    ],
    galeria: []
  },
  {
    id: 29,
    nome: "Intimus",
    categoria: "video",
    categoriaLabel: "Filmmaker + Direção",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Intimus - Creative Incubator em TikTok.",
    ficha: {
      "Função": "Filmmaker + Direção",
      "Marca": "Intimus",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Creative Incubator",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "Xn5h4xDTY6g", direcao: true, talento: "Maria Luíza Kropotoff" },
      { youtubeId: "tL6MSoLIWPs", direcao: true, talento: "Maria Luíza Kropotoff" }
    ],
    galeria: []
  },
  {
    id: 30,
    nome: "Domino's",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Domino's em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Domino's",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "o0mx1oSki2k", talento: "Jorge Hissa" },
      { youtubeId: "pNVspyGAHms", talento: "Jorge Hissa" },
      { youtubeId: "Pe50lqGN3zw", talento: "Jorge Hissa" },
      { youtubeId: "TqrsjTIEqhY", talento: "Jorge Hissa" },
      { youtubeId: "7C1QEG2m29k", talento: "Jorge Hissa" },
      { youtubeId: "NgqudglKjYY", talento: "Jorge Hissa" },
      { youtubeId: "7XygUZFTdI8", talento: "Jorge Hissa" },
      { youtubeId: "jmZ7Uab2hpY", talento: "Jorge Hissa" }
    ],
    galeria: []
  },
  {
    id: 31,
    nome: "Serasa",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Serasa em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Serasa",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "FK1GiTPrnt4", talento: "Raphael Monteiro" },
      { youtubeId: "rprRW3ReCoo", talento: "Raphael Monteiro" },
      { youtubeId: "1-VmKHjpzfs", talento: "Raphael Monteiro" },
      { youtubeId: "iBLVYhc1lNQ", talento: "Raphael Monteiro" },
      { youtubeId: "LJs7g6_08vs", talento: "Débora Melo" },
      { youtubeId: "9xypUfGo5nE", talento: "Débora Melo" },
      { youtubeId: "cfWFu7zlyFQ", talento: "Débora Melo" },
      { youtubeId: "ISe7rscHKVw", talento: "Débora Melo" },
      { youtubeId: "aJYINzKnweI", talento: "Quéren Hapuque" },
      { youtubeId: "gbVcmDSMZ90", talento: "Quéren Hapuque" },
      { youtubeId: "Tu1D2ugM_mA", talento: "Quéren Hapuque" },
      { youtubeId: "uqw2XmN7Vjw", talento: "Quéren Hapuque" }
    ],
    galeria: []
  },
  {
    id: 32,
    nome: "Movida",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Movida em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Movida",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "3yGiT5qdrys", talento: "Marcelo Klein" },
      { youtubeId: "JsT9oAogP4o", talento: "Marcelo Klein" },
      { youtubeId: "CD0-WI3Cl6Q", talento: "Marcelo Klein" },
      { youtubeId: "IxfzC-BVmVA", talento: "Clara Giffoni" },
      { youtubeId: "cdVMwx2pjwQ", talento: "Clara Giffoni" },
      { youtubeId: "fjBwFzbjzgw", talento: "Marcelo Klein" },
      { youtubeId: "1vJz6i2Oysw", talento: "Clara Giffoni" },
      { youtubeId: "8zVNOrVPzZs", talento: "Clara Giffoni" }
    ],
    galeria: []
  },
  {
    id: 33,
    nome: "KaBuM!",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas do KaBuM! em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "KaBuM!",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "49QCUcSAKuA", talento: "Lara Gay" },
      { youtubeId: "Y6SqHlpv3RM", talento: "Lara Gay" },
      { youtubeId: "MURgCVfDNbg", talento: "Lara Gay" },
      { youtubeId: "l_NFuiXX8Hs", talento: "Lara Gay" }
    ],
    galeria: []
  },
  {
    id: 34,
    nome: "Neo Energia",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Neo Energia em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Neo Energia",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "HrIE4gV11jA", talento: "Ismael Gotthardi" },
      { youtubeId: "53jQhy1RTXA", talento: "Ismael Gotthardi" },
      { youtubeId: "RQUdYKJSFD4", talento: "Ismael Gotthardi" },
      { youtubeId: "TGVVJxBPTHQ", talento: "Ismael Gotthardi" },
      { youtubeId: "U79hizyMLaM", talento: "Júlia Horta" },
      { youtubeId: "4x6q0joaIvc", talento: "Júlia Horta" },
      { youtubeId: "PVuKOKW0TMw", talento: "Júlia Horta" },
      { youtubeId: "bL1QKnbPACg", talento: "Júlia Horta" },
      { youtubeId: "2JwwXfYXo4k", talento: "Hannah Beatriz" },
      { youtubeId: "p6FXXTSpL0E", talento: "Hannah Beatriz" }
    ],
    galeria: []
  },
  {
    id: 35,
    nome: "Claro",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Claro em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Claro",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "WQKvY6xmOhs", talento: "Nalu Moura" },
      { youtubeId: "RzaWv1-lxQ0", talento: "Vinicius Scribel" },
      { youtubeId: "Hl5U6xSQ-o0", talento: "Vinicius Scribel" },
      { youtubeId: "TNwbZRTjOZI", talento: "Vinicius Scribel" },
      { youtubeId: "OTFYJYOT2Uo", talento: "Vinicius Scribel" }
    ],
    galeria: []
  },
  {
    id: 36,
    nome: "Vans",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Vans em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Vans",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "GMGoiJaMvo4", talento: "Jasmim Avelino" },
      { youtubeId: "UMCTBg0Aog0", talento: "Jasmim Avelino" },
      { youtubeId: "HoHtVzNKMMY", talento: "Jasmim Avelino" },
      { youtubeId: "IV1yjTzWiUI", talento: "Jasmim Avelino" }
    ],
    galeria: []
  },
  {
    id: 37,
    nome: "Bet Nacional",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Bet Nacional em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Bet Nacional",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "V1j8_wTIHJM", talento: "Wesley Jesus" },
      { youtubeId: "BBOBwlA6fF0", talento: "Wesley Jesus" }
    ],
    galeria: []
  },
  {
    id: 38,
    nome: "Bravecto",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Bravecto em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Bravecto",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "lH-SgFOGpJY", talento: "Cachorro - Yago" },
      { youtubeId: "8DOQ9eNbuGU", talento: "Ígor Arvelos" },
      { youtubeId: "iXMJt6yicoE", talento: "Whisky - Yago" },
      { youtubeId: "DrcgiaJ2K6o", talento: "Loretta Martins" },
      { youtubeId: "L9DDlLiVsqc", talento: "Loretta Martins" },
      { youtubeId: "vR6PoRlKxO4", talento: "Jorge Hissa" },
      { youtubeId: "7s8ah4HarJI", talento: "Cachorro - Yago" },
      { youtubeId: "rvWxO415PTw", talento: "Cachorro - Yago" },
      { youtubeId: "P0qRbPVlkcY", talento: "Loretta Martins" },
      { youtubeId: "y_DVjSTJGkA", talento: "Loretta Martins" },
      { youtubeId: "C8LcFan2gAs", talento: "Jorge Hissa" }
    ],
    galeria: []
  },
  {
    id: 39,
    nome: "Carrefour",
    categoria: "video",
    categoriaLabel: "Filmmaker + Direção",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas do Carrefour em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker + Direção",
      "Marca": "Carrefour",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2026"
    },
    videos: [
      { youtubeId: "d8HKRjdFRY8", direcao: true, talento: "Ismael Gotthardi" },
      { youtubeId: "DWJ4yAtYNoQ", direcao: true, talento: "Ismael Gotthardi" },
      { youtubeId: "nXS3De32PSY", direcao: true, talento: "Quézia Castro" }
    ],
    galeria: []
  },
  {
    id: 69,
    nome: "Oscar 2026",
    categoria: "ia",
    categoriaLabel: "Produção com IA",
    ano: "2026",
    videoId: "",
    descricao: "E se sua equipe fosse um filme, qual seria? Ana, founder da Allfluence, apresenta sua equipe fazendo uma analogia com o tema Oscar 2026.",
    ficha: {
      "Função": "Produção com IA",
      "Marca": "Allfluence",
      "Projeto": "Oscar 2026",
      "Tipo": "Conteúdo com IA",
      "Ano": "2026"
    },
    instagram: "https://www.instagram.com/allfluence/",
    website: "https://www.allfluence.com.br/",
    videos: [
      { url: "assets/projetos/oscar/video-1.mp4", talento: "Oscar 2026 - Produção com IA" }
    ],
    galeria: []
  },
  {
    id: 70,
    nome: "Teste de Fluxo",
    categoria: "ia",
    categoriaLabel: "Produção com IA",
    ano: "2025",
    videoId: "",
    descricao: "Teste de fluxo usando o Nano Banana + VEO3. Projeto pessoal de experimentação com ferramentas de IA generativa para criação de vídeo.",
    ficha: {
      "Função": "Produção com IA",
      "Ferramentas": "Nano Banana + VEO3",
      "Tipo": "Projeto Pessoal",
      "Ano": "2025"
    },
    videos: [
      { url: "assets/projetos/ia-projeto-1/video.mp4", talento: "Teste de Fluxo - Nano Banana + VEO3" }
    ],
    galeria: []
  },
  {
    id: 71,
    nome: "Dentro da Minha Cabeça",
    categoria: "ia",
    categoriaLabel: "Produção com IA",
    ano: "2025",
    videoId: "",
    descricao: "Projeto pessoal explorando ferramentas no Higgsfield",
    ficha: {
      "Função": "Produção com IA",
      "Ferramentas": "Higgsfield + Nano Banana + Flux AI",
      "Tipo": "Projeto Pessoal",
      "Ano": "2025"
    },
    videos: [
      { url: "assets/projetos/ia-projeto-2/video.mp4", talento: "Dentro da Minha Cabeça - Higgsfield + Flux AI" }
    ],
    galeria: []
  },
  {
    id: 72,
    nome: "Soldiers Nutrition",
    categoria: "ia",
    categoriaLabel: "Produção com IA",
    ano: "2026",
    videoId: "",
    descricao: "Campanha de conteúdo com avatares digitais para a linha de suplementos da Soldiers Nutrition — creatina, whey, pré-treino e termogênico.",
    ficha: {
      "Função": "Produção com IA",
      "Marca": "Soldiers Nutrition",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2026"
    },
    videos: [
      { youtubeId: "CVVdJetIjVk", talento: "Creatina 1kg" },
      { youtubeId: "OuHLFkBeXoE", talento: "Creatina 1kg" },
      { youtubeId: "KZroIhBn2tE", talento: "Creatina 1kg" },
      { youtubeId: "AdFQAPLVVFo", talento: "Creatina 1kg" },
      { youtubeId: "pM1HCsq2pZw", talento: "Creatina 1kg" },
      { youtubeId: "vO0ZCGvncRI", talento: "Creatina 1kg" },
      { youtubeId: "x7UEgPPzGmc", talento: "Creatina 1kg" },
      { youtubeId: "ej84rrYAzZA", talento: "Creatina 1kg" },
      { youtubeId: "qb2jJbX8j3w", talento: "Creatina 1kg" },
      { youtubeId: "m6DhIZuCuLs", talento: "Creatina 1kg" },
      { youtubeId: "gaw6A7pmmBc", talento: "Creatina 1kg" },
      { youtubeId: "gHgW5exW-6k", talento: "Creatina 1kg" },
      { youtubeId: "2X25AaaKFuw", talento: "Creatina 1kg" },
      { youtubeId: "igqbOIAN1s4", talento: "Creatina 1kg" },
      { youtubeId: "khg29vLriUc", talento: "Creatina 1kg" },
      { youtubeId: "t7ukjsCZY6M", talento: "Creatina 1kg" },
      { youtubeId: "8yoJXviw4i4", talento: "Creatina 1kg" },
      { youtubeId: "7rRFs9geI50", talento: "Creatina 1kg" },
      { youtubeId: "fCEIr6KWItA", talento: "Creatina 1kg" },
      { youtubeId: "Ty9WguB2QLY", talento: "Creatina 1kg" },
      { youtubeId: "wNll1WXo_EY", talento: "Creatina 500g" },
      { youtubeId: "PqmGzcPrixw", talento: "Creatina 500g" },
      { youtubeId: "sd6R4k0kiBM", talento: "Creatina 500g" },
      { youtubeId: "vpKD1pOlHDc", talento: "Creatina 500g" },
      { youtubeId: "Jcpy7kJwQTM", talento: "Creatina 500g" },
      { youtubeId: "7pvCcQZsez4", talento: "Creatina 500g" },
      { youtubeId: "2KA7xwBr1D4", talento: "Creatina 500g" },
      { youtubeId: "w8m4f5H439w", talento: "Creatina 500g" },
      { youtubeId: "EYHTgYp1Umg", talento: "Creatina 500g" },
      { youtubeId: "860B_SrEhkk", talento: "Creatina 500g" },
      { youtubeId: "wjr5-3z3hpI", talento: "Creatina 500g" },
      { youtubeId: "eOt6VXZns4s", talento: "Creatina 500g" },
      { youtubeId: "BZy6jB2r5pY", talento: "Creatina 500g" },
      { youtubeId: "9mWoBI4gq9U", talento: "Creatina 500g" },
      { youtubeId: "dzj3ngFJmK0", talento: "Creatina 500g" },
      { youtubeId: "ML1ukiLzuzA", talento: "Creatina 500g" },
      { youtubeId: "_tXUJVjclUs", talento: "Creatina 500g" },
      { youtubeId: "dg09dXXLVGU", talento: "Creatina 500g" },
      { youtubeId: "6AJtMY_J2nE", talento: "Creatina 500g" },
      { youtubeId: "d46xwRo3Tjw", talento: "Creatina 500g" },
      { youtubeId: "s_vau70jTYY", talento: "Whey Primal" },
      { youtubeId: "RYT7zCn32dU", talento: "Whey Primal" },
      { youtubeId: "35LPgKD1boM", talento: "Whey Primal" },
      { youtubeId: "c-gHr8KRzyw", talento: "Whey Primal" },
      { youtubeId: "_XOpG3DeS0E", talento: "Whey Primal" },
      { youtubeId: "RKgkpnGdkOM", talento: "Whey Primal" },
      { youtubeId: "kGNkZJq9GUc", talento: "Whey Primal" },
      { youtubeId: "Qa3xcRYRV_o", talento: "Whey Primal" },
      { youtubeId: "D3ndPDIEwQ0", talento: "Whey Primal" },
      { youtubeId: "sIuPMWH3Iek", talento: "Whey Primal" },
      { youtubeId: "6KxaueKb_zc", talento: "Whey Primal" },
      { youtubeId: "S7eCNcNnqpw", talento: "Whey Primal" },
      { youtubeId: "eWCYoHhu57Y", talento: "Whey Primal" },
      { youtubeId: "i6tnNyhzK-Q", talento: "Whey Primal" },
      { youtubeId: "7S92V-YFi_Q", talento: "Whey Primal" },
      { youtubeId: "PKpjAHDR4yU", talento: "Whey Primal" },
      { youtubeId: "aoAy0_wMQGA", talento: "Whey Primal" },
      { youtubeId: "nxw8GzVxhZw", talento: "Whey Primal" },
      { youtubeId: "DhLTs4AGi-8", talento: "Whey Primal" },
      { youtubeId: "dKUhat5biSg", talento: "Whey Primal" },
      { youtubeId: "b73JXIya8cY", talento: "Pré-Treino Evolution" },
      { youtubeId: "dVpzzASuG4Y", talento: "Pré-Treino Evolution" },
      { youtubeId: "1LFe5LdlON8", talento: "Pré-Treino Evolution" },
      { youtubeId: "_0dUiLv4qbQ", talento: "Pré-Treino Evolution" },
      { youtubeId: "aaEhGNY_sQU", talento: "Pré-Treino Evolution" },
      { youtubeId: "mlVp5VuIlF0", talento: "Pré-Treino Evolution" },
      { youtubeId: "vQDcssK0ohA", talento: "Pré-Treino Evolution" },
      { youtubeId: "ElRGkVwd7ts", talento: "Pré-Treino Evolution" },
      { youtubeId: "-9l2tGe_1hs", talento: "Pré-Treino Evolution" },
      { youtubeId: "AqVWbTiCiCs", talento: "Pré-Treino Evolution" },
      { youtubeId: "48tcVAUHWQw", talento: "Pré-Treino Evolution" },
      { youtubeId: "WcIZ0SyAeZA", talento: "Pré-Treino Evolution" },
      { youtubeId: "VNMPOTf5reY", talento: "Pré-Treino Evolution" },
      { youtubeId: "hnbTssGw-Hs", talento: "Pré-Treino Evolution" },
      { youtubeId: "_QSbkxU6xVQ", talento: "Pré-Treino Evolution" },
      { youtubeId: "Rh9au-MNS-8", talento: "Pré-Treino Evolution" },
      { youtubeId: "FoHBGD6Fhok", talento: "Pré-Treino Evolution" },
      { youtubeId: "1lSjmUXBiAc", talento: "Pré-Treino Evolution" },
      { youtubeId: "VtdzPWuFX0w", talento: "Pré-Treino Evolution" },
      { youtubeId: "WuBWnN4t7to", talento: "Pré-Treino Evolution" },
      { youtubeId: "j0Eh-m6qmPg", talento: "Thermo Dark" },
      { youtubeId: "ZhV0ww47bk4", talento: "Thermo Dark" },
      { youtubeId: "6vif4bpsC1U", talento: "Thermo Dark" },
      { youtubeId: "ev8_gDjqR4g", talento: "Thermo Dark" },
      { youtubeId: "xTpNvOQOkPU", talento: "Thermo Dark" },
      { youtubeId: "nhuMdmF98zA", talento: "Thermo Dark" },
      { youtubeId: "e4Z1z0q2KDw", talento: "Thermo Dark" },
      { youtubeId: "mD25X1GMypY", talento: "Thermo Dark" },
      { youtubeId: "Y_zMlbARUG8", talento: "Thermo Dark" },
      { youtubeId: "Mbojsdmolac", talento: "Thermo Dark" },
      { youtubeId: "8kdCskFzAsk", talento: "Thermo Dark" },
      { youtubeId: "44Ewt3Ca-VE", talento: "Thermo Dark" },
      { youtubeId: "Ph6IPxIDLLw", talento: "Thermo Dark" },
      { youtubeId: "jpXsc0H4QVA", talento: "Thermo Dark" },
      { youtubeId: "_TCqHcgqZdI", talento: "Thermo Dark" },
      { youtubeId: "jRCZI9vI4TY", talento: "Thermo Dark" },
      { youtubeId: "v962tIyJ3VU", talento: "Thermo Dark" },
      { youtubeId: "jDgIq-75EvQ", talento: "Thermo Dark" },
      { youtubeId: "FdtGaoMJfq8", talento: "Thermo Dark" },
      { youtubeId: "O72nhv6J6SY", talento: "Thermo Dark" }
    ],
    galeria: []
  },
  {
    id: 41,
    nome: "Allfluence",
    categoria: "video",
    categoriaLabel: "Filmmaker + Direção",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo interno e social media para a Allfluence, incluindo vídeos institucionais e de tendências com a equipe.",
    ficha: {
      "Função": "Filmmaker + Direção",
      "Marca": "Allfluence",
      "Plataforma": "TikTok / Instagram",
      "Tipo": "Social Media + Institucional",
      "Período": "Fev 2025 - 2026"
    },
    instagram: "https://www.instagram.com/allfluence/",
    website: "https://www.allfluence.com.br/",
    videos: [
      { youtubeId: "1heeu4JlBrs", talento: "Yago Capita" },
      { youtubeId: "CmNwHyH0wso", talento: "Yago Capita" },
      { youtubeId: "QLF4xBQ30jo", talento: "Yago Capita" },
      { youtubeId: "fMHNZbbcQJE", talento: "Yago Capita Pedro Valério" },
      { youtubeId: "wKvkhHMKs2s", talento: "Yago Capita" },
      { youtubeId: "zlgZVZlnYys", direcao: true, talento: "Camille Ana Claudia Padilha Savylla" },
      { youtubeId: "mATBN8ULM6o", talento: "Yago Capita Camille Ana Claudia Padilha Savylla" },
      { youtubeId: "fwhdF2NlIpY", direcao: true, talento: "Camille Ana Claudia Padilha Savylla" },
      { youtubeId: "1kdog5TY15k", direcao: true, talento: "Camille Ana Claudia Padilha Savylla" },
      { youtubeId: "JKvGdRN-eeE", direcao: true, talento: "Equipe Allfluence" },
      { url: "assets/projetos/oscar/video-1.mp4", talento: "Oscar 2026 - Produção com IA" }
    ],
    galeria: []
  },
  {
    id: 42,
    nome: "Veloe",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Veloe em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Veloe",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "mV13Vf1yRzg", talento: "Raphael Monteiro" }
    ],
    galeria: []
  },
  {
    id: 43,
    nome: "Agibank",
    categoria: "video",
    categoriaLabel: "Filmmaker + Direção",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Agibank em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker + Direção",
      "Marca": "Agibank",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "srXIpTh6Ips", talento: "Isadora Cecatto" },
      { youtubeId: "O0xg4LJcnTY", talento: "Isadora Cecatto" },
      { youtubeId: "h5ZbUewydlE", direcao: true, talento: "Isadora Cecatto" },
      { youtubeId: "EReFfZhL_r4", direcao: true, talento: "Isadora Cecatto" },
      { youtubeId: "vHKHH4UBFPg", direcao: true, talento: "Débora Melo" },
      { youtubeId: "AV3vjr8SrSI", direcao: true, talento: "Débora Melo" },
      { youtubeId: "yp5di3n_lM8", direcao: true, talento: "Débora Melo" },
      { youtubeId: "-rruV4XAFxM", direcao: true, talento: "Débora Melo" }
    ],
    galeria: []
  },
  {
    id: 44,
    nome: "Livelo",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Livelo em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Livelo",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "XIu7SO5hxZo", talento: "Quéren Hapuque" },
      { youtubeId: "lSF5HQzfglE", talento: "Quéren Hapuque" },
      { youtubeId: "-V-9LwVRXpo", talento: "Quéren Hapuque" },
      { youtubeId: "5KDSlaL1t_w", talento: "Quéren Hapuque" },
      { youtubeId: "lZBe8nEN6hk", talento: "Quéren Hapuque" },
      { youtubeId: "v-7Jdnsf1tg", talento: "Quéren Hapuque" },
      { youtubeId: "RENf_JTMZ5A", talento: "Quéren Hapuque" },
      { youtubeId: "IptEabWDjW0", talento: "Quéren Hapuque" },
      { youtubeId: "BUz4VewUxJ0", talento: "Quéren Hapuque" },
      { youtubeId: "wsDZVmBUrNo", talento: "Letícia Pedro" }
    ],
    galeria: []
  },
  {
    id: 45,
    nome: "Baby Sec",
    categoria: "video",
    categoriaLabel: "Filmmaker + Direção",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Baby Sec em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker + Direção",
      "Marca": "Baby Sec",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "9BZS3t242m0", talento: "Gabriel Peregrino" },
      { youtubeId: "jP0vGWfg3Vc", direcao: true, talento: "Gabriel Peregrino" },
      { youtubeId: "J58_VMwT7E4", direcao: true, talento: "Gabriel Peregrino" },
      { youtubeId: "Km8Mw4ew1sE", direcao: true, talento: "Gabriel Peregrino" }
    ],
    galeria: []
  },
  {
    id: 46,
    nome: "GA.MA",
    categoria: "video",
    categoriaLabel: "Filmmaker + Direção",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da GA.MA em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker + Direção",
      "Marca": "GA.MA",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "OFMijRGWQcw", direcao: true, talento: "Larissa Venturini" },
      { youtubeId: "G_ggKHUkqJ8", direcao: true, talento: "Larissa Venturini" },
      { youtubeId: "TFU6R7oTlUQ", direcao: true, talento: "Larissa Venturini" },
      { youtubeId: "pJfBXKSByCc", direcao: true, talento: "Larissa Venturini" }
    ],
    galeria: []
  },
  {
    id: 47,
    nome: "Bullsbet",
    categoria: "video",
    categoriaLabel: "Filmmaker + Direção",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Bullsbet em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker + Direção",
      "Marca": "Bullsbet",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "H2tWDso6ScE", direcao: true, talento: "Antônio Bastos" },
      { youtubeId: "MvwBEtwZ6XM", direcao: true, talento: "Antônio Bastos" },
      { youtubeId: "nLsCifRsfVA", direcao: true, talento: "Antônio Bastos" },
      { youtubeId: "TRxWckgUgwU", direcao: true, talento: "Antônio Bastos" }
    ],
    galeria: []
  },
  {
    id: 48,
    nome: "Faculdade Estácio",
    categoria: "video",
    categoriaLabel: "Filmmaker + Direção",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Faculdade Estácio em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker + Direção",
      "Marca": "Faculdade Estácio",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "ein__DWHnh0", direcao: true, talento: "Larissa Travassos" },
      { youtubeId: "3wWNUjj6ELI", direcao: true, talento: "Larissa Travassos" },
      { youtubeId: "jxHghz1u2OI", direcao: true, talento: "João Mendes" },
      { youtubeId: "kRs4zbA0B-U", direcao: true, talento: "Larissa Travassos" },
      { youtubeId: "m7DLJqcJecU", direcao: true, talento: "João Mendes" },
      { youtubeId: "zcFKV5W4YgE", direcao: true, talento: "João Mendes" },
      { youtubeId: "2MHPFeMDlHo", talento: "Larissa Travassos" },
      { youtubeId: "C8fOvcxr_7E", direcao: true, talento: "João Mendes" },
      { youtubeId: "4VjXFp7PK4c", talento: "Mariana Braga" },
      { youtubeId: "TqXiHSydBEw", talento: "Mariana Braga" },
      { youtubeId: "aQjrIn8v7gI", talento: "Mariana Braga" },
      { youtubeId: "cz2A4uSbQOI", talento: "Rodrigo Rabello" },
      { youtubeId: "Y4yW1to3re8", talento: "Rodrigo Rabello" },
      { youtubeId: "FBE1MW1hyvg", talento: "Rodrigo Rabello" },
      { youtubeId: "ZuonxxzGqcE", talento: "Rodrigo Rabello" },
      { youtubeId: "UBiPwU0Kkzw", talento: "Mariana Braga" },
      { youtubeId: "zPrMXgucQFU", talento: "Larissa Travassos" },
      { youtubeId: "Sx-Rylazlh4", talento: "Larissa Travassos" },
      { youtubeId: "ii1zsUCsKaw", talento: "Fernanda Penna" },
      { youtubeId: "-TQwyN3Eg6E", talento: "Fernanda Penna" },
      { youtubeId: "-HkT1-b3EjM", talento: "Larissa Travassos" },
      { youtubeId: "mxX3cv0Dqj0", talento: "Larissa Travassos" },
      { youtubeId: "-Eclfq86EGo", talento: "Fernanda Penna" },
      { youtubeId: "L4Kli6X2Mis", talento: "Fernanda Penna" }
    ],
    galeria: []
  },
  {
    id: 49,
    nome: "Reals Bet",
    categoria: "video",
    categoriaLabel: "Filmmaker + Direção",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Reals Bet em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker + Direção",
      "Marca": "Reals Bet",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "daS4IjfpigA", direcao: true, talento: "Pablo Sant'Anna" },
      { youtubeId: "SB9TvZa4G-A", direcao: true, talento: "Pablo Sant'Anna" },
      { youtubeId: "l5rExGkiRTo", direcao: true, talento: "Pablo Sant'Anna" },
      { youtubeId: "4YAsshDgYrE", direcao: true, talento: "Pablo Sant'Anna" }
    ],
    galeria: []
  },
  {
    id: 50,
    nome: "Sorriso",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Sorriso em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Sorriso",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "2k59DKam2Ak", talento: "Khiara" },
      { youtubeId: "75A3rMytAQE", talento: "Khiara" }
    ],
    galeria: []
  },
  {
    id: 51,
    nome: "Tramontina",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Tramontina em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Tramontina",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "9cN0JeeCHgc", talento: "Tati Infante" },
      { youtubeId: "RMPKvAVqwJ8", talento: "Tati Infante" }
    ],
    galeria: []
  },
  {
    id: 52,
    nome: "Softys Kitchen",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Softys Kitchen em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Softys Kitchen",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "kt4bPfBPMYw", talento: "Ígor Arvelos" },
      { youtubeId: "SifzvaTS70Y", talento: "Ígor Arvelos" },
      { youtubeId: "1PnTyixd9VM", talento: "Letícia Machado" },
      { youtubeId: "B_2bS-q02n8", talento: "Ígor Arvelos" },
      { youtubeId: "Nj75nnQPwtE", talento: "Letícia Machado" },
      { youtubeId: "lx8l6P-GmEI", talento: "Letícia Machado" },
      { youtubeId: "nqgNfNBQ4mc", talento: "Ígor Arvelos" },
      { youtubeId: "lyrgIE4SHbM", talento: "Letícia Machado" }
    ],
    galeria: []
  },
  {
    id: 53,
    nome: "Aiqfome",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Aiqfome em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Aiqfome",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "yDwK_0ma93s", talento: "Yago Capita" },
      { youtubeId: "NDl-BKL_jQA", talento: "Yago Capita" },
      { youtubeId: "jJlTNW5L8r8", talento: "Yago Capita" },
      { youtubeId: "iTBwPlIWLwo", talento: "Yago Capita" }
    ],
    galeria: []
  },
  {
    id: 54,
    nome: "Philco Britânia",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Philco Britânia em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Philco Britânia",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "ozhdJtYqrTs", talento: "Khiara" }
    ],
    galeria: []
  },
  {
    id: 55,
    nome: "Mycon",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Mycon em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Mycon",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { youtubeId: "KArk5ZJES3A", talento: "Adam Pereira" },
      { youtubeId: "dYoqcyU082E", talento: "Malu Medina" },
      { youtubeId: "49Wu2PZjiTY", talento: "Adam Pereira" },
      { youtubeId: "x7xXZs3LeEw", talento: "Malu Medina" },
      { youtubeId: "gQvE6zuFLR4", talento: "Adam Pereira" },
      { youtubeId: "MGnkhl2Dx84", talento: "Malu Medina" },
      { youtubeId: "4swS2g9mh80", talento: "Malu Medina" },
      { youtubeId: "tdXXqQLKeCA", talento: "Adam Pereira" }
    ],
    galeria: []
  },
  {
    id: 56,
    nome: "Atacadão",
    categoria: "video",
    categoriaLabel: "Filmmaker + Direção",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Atacadão em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker + Direção",
      "Marca": "Atacadão",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2026"
    },
    videos: [
      { youtubeId: "-2EXpu6Y_RM", direcao: true, talento: "Quézia Castro" }
    ],
    galeria: []
  },
  {
    id: 57,
    nome: "Cassino.Bet",
    categoria: "video",
    categoriaLabel: "Filmmaker",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo audiovisual para campanhas da Cassino.Bet em plataformas digitais.",
    ficha: {
      "Função": "Filmmaker",
      "Marca": "Cassino.Bet",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    instagram: "https://www.instagram.com/cassino.bet.br/",
    website: "https://cassino.bet.br/",
    videos: [
      { youtubeId: "thP2xd7T1ok", talento: "João Victor" },
      { youtubeId: "XNKlYL9lKBA", talento: "João Victor" }
    ],
    galeria: []
  }
];

// ----------------------------------------
// JS loaded flag (for .reveal CSS fallback)
// ----------------------------------------
document.documentElement.classList.add('js-loaded');

// ----------------------------------------
// Utility: escape HTML to prevent XSS
// ----------------------------------------
function escapeHTML(str) {
  if (str == null) return '';
  const div = document.createElement('div');
  div.textContent = String(str);
  return div.innerHTML;
}

function sanitizeURL(url) {
  if (!url) return '';
  try {
    const u = new URL(url, window.location.origin);
    if (['https:', 'http:'].includes(u.protocol)) return url;
    if (url.startsWith('assets/')) return url;
    return '';
  } catch { return ''; }
}

// ----------------------------------------
// Logo fallback (moved from inline onerror)
// ----------------------------------------
document.querySelectorAll('.marcas__logo').forEach(img => {
  img.addEventListener('error', () => {
    img.style.display = 'none';
    const fallback = img.nextElementSibling;
    if (fallback) fallback.style.display = 'flex';
  });
});

// ----------------------------------------
// Lazy load contato background video
// ----------------------------------------
const contatoBgVideo = document.getElementById('contatoBgVideo');
// Mesmo critério do vídeo global do topo (que usa media="(min-width: 768px)" no
// <source>): abaixo disso fica só o poster. Antes este vídeo baixava ~900KB no
// celular enquanto o outro era poupado.
function deveCarregarVideoDeFundo() {
  if (window.matchMedia('(max-width: 767px)').matches) return false;
  const conexao = navigator.connection;
  if (conexao && conexao.saveData) return false;
  return true;
}
if (contatoBgVideo && deveCarregarVideoDeFundo()) {
  const videoObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const source = document.createElement('source');
        source.src = 'assets/bg-contato-compressed.mp4';
        source.type = 'video/mp4';
        contatoBgVideo.appendChild(source);
        contatoBgVideo.load();
        contatoBgVideo.play().catch(() => {});
        videoObserver.unobserve(entry.target);
      }
    });
  }, { rootMargin: '200px' });
  videoObserver.observe(contatoBgVideo);
}

// ----------------------------------------
// Header scroll (throttled with rAF)
// ----------------------------------------
const header = document.getElementById('header');
let scrollTicking = false;
window.addEventListener('scroll', () => {
  if (!scrollTicking) {
    requestAnimationFrame(() => {
      if (header) header.classList.toggle('scrolled', window.scrollY > 80);
      scrollTicking = false;
    });
    scrollTicking = true;
  }
}, { passive: true });

// ----------------------------------------
// Fullscreen nav overlay
// ----------------------------------------
const sideMenu = document.getElementById('sideMenu');
const navOverlay = document.getElementById('navOverlay');
const burgerBtn = document.getElementById('burgerBtn');

// Ambos os gatilhos (burger no mobile, rótulo lateral no desktop) controlam o
// mesmo overlay, então os dois precisam refletir o estado para leitores de tela.
function setNavState(isOpen) {
  navOverlay.classList.toggle('active', isOpen);
  burgerBtn.classList.toggle('active', isOpen);
  document.body.classList.toggle('nav-open', isOpen);
  navOverlay.setAttribute('aria-hidden', String(!isOpen));
  [burgerBtn, sideMenu].forEach(btn => {
    btn.setAttribute('aria-expanded', String(isOpen));
    btn.setAttribute('aria-label', isOpen ? 'Fechar menu de navegação' : 'Abrir menu de navegação');
  });
  // O rótulo lateral é o gatilho do desktop; deixá-lo escrito "MENU" com o
  // overlay aberto escondia o único jeito de fechar (o burger some acima de 768px).
  sideMenu.textContent = isOpen ? 'FECHAR' : 'MENU';
  document.body.style.overflow = isOpen ? 'hidden' : '';
}

function toggleNav() {
  setNavState(!navOverlay.classList.contains('active'));
}

function closeNav() {
  // O overlay vira visibility:hidden ao fechar; se o foco estivesse dentro dele
  // (num dos links, por exemplo) ele cairia no body e o teclado perderia o lugar.
  const focoDentro = navOverlay.contains(document.activeElement);
  setNavState(false);
  if (focoDentro) {
    const gatilho = burgerBtn.offsetParent !== null ? burgerBtn : sideMenu;
    gatilho.focus({ preventScroll: true });
  }
}

sideMenu.addEventListener('click', toggleNav);
burgerBtn.addEventListener('click', toggleNav);

// Sem estas duas saídas o overlay vira uma armadilha: ele cobre a tela inteira
// e não tem botão de fechar próprio.
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && navOverlay.classList.contains('active')) closeNav();
});
navOverlay.addEventListener('click', e => {
  if (!e.target.closest('.nav-overlay__link')) closeNav();
});

navOverlay.querySelectorAll('.nav-overlay__link').forEach(link => {
  link.addEventListener('click', (e) => {
    // Só as âncoras da própria página são interceptadas para rolar suave. Links
    // para outra página (servicos.html) precisam navegar: com preventDefault
    // aqui eles fechavam o menu e não saíam do lugar.
    const href = link.getAttribute('href') || '';
    if (!href.startsWith('#')) {
      closeNav();
      return;
    }
    e.preventDefault();
    closeNav();
    const target = document.querySelector(href);
    if (target) {
      setTimeout(() => target.scrollIntoView({ behavior: 'smooth' }), 300);
    }
  });
});

// ----------------------------------------
// Smooth scroll
// ----------------------------------------
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    if (this.closest('.nav-overlay')) return;
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) target.scrollIntoView({ behavior: 'smooth' });
  });
});

// ----------------------------------------
// Filtros
// ----------------------------------------
const filtros = document.querySelectorAll('.trabalhos__filtro');
const items = document.querySelectorAll('.trabalhos__item');

// Quantos projetos aparecem antes de "Carregar Mais". Compartilhado com o
// bloco de paginação lá embaixo para o anúncio bater com o que está na tela.
const PROJETOS_POR_PAGINA = 12;

let activeFilter = 'todos';
filtros.forEach(btn => {
  btn.addEventListener('click', () => {
    filtros.forEach(b => {
      b.classList.remove('active');
      b.setAttribute('aria-pressed', 'false');
    });
    btn.classList.add('active');
    btn.setAttribute('aria-pressed', 'true');
    activeFilter = btn.dataset.filter;
    let visibleCount = 0;
    items.forEach(item => {
      const categories = (item.dataset.category || '').split(' ');
      const hidden = activeFilter !== 'todos' && !categories.includes(activeFilter);
      item.classList.toggle('hidden', hidden);
      if (!hidden) visibleCount++;
    });
    if (typeof announceStatus === 'function') {
      const label = btn.textContent.trim();
      // A paginação corta em PROJETOS_POR_PAGINA; anunciar o total do filtro
      // dizia "44 projetos" com 12 na tela.
      const exibidos = Math.min(visibleCount, PROJETOS_POR_PAGINA);
      let msg;
      if (visibleCount === 0) msg = `Nenhum projeto na categoria ${label}.`;
      else if (exibidos < visibleCount) msg = `Exibindo ${exibidos} de ${visibleCount} projetos na categoria ${label}. Use o botão Carregar Mais para ver o restante.`;
      else msg = `Exibindo ${visibleCount} ${visibleCount === 1 ? 'projeto' : 'projetos'} na categoria ${label}.`;
      announceStatus(msg);
    }
  });
});

// ----------------------------------------
// Modal
// ----------------------------------------
const modal = document.getElementById('projetoModal');
const modalClose = document.getElementById('modalClose');

// Proporção do player
// -------------------
// A moldura padrão é 16:9. Conteúdo 9:16 dentro dela fica espremido entre duas
// tarjas pretas, então o container encolhe para 9:16 quando o vídeo é vertical.
//
// As duas listas são geradas offline por `probe_aspect_videos.py` — rode-o de
// novo depois de adicionar vídeos ao portfólio. O YouTube depende disso: o
// iframe não expõe as dimensões e a CSP (connect-src 'self') impede consultar a
// API pelo navegador. Para mp4 local é só para não piscar: o navegador também
// descobre sozinho, mas só quando os metadados chegam, e aí a moldura já entrou
// em 16:9 e muda de tamanho na frente do usuário.
const VIDEOS_YT_VERTICAIS = new Set([
  "C8LcFan2gAs"
]);

const VIDEOS_LOCAIS_VERTICAIS = new Set([
  "assets/projetos/ia-projeto-1/video.mp4",
  "assets/projetos/ia-projeto-2/video.mp4",
  "assets/projetos/oscar/video-1.mp4"
]);

function marcarProporcao(container, ehVertical) {
  container.classList.toggle('modal__video--vertical', !!ehVertical);
}

// Rede de segurança para mp4 fora da lista acima (vídeo novo, lista desatualizada):
// o <video> conhece as próprias dimensões assim que os metadados chegam.
function ajustarProporcaoLocal(container) {
  const video = container.querySelector('video');
  if (!video) return;
  const aplicar = () => {
    // O player é reaproveitado entre projetos. Se os metadados demoram e o
    // usuário já abriu outro vídeo, este evento chega para um <video> que foi
    // descartado — aplicar a proporção dele deformaria o que está na tela.
    if (!container.contains(video)) return;
    if (video.videoWidth && video.videoHeight) {
      marcarProporcao(container, video.videoHeight > video.videoWidth);
    }
  };
  if (video.readyState >= 1) aplicar();
  else video.addEventListener('loadedmetadata', aplicar, { once: true });
}

// A CSP (media-src 'self' blob:) bloqueia mp4 de terceiros, então um vídeo com
// URL externa só renderiza um player vazio. Melhor omiti-lo até ser re-hospedado.
function videoReproduzivel(v) {
  if (!v) return false;
  if (v.youtubeId) return true;
  if (!v.url) return false;
  return !/^https?:\/\//i.test(v.url) || v.url.startsWith(location.origin);
}

// ----------------------------------------
// Tela cheia do player
// ----------------------------------------
// Num celular em retrato o player do modal tem a largura da tela menos o padding
// e altura derivada da proporção: um 16:9 fica com ~200px de altura e o vídeo
// abre pequeno demais. Ao tocar para dar play, promovemos o player a tela cheia.
// Três caminhos, do melhor para o mais compatível:
//   1. mp4 local no iPhone → player nativo do <video> (webkitEnterFullscreen),
//      que já gira sozinho conforme a proporção do vídeo;
//   2. Fullscreen API no container + travar a orientação (só o Android costuma
//      permitir o lock, e é justamente onde ele faz mais diferença);
//   3. .player-cinema — overlay fixo em CSS. É o plano B obrigatório porque o
//      Safari do iPhone não concede fullscreen a <iframe>, e ainda assim o
//      vídeo passa a ocupar a tela toda (e a preencher de verdade ao girar).
let playerCinema = null;      // container atualmente em modo cinema
let botaoSairCinema = null;

function ehTelaDeToque() {
  return window.matchMedia('(pointer: coarse)').matches ||
         window.matchMedia('(max-width: 1024px)').matches;
}

function emTelaCheiaNativa() {
  return !!(document.fullscreenElement || document.webkitFullscreenElement);
}

// Rejeita onde o lock não é permitido (iOS não implementa) — quem chama usa isso
// para decidir se mostra a dica de girar o aparelho.
function orientarTela(vertical) {
  const so = window.screen && screen.orientation;
  if (!so || typeof so.lock !== 'function') return Promise.reject();
  return so.lock(vertical ? 'portrait' : 'landscape');
}

function liberarOrientacao() {
  const so = window.screen && screen.orientation;
  if (!so || typeof so.unlock !== 'function') return;
  try { so.unlock(); } catch (e) { /* nem todo navegador implementa */ }
}

function expandirPlayer(container) {
  if (!container || !ehTelaDeToque()) return;
  if (playerCinema === container || emTelaCheiaNativa()) return;
  // Projeto de fotografia mostra um <img> neste mesmo container: nada a expandir.
  if (!container.querySelector('lite-youtube, iframe, video')) return;

  const vertical = container.classList.contains('modal__video--vertical');
  const videoLocal = container.querySelector('video');

  // readyState 0 = metadados ainda não chegaram, e aí o iOS lança
  // InvalidStateError em vez de abrir o player.
  if (videoLocal && !videoLocal.requestFullscreen && videoLocal.readyState >= 1 &&
      typeof videoLocal.webkitEnterFullscreen === 'function') {
    try {
      videoLocal.webkitEnterFullscreen();
      return;
    } catch (e) { /* segue para os caminhos abaixo */ }
  }

  const pedirTelaCheia = container.requestFullscreen || container.webkitRequestFullscreen;
  if (!pedirTelaCheia) {
    entrarModoCinema(container);
    return;
  }
  // O gesto do usuário ainda vale aqui: é o mesmo clique que ativou o player e
  // borbulhou até este handler.
  Promise.resolve()
    .then(() => pedirTelaCheia.call(container))
    // O catch é interno de propósito: falhar em girar a tela não é motivo para
    // cair no modo cinema — a tela cheia nativa já foi concedida.
    .then(() => orientarTela(vertical).catch(() => {}))
    // A dica de girar depende do estado real da tela, não do resultado do lock:
    // há navegador em que lock('landscape') resolve sem girar coisa alguma. O
    // atraso dá tempo de a orientação efetivar antes da checagem.
    .then(() => { setTimeout(() => mostrarDicaGirar(container), 400); })
    .catch(() => entrarModoCinema(container));
}

// position:fixed não se resolve contra a viewport quando algum ancestral cria um
// containing block — e o .modal__content tem transform (a animação de entrada).
// Sem neutralizar, o overlay do modo cinema herda a caixa do modal inteiro e
// vira uma tarja de milhares de pixels de altura em vez de cobrir a tela.
// Valor "neutro" por propriedade: o que faz o ancestral parar de criar o
// containing block (will-change volta para auto, não para none).
const PROPS_CONTAINING_BLOCK = {
  transform: 'none',
  filter: 'none',
  perspective: 'none',
  backdropFilter: 'none',
  contain: 'none',
  willChange: 'auto'
};
let ancestraisNeutralizados = [];

function neutralizarAncestrais(el) {
  restaurarAncestrais();
  for (let no = el.parentElement; no && no !== document.body; no = no.parentElement) {
    const estilo = getComputedStyle(no);
    Object.keys(PROPS_CONTAINING_BLOCK).forEach(prop => {
      const neutro = PROPS_CONTAINING_BLOCK[prop];
      if (!estilo[prop] || estilo[prop] === neutro) return;
      ancestraisNeutralizados.push({ no, prop, anterior: no.style[prop] });
      no.style[prop] = neutro;
    });
  }
}

function restaurarAncestrais() {
  ancestraisNeutralizados.forEach(({ no, prop, anterior }) => { no.style[prop] = anterior; });
  ancestraisNeutralizados = [];
}

function entrarModoCinema(container) {
  if (playerCinema) sairModoCinema();
  playerCinema = container;
  neutralizarAncestrais(container);
  container.classList.add('player-cinema');
  document.body.style.overflow = 'hidden';

  if (!botaoSairCinema) {
    botaoSairCinema = document.createElement('button');
    botaoSairCinema.type = 'button';
    botaoSairCinema.className = 'player-cinema-sair';
    botaoSairCinema.setAttribute('aria-label', 'Sair da tela cheia');
    botaoSairCinema.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>';
    botaoSairCinema.addEventListener('click', sairModoCinema);
  }
  // No <body>, não dentro do container: trocar de vídeo reescreve o innerHTML
  // dele e levaria o botão embora.
  document.body.appendChild(botaoSairCinema);
  mostrarDicaGirar(container);
}

function sairModoCinema() {
  if (!playerCinema) return;
  playerCinema.classList.remove('player-cinema');
  playerCinema = null;
  restaurarAncestrais();
  esconderDicaGirar();
  if (botaoSairCinema && botaoSairCinema.parentNode) botaoSairCinema.remove();
  // O modal também trava a rolagem: só devolver se ele não estiver aberto.
  if (!modal.classList.contains('active')) document.body.style.overflow = '';
}

function sairTelaCheia() {
  sairModoCinema();
  esconderDicaGirar();
  if (emTelaCheiaNativa()) {
    const sair = document.exitFullscreen || document.webkitExitFullscreen;
    if (sair) {
      try { sair.call(document); } catch (e) { /* já saiu */ }
    }
  }
}

document.addEventListener('fullscreenchange', () => {
  if (!document.fullscreenElement) {
    liberarOrientacao();
    esconderDicaGirar();
  }
});

// ----------------------------------------
// Dica "gire o celular"
// ----------------------------------------
// Vídeo horizontal em tela cheia com o aparelho em retrato ainda sobra tarja em
// cima e embaixo, e girar praticamente dobra o tamanho da imagem. Onde o lock de
// orientação funciona (Android) o giro já aconteceu sozinho e a dica nem
// aparece; ela existe para o iPhone, que não implementa o lock.
const DICA_GIRAR_MS = 4500;
let dicaGirar = null;
let dicaGirarTimer = null;

function mostrarDicaGirar(container) {
  if (!container || container.classList.contains('modal__video--vertical')) return;
  if (!window.matchMedia('(orientation: portrait)').matches) return;
  // Chamada com atraso no caminho nativo: o usuário pode já ter saído da tela
  // cheia, e aí a dica ficaria pendurada sobre o modal normal.
  if (!emTelaCheiaNativa() && playerCinema !== container) return;

  if (!dicaGirar) {
    dicaGirar = document.createElement('div');
    dicaGirar.className = 'player-dica-girar';
    // role=status para o leitor de tela anunciar sem roubar o foco do player.
    dicaGirar.setAttribute('role', 'status');
    dicaGirar.innerHTML =
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M4 9a8 8 0 0 1 13-3l2 2"/><path d="M19 4v4h-4"/>' +
      '<path d="M20 15a8 8 0 0 1-13 3l-2-2"/><path d="M5 20v-4h4"/></svg>' +
      '<span>Gire o celular para ampliar</span>';
  }
  // Dentro do container porque no fullscreen nativo só o que está dentro do
  // elemento em tela cheia é renderizado.
  container.appendChild(dicaGirar);

  if (dicaGirarTimer) clearTimeout(dicaGirarTimer);
  dicaGirarTimer = setTimeout(esconderDicaGirar, DICA_GIRAR_MS);
}

function esconderDicaGirar() {
  if (dicaGirarTimer) {
    clearTimeout(dicaGirarTimer);
    dicaGirarTimer = null;
  }
  if (dicaGirar && dicaGirar.parentNode) dicaGirar.remove();
}

// Girou: a dica cumpriu o papel. Não reaparece se voltar para retrato — insistir
// depois de já ter sido lida vira estorvo em cima do vídeo.
const mqRetrato = window.matchMedia('(orientation: portrait)');
const aoGirar = () => { if (!mqRetrato.matches) esconderDicaGirar(); };
if (typeof mqRetrato.addEventListener === 'function') mqRetrato.addEventListener('change', aoGirar);
else if (typeof mqRetrato.addListener === 'function') mqRetrato.addListener(aoGirar);

function openModal(id) {
  const p = projetos.find(x => x.id === id);
  if (!p) return;

  document.getElementById('modalCategoria').textContent = p.categoriaLabel;
  document.getElementById('modalTitulo').textContent = p.nome;
  document.getElementById('modalDescricao').textContent = p.descricao;

  const videoEl = document.getElementById('modalVideo');
  // Filter videos based on active filter
  const allVideos = p.videos && p.videos.length > 0 ? p.videos.filter(videoReproduzivel) : [];
  const displayVideos = activeFilter === 'direcao' && allVideos.length > 0
    ? allVideos.filter(v => v.direcao)
    : allVideos;
  const hasVideos = displayVideos.length > 0;

  marcarProporcao(videoEl, false);

  if (p.videoId && !p.videoId.startsWith('VIDEO_ID') && p.videoId !== '') {
    videoEl.style.display = '';
    videoEl.innerHTML = `<lite-youtube videoid="${escapeHTML(p.videoId)}" params="rel=0&modestbranding=1&mute=1" style="width:100%;height:100%;"></lite-youtube>`;
    marcarProporcao(videoEl, VIDEOS_YT_VERTICAIS.has(p.videoId));
  } else if (hasVideos) {
    videoEl.style.display = '';
    if (displayVideos[0].youtubeId) {
      videoEl.innerHTML = `<lite-youtube videoid="${escapeHTML(displayVideos[0].youtubeId)}" params="rel=0&modestbranding=1&mute=1" style="width:100%;height:100%;"></lite-youtube>`;
      marcarProporcao(videoEl, VIDEOS_YT_VERTICAIS.has(displayVideos[0].youtubeId));
    } else {
      videoEl.innerHTML = `<video controls playsinline preload="metadata" style="width:100%;height:100%;object-fit:contain;background:#000"><source src="${sanitizeURL(displayVideos[0].url)}" type="video/mp4">Seu navegador não suporta vídeo.</video>`;
      marcarProporcao(videoEl, VIDEOS_LOCAIS_VERTICAIS.has(displayVideos[0].url));
      ajustarProporcaoLocal(videoEl);
    }
    if (displayVideos[0].talento) {
      videoEl.insertAdjacentHTML('beforeend', `<div class="modal__video-talent">${escapeHTML(displayVideos[0].talento)}</div>`);
    }
  } else if (p.galeria && p.galeria.length > 0) {
    // Photography project: show hero image instead of video placeholder
    videoEl.style.display = '';
    videoEl.innerHTML = `<img src="${sanitizeURL(p.galeria[0])}" alt="${escapeHTML(p.nome)}" style="width:100%;height:100%;object-fit:cover;">`;
  } else {
    // Sem mídia exibível: esconder o container em vez de deixar um bloco vazio
    videoEl.style.display = 'none';
    videoEl.innerHTML = '';
  }

  const fichaEl = document.getElementById('modalFicha');
  fichaEl.innerHTML = Object.entries(p.ficha).map(([k, v]) => `<div><dt>${escapeHTML(k)}</dt><dd>${escapeHTML(v)}</dd></div>`).join('');

  // Social/link buttons
  const existingLinks = document.querySelectorAll('.modal__link-btn');
  existingLinks.forEach(el => el.remove());

  const linksContainer = document.createElement('div');
  linksContainer.className = 'modal__link-btn modal__links-row';

  // SVG icons
  const icons = {
    instagram: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>',
    youtube: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19.13C5.12 19.56 12 19.56 12 19.56s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.43z"/><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"/></svg>',
    tiktok: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 12a4 4 0 1 0 4 4V4a5 5 0 0 0 5 5"/></svg>',
    facebook: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>',
    spotify: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 15c3.5-1 7-1 10 1"/><path d="M7 12c4.5-1.5 9-1.5 13 1"/><path d="M6 9c5.5-2 11.5-2 16 1"/></svg>',
    linkedin: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>',
    website: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>'
  };

  function addSocialBtn(url, icon, label) {
    const btn = document.createElement('a');
    btn.href = url;
    btn.target = '_blank';
    btn.rel = 'noopener noreferrer';
    btn.className = 'modal__social-btn';
    btn.innerHTML = `${icon}<span>${label}</span>`;
    linksContainer.appendChild(btn);
  }

  if (p.instagram) {
    const handle = p.instagram.replace(/\/$/, '').split('/').pop();
    addSocialBtn(p.instagram, icons.instagram, '@' + handle);
  }
  if (p.instagram2) {
    const handle2 = p.instagram2.replace(/\/$/, '').split('/').pop();
    addSocialBtn(p.instagram2, icons.instagram, '@' + handle2);
  }
  if (p.youtube) {
    addSocialBtn(p.youtube, icons.youtube, 'YouTube');
  }
  if (p.youtubeVideo) {
    addSocialBtn(p.youtubeVideo, icons.youtube, 'Assistir Filme');
  }
  if (p.tiktok) {
    const handle = p.tiktok.replace(/\/$/, '').split('/').pop();
    addSocialBtn(p.tiktok, icons.tiktok, handle);
  }
  if (p.facebook) {
    addSocialBtn(p.facebook, icons.facebook, 'Facebook');
  }
  if (p.spotify) {
    addSocialBtn(p.spotify, icons.spotify, 'Spotify');
  }
  if (p.linkedin) {
    addSocialBtn(p.linkedin, icons.linkedin, 'LinkedIn');
  }
  if (p.website) {
    try {
      const domain = new URL(p.website).hostname.replace('www.', '');
      addSocialBtn(p.website, icons.website, domain);
    } catch (e) {
      addSocialBtn(p.website, icons.website, 'Website');
    }
  }
  if (p.website2) {
    try {
      const domain2 = new URL(p.website2).hostname.replace('www.', '');
      addSocialBtn(p.website2, icons.website, domain2);
    } catch (e) {
      addSocialBtn(p.website2, icons.website, 'Website');
    }
  }

  if (linksContainer.children.length > 0) {
    fichaEl.parentNode.insertBefore(linksContainer, fichaEl.nextSibling);
  }

  // Video gallery
  const galeriaEl = document.getElementById('galeriaGrid');
  galeriaEl.innerHTML = '';
  galeriaEl.classList.remove('modal__galeria-grid--photos');

  if (hasVideos && displayVideos.length > 1) {
    const videoGaleriaTitle = document.getElementById('galeriaTitle');
    if (videoGaleriaTitle) videoGaleriaTitle.textContent = `Produções (${displayVideos.length})`;

    displayVideos.forEach((v, i) => {
      const card = document.createElement('div');
      card.className = 'modal__video-card' + (i === 0 ? ' active' : '');
      card.innerHTML = `
        <div class="modal__video-card-play">
          <svg viewBox="0 0 24 24" fill="currentColor"><polygon points="5,3 19,12 5,21"/></svg>
        </div>
        <span class="modal__video-card-talent">${escapeHTML(v.talento || 'Video ' + (i + 1))}</span>
      `;
      card.addEventListener('click', () => {
        if (v.youtubeId) {
          videoEl.innerHTML = `<lite-youtube videoid="${escapeHTML(v.youtubeId)}" params="rel=0&modestbranding=1&mute=1" style="width:100%;height:100%;"></lite-youtube>`;
          marcarProporcao(videoEl, VIDEOS_YT_VERTICAIS.has(v.youtubeId));
        } else {
          videoEl.innerHTML = `<video controls autoplay playsinline preload="metadata" style="width:100%;height:100%;object-fit:contain;background:#000"><source src="${sanitizeURL(v.url)}" type="video/mp4">Seu navegador não suporta vídeo.</video>`;
          marcarProporcao(videoEl, VIDEOS_LOCAIS_VERTICAIS.has(v.url));
          ajustarProporcaoLocal(videoEl);
        }
        if (v.talento) {
          videoEl.insertAdjacentHTML('beforeend', `<div class="modal__video-talent">${escapeHTML(v.talento)}</div>`);
        }
        // Autoplay imediato no card click (gesto do usuario ja existe)
        if (v.youtubeId) {
          const lyt = videoEl.querySelector('lite-youtube');
          if (lyt && typeof lyt.activate === 'function') {
            requestAnimationFrame(() => lyt.activate());
          }
        }
        // Trocar de vídeo pelos cards também abre em tela cheia — o clique no
        // card é o gesto que o navegador exige.
        expandirPlayer(videoEl);
        galeriaEl.querySelectorAll('.modal__video-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        // Quem rola é o .modal (overflow-y:auto); o .modal__content não tem
        // scroll próprio, então chamar scrollTo nele não fazia nada.
        modal.scrollTo({ top: 0, behavior: 'smooth' });
      });
      galeriaEl.appendChild(card);
    });

    // Append gallery images after video cards if project has both
    if (p.galeria && p.galeria.length > 0) {
      const totalItems = displayVideos.length + p.galeria.length;
      if (videoGaleriaTitle) videoGaleriaTitle.textContent = `Produções e Galeria (${totalItems})`;
      p.galeria.forEach((src, i) => {
        const img = document.createElement('img');
        img.src = src;
        img.alt = p.nome;
        img.loading = 'lazy';
        img.style.cssText = 'width:100%;border-radius:8px;cursor:pointer;';
        img.onerror = function() { this.alt = 'Imagem indisponível'; this.style.opacity = '0.3'; };
        tornarFotoAcessivel(img, p.galeria, i, p.nome);
        galeriaEl.appendChild(img);
      });
    }
  } else {
    // Image gallery for non-video projects
    const galeriaList = p.galeria || [];
    const galeriaTitle = document.getElementById('galeriaTitle');
    if (galeriaTitle) {
      galeriaTitle.textContent = `Galeria (${galeriaList.length})`;
      // Não anunciar uma galeria vazia
      galeriaTitle.style.display = galeriaList.length ? '' : 'none';
    }

    // Use photo-optimized grid for photography projects
    if (p.categoria === 'fotografia' && galeriaList.length > 3) {
      galeriaEl.classList.add('modal__galeria-grid--photos');
    } else {
      galeriaEl.classList.remove('modal__galeria-grid--photos');
    }

    galeriaList.forEach((src, i) => {
      const img = document.createElement('img');
      img.src = sanitizeURL(src);
      img.alt = escapeHTML(p.nome);
      img.loading = 'lazy';
      img.style.cursor = 'pointer';
      img.onerror = function() { this.alt = 'Imagem indisponível'; this.style.opacity = '0.3'; };
      tornarFotoAcessivel(img, galeriaList, i, p.nome);
      galeriaEl.appendChild(img);
    });

    // YouTube videos in gallery
    if (p.youtubeGaleria && p.youtubeGaleria.length > 0) {
      if (galeriaTitle) galeriaTitle.textContent = `Galeria (${galeriaList.length + p.youtubeGaleria.length})`;
      p.youtubeGaleria.forEach(vid => {
        const wrapper = document.createElement('a');
        wrapper.href = `https://www.youtube.com/watch?v=${vid}`;
        wrapper.target = '_blank';
        wrapper.rel = 'noopener noreferrer';
        wrapper.style.cssText = 'position:relative;display:block;border-radius:8px;overflow:hidden;cursor:pointer;';
        wrapper.innerHTML = `
          <img src="https://img.youtube.com/vi/${vid}/hqdefault.jpg" alt="Vídeo" style="width:100%;display:block;aspect-ratio:16/9;object-fit:cover;">
          <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:60px;height:60px;background:rgba(255,0,0,0.85);border-radius:12px;display:flex;align-items:center;justify-content:center;">
            <svg viewBox="0 0 24 24" fill="white" width="28" height="28"><polygon points="6,3 20,12 6,21"/></svg>
          </div>`;
        galeriaEl.appendChild(wrapper);
      });
    }

    // YouTube playlist in gallery
    if (p.youtubePlaylist) {
      const wrapper = document.createElement('a');
      wrapper.href = `https://www.youtube.com/playlist?list=${p.youtubePlaylist}`;
      wrapper.target = '_blank';
      wrapper.rel = 'noopener';
      wrapper.style.cssText = 'position:relative;display:block;border-radius:8px;overflow:hidden;cursor:pointer;grid-column:1/-1;';
      wrapper.innerHTML = `
        <img src="assets/projetos/linha-producoes/capa.avif" alt="Playlist" style="width:100%;display:block;aspect-ratio:16/9;object-fit:cover;">
        <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);display:flex;align-items:center;gap:10px;background:rgba(255,0,0,0.85);border-radius:12px;padding:12px 20px;">
          <svg viewBox="0 0 24 24" fill="white" width="28" height="28"><polygon points="6,3 20,12 6,21"/></svg>
          <span style="color:white;font-weight:600;font-size:14px;">Assistir Playlist Completa</span>
        </div>`;
      galeriaEl.appendChild(wrapper);
    }
  }

  modal.classList.add('active');
  document.body.style.overflow = 'hidden';

  // Focus trap: move focus into modal
  const closeBtn = document.getElementById('modalClose');
  if (closeBtn) closeBtn.focus();
}

let lastFocusedElement = null;

function openModalWithFocus(id) {
  lastFocusedElement = document.activeElement;
  // P3.7: pushState para modal compartilhável + integração com View Transitions (P3.5)
  if (location.hash !== `#projeto-${id}`) {
    history.pushState({ modalId: id }, '', `#projeto-${id}`);
  }
  if (document.startViewTransition) {
    const vt = document.startViewTransition(() => openModal(id));
    // O foco definido dentro do callback da view transition não sobrevive ao
    // clique de mouse que abriu o modal — reaplicar depois que ela termina.
    vt.finished.catch(() => {}).then(() => {
      const closeBtn = document.getElementById('modalClose');
      if (closeBtn && modal.classList.contains('active')) closeBtn.focus();
    });
  } else {
    openModal(id);
  }
}

function closeModal() {
  // P3.7: limpar hash quando fechar
  if (location.hash.startsWith('#projeto-')) {
    history.pushState(null, '', location.pathname + location.search);
  }
  sairTelaCheia();
  const doClose = () => {
    modal.classList.remove('active');
    document.body.style.overflow = '';
    document.getElementById('modalVideo').innerHTML = '';
    if (lastFocusedElement) {
      lastFocusedElement.focus();
      lastFocusedElement = null;
    }
  };
  if (document.startViewTransition) {
    document.startViewTransition(doClose);
  } else {
    doClose();
  }
}

// P3.7: popstate handler — back/forward navega entre modal e site
window.addEventListener('popstate', (e) => {
  const m = location.hash.match(/^#projeto-(\d+)$/);
  if (m) {
    const id = parseInt(m[1]);
    if (!modal.classList.contains('active')) openModal(id);
  } else if (modal.classList.contains('active')) {
    sairTelaCheia();
    modal.classList.remove('active');
    document.body.style.overflow = '';
    document.getElementById('modalVideo').innerHTML = '';
  }
});

// P3.7: ao load, se hash referenciar projeto, abrir modal
document.addEventListener('DOMContentLoaded', () => {
  const m = location.hash.match(/^#projeto-(\d+)$/);
  if (m) openModal(parseInt(m[1]));
});

items.forEach(item => {
  // Accessibility: make items keyboard-navigable
  item.setAttribute('tabindex', '0');
  item.setAttribute('role', 'button');

  const handleItemClick = () => {
    const itemId = parseInt(item.dataset.id);
    if (!isNaN(itemId)) openModalWithFocus(itemId);
  };
  item.addEventListener('click', handleItemClick);
  item.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); handleItemClick(); }
  });

  // Hover video preview
  const id = parseInt(item.dataset.id);
  const projeto = projetos.find(x => x.id === id);
  if (!projeto) return;

  const videosOk = (projeto.videos || []).filter(videoReproduzivel);
  const hasVideos = videosOk.length > 0 || projeto.youtubePlaylist || projeto.youtubeGaleria;
  if (!hasVideos || !videosOk.length) return;

  const firstVideo = videosOk[0];
  if (!firstVideo.url && !firstVideo.youtubeId) return;

  let hoverVideo = null;
  let hoverTimeout = null;
  const thumb = item.querySelector('.trabalhos__thumb');
  const thumbImg = thumb.querySelector('img');
  const playIcon = thumb.querySelector('.trabalhos__play-icon');

  item.addEventListener('mouseenter', () => {
    if (!hoverVideo) {
      if (firstVideo.youtubeId) {
        // YouTube: iframe com autoplay+mute+loop (loop requer playlist=mesmoId)
        const id = encodeURIComponent(firstVideo.youtubeId);
        hoverVideo = document.createElement('iframe');
        hoverVideo.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&mute=1&controls=0&loop=1&playlist=${id}&modestbranding=1&playsinline=1&rel=0&disablekb=1&iv_load_policy=3`;
        hoverVideo.allow = 'autoplay; encrypted-media';
        hoverVideo.setAttribute('frameborder', '0');
        hoverVideo.setAttribute('aria-hidden', 'true');
        hoverVideo.tabIndex = -1;
      } else {
        hoverVideo = document.createElement('video');
        hoverVideo.src = firstVideo.url;
        hoverVideo.muted = true;
        hoverVideo.loop = true;
        hoverVideo.playsInline = true;
        hoverVideo.preload = 'metadata';
      }
      hoverVideo.className = 'trabalhos__hover-video';
      thumb.insertBefore(hoverVideo, playIcon);
    }
    // iframe YouTube: dimensiona com aspect 16:9 cobrindo o thumb (overflow corta excesso)
    if (hoverVideo.tagName === 'IFRAME') {
      const rect = thumb.getBoundingClientRect();
      if (rect.width > 0 && rect.height > 0) {
        const playerAspect = 16 / 9;
        const cardAspect = rect.width / rect.height;
        let w, h;
        if (cardAspect < playerAspect) {
          h = rect.height;
          w = h * playerAspect;
        } else {
          w = rect.width;
          h = w / playerAspect;
        }
        hoverVideo.style.width = `${w}px`;
        hoverVideo.style.height = `${h}px`;
      }
    }
    hoverTimeout = setTimeout(() => {
      if (hoverVideo.tagName === 'IFRAME') {
        hoverVideo.classList.add('active');
        if (thumbImg) thumbImg.style.opacity = '0';
      } else {
        hoverVideo.currentTime = 0;
        hoverVideo.play().then(() => {
          hoverVideo.classList.add('active');
          if (thumbImg) thumbImg.style.opacity = '0';
        }).catch(() => {
          if (hoverVideo) hoverVideo.classList.remove('active');
          if (thumbImg) thumbImg.style.opacity = '1';
        });
      }
    }, 300);
  });

  item.addEventListener('mouseleave', () => {
    clearTimeout(hoverTimeout);
    if (hoverVideo) {
      if (hoverVideo.tagName === 'VIDEO') {
        hoverVideo.pause();
      }
      hoverVideo.classList.remove('active');
      if (thumbImg) thumbImg.style.opacity = '1';
    }
  });
});

// ----------------------------------------
// Helpers de a11y: status messages + pause bg video (WCAG 4.1.3 / 2.2.2)
// ----------------------------------------
function announceStatus(msg) {
  const el = document.getElementById('liveStatus');
  if (!el) return;
  // Force re-announce mesmo se mensagem repete
  el.textContent = '';
  setTimeout(() => { el.textContent = msg; }, 50);
}

(function setupBgVideoToggle() {
  const btn = document.getElementById('bgVideoToggle');
  const video = document.getElementById('globalBgVideo');
  if (!btn || !video) return;
  const pauseIcon = btn.querySelector('.bg-video-toggle__pause');
  const playIcon = btn.querySelector('.bg-video-toggle__play');
  btn.addEventListener('click', () => {
    if (video.paused) {
      video.play().catch(() => {});
      btn.setAttribute('aria-label', 'Pausar vídeo de fundo');
      btn.setAttribute('aria-pressed', 'false');
      pauseIcon.style.display = '';
      playIcon.style.display = 'none';
      announceStatus('Vídeo de fundo retomado.');
    } else {
      video.pause();
      btn.setAttribute('aria-label', 'Retomar vídeo de fundo');
      btn.setAttribute('aria-pressed', 'true');
      pauseIcon.style.display = 'none';
      playIcon.style.display = '';
      announceStatus('Vídeo de fundo pausado.');
    }
  });
})();

// Focus trap helper — wrappa Tab dentro do container ativo (WCAG 2.1.2)
function trapFocus(container, e) {
  if (e.key !== 'Tab') return;
  const focusables = container.querySelectorAll(
    'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
  );
  if (!focusables.length) return;
  const first = focusables[0];
  const last = focusables[focusables.length - 1];
  // Se o foco escapou do diálogo (ou nunca entrou), traz de volta em vez de
  // deixar o Tab percorrer a página por trás do overlay.
  if (!container.contains(document.activeElement)) {
    (e.shiftKey ? last : first).focus();
    e.preventDefault();
    return;
  }
  if (e.shiftKey && document.activeElement === first) {
    last.focus();
    e.preventDefault();
  } else if (!e.shiftKey && document.activeElement === last) {
    first.focus();
    e.preventDefault();
  }
}

modalClose.addEventListener('click', closeModal);
modal.querySelector('.modal__backdrop').addEventListener('click', closeModal);

// Toque no player → tela cheia. O listener fica no container (que persiste entre
// projetos, ao contrário do conteúdo dele) e recebe por bubbling o mesmo clique
// que o lite-youtube usa para trocar o poster pelo iframe.
const modalVideoEl = document.getElementById('modalVideo');
if (modalVideoEl) {
  modalVideoEl.addEventListener('click', e => {
    // A tarja com o nome do talento fica sobre o player e não dá play.
    if (e.target.closest('.modal__video-talent')) return;
    expandirPlayer(modalVideoEl);
  });
}

document.addEventListener('keydown', e => {
  if (playerCinema && e.key === 'Escape') {
    sairModoCinema();
    return;
  }
  if (modal.classList.contains('active')) {
    if (e.key === 'Escape' && !lightbox.classList.contains('active')) closeModal();
    else if (!lightbox.classList.contains('active')) trapFocus(modal, e);
  }
});

// ----------------------------------------
// Showreel lazy embed
// ----------------------------------------
const showreelEl = document.getElementById('showreelVideo');
if (showreelEl) {
  showreelEl.addEventListener('click', () => {
    const vid = showreelEl.dataset.videoId;
    if (vid && vid !== 'VIDEO_ID') {
      const lyt = document.createElement('lite-youtube');
      lyt.setAttribute('videoid', vid);
      lyt.setAttribute('params', 'rel=0&modestbranding=1&mute=1');
      lyt.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;';
      const container = showreelEl.parentNode;
      container.appendChild(lyt);
      showreelEl.remove();
      if (typeof lyt.activate === 'function') {
        requestAnimationFrame(() => lyt.activate());
      }
      expandirPlayer(container);
    }
  });
}

// ----------------------------------------
// Scroll reveal
// ----------------------------------------
const revealElements = document.querySelectorAll('.sobre__image, .sobre__content, .trabalhos__header, .trabalhos__item, .showreel__container, .cta__content, .cta__quote, .contato__left, .contato__form, .quote__inner, .marcas__container');

if ('IntersectionObserver' in window) {
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  let trabalhoIdx = 0;
  revealElements.forEach(el => {
    el.classList.add('reveal');
    // Stagger reveal pra cards trabalhos — cascata visual (P2.5)
    if (el.classList.contains('trabalhos__item')) {
      el.style.setProperty('--i', trabalhoIdx % 6);
      trabalhoIdx++;
    }
    revealObserver.observe(el);
  });
} else {
  // Fallback: show all elements immediately
  revealElements.forEach(el => el.classList.add('reveal', 'visible'));
}

// ----------------------------------------
// Marcas -> Modal
// ----------------------------------------
// Custom cursor "PLAY" (P3.3) — só visível sobre cards de vídeo
(function setupCustomCursor() {
  if (window.matchMedia('(hover: none)').matches) return;
  if (window.matchMedia('(pointer: coarse)').matches) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const cursor = document.createElement('div');
  cursor.className = 'custom-cursor';
  cursor.setAttribute('aria-hidden', 'true');
  document.body.appendChild(cursor);
  let raf;
  // Tracking só ativa quando o cursor está sobre um card (poupa rAF fora)
  document.querySelectorAll('.trabalhos__item').forEach(item => {
    item.addEventListener('mouseenter', () => cursor.classList.add('cursor--play'));
    item.addEventListener('mouseleave', () => cursor.classList.remove('cursor--play'));
    item.addEventListener('mousemove', (e) => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        cursor.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
      });
    });
  });
})();

// Magnetic hover em CTAs (P3.4) — translate sutil seguindo o cursor
(function setupMagneticCTAs() {
  if (window.matchMedia('(hover: none)').matches) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const targets = document.querySelectorAll('.btn, .header__cta');
  targets.forEach(el => {
    el.addEventListener('mouseenter', () => {
      // Durante hover, transform reage rápido pra acompanhar mousemove sem lerp
      // Ordem CSS: background, color, border-color, box-shadow, transform
      el.style.transitionDuration = '0.3s, 0.3s, 0.3s, 0.3s, 0.08s';
    });
    el.addEventListener('mousemove', (e) => {
      const rect = el.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      el.style.transform = `translate(${x * 0.14}px, ${y * 0.14}px)`;
    });
    el.addEventListener('mouseleave', () => {
      // No mouseleave restaura transition mais lenta e zera transform → lerp suave
      el.style.transitionDuration = '';
      el.style.transform = '';
    });
  });
})();

document.querySelectorAll('.marcas__item').forEach(item => {
  item.setAttribute('tabindex', '0');
  item.setAttribute('role', 'button');
  // Sem isto o nome acessível era só a marca ("Drogasil"), sem dizer o que o
  // clique faz — o equivalente, para leitores de tela, do "Ver projeto" que o
  // hover mostra.
  const marca = item.dataset.name;
  if (marca) item.setAttribute('aria-label', `Ver projeto — ${marca}`);

  const handleClientClick = () => {
    lastFocusedElement = document.activeElement;
    if (item.dataset.ids) {
      const ids = item.dataset.ids.split(',').map(Number);
      const projs = ids.map(id => projetos.find(p => p.id === id)).filter(Boolean);
      if (projs.length === 1) {
        openModalWithFocus(projs[0].id);
        return;
      }
      showProjectPicker(projs);
      return;
    }
    const marcaName = item.dataset.name || item.textContent.trim();
    const projeto = projetos.find(p => p.nome.toLowerCase() === marcaName.toLowerCase());
    if (projeto) {
      openModalWithFocus(projeto.id);
    }
  };

  item.addEventListener('click', handleClientClick);
  item.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); handleClientClick(); }
  });
});

// Project picker for clients with multiple projects
function showProjectPicker(projs) {
  const existing = document.getElementById('projectPicker');
  if (existing) existing.remove();

  const picker = document.createElement('div');
  picker.id = 'projectPicker';
  picker.className = 'picker-overlay';
  picker.innerHTML = `
    <div class="picker-backdrop"></div>
    <div class="picker-content">
      <h3 class="picker-title">Escolha o projeto</h3>
      <div class="picker-options">
        ${projs.map(p => `
          <button class="picker-option" data-id="${p.id}">
            <span class="picker-option-name">${escapeHTML(p.nome)}</span>
            <span class="picker-option-label">${escapeHTML(p.categoriaLabel)}</span>
          </button>
        `).join('')}
      </div>
    </div>
  `;
  document.body.appendChild(picker);
  requestAnimationFrame(() => picker.classList.add('active'));

  const fecharPicker = () => {
    picker.classList.remove('active');
    document.removeEventListener('keydown', onPickerKeydown);
    setTimeout(() => picker.remove(), 300);
    if (lastFocusedElement) lastFocusedElement.focus();
  };
  function onPickerKeydown(e) {
    if (e.key === 'Escape') fecharPicker();
    else trapFocus(picker, e);
  }
  document.addEventListener('keydown', onPickerKeydown);

  picker.querySelector('.picker-backdrop').addEventListener('click', fecharPicker);
  const primeiraOpcao = picker.querySelector('.picker-option');
  if (primeiraOpcao) primeiraOpcao.focus();

  picker.querySelectorAll('.picker-option').forEach(btn => {
    btn.addEventListener('click', () => {
      picker.classList.remove('active');
      document.removeEventListener('keydown', onPickerKeydown);
      setTimeout(() => picker.remove(), 300);
      openModalWithFocus(parseInt(btn.dataset.id));
    });
  });
}

// ----------------------------------------
// Form
// ----------------------------------------
// O e-mail fica quebrado em data-user/data-dominio e só é remontado quando
// alguém clica. Montá-lo no carregamento deixaria o endereço no DOM, onde
// raspadores que executam JavaScript ainda o encontrariam; exigindo interação,
// ele não existe em lugar nenhum até uma pessoa de verdade pedir.
function montarEmail(el) {
  const user = el?.dataset.user;
  const dominio = el?.dataset.dominio;
  return (user && dominio) ? `${user}@${dominio}` : '';
}

// Seção Contato: botão "Mostrar e-mail" vira o endereço clicável.
document.querySelectorAll('.email-revelar').forEach(botao => {
  botao.addEventListener('click', () => {
    const endereco = montarEmail(botao);
    if (!endereco) return;
    const link = document.createElement('a');
    link.href = 'mailto:' + endereco;
    link.textContent = endereco;
    botao.replaceWith(link);
    // Mantém o teclado no lugar: quem acionou o botão continua no elemento
    // que tomou o seu lugar, em vez de perder o foco para o body.
    link.focus();
    if (typeof announceStatus === 'function') announceStatus('E-mail exibido: ' + endereco);
  });
});

// Rodapé: o ícone abre o cliente de e-mail no primeiro clique, sem etapa extra.
document.querySelectorAll('.email-abrir').forEach(link => {
  link.addEventListener('click', (e) => {
    const endereco = montarEmail(link);
    if (!endereco) return;
    e.preventDefault();
    window.location.href = 'mailto:' + endereco;
  });
});

// String aleatória do FormSubmit ("Invisible emails"): substitui o endereço de
// destino na URL, então o e-mail não existe em nenhum ponto do front-end — nem
// no HTML, nem aqui. Só o FormSubmit sabe para onde encaminhar.
// Para trocar de destino, gere uma nova string confirmando outro endereço lá.
const FORMSUBMIT_TOKEN = '6c5430f84d0c32ffe3e7e326393fcb61';

function endpointFormSubmit(viaAjax) {
  return 'https://formsubmit.co/' + (viaAjax ? 'ajax/' : '') + FORMSUBMIT_TOKEN;
}

const contatoForm = document.getElementById('contatoForm');
if (contatoForm) {
  // Preenche o action para preservar o submit nativo como fallback; o envio
  // normal continua sendo via fetch, logo abaixo.
  contatoForm.setAttribute('action', endpointFormSubmit(false));


  contatoForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const btn = form.querySelector('button[type="submit"]');
    const status = document.getElementById('formStatus');
    const originalText = btn.textContent;
    // Espelha o texto do botão na região aria-live para leitores de tela.
    const anunciar = (msg) => { btn.textContent = msg; if (status) status.textContent = msg; };
    anunciar('Enviando...');
    btn.disabled = true;

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);

    try {
      const res = await fetch(endpointFormSubmit(true), {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' },
        signal: controller.signal
      });
      clearTimeout(timeout);

      if (res.ok) {
        anunciar('Mensagem enviada!');
        form.reset();
        setTimeout(() => {
          btn.textContent = originalText;
          btn.disabled = false;
        }, 3000);
      } else {
        throw new Error('Erro no envio');
      }
    } catch (err) {
      clearTimeout(timeout);
      if (err.name === 'AbortError') {
        anunciar('Tempo esgotado. Tente novamente.');
      } else if (!navigator.onLine) {
        anunciar('Sem conexão. Verifique sua internet.');
      } else {
        anunciar('Erro ao enviar. Tente novamente.');
      }
      btn.disabled = false;
      setTimeout(() => { btn.textContent = originalText; }, 3000);
    }
  });
}

// ----------------------------------------
// Lightbox Fullscreen (Photo Gallery)
// ----------------------------------------
const lightbox = document.getElementById('lightbox');
const lightboxTrack = document.getElementById('lightboxTrack');
const lightboxCounter = document.getElementById('lightboxCounter');
const lightboxClose = document.getElementById('lightboxClose');
const lightboxPrev = document.getElementById('lightboxPrev');
const lightboxNext = document.getElementById('lightboxNext');

let lbImages = [];
let lbIndex = 0;
let touchStartX = 0;
let touchEndX = 0;

// Clicar numa <img> (não focável) faz o Chromium limpar o foco para o body
// depois dos handlers — o que anularia o focus() do lightbox. Suprimir o
// comportamento padrão do mousedown preserva o foco que definimos no JS.
document.addEventListener('mousedown', e => {
  if (e.target.closest('.modal__galeria img, .modal__video-card')) e.preventDefault();
});

// Quem abriu o lightbox, para devolver o foco ao fechar (senão ele cai no body
// e o usuário de teclado volta ao topo da página).
let lbLastFocused = null;

function openLightbox(images, startIndex) {
  lbLastFocused = document.activeElement;
  lbImages = images;
  lbIndex = startIndex || 0;
  showLightboxImage();
  lightbox.classList.add('active');
  document.body.style.overflow = 'hidden';
  if (lightboxClose) lightboxClose.focus();
}

function closeLightbox() {
  lightbox.classList.remove('active');
  // Only restore overflow if modal is not open
  if (!modal.classList.contains('active')) {
    document.body.style.overflow = '';
  }
  lightboxTrack.innerHTML = '';
  if (lbLastFocused && document.contains(lbLastFocused)) lbLastFocused.focus();
  lbLastFocused = null;
}

// Fotos da galeria são <img> puras: sem isto o lightbox só abre por mouse.
function tornarFotoAcessivel(img, lista, indice, nomeProjeto) {
  img.tabIndex = 0;
  img.setAttribute('role', 'button');
  img.setAttribute('aria-label', `Ampliar foto ${indice + 1} de ${lista.length} — ${nomeProjeto}`);
  img.addEventListener('click', () => openLightbox(lista, indice));
  img.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openLightbox(lista, indice); }
  });
}

function showLightboxImage() {
  const img = document.createElement('img');
  img.src = lbImages[lbIndex];
  img.alt = `Foto ${lbIndex + 1}`;
  img.onerror = function() { this.alt = 'Imagem indisponível'; this.style.opacity = '0.3'; };
  lightboxTrack.innerHTML = '';
  lightboxTrack.appendChild(img);
  lightboxCounter.textContent = `${lbIndex + 1} / ${lbImages.length}`;
  lightboxPrev.style.display = lbImages.length > 1 ? '' : 'none';
  lightboxNext.style.display = lbImages.length > 1 ? '' : 'none';
}

function lightboxGoTo(dir) {
  lbIndex = (lbIndex + dir + lbImages.length) % lbImages.length;
  showLightboxImage();
}

lightboxClose.addEventListener('click', closeLightbox);
lightbox.querySelector('.lightbox__backdrop').addEventListener('click', closeLightbox);
lightboxPrev.addEventListener('click', () => lightboxGoTo(-1));
lightboxNext.addEventListener('click', () => lightboxGoTo(1));

document.addEventListener('keydown', (e) => {
  if (!lightbox.classList.contains('active')) return;
  if (e.key === 'Escape') closeLightbox();
  if (e.key === 'ArrowLeft') lightboxGoTo(-1);
  if (e.key === 'ArrowRight') lightboxGoTo(1);
  trapFocus(lightbox, e);
});

// Touch swipe support
lightboxTrack.addEventListener('touchstart', (e) => {
  touchStartX = e.changedTouches[0].screenX;
}, { passive: true });

lightboxTrack.addEventListener('touchend', (e) => {
  touchEndX = e.changedTouches[0].screenX;
  const diff = touchStartX - touchEndX;
  if (Math.abs(diff) > 50) {
    lightboxGoTo(diff > 0 ? 1 : -1);
  }
}, { passive: true });

// ----------------------------------------
// "Carregar Mais" — limita projetos visíveis
// ----------------------------------------
(function() {
  const grid = document.getElementById('trabalhosGrid');
  const loadMoreBtn = document.getElementById('loadMoreBtn');
  const loadMoreWrap = loadMoreBtn ? loadMoreBtn.parentElement : null;
  if (!grid || !loadMoreBtn) return;

  const allItems = Array.from(grid.querySelectorAll('.trabalhos__item'));

  // Um clique só despejava os 44 projetos de uma vez. Agora o botão revela um
  // lote por vez e diz quantos ainda faltam.
  let limite = PROJETOS_POR_PAGINA;

  const doFiltroAtual = () => allItems.filter(i => !i.classList.contains('hidden'));

  function applyLimit() {
    const visiveis = doFiltroAtual();
    visiveis.forEach((item, i) => { item.style.display = i < limite ? '' : 'none'; });
    allItems.forEach(item => {
      if (item.classList.contains('hidden')) item.style.display = 'none';
    });

    const restantes = visiveis.length - limite;
    if (loadMoreWrap) loadMoreWrap.classList.toggle('hidden', restantes <= 0);
    if (restantes > 0) {
      const lote = Math.min(restantes, PROJETOS_POR_PAGINA);
      loadMoreBtn.textContent = `Carregar mais ${lote} (${restantes} restantes)`;
    }
  }

  applyLimit();

  loadMoreBtn.addEventListener('click', () => {
    const antes = limite;
    limite += PROJETOS_POR_PAGINA;
    applyLimit();

    const visiveis = doFiltroAtual();
    // Sem isto o foco cai no body quando o botão some no último lote — e mesmo
    // quando ele fica, o teclado perde o lugar na grade.
    const primeiroNovo = visiveis[antes];
    if (primeiroNovo) {
      primeiroNovo.setAttribute('tabindex', primeiroNovo.getAttribute('tabindex') || '0');
      primeiroNovo.focus({ preventScroll: true });
    }
    if (typeof announceStatus === 'function') {
      const exibidos = Math.min(limite, visiveis.length);
      announceStatus(exibidos >= visiveis.length
        ? `Todos os ${visiveis.length} projetos foram carregados.`
        : `Exibindo ${exibidos} de ${visiveis.length} projetos.`);
    }
  });

  // Re-apply on filter change
  filtros.forEach(btn => {
    btn.addEventListener('click', () => {
      limite = PROJETOS_POR_PAGINA;
      setTimeout(applyLimit, 10);
    });
  });
})();

// ----------------------------------------
// CTA de contato dentro do modal
// ----------------------------------------
(function() {
  const modalBody = document.querySelector('.modal__body');
  if (!modalBody) return;

  const existingCTA = modalBody.querySelector('.modal__contact-cta');
  if (existingCTA) return;

  const cta = document.createElement('a');
  cta.href = '#contato';
  cta.className = 'btn modal__contact-cta';
  cta.textContent = 'Solicitar Orçamento';
  cta.style.cssText = 'display:inline-block;margin-top:32px;';
  cta.addEventListener('click', (e) => {
    e.preventDefault();
    closeModal();
    setTimeout(() => {
      document.getElementById('contato').scrollIntoView({ behavior: 'smooth' });
    }, 400);
  });
  modalBody.appendChild(cta);
})();

// ----------------------------------------
// Hover video cleanup — remove após 5s de mouseleave
// ----------------------------------------
(function() {
  const MAX_CACHED = 3;
  const cachedVideos = [];

  document.querySelectorAll('.trabalhos__item').forEach(item => {
    item.addEventListener('mouseleave', () => {
      const video = item.querySelector('.trabalhos__hover-video');
      if (!video) return;
      cachedVideos.push({ el: video, item: item });
      while (cachedVideos.length > MAX_CACHED) {
        const oldest = cachedVideos.shift();
        if (oldest.el && oldest.el.parentNode) {
          if (oldest.el.tagName === 'VIDEO') {
            oldest.el.pause();
            oldest.el.removeAttribute('src');
            oldest.el.load();
          } else if (oldest.el.tagName === 'IFRAME') {
            // Para parar o player YouTube e liberar recursos
            oldest.el.src = 'about:blank';
          }
          oldest.el.remove();
        }
      }
    });
  });
})();

// ----------------------------------------
// Filtro por URL — ?filtro=fotografia#trabalhos
// ----------------------------------------
// A página de serviços linka para categorias específicas do portfólio. Em vez de
// duplicar a lógica de filtro, dispara um clique real no botão correspondente:
// assim tanto o filtro quanto a paginação reagem exatamente como no clique do
// usuário. Fica no fim do arquivo de propósito — os dois listeners (filtro e
// "Carregar Mais") já estão registrados a esta altura.
(function() {
  const filtroURL = new URLSearchParams(window.location.search).get('filtro');
  if (!filtroURL) return;

  const btn = document.querySelector(`.trabalhos__filtro[data-filter="${CSS.escape(filtroURL)}"]`);
  if (!btn || btn.classList.contains('active')) return;

  btn.click();

  // O href da página de serviços já traz #trabalhos, mas o navegador rola até a
  // âncora antes do filtro rodar — e a grade encurta debaixo do usuário. Rolar
  // de novo aqui recoloca a seção no lugar certo.
  const secao = document.getElementById('trabalhos');
  if (secao && window.location.hash === '#trabalhos') {
    secao.scrollIntoView({ behavior: 'auto', block: 'start' });
  }
})();
