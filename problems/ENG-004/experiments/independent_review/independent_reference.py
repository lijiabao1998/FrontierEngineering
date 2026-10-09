"""Independent fixed-time ballistic model, no candidate implementation import."""
import cmath, hashlib, json
from pathlib import Path
REPO=Path(__file__).resolve().parents[4]
ROOT=REPO/'problems/ENG-004/results/independent_review_20261009'
ROOT.mkdir(parents=True,exist_ok=True)
ENG=REPO/'runs/20261009T102807929160Z-gpt-ENG-004/frozen-spec.json'
def endpoint(h, v, case):
    # Direct ballistic trajectory, evaluated over complex scalars for independent
    # complex-step sensitivity. No saltation matrix or author derivative used.
    g, e, floor, T = (case[k] for k in ('g','e','floor','T'))
    w = cmath.sqrt(v*v + 2*g*(h-floor))
    impact = (v+w)/g
    remaining = T-impact
    return [floor+e*w*remaining-g*remaining*remaining/2, e*w-g*remaining]

def main():
    assert hashlib.sha256(ENG.read_bytes()).hexdigest()=='e1501059792e2f054e1e248b263409eb80b1a2f03d89d23f95ef887586bb5420'
    rows=[]
    for c in json.loads(ENG.read_text())['cases']:
        h,v=c['h0'],c['v0']; eps=1e-25
        cols=[[z.imag/eps for z in endpoint(h+eps*1j,v,c)],[z.imag/eps for z in endpoint(h,v+eps*1j,c)]]
        j=[[cols[col][row] for col in range(2)] for row in range(2)]
        det=j[0][0]*j[1][1]-j[0][1]*j[1][0]
        assert abs(det-c['e']**2)<1e-12
        rows.append({'case':c['name'],'endpoint':[z.real for z in endpoint(h,v,c)],'complex_step_jacobian':j,'determinant':det,'expected_determinant':c['e']**2})
    (ROOT/'independent-reference.json').write_text(json.dumps({'engineering':rows,'scope':'Independent complex-step derivatives; same frozen synthetic model, not real-world evidence.'},indent=2)+'\n')
    print('PASS: four complex-step references and determinant identities')
if __name__=='__main__': main()
