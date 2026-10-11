# Third-batch independent static/artifact review

Reviewer: `/root/independent_review`, separate Verifier/Skeptic session. Date: 2026-10-11. This review reads files only, apart from this requested report. It does not import author code, execute numerical functions, rerun an existing verifier, or perform an independent experimental replay.

Current status: **STATIC_PROTOCOL_HARNESS_PASS; NUMERICAL_EXECUTION_NOT_RUN; ADMISSION_NOT_CERTIFIED**. Final static review time: 2026-10-11 19:44:53 UTC. The coordinator's hard deadline is 2026-10-11 19:56:51 UTC. This report does not extend it.

## Scope and governance

Read both repositories' AGENTS.md, README.md, VALIDATION.md, STATUS.md, governance locks, protected problem cards, original specifications, relevant author implementations and existing verifier implementations. Both locks pin governance `9c3ae2dbaa1c814f3ef451c041dedfe3b77d926f`; the matching GovernanceV2 AGENTS.md and GATE_CONTRACT.md were inspected. Neither repository currently has `.agents/skills`.

- MED source base: `00a4d7f81b47fd96b2a7e4ce3ca8059676697c97`.
- ENG source base: `548813fd985a9cdc24046982610bfcf74a4cae57`; coordinator identifies original parent `e7821899751f7a5bdaf3700ea5aea5c4de5140a9`.
- New rounds inspected: `20261011T192958557438Z-gpt-MED-001` and `20261011T193346773525Z-gpt-ENG-004`. At this source review they are DRAFT with BLOCKED preflight, no admitted_at and no numerical result. Their topic branches are present in the records.

Governance requires each round to record scope and budget on an issue or PR: “在 issue 或 PR 留領題與預算”. Public claim/readback, fresh bounded searches and original-source reading, frozen acceptance, official pinned admission, exact-byte local freeze, one-CPU sequential execution and the deadline must be evidenced before launch. Neither this report nor a metadata gate is a substitute for those steps. Old FINISHED rounds do not authorize new artifacts. Both broad problem cards remain OPEN; protected specifications must not be changed in this audit.

## MED-001 source findings

The archived source describes completely synthetic Gaussian/Bernoulli rows, not patients, hospitals or a disease. The requested audit is arithmetic on existing prediction columns; it must not claim new clinical external validation, utility, prospective evidence, protected-group fairness, recalibration fitting or DGP reproduction.

The author computes evaluation-only groups with latent `x1 < 0` and `x1 >= 0`. Each seed/site CSV also contains calibration rows; those must be excluded from every subgroup metric. Declared schedules are five seeds (101, 202, 303, 404, 505), three sites (A_reference, B_intercept, C_measurement), 256 calibration and 512 evaluation rows per file. The 15-file/11,520-row schedule is a declared source contract, not a count newly computed by this reviewer.

For each of the 30 seed/site/group cells, freeze exact n and positives, Brier fixed and recalibrated, and the paired row difference `d_i = (y_i - p_recalibrated_i)^2 - (y_i - p_fixed_i)^2`. Negative delta means lower recalibrated Brier. Standard error uses the sample variance of the paired differences with denominator n-1, divided by n; it is not the SE of two independent Brier samples. Normal intervals use critical value `1.959963984540054`. Conditional row intervals ignore uncertainty from the fitted calibration sample and must be described accordingly.

For each of six site/group aggregates, take five seed-level delta means with equal weights, use sample variance with denominator 4, SE divided by sqrt(5), and the frozen two-sided t(4) critical value. Pooling rows or weighting by group size changes this estimand. Record all scheduled keys, reject duplicates/missing keys and nonfinite values, and do not let empty checks pass. Freeze an absolute tolerance of 1e-10 before execution.

The existing `verify_medicine.py` explicitly lists “Conditional row confidence intervals and subgroup summaries” under not_verified. This supports the stated gap in verification, not a scientific discovery. Its historical source/DGP/calibrator checks are inherited evidence, not a new run.

Twelve semantic controls must have independently fixed names, targets, actual changed values and expected rejection. They must exercise semantic comparisons, not merely a checksum guard. In these three scenarios observed_x1 is a positive multiple of x1, so replacing the grouping selector with observed_x1 has the same sign and would be an insensitive negative control. Counts, positives, both Briers, paired mean/SE/normal bounds, seed weighting/SE/t bounds need explicit coverage. Normal/reference acceptance must be required in addition to negative rejection.

## ENG-004 source findings

The original model is a frozen synthetic one-impact ballistic point mass. The requested audit does not rerun trajectories, event localization, Jacobian validation, physical devices, controller safety, or general calibration. Raw records are ordered little-endian `struct <5d`: dh, dv, h(T), v(T), tau. Outputs are columns 2 and 3, not the initial perturbations.

The original coverage code uses the nominal endpoint as center and diagonal population input covariance with variances `(sigma_h * scale)^2` and `(sigma_v * scale)^2`, where sigma_h=0.001 and sigma_v=0.002. Widths are `1.959963984540054 * sqrt((J Sigma J^T)[k][k])`; coverage uses inclusive `abs(output_k - nominal_k) <= width_k`. The empirical/sample covariance used in the old A3 transport check is a separate quantity and cannot replace population Sigma here. Centering at the sample mean would also change the check.

