import datetime

from pydantic import BaseModel, field_validator

from streamstats.constants import LEVELS


class Event(BaseModel):
    timestamp: datetime.datetime
    level: LEVELS
    source: str
    message: str
    @field_validator("source")
    @classmethod
    def validate_source(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Source must not be empty")
        return value

class SkippedEvent(BaseModel):
    skipped: int = 0
