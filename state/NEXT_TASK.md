# NEXT_TASK

## 唯一下一任务

> **对固定 12 篇逐篇重核原文与现有 deep analysis / source audit；只有在每条结论可追溯后，才原位修订唯一的 `landscape/WAM_COMPARISON_MATRIX_V1.md`。**

不新建路线表、extension、branch 或 taxonomy 版本。`WAM_COMPARISON_MATRIX_V1.md` 目前只是五篇锚点的历史基线，不是当前结论；若证据不足，保留 `UNKNOWN`，不能用旧 V1.1–V1.3 快照补齐。

## 每篇必须先核对的事实

```text
1. 训练图：未来/世界对象、监督、梯度与教师
2. 部署图：真实保留的模块、输入、动作接口与删去的模块
3. future 对象：视觉、BEV、latent、关系状态、候选后果或仅训练目标
4. candidate / score / selector：是否存在，谁拥有最终行动选择权
5. artifact / mode / paper-code 版本边界
6. 评测与反应性边界
```

## 允许的结果

```text
可证实的论文事实 / 代码事实
有边界的跨论文比较
明确标出的 OUR INFERENCE
UNKNOWN / NOT REPORTED
```

## 不允许的结果

```text
以“是否有 world model”“是否预测未来”“是否联合训练”直接命名路线；
把训练期未来监督写成在线 rollout；
把视频解码、离线可视化或固定 logged future 写成部署期反应式推演；
把同一论文不同 artifact/mode 压成一行；
先写路线名、再补证据。
```

## 停止条件

12 篇的证据边界均已重核；保留的唯一比较矩阵可清楚区分论文事实、代码事实、推断与未知；只有出现至少两个可复核成员的因果分叉，才讨论技术路线。