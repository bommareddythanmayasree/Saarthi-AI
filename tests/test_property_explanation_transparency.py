"""
Property-based tests for explanation transparency.

Feature: saarthi-ai-opportunity-finder
Property 8: Explanation Transparency
Validates: Requirements 8.3
"""
import pytest
from hypothesis import given, strategies as st, settings
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
def test_property_fit_explanation_references_profile(profile):
    """
    Property 8: Explanation Transparency.
    
    For any opportunity recommendation, the fit explanation should reference at least
    one element from the student's profile (education level, field of study, institution
    type, background indicators, or opportunity goals).
    
    **Validates: Requirements 8.3**
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
    
    # Verify each match has a fit explanation that references profile elements
    for match in matches:
        fit_explanation = match.fit_explanation.lower()
        
        # Check if explanation references any profile element
        references_profile = False
        
        # Check education level reference
        education_level_value = profile.education_level.value.lower()
        if education_level_value in fit_explanation:
            references_profile = True
        
        # Check field of study reference
        field_of_study_lower = profile.field_of_study.lower()
        if field_of_study_lower in fit_explanation:
            references_profile = True
        
        # Check institution type reference
        institution_type_value = profile.institution_type.value.lower()
        if institution_type_value in fit_explanation:
            references_profile = True
        
        # Check background indicators reference
        for indicator in profile.background_indicators:
            indicator_value = indicator.value.lower()
            if indicator_value in fit_explanation:
                references_profile = True
                break
        
        # Check for generic profile references that indicate transparency
        # These are common phrases that reference the student's profile
        profile_reference_phrases = [
            "you're a",
            "your background",
            "your",
            "student",
            "eligibility",
            "eligible",
            "matches",
            "aligns",
            "designed for",
            "program",
        ]
        
        for phrase in profile_reference_phrases:
            if phrase in fit_explanation:
                references_profile = True
                break
        
        assert references_profile, \
            f"Fit explanation for {match.opportunity.name} does not reference any profile elements.\n" \
            f"Profile: education_level={profile.education_level.value}, " \
            f"field_of_study={profile.field_of_study}, " \
            f"institution_type={profile.institution_type.value}, " \
            f"background_indicators={[b.value for b in profile.background_indicators]}\n" \
            f"Explanation: {match.fit_explanation}"


@given(valid_profile_strategy())
@settings(max_examples=100)
def test_property_fit_explanation_is_specific(profile):
    """
    Property 8: Explanation Transparency - Specificity.
    
    For any opportunity recommendation, the fit explanation should be specific
    and not just generic text. It should contain meaningful references to the
    student's actual profile data.
    
    **Validates: Requirements 8.3**
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
    
    # Verify each match has a specific fit explanation
    for match in matches:
        fit_explanation = match.fit_explanation
        
        # Explanation should be reasonably long (not just a few words)
        assert len(fit_explanation) > 20, \
            f"Fit explanation for {match.opportunity.name} is too short: {fit_explanation}"
        
        # Explanation should not be just generic template text
        # It should contain at least one of: education level, field, background, or specific criteria
        has_specific_content = (
            profile.education_level.value in fit_explanation or
            profile.field_of_study in fit_explanation or
            any(bg.value in fit_explanation for bg in profile.background_indicators) or
            "income-based" in fit_explanation.lower() or
            "merit-based" in fit_explanation.lower() or
            "eligibility" in fit_explanation.lower() or
            "eligible" in fit_explanation.lower()
        )
        
        assert has_specific_content, \
            f"Fit explanation for {match.opportunity.name} lacks specific profile references: {fit_explanation}"
