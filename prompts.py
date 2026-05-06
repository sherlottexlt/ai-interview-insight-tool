INTERVIEW_ANALYSIS_PROMPT = """你是一位资深 AI 产品经理和用户研究专家，擅长从用户访谈文本中提取结构化洞察。

请对以下用户访谈文本进行深度分析，输出严格的 JSON 对象。

## 严格规则
1. 只输出一个 JSON 对象，不要输出 Markdown 代码块标记（不要 ```json ```），不要输出任何解释性文字。
2. 每个痛点的 evidence 字段必须填写用户原话，不允许编造或改写。
3. 如果信息不确定或访谈中未提及，填写 "unknown"，不要编造。
4. severity 为 1-5 的整数，5 表示最严重。
5. emotion.score 为 -1 到 1 之间的小数，-1 表示极消极，1 表示极积极。
6. tags 为简短关键词列表，如：效率、协作、安全、学习成本等。
7. summary 为 100-200 字的中文摘要。

## 输出 JSON 结构
{{
  "interview_id": "访谈编号，如 interview_1",
  "summary": "访谈摘要，100-200字",
  "user_profile": {{
    "role": "用户角色/职业身份",
    "industry": "所在行业",
    "tech_level": "技术水平：初学者/中级/高级",
    "usage_frequency": "使用频率：偶尔/每周/每天"
  }},
  "usage_scenarios": ["使用场景1", "使用场景2"],
  "pain_points": [
    {{
      "pain": "痛点描述",
      "evidence": "用户原话，必须逐字引用",
      "severity": 3
    }}
  ],
  "explicit_needs": [
    {{
      "need": "显性需求描述",
      "source": "用户原话"
    }}
  ],
  "implicit_needs": [
    {{
      "need": "隐性需求描述（用户未直接说出但可推断）",
      "inferred_from": "推断依据的用户原话"
    }}
  ],
  "emotion": {{
    "label": "情绪标签，如：积极/中性/消极/焦虑/兴奋",
    "score": 0.3,
    "reason": "情绪判断依据"
  }},
  "tags": ["标签1", "标签2"],
  "product_opportunities": [
    {{
      "opportunity": "产品机会点描述",
      "related_pain": "关联的痛点描述"
    }}
  ]
}}

## 访谈编号
{interview_id}

## 访谈文本
{interview_text}"""


CLUSTER_PROMPT = """你是一位资深 AI 产品经理和用户研究专家，擅长从多份用户访谈分析结果中发现共性需求和跨访谈洞察。

请对以下多份访谈的分析结果进行需求聚类和标签统计，输出严格的 JSON 对象。

## 严格规则
1. 只输出一个 JSON 对象，不要输出 Markdown 代码块标记（不要 ```json ```），不要输出任何解释性文字。
2. 将语义相近的需求和痛点归入同一聚类，每个聚类需包含涉及该聚类的访谈编号。
3. tag_statistics 统计所有访谈中各标签出现的总次数。
4. cross_interview_insights 提取跨访谈的共性洞察，至少 3 条。
5. 不要编造信息，所有聚类必须基于提供的分析结果。

## 输出 JSON 结构
{{
  "total_interviews": 3,
  "tag_statistics": {{
    "效率": 5,
    "协作": 3
  }},
  "demand_clusters": [
    {{
      "cluster_name": "聚类名称",
      "cluster_description": "聚类描述",
      "items": ["属于该聚类的需求/痛点1", "属于该聚类的需求/痛点2"],
      "interview_ids": ["interview_1", "interview_2"],
      "frequency": 2
    }}
  ],
  "cross_interview_insights": [
    "跨访谈洞察1",
    "跨访谈洞察2"
  ]
}}

## 多份访谈分析结果
{analysis_results}"""
