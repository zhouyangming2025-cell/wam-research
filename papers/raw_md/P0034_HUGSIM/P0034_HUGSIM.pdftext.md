# P0034_HUGSIM - PDF text extraction

> Source PDF: `papers/pdf/P0034_HUGSIM.pdf`
> Conversion: Poppler `pdftotext -layout -enc UTF-8`
> Note: layout-preserving text extraction; the PDF remains the source of truth for figures, exact equations, and wording.

---

                                                                                                                                                                                          1




                                             HUGSIM: A Real-Time, Photo-Realistic and
                                            Closed-Loop Simulator for Autonomous Driving
                                        Hongyu Zhou                 Longzhong Lin   Jiabao Wang     Yichong Lu      Dongfeng Bai                                          Bingbing Liu
                                                                            Yue Wang     Andreas Geiger    Yiyi Liao

                                              Abstract—In the past few decades, autonomous driving algorithms have made significant progress in perception, planning, and control.
                                              However, evaluating individual components does not fully reflect the performance of entire systems, highlighting the need for more
                                              holistic assessment methods. This motivates the development of HUGSIM, a closed-loop, photo-realistic, and real-time simulator for
                                              evaluating autonomous driving algorithms. We achieve this by lifting captured 2D RGB images into the 3D space via 3D Gaussian
                                              Splatting, improving the rendering quality for closed-loop scenarios, and building the closed-loop environment. In terms of rendering, We
arXiv:2412.01718v1 [cs.CV] 2 Dec 2024




                                              tackle challenges of novel view synthesis in closed-loop scenarios, including viewpoint extrapolation and 360-degree vehicle rendering.
                                              Beyond novel view synthesis, HUGSIM further enables the full closed simulation loop, dynamically updating the ego and actor states and
                                              observations based on control commands. Moreover, HUGSIM offers a comprehensive benchmark across more than 70 sequences
                                              from KITTI-360, Waymo, nuScenes, and PandaSet, along with over 400 varying scenarios, providing a fair and realistic evaluation
                                              platform for existing autonomous driving algorithms. HUGSIM not only serves as an intuitive evaluation benchmark but also unlocks the
                                              potential for fine-tuning autonomous driving algorithms in a photorealistic closed-loop setting.

                                              Index Terms—Gaussian Splatting, Holistic Understanding, Dynamic Urban Scenes, Simulator, Autonomous Driving

                                                                                                                       ✦

                                        1    I NTRODUCTION


                                        V     ISION -based autonomous driving (AD) offers a promis-
                                              ing route to achieving full autonomy at low cost.
                                        Nonetheless, rigorously testing a vision-based AD system
                                                                                                                           resulting in video-game-style simulators. Although these
                                                                                                                           simulators provide numerous features for testing and train-
                                                                                                                           ing AD algorithms, significant domain gaps still exist be-
                                        in real-world environments poses significant challenges, pri-                      tween the real world and video games. Another downside
                                        marily due to safety concerns and the inherent inefficiencies                      of these simulators is the considerable time and manpower
                                        of such evaluations. Moreover, the risk associated with as-                        investment in manually creating assets and scenarios.
                                        sessing safety-critical scenarios in real settings is substantial,                     In this paper, we bridge the gap between real-world
                                        yet these situations are precisely where AD algorithms must                        evaluation and simulation by building a novel photorealistic
                                        demonstrate their reliability and effectiveness.                                   AD simulator leveraging advanced novel view synthesis
                                            Existing methods [8], [26], [44], [58], [69] primarily assess                  techniques. Although many previous works [39], [70], [83],
                                        vision-based AD algorithms using collected datasets, offer-                        [84] tackle novel view synthesis of urban scenes, there re-
                                        ing open-loop evaluations of specific components like per-                         mains a significant gap between urban novel view synthesis
                                        ception and planning. However, this approach falls short of                        and an AD simulator.
                                        capturing closed-loop performance [15], [16], [17], as it eval-                        First, a closed-loop simulator with interactive actors
                                        uates AD algorithms solely in pre-collected, safe and normal                       poses new challenges for the rendering process: 1) The
                                        driving environments conducted by experienced drivers.                             trajectories of dynamic objects are originally observed from
                                        This limitation underscores the urgent need for advanced                           discrete timestamps, whereas a closed-loop simulator re-
                                        simulators capable of conducting closed-loop evaluations of                        quires continuous trajectories. 2) Unlike typical novel view
                                        vision-based AD systems, enabling the safe exploration of                          synthesis tasks, which evaluate on interpolated views, sim-
                                        out-of-domain and safety-critical scenarios.                                       ulators require photo-realistic rendering even for extrapo-
                                            To tackle this issue, closed-loop AD simulators have                           lated views, especially for lane areas. 3) Since actors are
                                        been investigated. Some studies [9], [27], [66] implement                          observed under unpredictable viewpoints due to the inter-
                                        a closed-loop system for planning and control, assuming                            action between the ego vehicle and the actors, we should
                                        ground truth perception results are available, neglecting                          ensure that actors appear realistic from 360-degree view-
                                        the importance of perception. Other works [19], [42] offer                         points. Moreover, there are extra implementation steps for
                                        an end-to-end closed-loop system based on game engines,                            building a full-fledged closed-loop simulator. For instance,
                                                                                                                           a communication bridge between the simulator and AD
                                        •   H. Zhou, L. Lin, J. Wang, Y. Lu, Y. Wang and Y. Liao are affiliated with       algorithms is necessary; waypoints retrieved from AD algo-
                                            Zhejiang University, China.                                                    rithms must be converted into control commands to update
                                        •   D. Bai and B, Liu are affiliated with Huawei, China.                           the ego vehicle’s position and actor trajectories need to be
                                        •   A. Geiger is affiliated with the Autonomous Vision Group, University of
                                            Tübingen and Tübingen AI Center, Germany.                                    generated efficiently.
                                        •   Corresponding author: Yiyi Liao                                                    Recently, a concurrent work called NeuroNCAP [45]
                                        •   E-mails: hongyu zhou@zju.edu.cn, yiyi.liao@zju.edu.cn                          introduced, to the best of our knowledge, the first publicly
                                        •   Project Page: https://xdimlab.github.io/HUGSIM
                                                                                                                           available photorealistic closed-loop simulator that offers
                                                                                                                                   2


            Reconstruction                                       Closed-Loop Simulator                     Benchmark
KITTI-360




                                       Easy
Waymo




                                                                                                                Evaluation




                                       Medium
Nuscence




                                       Hard/Extreme
Pandaset




                                                                                                          Closed-Loop Challenges


Fig. 1: Overview of HUGSIM. We propose HUGSIM, a photorealistic closed-loop simulator for AD, supporting a variety
of scenes from different datasets and scenarios with varying levels of difficulty. HUGSIM also provides a closed-loop
benchmark and presents challenges for existing AD algorithms.
high-fidelity rendering. However, NeuroNCAP is not specif-       PandaSet [69]. To fairly evaluate different AD algorithms,
ically designed to address the challenges of viewpoint ex-       we propose an evaluation metric named HD-Score, inspired
trapolation, 360-degree high-fidelity actor rendering, or the    by NAVSIM [18] and DriveArena [73]. The HD-Score reflects
efficient simulation of interactive safety-critical scenarios.   AD performance based on N C (No Collision), DAC (Driv-
    In this paper, we propose HUGSIM, a novel vision-based       able Area Compliance), T T C (Time to Collision), COM
AD simulator to address the aforementioned challenges,           (Comfort), and Rc (Route Completion).
see Fig. 1. We start by extending 3D Gaussian Splatting             We summarize the contributions of this paper as follows:
(3DGS) [37] to model dynamic 3D scenes with multiple                 •   We present a novel simulator for autonomous
modalities, from RGB images and noisy 2D and 3D predic-                  driving, characterized by being closed-loop, photo-
tions. This approach enables holistic scene reconstruction,              realistic, and real-time, bridging the gap between
including appearance, semantics, flow, depth, and motion                 urban scene novel view synthesis and autonomous
of rigidly moving objects. Note that semantic information                driving simulators.
is essential for collision detection, while flow and depth           •   To address the specific rendering challenges in the
can be helpful for AD algorithms [82]. Importantly, we                   simulator, we leverage physical constraints and non-
apply physical constraints to both dynamic vehicles and                  native actors to improve fidelity, surpassing previous
the ground to enhance rendering quality. Specifically, we                novel view synthesis approaches.
regularize the trajectory of dynamic vehicles using a uni-           •   We propose an efficient actor trajectory generation
cycle model, allowing for improving the rendering quality                strategy, enabling the simulation of aggressive driv-
of dynamic vehicles given noisy 3D bounding box predic-                  ing behaviors even without HD maps.
tions. We further introduce a multi-plane ground model to            •   We introduce a new benchmark for fair evaluation of
address lane distortion in extrapolated views, which works               AD algorithms, offering more photorealistic simula-
across different types of ground, including sloped surfaces.             tion environments compared to existing closed-loop
In addition, we insert non-native actors reconstructed from              vision-based AD simulators. Additionally, the bench-
3DRealCar [20], ensuring both faithful geometry and ap-                  mark provides a variety of scenes built upon multiple
pearance from arbitrary observation views, in contrast to                datasets, with varying scenarios with different levels
partially observed native vehicles in typical driving scenes.            of difficulty.
Moreover, we close the simulation loop by querying way-
points from AD algorithms, applying a linear quadratic               This journal paper is an extension of a conference pa-
regulator (LQR) for control, extracting the multiple ground      per published at CVPR 2024, HUGS [83]. In comparison
planes, and updating the pose of ego vehicles and actors.        to HUGS, we 1) extend the novel view synthesis task by
By leveraging HD maps, we deploy the Intelligent Driver          constructing a closed-loop simulator; 2) design an efficient
Model (IDM) planning strategy [62] to simulate normal ac-        strategy for simulating safety-critical scenarios without re-
tor behavior. To simulate safety-critical scenarios, we design   lying on HD maps; 3) propose a multi-plane ground Gaus-
an attack planning strategy to generate aggressive actor         sian model and real captured vehicle models to enhance
behavior, which works effectively even in scenes without         appearance fidelity; 4) introduce a novel benchmark for fair
HD maps.                                                         evaluation of vision-based AD algorithms.
    Additionally, we encapsulate the entire scene into an
interactive closed-loop simulator and provide Gymnasium          2   R ELATED W ORK
APIs [6] to facilitate AD evaluation and the potential ap-       In this section, we first review methods in urban scene
plication of reinforcement learning in our simulator. Our        reconstruction, a core task for enabling AD simulators. Then
simulator operates in real-time, as it introduces minimal        we discuss existing datasets, benchmarks and simulators
computational overhead compared to 3DGS. It supports             used for training or evaluating AD algorithms. We compare
scenes from KITTI-360 [44], Waymo [58], nuScenes [8], and        various features of representative relative work in Table 1.
                                                                                                                               3

                            Closed-Loop RGB MV-Consistency P-Realistic FV-Actors IA-Actors Ext-Views Real-Time
      MARS [68]                  ✘       ✔       ✔             ✔          ✘          ✘         ✘         ✘
      StreetGaussian [70]        ✘       ✔       ✔             ✔          ✘          ✘         ✘         ✔
      KITTI [26]                 ✘       ✔       ✔             ✔          ✘          ✘         ✘         ✔
      NAVSIM [18]                ✘
                                 ✔       ✔       ✔             ✔          ✘          ✘         ✘         ✔
      nuplan [9]                 ✔       ✘       ✘             ✘          ✘         ✔          ✘         ✔
      Carla [19]                 ✔       ✔       ✔             ✘          ✔         ✔          ✔         ✔
      NeuroNCAP [45]             ✔       ✔       ✔             ✔          ✘          ✘         ✘         ✘
      DriveArena [73]            ✔       ✔       ✘             ✔          ✔         ✔          ✔         ✘
      HUGSIM (Ours)              ✔       ✔       ✔             ✔          ✔         ✔          ✔         ✔

TABLE 1: Comparison of Related Work, including autonomous driving-related reconstruction methods ,
 open-loop benchmarks , and closed-loop benchmarks . We compare various features like closed-loop evaluation (Closed-
Loop), RGB images (RGB), multi-view image consistency (MV-Consistency), photo-realistic rendering (P-Realistic), full-
view actors (FV-Actors), interactive actors (IA-Actors), fidelity of extrapolated views (Ext-Views), and real-time simulation
(Real-Time) capabilities. Note that only one representative work is shown for overlapping features.
2.1   Urban Scene Reconstruction                                 on the lanes are common. Some methods, such as [64],
                                                                 [77], leverage diffusion models to add additional views for
Static Scenes: Numerous studies have been conducted              supervision, addressing the problem of sparse input views
to reconstruct urban scenes using various methods. These         in urban scene reconstruction. However, diffusion models
methods can be categorized into four classes: point-based        introduce challenges such as inconsistency between views,
[1], [55], mesh-based [24], [40], NeRF-based [28], [46], [47],   increased training complexity, and a slowdown in training
[49], [53], [59], [67], [80] and 3DGS-based [29], [41], [56].    speed due to the heavy computational burden of these
While point-based and mesh-based methods demonstrate             models. GGS [29] presents a generalizable model based
faithful reconstructions, they struggle to recover all aspects   on MVSplat [11], incorporating a virtual lane generation
of the scene, especially when it comes to high-quality ap-       strategy during training to address the extrapolated view
pearance modeling. In contrast, NeRF-based models not            problem. While this approach significantly improves fidelity
only reconstruct scene appearance but also enable high-          in extrapolated views, MVSplat allows only a few frames
quality rendering from novel viewpoints, while 3DGS-based        as input, which may restrict scalability and lead to multi-
models support real-time rendering without sacrificing           view misalignment. In comparison, the concurrent works
quality. However, these approaches are primarily designed        AutoSplat [38] and RoGS [21] apply physical priors to
for static scenes, lacking the ability to handle dynamic urban   constrain ground Gaussians, similar to our approach. How-
environments. In this study, our focus lies in addressing the    ever, AutoSplat relies on LiDAR data for initialization, and
challenges of dynamic urban scenes.                              RoGS uniformly distributes Gaussians across the ground
                                                                 plane, with both approaches fixing Gaussian positions on
Dynamic Scenes: Several methods have also been devel-            the plane. These methods use a large number of Gaussians
oped to address the reconstruction of dynamic urban scenes.      to model non-textured areas, which we find unnecessary
Many of these approaches rely on the availability of accurate    and inefficient. By optimizing additional parameters such
3D bounding boxes for moving objects in order to separate        as position and scale, HUGSIM achieves better performance
the dynamic elements from the static components, as seen         without requiring as many Gaussians.
in [22], [52], [61], [68], [74], [84]. PNF [39], NeuRAD [61]         The related work mentioned above primarily focus on
and StreetGaussians [70] takes a different approach by lever-    novel view synthesis but still fall short of being fully devel-
aging monocular-based or LiDAR-based 3D bounding box             oped closed-loop simulator, as shown in Table 1.
predictions and proposes a joint optimization of object poses
during the reconstruction process. However, our experimen-
tal observations indicate that the straightforward optimiza-     2.2   Benchmarks
tion of object poses yields unsatisfactory results due to the
absence of physical constraints. Another method, SUDS [63],      Open-Loop: Most existing datasets and benchmarks [8],
avoids the use of 3D bounding boxes by grouping the scene        [26], [44], [58], [69] for AD algorithms follow an open-
based on learned feature fields. However, the accuracy of        loop approach, evaluating individual components of the
this approach lags behind. In parallel, EmerNeRF [71] and        algorithms separately. For instance, in the perception com-
PVG [12] follows a similar idea to SUDS by decomposing           ponent, tasks such as semantic segmentation, bounding
the scene purely into static and dynamic components. In          box detection, and lane detection are assessed, while the
our research, we have the capability to further decompose        planning component evaluates tasks like route planning,
individual dynamic objects within the scene and estimate         behavior prediction, and trajectory prediction. Although
their motion. This reconstructed motion can then be used to      these open-loop benchmarks provide detailed and convinc-
simulate driving behavior within the simulator.                  ing performance evaluations of each part, they evaluate the
                                                                 performance of AD algorithms using sensory data collected
