"""Request-scoped context variables propagated across async/thread boundaries."""

from contextvars import ContextVar

session_id: ContextVar[str] = ContextVar("session_id", default="--------")
