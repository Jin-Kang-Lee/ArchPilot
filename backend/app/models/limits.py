"""Contract character limits.

The values mirror ``03-DATA-CONTRACTS.md`` §3.1. They are plain constants, not
configuration: they are part of the accepted API contract, not a deployment
setting. ``ANSWER_MAX_LENGTH`` is defined here with its siblings so the
question-answer contract (M1-T04) can reuse one source of truth.
"""

from __future__ import annotations

TITLE_MAX_LENGTH = 120
BRIEF_MAX_LENGTH = 20_000
ANSWER_MAX_LENGTH = 4_000