Extrapolated View Rendering: Although the urban re-              by experts, lacking scenarios deviated from the expert-
construction methods mentioned above can render high-            collected sensory data. Without closed-loop feedback, the
fidelity images in interpolated views, most struggle with        long-term consequences of these deviations remain unex-
rendering in extrapolated views, where artifacts particularly    plored, which could be critical for understanding the ro-
                                                                                                                                                                         4


                    Scene Reconstruction                                                           Closed-Loop Simulation
                                                                                         Affine
                                                                                       Transform
                                                             concat          Render
                                                                                                                                                     Gymnasium API

    Appearance
                                                                                                                                                    Collision Detector
                                                                             Render

                                                                                                                                                       Benchmark
     Semantic
                        Native         Non-Native            Recon/Gen       Render
                       Vehicles         Vehicles             Trajectories

                                  Dynamic Gaussians
      Flow
                                                                             Render                                                                  AD Algorithms


                                                                                                                                 LQR
                                                                            Ego Pose
      Depth                       Multi-Plane Ground Model
 Static Gaussians                 Ground Gaussians                                             Ground Plane & Control Command              Predicted Waypoints


Fig. 2: The Pipeline of HUGSIM. We reconstruct urban scenes by disentangling them as ground, non-ground static
background, and dynamic objects, while also enabling multi-modal rendering. Subsequently, we implement a closed-loop
simulator based on the reconstructed results, providing a benchmark for evaluating autonomous driving algorithms.
bustness and safety of AD systems in real-world conditions.                 tion, designed to address rendering challenges in vision-
NAVSIM [18] provides a benchmark positioned between                         based AD simulation. Next, we describe our holistic urban
open-loop and closed-loop evaluations. Although it is a non-                Gaussian splatting approach, covering appearance, seman-
reactive simulator and lacks the capability for novel view                  tics, optical flow, and depth. Finally, we detail the loss
synthesis, it computes closed-loop metrics by forecasting                   functions employed in our scene reconstruction.
the planning trajectory for a few seconds into the future.
However, NAVSIM is limited to short time horizons and
                                                                            3.1   Preliminaries
does not address how accumulated deviations over time
impact driving safety.                                                      3D Gaussian Splatting: 3DGS [37] represents scenes us-
Closed-Loop: A number of closed-loop simulators have at-                    ing a set of anisotropic 3D Gaussians with differentiable
tempted to address the limitations of open-loop benchmarks                  properties, allowing for efficient image rendering through
in autonomous driving. Some simulators [9], [27], [66] pro-                 tile-based rasterization. Each 3D Gaussian is defined by its
vide ground-truth positions and rotations of other vehicles,                position µ, rotation R (also represented as quaternion q
lacking the perception aspect of the AD system, which is                    during training), scale S (comprising sx , sy , sz ), opacity α,
crucial for a comprehensive evaluation. Other works [19],                   and spherical harmonic coefficient SH . The 3D covariance
[42] use game engines to create simulators, offering high                   matrix Σ ∈ R3×3 of each Gaussian is defined as:
edit-ability but often lacking photorealism and requiring
                                                                                                             Σ = RSS T RT                                            (1)
extensive manual design of scenes, making them costly and
less scalable. Rapid advances in video diffusion models                     A 3D Gaussian is defined as follow:
[25], [31], [65], [72] have shown promise in generating                                           
                                                                                                     1
                                                                                                                       
photorealistic driving videos. DriveArena [73] uses a video                        G(x) = α exp − (x − µ)T Σ−1 (x − µ)                                               (2)
                                                                                                     2
diffusion model to build a closed-loop simulator, controlling
scene generation through scene layouts. However, these                          The color c of each Gaussian can be computed based on
models still suffer from issues like temporal inconsistency                 the view direction and its corresponding spherical harmon-
and significant computational demands. UniSim [74] and                      ics (SH ). Given a set of sorted 3D Gaussians N along the
NeuroNcap [45] takes a different approach by creating a                     ray, we obtain the accumulated color via volume rendering:
NeRF-based simulator that enables photorealistic, closed-                                                                       i−1
loop simulations. However, UniSim is not an open-source
                                                                                                                 X              Y
                                                                                                   π:    C=            ci αi′          (1 − αj′ )                    (3)
work, while NeuroNCAP has several shortcomings, includ-                                                          i∈N            j=1
ing non-real-time rendering, sub-optimal quality in extrapo-
lated views, and fully manual actor behavior design. In con-                Here α′ is determined by the projected 2D Gaussian and the
trast, HUGSIM addresses these challenges by offering real-                  3D opacity α following [85], see the appendix for details.
time performance, improved fidelity in extrapolated views,                  Coordinate System Definition: Given a sequence of urban
and efficient, automated generation of actor behaviors.                     images, we define the world coordinates based on the first
                                                                            frame throughout this paper. Specifically, the origin is set
                                                                            at the front camera of the first frame. The coordinate axes
3    U RBAN S CENE R ECONSTRUCTION                                          are aligned with OpenCV conventions [5], with the x axis
In this section, we begin by introducing the preliminaries.                 pointing to the right, the y axis pointing downward, and
We then present our decomposed urban scene representa-                      the z axis pointing forward.
                                                                                                                                       5

                                                                   sians to be distributed at the same height. However, this
                                                                   assumption overlooks more complex scenarios, such as
                                                                   sloped roads. To tackle this problem, we propose a multi-
                                                                   plane ground model, where we assume the ground to be
                                                                   planar only within a limited distance, denoted as ∆Z . In
                                                                   this model, each local plane is assumed to have a fixed
                                                                   height relative to the nearest camera. Since the camera
      w/o. Ground Model               w. Ground Model              poses reflect the surface slopes, this multi-plane approach
                                                                   effectively models such complex scenarios. Specifically, we
Fig. 3: Lane Distortion In the left image of the extrapolated
                                                                   optimize ground Gaussians and constrain the distribution
view, the lane appears highly distorted due to incorrect
                                                                   of Gaussians in 3D space by limiting the height variance
geometry of ground gaussians. In contrast, the right image,
                                                                   of sampled Gaussian patches within a small ∆Z in cor-
which applies the multi-plane ground model, shows signif-
                                                                   responding camera coordinates. Note that the local planes
icantly fewer artifacts in the same view.
                                                                   overlap with each other, hence avoiding boundary artifacts.
                                                                   More formally, the constraints of our ground model can be
                                                                   expressed as the optimization target:
                                                                       minimize           (1 − λSSIM )∥Î − Ĩ∥1 + λSSIM SSIM(Î, Ĩ)
                                                                    {µx,y,z ,sx,z ,c,α}
                                                                                                v
                                                                                                u
                                                                                                u 1 X      N
                                                                    subject to              lim t             (µcam − µ̄cam )2 = 0
                                                                                          ∆Z→0    N − 1 i=1 yi          y

                                                                                                                                   (4)
Fig. 4: The Multi-Plane Ground Model. Our ground model
is initialized by multiple planes, each containing a set of flat   where Î, Ĩ represent the rendered image and the ground
3D Gaussians. During training, we sample small patches of          truth image, respectively. N denotes the number of Gaus-
these Gaussians and constrain the height variance.                 sians in one local plane. µcam
                                                                                               yi  and µ̄cam
                                                                                                         y   represent heights of
                                                                   3D Gaussians in camera coordinates and average heights in
3.2   Decomposed Scene Representation                              a patch. Note that the sy and q of the Gaussians are kept
We assume the scene consists of static regions and dynamic         constant to ensure they remain flat and oriented upward.
vehicles exhibiting rigid motion. Static regions are decom-            Unlike previous approaches that use densely tiled or
posed into ground and non-ground regions, allowing the             LiDAR-initilaized Gaussians, as seen in RoGS [21] and
application of planar constraints to the ground to preserve        AutoSplat [38], we find that the ground can be efficiently
lane structure in extrapolated views. We consider two cate-        represented using sparser distributed Gaussians since the
gories of dynamic vehicles: native dynamic vehicles present        ground textures are not uniformly distributed. We therefore
in the original driving dataset and non-native dynamic             retain color, position, opacity, two dimensions of scale as
vehicles reconstructed from 360-degree captured images.            optimizable parameters, while also incorporating the den-
                                                                   sity control strategy [37]. Our approach enables high-quality
Non-Ground Static Gaussians: Following 3DGS [37], we
                                                                   ground rendering without the need for an excessive number
model all regions of urban scenes using 3D Gaussians. In
                                                                   of 3D Gaussians, as demonstrated in our experiments.
addition to the original definition of 3D Gaussians, We pro-
pose to additionally model semantic logits s ∈ RS of each          Native Dynamic Vehicle Gaussians and Unicycle Model:
3D Gaussian, allowing for rendering 2D semantic labels.            For dynamic vehicles, we assume 3D bounding boxes are
Furthermore, we can naturally obtain a rendered optical            predicted from the input RGB images, enabling 3D Gaussian
flow ft1 →t2 ∈ R2 for each 3D Gaussian by projecting the 3D        modeling in object coordinate space. To address noise in
position µ to the image space at two different timestamps,         predictions, we jointly optimize them by regularizing with
t1 and t2 , and calculating the motion. We provide details of      a unicycle model. Specifically, we parameterize the trans-
the multi-modality rendering in Section 3.3.                       formations (Rt , tt ) of each dynamic vehicle following the
                                                                   unicycle model1 . The state of a unicycle model is parameter-
Ground Gaussians: Lanes play a crucial role in the percep-
                                                                   ized by three elements: (xt , zt , θt ), where xt and zt represent
tion of AD algorithms. However, most existing reconstruc-
                                                                   horizontal coordinates of t with tt = [xt , yt , zt ], and θt is the
tion methods struggle to accurately render lane geometry
                                                                   yaw angle of Rt . To adapt the continuous unicycle model
in extrapolated views, as shown in Fig. 3. The cause of
                                                                   to discrete frames, we derive the calculus of the unicycle
these distortions is that ground Gaussians tend to overfit to
                                                                   model for the vehicle transition from timestamp t to t + 1 as
the training views, failing to reconstruct the correct ground
                                                                   follows:
geometry. Our preliminary experiments show that directly                                       vt
supervising the render depth fails to solve the problem, as                      xt+1 = xt + (sin θt+1 − sin θt )
                                                                                               ωt
Gaussians with incorrect geometry can still render accurate-                                   vt
looking 2D depth maps. Insteand, we regularize ground                            zt+1 = zt − (cos θt+1 − cos θt )
                                                                                               ωt
Gaussians to form planar structures, yielding correct geom-
                                                                                 θt+1 = θt + ωt                                      (5)
etry as shown in Fig. 4.
    A naive assumption would be to consider the ground              1. While it is more accurate to model vehicles using a bicycle model,
of scenes as a single planar surface, allowing ground Gaus-        we observe that using the simpler unicycle model is sufficient here.
                                                                                                                                  6




                                                                      Fig. 6: 3D Semantic Reconstruction. Comparison between
                                                                      applying softmax to accumulated 2D semantic logits (left)
                                                                      and to 3D semantic logits (right). Normalizing semantic
                                                                      logits in 3D space clearly reduces floaters and yields better
Fig. 5: Non-Native Vehicle Reconstruction We reconstruct              3D semantic reconstruction than the 2D normalization coun-
more than 100 vehicles from 3DRealCar [20] to enable                  terpart. This improvement is also crucial for our simulator
360-degree high-fidelity actor observation. Additionally, we          collision detection.
place shadow Gaussians with gradually changing opacity
inside a rounded rectangle to enhance the visual realism of           requires an accurate environment map, which is difficult to
the inserted actor.                                                   obtain from perspective cameras. Although some work [43],
                                                                      [50], [51], [57] has addressed the challenge of inverse ren-
Here, vt represents the forward velocity, and ωt is the               dering in Gaussian Splatting, it remains a computationally
angular velocity. This model integrates physical constraints          expensive operation. To simplify the problem, we assume
when compared to directly optimizing the transformations              the light source (the sun) is directly overhead, meaning
of dynamic vehicles at every frame independently, thus                shadows should appear beneath the vehicles. To render
enabling smoother motion modeling of moving objects and               vehicle shadows, we place flat Gaussians at the bottom of
making them less prone to local minima.                               the vehicle in canonical space, as shown in Fig. 5. The α
    While it is possible to define an initial state (x1 , z1 , θ1 )   attribute of these Gaussians decreases smoothly based on
and derive the following states recursively based on ve-              their distance from the bottom center. Although this is a
locities, vt and ωt , such a recursive parameterization is            simplified assumption, we observe that the inserted non-
challenging to optimize. In practice, we define a set of train-       native vehicles appear plausible in many scenarios, striking
able states {(xt , zt , θt )}Tt=1 along with trainable velocities     a good balance between efficiency and photorealism.
            −1
{vt , ωt }Tt=1 , and add a regularization term to ensure that
the vehicle’s states adhere to the characteristics of a unicycle
model in Eq. 5. The regularization terms will be described            3.3   Holistic Urban Gaussian Splatting
in Section 3.4. Additionally, we retrieve the vertical locations
                                                                      Given the representation specified above, we are able to
of the vehicle {yt }Tt=1 from our multi-plane ground model.
                                                                      render images, semantic maps and optical flow to supervise
During simulation, we interpolate the states from Eq. 5 by
                                                                      the model or make predictions at inference time. We now
given timestamps.
                                                                      elaborate on the rendering of each modality.
Non-Native Full-Observed Vehicle Gaussians: The AD
                                                                      Novel View Synthesis: The combination of static and
simulator requires rendering high-fidelity actors from all
                                                                      dynamic Gaussians can be sorted and projected onto the
360 degrees, particularly when integrating interactive actors
                                                                      image plane via α-blending π in Eq. 3.
into closed-loop simulations. However, vehicles in the origi-
                                                                          In contrast to single-object scenes, urban scenes typ-
nal reconstructed scenes are only captured from a limited set
                                                                      ically involve more complex lighting conditions and the
of viewpoints, resulting in noticeable artifacts when viewed
                                                                      images are usually captured with auto white balance and
from angles far outside the training perspectives. To address
                                                                      auto exposure. NeRF-based methods [47] typically feed a
this, we reconstruct vehicles using a densely captured real-
                                                                      per-frame appearance embedding along with the 3D posi-
world dataset, 3DRealCar [20], which provides 360-degree
                                                                      tions into a neural network to compute the color, thereby
observations of real-world vehicles. Our experiments show
                                                                      compensating exposure. However, when working with 3D
that real-world captured vehicles outperform vehicles from
                                                                      Gaussians, there is no neural network capable of processing
original scenes when inserted into the simulation scenes
                                                                      appearance embeddings. Inspired by Urban Radiance Field
with random viewing angles.
                                                                      [53], we generate an exposure affine matrix for each camera
    The 3DRealCar dataset provides masks of the vehicles.
                                                                      by mapping the camera’s extrinsic parameters to an affine
We leverage the mask information to ensure that the 3D
                                                                      matrix A ∈ R3×3 and vector b ∈ R3 via a small MLP:
Gaussians only model the car foreground. This is achieved
by considering an alpha mask loss in addition to the                                        C̃ = A × C + b                      (6)
vanilla rendering loss. Importantly, directly inserting the
foreground vehicles without shadows often appear as if                We demonstrate that modeling the exposure improves ren-
they are floating in the air. However, inverse rendering              dering quality in the experimental section.
                                                                                                                                                 7

Semantic Reconstruction: Similarly to Eq. 3, we can obtain                    We leverage the pre-trained perception model [4] to pro-
2D semantic labels via α-blending based on the 3D semantic                    vide noisy 2D semantic. To compensate for the absence of
logit s:                                                                      manually labeled 3D bounding boxes, we use pre-trained
                                                    i−1                       recognition models [32] to provide noisy 3D tracking results.
                                                                              These easy-to-obtain predictions are crucial for enabling
                       X                            Y
         πS :     S=         softmax(si )αi′              (1 − αj′ )    (7)
                       i∈N                          j=1                       RGB-only holistic scene understanding in both 2D and 3D
                                                                              space, without relying on LiDAR input or 3D semantic
