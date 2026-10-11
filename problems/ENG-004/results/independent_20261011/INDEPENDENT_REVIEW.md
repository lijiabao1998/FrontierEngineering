# Third-batch independent artifact review

Reviewer: `/root/independent_review`, separate Verifier/Skeptic session, 2026-10-11. Verdict: **ARTIFACT_REVIEW_PASS** for the bounded MED-001 and ENG-004 results below. No substantive scientific-artifact blocker was found. This is static and artifact review of the coordinator's single execution per problem, not a second experiment, independent experimental replay, external peer review or broad problem-completion certification.

The reviewer read archived JSON, manifests, commands, source code, raw stdout/stderr and mutation files, and performed hashes, Git-blob byte comparisons and structural JSON identity checks. The reviewer did not import author code, execute scientific functions, recalculate CSV Brier/SE/CI or raw-binary coverage/bias, or rerun any verifier. Only this requested review report was written during the artifact-review stage.

## Admission, frozen bytes and execution

| Item | MED-001 | ENG-004 |
| --- | --- | --- |
| Source base | `00a4d7f81b47fd96b2a7e4ce3ca8059676697c97` | `548813fd985a9cdc24046982610bfcf74a4cae57` |
| Round | `20261011T192958557438Z-gpt-MED-001` | `20261011T193346773525Z-gpt-ENG-004` |
| Recorded admission, UTC | 19:47:08.553459 | 19:47:10.696587 |
| Local protocol commit | `17575b1754d2918d32de32a99fa260babdf7519d` | `58b553e6ea243ec4e80181b8b72ec0dc103ac94d` |
| Execution inputs checked against local bytes and committed Git blobs | 38/38 match | 59/59 match |
| Pinned source snapshots checked against manifest and original base Git blobs | 26/26 match | 47/47 match |
| Launch, UTC | 19:47:53.047469 | 19:47:59.818345 |
| Finish, UTC | 19:47:53.439005 | 19:48:00.251449 |
| Recorded child wall seconds | 0.2341776999819558 | 0.2731642999860924 |
| Child exit / timeout | 0 / false | 0 / false |
| Launch affinity mask / CPU count / USD / replay | 1 / 1 / 0 / false | 1 / 1 / 0 / false |

Timestamps in original launch/execution records use +08:00; the table converts them to UTC. Both admissions precede the protocol-commit command (19:47:12.717201 to 19:47:16.597793 UTC, exit 0), and the protocol commit precedes both launches. MED completed before ENG started. Both completed before the unchanged preparation deadline 2026-10-11 19:56:51 UTC. Exactly one attempt-1 directory per problem was reviewed; no replay or timeout cleanup is recorded. Affinity is evidenced by the launch records together with the previously reviewed OS one-bit affinity/inheritance code, not by a separate live inspection of a terminated process.

Each launch command invokes the named Python 3.13.5 executable with `-X utf8`, the signed problem-local `verify.py`, exact `--repo` and `--round`, and `--output .../attempt-1/result.json`. Actual result files are at the attempt root, not a data subdirectory. The signed protocol, verifier, comparator, guard and runner match the static signoff. Public-claim/readback files are included among the exact frozen execution inputs; recorded claim status is POSTED_AND_READ_BACK. Admission command records invoke the pinned GovernanceV2 `frontier.py admit` and have exit 0. The reviewer did not perform an external comment write or fresh external readback.

A comparison of tracked changes to each source base found no path outside the new problem experiment/result directories and its new round directory. Pinned historical source/result files remain byte-identical to the base for all manifest entries. Original problem cards and protected specifications are not changed by this audit.

## MED-001 result and controls

The full result, execution verdict and stdout summary agree on `INDEPENDENT_SYNTHETIC_SUBGROUP_ARITHMETIC_PASS`, all_criteria_passed=true and child exit 0. The result reports 15 files, 11,520 archived synthetic rows, 30 evaluation subgroup cells and six site/group aggregates. All 15 raw-check SHA256 values equal the manifest entries; each raw check records 256 calibration and 512 evaluation rows and group_sum_consistent=true. These are observed artifact assertions from the single execution, not row statistics independently recalculated by this reviewer.

Clean comparison accepted with no errors; the reported maximum numerical gap is `5.551115123125783e-17`, below the frozen absolute tolerance `1e-10`. All six anchor checks are boolean true. Aggregate records have five seed-level observations per site/group; their reported means are A_reference 0.0010907555326155878 / 0.001831261758043151, B_intercept -0.07727165476976869 / -0.058930879035575014, C_measurement -0.008966369104907083 / -0.016871837028834324, ordered x1-negative / x1-nonnegative. These agree with the bounded inherited anchors as checked in the execution; they are not new clinical effects.

The protocol and result contain the same fixed ordered 12 controls, and exactly 12 named mutation files are present. For every mutation, the saved JSON was structurally compared with the archived author-report projection after applying only its predeclared operation. Every saved mutation exactly matches that expected candidate, every semantic_rejected is boolean true, every validation.accepted is boolean false and every control has a concrete error. This structural mutation identity check does not re-execute the scientific verifier.

