from pydantic import BaseModel, field_validator


class Question(BaseModel):
    question: str
    options: list[str]
    answer_index: int
    section: int = 1

    @field_validator("options")
    @classmethod
    def four_options(cls, v):
        if len(v) != 4:
            raise ValueError("each question needs exactly 4 options")
        return v

    @field_validator("answer_index")
    @classmethod
    def in_range(cls, v):
        if not 0 <= v <= 3:
            raise ValueError("answer_index must be 0-3")
        return v


class Quiz(BaseModel):
    questions: list[Question]
