"""
Property-based tests for form validation.

Feature: saarthi-ai-opportunity-finder
Property 1: Form Validation Correctness
Validates: Requirements 1.5, 1.6
"""
import pytest
from hypothesis import given, strategies as st
from saarthi_ai.models import (
    StudentProfile,
    EducationLevel,
    InstitutionType,
    BackgroundIndicator,
    OpportunityGoal,
    MissedOpportunityFrequency,
)


# Strategy for generating education levels
education_level_strategy = st.sampled_from(list(EducationLevel))

# Strategy for generating institution types
institution_type_strategy = st.sampled_from(list(InstitutionType))

# Strategy for generating background indicators
background_indicator_strategy = st.lists(
    st.sampled_from(list(BackgroundIndicator)),
    min_size=1,
    max_size=5
)

# Strategy for generating opportunity goals
opportunity_goal_strategy = st.lists(
    st.sampled_from(list(OpportunityGoal)),
    min_size=1,
    max_size=5
)

# Strategy for generating missed opportunity frequency
missed_opportunity_strategy = st.sampled_from(list(MissedOpportunityFrequency))


# Strategy for generating valid complete profiles
@st.composite
def valid_profile_strategy(draw):
    """Generate a valid complete student profile."""
    return StudentProfile(
        name=draw(st.text(min_size=1, max_size=50).filter(lambda x: x.strip())),
        age=draw(st.integers(min_value=1, max_value=100)),
        education_level=draw(education_level_strategy),
        degree=draw(st.text(min_size=1, max_size=50).filter(lambda x: x.strip())),
        field_of_study=draw(st.text(min_size=1, max_size=50).filter(lambda x: x.strip())),
        year_of_study=draw(st.integers(min_value=1, max_value=10)),
        institution_type=draw(institution_type_strategy),
        background_indicators=draw(background_indicator_strategy),
        opportunity_goals=draw(opportunity_goal_strategy),
        missed_opportunities_before=draw(missed_opportunity_strategy),
        gender=draw(st.one_of(st.none(), st.text(min_size=1, max_size=20))),
        additional_context=draw(st.one_of(st.none(), st.text(max_size=200))),
    )


# Strategy for generating profiles with missing fields
@st.composite
def incomplete_profile_strategy(draw):
    """Generate a student profile with at least one missing required field."""
    # Start with a valid profile
    profile_dict = {
        "name": draw(st.one_of(st.none(), st.just(""), st.text(min_size=1, max_size=50))),
        "age": draw(st.one_of(st.none(), st.integers(max_value=0), st.integers(min_value=1, max_value=100))),
        "education_level": draw(st.one_of(st.none(), education_level_strategy)),
        "degree": draw(st.one_of(st.none(), st.just(""), st.text(min_size=1, max_size=50))),
        "field_of_study": draw(st.one_of(st.none(), st.just(""), st.text(min_size=1, max_size=50))),
        "year_of_study": draw(st.one_of(st.none(), st.integers(max_value=0), st.integers(min_value=1, max_value=10))),
        "institution_type": draw(st.one_of(st.none(), institution_type_strategy)),
        "background_indicators": draw(st.one_of(st.just([]), background_indicator_strategy)),
        "opportunity_goals": draw(st.one_of(st.just([]), opportunity_goal_strategy)),
        "missed_opportunities_before": draw(st.one_of(st.none(), missed_opportunity_strategy)),
        "gender": draw(st.one_of(st.none(), st.text(min_size=1, max_size=20))),
        "additional_context": draw(st.one_of(st.none(), st.text(max_size=200))),
    }
    
    # Ensure at least one required field is invalid
    has_invalid_field = (
        profile_dict["name"] is None or profile_dict["name"] == "" or
        profile_dict["age"] is None or profile_dict["age"] <= 0 or
        profile_dict["education_level"] is None or
        profile_dict["degree"] is None or profile_dict["degree"] == "" or
        profile_dict["field_of_study"] is None or profile_dict["field_of_study"] == "" or
        profile_dict["year_of_study"] is None or profile_dict["year_of_study"] <= 0 or
        profile_dict["institution_type"] is None or
        not profile_dict["background_indicators"] or
        not profile_dict["opportunity_goals"] or
        profile_dict["missed_opportunities_before"] is None
    )
    
    # If by chance all fields are valid, force one to be invalid
    if not has_invalid_field:
        profile_dict["name"] = None
    
    return StudentProfile(**profile_dict)


@given(valid_profile_strategy())
def test_property_valid_profiles_accepted(profile):
    """
    Property 1: Form Validation Correctness - Valid profiles should be accepted.
    
    For any student profile submission, if all required fields are present,
    the submission should be accepted.
    
    Validates: Requirements 1.5, 1.6
    """
    is_valid, missing_fields = profile.validate()
    
    assert is_valid, f"Valid profile was rejected. Missing fields: {missing_fields}"
    assert len(missing_fields) == 0, f"Valid profile reported missing fields: {missing_fields}"


@given(incomplete_profile_strategy())
def test_property_incomplete_profiles_rejected(profile):
    """
    Property 1: Form Validation Correctness - Incomplete profiles should be rejected.
    
    For any student profile submission, if any required field is missing,
    the submission should be rejected with indication of missing fields.
    
    Validates: Requirements 1.5, 1.6
    """
    is_valid, missing_fields = profile.validate()
    
    assert not is_valid, "Incomplete profile was accepted"
    assert len(missing_fields) > 0, "Incomplete profile did not report missing fields"
    
    # Verify that the missing fields list contains actual missing fields
    for field in missing_fields:
        assert field in [
            "name", "age", "education_level", "degree", "field_of_study",
            "year_of_study", "institution_type", "background_indicators",
            "opportunity_goals", "missed_opportunities_before"
        ], f"Invalid field name in missing fields: {field}"
