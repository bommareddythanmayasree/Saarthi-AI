"""Unit tests for ExplanationGenerator component."""
import pytest
from hypothesis import given, strategies as st
from saarthi_ai.explanation_generator import ExplanationGenerator
from saarthi_ai.models import (
    StudentProfile,
    EducationLevel,
    InstitutionType,
    BackgroundIndicator,
    OpportunityGoal,
    MissedOpportunityFrequency
)
from saarthi_ai.knowledge_base import get_all_opportunities


@pytest.fixture
def generator():
    """Create an ExplanationGenerator instance."""
    return ExplanationGenerator()


def test_generate_profile_summary_basic(generator):
    """Test profile summary generation with basic profile."""
    profile = StudentProfile(
        name="Priya Sharma",
        age=20,
        education_level=EducationLevel.UG,
        degree="B.Tech",
        field_of_study="Computer Science",
        year_of_study=2,
        institution_type=InstitutionType.GOVERNMENT,
        background_indicators=[BackgroundIndicator.RURAL],
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES
    )
    
    summary = generator.generate_profile_summary(profile)
    
    # Verify summary contains student name
    assert "Priya Sharma" in summary
    
    # Verify summary contains education level
    assert "UG" in summary
    
    # Verify summary contains degree and field
    assert "B.Tech" in summary
    assert "Computer Science" in summary
    
    # Verify summary contains institution type
    assert "Government" in summary
    
    # Verify summary contains background indicators
    assert "Rural" in summary
    
    # Verify summary contains opportunity goals
    assert "Scholarships" in summary
    
    # Verify summary does NOT contain opportunity names
    assert "Central Sector" not in summary
    assert "AICTE" not in summary
    assert "NPTEL" not in summary


