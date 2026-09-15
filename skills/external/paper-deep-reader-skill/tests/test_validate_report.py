import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_report import (
    Results,
    infer_mode,
    split_sections,
    validate_manifest,
    validate_source_map,
    validate_structure,
)


def explain_report(
    *,
    include_terms: bool = True,
    include_example: bool = True,
    include_reasoning_bridge: bool = True,
) -> str:
    terms = (
        "### 2.1 先补齐必要概念\n"
        "**状态**：可以理解为系统此刻保存的信息；在本文中用于决定下一步更新。"
        if include_terms
        else "系统保存信息后继续运行。"
    )
    example = (
        "### 3.2 最小例子\n一个样本先被更新，再进入下一轮。"
        if include_example
        else "系统按顺序更新状态。"
    )
    bridge = (
        "这意味着误差下降来自闭环更新，因此支持核心机制主张。"
        if include_reasoning_bridge
        else "实验记录了误差下降。"
    )
    return f"""# 示例论文：深度解读

> **交付模式**：explain

## 1. 核心思想一句话总结

**一句话**：论文用闭环更新降低误差，并由受控实验验证。[论文 §1，PDF p.1]

## 2. 论文背景与动机

{terms}

旧方法无法根据新误差修正状态，因此需要闭环。

## 3. 核心方法详解

### 3.1 总体框架

输入经过更新器得到状态，再输出预测。

{example}

## 4. 实验与结果分析

受控比较提供**中等**支持。[表2，PDF p.4]

{bridge}

该结果不能说明开放环境中同样有效，边界是封闭任务。

## 5. 论文的贡献与影响

论文贡献是闭环更新。未来方向是检验开放环境；最小验证是在新分布上测试。

## 6. 结论

核心价值是把误差重新送回更新器，但外推边界仍未验证。

**最终判断**：值得继续阅读。[论文 §5，PDF p.7]
"""


def source_map(delivery: str = "explain") -> dict:
    return {
        "schema_version": 5,
        "paper": {
            "title": "示例",
            "sources": ["local"],
            "page_convention": "PDF pages",
        },
        "reader_profile": {
            "domain": "computer-science-ai",
            "selected_lenses": ["computer-science-ai"],
            "audience": "broad-to-expert",
            "entry_level": "novice",
            "technical_ceiling": "doctoral",
            "goal": "understand",
            "depth": "deep",
            "delivery": delivery,
            "language": "zh-CN",
        },
        "explanation": {
            "strategy": "intuition-to-precision",
            "define_terms_on_first_use": True,
            "report_structure": "six-section",
            "key_visual_policy": "all-key-visuals",
        },
        "execution": {
            "visual_mode": "visual",
            "visual_verification": "complete",
            "text_evidence_sources": [],
        },
        "visual_coverage": {
            "total_numbered": 1,
            "key": 1,
            "key_explained": 1,
        },
        "claims": [
            {
                "id": "C1",
                "claim": "示例主张",
                "status": "unsupported",
                "evidence": [],
            }
        ],
    }


def visual_manifest(*, selected: bool = True) -> dict:
    return {
        "schema_version": 4,
        "analysis_mode": "visual",
        "selection_policy": "all-key-visuals-in-explain-and-audit",
        "visuals": [
            {
                "kind": "figure",
                "number": "1",
                "label": "Figure 1",
                "key": True,
                "classification_reason": "该图承载核心结论",
                "selected_for_report": selected,
                "report_role": "evidence" if selected else None,
                "selection_reason": "该图直接承载主结果" if selected else "",
                "visual_verification": "complete",
                "crop_review_required": False,
                "selected_asset": "figure-1.png",
            }
        ],
    }


def visual_report(*, include_bridge: bool = True) -> str:
    bridge = (
        "**为什么这个观察支持正文判断？** 这意味着闭环确实降低误差，因此支持核心主张。"
        if include_bridge
        else "误差数值已记录。"
    )
    return f"""# 图表测试

## 4. 实验与结果分析

### 图1：闭环是否降低误差

**这张图回答什么问题？** 闭环更新是否有效。

**先看哪里、怎么读？** 先看横轴轮次、纵轴误差和两条图例；误差越低越好。

![图1：闭环与开环误差比较](figure-1.png)

**关键观察。** 结果显示闭环误差低于开环。

{bridge}

**它不能说明什么？** 不能说明开放环境也有效，这是外推边界。
"""


