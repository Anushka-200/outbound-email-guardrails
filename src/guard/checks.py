import re

SPAM_WORDS = ("guaranteed", "100% free", "act now", "risk-free", "limited time", "winner", "no obligation", "click here")
TOKEN_LEFT = re.compile(r"\{\{[^}]*\}\}|\[(?:first_?name|company|name)\]|\bundefined\b|\bNone\b", re.I)
NUMBER_CLAIM = re.compile(r"\b\d[\d,.]*\s?(?:%|x|k|m|million|customers|users|teams)\b", re.I)

def check_unresolved_tokens(email, ctx):
    m = TOKEN_LEFT.search(email["subject"] + " " + email["body"])
    return ("unresolved_token", f"found '{m.group(0)}'") if m else None

def check_unsubscribe(email, ctx):
    low = email["body"].lower()
    return None if ("unsubscribe" in low or "opt out" in low or "reply stop" in low) else ("no_unsubscribe", "missing opt-out line")

def check_spam_words(email, ctx):
    low = (email["subject"] + " " + email["body"]).lower()
    hits = [w for w in SPAM_WORDS if w in low]
    return ("spam_words", ", ".join(hits)) if hits else None

def check_claims_grounded(email, ctx):
    """Every numeric claim about *our product or customers* must appear in the approved fact sheet."""
    facts = " ".join(ctx.get("approved_facts", [])).lower()
    bad = [c for c in NUMBER_CLAIM.findall(email["body"]) if c.lower() not in facts]
    return ("ungrounded_claim", f"not in fact sheet: {bad[0]}") if bad else None

def check_length(email, ctx):
    words = len(email["body"].split())
    return ("too_long", f"{words} words (max {ctx.get('max_words', 120)})") if words > ctx.get("max_words", 120) else None

def check_recipient(email, ctx):
    if email["to"].lower() in {e.lower() for e in ctx.get("suppression_list", [])}:
        return ("suppressed_recipient", email["to"])
    return None

CHECKS = [check_unresolved_tokens, check_unsubscribe, check_spam_words, check_claims_grounded, check_length, check_recipient]

def lint_email(email, ctx):
    findings = [r for r in (c(email, ctx) for c in CHECKS) if r]
    return {"id": email["id"], "send": not findings, "findings": findings}