Note that we perform the softmax operation on 3D semantic                     supervision.
logits si prior to α blending, in contrast to most existing
methods that apply softmax to 2D semantic logits S̄ ob-                       Image-Based Losses: Our model is supervised with the
tained by accumulating unnormalized 3D semantic logits                        ground truth images using a combination of L1 and SSIM
si [23], [39], [81]. As shown in Fig. 6, applying softmax in                  losses. Our rendering loss is defined as follows:
2D space leads to noisy 3D semantic labels. This is due
to the fact that 2D space softmax can produce accurate 2D                          LI = (1 − λSSIM )∥Î − Ĩ∥1 + λSSIM SSIM(Î, Ĩ)           (11)
semantics by adjusting the scale of the 3D semantic logits,
allowing a single sampled point with a substantial logit                      where Î and Ĩ represent the rendered and the ground truth
value to significantly influence the volume rendering out-                    image, respectively. We additionally apply the cross-entropy
come. For example, an undesired floating point labeled with                   loss to the rendered semantic label wrt. pseudo-2D semantic
“car” may not be penalized despite the target rendered label                  segmentation ground truth Ŝ:
being “tree”, as long as a 3D Gaussian is providing a large                                                  S−1
logit value of “tree” along this ray. Our solution instead                                                   X
                                                                                                   LS = −          Ŝk log(Sk )               (12)
removes such floaters by normalizing logits in 3D space. See
                                                                                                             k=0
the appendix for more quantitative and qualitative details.
The removal of these floaters is also essential for building                  During the reconstruction of the non-native vehicles, we
our simulator, as the background collision detection is im-                   apply an alpha loss to prevent Gaussians from representing
plemented based on Gaussian semantics and geometry.                           the masked background and to ensure the reconstructed
                                                                              vehicle appears as a non-translucent entity:
Optical Flow: The 3D Gaussian representation also enables
the rendering of optical flow. Given two timestamps t1 and
                                                                                                        LA = ∥A − ĨM ∥2                      (13)
t2 , we first calculate the optical flow of each 3D Gaussian’s
center µ as ft1 →t2 . Specifically, we project µ to the 2D                    where ĨM denotes the ground truth mask and A the ren-
image space based on the camera’s intrinsic and extrinsic                     dered alpha map.
parameters:
                                                                              Physical-Based Regularizations: A 3D regularization loss
       µ′1 = K[Rcam   cam
                t1 ; tt1 ]µ,          µ′2 = K[Rcam   cam
                                               t2 ; tt2 ]µ,             (8)   is applied to the multi-plane ground model to limit the
and then calculate the motion vector as ft1 →t2 = µ′2 − µ′1 .                 variance in the height of the Gaussians, forcing the model
Next, we render the optical flow via accumulate the optical                   learns an almost flat ground patch. We express the opti-
flows via volume rendering:                                                   mization problem Eq. 4 as the multi-plane ground model
                                                                              regularization loss during training:
                              X              i−1
                                             Y
                πF :   F=           fi αi′         (1 − αj′ )           (9)                              1      X
                                                                                       Lground =                     (µcam − µ̄cam )2         (14)
                              i∈N            j=1
                                                                                                       N − 1 z −z <∆z yi       y
                                                                                                              i    0
Note that this rendering process assumes that any pixel
of a rendered 2D Gaussian splat shares the same optical                          We use a unicycle model to guide the noisy 3D bounding
flow direction as the corresponding Gaussian center but                       box predictions:
with scaled magnitude. While this is indeed a simplified                                       X                 X
approximation, we observe this to work well in practice.                                 Lt =     ∥xt − x̂t ∥2 +   ∥zt − ẑt ∥2     (15)
                                                                                                   t                    t
Depth: Depth maps are also provided during rendering.
Each Gaussian’s depth distance relative to the observed                       where x̂t and ŷt are the x and y locations of a noisy 3D
camera is defined as di . The depth map is rendered by                        bounding box at timestamp t.
accumulating di using volume rendering:                                           As mentioned earlier, we parameterize the vehicle’s
                              X              i−1
                                             Y                                states (xt , yt , θt ) and the velocities vt , ωt as learnable param-
                πD :   D=           di αi′         (1 − αj′ )          (10)   eters. Hence, we add the following regularization to make
                              i∈N            j=1                              the states adhere to the unicycle model as follows:
                                                                                             X               vt
3.4   Loss Functions                                                                Luni =        ∥xt+1 − xt −  (sin θt+1 − sin θt )∥+
                                                                                             t
                                                                                                             ωt
Our loss functions are divided into two parts. The first is                                  X              vt
image-based losses, which aim to fit the observed ground                                       ∥zt+1 − zt + (cos θt+1 − cos θt )∥+
                                                                                             t
                                                                                                            ω t
truth or pseudo-ground truth 2D images. The second is                                        X
geometry-based losses, which constrain the reconstructed                                       ∥θt+1 − θt − ωt ∥                       (16)
result to align with physical priors from the real world.                                     t
                                                                                                                                8




Fig. 7: The Aggressive Driving Behavior Model. From (a) to (e), we illustrate the behavior of an aggressive actor (orange)
attempting to collide the ego-vehicle (green) over a time period. In (a), the attacker selects the trajectory with the highest
probability of collision by estimating the future trajectory of the ego vehicle based on its current state. In (c), the attacker
re-estimates and updates the trajectory, successfully colliding with the ego vehicle in (e).

In addition, we regularize the acceleration of the forward        adaptation. To achieve this, we maintain separate reposi-
velocity vt and angular velocity ωt to be smooth:                 tories for the simulator and AD algorithms, implementing
                    X                                             them independently while enabling parallel execution and
             Lreg =     ∥vt+1 + vt−1 − 2vt ∥2 +                   communication. When both the simulator and AD algo-
                      t
                     X                                            rithms are run on the same machine, we use named pipes
                          ∥θt+1 + θt−1 − 2θt ∥2            (17)   to establish a communication bridge, minimizing commu-
                      t                                           nication costs. In other cases, web sockets are available for
                                                                  communication.
4     S IMULATION                                                 Controller: By providing observations and ego vehicle
In this section, we first elaborate on the construction of a      information to the AD algorithms, our simulator expects
closed-loop simulator based on the reconstruction of the          feedback in the form of either planned waypoints or a
previous section. Next, we present our method for effi-           sequence of control commands for the next several seconds.
ciently generating actor behaviors, including both normal         When the feedback is planning waypoints, these waypoints
and aggressive driving patterns. Finally, we introduce the        need to be converted into a sequence of control commands,
evaluation metrics used to assess AD algorithms within our        including steering angle (δ ) and acceleration (ȧ). To achieve
simulator.                                                        this conversion, we leverage a Linear Quadratic Regulator
                                                                  (LQR) control following [36], [45], [73].
4.1   Graphicial Configuration Interface                          Ego-Vehicle Kinematic Model: Given the control com-
We develop a graphicial user interface (GUI) to facilitate the    mands of steering angle (δ ) and acceleration (ȧ), the next
configuration of testing scenarios in our simulator. The GUI      states S of the ego vehicle can be computed by applying a
configuration involves several steps. The first step is config-   discrete version of the kinematic bicycle model, following
uring the camera settings, including the number of cameras,       [36], [54]. In this model, L denotes the length of the ego
camera intrinsics, and and the extrinsic parameters wrt.          vehicle:                        
                                                                                                      v cos θ
                                                                                                              
                                                                                         x
the vehicle. The second step is configuring the ego vehicle                            y  dS       v sin θ 
parameters, including specifying the kinematic model, the                          S=  θ  , dt =  v tan δ            (18)
                                                                                                            
control frequency, and the start state of the ego vehicle. The                                           L
final step involves configuring the actors, including native                             v               ȧ
and non-native vehicles with different behaviors specified
in Section 4.3. The appearance of all these actors can be         Collision Detection: We define two types of collisions
selected from a pool of more than 100 candidate 3D vehicles       for the ego vehicle: collisions with the foreground (actors)
reconstructed from 3DRealCar [20].                                and collisions with the background. Collisions with the
                                                                  foreground are detected by checking if the Bird’s Eye View
                                                                  (BEV) bounding boxes of the ego vehicle and actors overlap.
4.2   Closed-Loop Simulation                                      Collisions with the background are identified by counting
                                                                  the number of background Gaussians inside the ego vehi-
Simulator-User communication: Given the 3D Gaussian
                                                                  cle’s 3D bounding box, excluding Gaussians with ground
reconstruction results, we encapsulate the scenes as Gym-
                                                                  semantic labels and low opacities. If the number exceeds a
nasium environments [6], providing functions such as envi-
                                                                  preset threshold, a collision is considered to have occurred.
ronment resetting, retrieving camera observations, accessing
information about the ego vehicle and environment, and
advancing to the next state with specified control actions        4.3   Actor Driving Behaviors
for the ego vehicle. Ideally, the simulator should support        We design three patterns of driving behavior: replayed,
evaluating various AD algorithms without requiring code           normal and aggressive.
                                                                                                                                                  9

Replayed Driving Behavior: For native dynamic vehicles
in scenes, we reconstruct distinct actor pose observations
into a continuous trajectory using our unicycle models. The
reconstructed trajectory can be integrated into the HUGSIM
closed-loop simulation by providing corresponding times-
tamps. It is important to note that this replayed driving
behavior does not interact with the ego vehicle and is only
applied in some easy scenarios.
Normal Driving Behavior: Normal driving behavior fol-
lows IDM [62], a simple car-following model that relies on
HD maps for lane tracking and vehicle following. If no vehi-
cle is present in front, the model drives at a constant speed.
Among the datasets we consider in this work, NuScenes
is the only one that provides paired RGB images and HD
maps. Therefore, we apply the IDM-based normal driving
behavior on nuScenes alone. For other datasets, we use a
constant speed following a predefined driving direction as
a simple alternative.
Aggressive Driving Behavior: The design of aggressive                             Fig. 8: Illustration of sub-scores combined in HUGSIM.
driving behavior is illustrated in Fig. 7, this adversarial                       We present cases that result in the failure or reduction of the
model performs effectively both with and without the use of                       corresponding sub-scores.
HD maps. Inspired by KING [30] and CAT [78], we design
an optimization-based generative trajectory planner. Unlike                       frequency to further control the intensity of the adversarial
KING, we generate adversarial behavior during simulation                          attack.
rather than in a post-processing manner. In contrast to CAT,
our approach can generate candidate trajectories both with
and without HD maps. First, based on road information or                          4.4   Evaluation
current actor states, we generate a set of feasible candidate                     Inspired by NAVSIM [18] and DriveArena [73], we propose
                 a(i)
trajectories {s1:T }N i=1 based on a spline-planner for the                       the HD-Score (HUGSIM Driving Score) to measure the
attacking actor. T is the planning horizon and N is the                           performance of AD algorithms in our simulator. At each
                                     a(i)
number of candidate trajectories s1:T . The spline-planner                        timestamp, the HD-Score is defined as:
generates feasible trajectories through grid-based terminal                                                          
state sampling, spline-based trajectory interpolation, and                                            Y
                                                                                    HD-Scoret =               scorem  ×
feasibility filtering using dynamic constraints. This process
                                                                                                     m∈{N C,DAC}
enables the generation of diverse and robust trajectory sets                                     |               {z                 }
while ensuring adherence to physical and environmental                                                   driving policy items
                                                                                                                                           !
constraints. Next, we select from the feasible trajectories
                                                                                                     P
                                                                                                       w∈{T T C,COM } weightw × scorew
with the goal of attacking the ego vehicle while avoiding                                                  P                                   (20)
                                                                                                              w∈{T T C,COM } weightw
collision with other actors, achieved by predicting the future                                   |                           {z            }
trajectory of the ego vehicle and other actors. More formally,                                                        contributory items
we select the aggressive actor trajectory by minimizing the
                                                                                  The driving policy items include driving with no collisions
composite cost:
                                                                                  (N C ) and drivable area compliance (DAC ), these sub-
                 a(i)                a(i)                        a(i)             scores are crucial for driving safety. The contributory items
min Ctotal (s1:T ) = Cattack (s1:T ) + λCcollision (s1:T ),                       include time-to-collision (T T C ) and comfort (COM ), which
  i
          a(i)
Cattack (s1:T ) = min set − st
                                         a(i)
                                                ,                                 may not directly cause failure cases when they are low.
                        t=1:T                                                     Still, they can lead to feelings of insecurity and discomfort
                          M                                                       for passengers. We illustrate each sub-score in Fig. 8. The
            a(i)                            n(j)       a(i)
                          X
Ccollision (s1:T ) =            1( min st           − st      < tolerance).       detailed definition of these sub-scores can be found in [18].
                                 t=1:T
                         j=1                                                      In the calculation of N C and T T C , we consider collisions
                                                                           (19)   with static background entities such as buildings, fences,
                                                                                  vegetation, etc., leveraging our semantic information. This
                                                                    n(j)
where se1:T denotes the ego future trajectory and s1:T de-                        background entity collision is not included in NAVSIM nor
note the trajectories of other inserted actors, both predicted                    DriveArena.
based on their current states. Cattack denotes the distance                           Additionally, unlike NAVSIM and DriveArena, which
score for successful attacks, and Ccollision penalizes collision                  evaluate ego progress (EP ) using pseudo ground truth
with other actors. Furthermore, we can adjust the attack                          generated by planning algorithms such as the Predictive
intensity by randomly choosing from the top-k trajectories                        Driver Model (PDM) [17], we argue that in a closed-loop
                   a(i)
sorted by Ctotal (s1:T ), instead of choosing the most aggres-                    simulator, other metrics alone can sufficiently reflect the
sive one. Additionally, we can adjust the attack planning                         performance of AD algorithms. Furthermore, the PDM is
                                                                                                                                  10

                                                                                 PSNR↑ SSIM↑ LPIPS↓ mIoUcls ↑mIoUcat ↑
                                                                 mip-NeRF [2]     21.54 0.778 0.365  48.25    67.47
                                                                 PNF [39]         22.07 0.820 0.221  73.06    84.97
                                                                 MARS [68]        23.09 0.857 0.174    -        -
                                                                 Ours             23.38 0.870 0.121  72.65    85.64
                                                                TABLE 2: Novel View Semantic and Appearance Synthesis
                                                                on KITTI-360.
                                                                                              acc.↓    comp.↓     mIoUcls ↑
                                                                       Semantic Nerfacto      1.508     24.28      0.055
                                                                       Ours                   0.233     0.214      0.505
       MARS         Ours         MARS            Ours           TABLE 3: 3D Semantic Reconstruction on KITTI-360. Note
Fig. 9: Details Qualitative Comparison with MARS on             that all metrics are calculated in 3D space.
KITTI-360 Leaderboard.
                                                                dropout rate following existing evaluation protocols [44],
                                                                [68] on all of these datasets. We evaluate the dynamic scene
                                                                novel view synthesis task by comparing our method with
                                                                NSG [52] and MARS [68], which are two open-source meth-
                                                                ods for dynamic urban scenes. Additionally, we compare
                                                                the static novel view appearance task with mip-NeRF [2],
                                                                PNF [39], and MARS [68]. We adopt the default setting for
                                                                interpolated views quantitative assessments, including the
                                                                evaluation of PSNR, SSIM and LPIPS [79]. Although not our
              PNF                         Ours                  main foucus, we include a comparison using ground truth
Fig. 10: Qualitative Comparison with PNF on KITTI-360           3D bounding boxes in the appendix.
Leaderboard.                                                    Dynamic Scene with Noisy 3D Bounding Boxes: Fol-
                                                                lowing [52], [68], we evaluate our performance on dynamic
not a flawless algorithm, even provided with ground-truth
                                                                scenes of the KITTI and vKITTI datasets. In contrast to these
perception results. Additionally, there is often multiple ac-
                                                                methods that leverage ground truth poses, we investigate
ceptable driving style in most scenarios. For these reasons,
                                                                a more practical scenario where the bounding boxes are
evaluating AD algorithms using EP in a closed-loop man-
                                                                generated by a monocular-based 3D tracking algorithm,
ner becomes unsuitable. Instead of measuring ego progress
                                                                QD-3DT [32], in Table 4. Here, the predicted 3D bounding
at each frame, we introduce a global route completion score
                                                                boxes are only provided for training views, as testing views
Rc ∈ [0, 1], which represents the percentage of the driving
                                                                should not be used as inputs for the tracking model. In
distance completed by AD algorithms.
                                                                experiments where the unicycle model is not utilized, the
    The final HD-Score is averaged across all simulation
                                                                bounding boxes of testing views are obtained through linear
timestamps and multiplied by the global route completion
                                                                interpolation from neighbour training views. Where the
