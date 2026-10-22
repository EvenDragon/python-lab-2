from collections import Counter
from collections.abc import Iterable

from streamstats.models import Event


def count_events(events: Iterable[Event]) -> Counter:
    """Count the number of events in file by level"""
    counter: Counter[str] = Counter()
    for event in events:
        counter[event.level] += 1
    return counter
