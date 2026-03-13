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
      "Cliente": "Garagem Coletiva",
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
      "Cliente": "Devassas",
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
      "Cliente": "Warner Music UK",
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
      "Cliente": "Warner Music Brasil",
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
      "Cliente": "Casinha Acolhida / Ambev",
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
      "Cliente": "Casinha Acolhida / Doritos",
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
      "Cliente": "Linha Produções",
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
      "Cliente": "Força da Terra",
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
      "Cliente": "Doutora Drag",
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
      "Cliente": "Apsa",
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
      "Cliente": "Casinha Acolhida",
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
      "Cliente": "Irmãos Scribel",
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
      "Cliente": "Irmãos Scribel",
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
      "Cliente": "ONG Casinha Acolhida",
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
      "Cliente": "Dalla Cervejaria",
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
      "Cliente": "BRAX Sports Assets",
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
      "Cliente": "Teçá - Arte e Cultura",
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
      "Cliente": "Espetáculo Entretenimento",
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
    descricao: "Produção remota de projetos audiovisuais junto à equipe da agência, elaborando identidade visual para os projetos dos clientes e tendo participação na execução estratégica dos conteúdos focados em resultados de engajamento.",
    ficha: {
      "Função": "Videomaker e Designer",
      "Cliente": "Agência Imaginatto",
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
      "Cliente": "Doutora Drag / Dimitra Vulcana",
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
      "Cliente": "Clínica Imagem Integrada",
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
      "Cliente": "Linha Produções",
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
      "Cliente": "Força da Terra",
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
      "Cliente": "Devassas",
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
      "Cliente": "Coletiva Garagem",
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
      "Cliente": "Drogasil",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Período": "Fev - Ago 2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/07f45d42-291f-40b1-8a89-598cfac9a63e/%5B07%5D%5BP02%5D%5BNN%5D%20Raia%20-%20Drogasil%20Varejar_v1_29s_Daniela.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559070957&amp;usg=AOvVaw2P-ruilgXtdg2tSbagQrkv", direcao: true, talento: "Daniela Castelo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/0dd44d27-5cc6-413b-85f0-01516aa0f085/%5B05%5D%5BP02%5D%5BNN%5D%20Raia%20-%20Drogasil%20Varejar_v5_29s_Debora_Mel.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559071835&amp;usg=AOvVaw0Qw0oqmTu8hCVqZrtI-Y0v", talento: "Débora Melo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/490bc9f6-647d-45f3-9fcf-55f34b5195b9/%5B06%5D%5BP02%5D%5BNN%5D%20Raia%20-%20Drogasil%20Varejar_v3_32s_DeboraMelo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559072704&amp;usg=AOvVaw2l4nCnmg6u8G3ErTwvhWu-", talento: "Débora Melo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/ead54170-dfb6-4a08-b64a-f9641fe0ad13/%5B04%5D%5BP02%5D%5BNN%5D%20Raia%20-%20Drogasil%20Varejar_v5_Daniela%20Castelo_55s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559073871&amp;usg=AOvVaw2NXYiqMXV_gKFOebLZuW2q", talento: "Daniela Castelo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/247f3721-3bd1-41d3-af5f-95f81ab39a9c/%5B03%5D%5BP02%5D%5BNN%5D%20Raia%20-%20Drogasil%20Varejar_v2_24s_Frederico_Volkmann.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559074856&amp;usg=AOvVaw2XidhjZ7y7vvsRGGPI5teQ", talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/a9aae3b7-c5ee-4170-890d-1cf0f4cf642f/%5B10%5D%5BP02%5D%5BNN%5D%20Raia%20-%20Drogasil%20Varejar_v3_46s_Frederico.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559075756&amp;usg=AOvVaw0cYn6DvVlsGEpWant77GBu", talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/09a62d04-bbd1-448c-a32c-a4b237cca86e/%5B02%5D%5BP02%5D%5BNN%5D%20Raia%20-%20Drogasil%20Varejar_v2_41s_Quezia.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559076828&amp;usg=AOvVaw2OSUP2F_LPYYsqWXq0-R-z", direcao: true, talento: "Quézia Castro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/62def742-ba4c-4010-875e-17372125481d/%5B08%5D%5BP02%5D%5BNN%5D%20Raia%20-%20Drogasil%20Varejar_v4_37s_Quezia%20Fernandes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559077816&amp;usg=AOvVaw0bUQRUaQACM5SOPpdvilKN", direcao: true, talento: "Quézia Castro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c3104f63-b86f-4658-bc7d-14e8acc5bd91/%5B01%5D%20%5BP05%5D%5BNN%5D%20RAIA%20%20Drogasil%20Dia%20das%20M%C3%A3es_v3_39s_Clara_Giffoni.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559078751&amp;usg=AOvVaw1V2rio7bR09Lt8OKzSm62j", talento: "Clara Giffoni" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/bee811b5-5ca4-4573-987c-8396bd0f9b02/%5B01%5D%20%5BP04%5D%5BNN%5D%20RAIA%20%20%20Drogasil%20-%20Bond%20Repair_v3_21s_Julia%20Helen.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559079596&amp;usg=AOvVaw20z_w2IMrbJ1HQzuWjd79T", talento: "Julia Helen" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/cd45e2da-7e21-49b3-9543-e2a8f48468da/%5B07%5D%20%5BP04%5D%5BNN%5D%20RAIA%20%20%20Drogasil%20-%20Bond%20Repair_v3_44s_Julia%20Helen.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559080631&amp;usg=AOvVaw2qFsguGwa5PwI6u8GS2LCu", talento: "Julia Helen" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/0e1888cc-e6ea-418d-8575-3126f762799c/%5B09%5D%5BP04%5D%5BNN%5D%20RAIA%20%7C%20Drogasil%20-%20Bond%20Repair_v2_41s_JuliaHelen.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559081577&amp;usg=AOvVaw3DVRXp7tMjWh1uiQOYqi9Z", talento: "Julia Helen" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c4becab0-59ab-40f2-ba78-cbc750adf986/%5B13%5D%20%5BP04%5D%5BNN%5D%20RAIA%20%20Drogasil%20-%20Bond%20Repair_v4_38s_JULIA_HELEN.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559082633&amp;usg=AOvVaw2dnbdSlKdoJEebBg_yh5G-", talento: "Julia Helen" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/ae3cfc34-b38b-4221-b366-304ca23af65d/%5B06%5D%20%5BP09%5D%5BNN%5D%20RAIA%20Dia%20dos%20namorados%20Drogasil_v4_44s_LARISSA_VENTURINI.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559083632&amp;usg=AOvVaw1TLjBkZR7LMLOxxGe3kcuZ", direcao: true, talento: "Larissa Venturini" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/79772753-a2b4-4174-8a18-84f21cb77949/%5B03%5D%20%5BP09%5D%5BNN%5D%20RAIA%20%20%20Dia%20dos%20namorados%20-%20Drogasil_v2_39s_Larissa%20Venturini.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559084621&amp;usg=AOvVaw241K-VIaFNkCpMFF-VnlJ6", direcao: true, talento: "Larissa Venturini" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/3c7c68df-8f82-4d37-adce-34c2f8d45b11/%5B02%5D%20%5BP09%5D%5BNN%5D%20RAIA%20%20%20Dia%20dos%20namorados%20-%20Drogasil_v2_54s_Larissa%20Venturini.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559085633&amp;usg=AOvVaw139FsF1sY-lmkrheGyqiYG", direcao: true, talento: "Larissa Venturini" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/48e8e70d-d861-498c-bb0f-af163512beaa/%5B01%5D%20%5BP09%5D%5BNN%5D%20RAIA%20-%20Dia%20dos%20namorados%20-%20Drogasil_v5_50s_LarissaVenturini.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559086625&amp;usg=AOvVaw166jUcVfGaj3CNCwWgiMco", direcao: true, talento: "Larissa Venturini" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/f93d09fc-5f7c-4b85-927c-5da62f2b9af1/essa%20%C3%A9%20a%20matem%C3%A1tica%20que%20eu%20gosto_v1_30s-Yago.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559087567&amp;usg=AOvVaw1fDgNZSyJnW4gHuJNCBW0r", talento: "Yago Capita" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c0fb5c15-f73c-4300-b2cc-ebed92430e62/%5B01%5D%20%5BP14%5D%5BNN%5D%20RAIA%20%20Black%20Fraldas%20-%20Drogasil_v3_31s_Andrei_Lamberg.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559088449&amp;usg=AOvVaw2mSo4SWSCC7nrSUxO237iH", talento: "Andrei Lamberg" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/8b326ba4-5a6f-40f1-937c-58b103f7f844/%5B06%5D%20%5BP14%5D%5BNN%5D%20RAIA%20-%20Black%20Fraldas%20-%20Drogasil_v2_18s_Andrei.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559089302&amp;usg=AOvVaw0PbWe85vDVRO0pTYpqCKo5", talento: "Andrei Lamberg" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/2b49c1f5-0e2d-487e-9811-7bd6a39d472e/%5B07%5D%20%5BP14%5D%5BNN%5D%20RAIA%20%20%20Black%20Fraldas%20-%20Drogasil_v3_41s_Andrei%20Lamberg.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559090187&amp;usg=AOvVaw0_cHJvxuwYhaFomkZnuJ1t", talento: "Andrei Lamberg" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/3710b9ee-6bfc-4548-93a7-74da1e850806/%5B01%5D%20%5BP16%5D%5BNN%5D%20RAIA%20%20%20AlwaysOn%20Perfumaria%20JUL%20-%20Drogasil_v1_35s_Murillo%20Amorim.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559091105&amp;usg=AOvVaw29m4wZWgF7e0cmnjYFTDCB", talento: "Murilo Amorim" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/dc824298-c28c-4157-aa59-70e8ab8cadcd/%5B03%5D%20%5BP16%5D%5BNN%5D%20RAIA%20-%20AlwaysOn%20Perfumaria-JUL%20-%20Drogasil_v3_35s_Murillo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559091987&amp;usg=AOvVaw0gvH3ceOcfsWo2-UolJKxp", talento: "Murilo Amorim" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c7166ae2-bb72-4064-bb6c-1c61a8c73106/%5B04%5D%20%5BP16%5D%5BNN%5D%20RAIA%20AlwaysOn%20PerfumariaJUL%20-%20Drogasil_v1_45s_Murilo_Amorim.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559092891&amp;usg=AOvVaw0LmkvvuzFrHhko92GfbVe3", talento: "Murilo Amorim" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/1d34b5fe-bf4b-4ab2-a7b8-2c437cafcc22/%5B08%5D%20%5BP16%5D%5BNN%5D%20RAIA%20%20AlwaysOn%20PerfumariaJUL%20-%20Drogasil_v2_20s_Murilo_Amorim.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559093943&amp;usg=AOvVaw3p5QF01WogDmNEgMuQ6ccg", talento: "Murilo Amorim" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/ab86e5c3-c371-4fac-a756-9a8ee04fd452/%5B05%5D%20%5BP16%5D%5BNN%5D%20RAIA%20%20AlwaysOn%20PerfumariaJUL%20-%20Drogasil_v6_52s_Thays_Godinho_Ribeiro.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559095136&amp;usg=AOvVaw3M5aTUbL18ny0reHYrHIzN", talento: "Thays Godinho Ribeiro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/7bb85e4c-3da2-4f4a-851e-38a557a8ef46/%5B02%5D%20%5BP16%5D%5BNN%5D%20RAIA%20%20%20AlwaysOn%20Perfumaria%20JUL%20-%20Drogasil_v3_47s_Thays%20Godinho%20Ribeiro.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559096092&amp;usg=AOvVaw0XLvfFBFOp2c1QDkUqpBAt", talento: "Thays Godinho Ribeiro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/8bba1e70-e456-4bb7-b034-6c61a4f4d031/%5B06%5D%20%5BP16%5D%5BNN%5D%20RAIA%20%20%20AlwaysOn%20Perfumaria%20JUL%20-%20Drogasil_v2_36s_Thays%20Godinho.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559096966&amp;usg=AOvVaw15djCgfaGPZPh1059D57lL", talento: "Thays Godinho Ribeiro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/49cdcbcf-3014-4424-9949-f91745ed7c34/%5B07%5D%20%5BP16%5D%5BNN%5D%20RAIA%20%20AlwaysOn%20PerfumariaJUL%20-%20Drogasil_v3_38s_Thays_Godinho.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559097859&amp;usg=AOvVaw39ElrtM3Eidjc-Dik5Cvfk", talento: "Thays Godinho Ribeiro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/3d579141-eb4f-405d-961a-37bc0ab40207/%5B01%5D%20%5BP18%5D%5BNN%5D%20RAIA%20%20%20Autosservi%C3%A7o%20AlwaysOn%20Infantil%20-%20Drogasil_v2_34s_Anny%20Melo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559098791&amp;usg=AOvVaw0pLQYPP6XW7EAk9I9dEYyj", talento: "Anny Melo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/41aa8c31-8550-40ae-b765-a2432cdb6828/%5B02%5D%20%5BP18%5D%5BNN%5D%20RAIA%20-%20Autosservi%C3%A7o%20AlwaysOn%20Infantil%20-%20Drogasil_v2_42s_Anny_Melo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559099700&amp;usg=AOvVaw07dpLEuY73mGxNNvxEKmW5", talento: "Anny Melo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/34eb3b92-a76b-457b-831f-a268bf24caac/%5B03%5D%20%5BP18%5D%5BNN%5D%20RAIA%20%20%20Autosservi%C3%A7o%20AlwaysOn%20Infantil%20-%20Drogasil%20_v1_55s_Qu%C3%A9ren-hapuque.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559100784&amp;usg=AOvVaw23rSII1_xXIaQuovpZzw8H", direcao: true, talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/9eaeb63a-7ce8-489f-b18b-e861ac4a9c28/%5B04%5D%20%5BP18%5D%5BNN%5D%20RAIA%20%20%20Autosservi%C3%A7o%20AlwaysOn%20Infantil%20-%20Drogasil%20_v1_57s_Anny%20Melo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559101750&amp;usg=AOvVaw3zxwZo6Hk3U8BBFcxHoEkD", talento: "Anny Melo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/29e4a983-ded1-47f7-82de-8a3aa86864f0/%5B05%5D%20%5BP18%5D%5BNN%5D%20RAIA%20%20%20Autosservi%C3%A7o%20AlwaysOn%20Infantil%20-%20Drogasil_v2_19s_Anny.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559102668&amp;usg=AOvVaw0JO9Ut6d4bCix_AXcCPKxT", talento: "Anny Melo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/789b04e3-6b88-4974-9d8f-213ee8028021/%5B06%5D%20%5BP18%5D%5BNN%5D%20RAIA%20%20%20Autosservi%C3%A7o%20AlwaysOn%20Infantil%20-%20Drogasil_v3_54s_Qu%C3%A9ren-hapuque%20Fernandes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559103595&amp;usg=AOvVaw2sXo3vXwyXrB2T_MpCLwLA", direcao: true, talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/da80564b-0524-4867-a10b-73843a2293e5/%5B07%5D%20%5BP18%5D%5BNN%5D%20RAIA%20%20%20Autosservi%C3%A7o%20AlwaysOn%20Infantil%20-%20Drogasil_v1_30s_Qu%C3%A9ren.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559104543&amp;usg=AOvVaw3v_OmQXPsVh9r2GrzT8MQZ", direcao: true, talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/3e3195e1-e0ee-46fc-a886-6856fd0e2bde/%5B08%5D%20%5BP18%5D%5BNN%5D%20RAIA%20%20Autosservi%C3%A7o%20AlwaysOn%20Infantil%20-%20Drogasil_v3_48s_Queren.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559105473&amp;usg=AOvVaw28HrXR71F-9osiXRRh9X5M", direcao: true, talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c8c556b6-0093-4209-a248-a66875a0d537/%5B01%5D%20%5BP20%5D%5BNN%5D%20RAIA%20-%20Cuidado%20que%20vale%20mais%20-%20Drogasil_v4_49s_LiviaLima.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559106323&amp;usg=AOvVaw0rXUr2aNcauH3StvDCt-Q7", talento: "Lívia Lima" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/6fdba7a5-0a0d-4bf5-b3ef-f42d3d6f08d6/%5B02%5D%20%5BP20%5D%5BNN%5D%20RAIA%20%20%20Cuidado%20que%20vale%20mais%20%20%20Drogasil_v2_46s_frederico.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559107258&amp;usg=AOvVaw1BCEZQIyLwFOiw7F9gheGQ", talento: "Lívia Lima" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/88069cee-c153-4fb8-9beb-5c78b91ae99b/%5B03%5D%20%5BP20%5D%5BNN%5D%20RAIA%20%20%20Cuidado%20que%20vale%20mais%20%20%20Drogasil_v2_53s_Frederico%20Volkmann.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559108133&amp;usg=AOvVaw135BUyWiTCNW06C0NflzOR", talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/056e9f78-7ab7-40b5-ba52-c7171a7cc5d3/%5B04%5D%20%5BP20%5D%5BNN%5D%20RAIA%20%20%20Cuidado%20que%20vale%20mais%20%20%20Drogasil_v3_43s_Livia%20Lima.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559109029&amp;usg=AOvVaw1xc4DbwOxUyD9sOxX6_AH5", talento: "Lívia Lima" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/62111e2b-7407-416d-b6b4-232e148dcd52/%5B05%5D%20%5BP20%5D%5BNN%5D%20RAIA%20-%20Cuidado%20que%20vale%20mais%20-%20Drogasil_v3_31s_Frederico.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559109927&amp;usg=AOvVaw0lme_pKoBC5dYBC2PlqhHn", talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/fb442bcf-693a-4ecd-9bc9-b2c3921f3587/%5B06%5D%20%5BP20%5D%5BNN%5D%20RAIA%20-%20Cuidado%20que%20vale%20mais%20-%20Drogasil_v3_46s_FredericoVolkaman.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559110883&amp;usg=AOvVaw2RtFDmg9w23IepY0GIDWXv", talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/1a961381-bb06-48ee-8b2e-ce5095f51597/%5B07%5D%20%5BP20%5D%5BNN%5D%20RAIA%20Cuidado%20que%20vale%20mais%20Drogasil_v5_51_Livia_Lima.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559111891&amp;usg=AOvVaw1Kxj1GY0ATalvN-aSfrKiH", talento: "Lívia Lima" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/098d04f3-811a-43da-b6dd-8d6736c95601/%5B08%5D%20%5BP20%5D%5BNN%5D%20RAIA%20Cuidado%20que%20vale%20mais%20Drogasil_v1_36s_Frederico_Volkmann.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559112760&amp;usg=AOvVaw0WXMG6ZX3P-aCng9pDugvO", talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/7ab15ea3-e80c-417e-a3cf-6ddca79ef23e/%5B01%5D%20%5BP22%5D%5BNN%5D%20RAIA%20-%20OTC%20-%20Ciclo%20Gripal%20%20Drogasil_v6_54s_Yago.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559113657&amp;usg=AOvVaw1eaVIPl3lRtRcCQMGxnj_U", talento: "Yago Capita" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b74a83ba-ddc4-4454-8a75-8b8ad0d2269f/%5B03%5D%20%5BP22%5D%5BNN%5D%20RAIA%20-%20OTC%20-%20Ciclo%20Gripal%20%20Drogasil_v4_34s_Yago.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559114531&amp;usg=AOvVaw0G9iobjyKfBks7pHA3rHOF", talento: "Yago Capita" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/7b8b98ea-c3ab-483b-abb0-09a73d03fd23/%5B07%5D%20%5BP22%5D%5BNN%5D%20RAIA%20%20%20OTC%20-%20Ciclo%20Gripal%20%20Drogasil_v3_34s_Yago%20Capita.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559115410&amp;usg=AOvVaw2wyJ4FQA5z97FbfrpZKfiD", talento: "Yago Capita" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/74b8cdf1-a505-4b53-87b2-b92182165310/%5B08%5D%20%5BP22%5D%5BNN%5D%20RAIA%20OTC%20Ciclo%20Gripal%20Drogasil_v4_48s_Yago_Capita.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559116376&amp;usg=AOvVaw20Mg6JLwZ-Tg88sAESr_Hl", talento: "Yago Capita" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b5ce8235-b15c-4172-893f-336054717aa5/%5B03%5D%20%5BP24%5D%5BNN%5D%20RAIA%20-%20Marcas%20Coreanas%20-%20Drogasil_v2_27s_Carolina_cruz.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559117310&amp;usg=AOvVaw0ZCBE-6DRudqnAsDHN_WX_", talento: "Carolina Cruz" }
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
      "Cliente": "Mercado Pago",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Período": "Mar - Out 2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/4ad93d6f-324b-4cf4-9c7d-e675d7874324/%5B07%5D%20%5BP36%5D%5BCH%5DMercado%20Pago%20-%20TTCX-TESTES-SELLERS_v5_9s_NaluMoura.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559187447&amp;usg=AOvVaw1vTv-AqE_bHXXWZPO2MNDm", direcao: true, talento: "Nalu Moura" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/e82ccb06-502a-484d-b369-d61c964d4c80/%5B08%5D%20%5BP36%5D%5BCH%5DMercado%20Pago%20-%20TTCX-TESTE-SELLERS_v4_53s_NaluMoreira.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559188501&amp;usg=AOvVaw1xqg44mol2ygC64sTgjCvW", direcao: true, talento: "Nalu Moura" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/2663a671-a0c2-4a68-8bbf-86f3824922e5/%5B07%5D%20%5BP39%5D%5BCH%5D%20MERCADO%20PAGO%20%20%20MLB%20%20%20Junio%20Users_v3_39s_Nalu%20Moura.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559189452&amp;usg=AOvVaw1s51FIsW82Gv2-w4bU66ig", talento: "Nalu Moura" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/6feda22c-7685-4e54-99e1-ef45163ea2e1/%5B21%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO_v1_30s_Daniela_Castelo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559190522&amp;usg=AOvVaw1JXO1khTUPDMpaLivn9pKO", talento: "Daniela Castelo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/01a6445e-935d-45cf-9931-aeb58dd425bc/%5B22%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20-%20MLB%20-%20Individuals%20Sep-Oct_v2_22s_Daniela_castelo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559191494&amp;usg=AOvVaw0ea23aNJzz6JDLvxdlah1D", talento: "Daniela Castelo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/15dbfa46-cce5-4a90-8b8a-e08387c6c968/%5B23%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20%20%20MLB%20%20%20Individuals%20Sep%20Oct_v1_31s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559192414&amp;usg=AOvVaw1Ihx78TajKejBdBgos627u", talento: "Daniela Castelo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/f90a997c-972d-40c3-8e69-4fe42661841d/%5B24%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20-%20MLB%20-%20Individuals%20Sep-Oct_v3_35s_DanielaCastelo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559193380&amp;usg=AOvVaw3lnqMlEU_fUivqPxh_UdjE", talento: "Daniela Castelo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/3817b547-4709-4fd1-915a-df78cd565ea5/%5B25%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20%20%20MLB%20%20%20Individuals%20Sep%20Oct_v2_37s_Raphael%20Monteiro.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559194528&amp;usg=AOvVaw0ps6C030pEOM7Z7FGp_R4X", direcao: true, talento: "Raphael Monteiro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/4f1a2bd1-feb0-4605-a829-bfec3f8badd2/%5B26%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20-%20MLB%20-%20Individuals%20Sep-Oct_v3_23s_RhafaelMonteiro.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559195461&amp;usg=AOvVaw10wS0fkQfXVeLLaUJf9uzE", talento: "Raphael Monteiro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/5ae24548-5fbd-4c3a-9188-6d1b23b91fb7/%5B27%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20%20%20MLB%20%20%20Individuals%20Sep%20Oct_v2_28s_Raphael%20Monteiro.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559196457&amp;usg=AOvVaw2FUfZkyeJWdDSuAhks82Ct", talento: "Raphael Monteiro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/86d232d2-f0cb-45ef-b068-493e969114cc/%5B28%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20-%20MLB%20-%20Individuals%20Sep-Oct_v3_23s_RhafaelMonteiro.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559197506&amp;usg=AOvVaw3UAMxeti7ihSvI6vDcBDnB", talento: "Raphael Monteiro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b19ef0f9-e55d-4913-bbd3-ce05bad37cf4/%5B29%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO_v3_30s_Maria_Sousa.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559198439&amp;usg=AOvVaw1Jd4zFchYXYCg5MhGjoOsV", talento: "Maria Souza" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/1f98f2f9-ed54-49ee-b5fd-15268731889b/%5B30%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20%20%20MLB%20%20%20Individuals%20Sep%20Oct_v3_33s_Joa%CC%83o%20Mendes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559199333&amp;usg=AOvVaw1H1WmVGA7HJru5_M90JLRi", talento: "João Mendes" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/04a1f8d0-41cf-48b9-8a53-e5c454aaec9c/%5B31%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20%20%20MLB%20%20%20Individuals%20Sep%20Oct_v1_24s_Maria%20Eduarda.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559200229&amp;usg=AOvVaw2tTAeRGXDNoUQcUiGDiitc", talento: "Maria Souza" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/8d97fcde-a8e9-45dd-a9d2-356ab049cd39/%5B32%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20%20%20MLB%20%20%20Individuals%20Sep%20Oct_v2_22s_Maria%20Eduarda%20Sousa.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559201258&amp;usg=AOvVaw0r64xicGzkqkJdlR6O2wA5", talento: "Maria Souza" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/4057363d-c0b7-46d9-a403-3965887b3167/%5B33%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO_v3_30s_Joao_Mendes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559202336&amp;usg=AOvVaw0KP-e4YXdyygYiqOasDjCT", talento: "João Mendes" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/cf7dc35f-6609-4f54-b8b9-16cbc1aa1da1/%5B34%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20-%20MLB%20-%20Individuals%20Sep-Oct_v2_20s_Jo%C3%A3oMendes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559203348&amp;usg=AOvVaw0fqzY99XDQH5C06FqwHESW", talento: "João Mendes" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/16bb4105-0140-4c44-a45a-39b00149ef2e/%5B35%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20%20%20MLB%20%20%20Individuals%20Sep%20Oct%20_v1_13s_Jo%C3%A3o%20Mendes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559204320&amp;usg=AOvVaw3oj1iuec0ynwsG5dPd-CqB", talento: "João Mendes" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/2a124479-533c-4059-a48c-670761dfa0a2/%5B36%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20%20%20MLB%20%20%20Individuals%20Sep%20Oct_v2_30s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559205345&amp;usg=AOvVaw3Bfy3riTORLB1Lmaw-wfwq", talento: "Maria Souza" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/eb542d1e-790c-4f60-bddd-a97863713ee2/%5B45%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20MLB%20Individuals%20Sep-Oct_v2_19s_Loretta%20Martins.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559206354&amp;usg=AOvVaw0Yie2WtEOnFPh9hr32aoXw", talento: "Loretta Martins" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/4eb27e4a-410d-47cf-9e6c-b8fe22c2d024/%5B46%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20-%20MLB%20-%20Individuals%20Sep-Oct_v3_27sLorettaMartins.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559207330&amp;usg=AOvVaw3xDeeR5be0UEwOGV1vF_VT", talento: "Loretta Martins" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/8838206c-8763-4809-a047-9dab2d1b426a/%5B47%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20-%20MLB%20-%20Individuals%20Sep-Oct_v3_23s_Loretta_martins.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559208316&amp;usg=AOvVaw37gWzz2YU6nAMF8u6LjsrT", talento: "Loretta Martins" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/41b606a4-1aab-4bf9-802a-023072e95820/%5B48%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20%20%20MLB%20%20%20Individuals%20Sep%20Oct_v4_35s_Loretta%20Martins.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559209312&amp;usg=AOvVaw0Bq8cqw48A6ROE8QIxlsu4", talento: "Loretta Martins" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/948d953c-f3f4-49bc-89b2-3f33fd5a45d2/%5B49%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20-%20MLB%20-%20Individuals%20Sep-Oct_v2_25s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559210267&amp;usg=AOvVaw1LqUOwIIkNMnhYpE0UGyJI", talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/2a696331-5819-4768-89b8-3c02b5c90553/%5B50%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20%20%20MLB%20%20%20Individuals%20Sep%20Oct_v1_29s_frederico.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559211226&amp;usg=AOvVaw0nrnCHNhJxGzCP5a-tmb_k", talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/fdc70a95-88a8-4098-94eb-dc436ba7d535/%5B51%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20%20%20MLB%20%20%20Individuals%20Sep%20Oct_v2_23s_Frederico.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559212142&amp;usg=AOvVaw2kLrD-IIUJNdS8br3_hUXF", talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/7260d6e5-49d5-4aed-9b0c-5fa7bc316381/%5B52%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20-%20MLB%20-%20Individuals%20Sep-Oct_v4_22s_FredericoVolkam.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559213100&amp;usg=AOvVaw3gAbc94RVHmo-0e1-LAXZf", talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c11674a3-aef8-44e5-a997-4b37066c57e5/%5B53%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20-%20MLB%20-%20Individuals%20Sep-Oct_v3_21s_RenenTeiva.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559213990&amp;usg=AOvVaw13RklT9bMExeOobE3ihkZo", talento: "Renan Teiva" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/1d187cff-08de-4d54-a855-95286f2ef289/%5B54%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20-%20MLB%20-%20Individuals%20Sep-Oct_v3_20s_Renan_Telva.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559214907&amp;usg=AOvVaw1QkhF_oZrhQvh_i3o8eCgj", talento: "Renan Teiva" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/043aff5c-68bb-441c-8d2c-6761e93aa12a/%5B55%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO%20MLB%20Individuals%20SepOct_v2_28s_Renan%20Teiva.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559215970&amp;usg=AOvVaw07_Z6Z6L6anS1ayiprJv8O", talento: "Renan Teiva" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/035b2783-7663-4771-9ce5-3f9aea82c056/%5B56%5D%20%5BP44%5D%5BCH%5D%20MERCADO%20PAGO_v1_27s_Renan_Teiva.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559216908&amp;usg=AOvVaw1o4oHpIcLy7MW1AVLQxOa0", talento: "Renan Teiva" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c3188400-804c-42da-8422-d9311a1fc42c/%5B01%5D%20%5BP45%5D%5BNN%5D%20MERCADO%20PAGO%20-%20Mercado%20Pago%20-%20Tap%201_v3_35s_Vit%C3%B3ria_Rodrigues.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559217856&amp;usg=AOvVaw3FUkLHk8rGYT9c5CkcAA82", talento: "Vitória Rodrigues" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/2a84f06f-1f22-4de3-a886-e5a31b238ee3/%5B02%5D%20%5BP45%5D%5BNN%5D%20MERCADO%20PAGO_v3_31s_Raphael_Monteiro.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559218833&amp;usg=AOvVaw2qligG2FAfuq-twvfs9IVh", talento: "Raphael Monteiro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/d6e68c5c-6bba-4c7c-976d-cd865cff9aef/%5B03%5D%20%5BP45%5D%5BNN%5D%20MERCADO%20PAGO%20Mercado%20Pago_v1_27s_.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559219889&amp;usg=AOvVaw2o3DgDq4ZfVzwkokAmgfzE", talento: "Raphael Monteiro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/afac0389-7e1a-46f6-9a08-517a8fce8226/%5B04%5D%20%5BP45%5D%5BNN%5D%20MERCADO%20PAGO%20Mercado%20Pago_v2_28s_Vit%C3%B3ria_Rodrigues.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559220936&amp;usg=AOvVaw2r7-SmA_hQa6YxF9GrLLAt", talento: "Vitória Rodrigues" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/39ff43f4-b67a-41e1-ac40-d567fb73d6f0/%5B05%5D%20%5BP45%5D%5BNN%5D%20MERCADO%20PAGO%20%20%20Mercado%20Pago%20-%20Tap%201_v2_22s_Raphael.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559222000&amp;usg=AOvVaw2db4Mu2CBDg8JjWb7nj0dI", talento: "Raphael Monteiro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/0f43def5-5d95-4962-b12e-122c1ee5cdea/%5B06%5D%20%5BP45%5D%5BNN%5D%20MERCADO%20PAGO%20-%20Mercado%20Pago%20-%20Tap%201_v4_27s_VitoriaRodrigues.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559223010&amp;usg=AOvVaw0ZPDHoFQrhrObrAdTs_JYs", talento: "Vitória Rodrigues" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/1dcbe017-b1ec-4f72-ba21-af99b7cdddcc/%5B08%5D%20%5BP45%5D%5BNN%5D%20MERCADO%20PAGO%20-%20Mercado%20Pago%20-%20Tap%201_v2_17s_Vit%C3%B3ria_rodrigres.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559224001&amp;usg=AOvVaw1X5sPUumE8h4mf-QNtSSGl", talento: "Vitória Rodrigues" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/80bf703b-774f-4a8b-afcb-30d57ea20c79/%5B01%5D%20%5BP46%5D%5BNN%5D%20MERCADO%20PAGO%20%20%20Mercado%20Pago%20Point%20Smart_v2_30s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559224979&amp;usg=AOvVaw0jUtGixisdQ4uVLHz29jbP", talento: "Antônio Bastos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/54c9827a-f82b-4f68-82d8-4f5ac42868ad/%5B02%5D%20%5BP46%5D%5BNN%5D%20MERCADO%20PAGO%20-%20Mercado%20Pago%20Point%20Smart_v2_56s_MarceloKlain.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559225886&amp;usg=AOvVaw3ZuSObcxkpKpdQO8AcRd3l", talento: "Marcelo Klein" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/33f49b5e-bf3f-4f91-acda-de90820b9050/%5B03%5D%20%5BP46%5D%5BNN%5D%20MERCADO%20PAGO%20%20%20Mercado%20Pago%20Point%20Smart_v3_14s_Marcelo%20Klein.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559226893&amp;usg=AOvVaw1ZW7OR4cymeB7uBQjsBpHU", talento: "Marcelo Klein" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/83424729-87e8-4d9a-be72-1a9475581949/%5B04%5D%20%5BP46%5D%5BNN%5D%20MERCADO%20PAGO%20%20%20Mercado%20Pago%20Point%20Smart_v1_21s_Antonio%20Bastos.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559227841&amp;usg=AOvVaw1I12f0sQxzgEgldoqlVlO-", talento: "Antônio Bastos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/517ec2f7-ae21-4eeb-8390-aecda6d16048/%5B05%5D%20%5BP46%5D%5BNN%5D%20MERCADO%20PAGO%20-%20Mercado%20Pago%20Point%20Smart_v3_26s_AntonioBastos.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559228802&amp;usg=AOvVaw19jT8YLi_txTqwcN0POmz_", talento: "Antônio Bastos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/f9e9a0da-1a7a-421d-9920-485367d9250a/%5B06%5D%20%5BP46%5D%5BNN%5D%20MERCADO%20PAGO_v3_55s_Marcelo_Klein.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559229723&amp;usg=AOvVaw2Kmoq1g-BlxoxMuz9E3iER", talento: "Marcelo Klein" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/83f1ceca-92fc-4d61-a332-ea9beb344607/%5B07%5D%20%5BP46%5D%5BNN%5D%20MERCADO%20PAGO%20%20%20Mercado%20Pago%20Point%20Smart_v3_33s_.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559230791&amp;usg=AOvVaw2zT8zb3wLdb5ZCcFUosWUA", talento: "Marcelo Klein" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/fe91369a-69f5-4188-b5c3-4bc423650efd/%5B08%5D%20%5BP46%5D%5BNN%5D%20MERCADO%20PAGO%20-%20Mercado%20Pago%20Point%20Smart_v2_29s_antonio_basto.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559231758&amp;usg=AOvVaw2lHfLEVN8gByxXn124DNl-", talento: "Antônio Bastos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/a56a5731-59da-4c0a-aabb-dadbe43d0862/%5B02%5D%20%5BP47%5D%5BNN%5D%20MERCADO%20PAGO%20Mercado%20Pago_v2_35s_Daniela_Caste.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559232708&amp;usg=AOvVaw2CkSv7nPipDsW_1-uC9xRT", talento: "Daniela Castelo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/bd445597-d09a-450f-a245-a8f28bdafdde/%5B05%5D%20%5BP47%5D%5BNN%5D%20MERCADO%20PAGO%20-%20Mercado%20Pago%20-%20Conta%20PJ%20(2025-09-04)_v3_39s_Andr%C3%A9_Lemos.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559233686&amp;usg=AOvVaw1GpvKBLVQbWGwBBctgKt3M", talento: "André Lemos" }
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
      "Cliente": "Magazine Luiza",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b8379034-823e-415a-8167-91e1b5b29621/%5B04%5D%20%5BP51%5D%5BCH%5D%20MAGALU%20%20Top%20View%20Payday%20Abril%2025_v1_45s_Leticia_Machado.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559261038&amp;usg=AOvVaw0n5CBcfQ1ZsuSpSCqbPjDk", talento: "Letícia Machado" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/18004192-c81d-42c5-aeb2-840e557ccdf6/%5B05%5D%20%5BP50%5D%5BCH%5D%20MAGALU%20%20%20PayDay%20Abril%2025_v2_27s_Karol.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559262287&amp;usg=AOvVaw0NmQE0uYY7cQ4HEls5UAny", direcao: true, talento: "Karol Alves" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/ce8a0043-b5e6-4bd3-9212-c23b2648380d/%5B04%5D%20%5BP50%5D%5BCH%5D%20MAGALU%20%20%20PayDay%20Abril%2025_v1_41s_Julia%20Helen.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559263421&amp;usg=AOvVaw2p6bN0Fj4Qho1k96GmoPQN", direcao: true, talento: "Julia Helen" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/58d95c7b-ee5f-46b1-85b0-67c1e1e57401/%5B06%5D%20%5BP50%5D%5BCH%5D%20MAGALU%20%20%20PayDay%20Abril%2025_v3_27s_Karol.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559264523&amp;usg=AOvVaw3B3gJmDBZ2yl84Cb_e5xND", direcao: true, talento: "Karol Alves" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b0570488-b981-432f-b704-0de17b24d743/%5B16%5D%20%5BP50%5D%5BCH%5D%20MAGALU%20-%20PayDay%20Abril%2025_v3_32s_Julia_helen.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559265701&amp;usg=AOvVaw3IpDkhGsm8S3g7CowNIylG", direcao: true, talento: "Julia Helen" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/1e54fd04-3717-4e6a-97f6-7270719ef538/%5B15%5D%20%5BP50%5D%5BCH%5D%20MAGALU%20%20%20PayDay%20Abril%2025_v2_20s_Drico.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559266907&amp;usg=AOvVaw3mpLufzkiyH2mNwxAjOdFz", direcao: true, talento: "Drico Alves" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/57be187b-2301-4800-bcea-041a2b69139b/%5B10%5D%20%5BP50%5D%5BCH%5D%20MAGALU%20-%20PayDay%20Abril%2025_v2_20s_Drico_alves.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559268059&amp;usg=AOvVaw2d2ICdvg2vVOnIZSq2l1DF", direcao: true, talento: "Drico Alves" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/d17e58f2-3d32-46e4-8747-ca57fd6775f3/%5B09%5D%20%5BP53%5D%5BCH%5D%20MAGALU%20-%20Magalu%20-%20REVIEW%20DE%20PRODUTO_v3_58s_DricoAlvez_1.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559269073&amp;usg=AOvVaw1k40c_RqiUnzyljCJCQieG", talento: "Drico Alves" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/48bae3bc-4b84-48ca-8d1f-6ed4cbaf4c4f/%5B04%5D%20%5BP53%5D%5BCH%5D%20MAGALU%20%7C%20Magalu%20-%20REVIEW%20DE%20PRODUTO_v3_33s_SamiaAbreu.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559270096&amp;usg=AOvVaw1Y_JJZ35eiugqAKvA3eEDE", talento: "Samia Abreu" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/9262d2c6-77ce-41d6-8ff9-9405105a7281/%5B08%5D%20%5BP53%5D%5BCH%5D%20MAGALU%20-%20Magalu%20-%20REVIEW%20DE%20PRODUTO_v4_44s_Drico_Alves.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559271156&amp;usg=AOvVaw0w6Y5Ri6EgJKfA2061jYBg", talento: "Drico Alves" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/4cb78576-d1ef-4e8b-ba2c-2eb241652e77/%5B03%5D%20%5BP53%5D%5BCH%5D%20MAGALU%20%20Magalu%20-%20REVIEW%20DE%20PRODUTO_v3_30s_Samia_Abreu.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559272251&amp;usg=AOvVaw2TzHXepKhoNis4uUJsVQ5X", talento: "Samia Abreu" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/038b463a-4f6f-4650-8aae-8ce2f6254cf8/%5B02%5D%20%5BP53%5D%5BCH%5D%20MAGALU%20%20%20Magalu%20-%20REVIEW%20DE%20PRODUTO_v1_29s_Pedro%20Pires.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559273325&amp;usg=AOvVaw3t-cdgJMOifOJaVSMHyNvJ", talento: "Pedro Pires" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/e483e880-8734-4377-a828-2a78eb640565/%5B03%5D%20%5BP56%5D%5BNN%5D%20MAGALU%20%20S%C3%A3o%20Jo%C3%A3o%20-%20Junho%2025_v2_37s_Bruna_Noronha.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559274462&amp;usg=AOvVaw2CTIh8cX8urLmyx1vSYrZT", direcao: true, talento: "Bruna Noronha" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/283101a3-ac65-4297-bc8b-c77cc1c33292/%5B04%5D%20%5BP56%5D%5BNN%5D%20MAGALU%20%20S%C3%A3o%20Jo%C3%A3o%20-%20Junho%2025_v1_29s_BRUNA_NORONHA.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559275591&amp;usg=AOvVaw0zdcD5D_oD-kMLUUD2g6PH", direcao: true, talento: "Bruna Noronha" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/34654a9b-5ef4-4571-991f-05cd6884a31a/%5B02%5D%20%5BP56%5D%5BNN%5D%20MAGALU%20%20%20S%C3%A3o%20Jo%C3%A3o%20-%20Junho%2025_v2_31s_Bruna%20Noronha.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559276716&amp;usg=AOvVaw2daFI70BYOB8_zN3Uu07K5", direcao: true, talento: "Bruna Noronha" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/7f43d893-416f-4637-9af8-982d7679d750/%5B01%5D%20%5BP56%5D%5BNN%5D%20MAGALU%20%20%20S%C3%A3o%20Jo%C3%A3o%20-%20Junho%2025_v1_21s_Bruna%20Noronha.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559277807&amp;usg=AOvVaw2vIYw1HsVRcA2kJ6KD3CP0", direcao: true, talento: "Bruna Noronha" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/209641c3-bc70-4e1a-ac7a-9ec6e10a6638/%5B01%5D%20%5BP57%5D%5BNN%5D%20MAGALU%20-%20Compra%20Premiada%20Magalu_v2_37s_LaraGay.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559278843&amp;usg=AOvVaw2zL8LbvilOGmovkusWfvm3", talento: "Lara Gay" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/36ef0115-2795-4ccc-a7e2-92f3a54f8851/%5B02%5D%20%5BP57%5D%5BNN%5D%20MAGALU%20%20%20Compra%20Premiada%20Magalu_v2_32s_Lara.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559279810&amp;usg=AOvVaw1tylrfFZbr3BUHJ_XLoDgs", talento: "Lara Gay" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/2a6f2fbf-0e1f-4855-8edd-e5ba5f95599d/%5B03%5D%20%5BP57%5D%5BNN%5D%20MAGALU%20%20%20Compra%20Premiada%20Magalu_v6_47s_Lara%20Gay.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559280911&amp;usg=AOvVaw1xtcuqkKJRLDIY9YHBXMnr", talento: "Lara Gay" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/cd0501a4-081d-4567-8fe0-b03ca4fb9ad6/%5B04%5D%20%5BP57%5D%5BNN%5D%20MAGALU%20-%20Compra%20Premiada%20Magalu_v4_32s_Lara_Gay.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559281882&amp;usg=AOvVaw39VC4IbjydvaqcnI4FI9F6", talento: "Lara Gay" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/7d53f17e-597e-4c40-8a0d-e46a33c7db0d/%5B02%5D%20%5BP58%5D%5BNN%5D%20MAGALU%20-%20Compra%20Premiada%20Magalu%20Agosto_v5_25s_Qu%C3%A9ren%20Hapuque.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559282909&amp;usg=AOvVaw2q7VXNKQjmEPiQze-u70d9", talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/86995a8c-d093-4d31-8870-dd98631ffbd7/%5B03%5D%20%5BP58%5D%5BNN%5D%20MAGALU%20Compra%20Premiada_v2_29s_Queren_Hapuque.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559284062&amp;usg=AOvVaw31K6Ray_PQSpsdFpRGCf_m", talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/067106bc-9d0c-4dbe-bc36-378dec984b57/%5B04%5D%20%5BP58%5D%5BNN%5D%20MAGALU%20-%20Compra%20Premiada%20Magalu%20Agosto_v4_30s_Qu%C3%A9ren%20Hapuque.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559285128&amp;usg=AOvVaw2N33D6qaNAGomXhqH-g0sJ", talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/03db00e3-f763-44fd-a87d-671a1edcaa86/%5B01%5D%20%5BP61%5D%5BNN%5D%20%20%20%20Magalu%20Black%20das%20Blacks_v3_21s_Lara.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559286215&amp;usg=AOvVaw2l_oEhybRqfbDwGhEuwupH", talento: "Lara Gay" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/74dd3028-06f1-4e30-bf83-f00deb7874d3/%5B02%5D%20%5BP61%5D%5BNN%5D%20%20%20%20Magalu%20Black%20das%20Blacks_v3_21s_Lara.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559287291&amp;usg=AOvVaw2F6E2uHmNAiVOGHEhaHWqB", talento: "Lara Gay" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/9e114541-6ddd-49c5-bed3-228dde5cc846/%5B03%5D%20%5BP61%5D%5BNN%5D%20%20-%20Magalu%20Black%20das%20Blacks_v3_19s_Lara_Gay.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559288301&amp;usg=AOvVaw07ILOenMjIqtSXG04vuZRe", talento: "Lara Gay" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/dd01e4b1-ffc3-44fe-b7f7-783a05b31225/%5B04%5D%20%5BP61%5D%5BNN%5D%20%20-%20Magalu%20Black%20das%20Blacks_v5_16sLaraGay.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559289296&amp;usg=AOvVaw0_18sabtmghJEyJpe_k_W4", talento: "Lara Gay" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/d966c754-468a-4c81-960e-c728716d8b37/%5B01%5D%20%5BP90%5D%5BNN%5D%20MAGALU%20%20%20Magalu%20Black%20das%20Blacks_v4_44s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559290467&amp;usg=AOvVaw1R8mCnHx1_4Tk22dzkpmEJ", talento: "Lara Gay" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/cb2c3bda-eaf6-4a2e-84fd-85bdbb502a71/%5B02%5D%20%5BP90%5D%5BNN%5D%20MAGALU%20%20%20Magalu%20Black%20das%20Blacks_v5_25s_Lara%20Gay.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559291606&amp;usg=AOvVaw1yiXI-OJTl9RTfDDm36tTg", talento: "Lara Gay" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/562f993b-0c65-4f93-8053-06d91a74f498/%5B03%5D%20%5BP90%5D%5BNN%5D%20MAGALU%20-%20Magalu%20Black%20das%20Blacks_v1_26s_LaraGay.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559292622&amp;usg=AOvVaw1kxnvVfYcyGo5UZIByrlME", talento: "Lara Gay" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/e3d6b8bb-a9e0-476b-a06a-0bb0fc4102fe/%5B04%5D%20%5BP90%5D%5BNN%5D%20MAGALU%20%20%20Magalu%20Black%20das%20Blacks_v5_27s_Lara.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559293747&amp;usg=AOvVaw1jVhvzFh3rEbVUZT7jVHam", talento: "Lara Gay" }
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
      "Cliente": "Raia",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Período": "Mar - Ago 2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/ec910313-cab0-4ce1-8f2b-ecd1bf90d895/%5B10%5D%5BP01%5D%5BNN%5D%20Raia%20-%20Raia%20Varejar_v2_34s_Loretta%20Martins.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559118199&amp;usg=AOvVaw18pkd5GMx-KXRJ6A9_-0-m", talento: "Loretta Martins" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/e224f812-3cac-4ed1-abb3-805451551d51/%5B08%5D%5BP01%5D%5BNN%5D%20Raia%20-%20Raia%20Varejar_v2_23_Loretta%20Martins.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559119056&amp;usg=AOvVaw1QJLYjYDNv_kzK1OCRUyPi", talento: "Loretta Martins" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/4aaf3b12-86c9-4f0e-8dc5-eb25448b8de0/%5B05%5D%5BP01%5D%5BNN%5D%20Raia%20-%20Raia%20Varejar_v3_38s_Frederico%20Volkmann.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559119896&amp;usg=AOvVaw3M3xiSRpP1es44dYSTrFcV", talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/641aa6a0-a186-48d1-87b7-54cb45e77128/%5B09%5D%5BP01%5D%5BNN%5D%20Raia%20-%20Raia%20Varejar_v42_40s_Frederico.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559120761&amp;usg=AOvVaw1-I38q1pntCCdjcuRkFGef", talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/1c006628-7b04-43e8-b3b6-6d784b3c1cbf/%5B01%5D%5BP01%5D%5BNN%5D%20Raia%20-%20Raia%20Varejar_v3_31s._Quezia%20Fernandes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559121766&amp;usg=AOvVaw2_4VfGSWsLByAHIyZDmovM", direcao: true, talento: "Quézia Castro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/514abac4-fcd7-404d-adde-6c1e6f654e2e/%5B04%5D%5BP01%5D%5BNN%5D%20Raia%20-%20Raia%20Varejar_v2_48s_QueziaFernandesDeCastro.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559122699&amp;usg=AOvVaw3HO6g50ffRvpyWkV7LLv0k", direcao: true, talento: "Quézia Castro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/65492609-9233-494e-a082-57aae25f5f81/%5B02%5D%5BP01%5D%5BNN%5D%20Raia%20-%20Raia%20Varejar_v9_55s_AnaClaudiaPadilha.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559123561&amp;usg=AOvVaw24eEs35WX9I8n0XykhVU_C", talento: "Ana Claudia Padilha" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c3104f63-b86f-4658-bc7d-14e8acc5bd91/%5B01%5D%20%5BP05%5D%5BNN%5D%20RAIA%20%20Drogasil%20Dia%20das%20M%C3%A3es_v3_39s_Clara_Giffoni.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559124546&amp;usg=AOvVaw21MuIf2s80Dyy1HPBdxY72", talento: "Clara Giffoni" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/e296eaf5-a6bf-4a18-9a30-6994d5b2fa9e/%5B02%5D%20%5BP06%5D%5BNN%5D%20RAIA%20-Raia-Dia-das-Maes-_v5_54s_FredericoVolkamn.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559125564&amp;usg=AOvVaw3jIVfNUGogLQZjdYqcxnqo", direcao: true, talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/8658e096-9603-40cb-98ab-0053f40a4f33/%5B07%5D%20%5BP06%5D%5BNN%5D%20RAIA%20%20%20Raia%20Dia%20das%20M%C3%A3es_v2_44s_Frederico%20Volkmann.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559126570&amp;usg=AOvVaw3r4YhfMyVsz28tjChTStvk", direcao: true, talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/4a6a1e27-4d28-48c5-9aad-08c9664b6a7e/%5B08%5D%20%5BP06%5D%5BNN%5D%20RAIA%20-%20Raia%20Dia%20das%20M%C3%A3es_v5_46s_Frederico_Volkmann.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559127633&amp;usg=AOvVaw14b6p-4RuZ4Ncvw-ltnXtE", direcao: true, talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/ee256f93-b3d4-41a2-94d9-789bc2a23862/%5B06%5D%20%5BP06%5D%5BNN%5D%20RAIA%20Raia%20Dia%20das%20M%C3%A3es_v3_39s_Frederico%20Volkmann.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559128716&amp;usg=AOvVaw3ndfVHzMyNg0aTU25VNRiL", direcao: true, talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/718d321e-cba7-44cd-a3a8-62bba22e206c/%5B04%5D%20%5BP06%5D%5BNN%5D%20RAIA%20%20Raia%20Dia%20das%20M%C3%A3es_v4_50s_CLARA%20GIFONI.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559129678&amp;usg=AOvVaw1gSeUj6D2AubVMrZrfg9eB", talento: "Clara Giffoni" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/2b2f6599-3c29-43cf-b19d-68d197cab5a9/%5B04%5D%20%5BP07%5D%5BNN%5D%20RAIA%20%20%20Ciclo%20gripal%20OTC%20-%20Raia_v2_59s_Quezia.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559130735&amp;usg=AOvVaw1u-Ym5TwzYTwXIJ1n7EBsl", direcao: true, talento: "Quézia Castro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/bb82715b-b3a1-4c59-898d-930ac4a1d9cc/%5B02%5D%20%5BP07%5D%5BNN%5D%20RAIA%20-%20Ciclo%20gripal%20OTC%20-%20Raia_v4_48s_Quezia_Fernandes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559131768&amp;usg=AOvVaw2zn0Co0q6JJeIksA5ePhVG", direcao: true, talento: "Quézia Castro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/6cf51d0c-75a0-4d7e-9536-c26e52ce74aa/%5B05%5D%20%5BP07%5D%5BNN%5D%20RAIA%20%20%20Ciclo%20gripal%20OTC%20-%20Raia_v5_58s_Quezia%20Fernandes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559132726&amp;usg=AOvVaw0Vp_YgdE4FD9JloP2KncDx", direcao: true, talento: "Quézia Castro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/f4b9c99f-d042-4eb6-afd1-9c72429446cf/%5B08%5D%20%5BP07%5D%5BNN%5D%20RAIA%20%20%20Ciclo%20gripal%20OTC%20-%20Raia%20_v4_40s_Quezia.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559133710&amp;usg=AOvVaw08fEfa0LJ1HdVI_B0_M3vI", direcao: true, talento: "Quézia Castro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/7cd1e6b7-9a1c-4fe6-8b9e-31d22c39628f/%5B05%5D%20%5BP10%5D%5BNN%5D%20RAIA%20%20%20Dia%20dos%20namorados%20Raia_v3_43s_Frederico%20Volkmann.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559134711&amp;usg=AOvVaw1Hfw8wWWvoiHQ1KHbGgfTv", direcao: true, talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/73eb8b44-e303-457e-8ac8-d606b50d0041/%5B04%5D%20%5BP10%5D%5BNN%5D%20RAIA%20%20%20Dia%20dos%20namorados%20Raia_v2_41s_Frederico%20Volkmann.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559135737&amp;usg=AOvVaw1dZzwyqcS_qjiVvNfNUswb", direcao: true, talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/984bdef6-2eae-4322-a834-eae4f6fa8bb3/%5B06%5D%20%5BP10%5D%5BNN%5D%20RAIA%20%20%20Dia%20dos%20namorados%20Raia_v3_25s_Frederico.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559136662&amp;usg=AOvVaw2C0NzBJWAWUgrgmb1Vvj1I", talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/dfffdb35-1f1e-480a-bfac-442cd5fdd7df/%5B06%5D%20%5BP12%5D%5BNN%5D%20RAIA%20-%20Needs%20Raia_v4_33s_Carol_Gomes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559137582&amp;usg=AOvVaw2SahJyVfD-2QKUae0vGTVH", direcao: true, talento: "Carol Gomes" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/4e9a4ea6-f15e-4764-8463-866dc939dea8/%5B01%5D%20%5BP12%5D%5BNN%5D%20RAIA%20%20%20Needs%20Raia_v1_39s_Carol%20Gomes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559138462&amp;usg=AOvVaw0QeorhQ3l9FggMs-rzR-RO", talento: "Carol Gomes" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/0f7c567e-4513-4740-9c9b-19908998ad36/%5B08%5D%20%5BP12%5D%5BNN%5D%20RAIA%20-%20Needs%20Raia_v3_58s_Carol_Gomes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559139327&amp;usg=AOvVaw0XiTiNjjansyoUc3B5DrJO", talento: "Carol Gomes" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/eb73d759-130e-4102-8592-b6692ea926f8/%5B03%5D%20%5BP12%5D%5BNN%5D%20RAIA%20%20%20Needs%20Raia_v2_47s_Carol%20Gomes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559140217&amp;usg=AOvVaw3aoPi1OyDCUZX7sm1FKLst", talento: "Carol Gomes" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c1ece51c-6e53-4151-950e-fe0d72c520df/%5B01%5D%20%5BP13%5D%5BNN%5D%20RAIA%20%20%20Black%20Fraldas%20-%20Raia_v2_24s_Carolina.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559141276&amp;usg=AOvVaw2r62Yf7G1LgKhzVa1dUHsr", talento: "Carolina Malagutti" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/d88c1d84-4b16-40bc-a142-b5d3a04d9013/%5B05%5D%20%5BP13%5D%5BNN%5D%20RAIA%20%20Black%20Fraldas%20-%20Raia_v1_35s_Carolina%20Malagutti.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559142336&amp;usg=AOvVaw3915o0ZiTa5TTsBch2TksB", talento: "Carolina Malagutti" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/3a515267-5276-411e-a024-59a0f8760981/%5B06%5D%20%5BP13%5D%5BNN%5D%20RAIA%20%20%20Black%20Fraldas%20-%20Raia_v1_50s_Carolina%20Malagutti.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559143364&amp;usg=AOvVaw2pQhsJ038dFb7u00GNBD3M", talento: "Carolina Malagutti" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/e02258e3-3709-4488-b7dd-c79f5d972046/%5B07%5D%20%5BP13%5D%5BNN%5D%20RAIA%20-%20Black%20Fraldas%20-%20Raia_v2_22s_Carolina%20Malagutti-.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559144270&amp;usg=AOvVaw3dmEvmn_p4n5VkNAfQBbi1", talento: "Carolina Malagutti" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/422a935c-0a6f-4b8c-b408-ab531bffa464/%5B08%5D%20%5BP13%5D%5BNN%5D%20RAIA%20%20%20Black%20Fraldas%20-%20Raia%20_v1_27s_Loretta%20Martins.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559145177&amp;usg=AOvVaw3nihXP3JVLlp1VMTqVw24e", talento: "Loretta Martins" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/d04f90f7-6f60-41c3-bddd-6684bfeae071/%5B02%5D%20%5BP14%5D%5BNN%5D%20RAIA%20-%20Black%20Fraldas%20-%20Drogasil_v2_23s_MarianaBraga.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559146226&amp;usg=AOvVaw2qStD8bI8qkjwC9QMDthhf", talento: "Mariana Braga" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/613c8abd-d382-4f85-ba1c-33bae37d6280/%5B03%5D%20%5BP14%5D%5BNN%5D%20RAIA%20%20%20Black%20Fraldas%20-%20Drogasil_v1_32s_Mariana.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559147175&amp;usg=AOvVaw2MBBzncRJnPQqqIBvtat-e", talento: "Mariana Braga" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/9da14ec3-51da-4e68-8960-85cfb5eee87d/%5B05%5D%20%5BP14%5D%5BNN%5D%20RAIA%20%20Black%20Fraldas%20-%20Drogasil_v2_36s_Mariana_Braga.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559148190&amp;usg=AOvVaw3yuQPuyKPwtfXdLeHI5T8m", talento: "Mariana Braga" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/cbcf499e-d72b-4610-8fd0-4531f52996f3/%5B04%5D%20%5BP14%5D%5BNN%5D%20RAIA%20%20%20Black%20Fraldas%20-%20Drogasil_v3_20s_Andrei%20Lamberg.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559149166&amp;usg=AOvVaw147_WdIZrxDyBuNcMkd-DK", talento: "Andrei Lamberg" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/f6f1a55c-eb3c-4093-9038-05ec093b32df/%5B08%5D%20%5BP14%5D%5BNN%5D%20RAIA%20%20%20Black%20Fraldas%20-%20Drogasil%20_v2_25s_Mariana%20Braga.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559150157&amp;usg=AOvVaw3At_RhXSi5KVfO9rbemnG-", talento: "Mariana Braga" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/0daf44c6-c008-4905-b67b-93f0570c5b30/%5B01%5D%20%5BP15%5D%5BNN%5D%20RAIA%20%20AlwaysOn%20PerfumariaJUL_v4_43s_Julia_Nogueira.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559151125&amp;usg=AOvVaw2_De7AUXTYyvs8Oe3b1VSv", talento: "Julia Nogueira" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/0daf44c6-c008-4905-b67b-93f0570c5b30/%5B01%5D%20%5BP15%5D%5BNN%5D%20RAIA%20%20AlwaysOn%20PerfumariaJUL_v4_43s_Julia_Nogueira.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559152136&amp;usg=AOvVaw1jtNujTEcN9YW_maiWxePI", talento: "Julia Nogueira" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/5f7d5c75-aa1a-4116-a713-c05662d67c11/%5B02%5D%20%5BP15%5D%5BNN%5D%20RAIA%20-%20AlwaysOn%20Perfumaria-JUL%20-%20Raia_v3_33s_Rodrigo_Rabello.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559153117&amp;usg=AOvVaw3wPXIApbx2qGoihuqXgT_U", talento: "Rodrigo Rabello" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/775000f7-42fc-4032-b245-f6016a04dc8f/%5B03%5D%20%5BP15%5D%5BNN%5D%20RAIA%20%20%20AlwaysOn%20Perfumaria%20JUL%20-%20Raia_v1_23s_Rodrigo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559154054&amp;usg=AOvVaw0etueMMGDBrXLUnV9_o3bL", talento: "Rodrigo Rabello" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/a5c1ce61-339c-4dde-98c3-c1f941a04108/%5B04%5D%20%5BP15%5D%5BNN%5D%20RAIA%20%20%20AlwaysOn%20Perfumaria%20JUL%20-%20Raia_v2_50s_Julia%20Nogueira.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559155019&amp;usg=AOvVaw1jMw26CbA9k1iKDGYLxNbB", talento: "Julia Nogueira" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/1ef6b021-6c9e-491a-8465-c6dc40b7e45b/%5B05%5D%20%5BP15%5D%5BNN%5D%20RAIA%20%20%20AlwaysOn%20Perfumaria%20JUL%20-%20Raia_v2_50s_Julia%20Nogueira.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559155965&amp;usg=AOvVaw1kXrPlOY6HVtS4-RIFoTEL", talento: "Julia Nogueira" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/0246f0d1-8cb7-4c26-9f91-167f02505293/%5B06%5D%20%5BP15%5D%5BNN%5D%20RAIA%20-%20AlwaysOn%20Perfumaria-JUL%20-%20Raia_v6_27s_JuliaNogueira.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559156927&amp;usg=AOvVaw2_OIo6xUelaAlVKrE9YvR7", talento: "Julia Nogueira" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/ad5858b4-e044-4c55-b4cc-de013a8ddd67/%5B07%5D%20%5BP15%5D%5BNN%5D%20RAIA%20%20AlwaysOn%20PerfumariaJUL%20-%20Raia_v3_40s_Rodrigo_Rabello.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559157903&amp;usg=AOvVaw2wgawA-LX7kupybHU19OOw", talento: "Rodrigo Rabello" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/2582a684-39e7-41b5-a13c-f1a32b4c9760/%5B08%5D%20%5BP15%5D%5BNN%5D%20RAIA%20-%20AlwaysOn%20Perfumaria-JUL%20-%20Raia_v3_28s_Rodrigo_Rabello.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559158913&amp;usg=AOvVaw0dy-NCge2uez_zzSq6Wv-G", talento: "Rodrigo Rabello" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/464859a6-029c-4080-9280-5d75435af932/%5B01%5D%20%5BP17%5D%5BNN%5D%20RAIA%20-%20Autosservic%CC%A7o%20AlwaysOn%20Infantil%20-%20Raia_v3_30s_GabrielPeregrino.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559159937&amp;usg=AOvVaw1BYlsvyBYczk3UqvXI6Cgx", talento: "Gabriel Peregrino" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/0b03ec86-064e-46b9-aac8-9d7621471728/%5B02%5D%20%5BP17%5D%5BNN%5D%20RAIA%20%20%20Autosservi%C3%A7o%20AlwaysOn%20Infantil%20-%20Raia_v2_28s_karol.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559161017&amp;usg=AOvVaw1BTeJO0rFTNztC6ATa0xLg", talento: "Karol Alves" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c312e6c7-b029-4b2e-b4b8-7a18e4841dcf/%5B03%5D%20%5BP17%5D%5BNN%5D%20RAIA%20%20%20Autosservi%C3%A7o%20AlwaysOn%20Infantil%20-%20Raia_v1_20s_gabriel.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559161994&amp;usg=AOvVaw2BmR7URx7FSBf3vBPWZqOV", talento: "Gabriel Peregrino" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/af6062b6-47de-4725-bf29-c5ef7b3d25bf/%5B04%5D%20%5BP17%5D%5BNN%5D%20RAIA%20Autosservi%C3%A7o%20AlwaysOn%20Infantil_v1_31s_Karol_Alves.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559163007&amp;usg=AOvVaw1jy8HESe0ZIHJBZAxHvnHC", talento: "Karol Alves" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/2548ae5e-8772-41fe-8d7c-736d81159619/%5B05%5D%20%5BP17%5D%5BNN%5D%20RAIA%20%20%20Autosservi%C3%A7o%20AlwaysOn%20Infantil%20-%20Raia_v1_41s_Karol%20Alves.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559164014&amp;usg=AOvVaw3Dco9LVNr86tY2qzNIBRgI", talento: "Karol Alves" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/00a9431b-edfc-42f1-a994-379cffa17ca5/%5B06%5D%20%5BP17%5D%5BNN%5D%20RAIA%20-%20Autosservi%C3%A7o%20AlwaysOn%20Infantil%20-%20Raia_v2_36s_Gabriel_Peregrino.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559165009&amp;usg=AOvVaw0c40WuCYzrkcwGlPSfThYI", talento: "Gabriel Peregrino" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b34ab298-199d-42c3-9ff1-c554ab65dd5b/%5B07%5D%20%5BP17%5D%5BNN%5D%20RAIA%20-%20Autosservi%C3%A7o%20AlwaysOn%20Infantil%20-%20Raia_v2_52s_Karol_Alves.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559165972&amp;usg=AOvVaw3vtoGdt8uezT75ECVroKNC", talento: "Karol Alves" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/d7bad9f4-26e0-48e7-b431-b1d12c5094f5/%5B08%5D%20%5BP17%5D%5BNN%5D%20RAIA%20%20%20Autosservi%C3%A7o%20AlwaysOn%20Infantil%20-%20Raia%20_v2_22s_Gabriel%20Peregrino.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559167041&amp;usg=AOvVaw0ZxsZx816xfqf5ipO8mhuX", talento: "Gabriel Peregrino" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/8ada61bc-b962-4f99-b801-4d07083ca5b4/%5B01%5D%20%5BP19%5D%5BNN%5D%20RAIA%20%20Cuidado%20que%20vale%20mais%20%20Raia_v2_29s_Ismael-Gotthardi.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559168047&amp;usg=AOvVaw2QPI5S1RgIx77y8e1lh7ZT", talento: "Ismael Gotthardi" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b66a4bff-77b3-4d63-99df-fb1211d7a410/%5B02%5D%20%5BP19%5D%5BNN%5D%20RAIA%20%20%20Cuidado%20que%20vale%20mais%20%20%20Raia_v3_21s_J%C3%BAlia%20Horta.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559169100&amp;usg=AOvVaw1KVGAsa5fYPNL0dUxkgdOv", talento: "Júlia Horta" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/53eef26f-2d89-45b5-9ded-619d910bb00f/%5B03%5D%20%5BP19%5D%5BNN%5D%20RAIA%20-%20Cuidado%20que%20vale%20mais%20-%20Raia_v5_47s_Ismael.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559170013&amp;usg=AOvVaw1RqNiG_JBoxVqo7TFp4CKl", talento: "Ismael Gotthardi" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/e632aaee-cf48-4d66-8e6b-04e61c1408a1/%5B04%5D%20%5BP19%5D%5BNN%5D%20RAIA%20%20%20Cuidado%20que%20vale%20mais%20%20%20Raia_v2_26s_Julia.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559171057&amp;usg=AOvVaw1jRggahEAvI9lzmG-KkZAq", talento: "Júlia Horta" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/56e2c313-6d47-43ef-bea3-207af24c870d/%5B05%5D%20%5BP19%5D%5BNN%5D%20RAIA%20%20%20Cuidado%20que%20vale%20mais%20%20%20Raia_v1_44s_Ismael%20Gotthardi.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559172034&amp;usg=AOvVaw2yMP7nAVxPrU7WhQvzUw61", talento: "Ismael Gotthardi" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/4a42e8d0-9792-4be2-a7b6-bee6151fbd66/%5B06%5D%20%5BP19%5D%5BNN%5D%20RAIA%20-%20Cuidado%20que%20vale%20mais%20-%20Raia_v2_41s_Ismael.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559173029&amp;usg=AOvVaw3N2ewHDHTVtqvtJMA76Lbv", talento: "Ismael Gotthardi" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/72276f37-3518-4b4a-94d8-ab9cd770fd34/%5B07%5D%20%5BP19%5D%5BNN%5D%20RAIA%20-%20Cuidado%20que%20vale%20mais%20-%20Raia%20v3_55s_JuliaHorta.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559174041&amp;usg=AOvVaw2evsOM5-WoT3S58O-1ZECS", talento: "Júlia Horta" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/3a5cd887-5e8e-4b49-9d83-91617e4f7d16/%5B08%5D%20%5BP19%5D%5BNN%5D%20RAIA%20-%20Cuidado%20que%20vale%20mais%20-%20Raia_v2_46s_Julia_Horta.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559175091&amp;usg=AOvVaw05yW7dnfDyD_QJF3x3aybi", talento: "Júlia Horta" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/e2b8ab85-a983-4802-9a9e-7889c30af691/%5B01%5D%20%5BP21%5D%5BNN%5D%20RAIA%20-%20OTC%20-%20Ciclo%20Gripal%20Raia_v3_52s_LaraGay.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559176046&amp;usg=AOvVaw0TQ30bujsA7G-L_Tu5x8UL", talento: "Lara Gay" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c813cd0f-bf4c-40dd-b3c8-7f535cb0adce/%5B02%5D%20%5BP21%5D%5BNN%5D%20RAIA%20%20%20OTC%20-%20Ciclo%20Gripal%20Raia_v5_32s_Lara%20Gay.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559176967&amp;usg=AOvVaw33C5FTfZiv64uH2rAcTI5t", talento: "Lara Gay" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/d26a363b-4f1b-4ce9-a656-e06daebe3f5f/%5B05%5D%20%5BP21%5D%5BNN%5D%20RAIA%20OTC%20Ciclo%20Gripal%20Raia_v2_43s_Lara_Gay.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559177857&amp;usg=AOvVaw3gDhe8Fkk0EVtDyMcdnsqO", talento: "Lara Gay" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/a4ed81a2-2ee4-46e5-97ec-02a854f90a2a/%5B07%5D%20%5BP21%5D%5BNN%5D%20RAIA%20-%20OTC%20-%20Ciclo%20Gripal%20Raia%20_v3_34s_Lara_gay.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559178742&amp;usg=AOvVaw1gnAOK9pN0VNRLoKGQyPLR", talento: "Lara Gay" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/bd3f4582-91b1-4a0e-9995-71f3849feab2/%5B04%5D%20%5BP23%5D%5BNN%5D%20RAIA%20-%20Marcas%20Coreanas%20-%20Raia_v4_39s_ClaraGiofoni.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559179698&amp;usg=AOvVaw3h8_yjltlR7cGuhHxGDEED", talento: "Clara Giffoni" }
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
      "Cliente": "Bradesco",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/1da50ebb-0b75-4769-a7d2-f2183863dd27/%5B01%5D%20%5BP03%5D%5BNN%5D%20BRADESCO%20%20%20Sala%20de%20Performance%20-%20Abertura%20de%20Contas%20PF_v3_50s_Pedro.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559446233&amp;usg=AOvVaw1m-wuY9tyBlqRYMdvndGrx", talento: "Pedro Zurawski" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/92492774-d77d-48af-bc42-680885138a2a/%5B02%5D%20%5BP03%5D%5BNN%5D%20BRADESCO%20Sala%20de%20Performance%20-%20Abertura%20de%20Contas%20PF_v3_26s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559447420&amp;usg=AOvVaw3XN3k6JOU2B5o4cKibPvA4", talento: "Pedro Zurawski" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/e1a21a2d-0419-4708-9e04-2e551829a06e/%5B03%5D%20%5BP03%5D%5BNN%5D%20BRADESCO%20%20%20Sala%20de%20Performance%20-%20Abertura%20de%20Contas%20PF_v2_19s_Pedro%20Zurawski.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559448617&amp;usg=AOvVaw2JUSw2iBizfDl_WEy4xhKc", talento: "Pedro Zurawski" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/0eb06898-8522-4189-8fa5-b9915d04627a/%5B04%5D%20%5BP03%5D%5BNN%5D%20BRADESCO%20-%20Sala%20de%20Performance%20-%20Abertura%20de%20Contas%20PF_v7_34s_Pedro%20Zurawski.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559449893&amp;usg=AOvVaw2DXBoV8UJEOcEn1ZQyZDJ7", talento: "Pedro Zurawski" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/108ef842-4eab-4344-bf0f-08eaf061ae9d/%5B01%5D%20%5BP04%5D%5BNN%5D%20BRADESCO%20%20%20NetNew%20-%20LIME_v3_38s_Jorge%20Hissa.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559451262&amp;usg=AOvVaw2-SJ5Etr5rZ-FeDVV269sz", talento: "Jorge Hissa" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/91fa7565-3a51-401c-ad36-d507fe36a3e0/%5B03%5D%20%5BP04%5D%5BNN%5D%20BRADESCO%20%20%20NetNew%20-%20LIME_v2_33s_Jorge.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559452656&amp;usg=AOvVaw1-04VkJB4GG6aR3nUlh7U8", talento: "Jorge Hissa" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/2ec98c10-ce8c-4de0-babd-9d3b232de711/%5B04%5D%20%5BP04%5D%5BNN%5D%20BRADESCO%20-%20NetNew%20-%20LIME_v4_17s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559454011&amp;usg=AOvVaw302jW_-8OxX1o0eoBdkUg5", talento: "Jorge Hissa" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b13072b5-7ab6-4d08-8dc5-f76dd2fdb8c9/%5B05%5D%20%5BP04%5D%5BNN%5D%20BRADESCO_v3_39s_Pedro_Ruivo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559455230&amp;usg=AOvVaw1ZAc6Mq4qWdNbntuTtjiJ8", talento: "Pedro Ruivo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/8c0bb94a-5dd2-4e88-878d-a98ab2665377/%5B06%5D%20%5BP04%5D%5BNN%5D%20BRADESCO%20%20%20NetNew%20-%20LIME_v3_29s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559456298&amp;usg=AOvVaw1TkXEfkAh5Km_WDGHd6xQZ", talento: "Jorge Hissa" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/281d003c-6723-4972-b6a2-5b90e5018faf/%5B07%5D%20%5BP04%5D%5BNN%5D%20BRADESCO%20%20%20NetNew%20-%20LIME_v3_11s_Pedro%20Ruivo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559457457&amp;usg=AOvVaw3Cvja_dKK_yoefC-uvN-yR", talento: "Pedro Ruivo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c46fb27f-ed7e-4ac4-86bb-423c4567bd97/%5B08%5D%20%5BP04%5D%5BNN%5D%20BRADESCO%20%20%20NetNew%20-%20LIME_v2_15s_Pedro%20Ruivo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559458644&amp;usg=AOvVaw1uNCraiXy6XYe1x-d03vux", talento: "Pedro Ruivo" }
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
      "Cliente": "Netshoes",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/8ee3186a-b6ad-42b2-9555-6e4cd6e9996e/%5B01%5D%20%5BP12%5D%5BNN%5D%20NETSHOES_TTCX%20APP_NS_120325_v2_59s_Adam_Pereira.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559234670&amp;usg=AOvVaw3ONGyFAz4dj7GqZ9Xa5Q-a", direcao: true, talento: "Adam Pereira" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/d37641c6-f4fe-4d99-a8dc-468e83a66acf/%5B01%5D%20%5BP13%5D%5BNN%5D%20NETSHOES%20-%20NS%20TTCX%20-%20VSA%20RTG%207D%20-%20JUN25_v2_35s_Livia%20Lima.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559235724&amp;usg=AOvVaw2uAFt5CJqkcUUD424J7ZeT", direcao: true, talento: "Lívia Lima" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/4618ac61-1a46-40a7-bae4-513696a6bddb/%5B01%5D%20%5BP14%5D%5BNN%5D%20NETSHOES%20-%20TTCX%20APP%20-%20NS%2010-06-25_v1_26s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559236668&amp;usg=AOvVaw3UzrbuDIT0QwI2nhwPF7Wy", talento: "Mariana Braga" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/a2209761-6999-4cb2-9e20-9eea4e1cf2b2/%5B02%5D%20%5BP14%5D%5BNN%5D%20NETSHOES%20%20%20TTCX%20APP%20%20%20NS%2010%2006%2025_v1_29s_.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559237688&amp;usg=AOvVaw2NcHQSO4-Og9i4iOjCyNUX", talento: "Mariana Braga" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/9af3bbf4-290e-43b7-a65a-39eeea1f4ab7/%5B03%5D%20%5BP14%5D%5BNN%5D%20NETSHOES%20%20%20TTCX%20APP%20%20%20NS%2010%2006%2025_v1_38s_.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559238787&amp;usg=AOvVaw0UuyjRhVNhgkJaqyCDxYFX", talento: "Mariana Braga" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/542423a1-f6f1-4979-b264-9afc9513c999/%5B04%5D%20%5BP14%5D%5BNN%5D%20NETSHOES%20%20%20TTCX%20APP%20%20%20NS%2010%2006%2025_v1_29s_Mariana%20Braga.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559239739&amp;usg=AOvVaw1jW75NPwO5aZO1s6wSkVlx", talento: "Mariana Braga" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/f55bac19-fc7f-466a-bf19-720f84ee4611/%5B02%5D%20%5BP15%5D%5BNN%5D%20NETSHOES%20%20%20NS%20-%20TTCX%20%20%20Briefing%20Mar_v3_19s_Ana%20Claudia.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559240810&amp;usg=AOvVaw2PdyccdOlWgbV79v88St40", direcao: true, talento: "Ana Claudia Padilha" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/d1c5b073-6f05-467b-a5e8-fb0bcbf7fdf2/%5B04%5D%20%5BP15%5D%5BNN%5D%20NETSHOES%20%20%20NS%20-%20TTCX%20%20%20Briefing%20Maratona%20PAYDAY%2008%202025_v1_48s_Ana%20Claudia.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559241889&amp;usg=AOvVaw0o_a9sh_4nfVtF0UE_KHd2", direcao: true, talento: "Ana Claudia Padilha" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/73aed43a-f4a8-4997-b95c-bec4b99341b7/%5B07%5D%20%5BP15%5D%5BNN%5D%20NETSHOES%20-%20NS%20-%20TTCX%20-%20Briefing%20Maratona-PAYDAY%2008-2025_v2_40s_AnaClaudia.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559242977&amp;usg=AOvVaw3R6pxuUKilX2gKfzcadviy", direcao: true, talento: "Ana Claudia Padilha" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/81ca9b5c-6a52-433c-b2b0-d572c90a87e8/%5B08%5D%20%5BP15%5D%5BNN%5D%20NETSHOES%20-%20NS%20-%20TTCX%20-%20Briefing%20Maratona-PAYDAY%2008-2025_v4_41s_Ana_Claudia.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559244090&amp;usg=AOvVaw37LhtzyH3KW5CgvtTadmyP", direcao: true, talento: "Ana Claudia Padilha" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/08dc0a92-0c93-4a4d-be30-ae9c64af61b9/%5B03%5D%20%5BP16%5D%5BNN%5D%20NETSHOES%20-%20Netshoes%20-%20campanha%20brand-consideration_v1_13s_Frederico.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559245094&amp;usg=AOvVaw2VA6WCTDS0iztfa_HXlbyH", talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/0b1a71c5-43c5-48ac-aa88-31f8826016a4/%5B04%5D%20%5BP16%5D%5BNN%5D%20NETSHOES%20%20%20Netshoes%20-%20campanha%20brand-consideration%20_v1_24s_Fred%20Soares.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559246066&amp;usg=AOvVaw0CGeBmOt0onLmgJA5-LeOf", talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c056c609-2a0b-44d7-bebc-d5c6e481000a/%5B05%5D%20%5BP16%5D%5BNN%5D%20NETSHOES%2000_v2_35s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559247126&amp;usg=AOvVaw2PikiROPMF4-XajDexgUQT", talento: "Frederico Volkmann" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/704f8d90-d83e-440f-909a-7526fc1d4393/%5B06%5D%20%5BP16%5D%5BNN%5D%20NETSHOES%20%20%20Netshoes%20-%20campanha%20brand-consideration_v3_18s_Frederico%20Volkmann.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559248164&amp;usg=AOvVaw3gip-VRR5ObRTmfmtfCSuj", talento: "Frederico Volkmann" }
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
      "Cliente": "LG",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/7f13990f-4f7d-4fed-840a-42e93ffb475d/%5B13%5D%20%5BP02%5D%5BNN%5D%20LG%20%20%20LG%20do%20Brasil%20(2025%2003%2024)_v2_42s_Karol%20Alves.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559249310&amp;usg=AOvVaw2mvHWBMMs15ofZF9kczzbb", direcao: true, talento: "Karol Alves" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/6484c532-af74-4c27-aa6a-f99a4106ae90/%5B14%5D%20%5BP02%5D%5BNN%5D%20LG%20-%20LG%20do%20Brasil%20(2025-03-24)_v2_41s_Clara_Griffoni.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559250408&amp;usg=AOvVaw0r4fpyaGoLMLhtCUHo6-Tk", talento: "Clara Giffoni" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/fd7a3ec0-ad2e-48eb-a652-3af5016155e2/%5B11%5D%20%5BP02%5D%5BNN%5D%20LG-LG-do-Brasi2025-03-24_v3_50s_Karolalves.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559251570&amp;usg=AOvVaw2FEz7fDGV9pB3j7nXwfKoU", direcao: true, talento: "Karol Alves" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/14a5d158-9b4b-4a83-a53a-14777e589d35/%5B16%5D%20%5BP02%5D%5BNN%5D%20LG%20%20%20LG%20do%20Brasil%20(2025%2003%2024)_v2_59s_Karol%20Alves.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559252624&amp;usg=AOvVaw2-C7h0_IXWs5GWzuIajYpq", direcao: true, talento: "Karol Alves" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/7ffb5427-b64e-4ee4-99cb-226b9d2ac0ba/%5B06%5D%20%5BP02%5D%5BNN%5D%20LG%20%20%20LG%20do%20Brasil%20(2025%2003%2024)%20_v2_35s_Karol.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559253743&amp;usg=AOvVaw2iGAEd0phVD3tcWL5kiwia", direcao: true, talento: "Karol Alves" }
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
      "Cliente": "Uber",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b4ed0e2d-225f-4c28-bc86-8cef599edf9a/%5B03%5D%20%5BP02%5D%5BCH%5D%20UBER%20%20%20Creators_Core%20Demand%202.0_18%20Mar%2025_v1_39s_Juliana%20Da%20Silva.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559254693&amp;usg=AOvVaw3UzH3HOh_U1nhktb3xLSXy", talento: "Juliana Da Silva" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b9546329-0d1d-49b7-b3c6-d5a743042543/%5B04%5D%20%5BP02%5D%5BCH%5D%20UBER%20%20%20Creators_Core%20Demand%202.0_18%20Mar%2025_v2_20s_Juliana%20da%20Silva.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559255664&amp;usg=AOvVaw1Tl0bnBefChqJ7t-f3si9-", talento: "Juliana Da Silva" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/ca627286-cf2b-47c9-8b64-8511158a7fcf/%5B01%5D%20%5BP05%5D%5BNN%5D%20UBER%20-%20Uber%20para%20Empresas%20(2025-09-26)_v4_23s_Qu%C3%A9ren%20Hapuque.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559256814&amp;usg=AOvVaw0s9w05sNTHxUfBG4FOA0rS", talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/00777d27-9bb9-4b5f-82dd-461f3568a240/%5B02%5D%20%5BP05%5D%5BNN%5D%20UBER%20Uber%20para%20Empresas_v3_38s_Qu%C3%A9ren.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559257820&amp;usg=AOvVaw1nybh8H25KqQ6r-9TdgheW", talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/61fb5eea-cc8d-4b05-95e8-da8f76026368/%5B03%5D%20%5BP05%5D%5BNN%5D%20UBER%20-%20Uber%20para%20Empresas%20(2025-09-26)_v4_46s_Qu%C3%A9ren.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559258903&amp;usg=AOvVaw2y6tUM9uZFVtnwxKLU8LQn", talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/bcf3d17e-e521-4df8-a332-1d17e8d448c7/%5B04%5D%20%5BP05%5D%5BNN%5D%20UBER%20%20%20Uber%20para%20Empresas%20(2025%2009%2026)_v5_48s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559259991&amp;usg=AOvVaw2GOCsolWJ-rMZDPQebpHAO", talento: "Quéren Hapuque" }
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
      "Cliente": "Carolina Herrera",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/7faa4e5e-4b2b-43e6-bdf7-ecbf1bf7aaee/%5B02%5D%20%5BP01%5D%5BCH%5D%20CAROLINA%20HERRERA%20%20-%20Carolina%20herrera%20(2025-06-27)_v3_36s_Kiara.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559430907&amp;usg=AOvVaw2xuIoao_VaCHNi35djKvYF", talento: "Khiara" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/aed0a065-bb6b-4b59-9735-bfe4132c4eb8/%5B03%5D%20%5BP01%5D%5BCH%5D%20Carolina%20herrera%20(2025%2006%2027)_V2_21s_Drico%20Alves.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559432231&amp;usg=AOvVaw2le6h3fBvSwUiWZKJWaFHW", talento: "Drico Alves" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/178c93d3-dbab-49cf-97a5-8db92f0e6149/%5B04%5D%20%5BP01%5D%5BCH%5D%20CAROLINA%20HERRERA%20%20-%20Carolina%20herrera%20(2025-06-27)_v3_40s_DiogoMalta.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559433562&amp;usg=AOvVaw1jg2PPqoYGxybb8GTsX-Pl", talento: "Diogo Malta" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/f5c0bc2f-1a30-4a88-8032-c2e115ac1eb5/%5B05%5D%20%5BP01%5D%5BCH%5D%20CAROLINA%20HERRERA%20%20-%20Carolina%20herrera%20(2025-06-27)_v2_20s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559434815&amp;usg=AOvVaw0M0FbzhcLEOBu1M3snP7Fn", talento: "Diogo Malta" }
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
      "Cliente": "Nestlé",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais / Exibido no Cinema",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/60ecfe8b-6a3f-4120-b06e-162df66dcbbf/%5B06%5D%20%5BP06%5D%5BCH%5D%20NESTLE%CC%81%20%20%20Break%20digno%20de%20cinema!%20%E2%80%93%20KitKat%20Cereal%20%2B%20TikTok%20%2B%20Cinemark_01_v4_35s_LucasLeal.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559362710&amp;usg=AOvVaw3Zed0zL_SYCxZ5YjQW5sjG", talento: "Lucas Leal Souza" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/5272986f-5e0f-4e20-9a5d-1fccee645768/%5B06%5D%20%5BP06%5D%5BCH%5D%20NESTLE%CC%81%20-%20Break%20digno%20de%20cinema!%20%E2%80%93%20KitKat%20Cereal%20%2B%20TikTok%20%2B%20Cinemark_02_v4_30s_LucasLeal.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559363981&amp;usg=AOvVaw1bxO2pjkvW-75L7pl_c-90", talento: "Lucas Leal Souza" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/d67276bd-5db2-4caa-b3af-71fb0c100474/%5B09%5D%20%5BP06%5D%5BCH%5D%20NESTLE%CC%81%20%20%20Break%20digno%20de%20cinema!%20%E2%80%93%20KitKat%20Cereal_v5_22s_Lucas%20Leal.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559365334&amp;usg=AOvVaw000ewjnQFaB256MdRMbMyT", talento: "Lucas Leal Souza" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/50bd0f58-ffc9-4281-ae35-a9e49365af5d/%5B05%5D%20%5BP06%5D%5BCH%5D%20NESTLE%CC%81%20-%20Break%20digno%20de%20cinema!%20KitKat%20Cereal%20%2B%20TikTok%20%2B%20Cinemark_v7_15s_Alessandro%20Cerqueira.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559366665&amp;usg=AOvVaw26IgmBRlKNFndljLfTfq8D", talento: "Alessandro Cerqueira" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/6ac23daa-5c38-47e9-b919-8082bfd4f6f3/%5B12%5D%20%5BP06%5D%5BCH%5D%20NESTL%C3%89%20%20%20Break%20digno%20de%20cinema!%20%E2%80%93%20KitKat%20Cereal%20%2B%20TikTok%20%2B%20Cinemark_v1_59s_Alessandro.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559367923&amp;usg=AOvVaw2CKgK6DVXL0xw7aRJTujT_", talento: "Alessandro Cerqueira" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/cd932122-4918-4165-ba0a-1b74d40f3ed6/%5B10%5D%20%5BP01%5D%5BCH%5D%20NUTREN%20%20%20Guia%20Pr%C3%A1tico%20do%20Poder%20das%20Vitaminas_v3_17s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559369085&amp;usg=AOvVaw2ad-oCiD-AFQyjnskvSxm1", talento: "Tati Infante" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/8df60563-79ce-4d59-ad67-2a8829372106/%5B09%5D%20%5BP01%5D%5BCH%5D%20NUTREN%20-%20Guia%20Pr%C3%A1tico%20do%20Poder%20das%20Vitaminas_v6_34s_TatiInfante.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559370268&amp;usg=AOvVaw3v3mIzrfHJRVd90mvhk4Kl", talento: "Tati Infante" }
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
      "Cliente": "Philips",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/0b8cc255-ddc6-4e71-bff8-99a7ce63c212/%5BP07%5D%5B03%5D%20TikTok%20ON%20-%20Philips%20-%20Beauty_v1_34s_Luiza%20Veloso.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559180721&amp;usg=AOvVaw3Iys-Ilh7uSu6tP5l9J3zy", direcao: true, talento: "Luiza Veloso" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/e668d967-0b42-4cb6-8fb6-f0ced7b4d16f/%5BP07%5D%5B04%5D%20TikTok%20ON%20-%20Philips%20-%20Beauty_v3_26s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559181684&amp;usg=AOvVaw1qc4gpgVgb5Ice-RnJIk89", direcao: true, talento: "Luiza Veloso" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/70b76d3e-f19b-4c1f-b646-13061f97c310/%5BP07%5D%5B05%5D%20TikTok%20ON%20-%20Philips%20-%20Male%20Grooming_v1_28s_Rodrigo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559182556&amp;usg=AOvVaw31P2mpCZGH-krctkIN3eSH", talento: "Rodrigo Rabello" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c159c422-904f-4e30-ab58-884eb478597f/%5BP07%5D%5B06%5D%20TikTok%20ON%20-%20Philips%20-%20Male%20Grooming_v3_19s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559183452&amp;usg=AOvVaw1squ_snxDKkxEByf9hYxjf", talento: "Rodrigo Rabello" }
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
      "Cliente": "Intimus",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Creative Incubator",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/e3994362-1293-4a50-b00d-6c55b18df9bb/%5B09%5D%20%5BP06%5D%5BCH%5D%20Intimus%20-%20Creative%20Incubator%20(Fevereiro)_v3_25s_MARIA_KROPOTOFF.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559184435&amp;usg=AOvVaw0c6rCsv2RdfEJezccVRChm", direcao: true, talento: "Maria Luíza Kropotoff" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/86db63ca-383f-4d1b-9047-2cc81dd5b7b7/%5B10%5D%20%5BP06%5D%5BCH%5DIntimus-CreativeIncubator-%5BFevereiro%5D_v3_58s_MariaLuizaKropotoff.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559185540&amp;usg=AOvVaw0Lh1ssrfoqzt8xJUqdHVbN", direcao: true, talento: "Maria Luíza Kropotoff" }
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
      "Cliente": "Domino's",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/7b2c95ad-3d0e-4a09-936e-ab48be5c09ad/%5B01%5D%20%5BP04%5D%5BNN%5D%20DOMINOS%20%20%20TTCX%20Agosto%2025_v1_35s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559437072&amp;usg=AOvVaw1S8AAdGnt7J3Y1PVpGSFUT", talento: "Jorge Hissa" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/ae34a567-33aa-418f-bffc-0790836dc92f/%5B02%5D%20%5BP04%5D%5BNN%5D%20DOMINOS%20%20%20TTCX%20Agosto%2025_v1_37s_Jorge%20Hissa.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559438192&amp;usg=AOvVaw2A3jl6Gh0SjyfiuTZ5nMP3", talento: "Jorge Hissa" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/1b859f65-4a73-47c4-8470-43c9d18fbea6/%5B03%5D%20%5BP04%5D%5BNN%5D%20DOMINOS%20%20%20TTCX%20Agosto%2025_v4_59s_Jorge%20Hissa.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559439307&amp;usg=AOvVaw16-W_IIuKctbP54j-N78lo", talento: "Jorge Hissa" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b9493fa5-9358-4034-addf-a4661c11ddfa/%5B04%5D%20%5BP04%5D%5BNN%5D%20DOMINOS%20-%20TTCX%20Agosto-25_v4_42s_Jorge_Hissa.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559440430&amp;usg=AOvVaw3SuJvPih5p5GmdimvcpWbW", talento: "Jorge Hissa" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/5f258762-057f-4667-9b12-5ac7f41635ab/%5B01%5D%20%5BP05%5D%5BNN%5D%20DOMINOS%20%20%20TTCX%20Agosto%2025_v3_33s_Jorge%20Hissa.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559441481&amp;usg=AOvVaw1Vl8RFn8NeSN47ESHt7pUq", talento: "Jorge Hissa" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/56cf2d04-2ec1-4e3c-b566-390f5ac955b2/%5B02%5D%20%5BP05%5D%5BNN%5D%20DOMINOS%20-%20TTCX%20Agosto-25_v6_40s_JorgeHissa.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559442571&amp;usg=AOvVaw2PCaPv9Qx-4TpFz4pAyX0g", talento: "Jorge Hissa" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/f13c6340-e3b5-4b86-9b8d-e949c0990e21/%5B03%5D%20%5BP05%5D%5BNN%5D%20DOMINOS%20%20%20TTCX%20Agosto%2025_V5_24S_JORGE.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559443772&amp;usg=AOvVaw0mU4LkMOFfA85oL7fhpx1G", talento: "Jorge Hissa" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/191be07b-fdf6-4935-a679-1b67c1764ea6/%5B04%5D%20%5BP05%5D%5BNN%5D%20DOMINOS%20-%20TTCX%20Agosto-25_v5_27s_Jorge_Hissa.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559444946&amp;usg=AOvVaw33L-Udmed4_FSNc65yeK9m", talento: "Jorge Hissa" }
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
      "Cliente": "Serasa",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/664a0489-05a6-466f-956a-af433f153d08/%5B01%5D%20%5BP08%5D%5BNN%5D%20SERASA%20Sau%CC%81de%20do%20Seu%20Nego%CC%81cio_v3_31s_Raphael_Monteiro.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559403566&amp;usg=AOvVaw0gzJ2zJdndZDipiUevWJeF", talento: "Raphael Monteiro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/58a09f33-3cc0-48e7-a740-efa46783a85e/%5B02%5D%20%5BP08%5D%5BNN%5D%20SERASA%20-%20Sa%C3%BAde%20do%20Seu%20Neg%C3%B3cio_v5_40s_RaphaelMonteiro.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559404670&amp;usg=AOvVaw1Cn_ber6oiulPeG-RSSvbg", talento: "Raphael Monteiro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/a62a40f9-1526-4ad8-9015-840a51429bad/%5B03%5D%20%5BP08%5D%5BNN%5D%20SERASA%20-%20Sa%C3%BAde%20do%20Seu%20Neg%C3%B3cio_v4_29s_Raphael.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559406090&amp;usg=AOvVaw2CzcLS61tvFnSbYhfEsnpo", talento: "Raphael Monteiro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/5e7a9c3c-965e-4740-b8f7-0b18da278e63/%5B04%5D%20%5BP08%5D%5BNN%5D%20SERASA%20%20%20Sa%C3%BAde%20do%20Seu%20Neg%C3%B3cio_v2_44s_Raphael%20Monteiro.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559407358&amp;usg=AOvVaw1iYqiILCR3ltQmPr8sgnLr", talento: "Raphael Monteiro" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b8ebffff-a168-493b-b3ff-c13a72d58f62/%5B01%5D%20%5BP09%5D%5BNN%5D%20SERASA%20-%20Campanha%20stalker%20-%20Net%20New%20Recomenda_v6_57s_DeboraMelo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559408511&amp;usg=AOvVaw06O2Vc5n-yQ8hurbDY2ODc", talento: "Débora Melo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/e52514d6-8808-4863-9082-69c3d11f78bd/%5B02%5D%20%5BP09%5D%5BNN%5D%20SERASA%20%20%20Campanha%20stalker%20-%20Net%20New%20Recomenda%20_v5_45s_Debora%20Melo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559409635&amp;usg=AOvVaw0rQkE7OrHEwzzBzFy2l2p9", talento: "Débora Melo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/a14426e6-ad12-4c8c-989c-8dca24c8e172/%5B03%5D%20%5BP09%5D%5BNN%5D%20SERASA%20%20%20Campanha%20stalker%20-%20Net%20New%20Recomenda_v3_34s_Debora.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559410709&amp;usg=AOvVaw2SKg1iFGBYj6yUxA0x3Y9d", talento: "Débora Melo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/a0c13a61-1141-496e-95fa-2f064ef7e3ae/%5B04%5D%20%5BP09%5D%5BNN%5D%20SERASA%20-%20Campanha%20stalker%20-%20Net%20New%20Recomenda_v5_32s_Debora_Melo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559411830&amp;usg=AOvVaw0-qYhW_SATCxD2DDwGzRiC", talento: "Débora Melo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/73c52990-87f5-496e-bc62-4d53f48d82d9/%5B01%5D%20%5BP11%5D%5BNN%5D%20SERASA%20%20%20Campanha%20%23SemSustos%20PME%20-%20Consulta%20CPF%20CNPJ_v5_21s_Qu%C3%A9ren%20Hapuque.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559412937&amp;usg=AOvVaw2rPpIm1_5MpsT0wxzhw4lp", talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/efec1d3b-907c-42d5-ae23-133867111726/%5B02%5D%20%5BP11%5D%5BNN%5D%20SERASA%20Campanha%20%23SemSustos_v8_27s_Queren.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559414033&amp;usg=AOvVaw3aR2Bv8z5_r1dIGdZWBtS7", talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/26283daf-6720-4519-9e32-9f6bf117dad4/%5B03%5D%20%5BP11%5D%5BNN%5D%20SERASA%20%20%20Campanha%20%23SemSustos%20PME%20-%20Consulta%20CPF%20CNPJ_v5_25s_Qu%C3%A9ren%20Hapuque.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559415188&amp;usg=AOvVaw0M4QnuKb5kr_RsTu98r5FA", talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b6cc677f-a509-43e2-804f-ccd0c633574e/%5B04%5D%20%5BP11%5D%5BNN%5D%20SERASA%20Campanha%20%23SemSustos_v10_22s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559416279&amp;usg=AOvVaw32RMlN6khE4yk4ug163-ID", talento: "Quéren Hapuque" }
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
      "Cliente": "Movida",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/447681c5-e977-4a26-872b-a42baae2b95a/%5B01%5D%20%5BP10%5D%5BNN%5D%20MOVIDA%20-%20TTCX%20Seminovos%20Movida_v2_32s_Marcelo%20Klein.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559417351&amp;usg=AOvVaw1QvRkWO_Vr3I_zSfUCHGIP", talento: "Marcelo Klein" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/3d051cd3-3a88-4a81-ba0d-0b876529787b/%5B02%5D%20%5BP10%5D%5BNN%5D%20MOVIDA%20%20%20TTCX%20Seminovos%20Movida%20_v1_43s_Marcelo%20Klein.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559418415&amp;usg=AOvVaw3dhqbipQCCIu6rkkedOYwc", talento: "Marcelo Klein" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/d52f7347-8a70-4ed8-bb00-06360268510e/%5B03%5D%20%5BP10%5D%5BNN%5D%20MOVIDA%20-%20TTCX%20Seminovos%20Movida_v1_30s_Marcelo%20Klein.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559419481&amp;usg=AOvVaw3_d2H1HDfp68DP2MPdnyB2", talento: "Marcelo Klein" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/6bd99acd-0c2d-4e93-9606-42fe92e20a56/%5B04%5D%20%5BP10%5D%5BNN%5D%20MOVIDA%20%20%20TTCX%20Seminovos%20Movida_v2_50s_Clara%20Giffoni.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559420643&amp;usg=AOvVaw3B5DSde63SjLyjoJ40sPhB", talento: "Clara Giffoni" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/118e301a-0e41-4dbd-9790-5bccadfd6556/%5B05%5D%20%5BP10%5D%5BNN%5D%20MOVIDA%20%20%20TTCX%20Seminovos%20Movida_v2_41s_Clara.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559421697&amp;usg=AOvVaw1vCj0E1ChdNAIeSML2nRA-", talento: "Clara Giffoni" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/4335549b-d59c-4fcc-b258-2f8d3a8c6843/%5B06%5D%20%5BP10%5D%5BNN%5D%20MOVIDA%20%20%20TTCX%20Seminovos%20Movida_v2_41s_Marcelo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559422756&amp;usg=AOvVaw3OsK4dIXAKh-Y3eYrDGttN", talento: "Marcelo Klein" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/a784512e-557f-44c5-aa4f-159d364129cd/%5B07%5D%20%5BP10%5D%5BNN%5D%20MOVIDA%20-%20TTCX%20Seminovos%20Movida_v2_32s_Clara%20Giffoni.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559423844&amp;usg=AOvVaw18Uz3FNNfuBX7_-F8ro1JS", talento: "Clara Giffoni" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/5dce58c7-5c64-4d33-a2f8-b1ce09c8a763/%5B08%5D%20%5BP10%5D%5BNN%5D%20MOVIDA%20TTCX%20Seminovos%20Movida_v2_31s_Clara_Giffoni.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559424941&amp;usg=AOvVaw0ehXpY5-UU4ySUgTz7XzWP", talento: "Clara Giffoni" }
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
      "Cliente": "KaBuM!",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/a7e3ac6b-df5c-49be-9158-650fd6c6fdbc/%5B01%5D%20%5BP20%5D%5BNN%5D%20KABUM%20-%20TTCX%20-%20KaBuM!%20-%20Brand%20Consideration%20(08-2025)_v2_35s_Lara_Gay.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559426086&amp;usg=AOvVaw0pINXJZyqlpf5lNeAfZe-f", talento: "Lara Gay" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c20bec49-e01b-4a4e-875e-7a81a33d430d/%5B03%5D%20%5BP20%5D%5BNN%5D%20KABUM%20%20%20TTCX%20%20%20KaBuM!%20%20%20Brand%20Consideratio_v1_24s_Lara%20Gay.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559427199&amp;usg=AOvVaw1R_iW88h1lcyOzGxSj-OaO", talento: "Lara Gay" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/2c3108ab-ada2-4888-88d2-6bbd7de20d11/%5B06%5D%20%5BP20%5D%5BNN%5D%20KABUM%20-%20TTCX%20-%20KaBuM!%20-%20Brand%20Consideration%20(08-2025)_v2_27s_Lara%20Gay.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559428368&amp;usg=AOvVaw0ijviDhHxNVVRUKoUSIosT", talento: "Lara Gay" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/20587ced-b949-49ce-9615-b28cb3e790e6/%5B07%5D%20%5BP20%5D%5BNN%5D%20KABUM%20-%20TTCX%20-%20KaBuM!%20-%20Brand%20Consideration%20(08-2025)_v3_35s_Lara_gay.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559429601&amp;usg=AOvVaw3dqGVTiLxKuyvO4qGpfS8X", talento: "Lara Gay" }
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
      "Cliente": "Neo Energia",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/08082c39-05e3-40f8-9284-8d15cddf330d/%5B01%5D%20%5BP01%5D%5BNN%5D%20NEOENERGIA%20-%20NEOENERGIA%20COELBA_CLIENTES_v4_23s_ISMAEL.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559392098&amp;usg=AOvVaw3T62fTG5yawuTetDGjfiyl", talento: "Ismael Gotthardi" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/2294bb5f-d232-4b81-a762-ba55ad2a7b59/%5B02%5D%20%5BP01%5D%5BNN%5D%20NEOENERGIA%20-%20NEOENERGIA%20COELBA_CLIENTES_v4_39s_Ismael.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559393282&amp;usg=AOvVaw0ZhPC7KPtPVSn9aFiHKoEq", talento: "Ismael Gotthardi" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/e1c56375-8a89-4937-9cbc-bdacc48b3186/%5B03%5D%20%5BP01%5D%5BNN%5D%20NEOENERGIA%20-%20NEOENERGIA%20COELBA_CLIENTES_v4_27s_Ismael.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559394399&amp;usg=AOvVaw3oWZqq_IzK8HWgFXrx35om", talento: "Ismael Gotthardi" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c4eb88e9-25d5-4d6b-a8a5-cb3307fa2abf/%5B04%5D%20%5BP01%5D%5BNN%5D%20NEOENERGIA%20COELBA_CLIENTES_v2_35s_Ismael.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559395521&amp;usg=AOvVaw2uecKVCDoSt7Hr6q3VKYbT", talento: "Ismael Gotthardi" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/f55ba733-0559-4b49-ac0d-24b1849f600b/%5B01%5D%20%5BP02%5D%5BNN%5D%20NEOENERGIA%20%20%20NEOENERGIA%20BRASILIA_CLIENTES_v2_37s_Julia.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559396642&amp;usg=AOvVaw0LDtDubYtz128-BDai706G", talento: "Júlia Horta" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/4b0b43c8-4acf-414e-b770-f16862fecec0/%5B02%5D%20%5BP02%5D%5BNN%5D%20NEOENERGIA%20%20%20NEOENERGIA%20BRASILIA_CLIENTES_v1_32s_Julia%20Horta.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559397766&amp;usg=AOvVaw0ryBrpeyo4oPaAH65eNv-O", talento: "Júlia Horta" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/f5f07b46-1412-411d-8859-b865e472ff26/%5B03%5D%20%5BP02%5D%5BNN%5D%20NEOENERGIA%20NEOENERGIA%20BRASILIA_CLIENTES_v4_32s_JULIA_HORTA.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559398895&amp;usg=AOvVaw0AYGoH1o6CnBzp_Leo12oa", talento: "Júlia Horta" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/0865c709-4d88-4e6b-a052-18517850c498/%5B04%5D%20%5BP02%5D%5BNN%5D%20NEOENERGIA%20%20%20NEOENERGIA%20BRASILIA_CLIENTES_v5_22s_J%C3%BAlia%20Horta.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559400131&amp;usg=AOvVaw2ZTCPF8L9iXD9sJJi6neEf", talento: "Júlia Horta" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/fd35bc72-47ea-4e76-936b-b4866c162fb2/%5B03%5D%20%5BP04%5D%5BNN%5D%20NEOENERGIA%20%20%20NEOENERGIA%20PERNAMBUCO_CLIENTES_v3_33s_Hannah%20Beatriz.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559401277&amp;usg=AOvVaw3edWt487ICkpYKpqPZgb-I", talento: "Hannah Beatriz" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/484bd793-3939-43af-9203-ac9aead5b2fb/%5B04%5D%20%5BP04%5D%5BNN%5D%20NEOENERGIA%20-%20NEOENERGIA%20PERNAMBUCO_CLIENTES_v3_48s_Hannah.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559402463&amp;usg=AOvVaw3pu-q5PWjMoc7Vj8iZTP0f", talento: "Hannah Beatriz" }
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
      "Cliente": "Claro",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/cc9a3d7b-c8ac-404c-a87f-afdb44d391fe/%5B03%5D%20%5BP02%5D%5BCH%5D%20CLARO%20%20%20Claro%20Prezao_v6_35s_nalu.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559385073&amp;usg=AOvVaw0fchhkY9rvU26QuR9fDBnR", talento: "Nalu Moura" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/2b4005c8-8867-4c36-ac40-23b5c37e0daa/%5B01%5D%20%5BP04%5D%5BNN%5D%20CLARO%20%20%20Claro%20controle%20em%20Net%20New_v4_46s_Vinicius%20Scribel.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559386186&amp;usg=AOvVaw3TSJ-nxpetZiE1V3IYZ0Av", talento: "Vinicius Scribel" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/20a358cc-2b72-402b-ae52-db6b2d17d643/%5B02%5D%20%5BP04%5D%5BNN%5D%20CLARO%20-%20Claro%20controle%20em%20Net%20New_v11_50s_Vinicius%20Scribel.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559387461&amp;usg=AOvVaw3s4oQueeLzevjrRL1zWpWy", talento: "Vinicius Scribel" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/1554afc0-e193-41ec-a1c7-ce0d9e6ab17d/%5B03%5D%20%5BP04%5D%5BNN%5D%20CLARO%20%20%20Claro%20controle%20em%20Net%20New_v6_52s_Vinicius%20Scribel.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559388734&amp;usg=AOvVaw3jTDCNXY5aTWJ8Om0PeKjH", talento: "Vinicius Scribel" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/d07c6fab-4d5c-4943-ade0-474a484f4a88/%5B04%5D%20%5BP04%5D%5BNN%5D%20CLARO%20%20%20Claro%20controle%20em%20Net%20New_v6_45s_Vinicius%20Scribel.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559389950&amp;usg=AOvVaw3cT4Nj0isfeZSLTAWWCY-3", talento: "Vinicius Scribel" }
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
      "Cliente": "Vans",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/16555f2c-c8f9-4b2e-8454-c211dd398acd/%5B01%5D%20%5BP01%5D%5BNN%5D%20VANS%20-%20Vans%20Brasil%20(2025-06-09)_v3_31s_Jasmim_Avelino.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559391026&amp;usg=AOvVaw0E5OsKhKzPGNnRZpRcZfFb", talento: "Jasmim Avelino" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/571df829-ebfc-4aec-b9e3-af639458a676/%5B02%5D%20%5BP01%5D%5BNN%5D%20VANS%20%20%20Vans%20Brasil%20(2025%2006%2009)_v2_20s_Jasmin.mp4?authz_token=eyJhbGciOiJIUzI1NiIsImtpZCI6ImFybjphd3M6a21zOnVzLWVhc3QtMjo1MTQzMDg2NDE1OTI6YWxpYXMvYXR0YWNobWVudHMvYXV0aC8xIiwidHlwIjoiSldUIn0.eyJhdWQiOjg3OTEwMDc1LCJleHAiOjE3NzMzNDYzODQsInN1YiI6Imh0dHBzOi8vdDkwMDcwMDg2MDUucC5jbGlja3VwLWF0dGFjaG1lbnRzLmNvbS90OTAwNzAwODYwNS81NzFkZjgyOS1lYmZjLTRhZWMtYjllMy1hZjYzOTQ1OGE2NzYvJTVCMDIlNUQlMjAlNUJQMDElNUQlNUJOTiU1RCUyMFZBTlMlMjAlMjAlMjBWYW5zJTIwQnJhc2lsJTIwKDIwMjUlMjAwNiUyMDA5KV92Ml8yMHNfSmFzbWluLm1wNCIsIm1heFVzYWdlIjoxLCJyYW5kIjoiVDB4TyJ9.0RHhJrLP6MDbZrTrhiTyeWTdaWBpSUWIMCCo036PoaE&view=open", talento: "Jasmim Avelino" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/67855fe4-4d72-4b58-85ff-10c835e60b93/%5B03%5D%20%5BP01%5D%5BNN%5D%20VANS%20%20%20Vans%20Brasil%20(2025%2006%2009)_v2_52s_Jasmim%20Avelino.mp4?view=open", talento: "Jasmim Avelino" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/75e258b0-d8cf-4038-987b-f50bb440b56d/%5B04%5D%20%5BP01%5D%5BNN%5D%20VANS%20-%20Vans%20Brasil%20(2025-06-09)_v2_20s_JasmimAvelino.mp4?view=open", talento: "Jasmim Avelino" }
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
      "Cliente": "Bet Nacional",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/aa01d5fb-244a-44bf-92c9-998352146995/%5B01%5D%20%5BP02%5D%5BCH%5D%20BETNACIONAL%20-%20Betnacional%20TTCX%20-%20June%202025_v6_26s_WesleyJesus.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559382912&amp;usg=AOvVaw0y_FaMfJ5PZD1j8D-OPNCu", talento: "Wesley Jesus" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/ef6def79-567b-47d7-acd3-9efc55e1abfd/%5B02%5D%20%5BP02%5D%5BCH%5D%20BETNACIONAL%20%20Betnacional%20TTCX%20-%20June%202025_v2_41s_Wesley_Jesus.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559384058&amp;usg=AOvVaw3GXllgYyUmveFBPop5dt2u", talento: "Wesley Jesus" }
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
      "Cliente": "Bravecto",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/11170c6e-c430-4f01-95b5-cf5885246fe0/%5B02%5D%20%5BP01%5D%5BNN%5D%20BRAVECTO%20-%202025%20Bravecto%20Brasil%20%5Bregional%5D_v2_40s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559371371&amp;usg=AOvVaw3now2AYpvRk10aeEwhtNMU", talento: "Cachorro - Yago" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/6a95c00b-1ef9-424d-9b53-39bf272ed325/%5B01%5D%20%5BP01%5D%5BNN%5D%20BRAVECTO%20%20%202025%20Bravecto%20Brasil%20%5Bregional%5D_v3_27s_%C3%8Dgor%20Arvelos.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559372414&amp;usg=AOvVaw1goDLlLVXRoUXe-xu87uDi", talento: "Ígor Arvelos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/ac6ca81b-92c9-478c-bea4-960f22d06584/%5B01%5D%20%5BP04%5D%5BNN%5D%20BRAVECTO%202025%20Bravecto%20Brasil%20II_v1_34s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559373462&amp;usg=AOvVaw1gy7Ai1fxA5DVKvf4kD7wO", talento: "Whisky - Yago" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/98b919cc-3c0a-470a-aba1-3952654021e5/%5B02%5D%20%5BP04%5D%5BNN%5D%20BRAVECTO%20%20%202025%20Bravecto%20Brasil%20II_v1_25s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559374484&amp;usg=AOvVaw2-FSYmzdOpqkKnCVlILirD", talento: "Loretta Martins" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/88f833dd-776d-4b2b-8903-c909cb7ae394/%5B04%5D%20%5BP04%5D%5BNN%5D%20BRAVECTO%20%20%202025%20Bravecto%20Brasil%20II_v3_21s_loretta.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559375504&amp;usg=AOvVaw15jRxG2esXybJRIb1hgD-E", talento: "Loretta Martins" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/554efbdf-5744-4895-82b2-115e33aecc6f/%5B05%5D%20%5BP04%5D%5BNN%5D%20BRAVECTO%20%20%202025%20Bravecto%20Brasil%20II_v2_42s_Jorge.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559376576&amp;usg=AOvVaw1Yry59KC9r-sz7ZTbAPJcg", talento: "Jorge Hissa" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c0fb4f38-55fe-4929-bf53-cc3efc60170f/%5B06%5D%20%5BP04%5D%5BNN%5D%20BRAVECTO%20-%202025%20Bravecto%20Brasil%20II_v3_32s_Yago.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559377606&amp;usg=AOvVaw3iDkw94E__BrVYH9Qhvmzi", talento: "Cachorro - Yago" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/a74e590f-5b9a-4969-8aab-87c8dc7ab5f5/%5B07%5D%20%5BP04%5D%5BNN%5D%20BRAVECTO%20%20%202025%20Bravecto%20Brasil%20II_v3_27s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559378651&amp;usg=AOvVaw3Mg1BNXygH5KdhXmsLDALu", talento: "Cachorro - Yago" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/cd3681d3-3635-464f-ae34-8ba89321d692/%5B08%5D%20%5BP04%5D%5BNN%5D%20BRAVECTO%20-%202025%20Bravecto%20Brasil%20II_v3_24s_Loretta_Martins.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559379697&amp;usg=AOvVaw3UHAvjLlo37oUla5o56Ojf", talento: "Loretta Martins" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/327926bd-61be-4e81-9d7f-565260cc81cf/%5B09%5D%20%5BP04%5D%5BNN%5D%20BRAVECTO%20-%202025%20Bravecto%20Brasil%20II_v4_26s_LorettaMartins.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559380766&amp;usg=AOvVaw2aZUEobPKnRYkxYCCYA_vz", talento: "Loretta Martins" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/0b1379bc-4c09-40ef-b02a-87c1c4e9be97/%5B10%5D%20%5BP04%5D%5BNN%5D%20BRAVECTO%20%20%202025%20Bravecto%20Brasil%20II_v3_31s_Jorge%20Hissa.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559381858&amp;usg=AOvVaw1L4tTGYPOZQ0xvusJ-TYoO", talento: "Jorge Hissa" }
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
      "Cliente": "Carrefour",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2026"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/ba1147dc-71ec-432e-8241-269a00d68711/%5B02%5D%20%5BP03%5D%5BNN%5D%20CARREFOUR%20-%20Grupo%20Carrefour%20Brasil%20-%20JAN%202026_v5_23s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559488947&amp;usg=AOvVaw0XnhHDgVh_NPtB9J8dZcPp", direcao: true, talento: "Ismael Gotthardi" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/361303e4-fb37-4346-a185-1e5b73a080d5/%5B04%5D%20%5BP03%5D%5BNN%5D%20CARREFOUR%20%20%20Grupo%20Carrefour%20Brasil%20-%20JAN%202026_v4_29s_Ismael%20Gotthardi.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559490297&amp;usg=AOvVaw3fedUcOjpR3cnxw0VaRVPJ", direcao: true, talento: "Ismael Gotthardi" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/44ae2aa7-a483-40cc-8243-c1563c79abd6/%5B02%5D%20%5BP04%5D%5BNN%5D%20CARREFOUR%20-%20Grupo%20Carrefour%20Brasil_v2_26s_Quezia_Fernandes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559491541&amp;usg=AOvVaw3okcvWCbCtjYpZOndsEx32", direcao: true, talento: "Quézia Castro" }
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
      "Cliente": "Allfluence",
      "Projeto": "Oscar 2026",
      "Tipo": "Conteúdo com IA",
      "Ano": "2026"
    },
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
    descricao: "O que acontece dentro da minha cabeça. Projeto pessoal explorando Higgsfield, Nano Banana e Flux AI com referência ao Filipe Ret.",
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
    id: 41,
    nome: "Allfluence",
    categoria: "video",
    categoriaLabel: "Filmmaker + Direção",
    ano: "2025",
    videoId: "",
    descricao: "Produção de conteúdo interno e social media para a Allfluence, incluindo vídeos institucionais e de tendências com a equipe.",
    ficha: {
      "Função": "Filmmaker + Direção",
      "Cliente": "Allfluence",
      "Plataforma": "TikTok / Instagram",
      "Tipo": "Social Media + Institucional",
      "Período": "Fev 2025 - 2026"
    },
    instagram: "https://www.instagram.com/allfluence/",
    website: "https://www.allfluence.com.br/",
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/fc9d155a-efc6-49ba-98a5-5aedb5bda954/%5BSM%5D%5BR02%5D%5B10%5D%20Coisas%20que%20me%20d%C3%A3o%20arrepio_v2-1_15s_Yago%20Capita.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559060511&amp;usg=AOvVaw2LVCJMzO0L6GXm57wK6Rd8", talento: "Yago Capita" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/3e5c224a-8167-4026-966e-669841a7cdcc/%5BSM%5D%5BR02%5D%5B10%5D%20Coisas%20que%20me%20d%C3%A3o%20arrepio_v2-2_15s_Yago%20Capita.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559061508&amp;usg=AOvVaw1gi8Gk9EPKJIb2lmKOeKDe", talento: "Yago Capita" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/cf67f0d3-169a-4323-89ab-768fb361dc13/%5BSM%5D%5BR02%5D%5B10%5D%20Coisas%20que%20me%20d%C3%A3o%20arrepio_v2-3_13s_Yago%20Capita.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559062501&amp;usg=AOvVaw1OZ-K1aKzTqXTalSeqcGjS", talento: "Yago Capita" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/7f023b6c-c1f4-4b6f-94bd-94b29c3dcee8/%5BSM%5D%5BR02%5D%5B09%5D%20Mantra%20de%20Marketing_v3_25s_Pedro_Valerio_Yago_Capita.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559063398&amp;usg=AOvVaw3PYFPDu4ZWpVnWKNsyfat9", talento: "Yago Capita Pedro Valério" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/6eb9932c-ed8e-4bdd-b182-74d2290c4f41/%5BSM%5D%5BR02%5D%5B07%5D%20Erro%20Windows%20-%20Solicita%C3%A7%C3%A3o%20de%20acesso_v1_07s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559064376&amp;usg=AOvVaw38lUcvspWpTfIMYjBJztPs", talento: "Yago Capita" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/d4d14eaa-f457-48f5-8b66-cdb45febc318/%5BSM%5D%5BR02%5D%5B12%5D%20Equipe%20Unida%2C%20chefe%20Orgulhoso_v3_20s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559065430&amp;usg=AOvVaw3u3PatNXjeSpFs_GeQLzo7", direcao: true, talento: "Camille Ana Claudia Padilha Savylla" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/3bdc96f0-17f6-4363-86ff-31a85e5b263e/%5BSM%5D%5BR02%5D%5B14%5D_v2_24s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559066525&amp;usg=AOvVaw2dfyXW8Vb8XrYk1cUmlPSe", talento: "Yago Capita Camille Ana Claudia Padilha Savylla" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/d8b3b6a3-dd26-41b7-934d-a94d0881c99f/%5BSM%5D%5BR02%5D%5B17%5D%20Como%20eu%20fa%C3%A7o%20para%20ter%20uma%20equipe%20focada%20numa%20apresenta%C3%A7%C3%A3o_v1_07s_1.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559067727&amp;usg=AOvVaw3wuTpjTQQC1OwUemVmeTJ7", direcao: true, talento: "Camille Ana Claudia Padilha Savylla" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/85b07bae-3832-4cfa-a2fc-76ab428bd0f3/%5BSM%5D%5BR03%5D%5B02%5D_v1_36s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559068838&amp;usg=AOvVaw1bgb-DYUxdZwjW9OQ2NU8v", direcao: true, talento: "Camille Ana Claudia Padilha Savylla" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/fb5dcee7-fd25-4789-962d-c732145a582e/%5BSM%5D%5BE13%5D%20Confra%20-%20Trend%20-Jet2Holidays-%20remix_v1_10s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559070002&amp;usg=AOvVaw0Y8aOaQZWjgE9gqlIVOCgB", direcao: true, talento: "Equipe Allfluence" },
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
      "Cliente": "Veloe",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b9f0ef4f-31de-48cb-a6e7-e2982d0199e0/%5B03%5D%20%5BP01%5D%20VELOE%20-%20Veloe%20Go-PJ-VPO_v2_53s_Raphael%20Monteiro.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559186494&amp;usg=AOvVaw0ZXAffOKxhYR_azvBYEuXy", talento: "Raphael Monteiro" }
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
      "Cliente": "Agibank",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/41765364-6390-463f-849d-6f714ae6a092/%5B06%5D%5BP01%5D%5BNN%5D%20AGIBANK%20Agibank%20(2025%2003%2006)_v3_48s_ISADORA_CECATTO.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559296874&amp;usg=AOvVaw2sdrB1mNyNteqDXgtPwIeh", talento: "Isadora Cecatto" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/d6b57b83-cf77-4b13-80af-53043678a203/%5B07%5D%5BP01%5D%5BNN%5D%20AGIBANK%20%20Agibank%20(20250306)_v6_32s_Isadora_Cecatto.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559297895&amp;usg=AOvVaw3QEhiJXa6dXkIFGFUxjHHr", talento: "Isadora Cecatto" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/6dbb787b-174e-409c-a9e1-a0399f1f5a95/%5B08%5D%5BP01%5D%5BNN%5D%20AGIBANK%20-%20Agibank%20(2025-03-06)_v2_34s_Isadora_Cecatto.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559299118&amp;usg=AOvVaw1NwB0CXyJRSyZnQo6oYvkE", direcao: true, talento: "Isadora Cecatto" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/0542518f-008b-407c-929c-eddd9c1e23d7/%5B04%5D%5BP01%5D%5BNN%5D%20AGIBANK%20Agibank%20(20250306)_v3_25s_Debora%20Melo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559300302&amp;usg=AOvVaw24e1Me4iiBSmemkh5IOLAf", direcao: true, talento: "Isadora Cecatto" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/ae6d698a-5aa6-42c0-9ee2-828bc8fc2880/%5B03%5D%5BP01%5D%5BNN%5D%20AGIBANK%20-%20Agibank%20(2025-03-06)_v3_24s_Debora_Melo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559301429&amp;usg=AOvVaw1zZuVmpj5NLgosNz9jHyCF", direcao: true, talento: "Débora Melo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/96698954-22f2-49bd-a0cc-b0ade753f033/%5B05%5D%5BP01%5D%5BNN%5D%20AGIBANK%20%20%20Agibank%20(2025%2003%2006)_v1_28s_Isadora%20Cecatto.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559302573&amp;usg=AOvVaw2PgZBeX6I6xVRpNC9ZO-tG", direcao: true, talento: "Débora Melo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/ae41bd56-8f92-4561-a97e-e06379725ec3/%5B02%5D%5BP01%5D%5BNN%5D%20AGIBANK%20-%20Agibank%20(2025-03-06)_v4_36s_DeboraMello.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559303621&amp;usg=AOvVaw3ZhetxxNDs4dRfdlJUKRNd", direcao: true, talento: "Débora Melo" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/bc592bf4-6021-49d6-930a-49c137ee1756/%5B01%5D%5BP01%5D%5BNN%5D%20AGIBANK%20%20Agibank%20(2025%2003%2006)_v1_45s_Debora%20Melo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559304779&amp;usg=AOvVaw37Kp9VCj2sxLUOd16LewdP", direcao: true, talento: "Débora Melo" }
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
      "Cliente": "Livelo",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/e5089455-5021-42fc-967f-9004b67b84e4/%5B04%5D%20%5BP11%5D%5BNN%5D%20LIVELO%20%20%20Club%20Livelo%20(2025%2004%2030)_v3_27s_Qu%C3%A9ren.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559305812&amp;usg=AOvVaw3BSTY6SCK7lDMt-EVWcnt4", talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/1d9dcc75-414c-40f4-91e8-5c519c01d13e/%5B01%5D%20%5BP12%5D%5BNN%5D%20LIVELO%20%20%20Pontos%20Viram%20Dinheiro%20(2025%2005%2019)_v2_28s_Queren.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559306826&amp;usg=AOvVaw1aTxkIaBkOE9QaruALY_O6", talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/1218d8ef-1221-41fb-b869-b760723e2e3a/%5B02%5D%20%5BP12%5D%5BNN%5D%20LIVELO%20%20%20Pontos%20Viram%20Dinheiro%20(2025%2005%2019)_v4_37s_Queren.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559307855&amp;usg=AOvVaw1kefJROTL-qOG2DW33CEW_", talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/e242d9a3-d64e-4ac4-945a-69ad115f4164/%5B03%5D%20%5BP12%5D%5BNN%5D%20LIVELO%20-%20Pontos%20Viram%20Dinheiro%20(2025-05-19)_v3_40s-Qu%C3%A9remFernandes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559308884&amp;usg=AOvVaw2AbIkUOqqWVP0XewQbxJBk", talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/389efea9-128c-4cfb-9445-a8285bbd134d/%5B04%5D%20%5BP12%5D%5BNN%5D%20LIVELO%20-%20Pontos%20Viram%20Dinheiro%20(2025-05-19)_v2_39s_Queren%20Hapuque.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559309874&amp;usg=AOvVaw1WHLTZzwcnifuVVct7I5Yr", talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b3e24740-e878-4779-a5ad-0d2be0f16a97/%5B01%5D%20%5BP13%5D%5BNN%5D%20LIVELO%20%20%20Livelo%20(2025%2005%2019)_v3_35s_Queren.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559310950&amp;usg=AOvVaw1H0JSqxr2DgTZHcaxVDy27", talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/130f8068-7180-4037-9f83-c310e01a20fc/%5B02%5D%20%5BP13%5D%5BNN%5D%20LIVELO%20-%20Livelo%20(2025-05-19)_v4_23s_Queren.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559311953&amp;usg=AOvVaw3qbNr6J8OUXgiRxmUg-tLd", talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/1f05ad42-7b3f-46d9-846f-069716982a43/%5B03%5D%20%5BP13%5D%5BNN%5D%20LIVELO%20%20%20Livelo%20(2025%2005%2019)_v3_20s_Qu%C3%A9ren.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559313045&amp;usg=AOvVaw2UajnboPPaNopMyLwVe3cO", talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c6e59360-22e0-4f92-9031-9237ecd0a92a/%5B04%5D%20%5BP13%5D%5BNN%5D%20LIVELO%20-%20Livelo%20(2025-05-19)_v2_30s-Qu%C3%A9ren.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559314058&amp;usg=AOvVaw1tHFgFsTzT0dsb71Kmwvgj", talento: "Quéren Hapuque" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/226cc88f-cd13-4b30-8613-a60e2ee8ae06/%5B04%5D%20%5BP14%5D%5BCH%5D%20LIVELO%20%20%20Livelo%20Educacional%20-%20Brand%20Mission_v5_52s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559315092&amp;usg=AOvVaw2cic3bGFID94eyDsJFdSek", talento: "Letícia Pedro" }
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
      "Cliente": "Baby Sec",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b12fb52c-3677-4894-8c96-ca23b1f7d11d/%5B01%5D%20%5BP01%5D%5BNN%5D%20BABYSEC%20-%20Babysec%20Shortinho%20Talentos%20Maio_v3_52s_Gabriel_Peregrino.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559316227&amp;usg=AOvVaw36vfhhAyJ_YS3VTlQ66a8Q", talento: "Gabriel Peregrino" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/aa953e6b-52a5-4199-b070-d78784c2d406/%5B05%5D%20%5BP01%5D%5BNN%5D%20BABYSEC%20%20%20Babysec%20Shortinho%20Talentos%20Maio_v3_51s_Gabriel%20Peregrino.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559317264&amp;usg=AOvVaw3aoc3j9RK7_CvB4wBBSjiB", direcao: true, talento: "Gabriel Peregrino" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/bbb923e6-71dd-44a3-a162-709090088da5/%5B06%5D%20%5BP01%5D%5BNN%5D%20BABYSEC%20%20%20Babysec%20Shortinho%20Talentos%20Maio_v3_20s_Gabriel.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559318301&amp;usg=AOvVaw2y3XcKxOoYB2AGjxq0Jr72", direcao: true, talento: "Gabriel Peregrino" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/35d13306-f13b-4034-a0a0-e9b877415079/%5B08%5D%20%5BP01%5D%5BNN%5D%20BABYSEC%20-%20Babysec%20Shortinho%20Talentos%20Maio_v4_16s_Pedro_peregrino.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559319387&amp;usg=AOvVaw1Z1QiJoDjuAa1hB_v1eaVZ", direcao: true, talento: "Gabriel Peregrino" }
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
      "Cliente": "GA.MA",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/f38db0af-b842-476c-a8fa-34db4b0e9a39/%5B01%5D%20%5BP02%5D%5BNN%5D%20GA.MA%20%20%20%5BJunho%5D%20%C3%93leos%20Essenciais_v2_44s_Larissa.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559320424&amp;usg=AOvVaw1IfjhfNIekFulTIzuvJWWm", direcao: true, talento: "Larissa Venturini" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/efa1ac84-5f82-41a0-8dfc-36ff7270bf99/%5B02%5D%20%5BP02%5D%5BNN%5D%20GA.MA%20%5BJunho%5D%20%C3%93leos%20Essenciais_v2_52s_LARISSA_VENTURINI.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559321549&amp;usg=AOvVaw0pq-BZuqPtLYkMXK5wxDeI", direcao: true, talento: "Larissa Venturini" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/2c8c125c-fce4-49f6-904c-afa3d2216f26/%5B03%5D%20%5BP02%5D%5BNN%5D%20GA.MA%20%20%20%5BJunho%5D%20%C3%93leos%20Essenciais_v6_46s_Larissa%20Venturini.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559322632&amp;usg=AOvVaw2oUOx6Wyxj3pU51KovBli8", direcao: true, talento: "Larissa Venturini" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/85037e7f-2607-4147-9fcc-b5d464209a62/%5B04%5D%20%5BP02%5D%5BNN%5D%20GA.MA%20%20%20%5BJunho%5D%20%C3%93leos%20Essenciais_v4_38s_Larissa%20Venturini.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559323752&amp;usg=AOvVaw0M13rwUI6KeaVmVFkgjY5E", direcao: true, talento: "Larissa Venturini" }
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
      "Cliente": "Bullsbet",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/30080104-5807-4147-953a-9c3d4b0ddc4d/%5B02%5D%20%5BP01%5D%5BNN%5D%20BULLSBET%20-%20Bullsbet%20(2025-05-19)_v1_24s_Antonio_Bastos.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559324872&amp;usg=AOvVaw0fCCAhTq96uCn42Pnm9wU5", direcao: true, talento: "Antônio Bastos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/33e7bb26-d019-47a5-800e-45069953403d/%5B03%5D%20%5BP01%5D%5BNN%5D%20BULLSBET%20%20%20Bullsbet%20(2025%2005%2019)_v2_15s_Antonio%20Bastos.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559325977&amp;usg=AOvVaw1wdfTdH3d1JJKvti74u0So", direcao: true, talento: "Antônio Bastos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/af2c7e3d-b59a-443c-afe2-6e0bab2c0435/%5B04%5D%20%5BP01%5D%5BNN%5D%20BULLSBET%20-%20Bullsbet%20(2025-05-19)_v5_20s-AntonioBasto.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559327144&amp;usg=AOvVaw2-81Vx1eaoQZGayJXrsOsr", direcao: true, talento: "Antônio Bastos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b12d4b57-73ae-4fc5-a9b4-f2b775d841eb/%5B01%5D%20%5BP01%5D%5BNN%5D%20BULLSBET%20%20%20Bullsbet%20(2025%2005%2019)_v2_45s_Antonio%20Bastos.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559328314&amp;usg=AOvVaw3EPRMLKv399EMYIunxdeNm", direcao: true, talento: "Antônio Bastos" }
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
      "Cliente": "Faculdade Estácio",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/a5c14998-6369-4821-acf7-7f95089ae0d9/%5B08%5D%20%5BP04%5D%5BNN%5D%20ESTACIO%20-%20Est%C3%A1cio%20-%20Fundo%20-%20Maio-25_v6_30sLarissaTravassos.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559329427&amp;usg=AOvVaw37ArBu8eaz5GplcohvAWN6", direcao: true, talento: "Larissa Travassos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/63ff8e9e-63b4-4669-b211-7e6e4f7c3c94/%5B01%5D%20%5BP04%5D%5BNN%5D%20ESTACIO%20%20%20Est%C3%A1cio%20-%20Fundo%20-%20Maio%2025_v4_24s_Larissa%20Travassos.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559330651&amp;usg=AOvVaw31WU_U5XwH-EFjJeqQAHvf", direcao: true, talento: "Larissa Travassos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/454ce9af-89e2-4223-aaa0-ea5dff2b5091/%5B02%5D%20%5BP04%5D%5BNN%5D%20ESTACIO%20%20Est%C3%A1cio%20-%20Fundo%20-%20Maio25_v5_34s_Joao_Mendes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559331752&amp;usg=AOvVaw0dfJse1KlO9MOKnmdKSNwz", direcao: true, talento: "João Mendes" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/75bc1540-d3cb-456d-b528-d5a13809cece/%5B03%5D%20%5BP04%5D%5BNN%5D%20ESTACIO%20%20%20Est%C3%A1cio%20-%20Fundo%20-%20Maio%2025_v6_23s_Larissa_1.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559332900&amp;usg=AOvVaw20yAUNqbIn9ZZGX2E_i7pp", direcao: true, talento: "Larissa Travassos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/91ff7db1-6601-46a1-b221-bce8e9d1aea5/%5B04%5D%20%5BP04%5D%5BNN%5D%20ESTACIO%20-%20Est%C3%A1cio%20-%20Fundo%20-%20Maio-25_v9_20s-Jo%C3%A3oMendes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559334142&amp;usg=AOvVaw1zIYQS6AeX2ayw-xUYwfn1", direcao: true, talento: "João Mendes" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/897d5d93-8cfa-4baf-99bb-361891894922/%5B05%5D%20%5BP04%5D%5BNN%5D%20ESTACIO%20%20Est%C3%A1cio%20-%20Fundo%20-%20Maio25_v7_34s_Joao_Mendes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559335277&amp;usg=AOvVaw3qsxCUNJY6yYl1MwYPaMgc", direcao: true, talento: "João Mendes" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/03c4c5ea-bf47-48f9-b0d4-f46d844fabf1/%5B06%5D%20%5BP01%5D%5BNN%5D%20ESTACIO%20%20%20Est%C3%A1cio%20-%20Fundo%20-%20Maio%2025_v5_31s_Larissa%20Travassos.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559336381&amp;usg=AOvVaw2N3E_nrnyRg8uI2CfIBqEL", talento: "Larissa Travassos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/3ef6377e-7e99-49b9-93a0-c55c32a0f1d2/%5B07%5D%20%5BP04%5D%5BNN%5D%20ESTACIO%20%20%20Est%C3%A1cio%20-%20Fundo%20-%20Maio%2025_v4_33s_Jo%C3%A3o%20Mendes.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559337628&amp;usg=AOvVaw3d1CKdP3jbgI7VO_3sPvgZ", direcao: true, talento: "João Mendes" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/395a2e6d-11dc-4bdf-9a74-09ff9686853a/%5B01%5D%20%5BP05%5D%5BNN%5D%20ESTACIO%20-%20P%C3%B3s%20Est%C3%A1cio%20-%20Junho%202025_v6_36s_MarianaBraga.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559338906&amp;usg=AOvVaw3bSBk5Jah_rFN3Ka6H6g-b", talento: "Mariana Braga" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/f20d3934-936e-47a0-a692-c756590ef71a/%5B02%5D%20%5BP05%5D%5BNN%5D%20ESTACIO%20-%20P%C3%B3s%20Est%C3%A1cio%20-%20Junho%202025_v7_38s_MarianaBraga.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559339969&amp;usg=AOvVaw2m5rPGxW9TVEagMcAx9SCe", talento: "Mariana Braga" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/4afd33a5-ca5e-40c4-9ce6-a0310ee67be3/%5B03%5D%20%5BP05%5D%5BNN%5D%20ESTACIO%20%20%20P%C3%B3s%20Est%C3%A1cio%20-%20Junho%202025_v4_31s_Mariana%20Braga.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559340988&amp;usg=AOvVaw2lGwrzyFh0Jx56rcPqxbxq", talento: "Mariana Braga" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/5024686e-13e9-4089-9aeb-ea946e1c9095/%5B04%5D%20%5BP05%5D%5BNN%5D%20ESTACIO%20-%20P%C3%B3s%20Est%C3%A1cio%20-%20Junho%202025_v3_34sRodrigoRabello.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559342014&amp;usg=AOvVaw1umSMd0NR9wab7cq8yqM8p", talento: "Rodrigo Rabello" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/febdb296-d595-4b8f-a9e6-cca20025d356/%5B05%5D%20%5BP05%5D%5BNN%5D%20ESTACIO%20%20%20P%C3%B3s%20Est%C3%A1cio%20-%20Junho%202025_v6_37s_Rodrigo%20Rabello.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559343059&amp;usg=AOvVaw2QYcnMbelblPsr2iq9avmG", talento: "Rodrigo Rabello" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/15a70316-e00b-403f-a26a-1948e1ec6807/%5B06%5D%20%5BP05%5D%5BNN%5D%20ESTACIO%20%20%20P%C3%B3s%20Est%C3%A1cio%20-%20Junho%202025_v5_26s_Rodrigo%20Rabello.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559344529&amp;usg=AOvVaw1NasVPtlAO_mIBVespj1BP", talento: "Rodrigo Rabello" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/a4e0c25b-1ceb-47ad-b5ce-7ee0e7c75468/%5B07%5D%20%5BP05%5D%5BNN%5D%20ESTACIO%20%20P%C3%B3s%20Est%C3%A1cio%20-%20Junho%202025_v6_39s_Rodrigo_Rabello_Ribeiro.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559346080&amp;usg=AOvVaw2lC8YGEoCPreaGkKLKVhmh", talento: "Rodrigo Rabello" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/fdc3f24a-faee-434c-a446-d9c5f96f75d9/%5B08%5D%20%5BP05%5D%5BNN%5D%20ESTACIO%20P%C3%B3s%20Est%C3%A1cio%20-%20Junho%202025_v6_42s_Mariana_Braga.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559347342&amp;usg=AOvVaw0lat_bH2y0kMn4ENVZe6yv", talento: "Mariana Braga" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b3c0877f-dda8-4879-90a0-f944b4265104/%5B01%5D%20%5BP06%5D%5BNN%5D%20ESTACIO%20-%20Est%C3%A1cio%20-%20Performance%20-%20Outubro-2025_v5_21sLarissaTravassos.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559348514&amp;usg=AOvVaw1JbozECf5zUDbf_10FsJ5X", talento: "Larissa Travassos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/b04116bb-30de-4d13-ab3d-e7fd2f739290/%5B02%5D%20%5BP06%5D%5BNN%5D%20ESTACIO_v4_29s_Larissa_Travassos.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559349840&amp;usg=AOvVaw3QI5lxkDMEnPhTi7x9JFvm", talento: "Larissa Travassos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/9ca36de2-cad9-4614-9adc-8939a6518163/%5B03%5D%20%5BP06%5D%5BNN%5D%20ESTACIO%20-%20Est%C3%A1cio%20-%20Performance%20-%20Outubro-2025_v6_34s_FernandaPenha.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559350886&amp;usg=AOvVaw0jMAGCL8-1SAmbM9MuzwUW", talento: "Fernanda Penna" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/4cb76fbb-17ce-417d-ada6-5b2e3f52e062/%5B04%5D%20%5BP06%5D%5BNN%5D%20ESTACIO%20-%20Est%C3%A1cio%20-%20Performance%20-%20Outubro-2025_v4_27s_Fernanda_Penna.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559351987&amp;usg=AOvVaw0DSZT8TdKpfIFLx6s2HRSB", talento: "Fernanda Penna" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/bc7a5e38-eb1e-46df-a49b-a21172bc2399/%5B05%5D%20%5BP06%5D%5BNN%5D%20ESTACIO%20-%20Est%C3%A1cio%20-%20Performance%20-%20Outubro-2025_v5_44s_Larissa_travassos.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559353161&amp;usg=AOvVaw0sSyWLfa8ZECZAoDHagqLh", talento: "Larissa Travassos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/d51ce586-98f6-4353-87a8-1e0e05c0f90d/%5B06%5D%20%5BP06%5D%5BNN%5D%20ESTACIO_v6_41s_Larissa_Travassos.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559354445&amp;usg=AOvVaw3duD9BT8D8BClCbrNaR8kF", talento: "Larissa Travassos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/8d963fbe-3615-498b-92f2-ba535ff944b0/%5B07%5D%20%5BP06%5D%5BNN%5D%20ESTACIO_v4_36s_Fernanda_Penna.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559355463&amp;usg=AOvVaw1-P8LAZkMHXfvcz5_E9T3F", talento: "Fernanda Penna" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/aece9183-b7d9-4e08-924d-76615113aa66/%5B08%5D%20%5BP06%5D%5BNN%5D%20ESTACIO%20%20%20Est%C3%A1cio%20-%20Performance%20-%20Outubro%202025_v3_44s_Fernanda.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559356568&amp;usg=AOvVaw3yi2vc3CTO-0g9QTRam_wT", talento: "Fernanda Penna" }
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
      "Cliente": "Reals Bet",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/8e0173ef-1d12-4e89-a6b9-1c64ba75ef35/%5B01%5D%20%5BP01%5D%5BNN%5D%20REALS%20BET%20%20%20Reals%20Bet%20(2025%2005%2030)_v4_44s_Pablo.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559357758&amp;usg=AOvVaw1B74BlPCR6HXpHdV685LgX", direcao: true, talento: "Pablo Sant'Anna" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/8df1d07a-1bf6-4392-8e7a-09cd525a57dc/%5B02%5D%20%5BP01%5D%5BNN%5D%20REALS%20BET%20%20%20Reals%20Bet%20(2025%2005%2030)_v4_49s_Pablo%20Sant&#39;Anna.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559359004&amp;usg=AOvVaw2hMVvD4OaKJcR7w7Mdw25D", direcao: true, talento: "Pablo Sant'Anna" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/4b360130-4bed-4432-9e88-dd9ef8d1908c/%5B03%5D%20%5BP01%5D%5BNN%5D%20REALS%20BET%20-%20Reals%20Bet%20(2025-05-30)_v2_55s-PabloSantAna.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559360181&amp;usg=AOvVaw0JUcJL0xG3VyTy31pcwWBs", direcao: true, talento: "Pablo Sant'Anna" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/5fc72b68-69fa-4296-9245-3fd87295f8e2/%5B04%5D%20%5BP01%5D%5BNN%5D%20REALS%20BET%20-%20Reals%20Bet%20(2025-05-30)_v3_47s_Pablo_Sant&#39;Anna.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559361490&amp;usg=AOvVaw3ddfREXBiqsGBXkLsR0JHw", direcao: true, talento: "Pablo Sant'Anna" }
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
      "Cliente": "Sorriso",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/89fd8531-74f9-4e4c-ba66-97f2bd6ec158/%5B01%5D%20%5BP01%5D%5BNN%5D%20SORRISO%20%20%20NET%20NEW%20-%20CHALLENGE_v5_37s_Khiara.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559459830&amp;usg=AOvVaw04agp9dgCtiJ9OMcyiyZVc", talento: "Khiara" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/6c58ba61-ced2-4e5e-b3f4-b7327b533155/%5B02%5D%20%5BP01%5D%5BNN%5D%20SORRISO%20-%20NET%20NEW%20-%20CHALLENGE_v8_47s_Kiara.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559461066&amp;usg=AOvVaw3F22C12zIOsYVDhD3KfIlH", talento: "Khiara" }
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
      "Cliente": "Tramontina",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/7f7abf33-534a-4359-aba0-a0dab20e85ea/%5B03%5D%20%5BP03%5D%5BCH%5D%20TRAMONTINA%20%20%20Tramontina%202025%20%20%20TTCX%20Nova%20Marca_v8_41s_Tati%20Infante.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559462360&amp;usg=AOvVaw37mMwEOfMS4z7orcbPsX2J", talento: "Tati Infante" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/d9159069-9109-4c1d-a8c8-6196c023c9fc/%5B04%5D%20%5BP03%5D%5BCH%5D%20TRAMONTINA%20%20%20Tramontina%202025%20%20%20TTCX%20Nova%20Marca_v3_26s_Tati.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559463623&amp;usg=AOvVaw2__YHuhAmvhq4mabNhGnKh", talento: "Tati Infante" }
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
      "Cliente": "Softys Kitchen",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/3b8b05dc-8362-4769-9e7b-85bd3b95cf03/%5B01%5D%20%5BP01%5D%5BNN%5D%20SOFTYS%20KITCHEN_v6_29s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559464787&amp;usg=AOvVaw0Tfdx56jdY8MXo81l7D1HE", talento: "Ígor Arvelos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/1b372551-693c-4499-9c68-d811e493acd7/%5B02%5D%20%5BP01%5D%5BNN%5D%20SOFTYS%20KITCHEN%20Softys%20Kitchen%20(20250924)_v2_20s_Igor%20Arvelos.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559465961&amp;usg=AOvVaw0z1_OT5Qf-SqNhx2Y843Fy", talento: "Ígor Arvelos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/e3647ece-8a9b-4c0c-b9a2-3794cab18da8/%5B03%5D%20%5BP01%5D%5BNN%5D%20SOFTYS%20KITCHEN%20-%20Softys%20Kitchen%20(2025-09-24)_v1_39s_Leticia_Machado.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559467118&amp;usg=AOvVaw23hZtpn9VX8B5aeEmLsaSo", talento: "Letícia Machado" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/5ea16bc8-80fe-46f3-ab26-0afba545b09d/%5B04%5D%20%5BP01%5D%5BNN%5D%20SOFTYS%20KITCHEN_v2_37s_Igor.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559468163&amp;usg=AOvVaw1y6bmyZ40LHqtzj5F6ukJm", talento: "Ígor Arvelos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/37bd30e7-6614-477c-bd5b-367a594a8f21/%5B05%5D%20%5BP01%5D%5BNN%5D%20SOFTYS%20KITCHEN%20-%20Softys%20Kitchen%20(2025-09-24)_v2_20s_LeticiaMachado.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559469376&amp;usg=AOvVaw2iwOyMezc-fUqQ6DRlpZeS", talento: "Letícia Machado" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/bdfcc082-20a3-4591-96c0-5ed905ff3806/%5B06%5D%20%5BP01%5D%5BNN%5D%20SOFTYS%20KITCHEN_v2_52s_Leticia%20Machado%20de%20Matos.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559470522&amp;usg=AOvVaw3OGvVdrE4jDzKYL5zizb9Z", talento: "Letícia Machado" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/f8138185-76cb-45ed-a019-dc9fea49db86/%5B07%5D%20%5BP01%5D%5BNN%5D%20SOFTYS%20KITCHEN%20-%20Softys%20Kitchen%20(2025-09-24)_v2_19s_Igor_Arvelos.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559471662&amp;usg=AOvVaw3rEhlLJ-s0Ib6JCtbrXVq4", talento: "Ígor Arvelos" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/ec7dc0b3-1312-44de-bae3-abcbbf951f3f/%5B08%5D%20%5BP01%5D%5BNN%5D%20SOFTYS%20KITCHEN%20Softys%20Kitchen%20(20250924)_v1_25s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559472844&amp;usg=AOvVaw2u9A2xBZooOiZdzbt0wv3p", talento: "Letícia Machado" }
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
      "Cliente": "Aiqfome",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/a0b072fd-ea5a-414d-96e1-42478035214f/%5B01%5D%5BP04%5D%5BNN%5D%20%20-%20aiq_ttcx_oc_v4_19s_Yago.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559473910&amp;usg=AOvVaw1hJ3DwznoMwDTUTtc7a2Cm", talento: "Yago Capita" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/1b8bc4cf-21e1-477b-8d86-8688b2c6cc08/%5B02%5D%5BP04%5D%5BNN%5D%20%20%20%20aiq_ttcx_oc_v4_22s_yago.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559474975&amp;usg=AOvVaw2NRpaZBNYIn0Z0ENR9iFja", talento: "Yago Capita" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/f748b9c8-9e91-4e4d-a7ab-4aae1c55ccc5/%5B03%5D%5BP04%5D%5BNN%5D%20aiq_ttcx_oc_v5_47s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559476130&amp;usg=AOvVaw3B9ZZRt38BzgC76bxjOhwl", talento: "Yago Capita" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/df9aac1f-285f-4f3a-ba63-717894d33f5a/%5B04%5D%5BP04%5D%5BNN%5D%20%20%20%20aiq_ttcx_oc_v3_43_Yago.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559477208&amp;usg=AOvVaw1JsxtgJjt77ls8PH6zk4qb", talento: "Yago Capita" }
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
      "Cliente": "Philco Britânia",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/da3a7c5a-53f9-48fd-88bf-4833c83703d6/%5B03%5D%20%5BP02%5D%5BCH%5D%20BRIT%C3%82NIA%20%20%20Philco%20Extreme%20-%20Brand%20Mission%20Mega_v2_58s_Khiara.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559478354&amp;usg=AOvVaw02FMkgdIkLm6v_MFL1_YQt", talento: "Khiara" }
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
      "Cliente": "Mycon",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/cca51772-4fc5-4c99-bce4-8c000cbad358/%5B01%5D%20%5BP01%5D%5BNN%5D%20MYCON%20-%20Net%20New%20-%20Mensal%20(Janeiro%202026)_v3_39s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559479492&amp;usg=AOvVaw1O8BbeDmGjn1vidBrraFEt", talento: "Adam Pereira" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/c03dced2-777f-4d7c-97ba-0f62a0212735/%5B02%5D%20%5BP01%5D%5BNN%5D%20MYCON%20-%20Net%20New%20-%20Mensal%20(Janeiro%202026)_v3_21s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559480568&amp;usg=AOvVaw3Xmmd9WSi_cP6QG1C7VNsK", talento: "Malu Medina" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/1e163d12-e7d6-4f36-95cb-3478fb4b6aed/%5B03%5D%20%5BP01%5D%5BNN%5D%20MYCON%20%20%20Net%20New%20-%20Mensal%20(Janeiro%202026)_v3_48s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559481635&amp;usg=AOvVaw3bCO-XXDUCgZTPvsZQOrPq", talento: "Adam Pereira" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/e92331cb-12eb-4be1-aad3-f2d01b9e6902/%5B04%5D%20%5BP01%5D%5BNN%5D%20MYCON%20%20%20Net%20New%20-%20Mensal%20(Janeiro%202026)_v3_26s_Malu.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559483009&amp;usg=AOvVaw1icaMpAApLDGz5WHYkiQ6c", talento: "Malu Medina" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/931d5494-1822-4d43-b54f-e96f8f32fa4a/%5B05%5D%20%5BP01%5D%5BNN%5D%20MYCON%20%20%20Net%20New%20-%20Mensal%20(Janeiro%202026)_v2_17s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559484178&amp;usg=AOvVaw1JsH7IJ-JkblL5beORvq9C", talento: "Adam Pereira" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/5952744d-28ff-4284-a808-003c75695b78/%5B06%5D%20%5BP01%5D%5BNN%5D%20MYCON%20Net%20New%20Mensal%20(Janeiro%202026)_v4_23s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559485315&amp;usg=AOvVaw2VeqfdjlRNWEKWaDQdzOfs", talento: "Malu Medina" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/8eca60b6-7147-422b-8874-3eb0517b971a/%5B07%5D%20%5BP01%5D%5BNN%5D%20MYCON%20%20%20Net%20New%20-%20Mensal%20(Janeiro%202026)_v3_55s_Malu%20Medina.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559486481&amp;usg=AOvVaw0u4BLWTnhLBS1ooxJEW5to", talento: "Malu Medina" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/06c1c2a8-3567-42b8-93a0-635300721645/%5B08%5D%20%5BP01%5D%5BNN%5D%20MYCON%20-%20Net%20New%20-%20Mensal%20(Janeiro%202026)_v3_35s.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559487636&amp;usg=AOvVaw1mOJ7iwWsqYezU4Y0-x3uY", talento: "Adam Pereira" }
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
      "Cliente": "Atacadão",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2026"
    },
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/194dafb9-b753-4015-8d35-c593933b2073/%5B04%5D%20%5BP04%5D%5BNN%5D%20CARREFOUR%20%20%20Grupo%20Carrefour%20Brasil%20-%20FEV%202026_v2_25s_Quezia.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559492777&amp;usg=AOvVaw2PolPo9rbTIvLhkOw4Ijc8", direcao: true, talento: "Quézia Castro" }
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
      "Cliente": "Cassino.Bet",
      "Plataforma": "TikTok",
      "Agência": "Allfluence",
      "Tipo": "Conteúdo para Redes Sociais",
      "Ano": "2025"
    },
    instagram: "https://www.instagram.com/cassino.bet.br/",
    website: "https://cassino.bet.br/",
    videos: [
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/cf10efe3-8209-46e7-8f8b-3b0bf93a49e2/%5B03%5D%20%5BP01%5D%5BCH%5D%20CASSINO.BET%20%20%20Cassino.bet%20(2025%2004%2008)_v1_32s_Jo%C3%A3o%20Victor.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559294793&amp;usg=AOvVaw2Hmd_IiU2SEG4ph7WkNvXl", talento: "João Victor" },
      { url: "https://t9007008605.p.clickup-attachments.com/t9007008605/48488677-9c83-449c-838c-f0303c5a2a41/%5B04%5D%20%5BP01%5D%5BCH%5D%20CASSINO.BET%20%20Cassino_v1_25s_Jota.mp4?view%3Dopen&amp;sa=D&amp;source=editors&amp;ust=1773169559295816&amp;usg=AOvVaw1vW1-QHmLsN6qetjrSoiuw", talento: "João Victor" }
    ],
    galeria: []
  }
];

