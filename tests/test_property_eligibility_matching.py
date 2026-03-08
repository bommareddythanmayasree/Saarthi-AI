"""
Property-based tests for eligibility matching correctness.

Feature: saarthi-ai-opportunity-finder
Property 5: Eligibility Matching Correctness
Validates: Requirements 4.5, 5.3
"""
import pytest
from hypothesis import given, strategies as st, assume, settings
from saarthi_ai.opportunity_matcher import OpportunityMatcher
from saarthi_ai.profile_analyzer import ProfileAnalyzer
from saarthi_ai.blindspot_identifier import BlindspotIdentifier
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
        age=draw(st.integers(min_value=16, max_value=40)),
        education_level=draw(education_level_strategy),
        degree=draw(st.text(min_size=1, max_size=50).filter(lambda x: x.strip())),
        field_of_study=draw(st.text(min_size=1, max_size=50).filter(lambda x: x.strip())),
        year_of_study=draw(st.integers(min_value=1, max_value=6)),
        institution_type=draw(institution_type_strategy),
        background_indicators=draw(background_indicator_strategy),
        opportunity_goals=draw(opportunity_goal_strategy),
        missed_opportunities_before=draw(missed_opportunity_strategy),
        gender=draw(st.one_of(st.none(), st.sampled_from(["Male", "Female", "Other"]))),
        additional_context=draw(st.one_of(st.none(), st.text(max_size=200))),
    )


@given(valid_profile_strategy())
@settings(max_examples=100)
def test_property_all_recommendations_meet_eligibility(profile):
    """
    Property 5: Eligibility Matching Correctness.
    
    For any student profile and any recommended opportunity, the student must meet
    all eligibility criteria defined for that opportunity (education level, field of
    study if specified, institution type if specified, and background requirements
    if specified).
    
    **Validates: Requirements 4.5, 5.3**
    """
    # Create components
    matcher = OpportunityMatcher()
    analyzer = ProfileAnalyzer()
    blindspot_identifier = BlindspotIdentifier()
    
    # Analyze profile and identify blindspots
    analysis = analyzer.analyze(profile)
    blindspots = blindspot_identifier.identify_blindspots(profile, analysis)
    
    # Get opportunity matches
    matches = matcher.match_opportunities(profile, analysis, blindspots)
    
    # Verify each match meets eligibility criteria
    for match in matches:
        opportunity = match.opportunity
        criteria = opportunity.eligibility_criteria
        
        # Check education level
        assert profile.education_level in criteria.education_levels, \
            f"Profile education level {profile.education_level} not in eligible levels {criteria.education_levels} for {opportunity.name}"
        
        # Check field of study (if specified)
        if criteria.fields_of_study is not None:
            assert profile.field_of_study in criteria.fields_of_study, \
                f"Profile field {profile.field_of_study} not in eligible fields {criteria.fields_of_study} for {opportunity.name}"
        
        # Check institution type (if specified)
        if criteria.institution_types is not None:
            assert profile.institution_type in criteria.institution_types, \
                f"Profile institution type {profile.institution_type} not in eligible types {criteria.institution_types} for {opportunity.name}"
        
        # Check background requirements (if specified)
        if criteria.background_requirements is not None:
            has_required_background = any(
                req in profile.background_indicators
                for req in criteria.background_requirements
            )
            assert has_required_background, \
                f"Profile backgrounds {profile.background_indicators} don't meet requirements {criteria.background_requirements} for {opportunity.name}"


@given(valid_profile_strategy())
@settings(max_examples=100)
def test_property_is_eligible_consistency(profile):
    """
    Property: is_eligible method is consistent with match_opportunities filtering.
    
    Any opportunity returned by match_opportunities must pass the is_eligible check.
    
    **Validates: Requirements 4.5, 5.3**
    """
    # Create components
    matcher = OpportunityMatcher()
    analyzer = ProfileAnalyzer()
    blindspot_identifier = BlindspotIdentifier()
    
    # Analyze profile and identify blindspots
    analysis = analyzer.analyze(profile)
    blindspots = blindspot_identifier.identify_blindspots(profile, analysis)
    
    # Get opportunity matches
    matches = matcher.match_opportunities(profile, analysis, blindspots)
    
    # Verify each match passes is_eligible check
    for match in matches:
        assert matcher.is_eligible(profile, match.opportunity.eligibility_criteria), \
            f"Opportunity {match.opportunity.name} was recommended but fails is_eligible check"
