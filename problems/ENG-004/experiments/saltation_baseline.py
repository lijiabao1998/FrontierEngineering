#!/usr/bin/env python3
"""Synthetic single-impact replication. Reports metrics, never scientific success.

No dependencies beyond Python's standard library. Models are fixed by frozen-spec.
The direct derivative and finite differences are author consistency checks, not
independent verification. No card/evaluator/acceptance threshold is changed here.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,math,platform,random,struct,sys,time
from pathlib import Path

SPEC_HASH='e1501059792e2f054e1e248b263409eb80b1a2f03d89d23f95ef887586bb5420'

def matmul(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def transport(j,p): return matmul(matmul(j,p),list(map(list,zip(*j))))
def sub(a,b): return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def frob(a): return math.sqrt(sum(x*x for row in a for x in row))
def maxerr(a,b): return max(abs(x-y) for ar,br in zip(a,b) for x,y in zip(ar,br))
def phi(t): return [[1.,t],[0.,1.]]

def flight(h,v,g,t): return h+v*t-.5*g*t*t,v-g*t

def exact(c,h=None,v=None):
    h=c['h0'] if h is None else h; v=c['v0'] if v is None else v
    b,g,e,T=(c[k] for k in ('floor','g','e','T'))
    if not (h>b and g>0 and 0<e<=1): raise ValueError('unsupported initial/model condition')
    w=math.sqrt(v*v+2*g*(h-b)); tau=(v+w)/g
    if not (0<tau<T<tau+2*e*w/g): raise ValueError('not exactly one separated impact')
    u=T-tau
    return {'event_time':tau,'impact_velocity':-w,'endpoint':[b+e*w*u-.5*g*u*u,e*w-g*u]}

def saltation_jacobian(c,method='saltation'):
    q=exact(c); tau=q['event_time']; vminus=q['impact_velocity'];g,e=c['g'],c['e']
    reset=[[1.,0.],[0.,-e]]
    if method=='reset_only': s=reset
    else:
        # S = DR + (f+ - DR f-) n^T / (n^T f-), n=(1,0).
        correction=[[-(1.+e),0.],[-g*(1.+e)/vminus,0.]]
        sign=-1. if method=='wrong_timing_sign' else 1.
        s=[[reset[i][k]+sign*correction[i][k] for k in range(2)] for i in range(2)]
    return matmul(matmul(phi(c['T']-tau),s),phi(tau))

def direct_derivative(c):
    # Differentiate w and tau in the explicit final-state expression.
    q=exact(c);w=-q['impact_velocity'];u=c['T']-q['event_time'];g,e,v=c['g'],c['e'],c['v0']
    dw=[g/w,v/w]; dtau=[1/w,(1+v/w)/g]
    return [[e*u*dw[i]-(e*w-g*u)*dtau[i] for i in range(2)],
            [e*dw[i]+g*dtau[i] for i in range(2)]]

def finite_difference(c,epsilon):
    j=[[0.,0.],[0.,0.]]
    for k in range(2):
        xp=[c['h0'],c['v0']];xm=xp.copy();xp[k]+=epsilon;xm[k]-=epsilon
        yp=exact(c,*xp)['endpoint'];ym=exact(c,*xm)['endpoint']
        for i in range(2):j[i][k]=(yp[i]-ym[i])/(2*epsilon)
    return j

def event_stepper(c,dt,delayed=False):
    # Ballistic substeps are exact for constant g. Only event localization differs.
    h,v,t=c['h0'],c['v0'],0.;b,g,T=c['floor'],c['g'],c['T'];event=None;min_height=h-b;steps=0
    while t<T-1e-15:
        d=min(dt,T-t);hn,vn=flight(h,v,g,d);steps+=1
        if hn<=b and vn<0:
            if event is not None:raise ValueError('second event outside one-impact solver')
            if delayed:
                event=t+d;min_height=min(min_height,hn-b);h=b;v=-c['e']*vn;t+=d
            else:
                lo,hi=0.,d
                for _ in range(60):
                    mid=(lo+hi)/2
                    if flight(h,v,g,mid)[0]>b:lo=mid
                    else:hi=mid
                local=(lo+hi)/2;hit_h,hit_v=flight(h,v,g,local)
                event=t+local
                h,v=flight(b,-c['e']*hit_v,g,d-local);t+=d
                min_height=min(min_height,hit_h-b,h-b)
        else:h,v,t=hn,vn,t+d;min_height=min(min_height,h-b)
    if event is None:raise ValueError('missing impact')
    return {'event_time':event,'endpoint':[h,v],'min_sampled_height_above_guard':min_height,'steps':steps}

class Moments:
    def __init__(self):self.n=0;self.mean=[0.,0.];self.m2=[[0.,0.],[0.,0.]]
    def add(self,x):
        self.n+=1;delta=[x[i]-self.mean[i] for i in range(2)]
        self.mean=[self.mean[i]+delta[i]/self.n for i in range(2)]
        delta2=[x[i]-self.mean[i] for i in range(2)]
        for i in range(2):
            for k in range(2):self.m2[i][k]+=delta[i]*delta2[k]
    def covariance(self):return [[x/(self.n-1) for x in row] for row in self.m2]

def ensemble(c,seed,scale,sample):
    rng=random.Random(seed);mi,mo=Moments(),Moments();nom=exact(c);j=saltation_jacobian(c);bad=saltation_jacobian(c,'reset_only')
    p=[[sample['sigma_h']**2*scale**2,0.],[0.,sample['sigma_v']**2*scale**2]]
    pop=transport(j,p);width=[1.959963984540054*math.sqrt(pop[i][i]) for i in range(2)];counts=[0,0];records=[];hasher=hashlib.sha256()
    min_y=math.inf;mint=math.inf;maxt=-math.inf
    for idx in range(sample['n_per_run']):
        dh=rng.gauss(0,sample['sigma_h']*scale);dv=rng.gauss(0,sample['sigma_v']*scale)
        q=exact(c,c['h0']+dh,c['v0']+dv);y=q['endpoint'];mi.add([dh,dv]);mo.add(y);t=q['event_time'];min_y=min(min_y,y[0]-c['floor']);mint=min(mint,t);maxt=max(maxt,t)
        hasher.update(struct.pack('<5d',dh,dv,*y,t))
        for k in range(2): counts[k]+=abs(y[k]-nom['endpoint'][k])<=width[k]
        if idx<12:records.append([c['name'],seed,scale,idx,dh,dv,*y,t])
    empirical=mo.covariance();pred=transport(j,mi.covariance());reset_pred=transport(bad,mi.covariance());norm=frob(empirical)
    a=frob(sub(pred,empirical))/norm;b=frob(sub(reset_pred,empirical))/norm
    return {'case':c['name'],'seed':seed,'scale':scale,'n':mi.n,'input_mean_delta':mi.mean,'input_covariance':mi.covariance(),'output_mean':mo.mean,'nominal_endpoint':nom['endpoint'],'mean_bias':[mo.mean[i]-nom['endpoint'][i] for i in range(2)],'empirical_covariance':empirical,'saltation_predicted_covariance':pred,'reset_predicted_covariance':reset_pred,'relative_covariance_error':a,'reset_only_relative_covariance_error':b,'reset_to_saltation_error_ratio':b/a if a else None,'marginal_95_coverage':[n/mi.n for n in counts],'event_time_min':mint,'event_time_max':maxt,'exactly_one_event_count':mi.n,'endpoint_guard_violation_count':0 if min_y>=0 else None,'minimum_endpoint_height_above_guard':min_y,'raw_ensemble_sha256':hasher.hexdigest(),'raw_encoding':'ordered particle records struct.pack(<5d, dh,dv,h(T),v(T),tau), Python random.Random(seed).gauss; all 4096 records regenerated by --dump-raw'},records

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--spec',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--dump-raw',type=Path);a=ap.parse_args();start=time.monotonic()
    if hashlib.sha256(a.spec.read_bytes()).hexdigest()!=SPEC_HASH:raise ValueError('frozen specification hash mismatch')
    spec=json.loads(a.spec.read_text());a.output.mkdir(parents=True,exist_ok=True)
    sensitivities=[];events=[];ensembles=[];traces=[];controls=[]
    for c in spec['cases']:
        analytic=exact(c);direct=direct_derivative(c);salt=saltation_jacobian(c)
        sensitivities.append({'case':c['name'],'analytic':analytic,'saltation_jacobian':salt,'direct_jacobian':direct,'saltation_direct_max_abs_error':maxerr(salt,direct),'finite_differences':[{'epsilon':eps,'jacobian':finite_difference(c,eps),'max_abs_error':maxerr(finite_difference(c,eps),direct)} for eps in spec['fd_steps']]})
        for dt in spec['step_sizes']:
            q=event_stepper(c,dt);delay=event_stepper(c,dt,True)
            events.append({'case':c['name'],'dt':dt,'event_aware':q,'delayed_grid':delay,'event_aware_time_error':abs(q['event_time']-analytic['event_time']),'event_aware_endpoint_max_abs_error':max(abs(x-y) for x,y in zip(q['endpoint'],analytic['endpoint'])),'delayed_time_error':abs(delay['event_time']-analytic['event_time'])})
        for method in ['reset_only','wrong_timing_sign']:
            controls.append({'case':c['name'],'injection':method,'jacobian':saltation_jacobian(c,method),'direct_jacobian_max_abs_error':maxerr(saltation_jacobian(c,method),direct)})
        for seed in spec['sample_plan']['seeds']:
            for scale in spec['sample_plan']['scales']:
                result,records=ensemble(c,seed,scale,spec['sample_plan']);ensembles.append(result);traces.extend(records)
                if a.dump_raw:
                    a.dump_raw.mkdir(parents=True,exist_ok=True);rng=random.Random(seed);raw=bytearray()
                    for idx in range(spec['sample_plan']['n_per_run']):
                        dh=rng.gauss(0,spec['sample_plan']['sigma_h']*scale);dv=rng.gauss(0,spec['sample_plan']['sigma_v']*scale);q=exact(c,c['h0']+dh,c['v0']+dv)
                        raw.extend(struct.pack('<5d',dh,dv,*q['endpoint'],q['event_time']))
                    (a.dump_raw/(c['name']+'-'+str(seed)+'-'+str(scale)+'.bin')).write_bytes(raw)
    # Positive pre-impact case, direct polynomial propagation for symmetric cloud.
    initial=[[.001,.002],[.001,-.002],[-.001,.002],[-.001,-.002]];mi=Moments();mo=Moments();pre_t=.2
    for dh,dv in initial:mi.add([dh,dv]);mo.add([dh+dv*pre_t,dv])
    controls.append({'injection':'none_preimpact_positive','jacobian':phi(pre_t),'covariance_max_abs_error':maxerr(transport(phi(pre_t),mi.covariance()),mo.covariance())})
    for c in [dict(spec['cases'][0],h0=-1),dict(spec['cases'][0],T=2),dict(spec['cases'][0],e=0)]:
        try:exact(c);controls.append({'injection':'unsupported_boundary','observed':'unexpected acceptance'})
        except ValueError as e:controls.append({'injection':'unsupported_boundary','observed':'rejected','reason':str(e)})
    for name,data in [('sensitivities.json',sensitivities),('events.json',events),('ensembles.json',ensembles),('controls.json',controls)]:
        (a.output/name).write_text(json.dumps(data,indent=2,sort_keys=True,allow_nan=False)+'\n')
    with (a.output/'trace-samples.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['case','seed','scale','index','delta_h','delta_v','h_T','v_T','tau']);writer.writerows(traces)
    files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(a.output.iterdir()) if p.is_file() and p.name in ['sensitivities.json','events.json','ensembles.json','controls.json','trace-samples.csv']}
    (a.output/'SHA256SUMS.json').write_text(json.dumps(files,indent=2)+'\n')
    summary={'scope':'Author-generated synthetic metrics; independent verification pending. No scientific completion or safety certification.','configuration_count':36+16+12+8+1+3,'particle_trajectories':36*4096,'max_event_time_error':max(q['event_aware_time_error'] for q in events),'max_event_endpoint_error':max(q['event_aware_endpoint_max_abs_error'] for q in events),'max_saltation_direct_jacobian_error':max(q['saltation_direct_max_abs_error'] for q in sensitivities),'worst_best_fd_error':max(min(f['max_abs_error'] for f in q['finite_differences']) for q in sensitivities),'max_relative_covariance_error':max(q['relative_covariance_error'] for q in ensembles),'minimum_reset_to_saltation_error_ratio':min(q['reset_to_saltation_error_ratio'] for q in ensembles),'python':sys.version,'platform':platform.platform(),'elapsed_seconds':time.monotonic()-start,'frozen_spec_sha256':SPEC_HASH}
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
