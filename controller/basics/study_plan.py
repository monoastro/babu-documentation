"""A tiny but useful LangChain application: a study-plan generator."""

import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


def main() -> None:
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Copy .env.example to .env and add your key."
        )

    model = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        temperature=0,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a practical learning coach. Make plans beginner-friendly and concise.",
            ),
            (
                "human",
                "Create a 3-day study plan for learning {topic}. "
                "I have {minutes_per_day} minutes per day. "
                "For each day, give one goal, two concrete tasks, and a quick check for success.",
            ),
        ]
    )

    # The | operator connects LangChain components into a pipeline (a "chain").
    # Input dictionary -> formatted prompt -> model response -> plain text.
    study_plan = prompt | model | StrOutputParser()

    topic = input("What do you want to learn? ").strip() or "LangChain"
    minutes_per_day = input("Minutes available each day? ").strip() or "30"

    print("\nYour study plan:\n")
    print(study_plan.invoke({"topic": topic, "minutes_per_day": minutes_per_day}))


if __name__ == "__main__":
    main()
