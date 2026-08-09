"""LAO — Agent Reliability Plugin.

One-line install → first external verified Trust Event in ~5 minutes.
"""
__version__ = "0.1.0"

from .schema import TrustEvent, TrustEventLedger, make_event  # noqa: F401
from .init import init as init  # noqa: F401
