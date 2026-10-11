# ENG-004: bounded independent verification

Plan and baseline: see frozen PROTOCOL.json and byte-pinned SOURCE_MANIFEST.json in experiments/independent_20261011. Historical outputs and prior independent findings are inherited, not new numerical results.

Actual launch: 2026-10-11T19:47:59.818345+00:00; finished: 2026-10-11T19:48:00.251449+00:00; wall seconds 0.2731642999860924; child exit 0; verdict INDEPENDENT_ARCHIVED_COVERAGE_BIAS_PASS; all criteria True. Exactly one admitted execution, OS CPU affinity1, $0. See attempt-1/launch.json for exact start/command/cwd/environment and execution.json for exit/timeout. Raw stdout and stderr retained, including the Python runtime-location warning.

Finite archived synthetic one-impact cases only. Frozen nominal/J inherited from PR5 independent complex-step reference; not rederived. Population diagonal covariance reused; no empirical covariance revalidation, new samples, controller, joint coverage, safety threshold or deployment evidence. Seed reuse across cases/scales means 36 ensembles are not independent replicates. Boundary ambiguity means INCOMPLETE; no threshold adjustment. Search cannot prove no corrections or universally resolved uncertainty transport.

Independent implementation calculates the requested previously unverified report fields from archived raw data. Final independent review inspects code/artifacts and raw logs; it is not a second numerical replay or external peer review. New evidence is bounded report-field verification and semantic negative-control rejection only.

Original command (now FINISHED and one-attempt guard deliberately refuses replay):

```powershell
python -X utf8 problems/ENG-004/experiments/independent_20261011/run_bounded.py --repo . --round 20261011T193346773525Z-gpt-ENG-004
```

To reproduce, create a fresh isolated branch/round from the same pinned source, perform fresh preflight and public scope/budget registration, freeze the same source hashes, definitions and control list, obtain independent static review and official admission, then invoke the same runner with the NEW round id. Never delete attempt-1 or reset this finished round. No third-party libraries, samples or fitting are needed.
