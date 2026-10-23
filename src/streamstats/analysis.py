from collections import Counter
from collections.abc import Iterable
from datetime import datetime

from streamstats.models import Event


def analyze_events(events: Iterable[Event]) -> dict[str, object]:
    """Count the number of events in file by level, Find first and last event,
    Find most popular sources that return ERROR/CRITICAL level"""
    counter: Counter[str] = Counter()
    counter_by_source: Counter[str] = Counter()
    error_counter: Counter[str] = Counter()
    critical_counter: Counter[str] = Counter()
    first_event: datetime | None = None
    last_event: datetime | None = None
    for event in events:
        counter[event.level] += 1
        counter_by_source[event.source] += 1
        if event.level == "ERROR":
            error_counter[event.source] += 1
        elif event.level == "CRITICAL":
            critical_counter[event.source] += 1
        if first_event is None or event.timestamp< first_event:
            first_event = event.timestamp
        if last_event is None or event.timestamp> last_event:
            last_event = event.timestamp
    return{
        "total": counter.total(),
        "by_level": dict(counter),
        "by_source": dict(counter_by_source),
        "first_event": first_event.isoformat() if first_event is not None else None,
        "last_event": last_event.isoformat() if last_event is not None else None,
        "top_error_sources": error_counter.most_common(5),
        "top_critical_sources": critical_counter.most_common(5)
    }
