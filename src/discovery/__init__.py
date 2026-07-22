"""Discovery source interfaces and pipeline components for OpportunityLab."""

from src.discovery.discovery_run import DiscoveryRun
from src.discovery.execution_result import SourceExecutionResult
from src.discovery.opportunity_deduplicator import OpportunityDeduplicator
from src.discovery.opportunity_normalizer import OpportunityNormalizer
from src.discovery.result_aggregator import ResultAggregator
from src.discovery.search_source import SearchSource
from src.discovery.source_registry import SourceRegistry

__all__ = [
    "DiscoveryRun",
    "OpportunityDeduplicator",
    "OpportunityNormalizer",
    "ResultAggregator",
    "SearchSource",
    "SourceExecutionResult",
    "SourceRegistry",
]
