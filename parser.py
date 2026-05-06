import json
import re
from typing import Any

from schemas import dict_to_interview_result, dict_to_cluster_result


def extract_json(text: str) -> dict | None:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    code_block_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if code_block_match:
        try:
            return json.loads(code_block_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    brace_match = re.search(r"\{.*\}", text, re.DOTALL)
    if brace_match:
        candidate = brace_match.group(0)
        depth = 0
        for i, ch in enumerate(candidate):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(candidate[: i + 1])
                    except json.JSONDecodeError:
                        break

    return None


def _ok(data: Any) -> dict:
    return {"success": True, "data": data}


def _fail(error: str) -> dict:
    return {"success": False, "error": error}


def _validate_interview_data(data: dict) -> list[str]:
    errors = []
    if not data.get("interview_id"):
        errors.append("缺少 interview_id")
    if not data.get("summary"):
        errors.append("缺少 summary")
    pain_points = data.get("pain_points", [])
    for i, pp in enumerate(pain_points):
        if not pp.get("pain"):
            errors.append(f"pain_points[{i}] 缺少 pain")
        if not pp.get("evidence"):
            errors.append(f"pain_points[{i}] 缺少 evidence")
        sev = pp.get("severity", 3)
        if not isinstance(sev, int) or sev < 1 or sev > 5:
            errors.append(f"pain_points[{i}] severity 必须是 1-5 的整数")
    emotion = data.get("emotion", {})
    score = emotion.get("score", 0)
    if not isinstance(score, (int, float)) or score < -1 or score > 1:
        errors.append("emotion.score 必须是 -1 到 1 之间的数值")
    return errors


def _validate_cluster_data(data: dict) -> list[str]:
    errors = []
    if "total_interviews" not in data:
        errors.append("缺少 total_interviews")
    if not isinstance(data.get("demand_clusters", []), list):
        errors.append("demand_clusters 必须是列表")
    return errors


def validate_interview_result(data: dict) -> dict:
    if data is None:
        return _fail("JSON 解析失败，无法提取有效数据")
    errors = _validate_interview_data(data)
    if errors:
        return _fail("InterviewAnalysisResult 校验失败: " + "; ".join(errors))
    try:
        result = dict_to_interview_result(data)
        return _ok(result)
    except Exception as e:
        return _fail(f"InterviewAnalysisResult 转换失败: {e}")


def validate_cluster_result(data: dict) -> dict:
    if data is None:
        return _fail("JSON 解析失败，无法提取有效数据")
    errors = _validate_cluster_data(data)
    if errors:
        return _fail("ClusterResult 校验失败: " + "; ".join(errors))
    try:
        result = dict_to_cluster_result(data)
        return _ok(result)
    except Exception as e:
        return _fail(f"ClusterResult 转换失败: {e}")
