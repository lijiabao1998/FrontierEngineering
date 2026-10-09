# ENG-004 single-impact synthetic replication

## Result and boundaries

This round reproduces a known first-order saltation uncertainty-transport effect for four frozen, fully synthetic, single-impact conditions. It does not solve ENG-004, establish new science, calibrate a physical model, validate a controller, or demonstrate deployment safety. The problem card remains unchanged and OPEN.

Author metrics: 36 ensembles / 147,456 trajectories; maximum relative covariance error 6.826661001994398e-5; smallest reset-only-to-saltation error ratio 14,645.248. Maximum event time error was 8.88e-16 seconds; endpoint error 8.88e-15; direct-Jacobian discrepancy 4.44e-16. These numbers concern a simple exact ballistic model and small perturbations, not general hybrid systems.

An independent coordinator separately differentiated the explicit endpoint by complex step, checked determinant e², re-summed all 36 archived ensembles, and checked all 16 event outputs without importing the author implementation. Its report is `independent-review.json`; its code is deliberately excluded from this model/experiment PR because the repository requires evaluator changes in a separate PR. This is independent implementation within the same assistant/model family, not a second physical experiment or external peer review. See the report's scope and limitations.

## Frozen model and acceptance

`frozen-spec.json` SHA-256: e1501059792e2f054e1e248b263409eb80b1a2f03d89d23f95ef887586bb5420.

`admission-snapshot.json` preserves the ADMITTED record before experiments. The governance CLI at 9c3ae2dbaa1c814f3ef451c041dedfe3b77d926f admitted the local round before model code was run. Issue #3 claims scope and USD 0 / 30 minutes. Freeze/admission were local first, not a public preregistration before measurements.

Ballistic flow is dh/dt=v and dv/dt=-g. At downward contact h=b, v becomes -e*v. The experiment ends after exactly one isolated transverse impact. Four cases: nominal, elastic restitution, translated horizontal guard, and a separately specified low-gravity/restitution OOD case. Translation is a coordinate consistency check, not a distinct contact geometry. No simultaneous events, grazing, sticking, friction, uncertain guard/reset parameters, controller, process noise, sensor model, model-form uncertainty or real data are tested.

All 147,456 realized draws satisfy the single-event domain. Gaussian tails are mathematically unbounded; this finite sample does not establish same-mode validity for the entire nominal Gaussian distribution. Unsupported states and second-impact horizons are rejected.

Covariance error compares the centered output sample covariance with J times the *realized input sample covariance* times J-transpose. This reduces input sampling noise and tests local transport. It is not a population calibration or probabilistic coverage theorem. Reported marginal 95% coverages and means are descriptive only. Small-noise and post-event observation conditions avoid the mode-mixture issue around the event itself.

## Controls and failures

- Positive pre-impact covariance discrepancy: 4.235e-22.
- Reset-only wrong Jacobian discrepancy: 1.68 to 4.42; wrong timing sign: 3.36 to 8.85. Both fail the frozen 1e-3 negative-control threshold by a wide margin.
- Delayed-grid event errors: 0.0084 to 0.0789 seconds, with a recorded guard penetration of 0.226112 in synthetic length units. These are deliberately broken controls; no physical system was involved.
- Tampering the first output particle count from 4096 to 4095 changes the digest and is rejected. Integrity hashes do not establish truth or trusted signing.
- Invalid height, second-impact horizon and zero restitution are rejected as outside this solver's domain.
- No experiment crash, timeout, tuning, discarded draw or threshold revision occurred. All failures/controls remain in their raw records.
- Infrastructure: an initial unauthenticated `git ls-remote` attempt ended with environment review cancellation. A connector-based reconstruction then reproduced exact base commit 79594b5615bd097f8af9aea956308032d748dc37 and tree 830002fe117676ba902e983f8e19f67b3401c630. No credentials were read or sent. Existing Claude governance branches were already merged; no repair was duplicated.

## Reproduction

Python 3.12.14, standard library only; no packages, paid APIs, GPU, real devices or external calls in the experiment. One author run took approximately 0.92 seconds on Linux x86_64. There were 76 frozen configuration/control evaluations, below the 100-configuration cap. No parameter search was performed.

From the repository root:

```sh
python3 problems/ENG-004/experiments/saltation_baseline.py \
  --spec runs/20261009T102807929160Z-gpt-ENG-004/frozen-spec.json \
  --output /tmp/eng004-reproduce \
  --dump-raw /tmp/eng004-reproduce/raw
```

Compare regenerated JSON/CSV files and raw binary arrays to committed results. Runtime/platform summary may vary; deterministic result files and array hashes should agree on the documented Python runtime. The code's spec hash check refuses modified acceptance/configuration. The generator does not issue a scientific verdict. Do not regenerate into the committed result directory if preserving its full audit manifest.

Each `raw/<case>-<seed>-<scale>.bin` has 4096 records of five IEEE754 little-endian float64 values: delta_h, delta_v, h(T), v(T), event_time. Record size is 40 bytes, file size 163840 bytes. Initial h and v equal the frozen case nominal plus these deltas. The JSON ensemble record stores the SHA-256 over exactly those bytes. All 36 full raw arrays are committed. Two complete readable CSVs cover nominal seed7 scale1 and OOD seed101 scale0.25; `trace-samples.csv` contains the first12 rows from every configuration. Inputs are original synthetic data; no third-party dataset/code/figure is copied.

Pinned governance metadata checks:

```sh
python3 /path/to/FrontierLab-Governance/tools/frontier.py validate .
python3 /path/to/FrontierLab-Governance/tools/frontier.py check-diff . 79594b5615bd097f8af9aea956308032d748dc37 HEAD
```

The governance repository must be checked out at 9c3ae2dbaa1c814f3ef451c041dedfe3b77d926f. These validate records and allowed paths, not scientific truth.

## Search scope

Six fresh queries across all four required categories are preserved in `round.json`. Two distinct primary full texts were read in relevant sections:

- Kong et al., arXiv 2306.06862v2 (2024-06-20), https://arxiv.org/html/2306.06862v2: first-order saltation/covariance relation, event-time correction, and limitations concerning split distributions and simultaneous transitions. The small single-event replication is known territory.
- Mosekari, Scientific Reports 16, 27161 (2026), https://www.nature.com/articles/s41598-026-53809-5: event-aware hybrid sensitivity/covariance under regular transverse, isolated-event conditions. Its data statement expressly limits evidence to archived simulation/FE work, with some legacy figures not fully reproducible; no new laboratory data. Supplementary arrays were not reviewed.

No explicit correction/retraction was found in the bounded searches; this is not a comprehensive retraction audit or a proof that none exists. No broad novelty or external-resolution claim follows. Sources are paraphrased, not reproduced.

## Independent verifier specification

Read the frozen spec before author source. Re-derive the endpoint from the ballistic quadratic and impact reset. Differentiate with complex step or a symbolic/direct independent method; check det(J)=e². Independently sum means and centered covariances from all archived records, verify exact final states/event times and all declared SHA-256 values, and compare the frozen numerical thresholds. Verify that wrong reset/timing and deliberately delayed localization fail. Mutate one recorded value and confirm hash detection. Check parent card, evaluator, governance pin and workflow are unchanged. Do not infer universal coverage, new mechanism, stable feedback or field safety from these checks.

Next minimal work, requiring a new admitted round: a genuinely different contact geometry or a near-event split-distribution stress test with its own acceptance. No further experimental round is started here. Await owner review; no merge or deployment.
