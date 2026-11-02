import json, pathlib
from guard.checks import lint_email
from guard.campaign import plan_send

D = json.loads((pathlib.Path(__file__).parent.parent / "data/emails.json").read_text())
CTX, E = D["context"], {e["id"]: e for e in D["emails"]}
kinds = lambda i: {k for k, _ in lint_email(E[i], CTX)["findings"]}

def test_good_email_sends():
    assert lint_email(E["ok-1"], CTX)["send"]

def test_each_failure_mode():
    assert kinds("token-2") == {"unresolved_token"}
    assert kinds("claim-3") == {"ungrounded_claim"}
    assert kinds("noopt-4") == {"no_unsubscribe"}
    assert kinds("spam-5") == {"spam_words"}
    assert kinds("supp-6") == {"suppressed_recipient"}

def test_daily_cap_holds_extra_good_emails():
    plan = plan_send(D["emails"], CTX, daily_cap_per_domain=2)
    assert plan["send"] == ["ok-1", "ok-7"]
    assert any(h["id"] == "ok-8" and h["why"] == "cap reached" for h in plan["held"])

def test_grounded_numbers_allowed():
    assert not [f for f in lint_email(E["ok-7"], CTX)["findings"] if f[0] == "ungrounded_claim"]
