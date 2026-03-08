"""Unit tests for BlindspotIdentifier component."""
import pytest
from saarthi_ai.blindspot_identifier import BlindspotIdentifier
from saarthi_ai.profile_analyzer import ProfileAnalyzer
from saarthi_ai.models import (
    StudentProfile,
    EducationLevel,
    InstitutionType,
    BackgroundIndicator,
    OpportunityGoal,
    MissedOpportunityFrequency
)


@pytest.fixture
def identifier():
    """Create a BlindspotIdentifier instance."""
    return BlindspotIdentifier()


@pytest.fixture
def analyzer():
    """Create a ProfileAnalyzer instance."""
    return ProfileAnalyzer()


def test_stem_student_gets_research_blindspot(identifier, analyzer):
    """Test that STEM student receives research blindspot."""
    # Arrange - Create a STEM student profile
    profile = StudentProfile(
        name="Rahul Sharma",
        age=22,
        education_level=EducationLevel.PG,
        degree="M.Sc",
        field_of_study="Physics",
        year_of_study=1,
        institution_type=InstitutionType.AUTONOMOUS,
        background_indicators=[BackgroundIndicator.MINORITY],
        opportunity_goals=[OpportunityGoal.RESEARCH, OpportunityGoal.INTERNSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.ONCE_OR_TWICE
    )
    
    analysis = analyzer.analyze(profile)
    
    # Act
    blindspots = identifier.identify_blindspots(profile, analysis)
    
    # Assert - STEM student should get research blindspot
    research_blindspot_found = any(
        "Research" in blindspot.category 
        for blindspot in blindspots
    )
    assert research_blindspot_found, "STEM student should receive research blindspot"
    
    # Verify the specific research blindspot
    research_blindspot = next(
        (b for b in blindspots if "Research" in b.category),
        None
    )
    assert research_blindspot is not None
    assert "STEM" in research_blindspot.reason or "research" in research_blindspot.reason.lower()


def test_financial_background_gets_scholarship_blindspot(identifier, analyzer):
    """Test that student with financial background receives scholarship blindspot."""
    # Arrange - Create a student with financial support background
    profile = StudentProfile(
        name="Priya Kumar",
        age=19,
        education_level=EducationLevel.UG,
        degree="B.Tech",
        field_of_study="Civil Engineering",
        year_of_study=1,
        institution_type=InstitutionType.GOVERNMENT,
        background_indicators=[
            BackgroundIndicator.RURAL,
            BackgroundIndicator.FIRST_GENERATION,
            BackgroundIndicator.FINANCIAL_SUPPORT
        ],
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES
    )
    
    analysis = analyzer.analyze(profile)
    
    # Act
    blindspots = identifier.identify_blindspots(profile, analysis)
    
    # Assert - Student with financial background should get income-based scholarship blindspot
    scholarship_blindspot_found = any(
        "Income-based" in blindspot.category or "Scholarship" in blindspot.category
        for blindspot in blindspots
    )
    assert scholarship_blindspot_found, "Student with financial background should receive scholarship blindspot"
    
    # Verify the specific income-based scholarship blindspot
    income_scholarship = next(
        (b for b in blindspots if "Income-based" in b.category),
        None
    )
    assert income_scholarship is not None
    assert "scholarship" in income_scholarship.reason.lower()


def test_profile_with_all_goals(identifier, analyzer):
    """Test blindspot identification for profile with all opportunity goals."""
    # Arrange - Create a profile with all goals
    profile = StudentProfile(
        name="Multi Goal Student",
        age=21,
        education_level=EducationLevel.UG,
        degree="B.Tech",
        field_of_study="Computer Science",
        year_of_study=3,
        institution_type=InstitutionType.AUTONOMOUS,
        background_indicators=[BackgroundIndicator.FIRST_GENERATION],
        opportunity_goals=[
            OpportunityGoal.SCHOLARSHIPS,
            OpportunityGoal.INTERNSHIPS,
            OpportunityGoal.RESEARCH,
            OpportunityGoal.SKILLS,
            OpportunityGoal.GOVT_EXAMS
        ],
        missed_opportunities_before=MissedOpportunityFrequency.ONCE_OR_TWICE
    )
    
    analysis = analyzer.analyze(profile)
    
    # Act
    blindspots = identifier.identify_blindspots(profile, analysis)
    
    # Assert - Should return between 3 and 5 blindspots
    assert 3 <= len(blindspots) <= 5, f"Expected 3-5 blindspots, got {len(blindspots)}"
    
    # Assert - Each blindspot should have required fields
    for blindspot in blindspots:
        assert blindspot.category, "Blindspot should have a category"
        assert blindspot.reason, "Blindspot should have a reason"
        assert blindspot.relevance_score > 0, "Blindspot should have positive relevance score"
    
    # Assert - Should include diverse blindspot categories based on goals
    categories = [b.category for b in blindspots]
    
    # With all goals, should get multiple types of blindspots
    # At least research (STEM field), internships, skills, and govt exams related
    assert any("Research" in cat for cat in categories), "Should include research blindspot for STEM student"
    assert any("Internship" in cat or "Skill" in cat or "Exam" in cat for cat in categories), \
        "Should include blindspots related to other goals"


def test_profile_with_minimal_information(identifier, analyzer):
    """Test blindspot identification for profile with minimal information."""
    # Arrange - Create a minimal profile with only required fields
    profile = StudentProfile(
        name="Minimal Student",
        age=20,
        education_level=EducationLevel.UG,
        degree="BA",
        field_of_study="History",
        year_of_study=2,
        institution_type=InstitutionType.PRIVATE,
        background_indicators=[BackgroundIndicator.RURAL],  # Minimal - just one
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],  # Minimal - just one
        missed_opportunities_before=MissedOpportunityFrequency.NO
    )
    
    analysis = analyzer.analyze(profile)
    
    # Act
    blindspots = identifier.identify_blindspots(profile, analysis)
    
    # Assert - Should still return between 3 and 5 blindspots (fallback rules ensure minimum)
    assert 3 <= len(blindspots) <= 5, f"Expected 3-5 blindspots even with minimal info, got {len(blindspots)}"
    
    # Assert - Each blindspot should have required fields
    for blindspot in blindspots:
        assert blindspot.category, "Blindspot should have a category"
        assert blindspot.reason, "Blindspot should have a reason"
        assert blindspot.relevance_score > 0, "Blindspot should have positive relevance score"
    
    # Assert - Blindspots should be sorted by relevance score (descending)
    relevance_scores = [b.relevance_score for b in blindspots]
    assert relevance_scores == sorted(relevance_scores, reverse=True), \
        "Blindspots should be sorted by relevance score in descending order"


