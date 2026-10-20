class StreamStatsError(Exception):
    """Base error for app commands"""

class UnsupportedFormatError(StreamStatsError):

    def __init__(self) -> None:
        super().__init__("Unsupported Format")

class InvalidEventError(StreamStatsError):
    pass

class InvalidTimestampError(StreamStatsError):
    pass

class CLIConfigError(StreamStatsError):
    pass
