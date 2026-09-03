"""Command-line entry point for SnackStack."""

import argparse
from typing import Any
from uuid import uuid4

from langgraph.types import Command

from graph import compiled_graph
from logger import get_logger

logger = get_logger(__name__)


class SnackStackAssistant:
    """Manage conversations with the compiled SnackStack graph."""

    def __init__(self, graph: Any) -> None:
        self.graph = graph
        self.reset()

    def reset(self) -> None:
        """Start a fresh checkpointed conversation."""
        self.thread_id = str(uuid4())
        self.config = {"configurable": {"thread_id": self.thread_id}}

    def _get_interrupts(self) -> list[Any]:
        """Return all interrupts pending in the current conversation."""
        snapshot = self.graph.get_state(self.config)
        return [
            pending_interrupt
            for task in snapshot.tasks
            for pending_interrupt in task.interrupts
        ]

    @staticmethod
    def _interrupt_question(pending_interrupt: Any) -> str:
        """Convert an interrupt payload into a user-facing question."""
        value = pending_interrupt.value
        if isinstance(value, dict):
            return str(
                value.get("question", "Please provide the requested information.")
            )
        return str(value)

    def ask(self, question: str) -> str:
        """Invoke the graph and answer any human-in-the-loop interrupts."""
        graph_input = {
            "user_query": question,
            "messages": [],
            "route": [],
            "routing_reason": "",
            "menu_response": "",
            "order_response": "",
            "final_answer": "",
        }
        result = self.graph.invoke(graph_input, config=self.config)
        pending_interrupts = self._get_interrupts()

        while pending_interrupts:
            answers = {}
            for pending_interrupt in pending_interrupts:
                prompt = self._interrupt_question(pending_interrupt)
                answers[pending_interrupt.id] = input(f"{prompt}\n> ").strip()

            resume_value: str | dict[str, str]
            if len(answers) == 1:
                resume_value = next(iter(answers.values()))
            else:
                resume_value = answers

            result = self.graph.invoke(
                Command(resume=resume_value),
                config=self.config,
            )
            pending_interrupts = self._get_interrupts()

        final_answer = result.get("final_answer")
        if not final_answer:
            final_answer = self.graph.get_state(self.config).values.get("final_answer")
        return final_answer or "SnackStack did not produce a response."


def _read_question(use_voice: bool) -> str:
    """Read a typed question or record and transcribe a spoken question."""
    if not use_voice:
        return input("\nYou: ").strip()

    action = input("\nPress Enter to speak, or type reset/quit: ").strip()
    if action:
        return action

    from voice.recorder import record_and_transcribe

    print("Listening for 5 seconds...")
    question = record_and_transcribe()
    print(f"You said: {question}")
    return question


def _present_response(response: str, use_voice_out: bool) -> None:
    """Log and display a response, optionally speaking it aloud."""
    logger.info("Assistant response: %s", response)
    print(f"\nSnackStack: {response}")

    if not use_voice_out:
        return

    try:
        from voice.speaker import speak

        speak(response)
    except Exception:
        logger.exception("Voice output failed")
        print("Voice output failed; the text response is shown above.")


def run_text_loop(
    assistant: SnackStackAssistant,
    *,
    use_voice: bool = False,
    use_voice_out: bool = False,
) -> None:
    """Run the interactive SnackStack command loop."""
    print("SnackStack is ready.")
    print("Commands: reset, quit")
    if use_voice_out:
        print("Voice output is AI-generated.")

    while True:
        try:
            question = _read_question(use_voice)
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        except Exception:
            logger.exception("Voice input failed")
            print("Voice input failed. Check your microphone and audio settings.")
            continue

        if not question:
            continue

        command = question.casefold()
        if command in {"quit", "exit", "/quit"}:
            print("Goodbye!")
            break
        if command in {"reset", "/reset"}:
            assistant.reset()
            logger.info("Conversation reset")
            print("Conversation reset.")
            continue

        try:
            response = assistant.ask(question)
        except Exception:
            logger.exception("SnackStack request failed")
            print("SnackStack encountered an error.")
            continue

        _present_response(response, use_voice_out)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="SnackStack ordering assistant")
    parser.add_argument(
        "--ask",
        metavar="QUESTION",
        help="Ask one question and exit",
    )
    parser.add_argument(
        "--voice",
        action="store_true",
        help="Record spoken questions in the interactive loop",
    )
    parser.add_argument(
        "--voice-out",
        action="store_true",
        help="Speak assistant responses using AI-generated audio",
    )
    return parser.parse_args()


def main() -> None:
    """Run the SnackStack CLI."""
    args = parse_args()
    assistant = SnackStackAssistant(compiled_graph)

    if args.ask:
        response = assistant.ask(args.ask)
        if args.voice_out:
            print("Voice output is AI-generated.")
        _present_response(response, args.voice_out)
        return

    run_text_loop(
        assistant,
        use_voice=args.voice,
        use_voice_out=args.voice_out,
    )


if __name__ == "__main__":
    main()
