import csv
import json
from collections.abc import Iterator

from loguru import logger
from pydantic import ValidationError

from streamstats.errors import (
    InvalidEventError,
    InvalidTimestampError,
    UnsupportedFormatError,
)
from streamstats.models import Event, SkippedEvent


def parse_files(files: list[str],format: str, skipped: SkippedEvent, skip_invalid: bool = False) -> Iterator[Event]:
    """Parse files into one iterator"""
    if format == "jsonl":
        parser = parse_jsonl
    elif format == "csv":
        parser = parse_csv
    else:
        raise UnsupportedFormatError
    for path in files:
        yield from parser(path, skipped, skip_invalid)

def parse_jsonl(path: str, skipped: SkippedEvent, skip_invalid: bool = False) -> Iterator[Event]:
    """Generator. Parse jsonl file into Event"""
    with open(path,encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            try:
                event = parse_jsonl_line(line)

            except json.JSONDecodeError as e:
                if skip_invalid:
                    skipped.skipped += 1
                    logger.warning(f"Warning! In file {path} invalid line: {line_number}: {e}")
                    continue
                raise InvalidEventError(f"{path}:{line_number}: invalid event: {e}") from e

            except ValidationError as e:
                if skip_invalid:
                    skipped.skipped += 1
                    logger.warning(f"Warning! In file {path} invalid line: {line_number}: {e}")
                    continue
                for error in e.errors():
                    if error["loc"][:1] == ("timestamp",):
                        raise InvalidTimestampError(f"{path}:{line_number}: invalid event: {e}") from e
                raise InvalidEventError(f"{path}:{line_number}: invalid event: {e}") from e

            yield event

def parse_jsonl_line(line: str) -> Event:
    """Parse jsonl line into Event"""
    data = json.loads(line)
    event = Event.model_validate(data)
    return event

def parse_csv(path: str, skipped: SkippedEvent, skip_invalid: bool = False) -> Iterator[Event]:
    """Generator. Parse csv file into Event"""
    with open(path, encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for line in reader:
            line_number = reader.line_num
            try:
                event = Event.model_validate(line)

            except ValidationError as e:
                if skip_invalid:
                    skipped.skipped += 1
                    logger.warning(f"Warning! In file {path} invalid line: {line_number}: {e}")
                    continue
                for error in e.errors():
                    if error["loc"][:1] == ("timestamp",):
                        raise InvalidTimestampError(f"{path}:{line_number}: invalid event: {e}") from e
                raise InvalidEventError(f"{path}:{line_number}: invalid event: {e}") from e

            yield event
