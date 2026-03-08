"""
Property-based tests for blindspot output structure.

Feature: saarthi-ai-opportunity-finder
Property 3: Blindspot Output Structure
Validates: Requirements 3.1, 3.2, 3.4
"""
import pytest
from hypothesis import given, strategies as st
from saarthi_ai.models import (
    StudentProfile,
    ProfileAnalysis,
    EducationLevel,
    InstitutionType,
    BackgroundIndicator,
    OpportunityGoal,
    MissedOpportunityFrequency,
    AwarenessLevel,
)
from saarthi_ai.blindspot_identifier import BlindspotIdentifier
from saarthi_ai.profile_analyzer import ProfileAnalyzer


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


# List of specific opportunity names that should NOT appear in blindspot output
OPPORTUNITY_NAMES = [
    "Central Sector Scholarship",
    "AICTE Pragati",
    "AICTE Saksham",
    "NPTEL Research Internship",
    "State Government Merit Scholarships",
    "Ministry of Education Innovation Programs",
]


@given(valid_profile_strategy())
def test_property_blindspot_count(profile):
    """
    Property 3: Blindspot Output Structure - Count validation.
    
    For any valid student profile, the blindspot analysis should identify
    between 3 and 5 blindspot categories.
    
    Validates: Requirements 3.1
    """
    # Create analyzer and identifier
    analyzer = ProfileAnalyzer()
    identifier = BlindspotIdentifier()
    
    # Analyze profile and identify blindspots
    analysis = analyzer.analyze(profile)
    blindspots = identifier.identify_blindspots(profile, analysis)
    
    # Verify count is between 3 and 5
    assert 3 <= len(blindspots) <= 5, \
        f"Expected 3-5 blindspots, got {len(blindspots)}"


@given(valid_profile_strategy())
def test_property_blindspot_explanation_completeness(profile):
    """
    Property 3: Blindspot Output Structure - Explanation completeness.
    
    For any valid student profile, each blindspot should have a non-empty
    explanation (reason field).
    
    Validates: Requirements 3.2
    """
    # Create analyzer and identifier
    analyzer = ProfileAnalyzer()
    identifier = BlindspotIdentifier()
    
    # Analyze profile and identify blindspots
    analysis = analyzer.analyze(profile)
    blindspots = identifier.identify_blindspots(profile, analysis)
    
    # Verify each blindspot has a non-empty explanation
    for i, blindspot in enumerate(blindspots):
        assert blindspot.reason, \
            f"Blindspot {i} has empty reason"
        assert blindspot.reason.strip(), \
            f"Blindspot {i} has whitespace-only reason"
        assert len(blindspot.reason) > 0, \
            f"Blindspot {i} has zero-length reason"


@given(valid_profile_strategy())
def test_property_blindspot_no_opportunity_names(profile):
    """
    Property 3: Blindspot Output Structure - No specific opportunity names.
    
    For any valid student profile, the blindspot output should not contain
    specific opportunity names from the knowledge base.
    
    Validates: Requirements 3.4
    """
    # Create analyzer and identifier
    analyzer = ProfileAnalyzer()
    identifier = BlindspotIdentifier()
    
    # Analyze profile and identify blindspots
    analysis = analyzer.analyze(profile)
    blindspots = identifier.identify_blindspots(profile, analysis)
    
    # Check each blindspot for opportunity names
    for i, blindspot in enumerate(blindspots):
        # Check category field
        category_lower = blindspot.category.lower()
        for opp_name in OPPORTUNITY_NAMES:
            # Allow partial matches like "NPTEL" in the reason, but not full names
            assert opp_name.lower() not in category_lower, \
                f"Blindspot {i} category contains opportunity name '{opp_name}': {blindspot.category}"
        
        # Check reason field - allow mentions like "NPTEL" but not full opportunity names
        reason_lower = blindspot.reason.lower()
        # Only check for exact full names, not partial matches
        for opp_name in OPPORTUNITY_NAMES:
            # Skip checking for partial acronyms like "NPTEL" or "AICTE" 
            # since they can be used generically
            if opp_name in ["AICTE Pragati", "AICTE Saksham", 
                           "Central Sector Scholarship", 
                           "State Government Merit Scholarships",
                           "Ministry of Education Innovation Programs"]:
                assert opp_name.lower() not in reason_lower, \
                    f"Blindspot {i} reason contains full opportunity name '{opp_name}': {blindspot.reason}"


@given(valid_profile_strategy())
def test_property_blindspot_structure_complete(profile):
    """
    Property 3: Blindspot Output Structure - Complete structure validation.
    
    For any valid student profile, verify all structural requirements:
    - 3-5 blindspots returned
    - Each has non-empty category
    - Each has non-empty explanation
    - No specific opportunity names present
    
    Validates: Requirements 3.1, 3.2, 3.4
    """
    # Create analyzer and identifier
    analyzer = ProfileAnalyzer()
    identifier = BlindspotIdentifier()
    
    # Analyze profile and identify blindspots
    analysis = analyzer.analyze(profile)
    blindspots = identifier.identify_blindspots(profile, analysis)
    
    # Verify count
    assert 3 <= len(blindspots) <= 5, \
        f"Expected 3-5 blindspots, got {len(blindspots)}"
    
    # Verify each blindspot structure
    for i, blindspot in enumerate(blindspots):
        # Check category is non-empty
        assert blindspot.category, \
            f"Blindspot {i} has empty category"
        assert blindspot.category.strip(), \
            f"Blindspot {i} has whitespace-only category"
        
        # Check reason is non-empty
        assert blindspot.reason, \
            f"Blindspot {i} has empty reason"
        assert blindspot.reason.strip(), \
            f"Blindspot {i} has whitespace-only reason"
        
        # Check relevance score is present and valid
        assert blindspot.relevance_score is not None, \
            f"Blindspot {i} has no relevance score"
        assert 0.0 <= blindspot.relevance_score <= 1.0, \
            f"Blindspot {i} has invalid relevance score: {blindspot.relevance_score}"
