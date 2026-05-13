"""Small smoke test for the official PoliMillionaire API client."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from millionaire_client import AuthenticationError, MillionaireClient, MillionaireError


DEFAULT_API_URL = "http://131.175.15.22:51111/"
DEFAULT_USERNAME = "MarianoAkaMery"
DEFAULT_PASSWORD = "Test1234!"


def get_config() -> tuple[str, str, str]:
    """Read config from environment, falling back to notebook defaults."""
    api_url = os.environ.get("POLI_MILLIONAIRE_URL", DEFAULT_API_URL)
    username = os.environ.get("POLI_MILLIONAIRE_USERNAME", DEFAULT_USERNAME)
    password = os.environ.get("POLI_MILLIONAIRE_PASSWORD", DEFAULT_PASSWORD)
    return api_url, username, password


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-test the PoliMillionaire API client.")
    parser.add_argument("--competition-id", type=int, default=1)
    parser.add_argument("--mode", choices=["text", "speech"], default="text")
    parser.add_argument(
        "--answer-first-option",
        action="store_true",
        help="Submit the first available option. This affects a real game session.",
    )
    args = parser.parse_args()

    api_url, username, password = get_config()
    client = MillionaireClient(api_url)

    try:
        user = client.login(username, password)
        print(f"LOGIN_OK username={user.username} role={user.role}")

        competitions = client.competitions.list_all()
        print(f"COMPETITIONS_OK count={len(competitions)}")
        for comp in competitions:
            print(f"  {comp.id}: {comp.name} max_levels={comp.max_levels}")

        game = client.game.start(competition_id=args.competition_id, mode=args.mode)
        print(f"GAME_START_OK session_id={game.session_id} mode={game.mode}")
        print(f"LEVEL {game.current_level}")
        print(f"TIME_REMAINING {game.time_remaining}")

        question = game.current_question
        if question is None:
            print("QUESTION_MISSING")
            return 2

        print(f"QUESTION id={question.id} text={question.text!r}")
        for option in question.options:
            print(f"OPTION id={option.id} text={option.text!r}")

        if args.mode == "speech":
            question_audio = game.fetch_audio_question()
            first_option_audio = game.fetch_audio_option_next()
            print(f"SPEECH_AUDIO_OK question_bytes={len(question_audio)} option_a_bytes={len(first_option_audio)}")

        if args.answer_first_option:
            if not question.options:
                print("ANSWER_SKIPPED no options")
                return 2
            result = game.answer(question.options[0].id)
            print(
                "ANSWER_SUBMITTED "
                f"correct={result.correct} "
                f"timed_out={result.timed_out} "
                f"game_over={result.game_over} "
                f"earned={result.earned_amount}"
            )
        else:
            print("ANSWER_SKIPPED pass --answer-first-option to submit a real answer")

    except AuthenticationError as exc:
        print(f"AUTH_ERROR {exc}")
        return 1
    except MillionaireError as exc:
        print(f"API_ERROR {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
