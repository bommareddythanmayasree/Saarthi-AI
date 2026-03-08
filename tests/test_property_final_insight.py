"""Property-based tests for final insight completeness."""
import pytest
from hypothesis import given, strategies as st, assume, settings
from saarthi_ai.explanation_generator import ExplanationGenerator
from saarthi_ai.models import (
    StudentProfile,
    EducationLevel,
    InstitutionType,
    BackgroundIndicator,
    OpportunityGoal,
    MissedOpportunityFrequency,
    Blindspot,
    OpportunityMatch,
    Opportunity,
    EligibilityCriteria,
    VisibilityLevel,
    ImpactLevel,
    MissProbability
)


# Feature: saarthi-ai-opportunity-finder, Property 7: Final Insight Completeness
# Validates: Requirements 6.1, 6.2, 6.3
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
    age=st.integers(min_value=16, max_value=40),
    education_level=st.sampled_from(EducationLevel),
    degree=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
    field_of_study=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
    year_of_study=st.integers(min_value=1, max_value=6),
    institution_type=st.sampled_from(InstitutionType),
    background_indicators=st.lists(
        st.sampled_from(BackgroundIndicator),
        min_size=1,
        max_size=5,
        unique=True
    ),
    opportunity_goals=st.lists(
        st.sampled_from(OpportunityGoal),
        min_size=1,
        max_size=5,
        unique=True
    ),
    missed_opportunities_before=st.sampled_from(MissedOpportunityFrequency),
    gender=st.one_of(st.none(), st.text(min_size=1, max_size=20)),
    additional_context=st.one_of(st.none(), st.text(min_size=0, max_size=200)),
    num_blindspots=st.integers(min_value=1, max_value=5),
    num_matches=st.integers(min_value=1, max_value=3)
)
@settings(max_examples=100)
def test_property_final_insight_completeness(
    name, age, education_level, degree, field_of_study, year_of_study,
    institution_type, background_indicators, opportunity_goals,
    missed_opportunities_before, gender, additional_context,
    num_blindspots, num_matches
):
    """
    Property 7: Final Insight Completeness
    
    For any valid student profile, the final insight should:
    1. Be generated (not empty)
    2. Contain between 3 and 4 sentences
    3. Contain keywords related to awareness (e.g., "awareness", "knowing", "know", "miss", "missing")
    
    Validates: Requirements 6.1, 6.2, 6.3
    """
    # Arrange
    generator = ExplanationGenerator()
    
    profile = StudentProfile(
        name=name,
        age=age,
        education_level=education_level,
        degree=degree,
        field_of_study=field_of_study,
        year_of_study=year_of_study,
        institution_type=institution_type,
        background_indicators=background_indicators,
        opportunity_goals=opportunity_goals,
        missed_opportunities_before=missed_opportunities_before,
        gender=gender,
        additional_context=additional_context
    )
    
    # Generate random blindspots
    blindspot_categories = [
        "Income-based Central Scholarships",
        "Research Internships and Programs",
        "State Government Merit Scholarships",
        "Category-specific Technical Scholarships",
        "Ministry Innovation Programs"
    ]
    
    blindspots = [
        Blindspot(
            category=blindspot_categories[i % len(blindspot_categories)],
            reason=f"Test reason {i}",
            relevance_score=0.5 + (i * 0.1)
        )
        for i in range(num_blindspots)
    ]
    
    # Generate random opportunity matches
    matches = []
    for i in range(num_matches):
        opportunity = Opportunity(
            id=f"opp-{i}",
            name=f"Test Opportunity {i}",
            description=f"Test description {i}",
            eligibility_criteria=EligibilityCriteria(
                education_levels=[education_level]
            ),
            visibility_level=VisibilityLevel.LOW,
            impact_level=ImpactLevel.HIGH,
            category="Test"
        )
        
        match = OpportunityMatch(
            opportunity=opportunity,
            fit_explanation=f"Test fit explanation {i}",
            miss_reason=f"Test miss reason {i}",
            miss_probability=MissProbability.HIGH,
            relevance_score=0.8
        )
        matches.append(match)
    
    # Act
    insight = generator.generate_final_insight(profile, blindspots, matches)
    
    # Assert - Requirement 6.1: Final insight should be generated
    assert insight is not None, "Final insight should be generated"
    assert len(insight.strip()) > 0, "Final insight should not be empty"
    
    # Assert - Requirement 6.2: Final insight should contain 3-4 sentences
    # Count sentences by counting periods (each sentence ends with a period)
    sentence_count = insight.count(".")
    assert 3 <= sentence_count <= 4, \
        f"Final insight should contain 3-4 sentences, got {sentence_count}"
    
    # Assert - Requirement 6.3: Final insight should contain awareness keywords
    awareness_keywords = ["awareness", "knowing", "know", "miss", "missing", "exist"]
    insight_lower = insight.lower()
    
    has_awareness_keyword = any(keyword in insight_lower for keyword in awareness_keywords)
    assert has_awareness_keyword, \
        f"Final insight should contain at least one awareness keyword from {awareness_keywords}"