Freeze all four cases, three seeds (7,23,101), three scales (1.0,0.5,0.25), exactly 36 raw files and 4096 records/163,840 bytes per file. Record identity/hash checks and reject duplicates, missing files, unexpected file sizes, malformed records and nonfinite quantities. There are 72 marginal coverage values and 72 bias values. State whether nominal/J are inherited pinned references or independently derived in the new implementation; do not present inherited references as newly reproduced sensitivities.

Freeze bias as `fsum(output_k)/4096 - nominal_k`, or explicitly freeze another algebraically equivalent convention before execution. Compare to the archived bias with absolute tolerance 1e-12. Coverage must match the exact integer count/4096, without approximate tolerance. Do not confuse nominal-center coverage with the covariance discrepancy acceptance A3.

The coverage +1/4096 and bias +1e-6 controls must mutate a predetermined field and be rejected semantically. Declare names, targets, direction and completeness independently of produced cases. A coverage boundary with unresolved numerical uncertainty must be INCOMPLETE; the rounding/ambiguity policy must be fixed before observing output and cannot be widened afterward. Reported marginal 95% coverage is descriptive for archived draws and is not joint 95% coverage, a general safety guarantee or a new empirical experiment.

## Final protocol and harness review

Read the complete updated PROTOCOL.json, verify.py, common.py, admission_guard.py and run_bounded.py in both new experiment directories. No author module, scientific function, verifier or runner was executed by this reviewer. No substantive static freeze blocker remains for these exact bytes. Official admission and scientific execution are separate subsequent actions.

All three requested template fixes were resolved before this signoff:

1. ENG now computes `fsum(raw_output)/4096 - nominal` exactly as agreed.
2. MED and ENG have independently fixed ordered control-name tuples, verify their protocol tables against those tuples, and require rejection values to be the boolean True. MED additionally requires the precise ordered six site/group anchors and six successful checks. Caller domain/count checks prevent empty comparisons or duplicated controls from passing overall.
3. The shared comparator checks both expected and observed numerical values for finiteness and rejects booleans in numerical fields. Exact dictionary key domains and list lengths are checked; exact integer coverage counts have no approximate tolerance.

MED statically implements the 15-file seed/site schedule, exact CSV header, unique row IDs, finite numerical columns, binary outcomes, probability domains, exact calibration/evaluation split counts, 30 evaluation-only latent-x1 groups, paired-difference sample SE/normal bounds and six equal-weight five-seed aggregate SE/t(4) bounds. Full-group weighted count/Brier/delta consistency checks are present. Clean semantic comparison is required along with all 12 named negative rejections. Controls modify the actual candidate report in memory and compare it semantically; rejection is not inferred from a checksum mismatch. The selected control table is bounded and does not claim that every possible fault or every aggregate field has its own mutation.

ENG statically enforces the 36-key Cartesian schedule, raw byte sizes/hashes, 4096 `<5d` records each, finite values, inherited nominal/J references, frozen diagonal population covariance, inclusive nominal-centered marginal coverage, 72 exact count numerators and 72 fsum bias comparisons. Both fixed semantic controls and the inherited nominal anchor must pass. The predeclared 16-ulp ambiguity policy prevents any ambiguous boundary from receiving PASS and emits INCOMPLETE_BOUNDARY_AMBIGUITY. Nominal/J, trajectories and covariance transport are explicitly outside new verification.

Source snapshot integrity was checked by hashing and byte-size inspection only: MED has 26 unique manifest snapshots including 15 raw CSV snapshots; ENG has 47 unique manifest snapshots including 36 raw binaries. Every inspected snapshot SHA256 and byte size matches its manifest. This does not certify any newly calculated scientific statistic. Both repository HEADs match the pinned bases; ENG's stated parent is an ancestor of its base.

The guard statically requires the correct admitted/running round, recorded admission time, allowed preflight outcome, posted/read-back public claim proof, frozen protocol hash, one CPU, USD 0 and the absolute preparation deadline. The runner requires ADMITTED before launch, verifies all declared execution-input hashes within the repository, sets a one-bit OS process affinity, uses a single new attempt-1 directory and preserves raw stdout/stderr. Time remaining is recomputed before child launch and wait. Own-child-tree cleanup uses bounded taskkill/wait/kill/wait steps and preserves cleanup results; result parse failures become exit 2 rather than PASS. These are reviewed code paths, not an observation of a real launch or actual affinity.

Fresh-search/source limitations are explicitly retained in the protocols. Search metadata was read, not independently re-executed by this reviewer. No absence-of-retraction, full clinical-guideline review, clinical utility, broad engineering safety or novel scientific discovery is certified.

Exact reviewed file hashes are recorded in `THIRD_STATIC_SIGNOFF.json`. MED protocol SHA256 is `34527226a6f4a8c39baa1fc6d3bdba75b5e373467397fc854f397cd63c7280b7`; ENG protocol SHA256 is `7cf110e6f80ae6b1c457afac0020e1ca058c7e555802d97d6d05b3d3ce83e7e3`. Any change to a signed protocol or harness after this review requires review of those changed bytes before launch.

Next artifact review must compare each summary stdout to its projection of the full result JSON: the current harness intentionally omits independent/raw_checks/controls from stdout, so literal full-result equality is not the appropriate check. It must inspect actual command, input hashes, admission/freeze/launch order, affinity, timing, exit status, controls, boundary handling and preserved FAIL evidence. Scientific execution and independent experimental replay remain NOT_RUN at this static signoff.
