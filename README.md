# PoliMillionaire NLP QuizBot

Repository for the NLP 2025/26 group assignment **Who wants to be a
PoliMillionaire?**.

The project builds and evaluates local open-weight chatbot systems that play the
official online quiz through the course-provided API client. No paid LLM APIs are
used for answering questions.

## Submitted Notebooks

The repository contains two active notebooks:

| Notebook | Purpose |
| --- | --- |
| `PoliMillionaire_Text_QuizBot.ipynb` | Main text-mode system and benchmark notebook |
| `PoliMillionaire_Speech_QuizBot.ipynb` | Speech-mode experiment using local Whisper ASR |

The original `PoliMillionaire.ipynb` is kept as professor-provided reference
material for the game API. The `millionaire_client/` package is the official
course client used by both notebooks.

## Main Text System

The main system is implemented in:

```text
PoliMillionaire_Text_QuizBot.ipynb
```

It uses:

- the official `millionaire_client` package;
- text interaction mode;
- local Hugging Face open-weight models;
- category-specific prompts;
- all-category benchmarking;
- JSON run logs;
- deterministic Maths/statistics tools for recurring patterns;
- a specialized local Maths model as fallback for Maths questions.

Default benchmark settings:

```python
RUN_FULL_GAME = False
RUN_ALL_CATEGORIES_BENCHMARK = True
BENCHMARK_RUNS_PER_CATEGORY = 3
```

This runs three games for each category:

```text
Entertainment
Ancient History and Politics
Science and Nature
Maths
Philosophy and Psychology
News
```

The notebook contains provisional IDs for the six known categories, then
refreshes them from `client.competitions.list_all()` after login. This keeps the
benchmark aligned with the final testing phase if the server assigns different
public IDs.

Current text model settings:

```python
MODEL_A_NAME = "Qwen/Qwen2.5-3B-Instruct"
MATH_MODEL_NAME = "Qwen/Qwen2.5-Math-1.5B-Instruct"
LOAD_IN_4BIT = True
USE_ENSEMBLE = False
MAX_NEW_TOKENS = 2
MATH_MAX_NEW_TOKENS = 4
```

For Maths, the decision order is:

1. custom Maths/statistics heuristics;
2. simple calculator;
3. specialized Maths model.

Generative Maths question rewriting was tested and removed from the default
pipeline because it increased latency and sometimes produced non-parsable model
outputs.

## Speech System

The speech experiment is implemented in:

```text
PoliMillionaire_Speech_QuizBot.ipynb
```

Speech pipeline:

```text
server audio question/options
-> local Whisper transcription
-> deterministic transcript cleanup
-> local text model answer
-> official option_id submission
```

Current speech model settings:

```python
WHISPER_MODEL_NAME = "openai/whisper-small"
ANSWER_MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"
GAME_MODE = "speech"
```

Default speech benchmark settings:

```python
RUN_FULL_SPEECH_GAME = False
RUN_ALL_CATEGORIES_SPEECH_BENCHMARK = True
SPEECH_BENCHMARK_RUNS_PER_CATEGORY = 3
```

Speech mode logs raw transcripts, cleaned transcripts, audio sizes, time
remaining after ASR, model outputs, and final game results. A generative
transcript normalizer was tested and removed because it sometimes changed or
truncated answer options.

## Categories

| Key | Competition | Description |
| --- | --- | --- |
| `entertainment` | Entertainment | Music, Movies, Celebrities and more |
| `ancient_history_politics` | Ancient History and Politics | The Roman Empire, The Greeks, and more |
| `science_nature` | Science and Nature | Chemistry, Biology, Physics and similar subjects |
| `maths` | Maths | Mathematics and Statistics from High School and College |
| `philosophy_psychology` | Philosophy and Psychology | Great thinkers and the human psyche |
| `news` | News | Staying current with global breaking news |

## Design Choices

### No RAG in the Main System

RAG was considered but not used in the main submitted text system. The quiz is
open-domain and time-limited to 30 seconds per question. A real-time retrieval
pipeline would add latency, while a static corpus would be hard to justify for
all categories without adding substantial noise.

### Local Models Only

All answer generation is performed locally with open-weight models. The notebooks
do not call paid LLM APIs to answer quiz questions.

### Deterministic Tools

Maths uses deterministic tools only when a pattern is clear and stable, for
example percentage changes, confidence-interval interpretation, hypothesis-test
form selection, correlation interpretation, and selected statistics concepts.
Otherwise, the specialized Maths model answers directly.

## Observations

Text mode is fast enough for the 30-second limit. Most text answers are produced
in well under one second, except for some Maths questions.

Strongest observed categories:

- Entertainment
- Science and Nature

More unstable categories:

- Ancient History and Politics
- Maths

Maths improved after adding category routing, deterministic statistics tools,
and a specialized Maths model, but it remains difficult because many questions
are conceptual rather than simple arithmetic.

Speech mode is harder than text mode because audio fetching and ASR happen before
answering. The main errors come from transcription noise, especially for names,
technical terms, numbers, and short answer options.

## Running in Colab

1. Upload the repository folder to Google Drive.
2. Open one of the active notebooks.
3. Select a GPU runtime:

```text
Runtime > Change runtime type > T4 GPU
```

4. Run the notebook from top to bottom.

For one single text-mode run instead of the all-category benchmark:

```python
RUN_FULL_GAME = True
RUN_ALL_CATEGORIES_BENCHMARK = False
COMPETITION_KEY = "science_nature"
```

For speech mode, use the analogous flags:

```python
RUN_FULL_SPEECH_GAME = True
RUN_ALL_CATEGORIES_SPEECH_BENCHMARK = False
COMPETITION_KEY = "science_nature"
```

## Local API Smoke Test

To verify that the official API client works:

```powershell
python tests/test_api_smoke.py
```

This logs in, lists competitions, starts a text-mode game, and prints the
question format without submitting an answer.

To submit the first option as a real test answer:

```powershell
python tests/test_api_smoke.py --answer-first-option
```

## Repository Notes

`PoliMillionaire_Rana_Starter_Ensemble.ipynb` is intentionally not tracked. It
was used only as external reference material while comparing ideas.

The submitted work should focus on the two active notebooks listed above.

## Final Submission Reminder

Before uploading to WeBeep, the notebook header should include:

- group member names and Polimi email addresses;
- video link;
- coding assistant usage statement;
- exported `.html` version of the final notebook.
