# AI Email Suggested Response System

An end-to-end prototype that takes an incoming email, retrieves similar historical email/reply examples, generates a suggested response with an LLM, and evaluates response quality.

## 1. Approach

Pipeline:

Incoming email → retrieval over past emails → LLM response generation → multi-dimensional evaluation → per-response and overall scores.

The response generator uses RAG-style grounding. The retriever finds semantically/lexically similar historical emails and supplies their replies as few-shot examples to the LLM.

### Why RAG instead of fine-tuning?

RAG is easier to update: adding a new email/reply pair does not require retraining a model. It also makes the source examples visible and reduces the risk of the model inventing an organization-specific style. Fine-tuning could improve consistency at larger scale, but would require more data and a training/evaluation pipeline.

## 2. Dataset

The included dataset is synthetic and hand-authored. It was chosen to avoid exposing private email content while covering common professional scenarios: meetings, rescheduling, leave, follow-ups, information requests, customer questions, apologies, thank-you messages, and project updates.

Run:

```bash
python data/generate_dataset.py
```

The dataset is intentionally small for the prototype. For a production-quality experiment, expand it to hundreds/thousands of examples and add a held-out test split.

## 3. Generation

If `OPENAI_API_KEY` is configured, `src/generator.py` sends the new email plus retrieved historical examples to an OpenAI-compatible chat model. Set `OPENAI_MODEL` to the model available to your account.

Without an API key, the project still runs end-to-end using a deterministic retrieval fallback. This is useful for testing the evaluation and UI, but it is not the Gen-AI path and should not be presented as the final generation quality result.

Set:

```bash
export OPENAI_API_KEY="your-key"
export OPENAI_MODEL="your-model"
```

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your-key"
$env:OPENAI_MODEL="your-model"
```

## 4. Evaluation — core of the project

Exact string match is not appropriate because multiple replies can be equally good. For example, “Friday works for me” and “Friday is fine with me” have the same practical meaning.

The automatic evaluator therefore reports:

| Dimension | Weight |
|---|---:|
| Semantic correctness | 35% |
| Intent alignment | 25% |
| Important information coverage | 20% |
| Relevance | 10% |
| Professional tone | 10% |

Overall score:

`0.35*semantic + 0.25*intent + 0.20*coverage + 0.10*relevance + 0.10*tone`

The evaluator also produces an explanation and flags detected issues.

### Important limitation

The included evaluator is deliberately transparent and lightweight. Its semantic component is lexical cosine similarity rather than a hidden “magic” score. For a stronger experiment, replace this with a sentence-embedding model and/or an LLM judge, then validate it against humans.

## 5. Metric validation

A real validation study should sample generated responses and have human reviewers rate them on a 1–5 quality scale. Compare those ratings with automatic scores using Spearman correlation and inspect disagreements.

Recommended validation set:
- 50–100 generated responses
- At least two human raters where possible
- Include good, mediocre, and deliberately bad responses
- Report correlation and examples of false positives/false negatives

This matters because an evaluator can otherwise reward superficial text similarity rather than useful replies.

## 6. Running

Install:

```bash
pip install -r requirements.txt
```

Run the web demo:

```bash
streamlit run app.py
```

Run from the command line:

```bash
python -m src.main --email "Can we move our meeting to Friday afternoon?"
```

Evaluate a response when the reference reply is known:

```bash
python -m src.main   --email "Can we move our meeting to Friday afternoon?"   --reference "Sure, Friday afternoon works for me. What time would you prefer?"
```

Run tests:

```bash
pytest
```

## 7. Reporting per-response and overall scores

For a full experiment, generate responses for a held-out test set, call `evaluate()` for each response, and save the resulting JSON/CSV. The evaluator returns:

- overall score
- semantic correctness
- intent alignment
- information coverage
- relevance
- professional tone
- explanation

The mean of each dimension gives the overall system report.

## 8. Trade-offs and limitations

- Synthetic data is safer and easier to reproduce, but may not represent real-world email diversity perfectly.
- Lexical retrieval is simple and dependency-light, but production retrieval should use sentence embeddings/vector search.
- Automatic evaluation can disagree with humans; human correlation is required before treating the score as a trustworthy quality metric.
- The reference reply is used for evaluation, not for generation. In real use, there may be no reference reply, so generation-time quality should also be checked with a reference-free evaluator.
- Email privacy, prompt injection, confidential information, and hallucination controls would need additional engineering for production deployment.

## 9. AI tools used

AI assistance was used for project planning, code scaffolding, synthetic dataset drafting, debugging ideas, and README structure. The generated code should be reviewed and tested by the project author. No private email data is included in the repository.

## 10. Suggested next improvements

1. Expand dataset to 500+ examples.
2. Create train/retrieval and held-out test splits.
3. Use sentence-transformer embeddings + FAISS.
4. Add an LLM-as-judge evaluator with a strict JSON schema.
5. Run a 50–100 sample human evaluation.
6. Calculate Spearman correlation with human ratings.
7. Add confidence/abstention when the system is uncertain.
8. Add prompt-injection and hallucination tests.