def test_female_engineering_student_gets_category_specific_blindspot(identifier, analyzer):
    """Test that female engineering student receives category-specific blindspot."""
    # Arrange - Create a female engineering student profile
    profile = StudentProfile(
        name="Anjali Patel",
        age=20,
        education_level=EducationLevel.UG,
        degree="B.Tech",
        field_of_study="Computer Science",
        year_of_study=3,
        institution_type=InstitutionType.PRIVATE,
        background_indicators=[BackgroundIndicator.FIRST_GENERATION],
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS, OpportunityGoal.SKILLS],
        missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES,
        gender="Female"
    )
    
    analysis = analyzer.analyze(profile)
    
    # Act
    blindspots = identifier.identify_blindspots(profile, analysis)
    
    # Assert - Female student should get category-specific blindspot
    category_specific_found = any(
        "Category-specific" in blindspot.category or "Technical Scholarship" in blindspot.category
        for blindspot in blindspots
    )
    assert category_specific_found, "Female engineering student should receive category-specific blindspot"


def test_disabled_student_gets_category_specific_blindspot(identifier, analyzer):
    """Test that disabled student receives category-specific blindspot."""
    # Arrange - Create a disabled student profile
    profile = StudentProfile(
        name="Vikram Singh",
        age=21,
        education_level=EducationLevel.UG,
        degree="B.E",
        field_of_study="Mechanical Engineering",
        year_of_study=2,
        institution_type=InstitutionType.GOVERNMENT,
        background_indicators=[
            BackgroundIndicator.DISABLED,
            BackgroundIndicator.FINANCIAL_SUPPORT
        ],
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS, OpportunityGoal.INTERNSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES
    )
    
    analysis = analyzer.analyze(profile)
    
    # Act
    blindspots = identifier.identify_blindspots(profile, analysis)
    
    # Assert - Disabled student should get category-specific blindspot
    category_specific_found = any(
        "Category-specific" in blindspot.category
        for blindspot in blindspots
    )
    assert category_specific_found, "Disabled student should receive category-specific blindspot"


