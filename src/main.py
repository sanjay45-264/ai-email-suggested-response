import argparse, json
from pathlib import Path
from .generator import generate_reply
from .evaluator import evaluate

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--email",required=True)
    p.add_argument("--reference",default=None,help="Optional expected/reference reply for evaluation")
    args=p.parse_args()
    reply,mode=generate_reply(args.email)
    print("\nSUGGESTED REPLY\n----------------")
    print(reply)
    print(f"\nGeneration mode: {mode}")
    if args.reference:
        result=evaluate(args.email,args.reference,reply)
        print("\nQUALITY SCORE\n-------------")
        print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
