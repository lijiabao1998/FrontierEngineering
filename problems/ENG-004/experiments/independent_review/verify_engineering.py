"""Independent output verifier: no candidate code imported or executed."""
import hashlib,json,math,struct
from pathlib import Path
from independent_reference import ENG,ROOT,REPO,endpoint

R=REPO/'problems/ENG-004/results/20261009-saltation'
RAW=R/'raw'
def cov(rows):
    n=len(rows); mean=[math.fsum(r[i] for r in rows)/n for i in range(2)]
    return [[math.fsum((r[i]-mean[i])*(r[j]-mean[j]) for r in rows)/(n-1) for j in range(2)] for i in range(2)]
def transport(J,C):
    return [[math.fsum(J[i][k]*C[k][l]*J[j][l] for k in range(2) for l in range(2)) for j in range(2)] for i in range(2)]
def norm(M):return math.sqrt(math.fsum(x*x for r in M for x in r))
def gap(A,B):return [[A[i][j]-B[i][j] for j in range(2)] for i in range(2)]
def maxgap(A,B):return max(abs(x) for r in gap(A,B) for x in r)
def main():
    spec=json.loads(ENG.read_text()); cases={c['name']:c for c in spec['cases']}
    references={r['case']:r for r in json.loads((ROOT/'independent-reference.json').read_text())['engineering']}
    sensitivities=json.loads((R/'sensitivities.json').read_text())
    assert len(sensitivities)==4
    maxj=max(maxgap(x['saltation_jacobian'],references[x['case']]['complex_step_jacobian']) for x in sensitivities)
    assert maxj<1e-12
    rows=json.loads((R/'ensembles.json').read_text());assert len(rows)==36
    expected={(c,s,z) for c in cases for s in spec['sample_plan']['seeds'] for z in spec['sample_plan']['scales']}
    assert {(r['case'],r['seed'],r['scale']) for r in rows}==expected
    results=[]; largest_state_gap=0; particles=0
    for row in rows:
        name,seed,scale=row['case'],row['seed'],row['scale']; c=cases[name]
        data=(RAW/f'{name}-{seed}-{scale}.bin').read_bytes()
        assert hashlib.sha256(data).hexdigest()==row['raw_ensemble_sha256']
        points=list(struct.iter_unpack('<5d',data));assert len(points)==4096
        assert hashlib.sha256(data+b'!').hexdigest()!=row['raw_ensemble_sha256']
        for dh,dv,h,v,tau in points:
            y=endpoint(c['h0']+dh,c['v0']+dv,c)
            largest_state_gap=max(largest_state_gap,abs(h-y[0].real),abs(v-y[1].real))
            g,e=c['g'],c['e']; w=math.sqrt((c['v0']+dv)**2+2*g*(c['h0']+dh-c['floor']))
            t=((c['v0']+dv)+w)/g
            assert abs(t-tau)<1e-12 and t<c['T']<t+2*e*w/g
        particles+=len(points)
        C=cov([r[:2] for r in points]); E=cov([r[2:4] for r in points]);J=references[name]['complex_step_jacobian']
        P=transport(J,C);err=norm(gap(P,E))/norm(E)
        assert maxgap(C,row['input_covariance'])<1e-15 and maxgap(E,row['empirical_covariance'])<1e-15
        assert maxgap(P,row['saltation_predicted_covariance'])<1e-15
        # Reset-only comparator derived independently from two free-flight maps.
        w=math.sqrt(c['v0']**2+2*c['g']*(c['h0']-c['floor']));tau=(c['v0']+w)/c['g'];u=c['T']-tau
        JR=[[1,tau-c['e']*u],[0,-c['e']]]
        wrongerr=norm(gap(transport(JR,C),E))/norm(E)
        assert err<=.005 and wrongerr/err>=20
        assert abs(err-row['relative_covariance_error'])<1e-9
        results.append({'case':name,'seed':seed,'scale':scale,'independent_relative_error':err,'reset_to_correct_error_ratio':wrongerr/err,'raw_sha256':row['raw_ensemble_sha256']})
    assert largest_state_gap<1e-11
    # Recheck author event outputs against independent closed-form values.
    events=json.loads((R/'events.json').read_text());assert len(events)==16
    max_event_endpoint=0;max_event_time=0
    for x in events:
        c=cases[x['case']];ref=references[x['case']]
        w=math.sqrt(c['v0']**2+2*c['g']*(c['h0']-c['floor']));tau=(c['v0']+w)/c['g']
        et=abs(x['event_aware']['event_time']-tau)
        ep=max(abs(a-b) for a,b in zip(x['event_aware']['endpoint'],ref['endpoint']))
        assert et<=1e-11 and ep<=1e-10
        max_event_endpoint=max(max_event_endpoint,ep);max_event_time=max(max_event_time,et)
    out={'verdict':'INDEPENDENT_FINITE_SYNTHETIC_CHECK_PASS','limits':'Checks only frozen four-case one-impact model and archived draws. No general calibration, novelty, mechanical-system validity or deployment-safety claim. Independent complex-step derivative and covariance arithmetic; not a new empirical experiment. Candidate author test harness not used.','spec_sha256':hashlib.sha256(ENG.read_bytes()).hexdigest(),'particles':particles,'ensembles':len(rows),'max_jacobian_gap':maxj,'max_particle_endpoint_gap':largest_state_gap,'max_event_endpoint_gap':max_event_endpoint,'max_event_time_gap':max_event_time,'maximum_covariance_relative_error':max(r['independent_relative_error'] for r in results),'minimum_error_ratio':min(r['reset_to_correct_error_ratio'] for r in results),'tamper_control':'36/36 appended-byte archives rejected by hash mismatch','results':results}
    (ROOT/'engineering-independent-review.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='results'},indent=2))
if __name__=='__main__':main()
