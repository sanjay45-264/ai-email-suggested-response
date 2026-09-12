import json, re
from pathlib import Path
from collections import Counter

def tokenize(text):
    return re.findall(r"[a-zA-Z0-9']+", text.lower())

def cosine(a,b):
    keys=set(a)|set(b)
    da=sum(a.get(k,0)**2 for k in keys)**0.5
    db=sum(b.get(k,0)**2 for k in keys)**0.5
    if not da or not db: return 0.0
    return sum(a.get(k,0)*b.get(k,0) for k in keys)/(da*db)

def retrieve(email, k=3, dataset_path=None):
    dataset_path = dataset_path or Path(__file__).parents[1]/"data/emails.json"
    data=json.loads(Path(dataset_path).read_text(encoding="utf-8"))
    q=Counter(tokenize(email))
    scored=[]
    for item in data:
        d=Counter(tokenize(item["email"]))
        scored.append((cosine(q,d),item))
    scored.sort(key=lambda x:x[0],reverse=True)
    return [item for _,item in scored[:k]]