// ----------------------------------------
// Header scroll
// ----------------------------------------
const header = document.getElementById('header');
window.addEventListener('scroll', () => {
  header.classList.toggle('scrolled', window.scrollY > 80);
});

// ----------------------------------------
// Fullscreen nav overlay
// ----------------------------------------
const sideMenu = document.getElementById('sideMenu');
const navOverlay = document.getElementById('navOverlay');
const burgerBtn = document.getElementById('burgerBtn');

function toggleNav() {
  navOverlay.classList.toggle('active');
  burgerBtn.classList.toggle('active');
  document.body.style.overflow = navOverlay.classList.contains('active') ? 'hidden' : '';
}

function closeNav() {
  navOverlay.classList.remove('active');
  burgerBtn.classList.remove('active');
  document.body.style.overflow = '';
}

sideMenu.addEventListener('click', toggleNav);
burgerBtn.addEventListener('click', toggleNav);

navOverlay.querySelectorAll('.nav-overlay__link').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    closeNav();
    const target = document.querySelector(link.getAttribute('href'));
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

let activeFilter = 'todos';
filtros.forEach(btn => {
  btn.addEventListener('click', () => {
    filtros.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeFilter = btn.dataset.filter;
    items.forEach(item => {
      const categories = item.dataset.category.split(' ');
      item.classList.toggle('hidden', activeFilter !== 'todos' && !categories.includes(activeFilter));
    });
  });
});