def test_government_institution_student_gets_state_scholarship_blindspot(identifier, analyzer):
    """Test that government institution student receives state scholarship blindspot."""
    # Arrange - Create a government institution student profile
    profile = StudentProfile(
        name="Neha Gupta",
        age=20,
        education_level=EducationLevel.UG,
        degree="B.Sc",
        field_of_study="Mathematics",
        year_of_study=2,
        institution_type=InstitutionType.GOVERNMENT,
        background_indicators=[BackgroundIndicator.RURAL],
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES
    )
    
    analysis = analyzer.analyze(profile)
    
    # Act
    blindspots = identifier.identify_blindspots(profile, analysis)
    
    # Assert - Government institution student should get state scholarship blindspot
    state_scholarship_found = any(
        "State" in blindspot.category and "Scholarship" in blindspot.category
        for blindspot in blindspots
    )
    assert state_scholarship_found, "Government institution student should receive state scholarship blindspot"


def test_innovation_context_gets_innovation_blindspot(identifier, analyzer):
    """Test that student with innovation context receives innovation blindspot."""
    # Arrange - Create a profile with innovation in additional context
    profile = StudentProfile(
        name="Innovation Student",
        age=22,
        education_level=EducationLevel.UG,
        degree="B.Tech",
        field_of_study="Electronics",
        year_of_study=4,
        institution_type=InstitutionType.AUTONOMOUS,
        background_indicators=[BackgroundIndicator.FIRST_GENERATION],
        opportunity_goals=[OpportunityGoal.SKILLS],
        missed_opportunities_before=MissedOpportunityFrequency.ONCE_OR_TWICE,
        additional_context="I am interested in innovation and building new products"
    )
    
    analysis = analyzer.analyze(profile)
    
    # Act
    blindspots = identifier.identify_blindspots(profile, analysis)
    
    # Assert - Student with innovation context should get innovation blindspot
    innovation_found = any(
        "Innovation" in blindspot.category or "Skill" in blindspot.category
        for blindspot in blindspots
    )
    assert innovation_found, "Student with innovation context should receive innovation blindspot"


def test_skills_goal_gets_innovation_blindspot(identifier, analyzer):
    """Test that student with skills goal receives innovation/skill blindspot."""
    # Arrange - Create a profile with skills goal
    profile = StudentProfile(
        name="Skills Student",
        age=21,
        education_level=EducationLevel.UG,
        degree="BCA",
        field_of_study="Computer Applications",
        year_of_study=3,
        institution_type=InstitutionType.PRIVATE,
        background_indicators=[BackgroundIndicator.MINORITY],
        opportunity_goals=[OpportunityGoal.SKILLS],
        missed_opportunities_before=MissedOpportunityFrequency.ONCE_OR_TWICE
    )
    
    analysis = analyzer.analyze(profile)
    
    # Act
    blindspots = identifier.identify_blindspots(profile, analysis)
    
    # Assert - Student with skills goal should get skill/innovation blindspot
    skill_innovation_found = any(
        "Skill" in blindspot.category or "Innovation" in blindspot.category
        for blindspot in blindspots
    )
    assert skill_innovation_found, "Student with skills goal should receive skill/innovation blindspot"


