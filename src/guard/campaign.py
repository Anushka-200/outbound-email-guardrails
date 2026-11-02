from collections import Counter
from .checks import lint_email

def plan_send(emails, ctx, daily_cap_per_domain=50):
    """Lint every draft, then apply a per-sending-domain daily cap (deliverability protection)."""
    sent, held, per_domain = [], [], Counter()
    for e in emails:
        r = lint_email(e, ctx)
        dom = e["from"].split("@")[-1]
        if not r["send"]:
            held.append({**r, "why": "failed lint"})
        elif per_domain[dom] >= daily_cap_per_domain:
            held.append({"id": e["id"], "send": False, "findings": [("daily_cap", dom)], "why": "cap reached"})
        else:
            per_domain[dom] += 1
            sent.append(e["id"])
    return {"send": sent, "held": held, "sent_count": len(sent), "held_count": len(held)}
