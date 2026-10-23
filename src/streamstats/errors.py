class StreamStatsError(Exception):
    """Base error for app commands"""

class UnsupportedFormatError(StreamStatsError):

    def __init__(self) -> None:
        super().__init__("Unsupported Format")

class InvalidEventError(StreamStatsError):
    """Invalid Event"""

class InvalidTimestampError(StreamStatsError):
    """Invalid Timestamp"""

class CLIConfigError(StreamStatsError):
    """CLI Config Error"""
