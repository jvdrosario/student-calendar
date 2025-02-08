from typing import List, Optional

from langchain_community.callbacks import get_openai_callback

# from kor.extraction import create_extraction_chain
# from kor.nodes import Object, Text, Number

from pandas import DataFrame
from pydantic import BaseModel, Field, field_validator
from kor import extract_from_documents, from_pydantic, create_extraction_chain

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

import os
from langchain_openai import ChatOpenAI
import itertools

import sys
import json

# import FastAPI
import asyncio
import platform

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# setup connection to gpt-4o
os.environ["OPENAI_API_KEY"] = ""

llm = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0
)


# pydantic class of object descriptors
class Event(BaseModel):
    name: str = Field(
        description="The name of the event"
    )
    month: int = Field(
        description="Month in the year when the event is happening."
    )
    day: int = Field(
        description="Day in the month when the event is happening."
    )
    # start_time: Optional[str] = Field(
    #     description="What time is event starting, in hh:mm xm format"
    # )
    # end_time: Optional[str] = Field(
    #     description="What time is event ending, in hh:mm xm format"
    # )

    # must have these three elements to be classified an object
    @field_validator("name")
    def name_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("Name must not be empty")
        return v

    @field_validator("month")
    def month_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("Month must not be empty")
        return v

    @field_validator("day")
    def day_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("Day must not be empty")
        return v


schema, validator = from_pydantic(
    Event,
    description="Extract information about an assignment including the name of the assignment, date, location, and organizer",
    examples=[
        (
            "13- Jan Welcome, Class Logistics and Syllabus",
            {"name": "Welcome, Class Logistics and Syllabus", "month": 1, "day": 13}
        ),
        (
            "Monday Sept 27, 2010 23/9% Exam 1 please",
            {"name": "Exam 1", "month": 9, "day": 27}
        ),
        (
            "21-Sep T Deflection/Compression Members",
            {"name": "Deflection/Compression Members", "month": 9, "day": 21}
        ),
        (
            "Weeks 10 & 11: Race, Violence and the Intimacy of Power—Mexico (Nov. 9, 11, 16, 18) ",
            {"name": "Race, Violence and the Intimacy of Power—Mexico", "month": 11, "day": 9}
        ),
        (
            "Weeks 10 & 11: Race, Violence and the Intimacy of Power—Mexico (Nov. 9, 11, 16, 18) ",
            {"name": "Race, Violence and the Intimacy of Power—Mexico", "month": 11, "day": 11}
        ),
        (
            "Weeks 10 & 11: Race, Violence and the Intimacy of Power—Mexico (Nov. 9, 11, 16, 18) ",
            {"name": "Race, Violence and the Intimacy of Power—Mexico", "month": 11, "day": 16}
        ),
        (
            "Weeks 10 & 11: Race, Violence and the Intimacy of Power—Mexico (Nov. 9, 11, 16, 18) ",
            {"name": "Race, Violence and the Intimacy of Power—Mexico", "month": 11, "day": 18}
        ),
        (
            "#5: Monday, November 8",
            {"name": "#5", "month": 11, "day": 8}
        ),
        (
            "Final exam 25% ** *Two undocumented absences will reduce your grade of participation to ¼, and three to ZERO. **Monday, December 13, 9:00-12:00 noon ",
            {"name": "Final Exam", "month": 11, "day": 13}
            # , "start_time": "9:00 am", "end_time": "12:00 pm"
        )
    ],
    many=True
)

chain = create_extraction_chain(llm,
                                schema,
                                encoder_or_encoder_class="json",
                                validator=validator)


async def extract_data_from_txt(filename):
    if not filename:
        print("Error: Invalid Input")
        return
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            data = f.read()

        document = Document(page_content=data)
        split_documents = RecursiveCharacterTextSplitter().split_documents([document])

        with get_openai_callback() as cb:
            extractions = await extract_from_documents(
                chain, split_documents, max_concurrency=5, use_uid=False, return_exceptions=True
            )

        validated_data = list(
            itertools.chain.from_iterable(
                extraction["validated_data"] for extraction in extractions
            )
        )

        return DataFrame(record.model_dump() for record in validated_data)
    except Exception as e:
        print(f"Exception: {e}")
        return None


async def main():
    n = len(sys.argv)
    if n == 2:
        filename = str(sys.argv[1])
        json_str = await extract_data_from_txt(filename)
        print(json_str)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())  # Run the main async function manually
    except RuntimeError as e:
        print(f"RuntimeError: {e}")
    finally:
        loop.close()
