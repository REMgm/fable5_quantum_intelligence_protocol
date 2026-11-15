"""Stdlib regression tests for Qdrant setup and vector-integrity auditing."""
import contextlib
import io
import math
import os
import unittest
from unittest.mock import patch

os.environ.setdefault("QIP_QDRANT_URL", "https://example.invalid")
os.environ.setdefault("QIP_QDRANT_API_KEY", "test-only")
os.environ.setdefault("OPENAI_API_KEY", "test-only")

from qip import config, store


def point(vector=None, **payload_overrides):
    payload = {
        "embedding_model": config.CANONICAL_MODEL,
        "embedding_status": "embedded",
        "full_text": "durable knowledge",
    }
    payload.update(payload_overrides)
    result = {"id": "point-1", "payload": payload}
    if vector is not None:
        result["vector"] = vector
    return result


def valid_vector():
    return [1.0 / math.sqrt(config.VECTOR_SIZE)] * config.VECTOR_SIZE


class AuditTests(unittest.TestCase):
    def run_audit(self, points):
        with patch.object(store, "scroll", return_value=points) as scroll:
            with contextlib.redirect_stdout(io.StringIO()):
                result = store.audit()
        self.assertTrue(scroll.call_args.kwargs["with_vector"])
        return result

    def test_valid_vector_passes(self):
        self.assertTrue(self.run_audit([point(valid_vector())]))

    def test_missing_vector_fails(self):
        self.assertFalse(self.run_audit([point()]))

    def test_wrong_dimension_fails(self):
        self.assertFalse(self.run_audit([point([0.1] * 10)]))

    def test_zero_vector_fails(self):
        self.assertFalse(self.run_audit([point([0.0] * config.VECTOR_SIZE)]))

    def test_non_finite_vector_fails(self):
        vector = valid_vector()
        vector[0] = float("nan")
        self.assertFalse(self.run_audit([point(vector)]))

    def test_boolean_vector_fails(self):
        self.assertFalse(self.run_audit([point([True] * config.VECTOR_SIZE)]))


class SetupTests(unittest.TestCase):
    def test_unrelated_http_400_is_not_hidden(self):
        def request(method, path, body=None):
            if method == "GET":
                return {"result": {"collections": [
                    {"name": name} for name in config.ALL_COLLECTIONS
                ]}}
            raise RuntimeError("HTTP 400: invalid field schema")

        with patch.object(store, "qdrant", side_effect=request):
            with self.assertRaisesRegex(RuntimeError, "invalid field schema"):
                store.ensure_setup()

    def test_existing_index_is_idempotent(self):
        def request(method, path, body=None):
            if method == "GET":
                return {"result": {"collections": [
                    {"name": name} for name in config.ALL_COLLECTIONS
                ]}}
            raise RuntimeError("HTTP 400: index already exists")

        with patch.object(store, "qdrant", side_effect=request):
            with contextlib.redirect_stdout(io.StringIO()):
                store.ensure_setup()


if __name__ == "__main__":
    unittest.main()
