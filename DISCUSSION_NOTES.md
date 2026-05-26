# Discussion Notes

Short guide for the project video and final interview.

## Main System

The main submitted system is `PoliMillionaire_Text_QuizBot.ipynb`.

It uses text mode because the official game API already returns the question and
answer options in textual form. This is the cleanest and fastest interface for a
30-second quiz.

Core components:

- official `millionaire_client`;
- local open-weight Qwen2.5 3B model;
- category-specific prompts;
- deterministic Maths/statistics tools;
- specialized local Maths fallback model;
- repeated benchmark runs over all six final categories.

## Categories

The final testing phase includes six categories:

- Entertainment
- Ancient History and Politics
- Science and Nature
- Maths
- Philosophy and Psychology
- News

The notebooks include these categories and refresh competition IDs from the API
after login.

## Why No RAG

RAG was considered but not used in the main system.

Reasons:

- questions are broad and open-domain;
- retrieval would add latency inside a 30-second timeout;
- a static corpus would be difficult to justify across all categories;
- retrieved documents could add noise for short quiz questions.

The final system instead focuses on local models, prompt design, deterministic
tools, and benchmark analysis.

## Maths Strategy

Maths is the weakest and most variable category.

The final decision order is:

1. deterministic statistics/Maths heuristics;
2. simple calculator;
3. specialized local Maths model.

Generative Maths question rewriting was tested and removed because it increased
latency and sometimes produced non-parsable outputs.

## Speech Experiment

The speech notebook is `PoliMillionaire_Speech_QuizBot.ipynb`.

Pipeline:

```text
audio question/options -> Whisper ASR -> deterministic cleanup -> local answer model
```

Speech is not the main competitive system because ASR can distort names,
numbers, technical terms, and short answer options. It is still useful as an
additional architecture and shows the impact of transcription errors.

## Main Limitations

- niche factual knowledge can still fail;
- misleading answer options can confuse the model;
- Maths conceptual questions are not always solvable by simple tools;
- speech mode is sensitive to ASR quality;
- no external LLM API is used, so performance depends on local model capacity.