score Rc :
                               PT                               unicycle model is used, the bounding boxes of testing views
                                     HD-Scoret                  are computed using Eq. 5. For vKITTI, there is no pre-
             HD-Score = Rc × t=0                         (21)
                                       T                        trained monocular tracking algorithm. We hence jitter the
                                                                ground truth poses to simulate noisy monocular predictions,
5     R ENDERING E VALUATION                                    with an average noise of 0.5 meters in translation and 5
In this section, we evaluate HUGSIM from several perspec-       degrees in rotation. Our model’s robustness wrt. various
tives. In Section 5.1, we focus on evaluating interpolated      levels of noise will be analyzed in the ablation study.
views in both dynamic and static scenes. In Section 5.2, we         Table 4 demonstrate that our method consistently out-
assess the semantics and geometry of reconstructed scenes.      performs against the baselines. Note, that QD-3DT yields
In Section 5.3, we evaluate extrapolated views, which are       reasonable predictions on the KITTI dataset2 . Hence, NSG
significant in a closed-loop driving simulator. Finally, in     and MARS reconstruct the dynamic objects reasonably well,
Section 5.4, we conduct ablation studies on each component      but with more blurriness and artifacts (see Fig. 11), as they
of HUGSIM.                                                      do not model the optimization of the object poses. In con-
                                                                trast, our method allows for reconstructing dynamic objects
                                                                with sharp details, not only in cases of minor pose error
5.1   Novel View Synthesis on Interpolated Views                on the KITTI dataset but also on the vKITTI dataset with
We first evaluate HUGSIM for interpolated novel view syn-       more severe noise. We present the optimization progress of
thesis on KITTI [26], Virtual KITTI2 [7] and KITTI-360 [44]     noisy bounding boxes and a comparison before and after
including dynamic and static scenes. For dynamic scenes,        optimization in the appendix.
we leverage noisy 3D bounding box predictions as input,
                                                                Static Scene Leaderboard: We further evaluate our per-
instead of using the ground truth. We evaluate the dynamic
                                                                formance on the KITTI-360 leaderboard, which contains 5
scene rendering results on KITTI and vKITTI in this section
because previous dynamic urban reconstruction baselines          2. In fact, following the evaluation protocol of MARS, the sequences
have been tested on these two datasets. We apply 50%            we evaluate on are used as training sequences for QD-3DT.
                                                                                                                            11

                        KITTI Scene02              KITTI Scene06             vKITTI Scene02            vKITTI Scene06
                  PSNR↑ SSIM↑ LPIPS↓         PSNR↑ SSIM↑ LPIPS↓         PSNR↑ SSIM↑ LPIPS↓        PSNR↑ SSIM↑ LPIPS↓
  NSG [52]         23.00    0.664    0.373    23.78    0.717    0.234    21.40   0.689    0.376    20.60    0.719   0.255
  MARS [68]        23.30    0.731    0.139    25.09    0.856    0.083    22.67   0.882    0.128    21.67    0.856   0.134
  Ours             25.42    0.821    0.092    28.20    0.919    0.027    26.21   0.911    0.040    26.65    0.921   0.030
                  TABLE 4: Novel View Synthesis on Dynamic Scenes with predicted or noisy 3D trackings.
      KITTI
      vKITTI




                     NSG                        MARS                         Ours                         GT
Fig. 11: Qualitative Comparison on KITTI and vKITTI. We use monocular-based 3D bounding box predictions for KITTI,
and manually jittered 3D bounding boxes for vKITTI. We zoom in on a patch of a dynamic object for each KITTI scene.

static sequences. Our method achieves state-of-the-art per-      3D Semantic Scene Reconstruction: While existing 2D-
formance on the leaderboard as in Table 2 (left), demon-         to-3D semantic lifting methods solely evaluate their per-
strating the effectiveness of the 3D Gaussian representation     formance in the 2D image space, we further evaluate our
in modeling complex urban scenes. As we will discuss             performance in the 3D space to examine the underlying
in the ablation study, incorporating the affine transform        3D geometry. To this goal, we leverage the ground truth
to model camera exposure is important for reaching high          LiDAR points provided by the KITTI-360 dataset for evalu-
fidelity. Fig. 9 shows the qualitative comparison of our         ation. With each Gaussian possessing semantic information,
proposed method to another top-ranking method, MARS,             we can obtain a semantic point cloud by extracting the
on the leaderboard.                                              Gaussian’s center µ and its semantic label. We evaluate the
                                                                 geometric quality and semantic accuracy of this semantic
5.2       Semantic and Geometric Scene Understanding             point cloud in Table 3. We compare our method with Se-
Next, we evaluate our model on various semantic and geo-         mantic Nerfacto [60], a Semantic NeRF implemented using
metric scene understanding tasks on the KITTI-360 dataset        a more advanced backbone, as the state-of-the-art novel
[44] as it provides dense 2D and 3D labels. We compare           view semantic synthesis method, PNF, in Table 2 is not
the semantic synthesis task with mip-NeRF [2], PNF [39],         open-source. For this baseline, we extract a semantic point
and MARS [68]. Furthermore, we assess the quality of             cloud by specifying a threshold to the density field. While
3D semantic scene reconstruction by comparing it with            Semantic Nerfacto enables rendering faithful 2D semantic
Semantic Nerfacto [60]. We follow KITTI-360, which reports       labels as shown in the appendix, the underlying 3D seman-
the mean Intersection over Union on class (mIoUcls ) and         tic point cloud is significantly worse in comparison. The
category (mIoUcat ), respectively. Further, we evaluate our      Gaussian based representation instead allows for extracting
performance on 3D Semantic Segmentation against a ground         a much more accurate semantic point cloud in comparison.
truth semantic LiDAR point cloud, measuring both geo-            Accurate geometry is crucial for implementing the closed-
metric reconstruction quality and semantic accuracy. The         loop simulator.
geometric quality is evaluated as the chamfer distance be-
tween two point clouds, including completeness and accu-
racy, whereas the semantic accuracy is also measured using       5.3    Novel View Synthesis on Extrapolated Views
mIoUcls . Correct 3D semantics, the reduction of floaters, and
                                                                 The ego vehicle can change lanes or view scenes from a wide
the reconstruction of accurate geometry are essential for
                                                                 range of perspectives beyond the training views, which
building our closed-loop simulator and benchmark.
                                                                 may lead to artifacts in novel view synthesis, particularly
Novel View Semantic Synthesis: Our holistic represen-            causing distortion in lanes and other ground-level signals.
tation also enables novel view semantic synthesis. Hence,        However, since most extrapolated camera poses are not di-
we submit our novel view semantic synthesis performance          rectly observed, quantitative metrics like PSNR that require
to the KITTI-360 leaderboard for comparison as well, see         ground-truth images cannot be computed directly. Instead,
Table 2 (right). Despite not leveraging category-level prior     we use the Kernel Inception Distance (KID) [3] to measure
as done in previous work [39], our approach achieves com-        the similarity in distribution between extrapolated views
parable performance to the SOTA [39] as shown in Fig. 10.        and real captured images.
                                                                                                                              12

                                 Waymo                        NuScenes                    Attributes
                    PSNR↑ SSIM↑ LPIPS↓ KIDextrap ↓ PSNR↑ SSIM↑ LPIPS↓ KIDextrap ↓ FPS↑ #GS↓         Inputs
NeuRAD [61]          29.18 0.839   0.120 0.094      24.49 0.692  0.287  0.082     2.61     -     LiDAR+RGB
StreetGaussian [70] 27.20  0.868   0.113 0.151        -     -      -      -       66.50 6.85M LiDAR+RGB
Ours                 28.97 0.872   0.110 0.077      25.36 0.776  0.171  0.062     89.15 4.45M        RGB
TABLE 5: Quantitative Comparison with NeuRAD and StreetGaussian. All the experiments are conducted on a NVIDIA
RTX 3090.
StreetGaussian




                                                                  NeuRAD
                                                                  Ours
NeuRAD




                                                                  Fig. 13: Extrapolated Views Qualitative Comparison with
                                                                  NeuRAD [70] on nuScenes.

                                                                                   PSNR↑ SSIM↑ LPIPS↓ KIDextrap ↓ #GS↓
                                                                       ROGS [21]    18.70 0.795 0.158   0.223     1.02M
Ours




                                                                       Ours         27.44 0.924 0.061   0.196     0.71M
                                                                  TABLE 6: Quantative Comparison with RoGS. Note that
                                                                  we evaluate all the ground areas, which differs from the
                                                                  evaluation in the RoGS paper, where only sparse colored
Fig. 12: Extrapolated Views Qualitative Comparison with           LiDAR points are considered.
StreetGaussian and NeuRAD [70] on Waymo.
                                                                  Fig. 13 provides a qualitative comparison of HUGSIM and
                                                                  other methods. Without ground constraints, significant dis-
   We evaluate extrapolated views on the Waymo Open               tortion is evident in NeuRAD and StreetGaussian, while our
Dataset [58] and nuScenes [8] by comparing our method             method produces realistic results in extrapolated views.
to NeuRAD [61] and StreetGaussian [70], two recent ap-
                                                                  Ground Rendering: We further compare our ground model
proaches for novel view synthesis in urban scenes. Street-
                                                                  with RoGS [21], an approach specifically designed for
Gaussian supports the Waymo dataset, while NeuRAD
                                                                  ground reconstruction using 2D Gaussian Splatting [34]. The
supports both Waymo and nuScenes datasets. Notably,
                                                                  primary difference between RoGS and our method is that
NeuRAD is also the reconstruction and rendering method
                                                                  RoGS uniformly distributes Gaussians on the ground plane
used in NeuroNCAP [45]. We further compare our results
                                                                  and fixes their attributes, allowing only spherical harmonics
to RoGS [21], a method designed specifically for ground
                                                                  and height to be learned. In contrast, our method fixes
reconstruction in nuScenes.
                                                                  only the y-axis scale and rotations of Gaussians and applies
Full Scene Rendering: We selected two sequences from              Lground to constrain the ground flatness, as demonstrated
the Waymo dataset and two from nuScenes for comparison.           in Section 3.2.
During training, HUGSIM, StreetGaussian [70], and Neu-                The experiments are conducted on four sequences from
RAD [61] drop every 5th frame. To generate extrapolated           nuScenes. We utilize a semantic mask to color non-ground
views, we shift the original views horizontally to simulate       pixels black. Since the top half of the images does not
lane changes and slightly adjust the yaw angle to simulate        contain any ground pixels, we focus our evaluation on the
varied observation angles. In this experiment, we evaluate        lower half of the images for this experiment. Table 6 and
only the front camera rendering results, as the front view        Fig. 14 show our method surpasses RoGS both quantita-
plays the most crucial role for driving. For a fair comparison,   tively and qualitatively, while also using fewer Gaussians to
all methods use the same extrapolated views within the            reconstruct the scene and exhibiting greater flexibility with-
same sequences.                                                   out the need to assign the hyperparameter of road width.
    Table 5 shows that our method achieves comparable             We attribute the advantages of our method to its learnable
or better performance in interpolated views and state-of-         position, scaling, and opacity, allowing it to allocate more
the-art performance on extrapolated views. Additionally,          Gaussians to texture-rich areas and fewer to regions with
while both StreetGaussian and NeuRAD require LiDAR                minimal texture. This leads to to a reduced number of
point clouds as input, HUGSIM relies solely on RGB im-            Gaussians while maintaining high texture detail. In contrast,
ages. HUGSIM also outperforms the compared methods                the uniform distribution of large numbers of Gaussians, as
in rendering speed and number of Gaussians. Fig. 12 and           implemented in RoGS, still exists holes and results in less
                                                                                                                           13


RoGS
Ours




               Interpolated Views          Interp Zoom In            Extrapolated Views                Extrap Zoom In
Fig. 14: Qualitative Comparison with RoGS. Compared to our results, RoGS exhibits grid-style aliasing and limited
rendering areas. Both methods show no obvious distortion in extrapolated views.

                               KITTI (5% noise)              KITTI (10% noise)             KITTI (20% noise)
                        PSNR↑ SSIM↑ LPIPS↓ eR ↓ et ↓ PSNR↑ SSIM↑ LPIPS↓ eR ↓ et ↓ PSNR↑ SSIM↑ LPIPS↓ eR ↓ et ↓
w/o opt., w/o uni.       23.83 0.878 0.062 0.031 0.027 22.16 0.861 0.079 0.063 0.106 20.28 0.835 0.101 0.125 0.425
w/ opt., w/o uni.        24.80 0.897 0.038 0.022 0.051 22.75 0.879 0.056 0.054 0.130 20.56 0.855 0.081 0.135 0.612
w/ opt., w/ uni. (Ours) 28.78 0.928 0.023 0.017 0.022 26.66 0.908 0.032 0.037 0.035 23.59 0.875 0.061 0.081 0.176
                                    TABLE 7: Ablation Study of Dynamic Scenes of KITTI.

                              PSNR↑ SSIM↑ LPIPS↓ Depth ↓      cycle model on KITTI by manually adding noise to the 3D
   w/o Affine transform        24.18 0.827 0.083    –         bounding boxes and evaluate both the novel view synthesis
   w/o LS                      24.47 0.831 0.081  0.892       results and the tracking performance, see Table 7. In this
   Ours                        24.52 0.833 0.081  0.872       experiment, we compare our full model to two variants, i.e.,
 TABLE 8: Ablation Study of Static Scenes on KITTI-360.       using the noises without optimization (w/o opt., w/o uni.),
                                                              and performing naı̈ve per-frame optimization without using
                PSNR↑ SSIM↑ LPIPS↓ KIDinterp ↓ KIDextrap ↓    the unicycle model (w/ opt., w/o uni.). We evaluate 3D
- Lground        28.03 0.928 0.059   0.041       0.249        tracking performance by measuring the rotation and trans-
- lr sx , sz     25.84 0.909 0.079   0.050       0.266
                                                              lation error eR and et of our optimized 3D bounding boxes
- lr µ           26.91 0.916 0.065   0.039       0.242
Ours             27.44 0.924 0.061   0.039       0.196        wrt. the ground truth following [10]. The results validate
                                                              the effectiveness of the unicycle model, which obviously
TABLE 9: Quantitative Ablation of Ground Model. While         improves the rendering quality and 3D tracking accuracy.
the model without Lground demonstrates better metrics         Qualitative results in Fig. 15 further verify the effectiveness
in interpolated views, noticeable artifacts are rendered in   of our unicycle model in enabling accuracy object recon-
extrapolated views.                                           struction given noisy 3D bounding boxes.

                                                              Static Scene: We study the effect of different components
                                                              on three static scenes of KITTI-360 in Table 8. This allows
                                                              us to ablate design choices without mixing up the impact
                                                              of dynamic objects. The results indicate the significance
                                                              of exposure modeling, which is particularly important for
                                                              scenes with strong exposure variance. The semantic loss
                                                              has little contribution to improving novel view synthesis.
                                                              It is rational as imposing a constraint on the semantics
                                                              does not necessarily contribute to appearance. However,
                                                              note that incorporating the semantic supervision improves
                                                              the underlying geometry, see the appendix for qualitative
 w/o opt., w/o uni. w/ opt., w/o uni.           Ours          comparison. Moreover, we utilize the semantic information
Fig. 15: Detail Qualitative Comparison on KITTI with          for collision detection of our closed-loop simulator.
Noisy Bounding Boxes.
                                                              Ground Model: We ablate the effectiveness of Lground
                                                              and importance of learnable position, scaling and opacity,
satisfactory rendering outcomes.                              as shown Table 9 and Fig. 16. PSNR, SSIM and LPIPS are
                                                              evaluated in interpolated views, while KID is evaluated in
5.4    Ablation                                               extrapolated views. The results demonstrate the importance
We conduct ablation studies on dynamic, static scenes,        of Lground in significantly reducing floating Gaussians.
ground model and inserted vehicles.                           Additionally, the learnable position, scaling, and opacity
                                                              improve the reconstruction fidelity of our road model.
Dynamic Scene: As KITTI provides accurate 3D bounding
box ground truth, we ablate the effectiveness of our uni-     Inserted Vehicles:    To compare simulation quality with
                                                                                                                           14


