# PoliMillionaire-NLP-QuizBot

Project repository for the NLP 2025/26 group assignment: building local chatbot
systems that play **Who wants to be a PoliMillionaire?** through the official
course API client.

## Current State

We now keep two active project notebooks:

- `PoliMillionaire_Steroids_Ensemble.ipynb`  
  Main **text-mode** notebook.

- `PoliMillionaire_Speech_Whisper.ipynb`  
  Separate **speech-mode** experiment using local Whisper ASR.

The original `PoliMillionaire.ipynb` from the professor is kept as API
reference material.

The old starter notebook has been removed because the steroids notebook replaced
it as the working text-mode version.

## Main Text Approach

The current text-mode system uses:

- the official `millionaire_client` package;
- text interaction mode;
- local open-weight Hugging Face models;
- category-specific prompts;
- automatic benchmark runs across all four categories;
- JSON logs for later error analysis;
- a small Maths/statistics tool for recurring patterns;
- a specialized local Maths model as fallback for Maths questions.

No paid LLM APIs are used.

No RAG is used in the main system. The reason is practical: the quiz is
open-domain and the game has a 30-second limit. Real-time retrieval adds latency,
while a static corpus would be hard to justify without adding noise.

## Active Text Notebook

Use:

```text
PoliMillionaire_Steroids_Ensemble.ipynb
```

Default behavior:

```python
RUN_FULL_GAME = False
RUN_ALL_CATEGORIES_BENCHMARK = True
BENCHMARK_RUNS_PER_CATEGORY = 3
```

So by default it runs:

```text
Entertainment x3
Ancient History and Politics x3
Science and Nature x3
Maths x3
```

The current text model setup is:

```python
MODEL_A_NAME = "Qwen/Qwen2.5-3B-Instruct"
MATH_MODEL_NAME = "Qwen/Qwen2.5-Math-1.5B-Instruct"
LOAD_IN_4BIT = True
USE_ENSEMBLE = False
MAX_NEW_TOKENS = 2
MATH_MAX_NEW_TOKENS = 8
```

For Maths, the decision order is:

1. custom Maths/statistics tool;
2. simple calculator;
3. specialized Maths model.

For the other categories, the system uses the general 3B model.

## Speech Notebook

Use:

```text
PoliMillionaire_Speech_Whisper.ipynb
```

This notebook is intentionally separate from the text notebook.

Speech pipeline:

```text
server audio question/options
-> local Whisper transcription
-> local text model answer
-> option_id submitted with official client
```

Current speech setup:

```python
WHISPER_MODEL_NAME = "openai/whisper-small"
ANSWER_MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"
GAME_MODE = "speech"
```

The speech notebook is also configured for category benchmarking:

```python
RUN_FULL_SPEECH_GAME = False
RUN_ALL_CATEGORIES_SPEECH_BENCHMARK = True
SPEECH_BENCHMARK_RUNS_PER_CATEGORY = 3
```

Speech mode is expected to be harder because audio fetching, ASR latency, and
transcription errors happen before answering. The speech notebook logs
transcripts, audio sizes, time remaining after transcription, model output, and
final result.

## Categories

| Key | Competition | Description |
| --- | --- | --- |
| `entertainment` | Entertainment | Music, Movies, Celebrities and more |
| `ancient_history_politics` | Ancient History and Politics | The Roman Empire, The Greeks, and more |
| `science_nature` | Science and Nature | Chemistry, Biology, Physics and similar subjects |
| `maths` | Maths | Mathematics and Statistics from High School and College |

## Current Observations

The model is fast enough in text mode: most answers are produced well below the
30-second limit.

Best leaderboard categories so far:

- Entertainment
- Science and Nature

Current leaderboard status observed during testing:

```text
Entertainment: full score reached
Science and Nature: full score reached
Ancient History and Politics: decent but unstable
Maths: weakest category
```

Maths improved after adding:

- category routing;
- specialized Maths model;
- statistics heuristics;
- better debug logs.

But Maths remains difficult because many questions are not simple arithmetic.
They include statistics theory, abstract algebra, optimization, hypothesis tests,
sampling design, and geometry.

## Running in Colab

1. Upload the project folder to Google Drive.
2. Open either:

```text
PoliMillionaire_Steroids_Ensemble.ipynb
```

or:

```text
PoliMillionaire_Speech_Whisper.ipynb
```

3. Use a GPU runtime:

```text
Runtime > Change runtime type > T4 GPU
```

4. Run from top to bottom.

For a single text leaderboard run, change:

```python
RUN_FULL_GAME = True
RUN_ALL_CATEGORIES_BENCHMARK = False
COMPETITION_KEY = "science_nature"
```

or:

```python
COMPETITION_KEY = "entertainment"
```

## API Smoke Test

To check that the official API client works locally:

```powershell
python tests/test_api_smoke.py
```

This logs in, lists competitions, starts a text game, and prints the question
format without submitting an answer.

To submit a real answer:

```powershell
python tests/test_api_smoke.py --answer-first-option
```

## Repository Notes

Not pushed on purpose:

```text
PoliMillionaire_Rana_Starter_Ensemble.ipynb
```

That notebook was used only as inspiration/reference. The useful ideas were
integrated into our cleaner notebooks where appropriate.

## TODO for Final Submission

- Add group member names and Polimi emails.
- Add presentation video link.
- Add coding assistant usage statement.
- Export final notebook to `.html`.
- Add more benchmark tables across repeated runs.
- Add concise error analysis by category.
- Explain why RAG was not used in the main system.
- Explain speech-mode limitations and ASR impact.
- Ensure final code comments follow the Yoda-speaking-style requirement.
