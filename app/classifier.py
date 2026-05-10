import re

CATEGORY_KEYWORDS = {
    "Politics": [
        # Português
        "governo", "presidente", "congresso", "senado", "câmara",
        "ministro", "ministra", "stf", "supremo", "eleição", "eleições",
        "partido", "deputado", "senador", "prefeito", "governador",
        "política", "planalto",
        # English
        "government", "president", "congress", "senate", "minister",
        "election", "parliament", "prime minister", "policy", "politician",
    ],
    "Economy": [
        # Português
        "economia", "inflação", "juros", "selic", "dólar", "euro",
        "mercado", "bolsa", "ibovespa", "banco central", "pib",
        "imposto", "receita", "fazenda", "preço", "combustível",
        "salário", "emprego", "desemprego",
        # English
        "economy", "inflation", "interest rate", "market", "stocks",
        "central bank", "gdp", "tax", "unemployment", "trade",
        "recession", "tariff",
    ],
    "Technology": [
        # Português
        "tecnologia", "inteligência artificial", "software",
        "hardware", "internet", "celular", "aplicativo",
        "startup", "chip", "semicondutor", "robô", "automação",
        # English
        "technology", "artificial intelligence", "software", "hardware",
        "smartphone", "startup", "semiconductor", "robot",
        "automation", "ai model", "machine learning",
    ],
    "Security": [
        # Português
        "segurança", "polícia", "crime", "prisão", "operação",
        "investigação", "fraude", "golpe", "ataque", "hacker",
        "cibersegurança", "vazamento", "militar", "defesa",
        # English
        "police", "arrest", "investigation",
        "fraud", "cyberattack", "hacker", "cybersecurity", "breach",
        "military", "defense",
    ],
    "International": [
        # Português
        "internacional", "eua", "estados unidos", "china", "rússia",
        "ucrânia", "europa", "oriente médio", "israel", "gaza",
        "onu", "otan", "argentina", "méxico", "irã",
        # English
        "international", "united states", "china", "russia", "ukraine",
        "europe", "middle east", "israel", "gaza", "iran",
        "united nations", "nato", "foreign", "diplomat", "moscow",
        "ukrainian", "russian", "iranian", "israeli", "lebanon",
    ],
    "Health": [
        # Português
        "saúde", "hospital", "médico", "vacina", "doença",
        "vírus", "covid", "sus", "anvisa", "medicamento",
        # English
        "health", "hospital", "doctor", "vaccine", "disease",
        "virus", "outbreak", "medicine", "patient",
    ],
    "Sports": [
        # Português
        "futebol", "esporte", "campeonato", "time", "jogo",
        "seleção", "copa", "atleta", "corrida", "olimpíada",
        # English
        "football", "soccer", "championship",
        "olympics", "athlete", "tournament",
    ],
    "Environment": [
        # Português
        "meio ambiente", "clima", "amazônia", "desmatamento",
        "chuva", "seca", "enchente", "queimada", "sustentabilidade",
        "energia renovável",
        # English
        "climate", "environment", "deforestation", "flood",
        "drought", "wildfire", "sustainability", "renewable energy",
        "emissions", "carbon",
    ],
}


CATEGORY_PRIORITY = [
    "International",
    "Health",
    "Sports",
    "Environment",
    "Security",
    "Economy",
    "Technology",
    "Politics",
]


MIN_SCORE_TO_CLASSIFY = 1


def _count_keyword_matches(text, keywords):
    """
    Count how many keywords from the list appear in the text as whole words.
    Uses regex word boundaries to avoid matching 'ia' inside 'Brasília'.
    """
    score = 0
    for keyword in keywords:
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, text):
            score += 1
    return score


def classify_article(title, summary, source):
    """
    Classify an article using keyword matching with whole-word boundaries.

    Behavior:
    - The 'source' parameter is intentionally not used in the text
      to avoid the source name polluting classification.
    - Keywords are matched as whole words (regex \\b boundaries).
    - When categories tie, CATEGORY_PRIORITY decides the winner.
    - Scores below MIN_SCORE_TO_CLASSIFY fall back to 'General'.
    """
    text = f"{title} {summary}".lower()

    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = _count_keyword_matches(text, keywords)
        if score > 0:
            scores[category] = score

    if not scores:
        return "General"

    best_score = max(scores.values())

    if best_score < MIN_SCORE_TO_CLASSIFY:
        return "General"

    tied_categories = [cat for cat, score in scores.items() if score == best_score]

    for category in CATEGORY_PRIORITY:
        if category in tied_categories:
            return category

    return "General"