-Lground
-lr sx , sz
-lr µ




                                                                           Native                      Non-Native
 Ours




                                                                Fig. 17: Qualitative Comparison with native and non-native
                                                                vehicles insertion.
                    Interpolated              Extrapolated      focus on front and side views. Our experiments show that
              Fig. 16: Qualitatively Ablation of Ground Model   although UniAD and VAD are trained on a setup with six
                                                                surrounding cameras, they exhibit robust generalizability
                                                                even when only the front three camera views are provided.
native versus non-native vehicles, we inserted vehicles with
random poses into a sequence, as shown in Fig. 17. The          Scenarios: For each reconstructed scene, we design sce-
results indicate that native vehicles yield less satisfactory   narios across various difficulty levels: easy, medium, hard
rendering results due to limited observations.                  and extreme. Each reconstructed scene consists of more than
                                                                four scenarios, as each difficulty level may contain multiple
                                                                scenarios. Altogether, the HUGSIM benchmark comprises
6             C LOSED -L OOP B ENCHMARK                         over 400 scenarios, offering a diverse set of training and
In this section, we first establish the HUGSIM benchmark,       testing environments for AD algorithms with interactive
comprising a variety of scenes and scenarios with varying       actors.
difficulty levels for evaluating AD algorithms. Next, we            Easy scenarios feature mostly static scenes or only in-
use the HUGSIM benchmark to evaluate several existing           clude replayed driving actors modeled with a unicycle
AD algorithms, providing a fair, closed-loop evaluation.        model. Medium scenarios include IDM and constant-speed
Furthermore, we provide a brief case study on the failure       driving actors with typical driving behaviors, where IDM
cases of existing AD algorithms.                                actors yield to the ego vehicle. IDM is implemented only in
                                                                nuScenes due to its HD map availability. Hard and extreme
                                                                scenarios introduce aggressive actors that attempt to collide
6.1           HUGSIM Benchmark                                  with the ego vehicle, with extreme scenarios increasing both
We establish the HUGSIM benchmark based on KITTI-               the number of aggressive actors, a higher frequency of re-
360 [44], Waymo [58], nuScenes [8] and PandaSet [69].           planned attack routes and a greater likelihood of selecting
Our benchmark contains more than 70 scenes and over             the most aggressive trajectories. We provide details of the
400 scenarios with varying difficulty levels for testing AD     scenario designs in the appendix.
algorithms.
Scenes: The HUGSIM benchmark consists of scenes from            6.2   Evaluation on HUGSIM Benchmark
KITTI-360, Waymo, nuScenes, and PandaSet. These scenes
                                                                Evaluated AD Algorithms: The HUGSIM benchmark is
feature a variety of street layouts, lighting conditions, and
                                                                well-suited for testing AD algorithms that require only RGB
imaging styles.
                                                                images and ego vehicle status as inputs. In this paper, we
    As AD algorithms like UniAD [33], VAD [35] and Latent-
                                                                evaluate UniAD [33], VAD [35] and Latent-Transfuser (LTF)
Transfuser (LTF) [14] demand for a relative large field on
                                                                [14]. LTF is the LiDAR free version of Transfuser, which
view, KITTI [26] is not included in HUGSIM, as it only
                                                                replaces the LiDAR input as a template positional encoding.
provides two front-facing cameras. For scene reconstruction,
                                                                It is worth noting that only LTF requires data from the
we use the two front-facing perspective cameras and two
                                                                front three cameras, while UniAD and VAD demands for
side fisheye cameras converted to perspective [48] in KITTI-
                                                                input from six surrounding cameras. For all these three
360, the three front perspective cameras in Waymo, and all
                                                                methods, we implement evaluation APIs that interface with
six perspective cameras in both nuScenes and PandaSet.
                                                                HUGSIM Gymnasium environments [6]. These APIs receive
    For our simulator rendering, we use the same camera
                                                                data, parse it into the required format for model inference,
configuration as nuScenes. For scenes from nuScenes and
                                                                and send back the planned future waypoints to HUGSIM.
PandaSet, we provide rendered images from all six cameras
as observations to the AD algorithms. For scenes from           Closed-Loop Evaluation Results: The evaluation results on
KITTI-360 and Waymo, we provide renderings from only            our HUGSIM benchmark are presented in Fig. 18. Detailed
the front three cameras, as these two datasets primarily        evaluation results can be found in the appendix. UniAD
                                                                                                                                                            15

                          UniAD                                                  VAD                                         Latent-Transfuser
    1.0                                                    1.0                                                  1.0

    0.8                                        NC
                                               DAC
                                                           0.8                                      NC
                                                                                                    DAC
                                                                                                                0.8                                    NC
                                                                                                                                                       DAC
                                               TTC                                                  TTC                                                TTC
                                               COM                                                  COM                                                COM
                                               Rc                                                   Rc                                                 Rc
    0.6                                        KITTI-360   0.6                                      KITTI-360   0.6                                    KITTI-360
Score




                                                       Score




                                                                                                            Score
                                               Waymo                                                Waymo                                              Waymo
                                               NuScenes                                             NuScenes                                           NuScenes
                                               Pandaset                                             Pandaset                                           Pandaset
    0.4                                                    0.4                                                  0.4

    0.2                                                    0.2                                                  0.2

    0.0       Easy   Medium       Hard   Extreme           0.0   Easy   Medium         Hard   Extreme           0.0   Easy    Medium    Hard     Extreme
                       Level                                   Level                       Level
 Fig. 18: Evaluation Results on HUGSIM Benchmark. The histograms indicate performance of models on each type of
 dataset, while the lines represent the averaged sub-scores across datasets.

                                                                                  of original scenes, can be difficult for these algorithms,
                                                                                  highlighting the lack of generalization and the need for
        (a)                                                                       systematic analysis using a closed-loop simulator as pre-
                                                                                  sented in this paper. The greater challenges presented at the
                                                                                  medium, hard, and extreme levels indicate that substantial
                                                                                  efforts are still required to achieve the goal of full autonomy.
                                                                                  Case Study: We outline some common failure cases en-
        (b)                                                                       countered by AD algorithms in our closed-loop simulator
                                                                                  as shown in Fig. 19: (a) Since collisions never occur in open-
                                                                                  loop datasets, models rarely encounter situations where
                                                                                  there is no drivable area in front of the vehicle. As a result,
                                                                                  they consistently predict a drivable area ahead, regardless
                                                                                  of the RGB observations. (b) AD algorithms face difficulties
        (c)                                                                       with turning, often steering at inappropriate angles relative
                                                                                  to the street structure. (c) Although a leading vehicle is
                                                                                  detected, AD algorithms often do not take evasive action
                                                                                  in advance; instead, they attempt to make a sharp turn at
        (d)                                                                       a very close distance, which can easily result in a collision.
                                                                                  (d) The planned trajectory of AD algorithms can be unsta-
                                                                                  ble, which may lead to collisions in narrow streets and a
 Fig. 19: Case Study. The left part shows the RGB observa-
                                                                                  reduction in COM score.
 tions, perception results, and planning trajectories, the right
 part displays the predicted BEV information of UniAD.
                                                                                  7     C ONCLUSION
 and LTF demonstrate similar performance on the HUGSIM
 benchmark. While LTF performs better at easier scenarios,                        We present HUGSIM, a novel photorealistic closed-loop
 UniAD exhibits more powerful capabilities in handling                            simulator for autonomous driving, featuring real-time, high-
 most of the complex scenarios. We attribute this advantage                       quality rendering in extrapolated views and efficiently gen-
 of UniAD to its trajectory post-processing strategy based on                     erated actor behavior. Specifically, we reconstruct urban
 predicted occupancy. However, this post-processing strat-                        scenes using 3D Gaussians and introduce a ground model,
 egy also introduces non-smooth trajectories, negatively im-                      along with single-vehicle reconstruction, to improve the ren-
 pacting the COM score. Another notable point is that in                          dering quality of extrapolated views. For actor behavior, we
 KITTI-360 and Waymo scenes, only the front three camera                          propose an attack-cost-based trajectory interactively search
 views are provided, while UniAD is trained using sur-                            to simulate aggressive driving behaviors of actors.
 rounding six views. The similar performance on Waymo                                 Furthermore, we establish the HUGSIM benchmark
 and nuScenes indicates the generalizability of UniAD. VAD                        across multiple datasets including variance sequences, de-
 shows less satisfying performance compared to UniAD and                          signing more than 300 scenarios for evaluating and train-
 LTF on the HUGSIM benchmark, particularly on KITTI-360,                          ing AD algorithms. We evaluate several baselines on our
 Waymo, and PandaSet. This could potentially be due to                            benchmark. Our results show that the HUGSIM benchmark
 VAD overfitting to the scene and scenario styles in nuScenes,                    presents significant challenges for existing AD algorithms.
 making it challenging to handle out-of-domain observations                       This closed-loop benchmark reveals substantial room for
 in our closed-loop simulator. All these algorithms face chal-                    improvement in autonomous driving performance. We hope
 lenges with KITTI-360 scenes due to narrow streets and                           that our dataset and benchmark will fertilize new research
 numerous parked vehicles, along with an imaging style                            across communities, fostering progress towards the ultimate
 that differs significantly from nuScenes and nuPlan, which                       goal of full autonomy.
 are training datasets of these algorithms. Furthermore, the                          For future work, HUGSIM can be enhanced in several
 HUGSIM benchmark poses significant challenges for ex-                            ways. First, we assume all dynamic objects follow rigid
 isting AD algorithms. Even the easy level, which consists                        motion, which may cause blurring for non-rigidly moving
                                                                                                                                                        16

objects, such as pedestrians. This can be addressed by in-                    [14] K. Chitta, A. Prakash, B. Jaeger, Z. Yu, K. Renz, and A. Geiger,
corporating non-rigid dynamic reconstruction methods [13],                         “Transfuser: Imitation with transformer-based sensor fusion for
                                                                                   autonomous driving,” IEEE Trans. on Pattern Analysis and Machine
[75] into our framework. While our method improves ren-                            Intelligence (PAMI), 2023. 14,
dering at extrapolated viewpoints, it struggles with high-                    [15] F. Codevilla, M. Müller, A. López, V. Koltun, and A. Dosovitskiy,
fidelity rendering at views that are far from the input or                         “End-to-end driving via conditional imitation learning,” in Proc.
very close to objects. These challenges could be mitigated                         IEEE International Conf. on Robotics and Automation (ICRA). IEEE,
                                                                                   2018, pp. 4693–4700. 1
by leveraging priors from 2D generative models [64], [76].                    [16] F. Codevilla, E. Santana, A. M. López, and A. Gaidon, “Exploring
Furthermore, since our approach opens up the possibility                           the limitations of behavior cloning for autonomous driving,” in
for fine-tuning AD algorithms in a photorealistic closed-                          Proc. of the IEEE International Conf. on Computer Vision (ICCV), 2019,
loop setting, this presents a promising avenue for future                          pp. 9329–9338. 1
                                                                              [17] D. Dauner, M. Hallgarten, A. Geiger, and K. Chitta, “Parting with
exploration.                                                                       misconceptions about learning-based vehicle motion planning,” in
                                                                                   Proc. Conf. on Robot Learning (CoRL). PMLR, 2023, pp. 1268–1281.
                                                                                   1, 9
ACKNOWLEDGMENTS                                                               [18] D. Dauner, M. Hallgarten, T. Li, X. Weng, Z. Huang, Z. Yang, H. Li,
The authors thank Kashyap Chitta for providing details                             I. Gilitschenski, B. Ivanovic, M. Pavone et al., “Navsim: Data-
                                                                                   driven non-reactive autonomous vehicle simulation and bench-
of Transfuser and NAVSIM, and Chaojie Ji, Yuanbo Yang,                             marking,” arXiv preprint arXiv:2406.15349, 2024. 2, 3, 4, 9,
Xianxu Xiang, and Jiahao Shao for proofreading. This work                     [19] A. Dosovitskiy, G. Ros, F. Codevilla, A. Lopez, and V. Koltun,
is supported by NSFC under grant 62202418, U21B2004                                “Carla: An open urban driving simulator,” in Proc. Conf. on Robot
and the National Key R&D Program of China under Grant                              Learning (CoRL). PMLR, 2017, pp. 1–16. 1, 3, 4,
2021ZD0114501. Yiyi Liao is with the Zhejiang Provincial                      [20] X. Du, H. Sun, S. Wang, Z. Wu, H. Sheng, J. Ying, M. Lu, T. Zhu,
                                                                                   K. Zhan, and X. Yu, “3drealcar: An in-the-wild rgb-d car dataset
Key Laboratory of Information Processing, Communication                            with 360-degree views,” arXiv preprint arXiv:2406.04875, 2024. 2, 6,
and Networking (IPCAN). Andreas Geiger was supported                               8
by the ERC Starting Grant LEGO-3D (850533) and the DFG                        [21] Z. Feng, W. Wu, and H. Wang, “Rogs: Large scale road surface
                                                                                   reconstruction based on 2d gaussian splatting,” arXiv preprint
EXC number 2064/1 - project number 390727645.
                                                                                   arXiv:2405.14342, 2024. 3, 5, 12,
                                                                              [22] T. Fischer, J. Kulhanek, S. R. Bulò, L. Porzi, M. Pollefeys, and
                                                                                   P. Kontschieder, “Dynamic 3d gaussian fields for urban areas,”
R EFERENCES                                                                        arXiv preprint arXiv:2406.03175, 2024. 3
[1]  S. Agarwal, Y. Furukawa, N. Snavely, I. Simon, B. Curless, S. M.         [23] X. Fu, S. Zhang, T. Chen, Y. Lu, L. Zhu, X. Zhou, A. Geiger, and
     Seitz, and R. Szeliski, “Building rome in a day,” Communications of           Y. Liao, “Panoptic nerf: 3d-to-2d label transfer for panoptic urban
     the ACM, vol. 54, no. 10, pp. 105–112, 2011. 3                                scene segmentation,” in Proc. of the International Conf. on 3D Vision
[2] J. T. Barron, B. Mildenhall, M. Tancik, P. Hedman, R. Martin-                  (3DV). IEEE, 2022, pp. 1–11. 7
     Brualla, and P. P. Srinivasan, “Mip-nerf: A multiscale represen-         [24] D. Gallup, J.-M. Frahm, and M. Pollefeys, “Piecewise planar and
     tation for anti-aliasing neural radiance fields,” in Proc. of the IEEE        non-planar stereo for urban scene reconstruction,” in Proc. IEEE
     International Conf. on Computer Vision (ICCV), 2021, pp. 5855–5864.           Conf. on Computer Vision and Pattern Recognition (CVPR). IEEE,
     10, 11                                                                        2010, pp. 1418–1425. 3
[3] M. Bińkowski, D. J. Sutherland, M. Arbel, and A. Gretton, “De-           [25] S. Gao, J. Yang, L. Chen, K. Chitta, Y. Qiu, A. Geiger,
     mystifying mmd gans,” arXiv preprint arXiv:1801.01401, 2018. 11               J. Zhang, and H. Li, “Vista: A generalizable driving world model
[4] S. Borse, Y. Wang, Y. Zhang, and F. Porikli, “Inverseform: A loss              with high fidelity and versatile controllability,” arXiv preprint
     function for structured boundary-aware segmentation,” in Proc.                arXiv:2405.17398, 2024. 4
     IEEE Conf. on Computer Vision and Pattern Recognition (CVPR), 2021,      [26] A. Geiger, P. Lenz, and R. Urtasun, “Are we ready for autonomous
     pp. 5901–5911. 7,                                                             driving? the kitti vision benchmark suite,” in Proc. IEEE Conf. on
[5] G. Bradski, “The opencv library,” Dr. Dobb’s Journal of Software               Computer Vision and Pattern Recognition (CVPR). IEEE, 2012, pp.
     Tools, 2000. 4                                                                3354–3361. 1, 3, 10, 14,
[6] G. Brockman, “Openai gym,” arXiv preprint arXiv:1606.01540, 2016.         [27] C. Gulino, J. Fu, W. Luo et al., “Waymax: An accelerated, data-
     2, 8, 14                                                                      driven simulator for large-scale autonomous driving research,” in
[7] Y. Cabon, N. Murray, and M. Humenberger, “Virtual kitti 2,” arXiv              Advances in Neural Information Processing Systems (NIPS), 2023. 1, 4
     preprint arXiv:2001.10773, 2020. 10,                                     [28] J. Guo, N. Deng, X. Li, Y. Bai, B. Shi, C. Wang, C. Ding, D. Wang,