// ----------------------------------------
// Modal
// ----------------------------------------
const modal = document.getElementById('projetoModal');
const modalClose = document.getElementById('modalClose');

function openModal(id) {
  const p = projetos.find(x => x.id === id);
  if (!p) return;

  document.getElementById('modalCategoria').textContent = p.categoriaLabel;
  document.getElementById('modalTitulo').textContent = p.nome;
  document.getElementById('modalDescricao').textContent = p.descricao;

  const videoEl = document.getElementById('modalVideo');
  // Filter videos based on active filter
  const allVideos = p.videos && p.videos.length > 0 ? p.videos : [];
  const displayVideos = activeFilter === 'direcao' && allVideos.length > 0
    ? allVideos.filter(v => v.direcao)
    : allVideos;
  const hasVideos = displayVideos.length > 0;

  if (p.videoId && !p.videoId.startsWith('VIDEO_ID') && p.videoId !== '') {
    videoEl.style.display = '';
    videoEl.innerHTML = `<iframe src="https://www.youtube.com/embed/${p.videoId}?rel=0" allow="encrypted-media" allowfullscreen></iframe>`;
  } else if (hasVideos) {
    videoEl.style.display = '';
    if (displayVideos[0].youtubeId) {
      videoEl.innerHTML = `<iframe src="https://www.youtube.com/embed/${displayVideos[0].youtubeId}?rel=0&autoplay=1" allow="autoplay; encrypted-media" allowfullscreen style="width:100%;height:100%;border:none;"></iframe>`;
    } else {
      videoEl.innerHTML = `<video controls playsinline preload="metadata" style="width:100%;height:100%;object-fit:contain;background:#000"><source src="${displayVideos[0].url}" type="video/mp4">Seu navegador não suporta vídeo.</video>`;
    }
    if (displayVideos[0].talento) {
      videoEl.innerHTML += `<div class="modal__video-talent">${displayVideos[0].talento}</div>`;
    }
  } else if (p.galeria && p.galeria.length > 0) {
    // Photography project: show hero image instead of video placeholder
    videoEl.style.display = '';
    videoEl.innerHTML = `<img src="${p.galeria[0]}" alt="${p.nome}" style="width:100%;height:100%;object-fit:cover;">`;
  } else {
    videoEl.style.display = '';
    videoEl.innerHTML = `<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:var(--text-muted)"><p>Video em breve</p></div>`;
  }

  const fichaEl = document.getElementById('modalFicha');
  fichaEl.innerHTML = Object.entries(p.ficha).map(([k, v]) => `<div><dt>${k}</dt><dd>${v}</dd></div>`).join('');

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
    const domain = new URL(p.website).hostname.replace('www.', '');
    addSocialBtn(p.website, icons.website, domain);
  }
  if (p.website2) {
    const domain2 = new URL(p.website2).hostname.replace('www.', '');
    addSocialBtn(p.website2, icons.website, domain2);
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
        <span class="modal__video-card-talent">${v.talento || 'Video ' + (i + 1)}</span>
      `;
      card.addEventListener('click', () => {
        if (v.youtubeId) {
          videoEl.innerHTML = `<iframe src="https://www.youtube.com/embed/${v.youtubeId}?rel=0&autoplay=1" allow="autoplay; encrypted-media" allowfullscreen style="width:100%;height:100%;border:none;"></iframe>`;
        } else {
          videoEl.innerHTML = `<video controls autoplay playsinline preload="metadata" style="width:100%;height:100%;object-fit:contain;background:#000"><source src="${v.url}" type="video/mp4">Seu navegador não suporta vídeo.</video>`;
        }
        if (v.talento) {
          videoEl.innerHTML += `<div class="modal__video-talent">${v.talento}</div>`;
        }
        galeriaEl.querySelectorAll('.modal__video-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        modal.querySelector('.modal__content').scrollTo({ top: 0, behavior: 'smooth' });
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
        img.onerror = function() { this.style.display = 'none'; };
        img.addEventListener('click', () => openLightbox(p.galeria, i));
        galeriaEl.appendChild(img);
      });
    }
  } else {
    // Image gallery for non-video projects
    const galeriaTitle = document.getElementById('galeriaTitle');
    if (galeriaTitle) galeriaTitle.textContent = `Galeria (${p.galeria.length})`;

    // Use photo-optimized grid for photography projects
    if (p.categoria === 'fotografia' && p.galeria.length > 3) {
      galeriaEl.classList.add('modal__galeria-grid--photos');
    } else {
      galeriaEl.classList.remove('modal__galeria-grid--photos');
    }

    p.galeria.forEach((src, i) => {
      const img = document.createElement('img');
      img.src = src;
      img.alt = p.nome;
      img.loading = 'lazy';
      img.onerror = function() { this.style.display = 'none'; };
      img.addEventListener('click', () => openLightbox(p.galeria, i));
      galeriaEl.appendChild(img);
    });

    // YouTube videos in gallery
    if (p.youtubeGaleria && p.youtubeGaleria.length > 0) {
      if (galeriaTitle) galeriaTitle.textContent = `Galeria (${p.galeria.length + p.youtubeGaleria.length})`;
      p.youtubeGaleria.forEach(vid => {
        const wrapper = document.createElement('a');
        wrapper.href = `https://www.youtube.com/watch?v=${vid}`;
        wrapper.target = '_blank';
        wrapper.rel = 'noopener';
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
}

