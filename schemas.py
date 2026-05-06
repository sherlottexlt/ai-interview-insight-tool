from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UserProfile:
    role: str = ""
    industry: str = ""
    tech_level: str = ""
    usage_frequency: str = ""


@dataclass
class PainPoint:
    pain: str = ""
    evidence: str = ""
    severity: int = 3


@dataclass
class ExplicitNeed:
    need: str = ""
    source: str = ""


@dataclass
class ImplicitNeed:
    need: str = ""
    inferred_from: str = ""


@dataclass
class Emotion:
    label: str = ""
    score: float = 0.0
    reason: str = ""


@dataclass
class ProductOpportunity:
    opportunity: str = ""
    related_pain: str = ""


@dataclass
class InterviewAnalysisResult:
    interview_id: str = ""
    summary: str = ""
    user_profile: UserProfile = field(default_factory=UserProfile)
    usage_scenarios: list[str] = field(default_factory=list)
    pain_points: list[PainPoint] = field(default_factory=list)
    explicit_needs: list[ExplicitNeed] = field(default_factory=list)
    implicit_needs: list[ImplicitNeed] = field(default_factory=list)
    emotion: Emotion = field(default_factory=Emotion)
    tags: list[str] = field(default_factory=list)
    product_opportunities: list[ProductOpportunity] = field(default_factory=list)


@dataclass
class DemandCluster:
    cluster_name: str = ""
    cluster_description: str = ""
    items: list[str] = field(default_factory=list)
    interview_ids: list[str] = field(default_factory=list)
    frequency: int = 0


@dataclass
class ClusterResult:
    total_interviews: int = 0
    tag_statistics: dict[str, int] = field(default_factory=dict)
    demand_clusters: list[DemandCluster] = field(default_factory=list)
    cross_interview_insights: list[str] = field(default_factory=list)


@dataclass
class RiceScoreItem:
    item_name: str = ""
    pain_point: str = ""
    reach: int = 5
    impact: int = 4
    confidence: int = 7
    effort: int = 3
    rice_score: Optional[float] = None
    source_interview_ids: list[str] = field(default_factory=list)


def _dict_to_user_profile(d: dict) -> UserProfile:
    return UserProfile(
        role=d.get("role", ""),
        industry=d.get("industry", ""),
        tech_level=d.get("tech_level", ""),
        usage_frequency=d.get("usage_frequency", ""),
    )


def _dict_to_pain_point(d: dict) -> PainPoint:
    return PainPoint(
        pain=d.get("pain", ""),
        evidence=d.get("evidence", ""),
        severity=d.get("severity", 3),
    )


def _dict_to_explicit_need(d: dict) -> ExplicitNeed:
    return ExplicitNeed(
        need=d.get("need", ""),
        source=d.get("source", ""),
    )


def _dict_to_implicit_need(d: dict) -> ImplicitNeed:
    return ImplicitNeed(
        need=d.get("need", ""),
        inferred_from=d.get("inferred_from", ""),
    )


def _dict_to_emotion(d: dict) -> Emotion:
    return Emotion(
        label=d.get("label", ""),
        score=d.get("score", 0.0),
        reason=d.get("reason", ""),
    )


def _dict_to_product_opportunity(d: dict) -> ProductOpportunity:
    return ProductOpportunity(
        opportunity=d.get("opportunity", ""),
        related_pain=d.get("related_pain", ""),
    )


def dict_to_interview_result(d: dict) -> InterviewAnalysisResult:
    return InterviewAnalysisResult(
        interview_id=d.get("interview_id", ""),
        summary=d.get("summary", ""),
        user_profile=_dict_to_user_profile(d.get("user_profile", {})),
        usage_scenarios=d.get("usage_scenarios", []),
        pain_points=[_dict_to_pain_point(pp) for pp in d.get("pain_points", [])],
        explicit_needs=[_dict_to_explicit_need(en) for en in d.get("explicit_needs", [])],
        implicit_needs=[_dict_to_implicit_need(im) for im in d.get("implicit_needs", [])],
        emotion=_dict_to_emotion(d.get("emotion", {})),
        tags=d.get("tags", []),
        product_opportunities=[_dict_to_product_opportunity(op) for op in d.get("product_opportunities", [])],
    )


def _dict_to_demand_cluster(d: dict) -> DemandCluster:
    return DemandCluster(
        cluster_name=d.get("cluster_name", ""),
        cluster_description=d.get("cluster_description", ""),
        items=d.get("items", []),
        interview_ids=d.get("interview_ids", []),
        frequency=d.get("frequency", 0),
    )


def dict_to_cluster_result(d: dict) -> ClusterResult:
    return ClusterResult(
        total_interviews=d.get("total_interviews", 0),
        tag_statistics=d.get("tag_statistics", {}),
        demand_clusters=[_dict_to_demand_cluster(dc) for dc in d.get("demand_clusters", [])],
        cross_interview_insights=d.get("cross_interview_insights", []),
    )


def dataclass_to_dict(obj) -> dict:
    import dataclasses
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        result = {}
        for f in dataclasses.fields(obj):
            val = getattr(obj, f.name)
            if dataclasses.is_dataclass(val) and not isinstance(val, type):
                result[f.name] = dataclass_to_dict(val)
            elif isinstance(val, list):
                result[f.name] = [dataclass_to_dict(item) if dataclasses.is_dataclass(item) and not isinstance(item, type) else item for item in val]
            elif isinstance(val, dict):
                result[f.name] = val
            else:
                result[f.name] = val
        return result
    return obj
