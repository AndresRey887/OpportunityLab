"""Discovery source interfaces for OpportunityLab."""

from src.discovery.discovery_result import DiscoveryBatchResult, SourceExecutionResult
from src.discovery.result_aggregator import ResultAggregator
from src.discovery.search_source import SearchSource
from src.discovery.source_registry import SourceRegistry

__all__ = [
    "DiscoveryBatchResult",
    "ResultAggregator",
    "SearchSource",
    "SourceExecutionResult",
    "SourceRegistry",
]
