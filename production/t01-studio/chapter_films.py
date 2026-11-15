"""The next group of films in the Summit One teaching sequence."""

CHAPTER_FILMS = (
    "T02.3", "T02.E",
    "T03.1", "T03.2", "T03.3", "T03.E",
    "T04.1", "T04.2", "T04.3", "T04.E",
)

COURSE_FILMS = tuple(f"T{chapter:02}.{kind}" for chapter in range(5, 19) for kind in ("1", "2", "3", "E"))
