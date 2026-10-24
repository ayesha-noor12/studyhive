from pypdf import PdfReader


class NoTextError(Exception):
    pass


def split_text(text, words_per_section=700, min_words=30):
    """Split plain text into sections of roughly words_per_section words."""
    words = text.split()
    if len(words) < min_words:
        raise NoTextError(
            f"Not enough text ({len(words)} words). Please provide at least {min_words} words."
        )
    return [
        " ".join(words[i : i + words_per_section])
        for i in range(0, len(words), words_per_section)
    ]


def extract_sections(file, words_per_section=700, max_pages=20):
    """Read a PDF and split its text into sections."""
    reader = PdfReader(file)
    text = " ".join((page.extract_text() or "") for page in reader.pages[:max_pages])
    try:
        return split_text(text, words_per_section)
    except NoTextError:
        raise NoTextError(
            "No readable text found. This looks like a scanned PDF; "
            "try pasting the text instead."
        ) from None