def test_ug_stem_student_gets_research_blindspot(identifier, analyzer):
    """Test that UG STEM student receives research blindspot."""
    # Arrange - Create a UG STEM student profile
    profile = StudentProfile(
        name="UG STEM Student",
        age=20,
        education_level=EducationLevel.UG,
        degree="B.Tech",
        field_of_study="Computer Science",
        year_of_study=3,
        institution_type=InstitutionType.GOVERNMENT,
        background_indicators=[BackgroundIndicator.RURAL],
        opportunity_goals=[OpportunityGoal.INTERNSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES
    )
    
    analysis = analyzer.analyze(profile)
    
    # Act
    blindspots = identifier.identify_blindspots(profile, analysis)
    
    # Assert - UG STEM student should get research blindspot
    research_found = any(
        "Research" in blindspot.category
        for blindspot in blindspots
    )
    assert research_found, "UG STEM student should receive research blindspot"


def test_pg_stem_student_gets_research_blindspot(identifier, analyzer):
    """Test that PG STEM student receives research blindspot."""
    # Arrange - Create a PG STEM student profile
    profile = StudentProfile(
        name="PG STEM Student",
        age=23,
        education_level=EducationLevel.PG,
        degree="M.Tech",
        field_of_study="Data Science",
        year_of_study=1,
        institution_type=InstitutionType.AUTONOMOUS,
        background_indicators=[BackgroundIndicator.MINORITY],
        opportunity_goals=[OpportunityGoal.RESEARCH],
        missed_opportunities_before=MissedOpportunityFrequency.ONCE_OR_TWICE
    )
    
    analysis = analyzer.analyze(profile)
    
    # Act
    blindspots = identifier.identify_blindspots(profile, analysis)
    
    # Assert - PG STEM student should get research blindspot
    research_found = any(
        "Research" in blindspot.category
        for blindspot in blindspots
    )
    assert research_found, "PG STEM student should receive research blindspot"


def test_non_stem_student_no_stem_research_blindspot(identifier, analyzer):
    """Test that non-STEM student does not receive STEM-specific research blindspot."""
    # Arrange - Create a non-STEM student profile
    profile = StudentProfile(
        name="Non-STEM Student",
        age=21,
        education_level=EducationLevel.UG,
        degree="BA",
        field_of_study="English Literature",
        year_of_study=3,
        institution_type=InstitutionType.PRIVATE,
        background_indicators=[BackgroundIndicator.RURAL],
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES
    )
    
    analysis = analyzer.analyze(profile)
    
    # Act
    blindspots = identifier.identify_blindspots(profile, analysis)
    
    # Assert - Non-STEM student should not get STEM-specific research blindspot
    # (but may get general research blindspot if they have research goal)
    stem_research_found = any(
        "Research" in blindspot.category and 
        ("STEM" in blindspot.reason or "placements" in blindspot.reason)
        for blindspot in blindspots
    )
    assert not stem_research_found, "Non-STEM student should not receive STEM-specific research blindspot"


def test_blindspots_sorted_by_relevance(identifier, analyzer):
    """Test that blindspots are sorted by relevance score in descending order."""
    # Arrange - Create a profile that triggers multiple blindspots
    profile = StudentProfile(
        name="Test Student",
        age=20,
        education_level=EducationLevel.UG,
        degree="B.Tech",
        field_of_study="Computer Science",
        year_of_study=2,
        institution_type=InstitutionType.GOVERNMENT,
        background_indicators=[
            BackgroundIndicator.RURAL,
            BackgroundIndicator.FINANCIAL_SUPPORT
        ],
        opportunity_goals=[
            OpportunityGoal.SCHOLARSHIPS,
            OpportunityGoal.RESEARCH,
            OpportunityGoal.SKILLS
        ],
        missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES,
        gender="Female"
    )
    
    analysis = analyzer.analyze(profile)
    
    # Act
    blindspots = identifier.identify_blindspots(profile, analysis)
    
    # Assert - Blindspots should be sorted by relevance score (descending)
    relevance_scores = [b.relevance_score for b in blindspots]
    assert relevance_scores == sorted(relevance_scores, reverse=True), \
        "Blindspots should be sorted by relevance score in descending order"
    
    # Assert - First blindspot should have highest relevance
    assert blindspots[0].relevance_score >= blindspots[-1].relevance_score, \
        "First blindspot should have highest or equal relevance score"


def test_blindspot_count_always_between_3_and_5(identifier, analyzer):
    """Test that blindspot count is always between 3 and 5 for any valid profile."""
    # Test with various profile types
    test_profiles = [
        # Minimal profile
        StudentProfile(
            name="Minimal",
            age=20,
            education_level=EducationLevel.DIPLOMA,
            degree="Diploma",
            field_of_study="Electrical",
            year_of_study=2,
            institution_type=InstitutionType.PRIVATE,
            background_indicators=[BackgroundIndicator.RURAL],
            opportunity_goals=[OpportunityGoal.SKILLS],
            missed_opportunities_before=MissedOpportunityFrequency.NO
        ),
        # Maximal profile
        StudentProfile(
            name="Maximal",
            age=22,
            education_level=EducationLevel.PG,
            degree="M.Tech",
            field_of_study="Computer Science",
            year_of_study=1,
            institution_type=InstitutionType.GOVERNMENT,
            background_indicators=[
                BackgroundIndicator.RURAL,
                BackgroundIndicator.FIRST_GENERATION,
                BackgroundIndicator.FINANCIAL_SUPPORT,
                BackgroundIndicator.DISABLED
            ],
            opportunity_goals=[
                OpportunityGoal.SCHOLARSHIPS,
                OpportunityGoal.INTERNSHIPS,
                OpportunityGoal.RESEARCH,
                OpportunityGoal.SKILLS,
                OpportunityGoal.GOVT_EXAMS
            ],
            missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES,
            gender="Female",
            additional_context="Interested in innovation and startups"
        ),
        # PhD student
        StudentProfile(
            name="PhD Student",
            age=26,
            education_level=EducationLevel.PHD,
            degree="PhD",
            field_of_study="Chemistry",
            year_of_study=3,
            institution_type=InstitutionType.AUTONOMOUS,
            background_indicators=[BackgroundIndicator.MINORITY],
            opportunity_goals=[OpportunityGoal.RESEARCH],
            missed_opportunities_before=MissedOpportunityFrequency.ONCE_OR_TWICE
        )
    ]
    
    for profile in test_profiles:
        analysis = analyzer.analyze(profile)
        blindspots = identifier.identify_blindspots(profile, analysis)
        
        assert 3 <= len(blindspots) <= 5, \
            f"Expected 3-5 blindspots for {profile.name}, got {len(blindspots)}"


def test_each_blindspot_has_required_fields(identifier, analyzer):
    """Test that each blindspot has category, reason, and relevance_score."""
    # Arrange
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
    
    analysis = analyzer.analyze(profile)
    
    # Act
    blindspots = identifier.identify_blindspots(profile, analysis)
    
    # Assert - Each blindspot should have all required fields
    for blindspot in blindspots:
        assert blindspot.category, "Blindspot must have a category"
        assert isinstance(blindspot.category, str), "Category must be a string"
        assert len(blindspot.category) > 0, "Category must not be empty"
        
        assert blindspot.reason, "Blindspot must have a reason"
        assert isinstance(blindspot.reason, str), "Reason must be a string"
        assert len(blindspot.reason) > 0, "Reason must not be empty"
        
        assert blindspot.relevance_score is not None, "Blindspot must have a relevance score"
        assert isinstance(blindspot.relevance_score, (int, float)), "Relevance score must be numeric"
        assert blindspot.relevance_score > 0, "Relevance score must be positive"