[8] H. Caesar, V. Bankiti, A. H. Lang, S. Vora, V. E. Liong, Q. Xu,                and Y. Li, “Streetsurf: Extending multi-view implicit surface recon-
     A. Krishnan, Y. Pan, G. Baldan, and O. Beijbom, “nuscenes: A mul-             struction to street views,” arXiv preprint arXiv:2306.04988, 2023. 3
     timodal dataset for autonomous driving,” in Proc. IEEE Conf. on
                                                                              [29] H. Han, K. Zhou, X. Long, Y. Wang, and C. Xiao, “Ggs: Generaliz-
     Computer Vision and Pattern Recognition (CVPR), 2020, pp. 11 621–
                                                                                   able gaussian splatting for lane switching in autonomous driving,”
     11 631. 1, 2, 3, 12, 14,
                                                                                   arXiv preprint arXiv:2409.02382, 2024. 3
[9] H. Caesar, J. Kabzan, K. S. Tan, W. K. Fong, E. Wolff, A. Lang,
     L. Fletcher, O. Beijbom, and S. Omari, “nuplan: A closed-loop            [30] N. Hanselmann, K. Renz, K. Chitta, A. Bhattacharyya, and
     ml-based planning benchmark for autonomous vehicles,” arXiv                   A. Geiger, “King: Generating safety-critical driving scenarios for
     preprint arXiv:2106.11810, 2021. 1, 3, 4,                                     robust imitation via kinematics gradients,” in Proc. of the European
[10] X. Chen, Z. Dong, J. Song, A. Geiger, and O. Hilliges, “Category              Conf. on Computer Vision (ECCV), 2022. 9
     level object pose estimation via neural analysis-by-synthesis,” in       [31] A. Hu, L. Russell, H. Yeo, Z. Murez, G. Fedoseev, A. Kendall,
     Proc. of the European Conf. on Computer Vision (ECCV). Springer,              J. Shotton, and G. Corrado, “Gaia-1: A generative world model
     2020, pp. 139–156. 13,                                                        for autonomous driving,” arXiv preprint arXiv:2309.17080, 2023. 4
[11] Y. Chen, H. Xu, C. Zheng, B. Zhuang, M. Pollefeys, A. Geiger, T.-J.      [32] H.-N. Hu, Y.-H. Yang, T. Fischer, T. Darrell, F. Yu, and M. Sun,
     Cham, and J. Cai, “Mvsplat: Efficient 3d gaussian splatting from              “Monocular quasi-dense 3d object tracking,” IEEE Trans. on Pattern
     sparse multi-view images,” arXiv preprint arXiv:2403.14627, 2024.             Analysis and Machine Intelligence (PAMI), vol. 45, no. 2, pp. 1992–
     3                                                                             2008, 2022. 7, 10,
[12] Y. Chen, C. Gu, J. Jiang, X. Zhu, and L. Zhang, “Periodic vibra-         [33] Y. Hu, J. Yang, L. Chen, K. Li, C. Sima, X. Zhu, S. Chai, S. Du, T. Lin,
     tion gaussian: Dynamic urban scene reconstruction and real-time               W. Wang et al., “Planning-oriented autonomous driving,” in Proc.
     rendering,” arXiv:2311.18561, 2023. 3                                         IEEE Conf. on Computer Vision and Pattern Recognition (CVPR), 2023,
[13] Z. Chen, J. Yang, J. Huang, R. de Lutio, J. M. Esturo, B. Ivanovic,           pp. 17 853–17 862. 14,
     O. Litany, Z. Gojcic, S. Fidler, M. Pavone et al., “Omnire: Omni         [34] B. Huang, Z. Yu, A. Chen, A. Geiger, and S. Gao, “2d gaussian
     urban scene reconstruction,” arXiv preprint arXiv:2408.16760, 2024.           splatting for geometrically accurate radiance fields,” in ACM
     16                                                                            Trans. on Graphics, 2024, pp. 1–11. 12,
                                                                                                                                                    17

[35] B. Jiang, S. Chen, Q. Xu, B. Liao, J. Chen, H. Zhou, Q. Zhang,          [55] J. L. Schonberger and J.-M. Frahm, “Structure-from-motion revis-
     W. Liu, C. Huang, and X. Wang, “Vad: Vectorized scene repre-                 ited,” in Proc. IEEE Conf. on Computer Vision and Pattern Recognition
     sentation for efficient autonomous driving,” in Proc. of the IEEE            (CVPR), 2016, pp. 4104–4113. 3
     International Conf. on Computer Vision (ICCV), 2023, pp. 8340–8350.     [56] X. Shi, L. Chen, P. Wei, X. Wu, T. Jiang, Y. Luo, and L. Xie, “Dhgs:
     14,                                                                          Decoupled hybrid gaussian splatting for driving scene,” arXiv
[36] N. Karnchanachari, D. Geromichalos, K. S. Tan, N. Li, C. Erik-               preprint arXiv:2407.16600, 2024. 3
     sen, S. Yaghoubi, N. Mehdipour, G. Bernasconi, W. K. Fong,              [57] Y. Shi, Y. Wu, C. Wu, X. Liu, C. Zhao, H. Feng, J. Liu, L. Zhang,
     Y. Guo et al., “Towards learning-based planning: The nuplan                  J. Zhang, B. Zhou et al., “Gir: 3d gaussian inverse rendering for
     benchmark for real-world autonomous driving,” arXiv preprint                 relightable scene factorization,” arXiv preprint arXiv:2312.05133,
     arXiv:2403.04133, 2024. 8                                                    2023. 6
[37] B. Kerbl, G. Kopanas, T. Leimkühler, and G. Drettakis, “3d gaus-       [58] P. Sun, H. Kretzschmar, X. Dotiwalla et al., “Scalability in percep-
     sian splatting for real-time radiance field rendering.” ACM Trans.           tion for autonomous driving: Waymo open dataset,” in Proc. IEEE
     on Graphics, vol. 42, no. 4, pp. 139–1, 2023. 2, 4, 5,                       Conf. on Computer Vision and Pattern Recognition (CVPR), June 2020.
[38] M. Khan, H. Fazlali, D. Sharma, T. Cao, D. Bai, Y. Ren, and B. Liu,          1, 2, 3, 12, 14,
     “Autosplat: Constrained gaussian splatting for autonomous driv-         [59] M. Tancik, V. Casser, X. Yan, S. Pradhan, B. Mildenhall, P. P.
     ing scene reconstruction,” arXiv preprint arXiv:2407.02598, 2024. 3,         Srinivasan, J. T. Barron, and H. Kretzschmar, “Block-nerf: Scalable
     5                                                                            large scene neural view synthesis,” in Proc. IEEE Conf. on Computer
[39] A. Kundu, K. Genova, X. Yin, A. Fathi, C. Pantofaru, L. J. Guibas,           Vision and Pattern Recognition (CVPR), 2022, pp. 8248–8258. 3
     A. Tagliasacchi, F. Dellaert, and T. Funkhouser, “Panoptic neural       [60] M. Tancik, E. Weber, E. Ng, R. Li, B. Yi, T. Wang, A. Kristoffersen,
     fields: A semantic object-aware neural scene representation,” in             J. Austin, K. Salahi, A. Ahuja et al., “Nerfstudio: A modular
     Proc. IEEE Conf. on Computer Vision and Pattern Recognition (CVPR),          framework for neural radiance field development,” in ACM Trans.
     2022, pp. 12 871–12 881. 1, 3, 7, 10, 11,                                    on Graphics, 2023, pp. 1–12. 11,
[40] F. Lafarge, R. Keriven, M. Brédif, and H.-H. Vu, “A hybrid multi-      [61] A. Tonderski, C. Lindström, G. Hess, W. Ljungbergh, L. Svensson,
     view stereo algorithm for modeling urban scenes,” IEEE Trans. on             and C. Petersson, “Neurad: Neural rendering for autonomous
     Pattern Analysis and Machine Intelligence (PAMI), vol. 35, no. 1, pp.        driving,” in Proc. IEEE Conf. on Computer Vision and Pattern Recog-
     5–17, 2012. 3                                                                nition (CVPR), 2024, pp. 14 895–14 904. 3, 12,
[41] H. Li, Y. Gao, D. Zhang, C. Wu, Y. Dai, C. Zhao, H. Feng, E. Ding,      [62] M. Treiber, A. Hennecke, and D. Helbing, “Congested traffic states
     J. Wang, and J. Han, “Ggrt: Towards generalizable 3d gaussians               in empirical observations and microscopic simulations,” Physical
     without pose priors in real-time,” arXiv preprint arXiv:2403.10147,          review E, vol. 62, no. 2, p. 1805, 2000. 2, 9
     2024. 3                                                                 [63] H. Turki, J. Y. Zhang, F. Ferroni, and D. Ramanan, “Suds: Scalable
[42] Q. Li, Z. Peng, L. Feng, Q. Zhang, Z. Xue, and B. Zhou, “Metadrive:          urban dynamic scenes,” in Proc. IEEE Conf. on Computer Vision and
     Composing diverse driving scenarios for generalizable reinforce-             Pattern Recognition (CVPR), 2023, pp. 12 375–12 385. 3
     ment learning,” IEEE Trans. on Pattern Analysis and Machine Intelli-    [64] Q. Wang, L. Fan, Y. Wang, Y. Chen, and Z. Zhang, “Freevs: Gen-
     gence (PAMI), vol. 45, no. 3, pp. 3461–3475, 2022. 1, 4                      erative view synthesis on free driving trajectory,” arXiv preprint
[43] Z. Liang, Q. Zhang, Y. Feng, Y. Shan, and K. Jia, “Gs-ir: 3d gaussian        arXiv:2410.18079, 2024. 3, 16
     splatting for inverse rendering,” in Proc. IEEE Conf. on Computer       [65] X. Wang, Z. Zhu, G. Huang, X. Chen, J. Zhu, and J. Lu,
     Vision and Pattern Recognition (CVPR), 2024, pp. 21 644–21 653. 6            “Drivedreamer: Towards real-world-driven world models for au-
[44] Y. Liao, J. Xie, and A. Geiger, “Kitti-360: A novel dataset and              tonomous driving,” arXiv preprint arXiv:2309.09777, 2023. 4
     benchmarks for urban scene understanding in 2d and 3d,” IEEE            [66] L. Wenl, D. Fu, S. Mao, P. Cai, M. Dou, Y. Li, and Y. Qiao, “Limsim:
     Trans. on Pattern Analysis and Machine Intelligence (PAMI), vol. 45,         A long-term interactive multi-scenario traffic simulator,” in Proc.
     no. 3, pp. 3292–3310, 2022. 1, 2, 3, 10, 11, 14,                             IEEE Conf. on Intelligent Transportation Systems (ITSC). IEEE, 2023,
[45] W. Ljungbergh, A. Tonderski, J. Johnander, H. Caesar, K. Åström,           pp. 1255–1262. 1, 4
     M. Felsberg, and C. Petersson, “Neuroncap: Photorealistic closed-       [67] F. Wimbauer, N. Yang, C. Rupprecht, and D. Cremers, “Behind the
     loop safety testing for autonomous driving,” arXiv preprint                  scenes: Density fields for single view reconstruction,” in Proc. IEEE
     arXiv:2404.07762, 2024. 1, 3, 4, 8, 12,                                      Conf. on Computer Vision and Pattern Recognition (CVPR), 2023, pp.
[46] F. Lu, Y. Xu, G. Chen, H. Li, K.-Y. Lin, and C. Jiang, “Urban                9076–9086. 3
     radiance field representation with deformable neural mesh prim-         [68] Z. Wu, T. Liu, L. Luo, Z. Zhong, J. Chen, H. Xiao, C. Hou,
     itives,” in Proc. of the IEEE International Conf. on Computer Vision         H. Lou, Y. Chen, R. Yang et al., “Mars: An instance-aware, modular
     (ICCV), 2023, pp. 465–476. 3                                                 and realistic simulator for autonomous driving,” in International
[47] R. Martin-Brualla, N. Radwan, M. S. Sajjadi, J. T. Barron, A. Doso-          Conference on Artificial Intelligence (CICAI). Springer, 2023, pp.
     vitskiy, and D. Duckworth, “Nerf in the wild: Neural radiance                3–15. 3, 10, 11,
     fields for unconstrained photo collections,” in Proc. IEEE Conf. on     [69] P. Xiao, Z. Shao, S. Hao, Z. Zhang, X. Chai, J. Jiao, Z. Li, J. Wu,
     Computer Vision and Pattern Recognition (CVPR), 2021, pp. 7210–              K. Sun, K. Jiang et al., “Pandaset: Advanced sensor suite dataset
     7219. 3, 6                                                                   for autonomous driving,” in Proc. IEEE Conf. on Intelligent Trans-
[48] C. Mei and P. Rives, “Single view point omnidirectional camera               portation Systems (ITSC). IEEE, 2021, pp. 3095–3101. 1, 2, 3, 14,
     calibration from planar grids,” in Proc. IEEE International Conf. on    [70] Y. Yan, H. Lin, C. Zhou, W. Wang, H. Sun, K. Zhan, X. Lang,
     Robotics and Automation (ICRA). IEEE, 2007, pp. 3945–3950. 14,               X. Zhou, and S. Peng, “Street gaussians: Modeling dynamic urban
[49] S. Miao, J. Huang, D. Bai, W. Qiu, B. Liu, A. Geiger, and Y. Liao,           scenes with gaussian splatting,” in Proc. of the European Conf. on
     “Efficient depth-guided urban view synthesis,” arXiv preprint                Computer Vision (ECCV), 2024. 1, 3, 12,
     arXiv:2407.12395, 2024. 3                                               [71] J. Yang, B. Ivanovic, O. Litany, X. Weng, S. W. Kim, B. Li, T. Che,
[50] N. Moenne-Loccoz, A. Mirzaei, O. Perel, R. de Lutio, J. M.                   D. Xu, S. Fidler, M. Pavone et al., “Emernerf: Emergent spatial-
     Esturo, G. State, S. Fidler, N. Sharp, and Z. Gojcic, “3d gaus-              temporal scene decomposition via self-supervision,” arXiv preprint
     sian ray tracing: Fast tracing of particle scenes,” arXiv preprint           arXiv:2311.02077, 2023. 3
     arXiv:2407.07090, 2024. 6                                               [72] J. Yang, S. Gao, Y. Qiu, L. Chen, T. Li, B. Dai, K. Chitta, P. Wu,
[51] ——, “3d gaussian ray tracing: Fast tracing of particle scenes,”              J. Zeng, P. Luo et al., “Generalized predictive model for au-
     ACM Trans. on Graphics, 2024. 6                                              tonomous driving,” in Proc. IEEE Conf. on Computer Vision and
[52] J. Ost, F. Mannan, N. Thuerey, J. Knodt, and F. Heide, “Neural               Pattern Recognition (CVPR), 2024, pp. 14 662–14 672. 4
     scene graphs for dynamic scenes,” in Proc. IEEE Conf. on Computer       [73] X. Yang, L. Wen, Y. Ma, J. Mei, X. Li, T. Wei, W. Lei, D. Fu, P. Cai,
     Vision and Pattern Recognition (CVPR), 2021, pp. 2856–2865. 3, 10,           M. Dou, B. Shi, L. He, Y. Liu, and Y. Qiao, “Drivearena: A closed-
     11,                                                                          loop generative simulation platform for autonomous driving,”
[53] K. Rematas, A. Liu, P. P. Srinivasan, J. T. Barron, A. Tagliasacchi,         arXiv preprint arXiv:2408.00415, 2024. 2, 3, 4, 8, 9
     T. Funkhouser, and V. Ferrari, “Urban radiance fields,” in Proc.        [74] Z. Yang, Y. Chen, J. Wang, S. Manivasagam, W.-C. Ma, A. J. Yang,
     IEEE Conf. on Computer Vision and Pattern Recognition (CVPR), 2022,          and R. Urtasun, “Unisim: A neural closed-loop sensor simulator,”
     pp. 12 932–12 942. 3, 6                                                      in Proc. IEEE Conf. on Computer Vision and Pattern Recognition
