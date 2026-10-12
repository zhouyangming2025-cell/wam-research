#!/usr/bin/env python3
"""Single-factor synthetic comparisons; physically explicit but no road map or human labels.
All methods evaluate IDENTICAL positions and widths at identical times.
V0* is a handoff-formula port not frozen Gaussian V0. Wu is p=1 time-slice only.
"""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parent/'src'))
from trajectory_risk_pilot_r1_reference import v0_components,wu_kernel,poly
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent
T=np.round(np.arange(0,4.001,.1),3)
def st(x,y,vx,vy,yaw,length=4.7,width=1.8):return dict(x=float(x),y=float(y),vx=float(vx),vy=float(vy),psi_rad=float(yaw),length=length,width=width)
def pair(kind,variant,t):
 if kind=='gap':
  E=st(12*t,0,12,0,0);A=st((26 if variant=='far' else 17)+10*t,0,10,0,0)
 elif kind=='closing':
  ve=10 if variant=='same_speed' else 14;E=st(ve*t,0,ve,0,0);A=st(25+10*t,0,10,0,0)
 elif kind=='front_brake':
  E=st(12*t,0,12,0,0)
  if variant=='keep_10': ax=27+10*t;av=10
  else:
   dt=max(0,t-1);v=max(0,10-5*dt);ax=27+10*min(t,1)+(10*dt-2.5*dt*dt if dt<=2 else 10);av=v
  A=st(ax,0,av,0,0)
 elif kind=='rear_accel':
  E=st(10*t,0,10,0,0)
  if variant=='stable':ax=-20+10*t;av=10
  else:ax=-20+10*t+1.5*t*t;av=10+3*t
  A=st(ax,0,av,0,0)
 elif kind=='opposite':
  E=st(10*t,0,10,0,0)
  if variant=='same_direction':A=st(25+10*t,0,10,0,0)
  else:A=st(25-10*t,0,-10,0,np.pi)
 elif kind=='crossing':
  E=st(-16+8*t,0,8,0,0)
  if variant=='simultaneous':yy=-12+6*t
  else:yy=-12+6*(t-2)
  A=st(0,yy,0,6,np.pi/2)
 elif kind=='pedestrian':
  E=st(-12+6*t,0,6,0,0)
  if variant=='cross': yy=-6+3*t;vy=3
  else: yy=-6;vy=0
  A=st(0,yy,0,vy,np.pi/2,.6,.6)
 elif kind=='cutin':
  E=st(10*t,0,10,0,0)
  ay=3.5 if variant=='parallel' else 3.5*(1-min(t/3,1))
  avy=0 if variant=='parallel' or t>=3 else -3.5/3
  A=st(8+10*t,ay,10,avy,np.arctan2(avy,10))
 elif kind=='cone_yaw':
  E=st(-12+8*t,0,8,0,0)
  A=st(0,0,0,0,0 if variant=='yaw0' else np.pi/2,.4,.3)
 elif kind=='parked_car':
  E=st(-12+8*t,0,8,0,0)
  A=st(0,0,0,0,0 if variant=='yaw0' else np.pi/2,4.8,1.9)
 elif kind=='front_edge':
  E=st(0,0,0,0,0,5,2);A=st(2.45,0,0,0,0,.15,.15)
 else:raise ValueError(kind)
 return E,A
scenes={
 'gap':['far','near'],'closing':['same_speed','fast_ego'],'front_brake':['keep_10','brake_after_1s'],'rear_accel':['stable','accelerate'],'opposite':['same_direction','head_on'],'crossing':['simultaneous','delayed_2s'],'pedestrian':['wait','cross'],'cutin':['parallel','cut_in'],'cone_yaw':['yaw0','yaw90'],'parked_car':['yaw0','yaw90'],'front_edge':['touch','touch']}
out=[]
for kind,variants in scenes.items():
 for variant in dict.fromkeys(variants):
  for t in T:
   E,A=pair(kind,variant,t); ve=np.hypot(E['vx'],E['vy']);va=np.hypot(A['vx'],A['vy']);s,d=v0_components(E['x'],E['y'],A['x'],A['y'],A['psi_rad'],A['length'],A['width'],va,ve)
   w=wu_kernel(E['x'],E['y'],A['x'],A['y'],A['psi_rad'])*(.95**(t/.5))
   gap=poly(E).distance(poly(A))
   out.append(dict(case=kind,variant=variant,t_s=t,geom_gap_m=gap,collision=bool(poly(E).intersects(poly(A))),v0star_total=float(s+d),v0star_static=float(s),v0star_dynamic=float(d),wu_ts=float(w),ego_speed=ve,actor_speed=va))
