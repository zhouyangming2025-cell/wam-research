#!/usr/bin/env python3
"""Small candidate-trajectory risk-field audit, NOT a paper/system reproduction.

Inputs: INTERACTION recorded sample with header track_id,frame_id,...
Methods: reconstructed V0 single-actor scalar-speed kernel (unverified parity),
         Wu et al. 2024 Eq(7)-(9) single logged-mode time-sliced Gaussian,
         time-synchronous full-rectangle distance (independent geometric oracle).
Offline logged futures are privileged and must not be advertised as deployment predictions.
No TRTP/DRF/RSS/SimWAM replication or benchmark training is performed.
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from shapely.geometry import Polygon as ShapelyPolygon

PAPER_WU = 'https://arxiv.org/html/2404.00893v1'
REAL_DATA = 'https://github.com/SCP-CN-001/trajectory_dataset_support'
REAL_BLOB = 'f15a96fd2000b198e4719c38054098abf577c917'


def v0_components(qx,qy,ax,ay,yaw,L,W,v_a,v_e):
    """Hand-off formula port; center query; NOT bitwise official V0.
    Width, length, scalar actor & ego SPEED (magnitude), NOT projected longitudinal.
    """
    dx=np.asarray(qx)-ax;dy=np.asarray(qy)-ay
    fx=dx*np.cos(yaw)+dy*np.sin(yaw)
    fy=-dx*np.sin(yaw)+dy*np.cos(yaw)
    sx=1.5*L+0.001; sy=W+0.001
    sv=6.0*abs(v_a-v_e)+0.001
    d=-1.0 if v_a>v_e else 1.0
    stat=np.exp(-((fx/sx)**2+(fy/sy)**2))
    gate=1.0/(1.0+np.exp(np.clip(d*(fx-0.9*L*d),-60,60)))
    dyn=np.exp(-((fx/sv)**2+(fy/sy)**2))*gate
    return stat,dyn


def wu_kernel(qx,qy,ax,ay,yaw,a=6.,b=2.):
    """Wu et al 2024 Eq7 & Eq8, ONE future trajectory p=1, not TRTP."""
    dx=np.asarray(qx)-ax;dy=np.asarray(qy)-ay
    fx=dx*np.cos(yaw)+dy*np.sin(yaw)
    fy=-dx*np.sin(yaw)+dy*np.cos(yaw)
    return np.exp(-((fx/a)**2+(fy/b)**2))


def poly(row):
    x,y,th,L,W=[float(row[k]) for k in ('x','y','psi_rad','length','width')]
    cs=np.cos(th);sn=np.sin(th)
    basis=np.array([[cs,-sn],[sn,cs]])
    local=np.array([[L/2,W/2],[L/2,-W/2],[-L/2,-W/2],[-L/2,W/2]])
    return ShapelyPolygon(local@basis.T+[x,y])


def offset_ego(ego,amount):
    e=ego.copy()
    e['x']=ego['x']-amount*np.sin(ego['psi_rad'])
    e['y']=ego['y']+amount*np.cos(ego['psi_rad'])
    return e


def plot_vehicle(ax,row,edge,alpha=.9,lw=1.5):
    p=poly(row)
    q=np.array(p.exterior.coords)
    ax.add_patch(Polygon(q,closed=True,fill=False,edgecolor=edge,linewidth=lw,alpha=alpha))


def compute_records(df,offsets=(-1.,0.,1.),gamma=.95,a=6.,b=2.):
    piv={i:g.sort_values('frame_id').reset_index(drop=True) for i,g in df.groupby('track_id')}
    assert 70 in piv and 72 in piv and len(piv[70])==13
    frames=piv[70]['frame_id'].to_numpy().tolist()
    assert np.allclose(np.diff(frames),5)
    results=[]
    for off in offsets:
        for idx,frame in enumerate(frames):
            e0=piv[70].iloc[idx]
            e=offset_ego(e0,off)
            ve=float(np.hypot(e0.vx,e0.vy))
            static=dynamic=wu=0.
            min_d=np.inf;min_actor=None
            for ident in [71,72,73]:
                arow=piv[ident].iloc[idx]
                va=float(np.hypot(arow.vx,arow.vy))
                s,d=v0_components(e.x,e.y,arow.x,arow.y,arow.psi_rad,arow.length,arow.width,va,ve)
                static+=float(s);dynamic+=float(d)
                wu+=float(wu_kernel(e.x,e.y,arow.x,arow.y,arow.psi_rad,a,b))
                gap=poly(e).distance(poly(arow))
                if gap<min_d:
                    min_d=gap;min_actor=ident
            results.append(dict(offset_m=off,time_s=idx*.5,frame_id=frame,v0_static=static,v0_dynamic=dynamic,v0_total=static+dynamic,wu_field=gamma**idx*wu,geom_gap_m=min_d,nearest_actor=min_actor))
    return pd.DataFrame(results)


def real_risk_maps(df,output, gamma=.95,a=6.,b=2.):
    p={i:g.set_index('frame_id') for i,g in df.groupby('track_id')}
    frames=[2820,2840,2860]
    gridx=np.linspace(990,1015,131); gridy=np.linspace(987,1015,145)
    gx,gy=np.meshgrid(gridx,gridy)
    fig,axes=plt.subplots(2,3,figsize=(13.2,9),constrained_layout=True)
    maxvals=[0.,0.]
    arrays=[]
    for row,kind in enumerate(('V0 formula port','Wu 2024 Eq7-9')):
        for col,frame in enumerate(frames):
            ego=p[70].loc[frame];ve=np.hypot(ego.vx,ego.vy)
            tot=np.zeros_like(gx)
            for actor in (71,72,73):
                r=p[actor].loc[frame];va=np.hypot(r.vx,r.vy)
                if row==0:
                    st,dy=v0_components(gx,gy,r.x,r.y,r.psi_rad,r.length,r.width,va,ve);tot+=st+dy
                else:
                    tot+=gamma**((frame-2820)//5)*wu_kernel(gx,gy,r.x,r.y,r.psi_rad,a,b)
            arrays.append((row,col,frame,tot))
            maxvals[row]=max(maxvals[row],float(np.nanmax(tot)))
    for row,col,frame,arr in arrays:
        ax=axes[row,col]
        # Per-method fixed value scale across time; V0 vs Wu numerical scales not calibrated comparable.
        im=ax.imshow(arr,extent=(gridx[0],gridx[-1],gridy[0],gridy[-1]),origin='lower',cmap='jet',vmin=0,vmax=maxvals[row],aspect='equal')
        for actor in (71,72,73):plot_vehicle(ax,p[actor].loc[frame], 'white', lw=1.4)
        plot_vehicle(ax,p[70].loc[frame],'black',lw=2.5)
        ax.plot(p[70].loc[2820:2880,'x'].values,p[70].loc[2820:2880,'y'].values,'k--',lw=.9,alpha=.75)
        ax.set_title(f'{"V0 approximate" if row==0 else "Wu time-sliced"}  t={(frame-2820)/10:.1f}s',fontsize=10)
        ax.set_xlim(990,1015);ax.set_ylim(987,1015);ax.set_xlabel('world x (m)')
        if col==0:ax.set_ylabel('world y (m)')
        if col==2:
            fig.colorbar(im,ax=axes[row,:],orientation='horizontal',fraction=.04,pad=.07,label=('V0 score (unscaled)' if row==0 else 'Wu weighted field (unscaled)'))
    fig.suptitle('INTERACTION sample / logs t0=282 s; black: logged Ego #70; white: logged actors (GT-future oracle)',fontsize=12)
    fig.savefig(output,dpi=160)
    plt.close(fig)


def trend_chart(scores,out):
    fig,ax=plt.subplots(figsize=(10,5),constrained_layout=True)
    actual=scores.loc[scores.offset_m==0]
    ax.plot(actual.time_s,actual.v0_total,'o-',label='V0 formula port: score')
    ax.plot(actual.time_s,actual.wu_field,'s-',label='Wu time layer score (GT future)')
    ax.set_xlabel('Time from t0 (s)');ax.set_ylabel('Raw risk scores (not calibrated)')
    ax2=ax.twinx();ax2.plot(actual.time_s,actual.geom_gap_m,'^--',label='Polygon min gap (m)')
    ax2.set_ylabel('Full-footprint gap (m)')
    h,l=ax.get_legend_handles_labels();h2,l2=ax2.get_legend_handles_labels();ax.legend(h+h2,l+l2,fontsize=9)
    ax.grid(True,alpha=.2)
    ax.set_title('Recorded Ego and actors: synchronous trajectory-level risk / gap (oracle future)')
    fig.savefig(out,dpi=160);plt.close(fig)


def control_test():
    # Synthetic, diagnostic only; NOT a high-level validity/quality label.
    yaw0=sum(v0_components(-10,0,0,0,0,.4,.3,0,8))
    yaw90=sum(v0_components(-10,0,0,0,np.pi/2,.4,.3,0,8))
    # For collision test, Ego 5mx2m front edge at x=2.5; tiny cone inside footprint x=2.45.
    ego={'x':0,'y':0,'psi_rad':0,'length':5.,'width':2.}
    cone={'x':2.45,'y':0.,'psi_rad':.9,'length':.15,'width':.15}
    zero_point=sum(v0_components(0.,0.,cone['x'],cone['y'],cone['psi_rad'],cone['length'],cone['width'],0,0))
    true_gap=poly(ego).distance(poly(cone))
    # 2D physically synchronized spot crossing, circles radius .2, same spatial paths.
    t=np.arange(0,6.001,.01)
    ex=np.clip(t-2,-2,2)
    sy=np.clip(t-2,-2,2);ay=np.clip(t-4,-2,2)
    sync=np.hypot(ex,sy);async_d=np.hypot(ex,ay)
    # Crossing: actor orientation +y; score uses actual same-time position.
    risk_sync=np.exp(-(ex/2.)**2-(sy/.75)**2)
    risk_delayed=np.exp(-(ex/2.)**2-(ay/.75)**2)
    return dict(cross_sync_peak_wu=float(risk_sync.max()),cross_shift_peak_wu=float(risk_delayed.max()),cone_yaw0_v0=float(yaw0),cone_yaw90_v0=float(yaw90),yaw_difference=float(abs(yaw0-yaw90)),small_target_ego_center_score=float(zero_point),small_target_polygon_gap=float(true_gap),cross_sync_min_center_m=float(sync.min()),cross_shift_min_center_m=float(async_d.min()),same_speed_opposite_abs_speed_diff=0.,same_speed_opposite_relative_vector_speed=20.,brake_req_vclose2_gap20=2**2/(2*20),brake_req_vclose2_gap10=2**2/(2*10))


def controlled_plot(out):
    xx=np.linspace(-15,15,180); yy=np.linspace(-15,15,180); x,y=np.meshgrid(xx,yy)
    s0,d0=v0_components(x,y,0,0,0,.4,.3,0,8)
    s1,d1=v0_components(x,y,0,0,np.pi/2,.4,.3,0,8)
    t=np.arange(0,6.001,.01); ex=np.clip(t-2,-2,2); sy=np.clip(t-2,-2,2); ay=np.clip(t-4,-2,2)
    rs=np.exp(-(ex/2.)**2-(sy/.75)**2); rd=np.exp(-(ex/2.)**2-(ay/.75)**2)
    fig,axs=plt.subplots(2,2,figsize=(10,8),constrained_layout=True)
    for ax,zz,label in [(axs[0,0],s0+d0,"Cone yaw=0: reconstructed V0"),(axs[0,1],s1+d1,"Cone yaw=90 deg: SAME physical cone")]:
        im=ax.imshow(zz,extent=(-15,15,-15,15),origin='lower',vmin=0,vmax=1,cmap='jet')
        ax.plot([-10],[0],'wx',markersize=9)
        ax.set_title(label);ax.set_xlabel('relative x (m)');ax.set_ylabel('relative y (m)')
    fig.colorbar(im,ax=axs[0,:],orientation='horizontal',fraction=.045,pad=.08,label='V0 raw scalar risk, same scale')
    axs[1,0].plot(t,np.hypot(ex,sy),label='same-time crossing')
    axs[1,0].plot(t,np.hypot(ex,ay),label='delayed actor 2s')
    axs[1,0].axhline(.4,linestyle='--',label='sum of circle radii 0.4 m')
    axs[1,0].set_xlabel('t(s)');axs[1,0].set_ylabel('center distance (m)');axs[1,0].legend(fontsize=8);axs[1,0].set_title('Intersection: synchronous geometry')
    axs[1,1].plot(t,rs,label='Wu time-slice, simultaneous')
    axs[1,1].plot(t,rd,label='Wu time-slice, delayed')
    axs[1,1].set_xlabel('t(s)');axs[1,1].set_ylabel('unscaled field query');axs[1,1].legend(fontsize=8);axs[1,1].set_title('Time-slice response (a=2,b=.75)')
    fig.savefig(out,dpi=160);plt.close(fig)

def main():
    pa=argparse.ArgumentParser();pa.add_argument('--csv',required=True);pa.add_argument('--out',default='risk_pilot_output');a=pa.parse_args()
    folder=Path(a.out);folder.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(a.csv)
    df=df.loc[df.track_id.isin([70,71,72,73]) & df.frame_id.between(2820,2880) & ((df.frame_id-2820)%5==0)].copy()
    expected={70,71,72,73}
    assert set(df.track_id)==expected and len(df)==52 and df.frame_id.min()==2820 and df.frame_id.max()==2880
    raw=compute_records(df)
    raw.to_csv(folder/'real_trajectory_time_series.csv',index=False)
    sumdf=raw.groupby('offset_m').agg(v0_mean=('v0_total','mean'),v0_peak=('v0_total','max'),wu_mean=('wu_field','mean'),wu_peak=('wu_field','max'),geometry_min_gap_m=('geom_gap_m','min'),time_of_min_gap_s=('time_s',lambda s: float(raw.loc[s.index[np.argmin(raw.loc[s.index,'geom_gap_m'].values)],'time_s']))).reset_index()
    sumdf.to_csv(folder/'real_candidate_summary.csv',index=False)
    real_risk_maps(df,folder/'real_interaction_six_panels.png')
    trend_chart(raw,folder/'real_risk_vs_gap.png')
    controlled_plot(folder/'controlled_yaw_and_time.png')
    import json
    with open(folder/'controlled_diagnostics.json','w') as f: json.dump(control_test(),f,indent=2)
    print('SRC',REAL_DATA,REAL_BLOB)
    print('SCORES\n'+sumdf.to_string(index=False,float_format=lambda x:f'{x:.6f}'))
    print('CONTROLLED',json.dumps(control_test(),indent=2))

if __name__=='__main__':main()
