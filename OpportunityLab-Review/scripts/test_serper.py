from src.core.search_service import SearchService

service = SearchService()

results = service.search("woodworking company product tester")

print("\n=== Opportunities ===\n")

for i, opportunity in enumerate(results, start=1):
    print(f"{i}. {opportunity.title}")
    print(f"   {opportunity.url}")
    print(f"   {opportunity.snippet}")
    print()