df=pd.DataFrame(out)
df.to_csv(O/'results'/'controlled_10_factors_0p1s.csv',index=False)
summary=[]
for kind in scenes:
 for variant,grp in df[df.case==kind].groupby('variant'):
  summary.append(dict(case=kind,variant=variant,min_geom_gap_m=float(grp.geom_gap_m.min()),collision_detected=bool(grp.collision.any()),v0star_peak=float(grp.v0star_total.max()),v0star_t0=float(grp.v0star_total.iloc[0]),wu_ts_peak=float(grp.wu_ts.max()),wu_ts_t0=float(grp.wu_ts.iloc[0]),time_min_gap_s=float(grp.loc[grp.geom_gap_m.idxmin(),'t_s'])))
S=pd.DataFrame(summary);S.to_csv(O/'results'/'controlled_summary.csv',index=False)
print(S.to_string(index=False))
# line plots: per scenario preserve within-model numerical scale; geometry on right axis, not same units.
for page,cases in enumerate([['gap','closing','front_brake','rear_accel'],['opposite','crossing','pedestrian','cutin'],['cone_yaw','parked_car','front_edge']]):
 fig,axs=plt.subplots(len(cases),2,figsize=(13,3.7*len(cases)),constrained_layout=True)
 if len(cases)==1:axs=np.array([axs])
 for row,kind in enumerate(cases):
  subset=df[df.case==kind]
  for variant,g in subset.groupby('variant'):
   axs[row,0].plot(g.t_s,g.v0star_total,label=variant)
   axs[row,1].plot(g.t_s,g.wu_ts,label=variant)
  axs[row,0].set_title(f'{kind} | V0* (not frozen)');axs[row,1].set_title(f'{kind} | Wu time-slice (oracle)')
  for ax in axs[row]:ax.set_xlabel('Time (s)');ax.set_ylabel('Uncalibrated query');ax.grid(alpha=.2);ax.legend(fontsize=8)
 fig.savefig(O/'figures'/f'controlled_page_{page+1}.png',dpi=150);plt.close(fig)
# JSON experiment protocol labels
cfg={
 'label':'SYNTHETIC_INPUTS/ORACLE_INPUT_STATE','time_step_s':.1,'horizon_s':4,
 'formula_port':'V0* handoff source unverified; ego reference at center; actor SUM only one actor',
 'wu':'Wu Eq7-9 one deterministic future mode p=1; a=6,b=2, gamma=.95 per 0.5s; not TRTP',
 'geometry':'Shapely exact oriented rectangle per step; gap=0 insufficient by itself to distinguish deep overlap',
 'cases':{
  'gap':'fixed ego12m/s front10m/s; only initial 26m vs17m center spacing',
  'closing':'fixed front10m/s at 25m; ego10 vs14m/s; geometry at t=0 fixed',
  'front_brake':'fixed initial states; front 10m/s constant vs -5m/s^2 after t=1 (stop t=3)',
  'rear_accel':'fixed initial states; actor rear -20m at10m/s vs accelerating 3m/s2',
  'opposite':'same scalar speed 10m/s each; actor continues same direction vs heads toward ego from x25m (yaw rotates physically)',
  'crossing':'fixed linear tracks; actor passes intersection t=2 vs t=4; first sample differs by actor initial location',
  'pedestrian':'same actor initial location; actor waits vs cross t=2; ego constant',
  'cutin':'same ego and initial actor; actor keeps 3.5m lateral gap vs moves into ego lane by t=3, physically not dynamics-checked',
  'cone_yaw':'same tiny static obstacle occupancy approximated oriented 0.4x0.3m rectangle; change yaw only, note not exactly symmetric geometry',
  'parked_car':'actual oriented 4.8x1.9 rectangle yaw alters physical occupancy hence geometric risk may legitimately change',
  'front_edge':'ego rectangle 5x2 touching tiny .15m obstacle at x=2.45m with center 2.45m away'} }
(O/'config.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2),encoding='utf-8')