function closeModal() {
  modal.classList.remove('active');
  document.body.style.overflow = '';
  document.getElementById('modalVideo').innerHTML = '';
}

items.forEach(item => {
  item.addEventListener('click', () => openModal(parseInt(item.dataset.id)));

  // Hover video preview
  const id = parseInt(item.dataset.id);
  const projeto = projetos.find(x => x.id === id);
  if (!projeto) return;

  const hasVideos = (projeto.videos && projeto.videos.length > 0) || projeto.youtubePlaylist || projeto.youtubeGaleria;
  if (!hasVideos || !projeto.videos || !projeto.videos.length) return;

  const firstVideo = projeto.videos[0];
  if (!firstVideo.url && !firstVideo.youtubeId) return;
  // Only local/direct URLs work for hover preview (not YouTube embeds)
  if (!firstVideo.url) return;

  let hoverVideo = null;
  let hoverTimeout = null;
  const thumb = item.querySelector('.trabalhos__thumb');
  const thumbImg = thumb.querySelector('img');

  item.addEventListener('mouseenter', () => {
    if (!hoverVideo) {
      hoverVideo = document.createElement('video');
      hoverVideo.src = firstVideo.url;
      hoverVideo.muted = true;
      hoverVideo.loop = true;
      hoverVideo.playsInline = true;
      hoverVideo.preload = 'metadata';
      hoverVideo.className = 'trabalhos__hover-video';
      thumb.insertBefore(hoverVideo, thumb.querySelector('.trabalhos__play-icon'));
    }
    hoverTimeout = setTimeout(() => {
      hoverVideo.currentTime = 0;
      hoverVideo.play().then(() => {
        hoverVideo.classList.add('active');
        if (thumbImg) thumbImg.style.opacity = '0';
      }).catch(() => {});
    }, 300);
  });

  item.addEventListener('mouseleave', () => {
    clearTimeout(hoverTimeout);
    if (hoverVideo) {
      hoverVideo.pause();
      hoverVideo.classList.remove('active');
      if (thumbImg) thumbImg.style.opacity = '1';
    }
  });
});

