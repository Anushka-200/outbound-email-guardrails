import json, sys
from .campaign import plan_send

def main(argv=None):
    path = (argv or sys.argv[1:] or ["data/emails.json"])[0]
    d = json.load(open(path))
    plan = plan_send(d["emails"], d["context"], daily_cap_per_domain=2)
    print(f"send={plan['send']} held={plan['held_count']}")
    for h in plan["held"]:
        print(f"- {h['id']}: " + "; ".join(f"{k}: {v}" for k, v in h["findings"]))

if __name__ == "__main__":
    main()
