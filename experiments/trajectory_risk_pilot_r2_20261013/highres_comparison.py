#!/usr/bin/env python3
"""Compare the *recorded* 10 Hz INTERACTION sequence with 2 Hz downsampling.
The Gaussian is V0* only; Wu is deterministic single-recorded-mode (oracle).
"""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parent/'src'))
from trajectory_risk_pilot_r1_reference import v0_components,wu_kernel,poly
import pandas as pd,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=Path(__file__).parent
(OUT/'figures').mkdir(parents=True,exist_ok=True)  # clean checkout has no figures/
(OUT/'results').mkdir(parents=True,exist_ok=True)
df=pd.read_csv(OUT/'data/interaction_original_0p1s_70_73.csv')
groups={id:g.set_index('frame_id') for id,g in df.groupby('track_id')}
def evaluate(frame):
 e=groups[70].loc[frame];v_e=float(np.hypot(e.vx,e.vy));dt=(frame-2820)/10
 vals=[]
 for actor in (71,72,73):
  a=groups[actor].loc[frame];v_a=float(np.hypot(a.vx,a.vy))
  static,dynamic=v0_components(e.x,e.y,a.x,a.y,a.psi_rad,a.length,a.width,v_a,v_e)
  wu=wu_kernel(e.x,e.y,a.x,a.y,a.psi_rad)
  gap=poly(e).distance(poly(a))
  vals.append(dict(actor_id=actor,gap=float(gap),static=float(static),dynamic=float(dynamic),v0=float(static+dynamic),wu=float(wu)))
 return dict(t_s=dt,frame_id=frame,min_geom_gap_m=min(v['gap'] for v in vals),nearest_actor=min(vals,key=lambda v:v['gap'])['actor_id'],v0star_sum=sum(v['v0'] for v in vals),v0star_max=max(v['v0'] for v in vals),wu_ts_sum=(.95**(dt/.5))*sum(v['wu'] for v in vals),dominant_actor=max(vals,key=lambda v:v['v0'])['actor_id'])
R=pd.DataFrame([evaluate(t) for t in range(2820,2881)])
R.to_csv(OUT/'results'/'real_0p1s_time_series.csv',index=False)
r5=R[R.frame_id%5==0]
old=pd.read_csv(OUT/'data'/'baseline_R1_0p5s_scores.csv');old=old[old.offset_m==0]
joined=r5.merge(old,on='frame_id',suffixes=('_0p1','_old'))
parity={"geom_abs_max":float(np.max(abs(joined.min_geom_gap_m-joined.geom_gap_m))),"v0star_abs_max":float(np.max(abs(joined.v0star_sum-joined.v0_total))),"wu_abs_max":float(np.max(abs(joined.wu_ts_sum-joined.wu_field)))}
assert max(parity.values())<1e-11,parity
S={}
for sample,name in ((R,'0.1s'),(r5,'0.5s')):
 s=sample
 S[name]=dict(n=len(s),min_gap_m=float(s.min_geom_gap_m.min()),min_gap_t_s=float(s.loc[s.min_geom_gap_m.idxmin(),'t_s']),v0_peak=float(s.v0star_sum.max()),v0_peak_t_s=float(s.loc[s.v0star_sum.idxmax(),'t_s']),wu_peak=float(s.wu_ts_sum.max()),wu_peak_t_s=float(s.loc[s.wu_ts_sum.idxmax(),'t_s']),v0_mean_arithmetic=float(s.v0star_sum.mean()),wu_mean_arithmetic=float(s.wu_ts_sum.mean()),observed_collisions_count=int((s.min_geom_gap_m==0).sum()))
S['parity_0p5s_vs_original']=parity
(OUT/'results'/'sampling_comparison.json').write_text(json.dumps(S,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(S,ensure_ascii=False,indent=2))
fig,axs=plt.subplots(3,1,figsize=(12,10),sharex=True,constrained_layout=True)
for ax,k,label in zip(axs,['min_geom_gap_m','v0star_sum','wu_ts_sum'],['Full-body gap (m)','V0* raw query','Wu-TS raw query']):
 ax.plot(R.t_s,R[k],label='10 Hz recorded',lw=1.8)
 ax.plot(r5.t_s,r5[k],'o',label='2 Hz subsample',ms=4)
 ax.set_ylabel(label);ax.grid(alpha=.2);ax.legend()
axs[-1].set_xlabel('Time since first sample (s)');fig.suptitle('INTERACTION real logged coordinates: original 10 Hz vs 2 Hz subsampling\nV0* and Wu: same kernel/physical position; Oracle logged future',fontsize=12)
fig.savefig(OUT/'figures'/'sampling_0p1_vs_0p5_real.png',dpi=150);plt.close(fig)
