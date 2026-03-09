# Sprint 05 - Fingerprinting and Clustering

## Objective
Implement multi-signal fingerprinting and certificate serial correlation for infrastructure identity tracking.

## Source Code
- `src/nyxera_eye/fingerprinting/murmurhash3.py`
- `src/nyxera_eye/fingerprinting/ja3.py`
- `src/nyxera_eye/fingerprinting/jarm.py`
- `src/nyxera_eye/clustering/certificate_correlation.py`

## Logic
- Favicon fingerprinting uses MurmurHash3 x86 32-bit implementation.
- JA3 pipeline:
  - build JA3 string from TLS handshake vectors
  - compute MD5 digest as JA3 hash
- JARM uses canonicalized probe-result concatenation and SHA-256 hash.
- Certificate correlation groups unique IPs under certificate serial values.

## Architecture Impact
- Fingerprinting modules are pure functions, easy to compose in pipeline or analytics jobs.
- Clustering output supports tracking infrastructure movement beyond static IP identity.

## Validation Notes
- `tests/test_fingerprinting.py` covers deterministic hash vectors and cluster grouping.

## Risks and Follow-ups
- No collision confidence analysis/reporting yet.

## Mermaid Diagram

```mermaid
flowchart LR
  A[Inputs] --> B[Core Module Logic]
  B --> C[Normalized Output]
  C --> D[Validation Tests]
```
