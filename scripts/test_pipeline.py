from src.core.database_service import DatabaseService
from src.core.search_service import SearchService

print("=== OpportunityLab Pipeline Test ===")

database = DatabaseService()
database.initialize()

search = SearchService()

results = search.search("woodworking product tester")

print(f"\nResults returned: {len(results)}\n")

for opportunity in results:

    print("=" * 80)
    print(f"Title   : {opportunity.title}")
    print(f"Score   : {opportunity.score}")
    print(f"Source  : {opportunity.source}")
    print(f"URL     : {opportunity.url}")
    print()

    print("Rule Breakdown")
    print("-" * 30)

    for rule in opportunity.rule_results:

        print(
            f"{rule['rule']:<25} +{rule['points']}"
        )

    print()

    database.save_opportunity(opportunity)

print("\nPipeline test complete.")