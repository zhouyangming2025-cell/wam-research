"""Analytic longitudinal braking/RSS-style envelope; not CommonRoad library implementation.
Parameters are illustrative, not vendor-authoritative. Applies only to 1-D ordered vehicles.
"""
from pathlib import Path
import numpy as np, pandas as pd,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent
def rss_longitudinal(v_rear,v_front,rho=1.,a_accel_max=2.,b_rear_min=4.,b_front_max=6.):
 return max(0,v_rear*rho+.5*a_accel_max*rho**2 + (v_rear+a_accel_max*rho)**2/(2*b_rear_min) - v_front**2/(2*b_front_max))
rows=[]
for v_ego in [8,10,12,14,18]:
 for gap in [5,10,15,20,30,40]:
  vf=10
  b=(max(0.,v_ego-vf)**2)/(2*gap)
  threshold=rss_longitudinal(v_ego,vf)
  rows.append(dict(ego_v=v_ego,front_v=vf,gap=gap,b_required_simple=b,b_ratio_to_max4=b/4,rss_required_gap=threshold,rss_margin=gap-threshold,rss_violated=gap<threshold))
df=pd.DataFrame(rows);df.to_csv(O/'results'/'controlled_longitudinal_rss_analytic.csv',index=False)
# user specified physical validity: no rear/front shuffles; gap is bumper-to-bumper
fig,ax=plt.subplots(figsize=(9,5),constrained_layout=True)
for v in [8,10,12,14,18]:
 p=df[df.ego_v==v];ax.plot(p.gap,p.rss_margin,'o-',label=f'ego {v} m/s')
ax.axhline(0,c='k',ls='--',lw=1);ax.set_xlabel('Bumper gap (m)');ax.set_ylabel('Gap minus RSS-style longitudinal threshold (m)');ax.set_title('Illustrative RSS safety margin (not official library validation)');ax.grid(alpha=.2);ax.legend()
fig.savefig(O/'figures'/'longitudinal_safety_margin.png',dpi=155);plt.close(fig)
config={'rho_s':1,'max_accel_during_response_mps2':2,'min_ego_braking_mps2':4,'max_front_braking_mps2':6,'assumption':'single lane ordered rear ego/front actor; no lateral, exact speed; illustrative safety margin, not certified RSS implementation'}
(O/'results'/'longitudinal_assumptions.json').write_text(json.dumps(config,indent=2),encoding='utf-8')
print('same 10m/s and 20m gap threshold',rss_longitudinal(10,10),'; 14m/s following front10m/s',rss_longitudinal(14,10))
