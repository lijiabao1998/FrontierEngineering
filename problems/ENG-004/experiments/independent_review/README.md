# Independent ENG-004 verifier

This code does not import or execute the candidate implementation. It uses a directly written ballistic endpoint, complex-step sensitivity, determinant identity, compensated-sum covariance, and all archived input/output trajectories.

Run from repository root with Python3.12 standard library:

    python3 problems/ENG-004/experiments/independent_review/independent_reference.py
    python3 problems/ENG-004/experiments/independent_review/verify_engineering.py
    python3 problems/ENG-004/experiments/independent_review/test_negative_controls.py

This is a separate reviewer/evaluator publication unit. It leaves the author's method, original frozen acceptance, result bytes and problem card unchanged. It is deterministic verification of disclosed existing synthetic results, not blinded new science. No novel theorem, general calibration, physical-system validity or deployment-safety claim.