modalClose.addEventListener('click', closeModal);
modal.querySelector('.modal__backdrop').addEventListener('click', closeModal);
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

// ----------------------------------------
// Showreel lazy embed
// ----------------------------------------
const showreelEl = document.getElementById('showreelVideo');
if (showreelEl) {
  showreelEl.addEventListener('click', () => {
    const vid = showreelEl.dataset.videoId;
    if (vid && vid !== 'VIDEO_ID') {
      const iframe = document.createElement('iframe');
      iframe.src = `https://www.youtube.com/embed/${vid}?autoplay=1&rel=0`;
      iframe.allow = 'autoplay; encrypted-media';
      iframe.allowFullscreen = true;
      iframe.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;border:none;';
      showreelEl.parentNode.appendChild(iframe);
      showreelEl.remove();
    }
  });
}

// ----------------------------------------
// Scroll reveal
// ----------------------------------------
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.sobre__image, .sobre__content, .trabalhos__header, .trabalhos__item, .showreel__container, .cta__content, .cta__quote, .contato__left, .contato__form, .quote__inner, .clientes__container').forEach(el => {
  el.classList.add('reveal');
  revealObserver.observe(el);
});

// ----------------------------------------
// Clientes -> Modal
// ----------------------------------------
document.querySelectorAll('.clientes__item').forEach(item => {
  item.addEventListener('click', () => {
    // Multiple projects: show picker
    if (item.dataset.ids) {
      const ids = item.dataset.ids.split(',').map(Number);
      const projs = ids.map(id => projetos.find(p => p.id === id)).filter(Boolean);
      if (projs.length === 1) {
        openModal(projs[0].id);
        return;
      }
      showProjectPicker(projs);
      return;
    }
    const clienteName = item.dataset.name || item.textContent.trim();
    const projeto = projetos.find(p => p.nome.toLowerCase() === clienteName.toLowerCase());
    if (projeto) {
      openModal(projeto.id);
    }
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
            <span class="picker-option-name">${p.nome}</span>
            <span class="picker-option-label">${p.categoriaLabel}</span>
          </button>
        `).join('')}
      </div>
    </div>
  `;
  document.body.appendChild(picker);
  requestAnimationFrame(() => picker.classList.add('active'));

  picker.querySelector('.picker-backdrop').addEventListener('click', () => {
    picker.classList.remove('active');
    setTimeout(() => picker.remove(), 300);
  });

  picker.querySelectorAll('.picker-option').forEach(btn => {
    btn.addEventListener('click', () => {
      picker.classList.remove('active');
      setTimeout(() => picker.remove(), 300);
      openModal(parseInt(btn.dataset.id));
    });
  });
}

// ----------------------------------------
// Form
// ----------------------------------------
document.getElementById('contatoForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = e.target;
  const btn = form.querySelector('button[type="submit"]');
  const originalText = btn.textContent;
  btn.textContent = 'Enviando...';
  btn.disabled = true;

  try {
    const res = await fetch('https://formsubmit.co/ajax/savyllaadryan@gmail.com', {
      method: 'POST',
      body: new FormData(form),
      headers: { 'Accept': 'application/json' }
    });

    if (res.ok) {
      btn.textContent = 'Mensagem enviada!';
      form.reset();
      setTimeout(() => {
        btn.textContent = originalText;
        btn.disabled = false;
      }, 3000);
    } else {
      throw new Error('Erro no envio');
    }
  } catch (err) {
    btn.textContent = 'Erro ao enviar. Tente novamente.';
    btn.disabled = false;
    setTimeout(() => { btn.textContent = originalText; }, 3000);
  }
});

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

function openLightbox(images, startIndex) {
  lbImages = images;
  lbIndex = startIndex || 0;
  showLightboxImage();
  lightbox.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeLightbox() {
  lightbox.classList.remove('active');
  document.body.style.overflow = '';
  lightboxTrack.innerHTML = '';
}

function showLightboxImage() {
  lightboxTrack.innerHTML = `<img src="${lbImages[lbIndex]}" alt="Foto ${lbIndex + 1}">`;
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
