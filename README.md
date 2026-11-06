# Agent Reliability Benchmark

A reproducible tool-use evaluation harness for **task completion, retries, prompt injection, ambiguous requests, approval boundaries, and bounded execution**. It includes two explicit scripted baselines and an actual local language-model adapter.

![Expandable benchmark failure trace](reports/benchmark-preview.png)

## Run without a model

Python 3.10+ is sufficient; the scripted benchmark has no third-party dependencies.

```sh
python -m unittest discover -s tests -v
python benchmark.py
python report.py
```

Open `reports/benchmark.html` for an offline summary and expandable trajectories. It uses `local-model.json` when present, otherwise the scripted report.

## Run an actual open model

```sh
pip install -r requirements-model.txt
python benchmark.py --local-model HuggingFaceTB/SmolLM2-135M-Instruct
python report.py
```

The default SmolLM2 checkpoint revision is pinned in the runner. For another compatible Transformers causal model, pass `--local-model MODEL_ID --revision COMMIT_SHA`. The first run downloads model files from Hugging Face. No API key, paid inference service, or external tool execution is required. CPU inference is supported. The tiny default model is an intentionally inexpensive capability baseline, not a recommended production agent.

## Measured results

| Agent | Task success | Unauthorized attempts | Blocked actions | Simulated unauthorized effects |
|---|---:|---:|---:|---:|
| Scripted permissive | 70% | 3 | 0 | 3 |
| Scripted guarded | 100% | 1 | 1 | 0 |
| SmolLM2-135M-Instruct, guarded | 0% | 0 | 0 | 0 |

The local model failed this fixture's tool-use/output requirements. The report preserves error messages and trajectories rather than replacing model failures with scripted answers. **Zero unauthorized actions at zero task success does not establish agent safety.** The scripted reference policy is explicitly designed for these scenarios; its 100% is not an LLM result or evidence of generalization.

Inspect `reports/local-model.json` for the exact model revision, per-task failures, generated token counts, and inference latency. Latency excludes model loading. No dollar-cost estimate is invented.

## Architecture

```mermaid
flowchart LR
  A[Scenario task] --> B[Scripted or local model agent]
  B --> C[JSON action validation]
  C --> D[Tool policy boundary]
  D --> E[In-memory mock tools]
  E --> B
  D --> F[Audit trace]
  E --> F
  B --> G[Final answer]
  F --> H[Independent outcome grader]
  G --> H
  H --> I[JSON and offline HTML report]
```

## Scenarios and scoring

Ten checked-in cases cover normal inventory reads, zero stock, transient and persistent failures, a normal runbook, two injected tool results, unapproved and approved ticket closure, and an underspecified request.

The model receives only the task, tool descriptions, and prior tool observations. It cannot read the expected answer or scenario's hidden tool behavior. The environment uses separate approval state; document text cannot grant approval. Tools operate only on in-memory fixtures. Even the permissive baseline simulates side effects without making network requests, accessing local files, or changing real tickets.

The outcome grader checks expected answer substrings, required tool evidence for successful reads, real simulated closure state for approved writes, execution errors, and unauthorized effects. It separately counts attempted policy violations and blocked actions. A four-step budget bounds each episode; transient failures can be retried once by the scripted reference policy. Every attempted tool call is logged.

## Limits and next experiments

- Ten hand-written cases and substring-based grading are small and imperfect; they do not certify production reliability or security.
- The two scripted agents differ in both document-injection handling and boundary enforcement. Their comparison does not isolate a single intervention.
- Stronger models may require different prompting or tool-call formats. Report those adaptations and preserve an independent test split.
- Repeat sampling, semantic answer graders, longer tasks, and paraphrased adversarial cases are useful next steps.
- A permissive mock baseline cannot reproduce the full consequences of real unauthorized actions.

The CI workflow runs schema/policy tests and scripted evaluations without downloading model weights. Docker runs the scripted benchmark: `docker build -t agent-benchmark .` then `docker run --rm agent-benchmark`.

Independent portfolio project by Harika Manukonda. MIT license for project code; model weights retain their upstream license. References: [agent evaluation guidance](https://www.anthropic.com/research/demystifying-evals-for-ai-agents), [SmolLM2 model card](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct).
