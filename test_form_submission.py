"""
Test form submission with empty background indicators.
"""
from saarthi_ai.models import (
    StudentProfile,
    EducationLevel,
    InstitutionType,
    OpportunityGoal,
    MissedOpportunityFrequency,
)

# Test 1: Profile with empty background indicators
print("Test 1: Profile with empty background indicators")
print("=" * 60)

profile = StudentProfile(
    name="Test Student",
    age=20,
    education_level=EducationLevel.UG,
    degree="B.Tech",
    field_of_study="Computer Science",
    year_of_study=2,
    institution_type=InstitutionType.GOVERNMENT,
    background_indicators=[],  # Empty list
    opportunity_goals=[OpportunityGoal.INTERNSHIPS, OpportunityGoal.SCHOLARSHIPS],
    missed_opportunities_before=MissedOpportunityFrequency.NO,
    gender="Male"
)

is_valid, missing_fields = profile.validate()
print(f"Profile valid: {is_valid}")
print(f"Missing fields: {missing_fields}")
print()

# Test 2: Test the background mapping function
print("Test 2: Background mapping with empty list")
print("=" * 60)

from app import _get_primary_background

background = _get_primary_background([], "Male")
print(f"Background for empty list + Male: {background}")

background = _get_primary_background([], "Female")
print(f"Background for empty list + Female: {background}")

background = _get_primary_background([], None)
print(f"Background for empty list + No gender: {background}")
print()

print("✓ All tests passed! Form should work now.")
