#!/usr/bin/env python3
"""校验六部分、图文交错且来源可追溯的论文解读报告。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote


SECTION_RE = re.compile(r"^##\s+([1-9]\d*)(?:[.、])?\s*(.+?)\s*$", re.MULTILINE)
H2_RE = re.compile(r"^##\s+\S.*$", re.MULTILINE)
REPORT_BLOCK_HEADING_RE = re.compile(r"^#{2,3}\s+\S.*$", re.MULTILINE)
MODE_RE = re.compile(
    r"(?:解读模式|交付模式|report\s+mode)\s*(?:\*\*|__)?\s*[：:]\s*"
    r"(?:\*\*|__)?\s*`?(brief|explain|audit|targeted)`?",
    re.IGNORECASE,
)
SUPPORT_RE = re.compile(
    r"强(?:支持)?|中等|部分支持|弱(?:支持)?|不支持|"
    r"strong|moderate|partial|weak|unsupported",
    re.IGNORECASE,
)
BOUNDARY_RE = re.compile(
    r"边界|局限|限制|失效|不能推出|不能说明|不适用|"
    r"boundary|limitation|cannot|failure|fails?\s+when",
    re.IGNORECASE,
)
EXAMPLE_RE = re.compile(
    r"最小例子|具体例子|示例|例如|思想实验|"
    r"minimal\s+example|worked\s+example|for\s+example|case\s+study",
    re.IGNORECASE,
)
TERM_ONBOARDING_RE = re.compile(
    r"必要概念|关键概念|术语|前置知识|先认识|先补齐|"
    r"key\s+concepts?|terminology|prerequisites?",
    re.IGNORECASE,
)
DEFINITION_RE = re.compile(
    r"\*\*[^*\n]{1,80}\*\*\s*[：:]|"
    r"是指|指的是|也就是|可以理解为|在本文中(?:负责|表示|用于)|"
    r"means?|refers?\s+to|in\s+this\s+paper",
    re.IGNORECASE,
)
READING_GUIDE_RE = re.compile(
    r"回答什么|先看(?:哪里|什么)|如何读|怎么读|阅读任务|"
    r"横轴|纵轴|图例|单位|第.{0,8}(?:行|列|面板)|"
    r"what\s+to\s+look|how\s+to\s+read|x[- ]axis|y[- ]axis|legend",
    re.IGNORECASE,
)
OBSERVATION_RE = re.compile(
    r"关键观察|主要发现|结果显示|观察到|可见|数值|趋势|高于|低于|增加|下降|差异|"
    r"key\s+observation|results?\s+show|higher|lower|increase|decrease",
    re.IGNORECASE,
)
REASONING_BRIDGE_RE = re.compile(
    r"为什么.{0,24}(?:支持|说明)|这意味着|因此.{0,24}(?:支持|说明)|"
    r"由此.{0,24}(?:支持|说明)|观察.{0,24}(?:主张|结论)|推理桥|"
    r"(?:这一|该)(?:结果|差异|观察|现象)"
    r"(?![^。；\n]{0,8}不能).{0,24}(?:表明|说明|支持|证明)|"
    r"之所以.{0,40}是因为|"
    r"why.{0,24}(?:support|show)|this\s+(?:means|supports|suggests)|therefore",
    re.IGNORECASE,
)
FUTURE_RE = re.compile(
    r"未来|后续|下一步|值得探索|可检验问题|最小验证|"
    r"future|next\s+step|open\s+question|minimal\s+(?:test|experiment)",
    re.IGNORECASE,
)
SECTION_TITLE_PATTERNS = {
    1: re.compile(r"核心思想|一句话|elevator\s+pitch", re.IGNORECASE),
    2: re.compile(r"背景|动机|background|motivation", re.IGNORECASE),
    3: re.compile(
        r"方法|模型|理论|研究设计|core\s+(?:method|model)|study\s+design",
        re.IGNORECASE,
    ),
    4: re.compile(r"实验|结果|证据|experiments?|results?|evidence", re.IGNORECASE),
    5: re.compile(r"贡献|影响|contribution|impact", re.IGNORECASE),
    6: re.compile(r"结论|总结|conclusion", re.IGNORECASE),
}
DELIVERY_MODES = {"brief", "explain", "audit", "targeted"}
REPORT_VISUAL_ROLES = {
    "orientation",
    "mechanism",
    "comparison",
    "evidence",
    "boundary",
}
IMAGE_RE = re.compile(
    r"!\[(?P<alt>[^\]]*)\]\("
    r"(?P<path><[^>]+>|[^)\s]+)"
    r"(?:\s+[\"'][^\"']*[\"'])?\)"
)
PLACEHOLDER_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bTODO\b",
        r"\bTBD\b",
        r"待补(?:充|图|写)?",
        r"待填写",
        r"待插(?:入|图)?",
        r"\[论文标题\]",
        r"\[作者\]",
        r"\[official URL\]",
        r"\[(?:\.{3}|…)\]",
        r"<paper[-_ ]?(?:slug|title|path)>",
    )
]
ANCHOR_RE = re.compile(
    r"(?:图|表|附图|附表|补充图|补充表|图版|式|算法|定理|定义|命题|引理|案例|附录)"
    r"\s*[A-Z]?\s*\d+(?:\([a-z0-9]+\))?"
    r"|(?:Figure|Fig\.?|Table|Scheme|Plate|Box|Chart|Eq\.?|Equation|Algorithm|"
    r"Theorem|Definition|Proposition|Lemma|Case|Appendix)\s*[A-Z]?\s*\d+"
    r"|PDF\s*p\.\s*\d+"
    r"|§\s*\d+(?:\.\d+)*",
    re.IGNORECASE,
)
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
WORD_RE = re.compile(r"\b[\w'-]+\b", re.UNICODE)
TEXT_ONLY_DISCLOSURE_RE = re.compile(
    r"无视觉(?:模式|模型)|视觉内容(?:未|没有)(?:直接)?核验"
    r"|text[- ]only mode|visual (?:content|pixels?) (?:was |were )?not (?:directly )?verified",
    re.IGNORECASE,
)


class Results:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)


def strip_markdown(value: str) -> str:
    value = re.sub(r"```.*?```", " ", value, flags=re.DOTALL)
    value = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"[*_`>#~]", "", value)
    return re.sub(r"\s+", " ", value).strip()


def visible_length(value: str) -> int:
    plain = strip_markdown(value)
    return len(
        re.sub(
            r"[\s，。；：、“”‘’！？,.!?;:/\\|()\[\]{}<>《》—–\-+]",
            "",
            plain,
        )
    )


def split_sections(text: str) -> tuple[dict[int, str], list[int]]:
    matches = list(SECTION_RE.finditer(text))
    level_two_starts = [match.start() for match in H2_RE.finditer(text)]
    numbers = [int(match.group(1)) for match in matches]
    sections: dict[int, str] = {}
    for match in matches:
        number = int(match.group(1))
        end = next(
            (start for start in level_two_starts if start > match.start()),
            len(text),
        )
        sections[number] = text[match.end():end].strip()
    return sections, numbers


def numbered_section_titles(text: str) -> dict[int, str]:
    return {
        int(match.group(1)): match.group(2).strip()
        for match in SECTION_RE.finditer(text)
    }


def infer_mode(text: str, requested: str, section_numbers: list[int]) -> str:
    if requested != "auto":
        return requested
    match = MODE_RE.search(text)
    if match:
        return match.group(1).lower()
    if re.search(r"本报告为快读|快读模式|速览|brief\s+mode", text, re.IGNORECASE):
        return "brief"
    if section_numbers == [1, 2, 3, 4, 5, 6]:
        return "explain"
    return "explain"


def reading_units(value: str) -> int:
    """Count CJK characters plus non-CJK words as rough reading units."""
    plain = strip_markdown(value)
    cjk_count = len(CJK_RE.findall(plain))
    non_cjk = CJK_RE.sub(" ", plain)
    return cjk_count + len(WORD_RE.findall(non_cjk))


def first_content_line(section: str) -> str:
    for line in section.splitlines():
        candidate = strip_markdown(line)
        if candidate and not candidate.startswith("来源"):
            return candidate
    return ""


def resolve_local_target(report_path: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().strip("<>")
    if target.startswith(("http://", "https://", "data:", "#")):
        return None
    target = unquote(target.split("#", 1)[0])
    return (report_path.parent / target).resolve()


def validate_structure(
    report_path: Path,
    text: str,
    sections: dict[int, str],
    section_numbers: list[int],
    mode: str,
    results: Results,
    text_only: bool = False,
) -> None:
    if not re.search(r"^#\s+\S", text, re.MULTILINE):
        results.error("Missing level-1 report title.")

    if len(section_numbers) != len(set(section_numbers)):
        results.error(f"Numbered top-level sections repeat: {section_numbers}.")

    if mode in {"explain", "audit"}:
        if section_numbers != [1, 2, 3, 4, 5, 6]:
            results.error(
                "Explain/audit reports must contain the six numbered sections "
                f"1..6 in order; found {section_numbers or 'none'}."
            )
        for number in range(1, 7):
            if not strip_markdown(sections.get(number, "")):
                results.error(f"Section {number} is empty.")

        titles = numbered_section_titles(text)
        for number, expected in SECTION_TITLE_PATTERNS.items():
            title = titles.get(number, "")
            if title and not expected.search(title):
                results.error(
                    f"Section {number} title does not match the six-part report "
                    f"contract: {title!r}."
                )

    if mode in {"explain", "audit"}:
        pitch = first_content_line(sections.get(1, ""))
        if not pitch:
            results.error("Section 1 has no one-sentence paper claim.")
        else:
            pitch_body = re.sub(
                r"^(?:一句话|核心思想一句话总结|elevator\s+pitch)\s*[：:]\s*",
                "",
                pitch,
                flags=re.IGNORECASE,
            )
            pitch_length = visible_length(pitch_body)
            is_cjk_pitch = len(CJK_RE.findall(pitch_body)) >= 5
            if is_cjk_pitch and pitch_length > 50:
                results.error(
                    "Chinese elevator pitch exceeds 50 visible characters "
                    f"({pitch_length})."
                )
            elif not is_cjk_pitch:
                pitch_words = len(WORD_RE.findall(strip_markdown(pitch_body)))
                if pitch_words > 30:
                    results.error(
                        f"Elevator pitch exceeds 30 words ({pitch_words})."
                    )

        onboarding_text = sections.get(2, "") + "\n" + sections.get(3, "")
        if not TERM_ONBOARDING_RE.search(onboarding_text):
            results.error(
                "Sections 2–3 must explicitly introduce necessary concepts, "
                "terminology, or prerequisites for a zero-background reader."
            )
        if not DEFINITION_RE.search(onboarding_text):
            results.error(
                "No plain-language first-use definition was detected for a key term."
            )

        mechanism_text = sections.get(3, "")
        if not EXAMPLE_RE.search(mechanism_text):
            results.error(
                "The mechanism explanation must include a concrete or minimal example."
            )

        evidence_text = sections.get(4, "")
        if not SUPPORT_RE.search(evidence_text):
            results.error(
                "The evidence section must grade at least one claim as strong, "
                "moderate, weak, or unsupported."
            )
        if not REASONING_BRIDGE_RE.search(evidence_text):
            results.error(
                "Section 4 must explain at least one evidence reasoning bridge "
                "from observation to claim."
            )

        boundary_text = sections.get(4, "") + "\n" + sections.get(6, "")
        if not BOUNDARY_RE.search(boundary_text):
            results.error("The report must state a claim boundary or failure condition.")
        if not FUTURE_RE.search(sections.get(5, "")):
            results.error(
                "Section 5 must include concrete future directions or next-step tests."
            )
        if not re.search(r"最终判断|是否值得|final\s+judg|recommend", boundary_text, re.I):
            results.warn("Section 6 should end with an explicit research-use judgment.")

    budget_text = text
    if mode in {"explain", "audit"}:
        budget_text = "\n".join(sections.get(number, "") for number in range(1, 7))
    units = reading_units(budget_text)
    budgets = {
        "brief": (180, 1800),
        "explain": (1400, 12000),
        "audit": (1400, 15000),
        "targeted": (30, 3000),
    }
    minimum, maximum = budgets[mode]
    if units < minimum:
        results.warn(
            f"The {mode} report is unusually short ({units} reading units; "
            f"expected at least {minimum})."
        )
    if units > maximum:
        scope = "audit main report" if mode == "audit" else f"{mode} report"
        results.warn(
            f"The {scope} is unusually long and may contain repetition "
            f"({units} reading units; target maximum {maximum})."
        )

    if text_only and not TEXT_ONLY_DISCLOSURE_RE.search(text):
        results.error(
            "Text-only reports must explicitly disclose that visual content was "
            "not directly verified."
        )

    for pattern in PLACEHOLDER_PATTERNS:
        match = pattern.search(text)
        if match:
            results.error(f"Unresolved placeholder found: {match.group(0)!r}.")

    if text.count("$$") % 2:
        results.error("Unbalanced display-math delimiter '$$'.")

    anchor_count = len(ANCHOR_RE.findall(text))
    minimum_anchors = {
        "brief": 1,
        "explain": 6,
        "audit": 8,
        "targeted": 1,
    }[mode]
    if anchor_count < minimum_anchors:
        results.warn(
            f"Only {anchor_count} source-anchor occurrence(s) found; "
            f"expected at least {minimum_anchors}."
        )

    images = list(IMAGE_RE.finditer(text))
    for image in images:
        alt = image.group("alt").strip()
        raw_target = image.group("path")
        if not alt:
            results.error(f"Image has empty alt text: {raw_target}")
        local_path = resolve_local_target(report_path, raw_target)
        if local_path is not None and not local_path.is_file():
            results.error(f"Referenced image does not exist: {raw_target}")
    results.note(f"Found {len(images)} Markdown image reference(s).")


def label_pattern(kind: str, number: str) -> re.Pattern[str]:
    escaped = re.escape(number).replace(r"\ ", r"\s*")
    if kind == "figure":
        prefix = (
            r"(?:图|附图|补充图|(?:Extended\s+Data|Supplementary|Supplemental)\s+"
            r"(?:Figure|Fig\.?)|Figure|Fig\.?)"
        )
    elif kind == "table":
        prefix = (
            r"(?:表|附表|补充表|(?:Extended\s+Data|Supplementary|Supplemental)\s+"
            r"Table|Table)"
        )
    elif kind == "scheme":
        prefix = r"(?:Scheme|方案)"
    elif kind == "plate":
        prefix = r"(?:Plate|图版)"
    elif kind == "box":
        prefix = r"(?:Box|框)"
    elif kind == "chart":
        prefix = r"(?:Chart|图表)"
    else:
        prefix = r"(?:算法|Algorithm)"
    return re.compile(prefix + r"\s*" + escaped + r"(?!\d)", re.IGNORECASE)


def resolved_image_paths(report_path: Path, text: str) -> set[Path]:
    paths: set[Path] = set()
    for match in IMAGE_RE.finditer(text):
        path = resolve_local_target(report_path, match.group("path"))
        if path is not None:
            paths.add(path)
    return paths


def image_match_for_path(
    report_path: Path,
    text: str,
    asset_path: Path,
) -> re.Match[str] | None:
    for match in IMAGE_RE.finditer(text):
        resolved = resolve_local_target(report_path, match.group("path"))
        if resolved == asset_path:
            return match
    return None


def validate_visual_explanation_context(
    report_path: Path,
    text: str,
    results: Results,
    *,
    kind: str,
    number: str,
    label: str,
    asset_path: Path | None,
    text_only: bool,
) -> None:
    if text_only or asset_path is None:
        matches = list(label_pattern(kind, number).finditer(text))
    else:
        image_match = image_match_for_path(report_path, text, asset_path)
        matches = [image_match] if image_match is not None else []
    if not matches:
        return

    heading_starts = [item.start() for item in REPORT_BLOCK_HEADING_RE.finditer(text)]
    image_starts = [item.start() for item in IMAGE_RE.finditer(text)]

    contexts: list[tuple[str, str]] = []
    for match in matches:
        previous_heading = max(
            (start for start in heading_starts if start <= match.start()),
            default=max(0, match.start() - 1600),
        )
        next_heading = next(
            (start for start in heading_starts if start > match.start()),
            len(text),
        )
        next_image = next(
            (start for start in image_starts if start > match.start()),
            len(text),
        )
        context_end = min(next_heading, next_image, match.end() + 3200)
        before = text[max(previous_heading, match.start() - 1600):match.start()]
        after = text[match.end():context_end]
        contexts.append((before, after))

    def context_score(context: tuple[str, str]) -> int:
        before, after = context
        reading_context = before + "\n" + after[:500]
        return sum(
            (
                bool(READING_GUIDE_RE.search(reading_context)),
                bool(OBSERVATION_RE.search(after)),
                bool(REASONING_BRIDGE_RE.search(after)),
                bool(BOUNDARY_RE.search(after)),
            )
        )

    before, after = max(contexts, key=context_score)
    reading_context = before + "\n" + after[:500]
    if not READING_GUIDE_RE.search(reading_context):
        results.error(
            f"Key visual lacks nearby reading guidance (question/where to look): {label}."
        )
    if not OBSERVATION_RE.search(after):
        results.error(f"Key visual lacks a nearby concrete observation: {label}.")
    if not REASONING_BRIDGE_RE.search(after):
        results.error(
            f"Key visual lacks a nearby observation-to-claim reasoning bridge: {label}."
        )
    if not BOUNDARY_RE.search(after):
        results.error(
            f"Key visual lacks a nearby statement of what it cannot establish: {label}."
        )


def load_json(path: Path, results: Results, label: str) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        results.error(f"{label} not found: {path}")
    except json.JSONDecodeError as exc:
        results.error(f"{label} is invalid JSON ({path}): {exc}")
    return None


def unresolved_json_paths(value: Any, path: str = "$") -> list[str]:
    unresolved: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            unresolved.extend(unresolved_json_paths(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            unresolved.extend(unresolved_json_paths(child, f"{path}[{index}]"))
    elif isinstance(value, str) and value.strip().upper() in {
        "REPLACE_ME",
        "TODO",
        "TBD",
    }:
        unresolved.append(path)
    return unresolved


def validate_manifest(
    manifest_path: Path,
    report_path: Path,
    text: str,
    results: Results,
    mode: str = "explain",
    text_only: bool = False,
) -> None:
    manifest = load_json(manifest_path, results, "Visual manifest")
    if not isinstance(manifest, dict):
        return

    manifest_mode = str(manifest.get("analysis_mode", "")).strip()
    if text_only and manifest_mode != "text-only":
        results.error(
            "Text-only validation requires a manifest with analysis_mode='text-only'."
        )
    if not text_only and manifest_mode == "text-only":
        results.error(
            "Manifest was generated in text-only mode; rerun validation with --text-only."
        )
    try:
        manifest_schema_version = int(manifest.get("schema_version", 1))
    except (TypeError, ValueError):
        manifest_schema_version = 1

    visuals = manifest.get("visuals", [])
    if not isinstance(visuals, list):
        results.error("Visual manifest field 'visuals' must be a list.")
        return

    report_images = resolved_image_paths(report_path, text)
    allowed_text_only_images: set[Path] = set()
    unclassified = 0
    selection_unclassified = 0
    key_count = 0
    selected_count = 0

    for index, visual in enumerate(visuals, start=1):
        if not isinstance(visual, dict):
            results.error(f"Visual manifest item {index} is not an object.")
            continue
        kind = str(visual.get("kind", ""))
        number = str(visual.get("number", ""))
        label = str(visual.get("label") or f"{kind} {number}")
        if not kind or not number:
            results.error(f"Visual manifest item {index} lacks kind/number.")
            continue

        key = visual.get("key")
        if not isinstance(key, bool):
            unclassified += 1
            continue
        if (
            manifest_schema_version >= 4
            and not str(visual.get("classification_reason", "")).strip()
        ):
            results.error(
                f"Visual has no reason for its key/non-key classification: {label}."
            )

        selected_value = visual.get("selected_for_report")
        if manifest_schema_version >= 3 and not isinstance(selected_value, bool):
            selection_unclassified += 1
            selected = False
        elif isinstance(selected_value, bool):
            selected = selected_value
        else:
            # Legacy manifests inferred selection from report presence.
            selected = key and bool(label_pattern(kind, number).search(text))

        if mode in {"explain", "audit"} and key and not selected:
            results.error(
                f"Every key visual must be selected in {mode} mode: {label}."
            )

        mentioned = bool(label_pattern(kind, number).search(text))
        if mode == "audit" and not mentioned:
            results.error(f"Audit appendix omits numbered visual: {label}.")
        elif selected and not mentioned:
            results.error(f"Selected visual is absent from report: {label}.")

        if selected:
            selected_count += 1
            if not key:
                results.error(
                    f"Visual selected_for_report=true must also have key=true: {label}."
                )
            report_role = str(visual.get("report_role", "")).strip()
            if manifest_schema_version >= 3 and report_role not in REPORT_VISUAL_ROLES:
                results.error(
                    f"Selected visual has invalid report_role {report_role!r}: {label}."
                )
            if (
                manifest_schema_version >= 3
                and not str(visual.get("selection_reason", "")).strip()
            ):
                results.error(
                    f"Selected visual has no understanding-focused selection_reason: "
                    f"{label}."
                )
        if not key:
            continue

        key_count += 1
        embed_required = selected or mode == "audit"
        if text_only:
            visual_verification = str(
                visual.get("visual_verification", "")
            ).strip()
            if visual_verification not in {
                "not-performed",
                "externally-verified",
            }:
                results.error(
                    f"Key visual has invalid text-only visual_verification: {label}."
                )

            text_asset = visual.get("text_asset")
            if not text_asset:
                results.error(f"Key visual has no text_asset: {label}.")
            else:
                text_asset_path = (
                    manifest_path.parent / str(text_asset)
                ).resolve()
                if not text_asset_path.is_file():
                    results.error(
                        f"Text evidence asset for {label} does not exist: "
                        f"{text_asset_path}"
                    )

            text_review = visual.get("text_review")
            if not isinstance(text_review, dict):
                results.error(f"Key visual has no text_review object: {label}.")
            else:
                if text_review.get("status") != "complete":
                    results.error(f"Key visual text review is incomplete: {label}.")
                sources = text_review.get("sources")
                if (
                    not isinstance(sources, list)
                    or not sources
                    or not all(
                        isinstance(source, str) and source.strip()
                        for source in sources
                    )
                ):
                    results.error(
                        f"Key visual text review has no valid sources: {label}."
                    )
                if not str(text_review.get("notes", "")).strip():
                    results.error(
                        f"Key visual text review has no notes: {label}."
                    )
                if not str(text_review.get("limitations", "")).strip():
                    results.error(
                        f"Key visual text review has no limitations: {label}."
                    )

            if (
                visual_verification == "not-performed"
                and visual.get("crop_review_required") is False
            ):
                results.error(
                    f"Unverified text-only visual cannot clear crop review: {label}."
                )

            candidate_crop = visual.get("candidate_crop")
            if candidate_crop and visual_verification == "not-performed":
                candidate_path = (
                    manifest_path.parent / str(candidate_crop)
                ).resolve()
                if candidate_path in report_images:
                    results.error(
                        f"Unverified candidate crop is embedded in text-only report: "
                        f"{label}."
                    )
            if visual_verification == "externally-verified":
                if visual.get("crop_review_required") is not False:
                    results.error(
                        f"Externally verified visual still requires crop review: {label}."
                    )
                if not str(visual.get("review_notes", "")).strip():
                    results.error(
                        f"Externally verified visual has no reviewer notes: {label}."
                    )
                selected_asset = visual.get("selected_asset")
                if not selected_asset:
                    results.error(
                        f"Externally verified visual has no selected_asset: {label}."
                    )
                else:
                    selected_path = (
                        manifest_path.parent / str(selected_asset)
                    ).resolve()
                    allowed_text_only_images.add(selected_path)
                    if not selected_path.is_file():
                        results.error(
                            f"Externally verified asset does not exist: {selected_path}"
                        )
                    if embed_required and selected_path not in report_images:
                        results.error(
                            f"Externally verified asset is not embedded: {label}."
                        )
                    if (
                        selected_path in report_images
                        and not embed_required
                        and mode != "audit"
                    ):
                        results.warn(
                            f"Embedded visual is not selected_for_report=true: {label}."
                        )
            if selected:
                validate_visual_explanation_context(
                    report_path,
                    text,
                    results,
                    kind=kind,
                    number=number,
                    label=label,
                    asset_path=None,
                    text_only=True,
                )
            continue

        if (
            manifest_schema_version >= 2
            and visual.get("visual_verification")
            not in {"complete", "externally-verified"}
        ):
            results.error(f"Key visual lacks completed visual verification: {label}.")
        if visual.get("crop_review_required") is not False:
            results.error(f"Key visual still requires crop review: {label}.")

        selected_asset = visual.get("selected_asset")
        if not selected_asset:
            results.error(f"Key visual has no selected_asset: {label}.")
            continue
        asset_path = (manifest_path.parent / str(selected_asset)).resolve()
        if not asset_path.is_file():
            results.error(f"Selected asset for {label} does not exist: {asset_path}")
        if embed_required and asset_path not in report_images:
            results.error(f"Selected asset for {label} is not embedded in report.")
        if asset_path in report_images and not embed_required and mode != "audit":
            results.warn(
                f"Embedded visual is not selected_for_report=true: {label}."
            )
        if selected:
            validate_visual_explanation_context(
                report_path,
                text,
                results,
                kind=kind,
                number=number,
                label=label,
                asset_path=asset_path,
                text_only=False,
            )

    if unclassified:
        results.error(
            f"{unclassified} visual(s) have key=null; classify every numbered visual."
        )
    if selection_unclassified:
        results.error(
            f"{selection_unclassified} visual(s) have selected_for_report=null; "
            "classify every numbered visual for schema v3+."
        )
    if visuals and key_count == 0:
        results.warn("No visual is marked key=true; verify this is intentional.")
    if mode == "brief" and selected_count > 1:
        results.error(
            f"Brief mode selects {selected_count} visuals; the maximum is 1."
        )
    if mode in {"explain", "audit"} and key_count != selected_count:
        results.error(
            f"{mode} mode must select every key visual: "
            f"{selected_count} selected vs {key_count} key."
        )
    if mode == "explain" and visuals and key_count == 0:
        results.warn(
            "Explain mode marks no visual as key; manually confirm that no figure or "
            "table is needed to explain the paper."
        )
    if not visuals:
        results.note(
            "Manifest contains no detected visuals; manually confirm the paper has no "
            "numbered figures/tables or add missed entries."
        )
    if text_only:
        for image in IMAGE_RE.finditer(text):
            local_path = resolve_local_target(report_path, image.group("path"))
            if local_path is None:
                results.error(
                    "Text-only reports cannot embed remote/data images without a "
                    "manifested external visual verification."
                )
            elif local_path not in allowed_text_only_images:
                results.error(
                    f"Text-only report embeds an unverified image: {image.group('path')}"
                )
    results.note(
        f"Visual inventory: {len(visuals)} total, {key_count} key, "
        f"{selected_count} selected for the report."
    )


def validate_source_map(
    path: Path,
    results: Results,
    mode: str = "explain",
    text_only: bool = False,
) -> None:
    source_map = load_json(path, results, "Source map")
    if not isinstance(source_map, dict):
        return

    for placeholder_path in unresolved_json_paths(source_map):
        results.error(
            f"source_map.json contains an unresolved placeholder at {placeholder_path}."
        )

    paper = source_map.get("paper")
    if not isinstance(paper, dict):
        results.error("source_map.json requires a 'paper' object.")
    else:
        for field in ("title", "sources", "page_convention"):
            if not paper.get(field):
                results.error(f"source_map.json paper.{field} is missing.")

    try:
        schema_version = int(source_map.get("schema_version", 1))
    except (TypeError, ValueError):
        schema_version = -1
    if schema_version in {2, 3, 4, 5}:
        profile = source_map.get("reader_profile")
        if not isinstance(profile, dict):
            results.error(
                "source_map.json schema v2+ requires a 'reader_profile' object."
            )
        else:
            for field in ("domain", "audience", "goal", "depth", "language"):
                if not profile.get(field):
                    results.error(
                        f"source_map.json reader_profile.{field} is missing."
                    )
            selected_lenses = profile.get("selected_lenses")
            if (
                not isinstance(selected_lenses, list)
                or not selected_lenses
                or not all(
                    isinstance(item, str) and item.strip()
                    for item in selected_lenses
                )
            ):
                results.error(
                    "source_map.json reader_profile.selected_lenses must be "
                    "a non-empty string list."
                )
            if schema_version >= 4:
                delivery = profile.get("delivery")
                if delivery not in DELIVERY_MODES:
                    results.error(
                        "source_map.json reader_profile.delivery must be one of "
                        "brief, explain, audit, or targeted."
                    )
                elif delivery != mode:
                    results.error(
                        "source_map delivery conflicts with validator mode: "
                        f"{delivery!r} != {mode!r}."
                    )
            if schema_version >= 5:
                if profile.get("entry_level") not in {
                    "novice",
                    "research-basics",
                    "domain-familiar",
                }:
                    results.error(
                        "source_map reader_profile.entry_level is invalid."
                    )
                if profile.get("technical_ceiling") not in {
                    "conceptual",
                    "research",
                    "doctoral",
                }:
                    results.error(
                        "source_map reader_profile.technical_ceiling is invalid."
                    )
    elif schema_version != 1:
        results.warn(f"Unrecognized source_map schema_version: {schema_version!r}.")

    if schema_version >= 5:
        explanation = source_map.get("explanation")
        if not isinstance(explanation, dict):
            results.error(
                "source_map schema v5 requires an 'explanation' object."
            )
        else:
            expected_explanation = {
                "strategy": "intuition-to-precision",
                "define_terms_on_first_use": True,
                "report_structure": "six-section",
                "key_visual_policy": "all-key-visuals",
            }
            for field, expected in expected_explanation.items():
                if explanation.get(field) != expected:
                    results.error(
                        "source_map explanation."
                        f"{field} must be {expected!r}."
                    )

        visual_coverage = source_map.get("visual_coverage")
        if not isinstance(visual_coverage, dict):
            results.error(
                "source_map schema v5 requires a 'visual_coverage' object."
            )
        else:
            counts: dict[str, int] = {}
            for field in ("total_numbered", "key", "key_explained"):
                value = visual_coverage.get(field)
                if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                    results.error(
                        f"source_map visual_coverage.{field} must be a non-negative integer."
                    )
                else:
                    counts[field] = value
            if (
                mode in {"explain", "audit"}
                and counts.get("key") != counts.get("key_explained")
            ):
                results.error(
                    "source_map must report every key visual as explained in "
                    f"{mode} mode."
                )
            if (
                "total_numbered" in counts
                and "key" in counts
                and counts["key"] > counts["total_numbered"]
            ):
                results.error(
                    "source_map visual_coverage.key cannot exceed total_numbered."
                )

    if text_only and schema_version < 3:
        results.error(
            "Text-only reports require source_map schema v3+ execution metadata."
        )
    if schema_version >= 3:
        execution = source_map.get("execution")
        if not isinstance(execution, dict):
            results.error(
                "source_map.json schema v3+ requires an 'execution' object."
            )
        else:
            visual_mode = execution.get("visual_mode")
            visual_verification = execution.get("visual_verification")
            if visual_mode not in {"visual", "text-only"}:
                results.error(
                    "source_map.json execution.visual_mode must be visual or text-only."
                )
            if visual_verification not in {
                "complete",
                "not-performed",
                "externally-verified",
            }:
                results.error(
                    "source_map.json execution.visual_verification is invalid."
                )
            if text_only and visual_mode != "text-only":
                results.error(
                    "Text-only validation conflicts with source_map visual_mode."
                )
            if not text_only and visual_mode == "text-only":
                results.error(
                    "source_map visual_mode is text-only; use --text-only."
                )
            if (
                not text_only
                and visual_mode == "visual"
                and visual_verification
                not in {"complete", "externally-verified"}
            ):
                results.error(
                    "Visual source_map requires completed visual verification."
                )
            if (
                text_only
                and visual_verification
                not in {"not-performed", "externally-verified"}
            ):
                results.error(
                    "Text-only source_map cannot claim direct visual verification."
                )
            text_sources = execution.get("text_evidence_sources")
            if text_only and (
                not isinstance(text_sources, list)
                or not text_sources
                or not all(
                    isinstance(source, str) and source.strip()
                    for source in text_sources
                )
            ):
                results.error(
                    "Text-only source_map requires non-empty text_evidence_sources."
                )

    claims = source_map.get("claims")
    if not isinstance(claims, list) or not claims:
        results.error("source_map.json requires a non-empty 'claims' list.")
        return

    seen_ids: set[str] = set()
    allowed_statuses = {"strong", "partial", "weak", "unsupported"}
    for index, claim in enumerate(claims, start=1):
        if not isinstance(claim, dict):
            results.error(f"source_map claim {index} is not an object.")
            continue
        claim_id = str(claim.get("id", "")).strip()
        if not claim_id:
            results.error(f"source_map claim {index} has no id.")
        elif claim_id in seen_ids:
            results.error(f"Duplicate source_map claim id: {claim_id}")
        else:
            seen_ids.add(claim_id)
        if not claim.get("claim"):
            results.error(f"source_map claim {claim_id or index} has no text.")
        status = claim.get("status")
        if status not in allowed_statuses:
            results.error(
                f"source_map claim {claim_id or index} has invalid status: {status!r}."
            )
        evidence = claim.get("evidence")
        if status != "unsupported" and (not isinstance(evidence, list) or not evidence):
            results.error(
                f"Supported claim {claim_id or index} has no evidence row."
            )

    results.note(f"Source map contains {len(claims)} claim(s).")


def print_results(results: Results, strict: bool) -> int:
    for message in results.errors:
        print(f"ERROR: {message}")
    for message in results.warnings:
        print(f"WARNING: {message}")
    for message in results.notes:
        print(f"NOTE: {message}")

    blocking = len(results.errors) + (len(results.warnings) if strict else 0)
    if blocking:
        mode = "strict mode" if strict else "validation"
        print(
            f"FAIL ({mode}): {len(results.errors)} error(s), "
            f"{len(results.warnings)} warning(s)."
        )
        return 1
    print(f"PASS: 0 errors, {len(results.warnings)} warning(s).")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a six-section, beginner-accessible, visual-interleaved "
            "paper-reading Markdown report."
        )
    )
    parser.add_argument("report", help="Path to report.md.")
    parser.add_argument(
        "--mode",
        choices=("auto", "brief", "explain", "audit", "targeted"),
        default="auto",
        help=(
            "Delivery mode. Auto reads the report marker; a six-section report "
            "defaults to explain."
        ),
    )
    parser.add_argument(
        "--manifest", help="Path to visual_manifest.json (recommended)."
    )
    parser.add_argument(
        "--allow-missing-manifest",
        action="store_true",
        help="Do not warn when no visual manifest is supplied.",
    )
    parser.add_argument(
        "--source-map",
        help="Path to source_map.json. Defaults to report sibling source_map.json.",
    )
    parser.add_argument(
        "--allow-missing-source-map",
        action="store_true",
        help="Do not require source_map.json (for chat-only or explicitly reduced output).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures.",
    )
    parser.add_argument(
        "--text-only",
        action="store_true",
        help=(
            "Validate the no-vision workflow: require disclosure and completed "
            "text evidence reviews instead of direct crop verification."
        ),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report_path = Path(args.report).expanduser().resolve()
    if not report_path.is_file():
        print(f"ERROR: report not found: {report_path}", file=sys.stderr)
        return 2

    text = report_path.read_text(encoding="utf-8")
    results = Results()
    sections, section_numbers = split_sections(text)
    mode = infer_mode(text, args.mode, section_numbers)
    results.note(f"Delivery mode: {mode}.")
    validate_structure(
        report_path,
        text,
        sections,
        section_numbers,
        mode,
        results,
        text_only=args.text_only,
    )

    if args.manifest:
        manifest_path = Path(args.manifest).expanduser().resolve()
        validate_manifest(
            manifest_path,
            report_path,
            text,
            results,
            mode=mode,
            text_only=args.text_only,
        )
    elif not args.allow_missing_manifest:
        results.warn("No visual manifest supplied; full figure/table coverage is unverified.")

    if not args.allow_missing_source_map:
        source_map_path = (
            Path(args.source_map).expanduser().resolve()
            if args.source_map
            else report_path.parent / "source_map.json"
        )
        validate_source_map(
            source_map_path,
            results,
            mode=mode,
            text_only=args.text_only,
        )

    return print_results(results, args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
