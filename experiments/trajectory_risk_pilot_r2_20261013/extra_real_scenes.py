#!/usr/bin/env python3
"""True recorded 10 Hz snippets from INTERACTION third-party GitHub sample. No fabricated plans."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parent/'src'))
from trajectory_risk_pilot_r1_reference import v0_components,wu_kernel,poly
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
O=Path(__file__).parent
df=pd.read_csv(O/'data/interaction_extra_real_0p1s.csv')
SCENES={'turning_pair_46_47':(46,47,1780,1810),'opposite_26_27':(26,27,980,1010)}
all_results=[];summaries={}; fig,axes=plt.subplots(2,2,figsize=(13,11),constrained_layout=True)
for row,(name,(ego_id,actor_id,start,end)) in enumerate(SCENES.items()):
 a=df[df.track_id==actor_id].set_index('frame_id').sort_index();e=df[df.track_id==ego_id].set_index('frame_id').sort_index()
 records=[]
 for f in range(start,end+1):
  E=e.loc[f];A=a.loc[f];ve=np.hypot(E.vx,E.vy);va=np.hypot(A.vx,A.vy)
  s,d=v0_components(E.x,E.y,A.x,A.y,A.psi_rad,A.length,A.width,va,ve)
  wu=wu_kernel(E.x,E.y,A.x,A.y,A.psi_rad)*.95**((f-start)/5)
  g=poly(E).distance(poly(A))
  vrel=np.array([E.vx-A.vx,E.vy-A.vy]);pr=np.array([E.x-A.x,E.y-A.y]);rad=float(pr@vrel/np.linalg.norm(pr))
  records.append(dict(scene=name,frame_id=f,t_s=(f-start)*.1,ego_id=ego_id,actor_id=actor_id,gap_m=g,v0star_static=s,v0star_dynamic=d,v0star_total=s+d,wu_single_gt=wu,center_dist_m=np.linalg.norm(pr),separation_rate_mps=rad))
 rec=pd.DataFrame(records);all_results.extend(records)
 fmin=int(rec.loc[rec.gap_m.idxmin(),'frame_id']);p=rec.loc[rec.frame_id==fmin].iloc[0]
 summaries[name]=dict(ego_id=ego_id,actor_id=actor_id,samples=len(rec),min_gap_m=float(rec.gap_m.min()),time_min_gap_s=float(p.t_s),frame_min_gap=fmin,v0star_peak=float(rec.v0star_total.max()),time_peak_s=float(rec.loc[rec.v0star_total.idxmax(),'t_s']),wu_peak=float(rec.wu_single_gt.max()),wu_t_s=float(rec.loc[rec.wu_single_gt.idxmax(),'t_s']),sampled_fullbody_collision=bool((rec.gap_m==0).any()))
 ax=axes[row,0]
 for ID,arr,col in [(ego_id,e,'black'),(actor_id,a,'tab:orange')]:
  ax.plot(arr.x,arr.y,'-',lw=2,color=col,label=f'logged #{ID}')
  r=arr.loc[fmin];xyz=np.asarray(poly(r).exterior.coords)
  ax.add_patch(Polygon(xyz,closed=True,fill=False,edgecolor=col,lw=2))
  ax.arrow(r.x,r.y,.4*r.vx,.4*r.vy,width=.03,head_width=.3,color=col)
 ax.set_aspect('equal');ax.legend(fontsize=8);ax.set_title(f'{name} | closest t={p.t_s:.1f}s gap={p.gap_m:.2f} m')
 ax.grid(alpha=.15);ax.set_xlabel('World x (m)');ax.set_ylabel('World y (m)')
 ax2=axes[row,1];ax2.plot(rec.t_s,rec.v0star_total,label='V0* raw',color='tab:blue');ax2.plot(rec.t_s,rec.wu_single_gt,label='Wu-TS p=1 (oracle)',color='tab:orange');ax3=ax2.twinx();ax3.plot(rec.t_s,rec.gap_m,'k--',label='gap (m)')
 ax2.set_title('Different raw risk semantics vs full-body gap');ax2.set_xlabel('time (s)');ax2.set_ylabel('Uncalibrated field values');ax3.set_ylabel('polygon gap (m)');ax2.grid(alpha=.15)
 h1,l1=ax2.get_legend_handles_labels();h2,l2=ax3.get_legend_handles_labels();ax2.legend(h1+h2,l1+l2,fontsize=8)
pd.DataFrame(all_results).to_csv(O/'results'/'extra_real_scenes_0p1s.csv',index=False)
(O/'results'/'extra_real_summary.json').write_text(json.dumps(summaries,ensure_ascii=False,indent=2),encoding='utf-8')
fig.suptitle('Recorded INTERACTION samples: 10 Hz original states | V0* not parity tested | GT-future Oracle',fontsize=12)
fig.savefig(O/'figures'/'extra_real_pair_comparison.png',dpi=160);plt.close(fig)
print(json.dumps(summaries,ensure_ascii=False,indent=2))
