"""Generate the included synthetic email/reply dataset.
The examples are intentionally hand-authored and can be expanded safely.
"""
import json
from pathlib import Path
from copy import deepcopy

EXTRA = [
 {"id":"021","category":"rescheduling","email":"Could we shift our Friday review to Monday morning?","reply":"Sure, Monday morning works. What time would you prefer?"},
 {"id":"022","category":"follow_up","email":"I wanted to follow up about the invoice I sent earlier this week.","reply":"Thanks for following up. I’ll check on the invoice and get back to you shortly."},
 {"id":"023","category":"customer_question","email":"Can I change the delivery address for my order?","reply":"Please share your order number and the new address, and we’ll check whether it can still be changed."},
 {"id":"024","category":"project_update","email":"The client approved the revised scope, so we can begin implementation.","reply":"Excellent. Thanks for the update. Please keep me posted as implementation begins."},
 {"id":"025","category":"meeting","email":"Could we schedule a 30-minute meeting sometime tomorrow afternoon?","reply":"Sure. I’m available tomorrow afternoon. What time works best for you?"},
]

def main():
    path = Path(__file__).with_name("emails.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    existing = {x["id"] for x in data}
    data.extend([x for x in EXTRA if x["id"] not in existing])
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding="utf-8")
    print(f"Wrote {len(data)} examples to {path}")

if __name__ == "__main__":
    main()
