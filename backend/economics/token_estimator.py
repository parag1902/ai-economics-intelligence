import tiktoken


def get_tokenizer(model_name: str):
    """
    Returns the tokenizer compatible with the target model.

    Currently supports OpenAI models available in tiktoken.
    """

    try:
        return tiktoken.encoding_for_model(model_name)

    except KeyError:
        raise ValueError(
            f"No supported tokenizer mapping found for: {model_name}"
        )


def estimate_tokens(
    text: str,
    model_name: str = "gpt-4o-mini"
) -> int:
    """
    Counts tokens in actual text using the target model tokenizer.
    """

    if not text:
        return 0

    tokenizer = get_tokenizer(model_name)

    return len(tokenizer.encode(text))


def estimate_text_tokens(
    text: str,
    model_name: str = "gpt-4o-mini"
) -> dict:
    """
    Returns token count and estimation details.
    """

    token_count = estimate_tokens(text, model_name)

    return {
        "model": model_name,
        "character_count": len(text),
        "token_count": token_count,
        "method": "Model-compatible tokenizer",
        "is_actual_text_count": True
    }