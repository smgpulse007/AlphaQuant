from typing import Dict, Any


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    # TODO: fetch documents (Playwright/HTTPx) honoring robots.txt and TOS
    state["raw_docs"] = []  # list of RawDoc
    return state

