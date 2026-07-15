"""
OpportunityLab AI Tasks

Defines the jobs that AI providers may perform.
"""


class AITask:

    OPPORTUNITY_ANALYSIS = "opportunity_analysis"
    RELATED_SEARCHES = "related_searches"
    DRAFT_EMAIL = "draft_email"
    DRAFT_APPLICATION = "draft_application"
    CREATE_CHECKLIST = "create_checklist"
    REWRITE_TEXT = "rewrite_text"

    ALL = {
        OPPORTUNITY_ANALYSIS,
        RELATED_SEARCHES,
        DRAFT_EMAIL,
        DRAFT_APPLICATION,
        CREATE_CHECKLIST,
        REWRITE_TEXT
    }

    @classmethod
    def is_valid(cls, task):

        return task in cls.ALL