"""Independent archived-bin coverage/bias, conditional on frozen nominal/J."""
import argparse,copy,hashlib,json,math,struct,sys,traceback
from pathlib import Path
from admission_guard import require_admission
from common import compare
HERE=Path(__file__).resolve().parent
Z=1.959963984540054
EXPECTED_CONTROLS=('COVERAGE_PLUS_ONE_PARTICLE','BIAS_PLUS_1E6')

def calculate(protocol):
    manifest=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
    for row in manifest['files']:
        if hashlib.sha256((HERE/row['snapshot']).read_bytes()).hexdigest()!=row['sha256']:raise ValueError('frozen blob hash '+row['path'])
    ensembles=json.loads((HERE/'reference/ensembles.json').read_text())
    refs=json.loads((HERE/'reference/independent-reference.json').read_text())['engineering']
    refs={r['case']:r for r in refs}
    expected_keys={(c,s,scale) for c in protocol['cases'] for s in protocol['seeds'] for scale in protocol['scales']}
    keys={(r['case'],r['seed'],r['scale']) for r in ensembles}
    if len(ensembles)!=36 or keys!=expected_keys:raise ValueError('ensemble combinations')
    if set(refs)!=set(protocol['cases']):raise ValueError('reference domain')
    output={};author={};checks=[];ambiguous=[]
    for r in ensembles:
        case,seed,scale=r['case'],r['seed'],float(r['scale']);key=f'{case}-{seed}-{scale}'
        raw=(HERE/'reference/raw'/(key+'.bin')).read_bytes();digest=hashlib.sha256(raw).hexdigest()
        if digest!=r['raw_ensemble_sha256'] or len(raw)!=4096*40 or r['n']!=4096:raise ValueError('raw hash/count '+key)
        ref=refs[case];nominal=ref['endpoint'];j=ref['complex_step_jacobian']
        if any(abs(a-b)>1e-12 for a,b in zip(nominal,r['nominal_endpoint'])):raise ValueError('nominal disagreement')
        diagonal=[math.fsum([j[k][0]**2*(scale*0.001)**2,j[k][1]**2*(scale*0.002)**2]) for k in range(2)]
        radius=[Z*math.sqrt(v) for v in diagonal]
        values=[[],[]];counts=[0,0];min_margin=[math.inf,math.inf]
        for index,record in enumerate(struct.iter_unpack('<5d',raw)):
            if not all(math.isfinite(v) for v in record):raise ValueError('nonfinite record')
            for k in range(2):
                d=record[k+2]-nominal[k];values[k].append(record[k+2])
                margin=abs(abs(d)-radius[k]);min_margin[k]=min(min_margin[k],margin)
                ambiguity=16*(math.ulp(radius[k])+math.ulp(abs(record[k+2]))+math.ulp(abs(nominal[k])))
                if margin<=ambiguity:ambiguous.append({'key':key,'row':index,'component':k,'margin':margin,'roundoff_envelope':ambiguity})
                counts[k]+=int(abs(d)<=radius[k])
        output[key]={'coverage':counts,'bias':[math.fsum(v)/4096-nominal[k] for k,v in enumerate(values)]}
        # Store coverage as exact integer numerators, not a tolerant float.
        ac=r['marginal_95_coverage']
        if len(ac)!=2 or any(type(v) not in (int,float) or not math.isfinite(v) or v*4096!=int(v*4096) or not 0<=v<=1 for v in ac):raise ValueError('author coverage domain')
        author[key]={'coverage':[int(v*4096) for v in ac],'bias':r['mean_bias']}
        checks.append({'key':key,'sha256':digest,'rows':4096,'population_diagonal':diagonal,'radius':radius,'minimum_boundary_margin':min_margin,'coverage': [v/4096 for v in counts]})
    return output,author,checks,ambiguous

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--round',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    require_admission(a.repo,a.round,'ENG-004',HERE/'PROTOCOL.json')
    protocol=json.loads((HERE/'PROTOCOL.json').read_text())
    if tuple(c['name'] for c in protocol['controls'])!=EXPECTED_CONTROLS:raise ValueError('frozen control domain/order')
    if protocol['cases']!=['nominal','elastic','translated_guard','ood_low_gravity'] or protocol['seeds']!=[7,23,101] or protocol['scales']!=[1,.5,.25]:raise ValueError('frozen ensemble domain')
    expected,author,checks,ambiguous=calculate(protocol);clean=compare(expected,author,1e-12)
    out=Path(a.output).parent;mdir=out/'mutants';mdir.mkdir();controls=[]
    for c in protocol['controls']:
        mutant=copy.deepcopy(author);key=c['key'];mutant[key][c['field']][c['component']]+=c['delta']
        ver=compare(expected,mutant,1e-12)
        (mdir/(c['name']+'.json')).write_text(json.dumps(mutant,indent=2)+'\n',encoding='utf-8')
        controls.append({'name':c['name'],'semantic_rejected':not ver['accepted'],'validation':ver})
    anchor=expected['nominal-7-1.0'];anchors=anchor['coverage']==[3909,3888] and all(abs(v-w)<=1e-12 for v,w in zip(anchor['bias'],[-5.799101252312866e-6,5.219509491638519e-5]))
    ok=clean['accepted'] is True and len(controls)==2 and all(c['semantic_rejected'] is True for c in controls) and not ambiguous and anchors is True
    verdict='INDEPENDENT_ARCHIVED_COVERAGE_BIAS_PASS' if ok else 'INCOMPLETE_BOUNDARY_AMBIGUITY' if ambiguous else 'FAIL_CLOSED_COVERAGE_BIAS'
    payload={'verdict':verdict,'all_criteria_passed':ok,'raw_files':36,'rows':147456,'coverage_values':72,'bias_values':72,'source_integrity':True,
      'clean_validation':clean,'controls':controls,'ambiguous_boundaries':ambiguous,'anchor_passed':anchors,'raw_checks':checks,'independent':expected,
      'limits':protocol['limits'],'broad_problem_completion':False,'author_code_imported':False,'samples_generated':0,'nominal_and_j_revalidated':False}
    Path(a.output).write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in payload.items() if k not in ['controls','independent','raw_checks']}));return 0 if ok else 1

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as e:print(json.dumps({'verdict':'INCOMPLETE_FAIL_CLOSED','error':str(e)}),file=sys.stderr);traceback.print_exc();sys.exit(2)
