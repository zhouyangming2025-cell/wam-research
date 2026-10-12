"""Short-interval linear pose interpolation check of missed polygon contact.
Interpolation is a mathematical sensitivity check, not new observed ground truth.
"""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parent/'src'))
from trajectory_risk_pilot_r1_reference import poly
import numpy as np,pandas as pd
O=Path(__file__).parent
real=pd.read_csv(O/'data/interaction_original_0p1s_70_73.csv')
extra=pd.read_csv(O/'data/interaction_extra_real_0p1s.csv')
cases={'real_70_vs_72':(real,70,72,2820,2880),'turning_46_vs_47':(extra,46,47,1780,1810),'opposite_26_vs_27':(extra,26,27,980,1010)}
def interp(a,b,w):
 d={}
 for c in ('x','y','vx','vy','length','width'):d[c]=(1-w)*a[c]+w*b[c]
 dth=np.arctan2(np.sin(b['psi_rad']-a['psi_rad']),np.cos(b['psi_rad']-a['psi_rad']))
 d['psi_rad']=a['psi_rad']+w*dth
 return d
items=[]
for name,(df,i,j,st,en) in cases.items():
 A=df[df.track_id==i].set_index('frame_id');B=df[df.track_id==j].set_index('frame_id')
 best=(float('inf'),None);snap=(float('inf'),None);n=0;hits=0
 for f in range(st,en+1):
  x=poly(A.loc[f]).distance(poly(B.loc[f]));
  if x<snap[0]:snap=(float(x),int(f))
 for f in range(st,en):
  for k in range(10):
   w=k/10
   x=poly(interp(A.loc[f],A.loc[f+1],w)).distance(poly(interp(B.loc[f],B.loc[f+1],w)))
   n+=1
   if x<=1e-9:hits+=1
   if x<best[0]:best=(float(x),float(f+w))
 item=dict(case=name,observed_0p1_min_gap_m=snap[0],observed_frame_of_min=snap[1],linear_pose_interpolated_0p01_min_gap_m=best[0],interpolated_frame=best[1],interpolated_contact_count=hits,samples=n,interpolation_assumption='linear center position/shortest heading-angle over each recorded 0.1s interval')
 items.append(item)
print(json.dumps(items,indent=2,ensure_ascii=False))
(O/'results'/'swept_interpolation_check.json').write_text(json.dumps(items,indent=2,ensure_ascii=False),encoding='utf-8')
