These are the exact response texts from mutation calls 4 and 5 of the local
`paid-smoke-3-20260831-02` run (both reported `finish_reason: stop`). Only the
response text is retained; no request, credentials, or machine paths are included.

- `attempt_1.txt`: SEARCH markers missing; code fences close before separators
  and replacement payloads.
- `attempt_2.txt`: SEARCH and REPLACE markers missing.

These are intentionally invalid parser fixtures, not runnable or approved BPR
implementations. Tests use a separate, trivial valid edit to verify correction.