def text_only_visual_report() -> str:
    return """# 纯文本图表测试

### 图1：文本证据卡

**这张图回答什么问题？** 闭环更新是否有效。

**如何读？** 先比较正文报告的两组误差，误差越低越好。

**关键观察。** 作者报告闭环误差低于开环。

**为什么这个观察支持正文判断？** 这意味着反馈信息帮助了更新，因此支持核心主张。

**它不能说明什么？** 不能核验曲线、颜色或面板，也不能说明开放环境有效。
"""


class StructureTests(unittest.TestCase):
    def validate(self, text: str) -> Results:
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.md"
            report.write_text(text, encoding="utf-8")
            sections, numbers = split_sections(text)
            results = Results()
            validate_structure(
                report,
                text,
                sections,
                numbers,
                "explain",
                results,
            )
            return results

    def test_bold_mode_marker_is_detected(self) -> None:
        mode = infer_mode("> **交付模式**：audit", "auto", [1, 2, 3, 4, 5, 6])
        self.assertEqual(mode, "audit")

    def test_six_sections_default_to_explain(self) -> None:
        mode = infer_mode("# 报告", "auto", [1, 2, 3, 4, 5, 6])
        self.assertEqual(mode, "explain")

    def test_numbered_section_stops_before_appendix(self) -> None:
        text = "\n".join(
            [f"## {number}. S{number}\n正文" for number in range(1, 7)]
        ) + "\n## 附录 A\n" + "长附录" * 50
        sections, numbers = split_sections(text)
        self.assertEqual(numbers, [1, 2, 3, 4, 5, 6])
        self.assertEqual(sections[6], "正文")

    def test_valid_explain_structure_has_no_errors(self) -> None:
        results = self.validate(explain_report())
        self.assertEqual(results.errors, [])

    def test_explain_requires_term_onboarding(self) -> None:
        results = self.validate(explain_report(include_terms=False))
        self.assertTrue(any("terminology" in error for error in results.errors))

    def test_explain_requires_worked_example(self) -> None:
        results = self.validate(explain_report(include_example=False))
        self.assertTrue(any("example" in error for error in results.errors))

    def test_explain_requires_evidence_reasoning_bridge(self) -> None:
        results = self.validate(explain_report(include_reasoning_bridge=False))
        self.assertTrue(any("reasoning bridge" in error for error in results.errors))