def test_generate_profile_summary_multiple_backgrounds(generator):
    """Test profile summary with multiple background indicators."""
    profile = StudentProfile(
        name="Rahul Kumar",
        age=22,
        education_level=EducationLevel.PG,
        degree="M.Sc",
        field_of_study="Physics",
        year_of_study=1,
        institution_type=InstitutionType.AUTONOMOUS,
        background_indicators=[
            BackgroundIndicator.RURAL,
            BackgroundIndicator.FIRST_GENERATION,
            BackgroundIndicator.FINANCIAL_SUPPORT
        ],
        opportunity_goals=[OpportunityGoal.RESEARCH, OpportunityGoal.SCHOLARSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.ONCE_OR_TWICE
    )
    
    summary = generator.generate_profile_summary(profile)
    
    # Verify all background indicators are present
    assert "Rural" in summary
    assert "First-generation" in summary
    assert "Financial support" in summary


def test_generate_profile_summary_multiple_goals(generator):
    """Test profile summary with multiple opportunity goals."""
    profile = StudentProfile(
        name="Anjali Patel",
        age=21,
        education_level=EducationLevel.UG,
        degree="B.E",
        field_of_study="Mechanical Engineering",
        year_of_study=3,
        institution_type=InstitutionType.PRIVATE,
        background_indicators=[BackgroundIndicator.MINORITY],
        opportunity_goals=[
            OpportunityGoal.SCHOLARSHIPS,
            OpportunityGoal.INTERNSHIPS,
            OpportunityGoal.SKILLS
        ],
        missed_opportunities_before=MissedOpportunityFrequency.NO
    )
    
    summary = generator.generate_profile_summary(profile)
    
    # Verify all goals are present
    assert "Scholarships" in summary
    assert "Internships" in summary
    assert "Skills" in summary


def test_generate_profile_summary_format(generator):
    """Test that profile summary has correct format with bullet points."""
    profile = StudentProfile(
        name="Test Student",
        age=19,
        education_level=EducationLevel.DIPLOMA,
        degree="Diploma",
        field_of_study="Electronics",
        year_of_study=2,
        institution_type=InstitutionType.GOVERNMENT,
        background_indicators=[BackgroundIndicator.RURAL],
        opportunity_goals=[OpportunityGoal.SKILLS],
        missed_opportunities_before=MissedOpportunityFrequency.NO
    )
    
    summary = generator.generate_profile_summary(profile)
    
    # Verify greeting format
    assert summary.startswith("Hi Test Student!")
    
    # Verify bullet points are present
    assert "•" in summary
    
    # Count bullet points (should have at least 4: education, degree/field, institution, goals)
    bullet_count = summary.count("•")
    assert bullet_count >= 4


def test_generate_profile_summary_no_opportunity_names(generator):
    """Test that profile summary does not contain specific opportunity names."""
    profile = StudentProfile(
        name="Student Name",
        age=20,
        education_level=EducationLevel.UG,
        degree="B.Tech",
        field_of_study="Engineering",
        year_of_study=2,
        institution_type=InstitutionType.GOVERNMENT,
        background_indicators=[BackgroundIndicator.DISABLED],
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES
    )
    
    summary = generator.generate_profile_summary(profile)
    
    # Verify no specific opportunity names are present
    opportunity_keywords = [
        "Central Sector",
        "AICTE",
        "Pragati",
        "Saksham",
        "NPTEL",
        "State Government",
        "Ministry of Education",
        "Innovation"
    ]
    
    for keyword in opportunity_keywords:
        assert keyword not in summary


# Property-Based Tests

# Feature: saarthi-ai-opportunity-finder, Property 2: Profile Summary Completeness
# Validates: Requirements 2.1, 2.2, 2.3
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
    additional_context=st.one_of(st.none(), st.text(min_size=0, max_size=200))
)
def test_property_profile_summary_completeness(
    name, age, education_level, degree, field_of_study, year_of_study,
    institution_type, background_indicators, opportunity_goals,
    missed_opportunities_before, gender, additional_context
):
    """
    Property 2: Profile Summary Completeness
    
    For any valid student profile, the generated profile summary should:
    1. Contain the student's name
    2. Contain education level
    3. Contain field of study
    4. Contain institution type
    5. Contain background indicators (if present)
    6. Contain opportunity goals
    7. NOT contain any specific opportunity names
    
    Validates: Requirements 2.1, 2.2, 2.3
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
    
    # Act
    summary = generator.generate_profile_summary(profile)
    
    # Assert - Requirement 2.1: Summary addresses student by name
    assert profile.name in summary, f"Summary should contain student name '{profile.name}'"
    
    # Assert - Requirement 2.2: Summary includes education level
    assert profile.education_level.value in summary, \
        f"Summary should contain education level '{profile.education_level.value}'"
    
    # Assert - Requirement 2.2: Summary includes field of study
    assert profile.field_of_study in summary, \
        f"Summary should contain field of study '{profile.field_of_study}'"
    
    # Assert - Requirement 2.2: Summary includes institution type
    assert profile.institution_type.value in summary, \
        f"Summary should contain institution type '{profile.institution_type.value}'"
    
    # Assert - Requirement 2.2: Summary includes background indicators
    for indicator in profile.background_indicators:
        assert indicator.value in summary, \
            f"Summary should contain background indicator '{indicator.value}'"
    
    # Assert - Requirement 2.2: Summary includes opportunity goals
    for goal in profile.opportunity_goals:
        assert goal.value in summary, \
            f"Summary should contain opportunity goal '{goal.value}'"
    
    # Assert - Requirement 2.3: Summary does NOT contain specific opportunity names
    # Get all opportunity names from knowledge base
    opportunities = get_all_opportunities()
    
    # Check for specific opportunity identifiers that should NOT appear
    # These are distinctive parts of opportunity names that wouldn't naturally
    # appear in a profile summary
    forbidden_keywords = [
        "Central Sector",
        "AICTE",
        "Pragati",
        "Saksham",
        "NPTEL",
        "State Government Merit",
        "Ministry of Education Innovation"
    ]
    
    for keyword in forbidden_keywords:
        assert keyword not in summary, \
            f"Summary should NOT contain opportunity identifier '{keyword}'"


# Unit tests for generate_final_insight

def test_generate_final_insight_scholarship_focus(generator):
    """Test final insight generation for scholarship-focused blindspots."""
    from saarthi_ai.models import Blindspot, OpportunityMatch, Opportunity, EligibilityCriteria, VisibilityLevel, ImpactLevel, MissProbability
    
    profile = StudentProfile(
        name="Priya Sharma",
        age=20,
        education_level=EducationLevel.UG,
        degree="B.Tech",
        field_of_study="Computer Science",
        year_of_study=2,
        institution_type=InstitutionType.GOVERNMENT,
        background_indicators=[BackgroundIndicator.RURAL, BackgroundIndicator.FINANCIAL_SUPPORT],
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES
    )
    
    blindspots = [
        Blindspot(
            category="Income-based Central Scholarships",
            reason="Many students don't know about central government scholarships",
            relevance_score=0.9
        ),
        Blindspot(
            category="State Government Merit Scholarships",
            reason="State scholarships have poor visibility",
            relevance_score=0.7
        )
    ]
    
    # Create a mock opportunity
    opportunity = Opportunity(
        id="central-sector",
        name="Central Sector Scholarship",
        description="Income-based scholarship",
        eligibility_criteria=EligibilityCriteria(education_levels=[EducationLevel.UG]),
        visibility_level=VisibilityLevel.MEDIUM,
        impact_level=ImpactLevel.HIGH,
        category="Scholarship"
    )
    
    matches = [
        OpportunityMatch(
            opportunity=opportunity,
            fit_explanation="Matches your profile",
            miss_reason="Low visibility",
            miss_probability=MissProbability.HIGH,
            relevance_score=0.9
        )
    ]
    
    insight = generator.generate_final_insight(profile, blindspots, matches)
    
    # Verify insight contains scholarship mention
    assert "scholarship" in insight.lower()
    
    # Verify insight emphasizes awareness (Requirement 6.3)
    awareness_keywords = ["awareness", "knowing", "know", "miss", "missing", "exist"]
    assert any(keyword in insight.lower() for keyword in awareness_keywords)
    
    # Verify insight is 3-4 sentences
    sentence_count = insight.count(". ")
    assert 3 <= sentence_count <= 4, f"Expected 3-4 sentences, got {sentence_count}"
    
    # Verify tailored suggestion for YES_MANY_TIMES (Requirement 6.4)
    assert "alerts" in insight.lower() or "exploring" in insight.lower()


def test_generate_final_insight_research_focus(generator):
    """Test final insight generation for research-focused blindspots."""
    from saarthi_ai.models import Blindspot, OpportunityMatch, Opportunity, EligibilityCriteria, VisibilityLevel, ImpactLevel, MissProbability
    
    profile = StudentProfile(
        name="Rahul Kumar",
        age=22,
        education_level=EducationLevel.PG,
        degree="M.Sc",
        field_of_study="Physics",
        year_of_study=1,
        institution_type=InstitutionType.AUTONOMOUS,
        background_indicators=[BackgroundIndicator.RURAL],
        opportunity_goals=[OpportunityGoal.RESEARCH],
        missed_opportunities_before=MissedOpportunityFrequency.ONCE_OR_TWICE
    )
    
    blindspots = [
        Blindspot(
            category="Research Internships and Programs",
            reason="STEM students often focus on placements",
            relevance_score=0.8
        )
    ]
    
    opportunity = Opportunity(
        id="nptel",
        name="NPTEL Research Internship",
        description="Research opportunity",
        eligibility_criteria=EligibilityCriteria(education_levels=[EducationLevel.PG]),
        visibility_level=VisibilityLevel.MEDIUM,
        impact_level=ImpactLevel.MEDIUM,
        category="Research"
    )
    
    matches = [
        OpportunityMatch(
            opportunity=opportunity,
            fit_explanation="Matches your profile",
            miss_reason="Low visibility",
            miss_probability=MissProbability.MEDIUM,
            relevance_score=0.8
        )
    ]
    
    insight = generator.generate_final_insight(profile, blindspots, matches)
    
    # Verify insight mentions research/internships
    assert "research" in insight.lower() or "internship" in insight.lower()
    
    # Verify insight emphasizes awareness
    awareness_keywords = ["awareness", "knowing", "know", "miss", "missing", "exist"]
    assert any(keyword in insight.lower() for keyword in awareness_keywords)
    
    # Verify tailored suggestion for ONCE_OR_TWICE
    assert "explore" in insight.lower() or "eligible" in insight.lower()


def test_generate_final_insight_never_missed(generator):
    """Test final insight generation for student who never missed opportunities."""
    from saarthi_ai.models import Blindspot, OpportunityMatch, Opportunity, EligibilityCriteria, VisibilityLevel, ImpactLevel, MissProbability
    
    profile = StudentProfile(
        name="Anjali Patel",
        age=21,
        education_level=EducationLevel.UG,
        degree="B.E",
        field_of_study="Mechanical Engineering",
        year_of_study=3,
        institution_type=InstitutionType.PRIVATE,
        background_indicators=[BackgroundIndicator.MINORITY],
        opportunity_goals=[OpportunityGoal.SKILLS],
        missed_opportunities_before=MissedOpportunityFrequency.NO
    )
    
    blindspots = [
        Blindspot(
            category="Ministry Innovation Programs",
            reason="Innovation programs are buried in government websites",
            relevance_score=0.6
        )
    ]
    
    opportunity = Opportunity(
        id="innovation",
        name="Ministry Innovation Program",
        description="Innovation program",
        eligibility_criteria=EligibilityCriteria(education_levels=[EducationLevel.UG]),
        visibility_level=VisibilityLevel.LOW,
        impact_level=ImpactLevel.MEDIUM,
        category="Program"
    )
    
    matches = [
        OpportunityMatch(
            opportunity=opportunity,
            fit_explanation="Matches your profile",
            miss_reason="Low visibility",
            miss_probability=MissProbability.HIGH,
            relevance_score=0.7
        )
    ]
    
    insight = generator.generate_final_insight(profile, blindspots, matches)
    
    # Verify insight emphasizes awareness
    awareness_keywords = ["awareness", "knowing", "know", "miss", "missing", "exist"]
    assert any(keyword in insight.lower() for keyword in awareness_keywords)
    
    # Verify tailored suggestion for NO (never missed)
    assert "aware" in insight.lower() or "action" in insight.lower() or "qualified" in insight.lower()
    
    # Verify positive tone
    assert "Awareness is the first step to opportunity" in insight


def test_generate_final_insight_sentence_count(generator):
    """Test that final insight has 3-4 sentences."""
    from saarthi_ai.models import Blindspot, OpportunityMatch, Opportunity, EligibilityCriteria, VisibilityLevel, ImpactLevel, MissProbability
    
    profile = StudentProfile(
        name="Test Student",
        age=20,
        education_level=EducationLevel.UG,
        degree="B.Tech",
        field_of_study="Engineering",
        year_of_study=2,
        institution_type=InstitutionType.GOVERNMENT,
        background_indicators=[BackgroundIndicator.RURAL],
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES
    )
    
    blindspots = [
        Blindspot(category="Test Category", reason="Test reason", relevance_score=0.8)
    ]
    
    opportunity = Opportunity(
        id="test",
        name="Test Opportunity",
        description="Test",
        eligibility_criteria=EligibilityCriteria(education_levels=[EducationLevel.UG]),
        visibility_level=VisibilityLevel.LOW,
        impact_level=ImpactLevel.HIGH,
        category="Test"
    )
    
    matches = [
        OpportunityMatch(
            opportunity=opportunity,
            fit_explanation="Test",
            miss_reason="Test",
            miss_probability=MissProbability.HIGH,
            relevance_score=0.8
        )
    ]
    
    insight = generator.generate_final_insight(profile, blindspots, matches)
    
    # Count sentences (periods followed by space or end of string)
    sentence_count = insight.count(". ")
    assert 3 <= sentence_count <= 4, f"Expected 3-4 sentences, got {sentence_count}"


def test_generate_final_insight_positive_tone(generator):
    """Test that final insight has positive and encouraging tone."""
    from saarthi_ai.models import Blindspot, OpportunityMatch, Opportunity, EligibilityCriteria, VisibilityLevel, ImpactLevel, MissProbability
    
    profile = StudentProfile(
        name="Student",
        age=20,
        education_level=EducationLevel.UG,
        degree="B.Tech",
        field_of_study="Engineering",
        year_of_study=2,
        institution_type=InstitutionType.GOVERNMENT,
        background_indicators=[BackgroundIndicator.RURAL],
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.ONCE_OR_TWICE
    )
    
    blindspots = [
        Blindspot(category="Scholarships", reason="Test", relevance_score=0.8)
    ]
    
    opportunity = Opportunity(
        id="test",
        name="Test",
        description="Test",
        eligibility_criteria=EligibilityCriteria(education_levels=[EducationLevel.UG]),
        visibility_level=VisibilityLevel.LOW,
        impact_level=ImpactLevel.HIGH,
        category="Scholarship"
    )
    
    matches = [
        OpportunityMatch(
            opportunity=opportunity,
            fit_explanation="Test",
            miss_reason="Test",
            miss_probability=MissProbability.HIGH,
            relevance_score=0.8
        )
    ]
    
    insight = generator.generate_final_insight(profile, blindspots, matches)
    
    # Verify positive/encouraging words are present
    positive_keywords = ["eligible", "qualified", "opportunity", "awareness", "explore", "action"]
    assert any(keyword in insight.lower() for keyword in positive_keywords)
    
    # Verify no negative/discouraging language
    negative_keywords = ["can't", "cannot", "won't", "unable", "impossible", "difficult"]
    assert not any(keyword in insight.lower() for keyword in negative_keywords)
