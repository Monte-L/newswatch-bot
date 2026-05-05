CATEGORY_KEYWORDS = {
    "Politics": [
        "governo", "presidente", "congresso", "senado", "câmara",
        "ministro", "ministra", "stf", "supremo", "eleição", "eleições",
        "partido", "deputado", "senador", "prefeito", "governador",
        "política", "planalto"
    ],
    "Economy": [
        "economia", "inflação", "juros", "selic", "dólar", "euro",
        "mercado", "bolsa", "ibovespa", "banco central", "pib",
        "imposto", "receita", "fazenda", "preço", "combustível",
        "salário", "emprego", "desemprego"
    ],
    "Technology": [
        "tecnologia", "inteligência artificial", "ia", "software",
        "hardware", "internet", "celular", "aplicativo", "dados",
        "startup", "chip", "semicondutor", "robô", "automação"
    ],
    "Security": [
        "segurança", "polícia", "crime", "prisão", "operação",
        "investigação", "fraude", "golpe", "ataque", "hacker",
        "cibersegurança", "vazamento", "militar", "defesa"
    ],
    "International": [
        "internacional", "eua", "estados unidos", "china", "rússia",
        "ucrânia", "europa", "oriente médio", "israel", "gaza",
        "onu", "otan", "argentina", "mexico", "méxico"
    ],
    "Health": [
        "saúde", "hospital", "médico", "vacina", "doença",
        "vírus", "covid", "sus", "anvisa", "medicamento"
    ],
    "Sports": [
        "futebol", "esporte", "campeonato", "time", "jogo",
        "seleção", "copa", "atleta", "corrida", "olimpíada"
    ],
    "Environment": [
        "meio ambiente", "clima", "amazônia", "desmatamento",
        "chuva", "seca", "enchente", "queimada", "sustentabilidade",
        "energia renovável"
    ],
}


def classify_article(title, summary, source):
    """
    Classify an article using simple keyword matching.

    This is an initial rule-based classifier.
    Later, this can be improved with better NLP or manual categories per feed.
    """
    text = f"{title} {summary} {source}".lower()

    best_category = "General"
    best_score = 0

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0

        for keyword in keywords:
            if keyword in text:
                score += 1

        if score > best_score:
            best_score = score
            best_category = category

    return best_category