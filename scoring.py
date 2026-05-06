from schemas import RiceScoreItem

# RICE 评分默认值（MVP 阶段使用，后续可由用户在 UI 中调整）
DEFAULT_REACH = 5
DEFAULT_IMPACT = 4
DEFAULT_CONFIDENCE = 7       # schema 中为 1-10 整数，7 对应 70% 信心度
DEFAULT_EFFORT = 3


def calculate_rice(reach: int, impact: int, confidence: int, effort: int) -> float:
    """
    RICE 优先级评分公式：
    Score = (Reach × Impact × Confidence) / Effort

    - Reach:     影响用户数，1-10
    - Impact:    影响程度，1-10
    - Confidence: 信心度，1-10（计算时除以 10 转为百分比）
    - Effort:    开发成本，1-10
    """
    if effort == 0:
        return 0.0
    # confidence 除以 10，将 1-10 转为 0.1-1.0 的百分比
    confidence_pct = confidence / 10.0
    score = (reach * impact * confidence_pct) / effort
    return round(score, 2)


def generate_rice_scores(
    opportunities: list[dict],
    reach: int = DEFAULT_REACH,
    impact: int = DEFAULT_IMPACT,
    confidence: int = DEFAULT_CONFIDENCE,
    effort: int = DEFAULT_EFFORT,
) -> list[RiceScoreItem]:
    """
    为产品机会点列表生成 RICE 评分。

    参数:
        opportunities: 产品机会点列表，每项包含 opportunity 和 related_pain
        reach/impact/confidence/effort: 默认评分值，MVP 阶段统一使用

    返回:
        按 rice_score 从高到低排序的 RiceScoreItem 列表
    """
    results = []
    for opp in opportunities:
        # 从 opportunity 字典中提取名称和关联痛点
        opp_name = opp.get("opportunity", "未知机会点")
        related_pain = opp.get("related_pain", "")
        source_ids = opp.get("source_interview_ids", [])

        rice_score = calculate_rice(reach, impact, confidence, effort)

        item = RiceScoreItem(
            item_name=opp_name,
            pain_point=related_pain,
            reach=reach,
            impact=impact,
            confidence=confidence,
            effort=effort,
            rice_score=rice_score,
            source_interview_ids=source_ids,
        )
        results.append(item)

    # 按 rice_score 从高到低排序
    results.sort(key=lambda x: x.rice_score or 0, reverse=True)
    return results
