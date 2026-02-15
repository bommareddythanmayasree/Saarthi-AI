"""
Quick test script for the JSON matcher.
"""
from saarthi_ai.json_matcher import JSONOpportunityMatcher

# Initialize matcher
matcher = JSONOpportunityMatcher()

# Test student profile 1: UG Engineering student, 1st year
student1 = {
    'education_level': 'UG',
    'field': 'Engineering',
    'year': '1st',
    'institution_type': 'Government',
    'background': 'Financial Need'
}

print("=" * 60)
print("Test 1: UG Engineering, 1st year, Government, Financial Need")
print("=" * 60)
matches1 = matcher.match_opportunities(student1)
print(f"Found {len(matches1)} matches:\n")
for match in matches1[:5]:  # Show top 5
    print(f"✓ {match['opportunity_name']}")
    print(f"  Category: {match['category']}")
    print(f"  Score: {match['matching_score']}/7")
    print(f"  Why missed: {match['why_missed']}")
    print()

# Test student profile 2: UG Science student, 2nd year
student2 = {
    'education_level': 'UG',
    'field': 'Science',
    'year': '2nd',
    'institution_type': 'Any',
    'background': 'Any'
}

print("=" * 60)
print("Test 2: UG Science, 2nd year, Any institution, Any background")
print("=" * 60)
matches2 = matcher.match_opportunities(student2)
print(f"Found {len(matches2)} matches:\n")
for match in matches2[:5]:  # Show top 5
    print(f"✓ {match['opportunity_name']}")
    print(f"  Category: {match['category']}")
    print(f"  Score: {match['matching_score']}/7")
    print(f"  Impact: {match['impact_level']}")
    print()

# Test student profile 3: UG Engineering, 3rd year, Female
student3 = {
    'education_level': 'UG',
    'field': 'Engineering',
    'year': '3rd',
    'institution_type': 'Any',
    'background': 'Women'
}

print("=" * 60)
print("Test 3: UG Engineering, 3rd year, Women")
print("=" * 60)
matches3 = matcher.match_opportunities(student3)
print(f"Found {len(matches3)} matches:\n")
for match in matches3[:5]:  # Show top 5
    print(f"✓ {match['opportunity_name']}")
    print(f"  Category: {match['category']}")
    print(f"  Score: {match['matching_score']}/7")
    print(f"  Awareness: {match['awareness_level']}")
    print()

# Test eligibility function directly
print("=" * 60)
print("Test 4: Direct eligibility check")
print("=" * 60)
test_opp = {
    'education_level': 'UG',
    'eligible_fields': 'Engineering',
    'target_year': '1st',
    'institution_type': 'Any',
    'background_priority': 'Any'
}

test_student = {
    'education_level': 'UG',
    'field': 'Engineering',
    'year': '1st',
    'institution_type': 'Government',
    'background': 'Any'
}

is_eligible = matcher.is_eligible(test_student, test_opp)
print(f"Student eligible for test opportunity: {is_eligible}")

score = matcher.calculate_score(test_student, test_opp)
print(f"Matching score: {score}/7")
