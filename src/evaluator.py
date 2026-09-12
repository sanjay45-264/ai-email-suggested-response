import re, math
from collections import Counter

def tokens(text):
    return re.findall(r"[a-zA-Z0-9']+", text.lower())

def cosine(a,b):
    keys=set(a)|set(b)
    na=sum(a.get(k,0)**2 for k in keys)**0.5
    nb=sum(b.get(k,0)**2 for k in keys)**0.5
    if not na or not nb: return 0
    return sum(a.get(k,0)*b.get(k,0) for k in keys)/(na*nb)

def overlap(a,b):
    A=set(tokens(a)); B=set(tokens(b))
    return len(A&B)/max(1,len(A|B))

def important_terms(text):
    # Lightweight heuristic: numbers, times, dates, and longer content words.
    raw=tokens(text)
    return {x for x in raw if any(c.isdigit() for c in x) or len(x)>=6}

def evaluate(incoming, reference_reply, generated):
    semantic=round(100*cosine(Counter(tokens(reference_reply)),Counter(tokens(generated))),1)
    info_terms=important_terms(incoming)
    gen=set(tokens(generated))
    coverage=100 if not info_terms else round(100*len(info_terms & gen)/len(info_terms),1)
    # Intent proxy: compare generated and reference meaning/content overlap.
    intent=round(100*overlap(reference_reply,generated),1)
    relevance=round(min(100,0.65*semantic+0.35*intent),1)
    professional=100.0
    informal={"lol","haha","bro","dude","gonna","wanna"}
    if informal & gen: professional-=25
    if len(generated.split())>100: professional-=10
    professional=max(0,professional)
    score=round(.35*semantic+.25*intent+.20*coverage+.10*relevance+.10*professional,1)
    issues=[]
    if semantic<60: issues.append("The generated reply differs substantially in meaning/content from the reference.")
    if coverage<80: issues.append("Some potentially important details from the incoming email may be missing.")
    if professional<90: issues.append("Tone or length could be more professional.")
    if not issues: issues.append("No major quality issues detected by the automatic evaluator.")
    return {
      "overall_score":score,
      "semantic_correctness":semantic,
      "intent_alignment":intent,
      "information_coverage":coverage,
      "relevance":relevance,
      "professional_tone":round(professional,1),
      "explanation":" ".join(issues)
    }

def evaluate_dataset(items):
    results=[]
    for x in items:
        r=evaluate(x["email"],x["reply"],x["generated_reply"])
        results.append({"id":x["id"],**r})
    avg={k:round(sum(r[k] for r in results)/len(results),1) for k in
         ["overall_score","semantic_correctness","intent_alignment","information_coverage","relevance","professional_tone"]}
    return results,avg
