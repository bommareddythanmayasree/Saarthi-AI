"""
Property-based tests for recommendation structure completeness.

Feature: saarthi-ai-opportunity-finder
Property 4: Recommendation Structure Completeness
Validates: Requirements 4.1, 4.2, 4.3, 4.4
"""
import pytest
from hypothesis import given, strategies as st
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
    MissProbability,
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
def test_property_recommendation_count(profile):
    """
    Property 4: Recommendation Structure Completeness - Count.
    
    For any valid student profile, the opportunity recommendations should include
    between 2 and 3 opportunities.
    
    Validates: Requirements 4.1
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
    
    # Verify count is between 2 and 3
    assert len(matches) >= 2, f"Expected at least 2 recommendations, got {len(matches)}"
    assert len(matches) <= 3, f"Expected at most 3 recommendations, got {len(matches)}"


@given(valid_profile_strategy())
def test_property_recommendation_has_fit_explanation(profile):
    """
    Property 4: Recommendation Structure Completeness - Fit Explanation.
    
    For any valid student profile, each recommendation should have a non-empty
    fit explanation.
    
    Validates: Requirements 4.2
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
    
    # Verify each match has a non-empty fit explanation
    for match in matches:
        assert match.fit_explanation is not None, \
            f"Fit explanation is None for {match.opportunity.name}"
        assert len(match.fit_explanation.strip()) > 0, \
            f"Fit explanation is empty for {match.opportunity.name}"


@given(valid_profile_strategy())
def test_property_recommendation_has_miss_reason(profile):
    """
    Property 4: Recommendation Structure Completeness - Miss Reason.
    
    For any valid student profile, each recommendation should have a non-empty
    miss reason.
    
    Validates: Requirements 4.3
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
    
    # Verify each match has a non-empty miss reason
    for match in matches:
        assert match.miss_reason is not None, \
            f"Miss reason is None for {match.opportunity.name}"
        assert len(match.miss_reason.strip()) > 0, \
            f"Miss reason is empty for {match.opportunity.name}"


@given(valid_profile_strategy())
def test_property_recommendation_has_valid_miss_probability(profile):
    """
    Property 4: Recommendation Structure Completeness - Miss Probability.
    
    For any valid student profile, each recommendation should have a miss probability
    rating of High, Medium, or Low.
    
    Validates: Requirements 4.4
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
    
    # Verify each match has a valid miss probability
    valid_probabilities = [MissProbability.HIGH, MissProbability.MEDIUM, MissProbability.LOW]
    for match in matches:
        assert match.miss_probability in valid_probabilities, \
            f"Invalid miss probability {match.miss_probability} for {match.opportunity.name}"


@given(valid_profile_strategy())
def test_property_recommendation_complete_structure(profile):
    """
    Property 4: Recommendation Structure Completeness - Complete.
    
    For any valid student profile, the opportunity recommendations should include
    between 2 and 3 opportunities, and each recommendation should have a non-empty
    fit explanation, a non-empty miss reason, and a valid miss probability rating.
    
    Validates: Requirements 4.1, 4.2, 4.3, 4.4
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
    
    # Verify count
    assert len(matches) >= 2, f"Expected at least 2 recommendations, got {len(matches)}"
    assert len(matches) <= 3, f"Expected at most 3 recommendations, got {len(matches)}"
    
    # Verify structure of each match
    valid_probabilities = [MissProbability.HIGH, MissProbability.MEDIUM, MissProbability.LOW]
    for match in matches:
        # Check fit explanation
        assert match.fit_explanation is not None, \
            f"Fit explanation is None for {match.opportunity.name}"
        assert len(match.fit_explanation.strip()) > 0, \
            f"Fit explanation is empty for {match.opportunity.name}"
        
        # Check miss reason
        assert match.miss_reason is not None, \
            f"Miss reason is None for {match.opportunity.name}"
        assert len(match.miss_reason.strip()) > 0, \
            f"Miss reason is empty for {match.opportunity.name}"
        
        # Check miss probability
        assert match.miss_probability in valid_probabilities, \
            f"Invalid miss probability {match.miss_probability} for {match.opportunity.name}"
