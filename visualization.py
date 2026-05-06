from collections import Counter

import plotly.graph_objects as go

from schemas import InterviewAnalysisResult, RiceScoreItem


def plot_tag_frequency(results: list[InterviewAnalysisResult]) -> go.Figure | None:
    if not results:
        return None

    tag_counter = Counter()
    for r in results:
        tag_counter.update(r.tags)

    if not tag_counter:
        return None

    tags = [t for t, _ in tag_counter.most_common()]
    counts = [tag_counter[t] for t in tags]

    fig = go.Figure(go.Bar(
        x=tags,
        y=counts,
        marker_color="#636EFA",
    ))
    fig.update_layout(
        title="标签频次统计",
        xaxis_title="标签",
        yaxis_title="出现次数",
        margin=dict(l=40, r=20, t=50, b=40),
    )
    return fig


def plot_emotion_distribution(results: list[InterviewAnalysisResult]) -> go.Figure | None:
    if not results:
        return None

    emotion_counter = Counter()
    for r in results:
        emotion_counter[r.emotion.label] += 1

    if not emotion_counter:
        return None

    labels = list(emotion_counter.keys())
    values = list(emotion_counter.values())

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
    ))
    fig.update_layout(
        title="情绪分布",
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def plot_pain_severity(results: list[InterviewAnalysisResult]) -> go.Figure | None:
    if not results:
        return None

    pains = []
    severities = []
    for r in results:
        for pp in r.pain_points:
            pains.append(pp.pain)
            severities.append(pp.severity)

    if not pains:
        return None

    # 痛点名称过长时截断，避免图表拥挤
    display_names = [p[:20] + "..." if len(p) > 20 else p for p in pains]

    fig = go.Figure(go.Bar(
        x=display_names,
        y=severities,
        marker_color=severities,
        marker_colorscale="Reds",
        marker_reversescale=False,
    ))
    fig.update_layout(
        title="痛点严重程度",
        xaxis_title="痛点",
        yaxis_title="严重程度 (1-5)",
        yaxis=dict(dtick=1, range=[0, 6]),
        margin=dict(l=40, r=20, t=50, b=100),
        xaxis_tickangle=-30,
    )
    return fig


def plot_rice_scores(rice_scores: list[RiceScoreItem]) -> go.Figure | None:
    if not rice_scores:
        return None

    names = [r.item_name for r in rice_scores]
    scores = [r.rice_score or 0 for r in rice_scores]

    # 横向条形图：y 轴放名称，x 轴放分数
    fig = go.Figure(go.Bar(
        x=scores,
        y=names,
        orientation="h",
        marker_color="#00CC96",
        text=[f"{s:.2f}" for s in scores],
        textposition="auto",
    ))
    fig.update_layout(
        title="RICE 优先级评分",
        xaxis_title="RICE 分数",
        yaxis_title="",
        margin=dict(l=150, r=20, t=50, b=40),
        height=max(300, len(names) * 40),
    )
    return fig
