#!/usr/bin/env python
import asyncio
from typing import List

from crewai.flow.flow import Flow, listen, start
from icecream import ic
from pydantic import BaseModel

from .crews.outline_book_crew.outline_crew import OutlineCrew
from .crews.write_book_chapter_crew.write_book_chapter_crew import WriteBookChapterCrew
from .types import Chapter, ChapterOutline


class BookState(BaseModel):
    title: str = "The Current State of AI in September 2024 - Trends Across Industries"
    book: List[Chapter] = []
    book_outline: List[ChapterOutline] = []
    topic: str = (
        "Exploring the latest trends in AI across different industries as of September 2024"
    )
    goal: str = """
        The goal of this chapter is to provide a comprehensive overview of the current state of artificial intelligence in September 2024.
        It will delve into the latest trends impacting various industries, analyze significant advancements,
        and discuss potential future developments. The chapter aims to inform readers about cutting-edge AI technologies
        and prepare them for upcoming innovations in the field.
        
    """


#   goal: str = """
#         The goal of this book is to provide a comprehensive overview of the current state of artificial intelligence in September 2024.
#         It will delve into the latest trends impacting various industries, analyze significant advancements,
#         and discuss potential future developments. The book aims to inform readers about cutting-edge AI technologies
#         and prepare them for upcoming innovations in the field.
#         create only 2 chapters of the book.
#     """


class BookFlow(Flow[BookState]):

    @start()
    def generate_book_outline(self):
        ic("Kickoff the Book Outline Crew")
        output = (
            OutlineCrew()
            .crew()
            .kickoff(inputs={"topic": self.state.topic, "goal": self.state.goal})
        )

        chapters = output["chapters"]
        ic("Chapters:", chapters)

        self.state.book_outline = chapters

    @listen(generate_book_outline)
    async def write_chapters(self):
        ic("Writing Book Chapters")
        tasks = []

        async def write_single_chapter(chapter_outline):
            output = (
                WriteBookChapterCrew()
                .crew()
                .kickoff(
                    inputs={
                        "goal": self.state.goal,
                        "topic": self.state.topic,
                        "chapter_title": chapter_outline.title,
                        "chapter_description": chapter_outline.description,
                        "book_outline": [
                            chapter_outline.model_dump_json()
                            for chapter_outline in self.state.book_outline
                        ],
                    }
                )
            )
            title = output["title"]
            content = output["content"]
            chapter = Chapter(title=title, content=content)
            return chapter

        for chapter_outline in self.state.book_outline:
            ic(f"Writing Chapter: {chapter_outline.title}")
            ic(f"Description: {chapter_outline.description}")
            # Schedule each chapter writing task
            task = asyncio.create_task(write_single_chapter(chapter_outline))
            tasks.append(task)

        # Await all chapter writing tasks concurrently
        chapters = await asyncio.gather(*tasks)
        ic("Newly generated chapters:", chapters)
        self.state.book.extend(chapters)

        ic("Book Chapters", self.state.book)

    @listen(write_chapters)
    async def join_and_save_chapter(self):
        ic("Joining and Saving Book Chapters")
        # Combine all chapters into a single markdown string
        book_content = ""

        for chapter in self.state.book:
            # Add the chapter title as an H1 heading
            book_content += f"# {chapter.title}\n\n"
            # Add the chapter content
            book_content += f"{chapter.content}\n\n"

        # The title of the book from self.state.title
        book_title = self.state.title

        # Create the filename by replacing spaces with underscores and adding .md extension
        filename = f"./{book_title.replace(' ', '_')}.md"

        # Save the combined content into the file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(book_content)

        ic(f"Book saved as {filename}")


def kickoff():
    book_flow = BookFlow()
    book_flow.kickoff()


def plot():
    book_flow = BookFlow()
    book_flow.plot()


if __name__ == "__main__":
    kickoff()
