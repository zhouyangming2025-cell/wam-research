#!/usr/bin/env python3
"""Auditable component-only diagnosis of the *unverified* V0* 13-step port.
Never calls a frozen original; does not claim to reproduce SimWAM or real candidate scores."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parent/'src'))
from trajectory_risk_pilot_r1_reference import v0_components,poly
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
OUT=Path(__file__).parent
DF=pd.read_csv(str(OUT/'data'/'interaction_R1_0p5s_70_73.csv'))
T=[]
for frame in sorted(DF.frame_id.unique()):
    ego=DF[(DF.track_id==70)&(DF.frame_id==frame)].iloc[0]
    ve=np.hypot(ego.vx,ego.vy)
    local=[]
    for i in (71,72,73):
        a=DF[(DF.track_id==i)&(DF.frame_id==frame)].iloc[0]
        va=np.hypot(a.vx,a.vy)
        dx=ego.x-a.x;dy=ego.y-a.y
        f=dx*np.cos(a.psi_rad)+dy*np.sin(a.psi_rad)
        lat=-dx*np.sin(a.psi_rad)+dy*np.cos(a.psi_rad)
        sx=1.5*a.length+.001;sy=a.width+.001;sv=6*abs(ve-va)+.001
        d=(-1 if va>ve else 1)
        arg=d*(f-.9*a.length*d)
        gate=1/(1+np.exp(np.clip(arg,-60,60)))
        stat,dyn=v0_components(ego.x,ego.y,a.x,a.y,a.psi_rad,a.length,a.width,va,ve)
        gap=poly(ego).distance(poly(a))
        velrel=(ego.vx-a.vx,ego.vy-a.vy)
        radial= (dx*velrel[0]+dy*velrel[1])/max(1e-9,np.hypot(dx,dy))
        heading_tangent=np.arctan2(a.vy,a.vx) if va>0.05 else float('nan')
        theta_d=np.arctan2(np.sin(a.psi_rad-heading_tangent),np.cos(a.psi_rad-heading_tangent)) if va>0.05 else float('nan')
        local.append(dict(frame_id=int(frame),t_s=round((frame-2820)/10,2),actor_id=i,center_distance_m=float(np.hypot(dx,dy)),poly_gap_m=float(gap),dx_world_m=float(dx),dy_world_m=float(dy),local_forward_m=float(f),local_lateral_m=float(lat),actor_speed_mps=float(va),ego_speed_mps=float(ve),speed_magnitude_difference_mps=float(abs(ve-va)),relative_vx_mps=float(velrel[0]),relative_vy_mps=float(velrel[1]),radial_sep_rate_mps=float(radial),sigma_static_long_m=float(sx),sigma_dynamic_long_m=float(sv),sigma_lateral_m=float(sy),gate=float(gate),gate_logit=float(arg),static=float(stat),dynamic=float(dyn),total=float(stat+dyn),actor_yaw_rad=float(a.psi_rad),actor_velocity_tangent_rad=float(heading_tangent),yaw_minus_velocity_dir_rad=float(theta_d),ego_x=float(ego.x),ego_y=float(ego.y),ego_yaw=float(ego.psi_rad),actor_x=float(a.x),actor_y=float(a.y),actor_length_m=float(a.length),actor_width_m=float(a.width)))
    for z in local:
        z['sum_actor_total']=sum(r['total'] for r in local)
        z['max_actor_total']=max(r['total'] for r in local)
    T.extend(local)
R=pd.DataFrame(T)
R.to_csv(OUT/'results'/'v0star_actor_components_0p5s.csv',index=False)
peaks=R.groupby('frame_id')['total'].sum(); fmax=int(peaks.idxmax())
summary={'v0star_peak_frame':fmax,'v0star_peak_t_s':(fmax-2820)/10,'v0star_peak_sum':float(peaks.max()),'per_actor_peak':R[R.frame_id==fmax][['actor_id','static','dynamic','total','poly_gap_m','local_forward_m','local_lateral_m','sigma_dynamic_long_m','sigma_lateral_m','gate','radial_sep_rate_mps','actor_speed_mps','ego_speed_mps']].to_dict(orient='records'),'nearest_at_t_2p5':R[R.frame_id==2845][['actor_id','poly_gap_m','total','static','dynamic','local_forward_m','local_lateral_m']].to_dict(orient='records'),'not_frozen_v0':True}
(OUT/'results'/'v0star_anomaly_attribution.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(summary,indent=2))
# Equal coordinate ratio, constant colorbar within V0* panels for 2.5 /4.5.
fig,axes=plt.subplots(2,3,figsize=(15,10),constrained_layout=True)
X,Y=np.meshgrid(np.linspace(990,1013,230),np.linspace(987,1015,280))
M={}
for row,frame in enumerate([2845,2865]):
 ego=DF[(DF.track_id==70)&(DF.frame_id==frame)].iloc[0];ve=np.hypot(ego.vx,ego.vy)
 S=np.zeros_like(X);D=np.zeros_like(X)
 for ident in (71,72,73):
  a=DF[(DF.track_id==ident)&(DF.frame_id==frame)].iloc[0];va=np.hypot(a.vx,a.vy)
  s,d=v0_components(X,Y,a.x,a.y,a.psi_rad,a.length,a.width,va,ve);S+=s;D+=d
 M[(row,0)]=S;M[(row,1)]=D;M[(row,2)]=S+D
for col,label in enumerate(['Static','Dynamic','Total']):
 vmax=max(M[(0,col)].max(),M[(1,col)].max())
 for row,frame in enumerate([2845,2865]):
  ax=axes[row,col];im=ax.imshow(M[(row,col)],extent=(990,1013,987,1015),origin='lower',cmap='jet',vmin=0,vmax=vmax,aspect='equal')
  for id,color in [(70,'black'),(71,'white'),(72,'cyan'),(73,'magenta')]:
   v=DF[(DF.track_id==id)&(DF.frame_id==frame)].iloc[0]
   coords=np.array(poly(v).exterior.coords)
   ax.add_patch(Polygon(coords,closed=True,fill=False,edgecolor=color,linewidth=2 if id==70 else 1.5))
   ax.arrow(v.x,v.y,v.vx*.6,v.vy*.6,color=color,width=.03,head_width=.25,length_includes_head=True)
   ax.text(v.x+.2,v.y+.25,str(id),color=color,weight='bold',fontsize=9)
  ax.plot([DF[(DF.track_id==70)&(DF.frame_id==frame)].iloc[0].x],[DF[(DF.track_id==70)&(DF.frame_id==frame)].iloc[0].y],'kx',ms=5)
  ax.set_xlim(990,1013);ax.set_ylim(987,1015);ax.set_aspect('equal',adjustable='box');ax.set_title(f't={(frame-2820)/10:.1f}s | {label} | unverified V0*')
  fig.colorbar(im,ax=ax,shrink=.55)
fig.savefig(OUT/'figures'/'v0star_2p5_vs_4p5_components.png',dpi=150)
plt.close(fig)
# Per-actor time breakdown
fig,ax=plt.subplots(figsize=(11,5.2),constrained_layout=True)
for id in (71,72,73):
 v=R[R.actor_id==id];ax.plot(v.t_s,v.total,'o-',label=f'Actor {id} | total')
ax.plot(R[R.actor_id==71].t_s,R[R.actor_id==71].sum_actor_total,'k--',lw=1.3,label='Actor SUM')
ax.set_xlabel('Seconds since frame2820');ax.set_ylabel('Raw V0* at Ego center');ax.set_title('Actor contributions: not frozen V0, logged real positions');ax.legend();ax.grid(alpha=.25)
fig.savefig(OUT/'figures'/'v0star_actor_risk_by_time.png',dpi=160);plt.close(fig)
