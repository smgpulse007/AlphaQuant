from typing import Dict, Any


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    # TODO: tag entities (tickers, sectors, macro tags) using spaCy/regex
    state["entities"] = {"tickers": [], "macro_tags": []}
    return state

