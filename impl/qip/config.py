"""Environment-driven configuration. Loads .env from repo root if present."""
import os
import pathlib

CANONICAL_MODEL = "text-embedding-3-small"
VECTOR_SIZE = 1536
DISTANCE = "Cosine"

COLLECTIONS = {
    "business": "qip_knowledge",
    "research": "qip_research",
    "session": "qip_memory",
    "agents": "qip_agents",
    "documents": "qip_documents",
}
ALL_COLLECTIONS = list(COLLECTIONS.values())
INDEXED_FIELDS = ["tier", "type", "project", "status"]
TIERS = ["mind_pin", "L1-long", "L2-mid", "L3-active"]


def _load_dotenv():
    here = pathlib.Path(__file__).resolve()
    for base in [pathlib.Path.cwd(), here.parents[1], here.parents[2]]:
        f = base / ".env"
        if f.is_file():
            for line in f.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    os.environ.setdefault(k.strip(), v.strip())
            return


_load_dotenv()


def require(name):
    v = os.environ.get(name, "").strip()
    if not v:
        raise SystemExit(f"[config] missing required env var {name} (see .env.example)")
    return v


QDRANT_URL = require("QIP_QDRANT_URL").rstrip("/")
QDRANT_KEY = require("QIP_QDRANT_API_KEY")
OPENAI_KEY = require("OPENAI_API_KEY")
AGENT_ID = os.environ.get("QIP_AGENT_ID", "fable5")
AGENT_KEY = os.environ.get("QIP_AGENT_KEY", "")
PROJECT = os.environ.get("QIP_PROJECT", "QIP-CORE")
TRUST_THRESHOLD = float(os.environ.get("QIP_TRUST_THRESHOLD", "0.6"))
