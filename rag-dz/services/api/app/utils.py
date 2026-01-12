def estimate_tokens(text: str) -> int:
    """Estimation conservative des tokens (1.3 tokens par mot)"""
    return max(100, int(1.3 * len(text.split())))
