"""Validation models for JSON data."""
from __future__ import annotations

from pydantic import BaseModel


class GoeStatus(BaseModel):
    """Validate JSON response of /status endpoint of go-e API."""

    car: int
    nrg: list[int]
