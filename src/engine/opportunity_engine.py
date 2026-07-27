"""
Opportunity Engine

Evaluates opportunities using a collection of rules.
"""

from src.rules.product_rule import ProductRule
from src.rules.business_rule import BusinessRule
from src.rules.supplier_rule import SupplierRule
from src.rules.manufacturer_rule import ManufacturerRule
from src.rules.australian_rule import AustralianRule
from src.core.app_logger import get_logger
from src.rules.profile_opportunity_rule import ProfileOpportunityRule
from src.rules.evidence_quality_rule import EvidenceQualityRule
from src.rules.supporter_prospect_rule import SupporterProspectRule


logger = get_logger("OpportunityEngine")


class OpportunityEngine:

    def __init__(self, profile_service=None):

        logger.info("Engine ready")

        self.rules = [

            ProductRule(),
            BusinessRule(),
            SupplierRule(),
            ManufacturerRule(),
            AustralianRule(),
            ProfileOpportunityRule(profile_service),
            SupporterProspectRule(profile_service),
            EvidenceQualityRule(),

        ]

    def score(self, opportunity):

        total_score = 0

        for rule in self.rules:

            total_score += rule.evaluate(opportunity)

        opportunity.score = max(0, min(total_score, 100))

        return opportunity