[54] C. V. Samak, T. V. Samak, and S. Kandhasamy, “Control strategies             (CVPR), 2023, pp. 1389–1399. 3, 4
     for autonomous vehicles,” in Autonomous driving and advanced            [75] Z. Yang, X. Gao, W. Zhou, S. Jiao, Y. Zhang, and X. Jin, “De-
     driver-assistance systems (ADAS). CRC Press, 2021, pp. 37–86. 8              formable 3d gaussians for high-fidelity monocular dynamic scene
                                                                                                                            18

     reconstruction,” in Proc. IEEE Conf. on Computer Vision and Pattern     Yichong Lu Yichong Lu is a Master’s student
     Recognition (CVPR), 2024, pp. 20 331–20 341. 16                         in Zhejiang University. Before that, he obtained
[76] W. Yu, J. Xing, L. Yuan, W. Hu, X. Li, Z. Huang, X. Gao, T.-T.          bachelor degree in the College of Information
     Wong, Y. Shan, and Y. Tian, “Viewcrafter: Taming video diffusion        Science and Electronic Engineering, Zhejiang
     models for high-fidelity novel view synthesis,” arXiv preprint          University. His research interest lies in 3D com-
     arXiv:2409.02048, 2024. 16                                              puter vision, including scene understanding, 3D
[77] Z. Yu, H. Wang, J. Yang, H. Wang, Z. Xie, Y. Cai, J. Cao, Z. Ji, and    reconstruction and 3D generative models.
     M. Sun, “Sgd: Street view synthesis with gaussian splatting and
     diffusion prior,” arXiv preprint arXiv:2403.20079, 2024. 3
[78] L. Zhang, Z. Peng, Q. Li, and B. Zhou, “Cat: Closed-loop adver-
     sarial training for safe end-to-end driving,” in Proc. Conf. on Robot
     Learning (CoRL), 2023. 9
[79] R. Zhang, P. Isola, A. A. Efros, E. Shechtman, and O. Wang, “The
     unreasonable effectiveness of deep features as a perceptual met-
                                                                             Dongfeng Bai received the M.S. degree in the
     ric,” in Proc. IEEE Conf. on Computer Vision and Pattern Recognition
                                                                             Department of Artificial Intelligence from Xi’an
     (CVPR), 2018, pp. 586–595. 10,
                                                                             Jiaotong University, Xi’an, China, in 2020. He is
[80] X. Zhang, A. Kundu, T. Funkhouser, L. Guibas, H. Su, and K. Gen-
                                                                             a researcher in Noah’s Ark Lab, Huawei. His re-
     ova, “Nerflets: Local radiance fields for efficient structure-aware
                                                                             search interests include 3D reconstruction, neu-
     3d scene representation from 2d supervision,” in Proc. IEEE Conf.
                                                                             ral rendering and 3D generation.
     on Computer Vision and Pattern Recognition (CVPR), 2023, pp. 8274–
     8284. 3
[81] S. Zhi, T. Laidlow, S. Leutenegger, and A. J. Davison, “In-place
     scene labelling and understanding with implicit scene represen-
     tation,” in Proc. of the IEEE International Conf. on Computer Vision
     (ICCV), 2021, pp. 15 838–15 847. 7,
[82] B. Zhou, P. Krähenbühl, and V. Koltun, “Does computer vision
     matter for action?” Science Robotics, vol. 4, no. 30, p. eaaw6661,
     2019. 2                                                                 Bingbing Liu (M09) is a Technology Special-
[83] H. Zhou, J. Shao, L. Xu, D. Bai, W. Qiu, B. Liu, Y. Wang, A. Geiger,    ist with Noah’s Ark Lab, Huawei. Previously he
     and Y. Liao, “Hugs: Holistic urban 3d scene understanding via           worked as a Research Scientist with Institute for
     gaussian splatting,” in Proc. IEEE Conf. on Computer Vision and         Infocomm Research, A*STAR, Singapore. He re-
     Pattern Recognition (CVPR), June 2024, pp. 21 336–21 345. 1, 2,         ceived his Bachelor degree from Harbin Institute
[84] X. Zhou, Z. Lin, X. Shan, Y. Wang, D. Sun, and M.-H. Yang,              of Technology, China and the Ph.D degree from
     “Drivinggaussian: Composite gaussian splatting for surrounding          Nanyang Technological University, Singapore re-
     dynamic autonomous driving scenes,” in Proc. IEEE Conf. on              spectively. His research interests are computer
     Computer Vision and Pattern Recognition (CVPR), 2024, pp. 21 634–       vision technologies for autonomous driving and
     21 643. 1, 3                                                            robotics.
[85] M. Zwicker, H. Pfister, J. Van Baar, and M. Gross, “Ewa splatting,”
     IEEE Transactions on Visualization and Computer Graphic (TVCG),
     vol. 8, no. 3, pp. 223–238, 2002. 4,

                                                                             Yue Wang received the Ph.D. degree from the
                        Hongyu Zhou is a Ph.D. student at Zhejiang           Department of Control Science and Engineering,
                        University. Before that, he received his B.S.        Zhejiang University, Hangzhou, China, in 2016.
                        degree from College of Software Engineering,         He is currently working as a Professor with the
                        Tongji University, China. His research interests     Department of Control Science and Engineer-
                        include 3D computer vision and 3D reconstruc-        ing, Zhejiang University. His current research
                        tion and generative models.                          interests include autonomous robots and robot
                                                                             learning.




                                                                             Andreas Geiger received his Diploma in com-
                        Longzhong Lin is a Ph.D. student at Zhejiang
                                                                             puter science and his Ph.D. degree from Karl-
                        University. Before that, he received his B.S. de-
                                                                             sruhe Institute of Technology in 2008 and 2013.
                        gree from the College of Control Science and
                                                                             Currently, he is leading the Autonomous Vision
                        Engineering, Zhejiang University, China. His re-
                                                                             Group at the University of Tübingen. He is also a
                        search interests include autonomous robots and
                                                                             core faculty member of the Tübingen AI Center.
                        robot learning.
                                                                             His research interests include computer vision,
                                                                             machine learning and scene understanding with
                                                                             a focus on self-driving vehicles.




                        Jiabao Wang is an undergraduate student at           Yiyi Liao is an assistant professor at Zhejiang
                        Zhejiang University in the College of Informa-       University, leading the X-Dimensional Represen-
                        tion Science and Electronic Engineering. His re-     tations Lab. She received her Ph.D. in Control
                        search interests include 3D computer vision and      Science and Engineering from Zhejiang Univer-
                        reinforcement learning.                              sity in June 2018 and her B.S. degree from Xi’an
                                                                             Jiaotong University in 2013. Her research inter-
                                                                             ests include 3D vision and scene understanding.
A PPENDIX A                                                                  Gaussians based on their distances from the camera takes
I MPLEMENTATION                                                              the majority of computations in the rendering process. These
                                                                             computations need to be performed only once for rendering
In this section, we begin by discussing our 3D Gaussian
                                                                             all modalities, thus maintaining the real-time rendering
details, encompassing semantic, opacity and depth imple-
                                                                             property of the original 3D Gaussian Splatting.
mentation (A.1). Subsequently, we discuss the difference
between 3D softmax and 2D softmax in 3D Semantic Scene
Reconstruction (A.2). Finally, we elucidate the evaluation                   A.2   3D Semantic Scene Reconstruction
metrics we utilize (A.3).                                                    We utilize Eq. 26, referred to as 3D softmax, to render seman-
                                                                             tic maps. This is in contrast to most existing NeRF-based se-
A.1   3D Gaussian Details                                                    mantic reconstruction methods that perform softmax to the
                                                                             accumulated 2D logits [23], [81], described in Eq. 29, referred
Following [37], each Gaussian has the following attributes:                  to as 2D softmax. The fundamental difference between these
rotation (Rg ∈ R3×3 ), scale (Sg ∈ R3×1 ), opacity (α) and                   two rendering techniques lies in the fact that 3D softmax
spherical harmonics (SH ). The corresponding 3D covari-                      normalizes the logits of each 3D point. This normalization
ance matrix Σ ∈ R3×3 can be calculated using the following                   process helps prevent a single point with a significantly high
formula:                                                                     logit value from imposing an overwhelming influence on
                     Σ = Rg Sg STg RTg                 (22)                  the overall volume rendering outcome. On the other hand,
When provided with a viewing transformation W ∈ R3×3                         it also prevents placing 3D points of low logit values in
and the Jacobian of the affine approximation of the pro-                     empty space. As a result, 3D softmax is effective in reducing
jective transformation J ∈ R3×3 , the covariance matrix                      floaters and enhancing the geometry of the reconstruction
Σ′ ∈ R3×3 in camera coordinates can be expressed as:                         results. In Eq. E.3, we present a comprehensive analysis of
                                                                             the qualitative and quantitative comparison results between
                    Σ′ = JWΣWT JT                                     (23)   these two rendering methods.
Following EWA splatting [85], we can skip the third row                                                                                
and column of Σ′ to obtain a 2 × 2 covariance matrix with                                                    X            i−1
                                                                                                                          Y
the same structure and properties. For brevity, we still use                        S2D norm = softmax          si αi′         (1 − αj′ )   (29)
the notation Σ′ ∈ R2×2 to denote the 2D covariance matrix.                                                 i∈N            j=1

   By considering the projected 3D Gaussian center µ ∈                       In the following sections, we refer to our default setting
R2×1 and an arbitrary point x ∈ R2×1 on camera coordi-                       obtained by Eq. 26 as S3D norm .
nates, the opacity α′ of x contributed by this 3D Gaussian
can be computed as follows:                                                  A.3   Metrics
                                                
                        1
         α′ = α exp − (x − µ)T (Σ′ )−1 (x − µ)           (24)                Novel View Appearance Synthesis: To assess the quality of
                        2
                                                                             novel view appearance synthesis, we utilize the Peak Signal-
The color c of each Gaussian can be computed based on the                    to-Noise Ratio (PSNR), Structural Similarity Index (SSIM),
view direction and its corresponding spherical harmonics                     and Learned Perceptual Image Patch Similarity (LPIPS) [79]
(SH ). Given a set of sorted 3D Gaussians N along the ray,                   following the common practice.
we obtain the accumulated color via volume rendering:
                                                                             Novel View Semantic Synthesis: Following KITTI-360 [44],
                                             i−1
                             X               Y                               we evaluate the quality of novel view semantic synthesis via
              π:    C=              ci αi′         (1 − αj′ )         (25)   the mean Intersection over Union (mIoU) metric.
                            i∈N              j=1
                                                                             3D Semantic Reconstruction: We evaluate 3D semantic re-
The same volume rendering technique can be applied to                        construction quality by extracting a 3D semantic point cloud
obtain semantic S, depth D and optical flow F. With the                      and comparing it with the ground truth LiDAR points.
given semantic feature si , depth value di , and Gaussian                    We evaluate both geometric and semantic metrics in the
motion fi relative to the camera pose, we can define the                     3D space. Specifically, we evaluate geometric reconstruction
semantic rendering, depth rendering, and flow rendering as                   quality by measuring the accuracy (acc.) and completeness
follows:                                                                     (comp.). Accuracy measures the average distance from re-
                                                   i−1
                   X                               Y                         constructed points to the nearest LiDAR point, while com-
              S=         softmax(si )αi′                 (1 − αj′ )   (26)   pleteness measures the average distance from LiDAR points
                   i∈N                             j=1                       to the nearest reconstructed points. In order to measure the
                                  i−1
                   X              Y                                          semantic quality of the reconstructed point cloud, we map
             D=          di αi′         (1 − αj′ )                    (27)   the predicted 3D semantics to the LiDAR points. Concretely,
                   i∈N            j=1
                                                                             for each point in the LiDAR point cloud, we identify its
                                  i−1
                   X              Y                                          closest counterpart in the predicted semantic point cloud
             F=          fi αi′         (1 − αj′ )                    (28)   and allocate a semantic label based on this nearest neighbor.
                   i∈N            j=1
                                                                             The assigned semantic labels of all LiDAR points are then
Note that all the projections and volume rendering tech-                     compared with the 3D semantic segmentation ground truth
niques mentioned are implemented in CUDA. Calculating                        provided by KITTI-360, evaluated via the mIoU metric. Note
the projected 2D opacity α′ on each pixel and sorting                        that we only use the LiDAR point clouds for evaluation.
                 Medium

                                   (a)                           (b)                           (c)
                 Hard




                                   (a)                           (b)                           (c)
                 Extreme




                                   (a)                           (b)                           (c)

Fig. 20: Scenarios Design. Green, blue, gray, and orange represent the ego vehicle, static actors, normal actors, and
aggressive actors, respectively.

3D Tracking: To demonstrate the effectiveness of our model
in rectifying noisy 3D tracking results, we evaluate the accu-
racy of predicted poses compared to ground truth poses in
our ablation study. Considering the rotation and translation
parameters of a ground truth bounding box denoted as R̂
and t̂, respectively, and the corresponding parameters of
predicted poses, represented as R and t, we employ two
metrics for this evaluation following [10]: eR quantifies the
rotation accuracy, while et assesses the translation accuracy
as follows
                             T r(R̂ · R−1 ) − 1
               eR = arccos                                (30)
                                      2
                et = ∥t̂ − t∥2                            (31)
where T r represents the trace of a matrix.
Depth Estimation: In our ablation study, we evaluate the
depth estimation quality of our different variants. This is
achieved by first projecting the LiDAR points acquired at the
same frame to the 2D image space, followed by measuring
the L2 distance between the projected LiDAR depth and our              Ours w/ S2D norm               Ours w/ S3D norm
method. Considering the projected LiDAR depth is sparse,
                                                                 Fig. 21: Qualitative Comparison of 3D and 2D softmax
our assessment focuses solely on pixels with valid LiDAR
                                                                 results. Note that normalizing semantic logits in 3D space
projections when calculating the L2 distance.
                                                                 (Ours w/ S3D norm ) clearly reduces floaters and yields bet-
                                                                 ter 3D semantic reconstruction than the 2D normalization
A PPENDIX B                                                      counterpart (Ours w/ S2D norm ).
DATA
In this section, we present details of datasets on which we      KITTI 2 (vKITTI) [7], KITTI-360 [44], Waymo [58], nuScenes
conducted our experiments, including KITTI [26], Virtual         [8] and PandaSet [69].
                                       Pre.     + π RGB         + Affine      + π Semantic       + π Flow
                          Speed (ms)   6.25    8.13 (+1.88)   8.54 (+0.41)     9.70 (+1.16)    10.17 (+0.47)

                                  TABLE 10: Time consumption breakdown of our method.

                     KITTI Scene02                  KITTI Scene06                 vKITTI Scene02               vKITTI Scene06
               PSNR↑ SSIM↑ LPIPS↓             PSNR↑ SSIM↑ LPIPS↓             PSNR↑ SSIM↑ LPIPS↓           PSNR↑ SSIM↑ LPIPS↓
  NSG [52]      22.51    0.653    0.397        23.38    0.717    0.243        23.50   0.718    0.352       26.42    0.811   0.170
  MARS [68]     22.95    0.728    0.145        27.01    0.883    0.062        29.80   0.950    0.034       32.71    0.959   0.023
  Ours          25.89    0.829    0.092        28.90    0.925    0.016        30.73   0.955    0.018       33.31    0.963   0.010

                TABLE 11: Novel View Appearance on Dynamic Scenes with ground truth 3D trackings.




              Semantic Nerfacto                                Ours                                      Pseudo GT

Fig. 22: Qualitative Comparison with Nerfacto on 2D space. The Pseudo GT column represents the semantic maps that are
predicted by [4] on GT RGB images.


                                                                                                        eR ↓    et ↓
                                                                                              QD-3DT    0.027   0.215
                                                                                      02
                                                                                              Ours      0.018   0.108
                                                                                              QD-3DT    0.017   0.046
                                                                                      06
                                                                                              Ours      0.012   0.033

                                                                    TABLE 12: Quantitative Pose Comparison on two KITTI
                                                                    sequences.

                                                                    KITTI-360: We perform experiments on KITTI-360, en-
                                                                    compassing both static and dynamic scenes. For the tasks
                                                                    of novel view synthesis and novel semantic synthesis on
                                                                    the leaderboard, we conduct experiments on the sequences
                                                                    provided by the official dataset. We also explore dynamic
      Semantic Nerfacto                       Ours                  scenes, such as frames 11322 to 11381 from sequence 00,
                                                                    as showcased in our teaser. Additionally, We construct our
