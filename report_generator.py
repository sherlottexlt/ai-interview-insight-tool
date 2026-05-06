from datetime import datetime

from schemas import InterviewAnalysisResult, ClusterResult, RiceScoreItem


def generate_markdown_report(
    project_name: str,
    target_user: str,
    results: list[InterviewAnalysisResult],
    cluster_result: ClusterResult | None = None,
    rice_scores: list[RiceScoreItem] | None = None,
) -> str:
    lines: list[str] = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # === 报告头 ===
    lines.append(f"# {project_name} — 用户访谈洞察报告\n")
    lines.append(f"> 生成时间：{now}  \n")
    lines.append(f"> 分析工具：AI 用户访谈分析工具 MVP  \n")

    # === 1. 项目背景 ===
    lines.append("## 1. 项目背景\n")
    lines.append(f"- **项目名称**：{project_name}")
    lines.append(f"- **目标用户**：{target_user}")
    lines.append(f"- **访谈样本数**：{len(results)} 份")
    lines.append("")

    # === 2. 访谈样本概况 ===
    lines.append("## 2. 访谈样本概况\n")
    lines.append("| 编号 | 角色 | 行业 | 技术水平 | 使用频率 |")
    lines.append("|------|------|------|----------|----------|")
    for r in results:
        p = r.user_profile
        lines.append(f"| {r.interview_id} | {p.role} | {p.industry} | {p.tech_level} | {p.usage_frequency} |")
    lines.append("")

    # === 3. 核心发现 ===
    lines.append("## 3. 核心发现\n")
    for r in results:
        lines.append(f"### {r.interview_id}\n")
        lines.append(f"**摘要**：{r.summary}\n")
        lines.append(f"- **使用场景**：{'、'.join(r.usage_scenarios)}")
        lines.append(f"- **情绪倾向**：{r.emotion.label}（得分 {r.emotion.score}）— {r.emotion.reason}")
        lines.append(f"- **标签**：{'、'.join(r.tags)}")
        lines.append("")

    # === 4. 高频痛点 ===
    lines.append("## 4. 高频痛点\n")
    all_pains = []
    for r in results:
        for pp in r.pain_points:
            all_pains.append((r.interview_id, pp))
    all_pains.sort(key=lambda x: x[1].severity, reverse=True)

    lines.append("| 严重程度 | 痛点描述 | 来源访谈 |")
    lines.append("|:--------:|----------|:--------:|")
    for iid, pp in all_pains:
        lines.append(f"| {pp.severity}/5 | {pp.pain} | {iid} |")
    lines.append("")

    # === 5. 用户原话证据 ===
    lines.append("## 5. 用户原话证据\n")
    lines.append("> 每条痛点均绑定用户原话，确保洞察可溯源、可验证。\n")
    for iid, pp in all_pains:
        lines.append(f"- **[{iid}]** {pp.pain}")
        lines.append(f"  > 「{pp.evidence}」")
    lines.append("")

    # === 6. 产品机会点 ===
    lines.append("## 6. 产品机会点\n")
    lines.append("| 机会点 | 关联痛点 | 来源访谈 |")
    lines.append("|--------|----------|:--------:|")
    for r in results:
        for opp in r.product_opportunities:
            lines.append(f"| {opp.opportunity} | {opp.related_pain} | {r.interview_id} |")
    lines.append("")

    # === 7. 需求聚类结果 ===
    lines.append("## 7. 需求聚类结果\n")
    if cluster_result:
        lines.append(f"共分析 **{cluster_result.total_interviews}** 份访谈，识别出 **{len(cluster_result.demand_clusters)}** 个需求聚类。\n")

        for dc in cluster_result.demand_clusters:
            lines.append(f"### {dc.cluster_name}\n")
            lines.append(f"- **描述**：{dc.cluster_description}")
            lines.append(f"- **出现频次**：{dc.frequency}")
            lines.append(f"- **涉及访谈**：{'、'.join(dc.interview_ids)}")
            lines.append(f"- **包含项**：")
            for item in dc.items:
                lines.append(f"  - {item}")
            lines.append("")

        if cluster_result.tag_statistics:
            lines.append("### 标签频次统计\n")
            lines.append("| 标签 | 出现次数 |")
            lines.append("|------|:--------:|")
            for tag, count in sorted(cluster_result.tag_statistics.items(), key=lambda x: x[1], reverse=True):
                lines.append(f"| {tag} | {count} |")
            lines.append("")

        if cluster_result.cross_interview_insights:
            lines.append("### 跨访谈洞察\n")
            for insight in cluster_result.cross_interview_insights:
                lines.append(f"- {insight}")
            lines.append("")
    else:
        lines.append("*暂无聚类结果（需上传 2 份以上访谈后生成）。*\n")

    # === 8. RICE 优先级建议 ===
    lines.append("## 8. RICE 优先级建议\n")
    if rice_scores:
        lines.append("公式：**RICE Score = (Reach × Impact × Confidence%) / Effort**\n")
        lines.append("| 排名 | 机会点 | Reach | Impact | Confidence | Effort | RICE 分数 |")
        lines.append("|:----:|--------|:-----:|:------:|:----------:|:------:|:---------:|")
        for i, rs in enumerate(rice_scores, 1):
            conf_pct = f"{rs.confidence / 10:.0%}"
            score_str = f"{rs.rice_score:.2f}" if rs.rice_score else "-"
            lines.append(f"| {i} | {rs.item_name} | {rs.reach} | {rs.impact} | {conf_pct} | {rs.effort} | {score_str} |")
        lines.append("")
    else:
        lines.append("*暂无 RICE 评分（需先分析访谈并生成机会点）。*\n")

    # === 9. 后续验证方案 ===
    lines.append("## 9. 后续验证方案\n")
    lines.append("1. **定量验证**：针对高频痛点设计问卷，扩大样本量验证痛点普遍性。")
    lines.append("2. **可用性测试**：针对高 RICE 分数的机会点制作原型，观察用户实际操作反馈。")
    lines.append("3. **A/B 测试**：对优先级接近的机会点进行 A/B 测试，用数据决定落地顺序。")
    lines.append("4. **持续访谈**：每季度补充 3-5 份新访谈，追踪痛点变化和需求演进。")
    lines.append("")

    return "\n".join(lines)
