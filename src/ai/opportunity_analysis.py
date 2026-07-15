"""
Opportunity Analysis Model

Central AI model used throughout OpportunityLab.
"""

from datetime import datetime


class OpportunityAnalysis:

    def __init__(
        self,
        summary="",
        category="",
        confidence=0,
        opportunity_value=0,
        difficulty="Unknown",
        time_sensitivity="Unknown",
        estimated_effort="Unknown",
        recommended_action="",
        positives=None,
        negatives=None,
        tags=None,
        warnings=None,
        analysed_at=None,
        provider="",
        model=""
    ):

        self.summary = summary
        self.category = category
        self.confidence = confidence
        self.opportunity_value = opportunity_value
        self.difficulty = difficulty
        self.time_sensitivity = time_sensitivity
        self.estimated_effort = estimated_effort
        self.recommended_action = recommended_action

        self.positives = positives or []
        self.negatives = negatives or []
        self.tags = tags or []
        self.warnings = warnings or []

        self.provider = provider
        self.model = model

        self.analysed_at = (
            analysed_at
            if analysed_at
            else datetime.now().isoformat(timespec="seconds")
        )

    def add_positive(self, text):

        text = str(text).strip()

        if text:
            self.positives.append(text)

    def add_negative(self, text):

        text = str(text).strip()

        if text:
            self.negatives.append(text)

    def add_tag(self, tag):

        tag = str(tag).strip()

        if tag:
            self.tags.append(tag)

    def add_warning(self, warning):

        warning = str(warning).strip()

        if warning:
            self.warnings.append(warning)

    def to_dict(self):

        return {
            "summary": self.summary,
            "category": self.category,
            "confidence": self.confidence,
            "opportunity_value": self.opportunity_value,
            "difficulty": self.difficulty,
            "time_sensitivity": self.time_sensitivity,
            "estimated_effort": self.estimated_effort,
            "recommended_action": self.recommended_action,
            "positives": list(self.positives),
            "negatives": list(self.negatives),
            "tags": list(self.tags),
            "warnings": list(self.warnings),
            "provider": self.provider,
            "model": self.model,
            "analysed_at": self.analysed_at
        }

    @classmethod
    def from_dict(cls, data):

        if not isinstance(data, dict):
            return cls()

        return cls(
            summary=data.get("summary", ""),
            category=data.get("category", ""),
            confidence=data.get("confidence", 0),
            opportunity_value=data.get("opportunity_value", 0),
            difficulty=data.get("difficulty", "Unknown"),
            time_sensitivity=data.get("time_sensitivity", "Unknown"),
            estimated_effort=data.get("estimated_effort", "Unknown"),
            recommended_action=data.get("recommended_action", ""),
            positives=data.get("positives", []),
            negatives=data.get("negatives", []),
            tags=data.get("tags", []),
            warnings=data.get("warnings", []),
            provider=data.get("provider", ""),
            model=data.get("model", ""),
            analysed_at=data.get("analysed_at")
        )

    def __repr__(self):

        return (
            "OpportunityAnalysis("
            f"value={self.opportunity_value}, "
            f"confidence={self.confidence}, "
            f"category='{self.category}'"
            ")"
        )