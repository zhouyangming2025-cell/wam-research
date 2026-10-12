# 第二批候选轨迹风险评价：小规模实验（2026-10-13）

本目录是**独立可复现实验**，不是最终模型，也不修改 WAM 主程序状态。核心结论见 [RESEARCH_REPORT_CN.md](RESEARCH_REPORT_CN.md)。真实 INTERACTION 10Hz 原记录摘录及原始源 blob SHA 已记录在研究报告；不是模拟器生成轨迹。原 Gaussian 正式冻结文件未获取，所有复刻分数必须标 `V0*`。

本目录文字、CSV 与脚本可通过 `python run_all.py` 离线重现（需 numpy/pandas/shapely/matplotlib）。原始完整图件和带图件的 `index.html` 保存在独立完整 ZIP 工件中，不作为 GitHub 主研究入口。**不会重训任何模型、不下载全量数据、不改 benchmark 评分。**

仓库独立实验分支用于人工验收，研究结论必须区分真实日志、GT future Oracle、解析构造和原始冻结核是否对齐。
