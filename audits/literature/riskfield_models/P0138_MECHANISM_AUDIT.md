# P0138｜Research on local path planning of unmanned vehicles based on improved driving risk field

本地风险场 MD 库编号（与 WAM 编号独立）。来源：用户 `all_md.zip`；原 MD SHA-256 `cfd737c556117a9901482e0791b42eb240f7a7bfc3aba158d28357f4ebf6ff90`。审计级别 **METHOD_CHAIN_SPOT_AUDIT**；PDF 未视觉核验；主文原始公式全量与上下文见本次 `BATCH3_MATH_AUDIT.zip` 的同名 card。

### 场的公式链
机动车方向/车长宽核 L_e Eq.(1) L32–34、虚拟质量 M_iequ Eq.(2) L42–44，再形成车辆场 Eq.(3) L50–52：
```latex
E _ {v} = R _ {d} M _ {i e q u} L _ {e},\tag{3}
```
行人速度条件场 Eq.(4) L74–76：
```latex
E _ {p e d} = \frac {H}{\left(\frac {(x - x _ {o})}{\gamma + k _ {p l} v _ {z}}\right) ^ {2} + \left(\frac {(y - y _ {o})}{\delta + k _ {p w} v _ {c}}\right) ^ {2} + 1},\tag{4}
```
道路/车道风险 Eq.(5) L109–111；总场和虚拟力 Eq.(6),(7) L123–133。
**场源**为周车/行人/道路，ego 查询总场；速度改变二维场形，**没有固定 ego/周车同步未来的直接接触运算**。

**DERIVED / PDF_REQUIRED：** Eq.(1) 包含嵌套平方、单位组合异常；Eq.(5) MinerU 具有可疑指数括号残缺。不能从热力图合理就推断低中风险事件标定有效。