class EvidenceAssetTests(unittest.TestCase):
    def test_schema_v4_requires_visual_classification_reason(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = root / "report.md"
            report.write_text(visual_report(), encoding="utf-8")
            (root / "figure-1.png").write_bytes(b"fake")
            manifest = visual_manifest()
            manifest["visuals"][0].pop("classification_reason")
            manifest_path = root / "visual_manifest.json"
            manifest_path.write_text(
                json.dumps(manifest, ensure_ascii=False), encoding="utf-8"
            )
            results = Results()
            validate_manifest(
                manifest_path,
                report,
                report.read_text(encoding="utf-8"),
                results,
                mode="explain",
            )
            self.assertTrue(
                any("classification" in error for error in results.errors)
            )

    def test_key_visual_requires_selection_in_explain(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = root / "report.md"
            report.write_text("# 报告\n\n图1说明闭环。\n", encoding="utf-8")
            (root / "figure-1.png").write_bytes(b"fake")
            manifest_path = root / "visual_manifest.json"
            manifest_path.write_text(
                json.dumps(visual_manifest(selected=False), ensure_ascii=False),
                encoding="utf-8",
            )
            results = Results()
            validate_manifest(
                manifest_path,
                report,
                report.read_text(encoding="utf-8"),
                results,
                mode="explain",
            )
            self.assertTrue(any("Every key visual" in error for error in results.errors))

    def test_valid_key_visual_has_interleaved_explanation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = root / "report.md"
            report.write_text(visual_report(), encoding="utf-8")
            (root / "figure-1.png").write_bytes(b"fake")
            manifest_path = root / "visual_manifest.json"
            manifest_path.write_text(
                json.dumps(visual_manifest(), ensure_ascii=False), encoding="utf-8"
            )
            results = Results()
            validate_manifest(
                manifest_path,
                report,
                report.read_text(encoding="utf-8"),
                results,
                mode="explain",
            )
            self.assertEqual(results.errors, [])

    def test_key_visual_requires_reasoning_bridge(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = root / "report.md"
            report.write_text(visual_report(include_bridge=False), encoding="utf-8")
            (root / "figure-1.png").write_bytes(b"fake")
            manifest_path = root / "visual_manifest.json"
            manifest_path.write_text(
                json.dumps(visual_manifest(), ensure_ascii=False), encoding="utf-8"
            )
            results = Results()
            validate_manifest(
                manifest_path,
                report,
                report.read_text(encoding="utf-8"),
                results,
                mode="explain",
            )
            self.assertTrue(any("reasoning bridge" in error for error in results.errors))

    def test_text_only_key_visual_uses_interleaved_evidence_card(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = root / "report.md"
            report.write_text(text_only_visual_report(), encoding="utf-8")
            text_asset = root / "text" / "visuals" / "figure-1.md"
            text_asset.parent.mkdir(parents=True)
            text_asset.write_text("文字证据", encoding="utf-8")
            manifest = {
                "schema_version": 4,
                "analysis_mode": "text-only",
                "selection_policy": "all-key-visuals-in-explain-and-audit",
                "visuals": [
                    {
                        "kind": "figure",
                        "number": "1",
                        "label": "Figure 1",
                        "key": True,
                        "classification_reason": "该图承载核心结论",
                        "selected_for_report": True,
                        "report_role": "evidence",
                        "selection_reason": "该图承载主结果",
                        "visual_verification": "not-performed",
                        "crop_review_required": True,
                        "candidate_crop": None,
                        "text_asset": "text/visuals/figure-1.md",
                        "text_review": {
                            "status": "complete",
                            "sources": ["caption", "body-reference"],
                            "notes": "作者报告闭环误差更低",
                            "limitations": "未核验曲线和面板",
                        },
                    }
                ],
            }
            manifest_path = root / "visual_manifest.json"
            manifest_path.write_text(
                json.dumps(manifest, ensure_ascii=False), encoding="utf-8"
            )
            results = Results()
            validate_manifest(
                manifest_path,
                report,
                report.read_text(encoding="utf-8"),
                results,
                mode="explain",
                text_only=True,
            )
            self.assertEqual(results.errors, [])


class SourceMapTests(unittest.TestCase):
    def test_valid_v5_source_map(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source_map.json"
            path.write_text(
                json.dumps(source_map(), ensure_ascii=False), encoding="utf-8"
            )
            results = Results()
            validate_source_map(path, results, mode="explain")
            self.assertEqual(results.errors, [])

    def test_source_map_delivery_must_match_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source_map.json"
            path.write_text(
                json.dumps(source_map(), ensure_ascii=False), encoding="utf-8"
            )
            results = Results()
            validate_source_map(path, results, mode="audit")
            self.assertTrue(any("conflicts" in error for error in results.errors))

    def test_schema_v4_source_map_remains_compatible(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = source_map()
            data["schema_version"] = 4
            data["reader_profile"].pop("entry_level")
            data["reader_profile"].pop("technical_ceiling")
            data.pop("explanation")
            data.pop("visual_coverage")
            path = Path(directory) / "source_map.json"
            path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            results = Results()
            validate_source_map(path, results, mode="explain")
            self.assertEqual(results.errors, [])

    def test_source_map_requires_all_key_visuals_explained(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = source_map()
            data["visual_coverage"]["key_explained"] = 0
            path = Path(directory) / "source_map.json"
            path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            results = Results()
            validate_source_map(path, results, mode="explain")
            self.assertTrue(any("every key visual" in error for error in results.errors))


if __name__ == "__main__":
    unittest.main()
