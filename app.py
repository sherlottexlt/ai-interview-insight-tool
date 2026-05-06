import json
import os
from datetime import datetime

import streamlit as st

from prompts import INTERVIEW_ANALYSIS_PROMPT, CLUSTER_PROMPT
from llm_client import call_llm
from parser import extract_json, validate_interview_result, validate_cluster_result
from scoring import generate_rice_scores
from visualization import plot_tag_frequency, plot_emotion_distribution, plot_pain_severity, plot_rice_scores
from report_generator import generate_markdown_report
from schemas import InterviewAnalysisResult, RiceScoreItem, ClusterResult, dataclass_to_dict, dict_to_interview_result, dict_to_cluster_result
from ui_components import (
    inject_global_css, render_sidebar_logo, render_page_header,
    render_kpi_card, render_project_card, render_status_badge,
    render_section_card, render_tag, render_quote_block,
    render_pain_card, render_priority_badge, render_empty_state,
    render_flow_cta,
)

PAGES = [
    "📊 项目看板",
    "📝 新建访谈",
    "🔍 洞察分析",
    "🔗 需求聚类",
    "📐 RICE 优先级",
    "📄 报告导出",
]

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
STATE_FILE = os.path.join(DATA_DIR, "app_state.json")


def _save_state():
    os.makedirs(DATA_DIR, exist_ok=True)
    state = {
        "results": [dataclass_to_dict(r) for r in st.session_state.results],
        "cluster_result": dataclass_to_dict(st.session_state.cluster_result) if st.session_state.cluster_result else None,
        "rice_scores": [dataclass_to_dict(rs) for rs in st.session_state.rice_scores],
        "interview_counter": st.session_state.interview_counter,
        "_project_name": st.session_state._project_name,
        "_target_user": st.session_state._target_user,
    }
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def _load_state() -> dict | None:
    if not os.path.exists(STATE_FILE):
        return None
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def init_session_state():
    saved = _load_state()
    defaults = {
        "results": [],
        "cluster_result": None,
        "rice_scores": [],
        "interview_counter": 0,
        "current_page": PAGES[0],
        "_project_name": "我的产品项目",
        "_target_user": "产品核心用户",
        "_is_analyzing": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if saved and not st.session_state.results:
        st.session_state.results = [dict_to_interview_result(r) for r in saved.get("results", [])]
        if saved.get("cluster_result"):
            st.session_state.cluster_result = dict_to_cluster_result(saved["cluster_result"])
        else:
            st.session_state.cluster_result = None
        st.session_state.rice_scores = []
        for rs_data in saved.get("rice_scores", []):
            st.session_state.rice_scores.append(RiceScoreItem(
                item_name=rs_data.get("item_name", ""),
                pain_point=rs_data.get("pain_point", ""),
                reach=rs_data.get("reach", 5),
                impact=rs_data.get("impact", 4),
                confidence=rs_data.get("confidence", 7),
                effort=rs_data.get("effort", 3),
                rice_score=rs_data.get("rice_score"),
                source_interview_ids=rs_data.get("source_interview_ids", []),
            ))
        st.session_state.interview_counter = saved.get("interview_counter", 0)
        if saved.get("_project_name"):
            st.session_state._project_name = saved["_project_name"]
        if saved.get("_target_user"):
            st.session_state._target_user = saved["_target_user"]


def navigate_to(page: str):
    st.session_state.current_page = page
    st.rerun()


def call_and_validate(prompt: str, validator, error_label: str) -> dict | None:
    raw_output = call_llm(prompt)

    if raw_output.startswith("[LLM 调用失败]"):
        st.error(f"{error_label}：{raw_output}")
        return None

    parsed = extract_json(raw_output)
    validation = validator(parsed)

    if validation["success"]:
        return validation["data"]

    st.error(f"{error_label}：{validation['error']}")
    with st.expander("查看 LLM 原始输出"):
        st.text(raw_output)
    return None


def rebuild_rice_scores():
    all_opps = []
    for r in st.session_state.results:
        for opp in r.product_opportunities:
            opp_dict = dataclass_to_dict(opp)
            opp_dict["source_interview_ids"] = [r.interview_id]
            all_opps.append(opp_dict)
    st.session_state.rice_scores = generate_rice_scores(all_opps)
    _save_state()


def render_table(title: str, data: list[dict], empty_msg: str = "暂无数据"):
    st.subheader(title)
    if data:
        st.table(data)
    else:
        st.info(empty_msg)


# ==================== 页面：项目看板 ====================
def render_page_dashboard():
    render_page_header("项目看板", "数据概览与项目进度")

    results = st.session_state.results

    total_pains = sum(len(r.pain_points) for r in results)
    all_tags = set()
    for r in results:
        all_tags.update(r.tags)

    kpi_cols = st.columns(4)
    st.markdown('<div class="if-dashboard-grid">', unsafe_allow_html=True)
    with kpi_cols[0]:
        render_kpi_card("已分析访谈", len(results), "份", "📄", "blue")
    with kpi_cols[1]:
        render_kpi_card("识别痛点", total_pains, "个", "⊘", "red")
    with kpi_cols[2]:
        render_kpi_card("需求标签", len(all_tags), "个", "🏷", "green")
    with kpi_cols[3]:
        render_kpi_card("产品机会点", len(st.session_state.rice_scores), "个", "💡", "purple")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    st.subheader("进行中项目")
    if results:
        project_cards = results[:3]
        proj_cols = st.columns(min(len(project_cards), 3))
        for i, r in enumerate(project_cards):
            with proj_cols[i]:
                insight_count = len(r.pain_points) + len(r.explicit_needs) + len(r.implicit_needs)
                progress = min(100, max(20, insight_count * 20))
                render_project_card(
                    name=f"{r.interview_id} · {r.user_profile.role}",
                    interview_count=1,
                    insight_count=insight_count,
                    updated=datetime.now().strftime("%m-%d %H:%M"),
                    progress=progress,
                )
    else:
        st.markdown(
            '<div class="if-onboarding">'
            '<div class="if-onboarding-icon">🚀</div>'
            '<div class="if-onboarding-title">开始你的第一个用户访谈分析</div>'
            '<div class="if-onboarding-steps">'
            '<div class="step"><span class="num">1</span><span>粘贴或上传访谈文本</span></div>'
            '<div class="step"><span class="num">2</span><span>AI 自动提取痛点与需求</span></div>'
            '<div class="step"><span class="num">3</span><span>查看洞察报告与优先级</span></div>'
            '</div>'
            '<div style="margin-top:20px">',
            unsafe_allow_html=True,
        )
        if st.button("📝 创建第一个访谈项目", type="primary", key="empty_dashboard_cta"):
            navigate_to(PAGES[1])
        st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    st.subheader("最近分析")
    if results:
        head = (
            "<tr>"
            "<th>访谈 ID</th>"
            "<th>项目名称</th>"
            "<th>受访者</th>"
            "<th style='text-align:center'>日期</th>"
            "<th style='text-align:center'>状态</th>"
            "<th style='text-align:right'>洞察数</th>"
            "</tr>"
        )
        body = ""
        for idx, r in enumerate(results):
            status_html = render_status_badge("已完成")
            body += (
                f"<tr>"
                f"<td>{r.interview_id}</td>"
                f"<td>{st.session_state._project_name}</td>"
                f"<td>{r.user_profile.role}</td>"
                f"<td class='center'>{datetime.now().strftime('%Y-%m-%d')}</td>"
                f"<td class='center'>{status_html}</td>"
                f"<td class='num'>{len(r.pain_points) + len(r.explicit_needs) + len(r.implicit_needs)}</td>"
                f"</tr>"
            )
        st.markdown(
            f'<table class="if-list-table"><thead>{head}</thead><tbody>{body}</tbody></table>',
            unsafe_allow_html=True,
        )

        for idx, r in enumerate(results):
            if st.button(f"查看 {r.interview_id} 详情", key=f"row_click_{idx}", help="点击查看该访谈的洞察分析"):
                navigate_to(PAGES[2])
    else:
        render_empty_state("📊", "暂无分析记录")

    if not results:
        if render_flow_cta("开始新访谈", "粘贴访谈文本，AI 自动提取结构化洞察", "📝 新建访谈项目", "cta_dashboard_to_input"):
            navigate_to(PAGES[1])


# ==================== 页面：新建访谈 ====================
def render_page_input():
    render_page_header("新建访谈", "粘贴或上传用户访谈文本，AI 自动提取结构化洞察")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown('<div class="if-section">', unsafe_allow_html=True)
        st.markdown('<div class="if-section-title">📝 输入访谈内容 <span style="color:var(--danger);margin-left:4px">*</span></div>', unsafe_allow_html=True)
        interview_text = st.text_area("访谈内容", height=280, key="paste_text", label_visibility="collapsed")

        st.markdown('<div style="font-size:13px;font-weight:500;color:var(--text-3);margin-bottom:6px">� 或上传 .txt 文件</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("支持 .txt 格式，最大 10MB", type=["txt"], key="file_upload", label_visibility="collapsed", help="仅支持纯文本文件 (.txt)，最大 10MB")

        if interview_text or uploaded_file is not None:
            st.markdown(
                '<div style="display:flex;align-items:center;gap:6px;padding:8px 12px;background:var(--success-bg);border-radius:var(--r);font-size:12px;color:var(--success);margin-bottom:12px">'
                '💾 内容已自动保存至当前会话'
                '</div>',
                unsafe_allow_html=True,
            )

        if uploaded_file is not None:
            file_size = uploaded_file.size
            size_display = f"{file_size / 1024:.1f} KB" if file_size < 1024 * 1024 else f"{file_size / (1024 * 1024):.1f} MB"
            st.markdown(
                f'<div style="display:flex;align-items:center;justify-content:space-between;padding:8px 12px;background:var(--surface-2);border-radius:var(--r);margin-top:8px;font-size:13px">'
                f'<div style="display:flex;align-items:center;gap:8px">'
                f'<span>📄</span>'
                f'<span style="color:var(--text)">{uploaded_file.name}</span>'
                f'<span style="color:var(--text-3)">({size_display})</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            col_remove, _ = st.columns([0.15, 0.85])
            with col_remove:
                if st.button("✕", key="remove_file", help="移除文件"):
                    st.session_state.file_upload = None
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        char_count = len(interview_text) if interview_text else 0
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px;font-size:12px;color:var(--text-3)">'
            f'<span>已输入 <strong style="color:var(--text-2)">{char_count}</strong> 字</span>'
            f'<span>建议 500-5000 字以获得最佳分析效果</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        project_name = st.text_input("项目名称", value=st.session_state._project_name)
        target_user = st.text_input("目标用户", value=st.session_state._target_user)

        has_content = bool(interview_text.strip() or uploaded_file is not None)

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        analyze_btn = st.button(
            "⏳ 正在分析..." if st.session_state._is_analyzing else "✨ 开始 AI 分析",
            type="primary",
            use_container_width=True,
            disabled=not has_content or st.session_state._is_analyzing,
        )

        if st.session_state.get("_form_error"):
            st.markdown(
                f'<div style="margin-top:8px;padding:10px 12px;background:var(--danger-bg);color:var(--p0);border-radius:var(--r);font-size:13px">'
                f'⚠️ {st.session_state._form_error}'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.session_state._form_error = None

        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        if analyze_btn and not st.session_state._is_analyzing:
            st.session_state._is_analyzing = True
            st.rerun()

        if st.session_state._is_analyzing:
            text_to_analyze = ""
            if uploaded_file is not None:
                text_to_analyze = uploaded_file.read().decode("utf-8")
            elif interview_text.strip():
                text_to_analyze = interview_text.strip()

            if not text_to_analyze:
                st.session_state._form_error = "请先粘贴访谈文本或上传文件，再点击「开始 AI 分析」"
                st.session_state._is_analyzing = False
            else:
                st.session_state.interview_counter += 1
                interview_id = f"interview_{st.session_state.interview_counter}"

                with st.spinner(f"正在分析 {interview_id}，请稍候..."):
                    prompt = INTERVIEW_ANALYSIS_PROMPT.format(
                        interview_id=interview_id,
                        interview_text=text_to_analyze,
                    )
                    result = call_and_validate(prompt, validate_interview_result, "分析结果校验失败")

                if result is not None:
                    st.session_state.results.append(result)
                    rebuild_rice_scores()
                    st.session_state._is_analyzing = False
                    st.success(f"✅ {interview_id} 分析完成！")
                    with st.expander("查看原始 JSON 结果"):
                        st.json(dataclass_to_dict(result))

                    if render_flow_cta("查看洞察分析", "深入查看痛点、需求和产品机会点", "🔍 查看结构化洞察", "cta_input_to_insight"):
                        navigate_to(PAGES[2])

            st.session_state._project_name = project_name
            st.session_state._target_user = target_user

        st.markdown('<div class="if-section">', unsafe_allow_html=True)
        st.markdown('<div class="if-section-title">📊 分析记录</div>', unsafe_allow_html=True)

        if st.session_state.results:
            st.markdown(
                f'<div style="margin-bottom:16px">已分析 '
                f'<span class="if-count">{len(st.session_state.results)} 份</span> 访谈</div>',
                unsafe_allow_html=True,
            )
            for r in st.session_state.results:
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:8px;padding:8px 0;'
                    f'border-bottom:1px solid var(--divider)">'
                    f'<span style="font-size:14px;font-weight:500;color:var(--text)">{r.interview_id}</span>'
                    f'<span style="font-size:14px;color:var(--text-2)">— {r.user_profile.role}</span>'
                    f'{render_status_badge("已完成")}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        else:
            render_empty_state("📋", "尚未分析任何访谈，请在左侧输入内容后点击「开始 AI 分析」")
        st.markdown('</div>', unsafe_allow_html=True)


# ==================== 页面：洞察分析 ====================
def render_page_insight():
    render_page_header("洞察分析", "查看单份访谈的深度分析结果")

    if not st.session_state.results:
        render_empty_state("🔍", "请先在「新建访谈」中分析至少一份访谈")
        return

    selected_id = st.selectbox(
        "选择访谈记录",
        options=[r.interview_id for r in st.session_state.results],
        key="selected_interview",
    )
    selected = next(r for r in st.session_state.results if r.interview_id == selected_id)

    cols = st.columns(4)
    with cols[0]:
        render_kpi_card("痛点数", len(selected.pain_points), "个", "⊘", "red")
    with cols[1]:
        render_kpi_card("显性需求", len(selected.explicit_needs), "个", "📢", "blue")
    with cols[2]:
        render_kpi_card("隐性需求", len(selected.implicit_needs), "个", "🔮", "purple")
    with cols[3]:
        render_kpi_card("机会点", len(selected.product_opportunities), "个", "💡", "green")

    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.markdown('<div class="if-section">', unsafe_allow_html=True)
        st.markdown('<div class="if-section-title">访谈摘要</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:14px;color:var(--text-2);line-height:1.7">{selected.summary}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="if-section">', unsafe_allow_html=True)
        st.markdown('<div class="if-section-title">使用场景</div>', unsafe_allow_html=True)
        scenes_html = "".join(f'<div class="if-scene">{s}</div>' for s in selected.usage_scenarios)
        st.markdown(scenes_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="if-section">', unsafe_allow_html=True)
        st.markdown('<div class="if-section-title">用户画像</div>', unsafe_allow_html=True)
        p = selected.user_profile
        profile_html = (
            f'<div class="if-profile">'
            f'<div><div class="k">角色</div><div class="v">{p.role}</div></div>'
            f'<div><div class="k">行业</div><div class="v">{p.industry}</div></div>'
            f'<div><div class="k">技术水平</div><div class="v">{p.tech_level}</div></div>'
            f'<div><div class="k">使用频率</div><div class="v">{p.usage_frequency}</div></div>'
            f'</div>'
        )
        st.markdown(profile_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="if-section">', unsafe_allow_html=True)
        st.markdown('<div class="if-section-title">情绪倾向</div>', unsafe_allow_html=True)
        e = selected.emotion
        score_pct = int((e.score + 1) / 2 * 100)
        if e.score > 0.3:
            emotion_cls = "expect"
            emotion_label = "期待"
        elif e.score < -0.3:
            emotion_cls = "anxiety"
            emotion_label = "焦虑"
        else:
            emotion_cls = "confused"
            emotion_label = "中性"
        emotion_html = (
            f'<div class="if-emotion-grid">'
            f'<div class="if-emotion anxiety"><div class="l">焦虑</div><div class="v">{max(0, score_pct - 20)}%</div></div>'
            f'<div class="if-emotion confused"><div class="l">困惑</div><div class="v">{max(0, 100 - score_pct - 30)}%</div></div>'
            f'<div class="if-emotion expect"><div class="l">期待</div><div class="v">{score_pct}%</div></div>'
            f'<div class="if-emotion stress"><div class="l">压力</div><div class="v">{max(0, 100 - score_pct - 40)}%</div></div>'
            f'</div>'
            f'<div style="font-size:13px;color:var(--text-3);margin-top:8px">{e.reason}</div>'
        )
        st.markdown(emotion_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="if-section">', unsafe_allow_html=True)
        st.markdown('<div class="if-section-title">标签</div>', unsafe_allow_html=True)
        pills_html = "".join(f'<span class="if-pill">{t}</span>' for t in selected.tags)
        st.markdown(pills_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

    st.markdown('<div class="if-section">', unsafe_allow_html=True)
    st.markdown('<div class="if-section-title">痛点</div>', unsafe_allow_html=True)
    if selected.pain_points:
        for pp in selected.pain_points:
            opp = None
            for o in selected.product_opportunities:
                if o.related_pain == pp.pain:
                    opp = o.opportunity
                    break
            render_pain_card(pp.pain, pp.evidence, pp.severity, opp)
    else:
        st.markdown('<div style="font-size:14px;color:var(--text-3);padding:8px 0">无痛点数据</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown('<div class="if-section">', unsafe_allow_html=True)
        st.markdown('<div class="if-section-title">显性需求</div>', unsafe_allow_html=True)
        if selected.explicit_needs:
            items = "".join(
                f'<li>{en.need}'
                f'<div class="if-quote" style="margin:4px 0 8px">{en.source}</div>'
                f'</li>'
                for en in selected.explicit_needs
            )
            st.markdown(f'<ul class="if-need-list">{items}</ul>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size:14px;color:var(--text-3)">无显性需求数据</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_d:
        st.markdown('<div class="if-section">', unsafe_allow_html=True)
        st.markdown('<div class="if-section-title">隐性需求</div>', unsafe_allow_html=True)
        if selected.implicit_needs:
            items = "".join(
                f'<li>{im.need}'
                f'<div style="font-size:13px;color:var(--text-3);margin:2px 0 8px">推断依据：{im.inferred_from}</div>'
                f'</li>'
                for im in selected.implicit_needs
            )
            st.markdown(f'<ul class="if-need-list implicit">{items}</ul>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size:14px;color:var(--text-3)">无隐性需求数据</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

    st.markdown('<div class="if-section">', unsafe_allow_html=True)
    st.markdown('<div class="if-section-title">产品机会点</div>', unsafe_allow_html=True)
    if selected.product_opportunities:
        opp_colors = ["green", "blue", "purple"]
        for i, opp in enumerate(selected.product_opportunities):
            color = opp_colors[i % len(opp_colors)]
            st.markdown(
                f'<div class="if-opp {color}">'
                f'<div class="t">{opp.opportunity}</div>'
                f'<div class="d">关联痛点：{opp.related_pain}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown('<div style="font-size:14px;color:var(--text-3)">无产品机会点数据</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if len(st.session_state.results) >= 2:
        if render_flow_cta("多访谈交叉分析", "查看需求聚类和跨访谈洞察", "🔗 进入需求聚类", "cta_insight_to_cluster"):
            navigate_to(PAGES[3])
    else:
        if render_flow_cta("继续添加访谈", "再分析 1 份访谈即可解锁多访谈洞察", "📝 新建访谈", "cta_insight_to_input"):
            navigate_to(PAGES[1])


# ==================== 页面：需求聚类 ====================
def render_page_cluster():
    render_page_header("需求聚类", "多份访谈的交叉分析和需求聚类")

    if len(st.session_state.results) < 2:
        render_empty_state("🔗", "需要至少 2 份访谈分析结果才能生成需求聚类")
        return

    results = st.session_state.results

    all_tags = []
    for r in results:
        all_tags.extend(r.tags)
    tag_freq = {}
    for t in all_tags:
        tag_freq[t] = tag_freq.get(t, 0) + 1

    if tag_freq:
        st.markdown('<div class="if-section">', unsafe_allow_html=True)
        st.markdown('<div class="if-section-title">需求标签词云</div>', unsafe_allow_html=True)
        mx = max(tag_freq.values())
        def _pill_size(freq, mx):
            r = freq / mx if mx else 0
            if r >= 0.7: return "lg"
            if r >= 0.4: return "md"
            return "sm"
        pills_html = "".join(
            f'<span class="if-pill {_pill_size(f, mx)}">{t}</span>'
            for t, f in sorted(tag_freq.items(), key=lambda x: -x[1])
        )
        st.markdown(pills_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col_chart1, col_chart2 = st.columns(2)
    chart_pairs = [
        (col_chart1, [(plot_tag_frequency, results), (plot_pain_severity, results)]),
        (col_chart2, [(plot_emotion_distribution, results), (plot_rice_scores, st.session_state.rice_scores)]),
    ]

    for col, plots in chart_pairs:
        with col:
            for plot_fn, data in plots:
                fig = plot_fn(data)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.markdown(
                        '<div style="text-align:center;padding:40px;color:var(--text-3);font-size:14px">'
                        '📊 暂无足够数据'
                        '</div>',
                        unsafe_allow_html=True,
                    )

    st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

    st.markdown('<div class="if-section">', unsafe_allow_html=True)
    st.markdown('<div class="if-section-title">需求聚类</div>', unsafe_allow_html=True)
    if st.button("✨ 生成需求聚类", type="primary"):
        analysis_results_str = "\n\n---\n\n".join(
            json.dumps(dataclass_to_dict(r), ensure_ascii=False) for r in results
        )

        with st.spinner("正在生成需求聚类，请稍候..."):
            prompt = CLUSTER_PROMPT.format(analysis_results=analysis_results_str)
            cluster = call_and_validate(prompt, validate_cluster_result, "聚类结果校验失败")

        if cluster is not None:
            st.session_state.cluster_result = cluster
            _save_state()
            st.success("✅ 需求聚类生成完成！")
    st.markdown('</div>', unsafe_allow_html=True)

    cluster = st.session_state.cluster_result
    if not cluster:
        return

    st.markdown(
        f'<div style="margin-bottom:20px;font-size:14px;color:var(--text-2)">'
        f'共分析 <span class="if-count">{cluster.total_interviews} 份</span> 访谈，'
        f'识别出 <span class="if-count">{len(cluster.demand_clusters)} 个</span> 需求聚类'
        f'</div>',
        unsafe_allow_html=True,
    )

    cluster_cards_html = '<div class="if-cluster-grid">'
    for dc in cluster.demand_clusters:
        items_html = "".join(f'<li>{item}</li>' for item in dc.items)
        cluster_cards_html += (
            f'<div class="if-cluster">'
            f'<div class="if-cluster-head">'
            f'<div class="if-cluster-title">📌 {dc.cluster_name}</div>'
            f'<span class="if-count">{dc.frequency} 次</span>'
            f'</div>'
            f'<div style="font-size:14px;color:var(--text-2);margin-bottom:10px">{dc.cluster_description}</div>'
            f'<div style="font-size:12px;color:var(--text-3);margin-bottom:8px">涉及访谈：{"、".join(dc.interview_ids)}</div>'
            f'<ul class="if-need-list">{items_html}</ul>'
            f'</div>'
        )
    cluster_cards_html += '</div>'
    st.markdown(cluster_cards_html, unsafe_allow_html=True)

    if cluster.cross_interview_insights:
        st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="if-section">', unsafe_allow_html=True)
        st.markdown('<div class="if-section-title">跨访谈洞察</div>', unsafe_allow_html=True)
        findings_html = '<div class="if-finding">'
        for insight in cluster.cross_interview_insights:
            findings_html += f'<div class="row">{insight}</div>'
        findings_html += '</div>'
        st.markdown(findings_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.rice_scores:
        if render_flow_cta("RICE 优先级评分", "量化评估产品机会点的落地优先级", "📐 查看 RICE 优先级", "cta_cluster_to_rice"):
            navigate_to(PAGES[4])
    else:
        if render_flow_cta("继续添加访谈", "更多访谈数据将提升 RICE 评分准确度", "📝 新建访谈", "cta_cluster_to_input"):
            navigate_to(PAGES[1])


# ==================== 页面：RICE 优先级 ====================
def render_page_rice():
    render_page_header("RICE 优先级", "产品机会点的 RICE 优先级评分")

    if not st.session_state.rice_scores:
        render_empty_state("📐", "暂无 RICE 评分数据，请先分析访谈")
        return

    st.markdown(
        '<div class="if-table-caption">'
        '<div class="if-section-title" style="margin-bottom:0">RICE 评分表</div>'
        '<div class="formula">RICE = (Reach × Impact × Confidence) ÷ Effort</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    head_cols = ["产品机会点", "对应痛点", "Reach", "Impact", "Confidence", "Effort", "RICE 分数", "优先级"]
    sort_keys = ["item_name", "pain_point", "reach", "impact", "confidence", "effort", "rice_score", None]

    if "_rice_sort_col" not in st.session_state:
        st.session_state._rice_sort_col = 6
    if "_rice_sort_asc" not in st.session_state:
        st.session_state._rice_sort_asc = False

    def get_sort_indicator(col_idx):
        if col_idx == st.session_state._rice_sort_col:
            return " ▲" if st.session_state._rice_sort_asc else " ▼"
        return ""

    head = "<tr>"
    for i, c in enumerate(head_cols):
        if sort_keys[i] is not None:
            head += f"<th style='cursor:pointer;user-select:none'>{c}<span class='sort-indicator'>{get_sort_indicator(i)}</span></th>"
        else:
            head += f"<th>{c}</th>"
    head += "</tr>"

    sorted_scores = list(st.session_state.rice_scores)
    sort_key = sort_keys[st.session_state._rice_sort_col]
    if sort_key:
        reverse_order = not st.session_state._rice_sort_asc
        sorted_scores.sort(
            key=lambda x: getattr(x, sort_key, 0) or 0,
            reverse=reverse_order,
        )

    for i, (c, key) in enumerate(zip(head_cols, sort_keys)):
        if key is not None:
            col_name = f"sort_{i}"
            if st.button(f"按 {c} 排序", key=col_name, help=f"点击按 {c} {'升序' if i == st.session_state._rice_sort_col and st.session_state._rice_sort_asc else '降序'}"):
                if st.session_state._rice_sort_col == i:
                    st.session_state._rice_sort_asc = not st.session_state._rice_sort_asc
                else:
                    st.session_state._rice_sort_col = i
                    st.session_state._rice_sort_asc = False
                st.rerun()

    body = ""
    for rs in sorted_scores:
        priority = "P0" if rs.rice_score and rs.rice_score >= 5 else "P1" if rs.rice_score and rs.rice_score >= 3 else "P2"
        rice_val = f"{rs.rice_score:.1f}" if rs.rice_score else "-"
        body += (
            f"<tr>"
            f"<td class='truncate' title='{rs.item_name}'>{rs.item_name}</td>"
            f"<td class='muted truncate' title='{rs.pain_point or '-'}'>{rs.pain_point or '-'}</td>"
            f"<td class='num'>{rs.reach}</td>"
            f"<td class='num'>{rs.impact}</td>"
            f"<td class='num'>{rs.confidence / 10:.0%}</td>"
            f"<td class='num'>{rs.effort}</td>"
            f"<td class='num' style='font-weight:700'>{rice_val}</td>"
            f"<td class='center'>{render_priority_badge(priority)}</td>"
            f"</tr>"
        )

    st.markdown(
        f'<div class="if-table-wrapper">'
        f'<div class="if-table-scroll-hint">← 左右滑动查看更多 →</div>'
        f'<table class="if-table-numeric"><thead>{head}</thead><tbody>{body}</tbody></table>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="if-formula">'
        '<div class="h">RICE 评分公式说明</div>'
        '<div class="grid">'
        '<div><span class="k">Reach</span> <span class="v">— 影响用户数（人/季度）</span></div>'
        '<div><span class="k">Impact</span> <span class="v">— 单用户影响度（1–5）</span></div>'
        '<div><span class="k">Confidence</span> <span class="v">— 信心系数（0–100%）</span></div>'
        '<div><span class="k">Effort</span> <span class="v">— 开发成本（人/月）</span></div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

    fig = plot_rice_scores(st.session_state.rice_scores)
    if fig:
        st.plotly_chart(fig, use_container_width=True)

    if render_flow_cta("导出洞察报告", "一键生成完整 Markdown 报告并下载", "📄 导出报告", "cta_rice_to_report"):
        navigate_to(PAGES[5])


# ==================== 页面：报告导出 ====================
def render_page_report():
    render_page_header("报告导出", "生成 Markdown 报告并下载")

    if not st.session_state.results:
        render_empty_state("📄", "请先在「新建访谈」中分析至少一份访谈")
        return

    results = st.session_state.results
    cluster = st.session_state.cluster_result
    rice_scores = st.session_state.rice_scores or []

    toc_items = [
        ("sec-background", "项目背景", False),
        ("sec-samples", "访谈样本概况", False),
        ("sec-findings", "核心发现", False),
        ("sec-pains", "高频痛点", False),
        ("sec-opps", "产品机会点", False),
        ("sec-clusters", "需求聚类结果", False),
        ("sec-rice", "RICE 优先级建议", False),
        ("sec-nextsteps", "后续验证方案", False),
    ]

    toc_html = '<ul class="if-toc">'
    for i, (sec_id, title, is_sub) in enumerate(toc_items):
        cls = "" if i > 0 else ""
        sub_cls = " sub" if is_sub else ""
        toc_html += f'<li class="{cls}{sub_cls}"><a href="#{sec_id}" class="toc-link">{title}</a></li>'
    toc_html += '</ul>'

    preview_parts = []

    preview_parts.append(f'<h1>{st.session_state._project_name} — 用户访谈洞察报告</h1>')
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    preview_parts.append(f'<p>生成时间：{now} ｜ 分析工具：InsightFlow AI</p>')

    preview_parts.append(f'<h2 id="sec-background">1. 项目背景</h2>')
    preview_parts.append(
        f'<p><strong>项目名称</strong>：{st.session_state._project_name}<br>'
        f'<strong>目标用户</strong>：{st.session_state._target_user}<br>'
        f'<strong>访谈样本数</strong>：{len(results)} 份</p>'
    )

    preview_parts.append('<h2 id="sec-samples">2. 访谈样本概况</h2>')
    profile_rows = ""
    for r in results:
        p = r.user_profile
        profile_rows += (
            f'<tr>'
            f'<td>{r.interview_id}</td>'
            f'<td>{p.role}</td>'
            f'<td>{p.industry}</td>'
            f'<td>{p.tech_level}</td>'
            f'<td>{p.usage_frequency}</td>'
            f'</tr>'
        )
    preview_parts.append(
        f'<table class="if-table-numeric">'
        f'<thead><tr><th>编号</th><th>角色</th><th>行业</th><th>技术水平</th><th>使用频率</th></tr></thead>'
        f'<tbody>{profile_rows}</tbody></table>'
    )

    preview_parts.append('<h2 id="sec-findings">3. 核心发现</h2>')
    for r in results:
        tags_html = "".join(f'<span class="if-pill sm">{t}</span>' for t in r.tags)
        preview_parts.append(
            f'<h3>{r.interview_id}</h3>'
            f'<p>{r.summary}</p>'
            f'<p><strong>使用场景</strong>：{"、".join(r.usage_scenarios)}<br>'
            f'<strong>情绪倾向</strong>：{r.emotion.label}（得分 {r.emotion.score}）— {r.emotion.reason}</p>'
            f'<div style="margin-bottom:12px">{tags_html}</div>'
        )

    preview_parts.append('<h2 id="sec-pains">4. 高频痛点</h2>')
    all_pains = []
    for r in results:
        for pp in r.pain_points:
            all_pains.append((r.interview_id, pp))
    all_pains.sort(key=lambda x: x[1].severity, reverse=True)
    for iid, pp in all_pains:
        dots = ''.join(
            '<span class="dot on"></span>' if i < pp.severity else '<span class="dot"></span>'
            for i in range(5)
        )
        preview_parts.append(
            f'<div class="if-pain embedded">'
            f'<div class="if-pain-head">'
            f'<div class="if-pain-title">{pp.pain}</div>'
            f'<div class="if-severity">严重程度 '
            f'<span class="dots">{dots}</span> '
            f'<span class="score">{pp.severity}/5</span>'
            f'</div>'
            f'</div>'
            f'{render_quote_block(pp.evidence, f"来源：{iid}")}'
            f'</div>'
        )

    preview_parts.append('<h2 id="sec-opps">5. 产品机会点</h2>')
    for r in results:
        for opp in r.product_opportunities:
            preview_parts.append(
                f'<div class="if-opp green">'
                f'<div class="t">💡 {opp.opportunity}</div>'
                f'<div class="d">关联痛点：{opp.related_pain} ｜ 来源：{r.interview_id}</div>'
                f'</div>'
            )

    preview_parts.append('<h2 id="sec-clusters">6. 需求聚类结果</h2>')
    if cluster:
        preview_parts.append(
            f'<p>共分析 <span class="if-count">{cluster.total_interviews} 份</span> 访谈，'
            f'识别出 <span class="if-count">{len(cluster.demand_clusters)} 个</span> 需求聚类。</p>'
        )
        cluster_items = ""
        for dc in cluster.demand_clusters:
            cluster_items += (
                f'<div class="item">'
                f'<div class="t">📌 {dc.cluster_name}</div>'
                f'<div class="m">{dc.cluster_description}（{dc.frequency} 次）</div>'
                f'</div>'
            )
        preview_parts.append(f'<div class="if-mini-cluster">{cluster_items}</div>')

        if cluster.cross_interview_insights:
            findings_html = '<div class="if-finding">'
            for insight in cluster.cross_interview_insights:
                findings_html += f'<div class="row">{insight}</div>'
            findings_html += '</div>'
            preview_parts.append(findings_html)
    else:
        preview_parts.append('<p>暂无聚类结果（需上传 2 份以上访谈后生成）。</p>')

    preview_parts.append('<h2 id="sec-rice">7. RICE 优先级建议</h2>')
    if rice_scores:
        preview_parts.append(
            '<div class="if-formula">'
            '<div class="formula">RICE = (Reach × Impact × Confidence) ÷ Effort</div>'
            '</div>'
        )
        rice_head = "<tr><th>机会点</th><th>RICE 分数</th><th>优先级</th></tr>"
        rice_body = ""
        for rs in rice_scores:
            priority = "P0" if rs.rice_score and rs.rice_score >= 5 else "P1" if rs.rice_score and rs.rice_score >= 3 else "P2"
            rice_val = f"{rs.rice_score:.1f}" if rs.rice_score else "-"
            rice_body += (
                f'<tr>'
                f'<td>{rs.item_name}</td>'
                f'<td class="num" style="font-weight:700">{rice_val}</td>'
                f'<td class="center">{render_priority_badge(priority)}</td>'
                f'</tr>'
            )
        preview_parts.append(
            f'<table class="if-table-numeric"><thead>{rice_head}</thead><tbody>{rice_body}</tbody></table>'
        )
    else:
        preview_parts.append('<p>暂无 RICE 评分（需先分析访谈并生成机会点）。</p>')

    preview_parts.append('<h2 id="sec-nextsteps">8. 后续验证方案</h2>')
    preview_parts.append(
        '<ol style="font-size:14px;color:var(--text-2);line-height:1.7;padding-left:20px">'
        '<li><strong>定量验证</strong>：针对高频痛点设计问卷，扩大样本量验证痛点普遍性。</li>'
        '<li><strong>可用性测试</strong>：针对高 RICE 分数的机会点制作原型，观察用户实际操作反馈。</li>'
        '<li><strong>A/B 测试</strong>：对优先级接近的机会点进行 A/B 测试，用数据决定落地顺序。</li>'
        '<li><strong>持续访谈</strong>：每季度补充 3-5 份新访谈，追踪痛点变化和需求演进。</li>'
        '</ol>'
    )

    preview_html = '<div class="if-report-preview">' + "".join(preview_parts) + '</div>'

    export_panel_html = (
        '<div class="if-export-panel">'
        '<div class="if-card" style="padding:20px">'
        '<div class="group-title">📤 导出选项</div>'
        '<div class="export-option active">'
        '<div class="opt-header"><span class="opt-icon">📝</span><span>Markdown</span></div>'
        '<div class="opt-desc">原始格式，支持任何 Markdown 编辑器</div>'
        '</div>'
        '<div class="export-option">'
        '<div class="opt-header"><span class="opt-icon">📄</span><span>PDF（开发中）</span></div>'
        '<div class="opt-desc">打印友好格式，即将上线</div>'
        '</div>'
        '<div class="export-option">'
        '<div class="opt-header"><span class="opt-icon">📊</span><span>CSV 数据（开发中）</span></div>'
        '<div class="opt-desc">结构化数据，便于 Excel 分析</div>'
        '</div>'
        '<div class="export-status" id="export-status"></div>'
        '</div>'
        '</div>'
    )

    st.markdown(
        f'<div class="if-report-layout">'
        f'<div>{toc_html}</div>'
        f'{preview_html}'
        f'{export_panel_html}'
        f'</div>'
        f'<script>'
        f'(function(){{'
        f'const toc=document.querySelector(".if-toc");'
        f'const sections=document.querySelectorAll(".if-report-preview h2[id]");'
        f'const tocItems=toc.querySelectorAll("li");'
        f'function updateActive(){{'
        f'let current=sections[0]?.id||"";'
        f'sections.forEach(s=>{{'
        f'const rect=s.getBoundingClientRect();'
        f'if(rect.top<=100)current=s.id;'
        f'}});'
        f'tocItems.forEach(li=>{{'
        f'li.classList.toggle("active",li.querySelector("a")?.getAttribute("href")==="#"+current);'
        f'}});'
        f'}}'
        f'toc.addEventListener("click",e=>{{'
        f'e.preventDefault();'
        f'const link=e.target.closest(".toc-link");'
        f'if(link){{'
        f'document.querySelector(link.getAttribute("href"))?.scrollIntoView({{behavior:"smooth",block:"start"}});'
        f'}}'
        f'}});'
        f'window.addEventListener("scroll",updateActive,{{passive:true}});'
        f'updateActive();'
        f'}})();'
        f'</script>',
        unsafe_allow_html=True,
    )

    st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

    col_gen, col_spacer = st.columns([1, 3])
    with col_gen:
        report_exists = "md_report" in st.session_state and st.session_state.md_report
        btn_label = "🔄 重新生成报告" if report_exists else "📋 生成 Markdown 报告"
        generating = st.button(btn_label, type="primary", use_container_width=True, disabled=not bool(results))

        if generating:
            progress_bar = st.progress(0, text="准备生成...")
            status_text = st.empty()

            try:
                status_text.text("正在分析访谈数据... (20%)")
                progress_bar.progress(20)
                import time; time.sleep(0.2)

                status_text.text("正在提取核心洞察... (50%)")
                progress_bar.progress(50)

                st.session_state.md_report = generate_markdown_report(
                    project_name=st.session_state._project_name,
                    target_user=st.session_state._target_user,
                    results=results,
                    cluster_result=cluster,
                    rice_scores=rice_scores or None,
                )

                status_text.text("正在格式化报告... (90%)")
                progress_bar.progress(90)
                time.sleep(0.15)

                progress_bar.progress(100)
                status_text.empty()
                st.success("✅ Markdown 报告已生成！")
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ 生成失败：{str(e)}")

    if "md_report" not in st.session_state:
        st.info("💡 点击上方「生成报告」按钮后即可下载")
        return

    st.markdown('<div class="if-download-section">', unsafe_allow_html=True)
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        md_size = len(st.session_state.md_report.encode("utf-8")) / 1024
        st.download_button(
            label=f"📝 Markdown 报告 ({md_size:.1f} KB)",
            data=st.session_state.md_report.encode("utf-8"),
            file_name=f"{st.session_state._project_name}_访谈洞察报告.md",
            mime="text/markdown",
            use_container_width=True,
            help="兼容 Typora / Obsidian / VS Code",
        )
        st.caption("推荐：适合文档编辑和版本管理")
    with col_dl2:
        json_data = json.dumps(
            [dataclass_to_dict(r) for r in results],
            ensure_ascii=False,
            indent=2,
        )
        json_size = len(json_data.encode("utf-8")) / 1024
        st.download_button(
            label=f"📊 JSON 数据 ({json_size:.1f} KB)",
            data=json_data.encode("utf-8"),
            file_name=f"{st.session_state._project_name}_分析结果.json",
            mime="application/json",
            use_container_width=True,
            help="结构化数据，支持程序化处理",
        )
        st.caption("适合：数据分析和二次开发")
    st.markdown('</div>', unsafe_allow_html=True)


PAGE_RENDERERS = {
    PAGES[0]: render_page_dashboard,
    PAGES[1]: render_page_input,
    PAGES[2]: render_page_insight,
    PAGES[3]: render_page_cluster,
    PAGES[4]: render_page_rice,
    PAGES[5]: render_page_report,
}


def main():
    st.set_page_config(
        page_title="InsightFlow AI",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_global_css()
    init_session_state()

    with st.sidebar:
        render_sidebar_logo()
        current = st.radio("导航", PAGES, index=PAGES.index(st.session_state.current_page), label_visibility="collapsed")
        if current != st.session_state.current_page:
            st.session_state.current_page = current
            st.rerun()

    PAGE_RENDERERS[st.session_state.current_page]()


main()