| Control | Observed semantic rejection |
| --- | --- |
| N_PLUS_ONE | n 268 to 269, integer mismatch |
| POSITIVES_PLUS_ONE | positives 56 to 57, integer mismatch |
| FIXED_BRIER_PLUS_1E4 | fixed Brier +0.0001, numeric mismatch |
| RECALIBRATED_BRIER_PLUS_1E4 | recalibrated Brier +0.0001, numeric mismatch |
| DELTA_MEAN_PLUS_1E4 | paired mean +0.0001, numeric mismatch |
| DELTA_SE_PLUS_1E4 | paired SE +0.0001, numeric mismatch |
| DELTA_CI_LOWER_MINUS_1E4 | paired lower bound -0.0001, numeric mismatch |
| DELTA_CI_UPPER_PLUS_1E4 | paired upper bound +0.0001, numeric mismatch |
| AGGREGATE_MEAN_PLUS_1E4 | aggregate mean +0.0001, numeric mismatch |
| AGGREGATE_SE_PLUS_1E4 | aggregate SE +0.0001, numeric mismatch |
| DELETE_SUBGROUP | missing subgroup, key/domain mismatch |
| NAN_DELTA_MEAN | NaN paired mean, nonfinite/not-numeric rejection |

The NaN negative candidate intentionally contains a Python JSON NaN token; it is a preserved invalid numerical candidate, not a normal successful result. The clean result/stdout contain finite numerical values. No claim of exhaustive fault coverage follows from these 12 selected controls.

## ENG-004 result and controls

The full result, execution verdict and stdout summary agree on `INDEPENDENT_ARCHIVED_COVERAGE_BIAS_PASS`, all_criteria_passed=true and child exit 0. The result has 36 ensemble keys and 36 raw checks, reporting 147,456 archived rows, 72 marginal coverage values and 72 mean-bias values. All 36 raw-check SHA256 values equal their pinned manifest entries; the raw snapshots have the required 163,840-byte size. No new ensemble was generated.

Clean comparison accepted with no errors. Coverage is represented by exact integer count numerators and compared exactly; the reported maximum numerical gap for tolerant values is `7.105427357601002e-15`, below the frozen bias tolerance `1e-12`. The nominal seed-7 scale-1 coverage anchor is [3909,3888]/4096 and anchor_passed is boolean true. ambiguous_boundaries is an empty list. The signed harness uses `fsum(output)/4096 - nominal`, inclusive nominal-centered coverage, frozen diagonal population covariance and the predeclared 16-ulp boundary policy. The reviewer did not recompute boundary classifications from raw doubles.

Exactly two fixed controls and two saved mutation files are present. Both saved candidates exactly match their predeclared mutation of the archived author-report projection, and both have semantic_rejected=true, validation.accepted=false and a concrete error:

- COVERAGE_PLUS_ONE_PARTICLE changes nominal-7-1.0 coverage component 0 from 3909 to 3910, a fraction change of 1/4096. Rejection is an integer mismatch; no tolerant coverage acceptance was used.
- BIAS_PLUS_1E6 changes nominal-7-1.0 bias component 0 to `-4.799101252312866e-06`. Rejection reports expected independent bias `-5.799101252201844e-06` and gap `9.999999998889774e-07`, exceeding 1e-12. The minor preexisting author/reference arithmetic difference is retained rather than substituted away.

Nominal endpoints and J are explicitly inherited from the pinned PR5 complex-step reference. This execution does not rederive those quantities, regenerate trajectories, revalidate empirical covariance, establish joint coverage or verify real controller safety.

## Raw output, warnings and claim limits

For each problem, parsing stdout yields exactly the full result JSON projection after omitting independent, raw_checks and controls. The omitted fields and mutation files are present in the preserved full artifacts. Literal full-result equality with summary stdout was not required or claimed.

Both stderr files are 98 bytes and contain the preserved Python startup/runtime-location warning `Failed to find real location of C:\Users\Leon1\AppData\Local\Programs\Python\Python313\python.exe`. They are not empty. Both child processes nevertheless completed with exit 0 and readable result JSON; no scientific traceback is present. The same warning appeared in this reviewer's read-only hashing Python invocation, which imported only standard-library modules and did not run science.

| Artifact SHA256 | MED-001 | ENG-004 |
| --- | --- | --- |
| result.json | `185842a7ec032f41e60176f03229615a9e0c8b12d6371c1f4d94daa07a1bba90` | `ed656c3d8e64e174092c49b66222ec837385690805adef54e6845a53ede11175` |
| stdout.txt | `c0357b0a80a11fdcdfc7c07f25b47d7b4832e1ccfbb96fee8e792cff1c753fab` | `1ecaff21f35b814ddc39e6a2a17ff60875dbe791e8dfa6377158a8a0be783542` |
| stderr.txt | `8531d820d22f5cdadd3f00c00d592e13c211ecf2ec0fe113c1931848a5ccc97d` | `8531d820d22f5cdadd3f00c00d592e13c211ecf2ec0fe113c1931848a5ccc97d` |

MED is arithmetic verification of existing synthetic predictions and previously unverified subgroup/conditional intervals. Conditional row intervals ignore calibration-set variability; five-seed t4 summaries are rough Monte Carlo summaries. There is no clinical, real-patient, fairness, causal or novel medical discovery claim. ENG is arithmetic verification on archived finite one-impact cases; seed reuse prevents treating all 36 ensembles as independent replicates. There is no new physical discovery or general safety/calibration guarantee. Both broad_problem_completion flags remain false, author_code_imported flags false and samples_generated zero; MED fits is zero and ENG nominal_and_j_revalidated is false. Source/search failures and abstract-only limits remain explicitly preserved in the protocols and summaries.

## Coordinator finalization still required

At the round-record read during this artifact review, each round remained ADMITTED with execution.status=NOT_RUN and result=null. Actual completed attempt artifacts are present and reviewed above. The coordinator is expected to reconcile these metadata records, write FINISHED/round report/manifests and make local result commits before the unchanged deadline. This review does not prematurely certify FINISHED, final committed result bytes, publication or CI. Those metadata/final-commit checks require their actual records after finalization, without another scientific execution.
