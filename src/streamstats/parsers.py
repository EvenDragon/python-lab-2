import json
from collections.abc import Iterator

from loguru import logger
from pydantic import ValidationError

from streamstats.errors import InvalidEventError
from streamstats.models import Event


def parse_jsonl(path: str, skip_invalid: bool = False) -> Iterator[Event]:
    """Generator. Parse jsonl file into Event"""
    with open(path,encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            try:
                event = parse_jsonl_line(line)
            except (json.JSONDecodeError, ValidationError) as e:
                if skip_invalid:
                    logger.warning(f"Warning! In file {path} invalid line: {line_number}: {e}")
                    continue
                raise InvalidEventError(f"{path}:{line_number}: invalid event: {e}") from e
            yield event

def parse_jsonl_line(line: str) -> Event:
    """Parse jsonl line into Event"""
    data = json.loads(line)
    event = Event.model_validate(data)
    return event
