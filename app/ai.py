import logging
import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# Categorias que recebem resumo mais detalhado (2-3 linhas).
# As demais recebem um resumo curto de 1 linha.
HIGH_PRIORITY_CATEGORIES = {"Politics", "Economy", "Security"}

# Categorias que recebem processamento por IA.
# As demais são exibidas no Source Feed mas não ganham resumo gerado.
RELEVANT_CATEGORIES = {"Politics", "Economy", "Security", "International"}

MODEL = "claude-haiku-4-5"

def is_eligible_for_ai(category, source):
    """
    Decide whether an article should be processed by the AI.

    Currently only the category matters. The 'source' parameter is kept
    in the signature for future flexibility (e.g. excluding low-quality
    sources or applying source-specific rules).
    """
    return category in RELEVANT_CATEGORIES


def _build_prompt(title, summary, category):
    """
    Build the prompt sent to the AI based on the article's category.
    """
    is_high_priority = category in HIGH_PRIORITY_CATEGORIES
    target_length = "2 a 3 linhas" if is_high_priority else "1 linha"

    return (
        f"Você é um analista de notícias. Resuma o artigo abaixo em português, "
        f"em {target_length}. Seja direto, factual, sem opinião. "
        f"Não use frases introdutórias como 'O artigo fala sobre'. "
        f"Comece direto pelo conteúdo.\n\n"
        f"Título: {title}\n\n"
        f"Conteúdo: {summary}"
    )


def generate_article_summary(title, summary, category):
    """
    Generate an AI summary for a single article.

    Returns the summary text, or None if generation failed.
    """
    if not summary or not summary.strip():
        logging.info("Skipping AI summary: article has no source summary.")
        return None

    client = Anthropic()
    prompt = _build_prompt(title, summary, category)

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=300,
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        result = response.content[0].text.strip()

        logging.info(
            f"AI summary generated. Tokens: "
            f"{response.usage.input_tokens} in, "
            f"{response.usage.output_tokens} out."
        )

        return result

    except Exception as error:
        logging.exception(f"Failed to generate AI summary: {error}")
        return None
    
DAILY_BRIEFING_PROMPT = """Você é um analista sênior de inteligência de notícias. Sua tarefa é produzir o briefing diário do dia, em português, baseado nos resumos dos artigos fornecidos abaixo.

Estrutura obrigatória do briefing:

**Cenário geral:** 2 linhas que sintetizam o tom geral do dia.
**Mundo:** 3 a 4 linhas conectando os principais fios geopolíticos e econômicos internacionais. Identifique padrões e relações entre eventos quando existirem.
**Brasil:** 3 a 4 linhas com os principais movimentos da política, economia e segurança no país.
**Por que importa hoje:** 2 linhas explicando o que torna esse dia significativo, ou o que observar a seguir.

Diretrizes:
- Tom factual com análise leve. Você pode conectar pontos e identificar tendências, mas evite opinião editorial.
- Não invente fatos que não estão nos artigos.
- Se uma seção não tiver matéria-prima suficiente, escreva uma linha curta reconhecendo isso ("Pouca movimentação relevante no Brasil hoje.") em vez de inflar.
- Não use listas com bullets. Texto corrido em cada seção.
- Mantenha cada seção no tamanho indicado.

Artigos do dia:

{articles_block}
"""


def _format_articles_for_briefing(articles):
    """
    Format article summaries into a numbered text block for the briefing prompt.
    """
    lines = []
    for i, article in enumerate(articles, start=1):
        lines.append(
            f"[{i}] ({article['category']} | {article['source']}) "
            f"{article['title']}\n"
            f"    {article['ai_summary']}"
        )
    return "\n\n".join(lines)


def generate_daily_briefing(articles):
    """
    Generate the daily briefing from a list of articles with ai_summary.

    Returns a dict with: content, input_tokens, output_tokens, model.
    Returns None if generation failed or no articles were provided.
    """
    if not articles:
        logging.info("No articles available to generate daily briefing.")
        return None

    client = Anthropic()
    articles_block = _format_articles_for_briefing(articles)
    prompt = DAILY_BRIEFING_PROMPT.format(articles_block=articles_block)

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=600,
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        content = response.content[0].text.strip()

        logging.info(
            f"Daily briefing generated. Articles: {len(articles)}. "
            f"Tokens: {response.usage.input_tokens} in, "
            f"{response.usage.output_tokens} out."
        )

        return {
            "content": content,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "model": MODEL,
        }

    except Exception as error:
        logging.exception(f"Failed to generate daily briefing: {error}")
        return None