Fig. 23: Qualitative Comparison with Nerfacto on 3D space.          closed-loop benchmark based on KITTI-360, using both the
The semantic point cloud extracted from Semantic Nerfacto           front two stereo cameras and the side two fisheye cameras.
struggles to faithfully represent the geometry.                     We convert images from the fisheye cameras to perspective
                                                                    images using the model of [48] as the projection model.
KITTI: Following NSG [52] and MARS [68], we select
                                                                    Waymo: We perform experiments on Waymo to compare
frames 140 to 224 from Scene02 and frames 65 to 120 from
                                                                    with StreetGaussian [70] and NeuRAD [61] in extrapo-
Scene06 on KITTI for conducting our experiments.
                                                                    lated views. We select all frames from sequences segment-
vKITTI: Virtual KITTI 2 is a synthetic dataset that closely         10676267326664322837 and segment-9385013624094020582
resembles the scenes present in KITTI. In line with the set-        for the experiments. Every 5th frame is dropped as the test
tings outlined in NSG and MARS, we conduct experiments              frame, and use the front, front-left and front-right cameras
on exactly the same frames from Scene02 and Scene06.                as inputs. Additionally, we construct HUGSIM based on
                 10 steps                                 2000 steps                               5000 steps

Fig. 24: Visualization of Optimization Progress. Our method jointly optimizes the static background and the trajectory
of the dynamic foreground objects. By integrating physical constraints using the unicycle model, our method allows for
recovering a smooth trajectory from noisy 3D bounding boxes. To prevent visual clutter, we exclude point clouds of the
dynamic object and only visualize the bounding boxes.

                                                                 Hard: Scenario (a) simulates a vehicle driving in reverse.
                                                                 Scenario (b) simulates a stationary vehicle ahead and a
                                                                 vehicle reversing in the side lane. Scenario (c) simulates an
                                                                 oncoming aggressive vehicle attempting to attack the ego
                                                                 vehicle.

                                                                 Extreme: Scenario (a) simulates a situation similar to Hard
                                                                 scenario (c), but with the aggressive vehicle having a larger
                                                                 attack frequency and being more likely to select the most
          Fig. 25: Pose comparison with QD-3DT.                  aggressive trajectory. Scenario (b) simulates an aggressive
                                                                 vehicle suddenly changing lanes in front of the ego vehicle.
                                                                 Scenario (c) simulates multiple reverse-driving vehicles.
Waymo using the same settings.
Nuscenes: NuScenes is used to compare our method with
StreetGaussian, NeuRAD, and RoGS [21] in extrapolated
views. We select all frames from sequences 0051, 0411, and       C.2   Implementation of Tested AD Algorithms
0655. Every 5th frame is dropped as the test frame, and we
use all 6 surrounding cameras as inputs. HUGSIM bench-           We implement inference scripts for UniAD [33], VAD
mark is also constructed based on nuScenes. It is important      [35], and LTF [14] to integrate these AD algorithms with
to note that the camera extrinsics of nuScenes are not well      HUGSIM. We build communication bridges based on
refined, so we apply a rigid bundle adjustment to obtain         named pipelines in memory, which transfer data at ultra-
more accurate camera extrinsics.                                 high speed, with nearly no additional time consumption.

PandaSet: Scenes from PandaSet are also part of the              UniAD: UniAD proposes an end-to-end AD algorithm, en-
HUGSIM benchmark. We use all 6 surrounding cameras in            abling flexible intermediate representations and exchanging
PandaSet and drop every 5th frame as the test frame during       multi-task knowledge toward planning. The inference code
scene reconstruction training.                                   of the official UniAD implementation couples observations,
                                                                 CAN-bus data, and ground-truth information together. We
                                                                 re-implement the inference script, which only requires RGB
A PPENDIX C                                                      image observations and sensor poses, based on the official
HUGSIM B ENCHMARK                                                code.
C.1   Scenario Design                                            VAD: VAD proposes an end-to-end vectorized paradigm
We design easy, medium, hard and extreme levels for our          for AD and is developed on the UniAD codebase. We re-
HUGSIM benchmark. The easy scenarios consist of static           implemented the inference script for VAD in a similar way
scenes or replayed dynamic vehicle behaviors. The design         to UniAD.
of scenarios for the medium, hard, and extreme levels is
                                                                 LTF: Latent TransFuser (LTF) is an image-only version of
shown in Fig. 20.
                                                                 Transfuser [14], replacing the LiDAR BEV histogram input
Medium: Scenario (a) simulates a stationary vehicle in the       with a positional encoding. The original version of LTF is
front of ego vehicle. Scenario (b) simulates a vehicle driving   trained on CARLA [19], we use the version implemented in
ahead the ego but may slower than ego vehicle. Scenario (c)      NAVSIM [18] which is trained on nuplan [9], offering better
simulates a vehicle driving ahead but suddenly stops.            alignment with the real world.
                                      UniAD [33]                       VAD [35]                         LTF [14]
                          Easy Medium Hard Extreme          Easy Medium Hard Extreme         Easy Medium Hard Extreme
                NC ↑      0.459 0.379 0.315 0.242           0.333 0.322 0.253 0.171          0.330 0.170 0.181 0.133
                DAC ↑     0.712 0.711 0.754 0.750           0.603 0.604 0.609 0.657          0.646 0.627 0.622 0.633
 KITTI-360 [44] T T C ↑   0.271 0.193 0.131 0.091           0.204 0.162 0.105 0.090          0.290 0.125 0.132 0.080
                COM ↑     0.672 0.652 0.555 0.527           1.000 1.000 1.000 1.000          1.000 0.996 1.000 1.000
                Rc ↑      0.166 0.117 0.122 0.094           0.138 0.125 0.122 0.110          0.245 0.138 0.121 0.111
                HD-Score↑ 0.047 0.019 0.017 0.006           0.029 0.014 0.014 0.008          0.080 0.028 0.017 0.003
                NC ↑      0.900 0.903 0.792 0.512           0.698 0.493 0.526 0.416          0.855 0.544 0.451 0.333
                DAC ↑     0.863 0.903 0.771 0.915           0.568 0.679 0.694 0.726          0.779 0.830 0.861 0.852
 Waymo [58]     TTC ↑     0.862 0.778 0.711 0.461           0.641 0.363 0.437 0.299          0.833 0.518 0.428 0.258
                COM ↑     0.890 0.767 0.712 0.483           1.000 1.000 1.000 1.000          0.992 0.995 0.995 1.000
                Rc ↑      0.784 0.547 0.590 0.326           0.323 0.266 0.259 0.272          0.698 0.371 0.357 0.261
                HD-Score↑ 0.664 0.419 0.401 0.171           0.154 0.093 0.110 0.085          0.546 0.200 0.219 0.071
                NC ↑      0.823 0.761 0.781 0.688           0.765 0.486 0.516 0.467          0.835 0.587 0.513 0.401
                DAC ↑     0.967 0.925 0.929 0.973           0.824 0.917 0.941 0.971          0.858 0.872 0.872 0.928
 Nuscenes [8] T T C ↑     0.787 0.652 0.673 0.519           0.692 0.365 0.376 0.396          0.781 0.527 0.453 0.353
                COM ↑     0.880 0.728 0.729 0.642           1.000 1.000 1.000 1.000          0.994 0.995 1.000 0.993
                Rc ↑      0.703 0.510 0.516 0.291           0.540 0.340 0.383 0.311          0.847 0.542 0.498 0.357
                HD-Score↑ 0.589 0.378 0.365 0.168           0.348 0.132 0.204 0.158          0.616 0.307 0.226 0.171
                NC ↑      0.914 0.851 0.771 0.732           0.847 0.529 0.474 0.388          0.945 0.597 0.481 0.265
                DAC ↑     0.998 0.933 0.987 0.947           0.963 0.990 0.995 0.993          0.987 1.000 0.999 0.991
 Pandaset [69] T T C ↑    0.913 0.792 0.685 0.644           0.793 0.270 0.235 0.251          0.919 0.560 0.467 0.182
                COM ↑     0.871 0.734 0.692 0.689           1.000 1.000 1.000 1.000          1.000 1.000 1.000 1.000
                Rc ↑      0.691 0.473 0.389 0.329           0.548 0.349 0.257 0.229          0.947 0.579 0.498 0.293
                HD-Score↑ 0.647 0.366 0.308 0.226           0.442 0.158 0.087 0.079          0.871 0.450 0.331 0.080
                NC ↑      0.774 0.724 0.665 0.544           0.661 0.457 0.443 0.361          0.741 0.474 0.407 0.283
                DAC ↑     0.885 0.868 0.860 0.896           0.739 0.798 0.810 0.837          0.817 0.832 0.839 0.851
 Average        TTC ↑     0.708 0.604 0.550 0.429           0.582 0.290 0.288 0.259          0.706 0.433 0.370 0.218
                COM ↑     0.828 0.720 0.672 0.585           1.000 1.000 1.000 1.000          0.996 0.997 0.999 0.998
                Rc ↑      0.586 0.412 0.404 0.260           0.387 0.270 0.255 0.230          0.684 0.407 0.369 0.255
                HD-Score↑ 0.487 0.295 0.273 0.143           0.243 0.099 0.104 0.082          0.528 0.246 0.198 0.081

                           TABLE 13: AD Algorithms Evaluating on the HUGSIM Benchmark

A PPENDIX D                                                     sis. To the best of our knowledge, PNF is the only work
BASELINES                                                       that considers the optimization of noisy 3D bounding boxes
                                                                of dynamic objects. In our ablation study, we conduct a
In this section, we discuss the baselines against which we      naı̈ve baseline that optimizes the 3D bounding boxes of
compare our approach, including NSG [52], MARS [68],            each frame independently, which can be considered as a re-
PNF [39], Semantic Nerfacto [60], StreetGaussian [70], Neu-     implementation of PNF’s bounding box optimization in our
RAD [61] and RoGS [21].                                         framework.
NSG: NSG is the pioneering method that introduces the de-
                                                                Semantic Nerfacto: For the evaluation of 3D semantic point
composition of dynamic scenes into static background and
                                                                cloud geometry, we compare our results with Semantic
dynamic foreground components. They propose a learned
                                                                Nerfacto [60] as an alternative to PNF [39]. Nerfacto [60] is
scene graph representation that enables efficient rendering
                                                                an integration of several successful methods that demon-
of novel scene arrangements and viewpoints. However,
                                                                strate strong performance on real data. It incorporates
the official source code provided by NSG often encounters
                                                                camera pose refinement, per-image appearance embedding,
issues when training on KITTI Scene02. Therefore, we utilize
                                                                proposal sampling, scene contraction, and hash encoding
the version implemented by the authors of MARS, which is
                                                                within its pipeline. Additionally, Nerfacto includes a se-
more stable and yields slightly improved results compared
                                                                mantic head in its framework, enabling the generation of
to the original version.
                                                                meaningful semantic maps, as demonstrated in E.2.
MARS: We utilize the latest version of the code provided
by the official MARS repository. This latest version incorpo-   StreetGaussian: StreetGaussian is a concurrent work to
rates bug fixes and includes additional training iterations,    HUGS [83], proposing a dynamic urban scene reconstruc-
resulting in improved performance. In fact, the updated         tion algorithm also based on 3D Gaussian Splatting [37],
version achieves a notable improvement of 3 to 4 dB on          with primary experiments conducted on Waymo. Street-
PSNR compared to the numbers reported in the original           Gaussian requires both LiDAR and RGB data as inputs.
paper.
                                                                NeuRAD: NeuRAD is also a concurrent work to HUGS,
PNF: Since PNF is not open-source, we directly compare          proposing a NeRF-based dynamic urban scene reconstruc-
our method to their submission on the KITTI-360 leader-         tion method. NeuRAD integrates various strategies, achiev-
board regarding novel view appearance & semantic synthe-        ing state-of-the-art performance across many AD datasets.
                              Seq01 mIoUcls ↑       Seq02 mIoUcls ↑        Seq03 mIoUcls ↑         Average mIoUcls ↑
      Ours w/ S2D norm             0.427                 0.363                  0.416                    0.402
      Ours w/ S3D norm             0.544                 0.452                  0.520                    0.505

                         TABLE 14: Comparison on 3D and 2D Semantic Softmax on KITTI-360.
                                                              Details of Comparison with Semantic Nerfacto: While
                                                              Semantic Nerfacto excels at rendering meaningful novel
                                                              view semantic images (as seen in Fig. 22), Fig. 23 shows
                                                              it struggling to accurately reconstruct correct geometry.
                                                              Following the common practice of NeRF-based semantic re-
                                                              construction methods [60], we apply 2D softmax to Semantic
                                                              Nerfacto. when we attempted to apply the 3D Softmax tech-
                                                              nique to Nerfacto, it did not yield better results compared
                                                              to using 2D softmax. The results can be attributed to the
                                                              incorrect of Nerfacto’s 3D geometry. Instead of adjusting 2D
                                                              logits with large-scale logits in 3D, the use of 3D softmax
                                                              prevents the ”cheating” approach by normalizing logits in
                                                              3D space. However, this normalization requirement necessi-
                                                              tates sufficiently accurate geometry for satisfactory results.
                                                              Comparisons with Tracking Methods: To further compare
                                                              with off-the-shelf tracking methods, we show the perfor-
                                                              mance of QD-3DT [32] and our optimized pose initialized
                                                              with [32] in Table 12 and qualitatively illustrate the poses
                                                              of one vehicle in Fig. 25. Our method consistently improves
           w/o LS                        w/ LS                [32] across two KITTI scenes.
Fig. 26: Qualitative Comparison on depth. In the presence
of the semantic loss LS , We set the sky region’s depth       E.3   Additional Ablation Experiments
infinite based on its semantic label.
                                                              3D and 2D Semantic Softmax: We provide more 3D and 2D
                                                              semantic logits softmax comparison in Fig. 21 and Fig. 14.
Like StreetGaussian, NeuRAD requires both LiDAR and           As can be seen, normalizing semantic logits in 3D space
RGB data as inputs. It is worth noting that NeuRAD is the     leads to notable qualitative and quantitative improvement
reconstruction rendering method used in NeuroNCAP [45].       compared to 2D space normalization.
RoGS: RoGS is a concurrent work to HUGSIM, proposing          Improvements on Geometry: We now qualitatively exam-
an efficient method tailored to ground reconstruction based   ine how the semantic loss LS impact the geometry, as shown
on 2D Gaussian Splatting [34] in nuScenes. It requires only   in Fig. 26. Th figure reveals that incorporating the semantic
RGB images for ground reconstruction and uniformly tiles      loss improves the underlying geometry. It’s important to
Gaussians on the ground plane.                                note that when the semantic loss LS is active, the sky region
                                                              of the depth maps in Fig. 26 is set to infinite.

A PPENDIX E
                                                              E.4   Visualization of Optimization Progress
A DDITIONAL E XPERIMENT R ESULTS
                                                              We present the visualization of the optimization progress for
E.1   Time Consumption Breakdown                              both the noisy bounding boxes and the background seman-
Table 10 shows our detailed runtime breakdown as various      tic point cloud in Fig. 24. Using noisy 3D bounding boxes as
components are incrementally enabled. Preparation (Pre.)      input, our approach optimizes both the background and the
contains operations like tile partition and Gaussian sort-    poses of the bounding boxes simultaneously. As evident, the
ing. π denotes volume rendering, and affine denotes affine    application of physical constraints derived from the unicycle
transform. Other components like unicycle model, dynamic      model results in a smooth trajectory for the bounding boxes.
decomposition, and depth rendering are excluded as they
hardly consume any additional time.                           E.5   HUGSIM Benchmark evaluation results
                                                              We present the results of HD-Score and sub-scores N C ,
E.2   Additional Comparison Experiments                       DAC , T T C , COM , and Rc for evaluating UniAD [33], VAD
                                                              [35], and LTF [14] on our HUGSIM benchmark in Table 13.
Dynamic Scene with GT 3D Bounding Boxes: Despite              These results are identical to those in Fig. 18, but presented
not being our primary focus, we additionally provide a        in a more detailed format.
comparison with NSG and MARS using ground truth 3D
trackings. In this setting, our approach demonstrates supe-
rior performance across all test scenes, see Table 11.
