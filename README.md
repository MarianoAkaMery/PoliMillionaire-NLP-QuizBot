# PoliMillionaire-NLP-QuizBot

Project starter for the NLP 2025/26 group assignment: building a local chatbot
that plays **Who wants to be a PoliMillionaire?** through the official course
API client.

## Current Approach

The current implementation focuses on a stable text-mode baseline:

- use the official `millionaire_client` package provided with the course;
- play through the text API, not browser automation;
- run local open-weight Hugging Face models in Colab;
- avoid paid/generative APIs;
- avoid RAG for the first stable version;
- use category-specific prompts for the four competitions;
- benchmark all categories automatically;
- save JSON logs for later error analysis.

The main reason for avoiding RAG for now is practical: the quiz is open-domain
and time-limited to 30 seconds. Real-time retrieval adds latency, while a static
corpus would be hard to justify without adding a lot of noise.

## Notebooks

### `PoliMillionaire.ipynb`

Original notebook provided with the assignment. It documents how the official
API client works.

### `PoliMillionaire_Starter_Ensemble.ipynb`

Clean baseline notebook. It uses:

- one local quantized model;
- category-specific prompts;
- optional calculator support for Maths;
- official `millionaire_client`;
- single-category game runs.

### `PoliMillionaire_Steroids_Ensemble.ipynb`

Experimental benchmark notebook. Despite the name, the current default is a
fast single-model benchmark because ensemble and judge strategies were too slow
in Colab and caused timeouts.

Default behavior:

- runs one game for each category;
- compares Entertainment, Ancient History and Politics, Science and Nature, and
  Maths;
- saves a combined run log under `runs/`.

## Current Model Setup

The current Colab-friendly configuration is:

```python
MODEL_A_NAME = "Qwen/Qwen2.5-3B-Instruct"
LOAD_IN_4BIT = True
USE_ENSEMBLE = False
MAX_NEW_TOKENS = 2
```

This setup was chosen because larger models or multi-model ensembles were often
too slow or unstable on Colab T4.

## Categories

The game currently exposes four text-mode competitions:

| Key | Competition | Description |
| --- | --- | --- |
| `entertainment` | Entertainment | Music, Movies, Celebrities and more |
| `ancient_history_politics` | Ancient History and Politics | The Roman Empire, The Greeks, and more |
| `science_nature` | Science and Nature | Chemistry, Biology, Physics and similar subjects |
| `maths` | Maths | Mathematics and Statistics from High School and College |

## Recent Benchmark Example

One recent benchmark run gave:

```text
Entertainment: 11/12 | level=12 | earned=64000
Ancient History and Politics: 3/4 | level=4 | earned=300
Science and Nature: 9/10 | level=10 | earned=16000
Maths: 2/3 | level=3 | earned=200
```

Another run reached 15/15 on Science and Nature, so there is some variability.
At the moment, Entertainment and Science and Nature look like the most promising
categories for leaderboard runs.

## Running in Colab

1. Upload the project folder to Google Drive.
2. Open `PoliMillionaire_Steroids_Ensemble.ipynb`.
3. Use a GPU runtime, preferably T4:

```text
Runtime > Change runtime type > T4 GPU
```

4. Run the notebook from top to bottom.

The notebook is currently configured to run the all-category benchmark:

```python
RUN_FULL_GAME = False
RUN_ALL_CATEGORIES_BENCHMARK = True
BENCHMARK_RUNS_PER_CATEGORY = 1
```

For a single leaderboard run, change:

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

To submit the first option as a real answer:

```powershell
python tests/test_api_smoke.py --answer-first-option
```

## Notes for the Final Assignment

The final notebook should still be expanded with:

- group member names and Polimi email addresses;
- link to the presentation video;
- coding assistant usage statement;
- more benchmark tables across repeated runs;
- error analysis by category;
- discussion of why RAG and speech mode were not used in the main system;
- comments in Yoda speaking style, as required by the assignment.
