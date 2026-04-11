# PR Verification Notes (commit 1860a8b)

Date: 2026-04-11
Reviewer: Codex

## Scope reviewed
- `custom_components/ztm_warsaw/client.py`
- `custom_components/ztm_warsaw/coordinator.py`
- `custom_components/ztm_warsaw/sensor.py`
- `custom_components/ztm_warsaw/manifest.json`

## What was validated
1. Network/API failure path now returns `None` from the client instead of an empty object.
2. Coordinator fallback logic keeps last cached timetable when a refresh fails.
3. Sensor now explicitly pushes HA state in no-data / no-departure branches.
4. Manifest version bump from `1.1.3` to `1.1.4` is consistent with the behavior change.

## Checks run
- `python -m compileall custom_components/ztm_warsaw`

## Result
- No blocking regression found in the reviewed change set.
- The PR behavior is coherent: it prioritizes stale-but-valid cached data over transient API outages, which should reduce entity flapping during short failures.

## Follow-up recommendation (non-blocking)
- Consider adding lightweight async unit tests for:
  - `client.get()` returning `None` on HTTP/non-JSON/network errors.
  - `coordinator._async_update_data()` returning cached data when `client.get()` fails.
  - sensor state updates on branches with no timetable/no future departures.
