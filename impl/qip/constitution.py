"""Constitutional Layer runtime checks (spec/13). Invariants I1-I7."""
import re

# I3: secret hygiene. Applied to every capture before embedding.
_SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),                      # OpenAI-style keys
    re.compile(r"eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{5,}"),  # JWTs
    re.compile(r"(?i)bearer\s+[A-Za-z0-9_\-.]{16,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[=:]\s*\S{8,}"),
    re.compile(r"gh[pos]_[A-Za-z0-9]{20,}"),                    # GitHub tokens
]

# I4: external-action gate. Conservative keyword screen; the reasoning agent
# confirms, this screen only refuses to stay silent.
_EXTERNAL_MARKERS = [
    "send email", "send mail", "email to", "post to", "publish", "tweet",
    "send message", "slack ", "whatsapp", "deploy", "purchase", "buy ",
    "transfer", "wire ", "dm ", "reply to client", "send to client",
]

# I6: non-destruction screen.
_DESTRUCTIVE = [re.compile(r"\brm\s+-rf?\b"), re.compile(r"\bDROP\s+(TABLE|COLLECTION|DATABASE)\b", re.I),
                re.compile(r"\bdelete\s+collection\b", re.I), re.compile(r"force[- ]?push", re.I)]


def redact(text):
    """I3: strip credentials from any text bound for memory."""
    out = text
    for pat in _SECRET_PATTERNS:
        out = pat.sub("[REDACTED]", out)
    return out


def screen_task(text):
    """Pre-execution screen. Returns list of (invariant, flag) tuples; empty = clear."""
    flags = []
    low = text.lower()
    for marker in _EXTERNAL_MARKERS:
        if marker in low:
            flags.append(("I4", f"external action marker '{marker.strip()}': requires principal approval"))
            break
    for pat in _DESTRUCTIVE:
        if pat.search(text):
            flags.append(("I6", "destructive operation pattern: supersede, do not destroy; ask first"))
            break
    if redact(text) != text:
        flags.append(("I3", "task text contains credential-like material; redact at capture"))
    return flags


def assert_write_ok(payload):
    """I2 support: refuse captures whose full_text still contains secrets."""
    if redact(payload.get("full_text", "")) != payload.get("full_text", ""):
        raise SystemExit("[constitution] I3 violation: unredacted secret in full_text; write refused")
