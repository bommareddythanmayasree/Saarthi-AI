"""Unit tests for ProfileAnalyzer component."""
import pytest
from saarthi_ai.profile_analyzer import ProfileAnalyzer
from saarthi_ai.models import (
    StudentProfile,
    EducationLevel,
    InstitutionType,
    BackgroundIndicator,
    OpportunityGoal,
    MissedOpportunityFrequency,
    AwarenessLevel
)


def test_analyze_basic_profile():
    """Test basic profile analysis."""
    analyzer = ProfileAnalyzer()
    
    profile = StudentProfile(
        name="Test Student",
        age=20,
        education_level=EducationLevel.UG,
        degree="B.Tech",
        field_of_study="Computer Science",
        year_of_study=2,
        institution_type=InstitutionType.GOVERNMENT,
        background_indicators=[BackgroundIndicator.RURAL, BackgroundIndicator.FIRST_GENERATION],
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS, OpportunityGoal.INTERNSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES
    )
    
    analysis = analyzer.analyze(profile)
    
    # Verify key characteristics
    assert "UG" in analysis.key_characteristics
    assert "Computer Science" in analysis.key_characteristics
    assert "Government" in analysis.key_characteristics
    assert "Rural" in analysis.key_characteristics
    assert "First-generation" in analysis.key_characteristics
    
    # Verify eligibility tags
    assert "Rural" in analysis.eligibility_tags
    assert "First-generation" in analysis.eligibility_tags
    
    # Verify awareness level mapping
    assert analysis.awareness_level == AwarenessLevel.LOW
    
    # Verify priority goals
    assert OpportunityGoal.SCHOLARSHIPS in analysis.priority_goals
    assert OpportunityGoal.INTERNSHIPS in analysis.priority_goals


def test_awareness_level_mapping_low():
    """Test awareness level mapping for YES_MANY_TIMES."""
    analyzer = ProfileAnalyzer()
    
    profile = StudentProfile(
        name="Test",
        age=20,
        education_level=EducationLevel.UG,
        degree="B.Tech",
        field_of_study="Engineering",
        year_of_study=2,
        institution_type=InstitutionType.PRIVATE,
        background_indicators=[BackgroundIndicator.RURAL],
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES
    )
    
    analysis = analyzer.analyze(profile)
    assert analysis.awareness_level == AwarenessLevel.LOW


def test_awareness_level_mapping_medium():
    """Test awareness level mapping for ONCE_OR_TWICE."""
    analyzer = ProfileAnalyzer()
    
    profile = StudentProfile(
        name="Test",
        age=20,
        education_level=EducationLevel.UG,
        degree="B.Tech",
        field_of_study="Engineering",
        year_of_study=2,
        institution_type=InstitutionType.PRIVATE,
        background_indicators=[BackgroundIndicator.RURAL],
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.ONCE_OR_TWICE
    )
    
    analysis = analyzer.analyze(profile)
    assert analysis.awareness_level == AwarenessLevel.MEDIUM


def test_awareness_level_mapping_high():
    """Test awareness level mapping for NO."""
    analyzer = ProfileAnalyzer()
    
    profile = StudentProfile(
        name="Test",
        age=20,
        education_level=EducationLevel.UG,
        degree="B.Tech",
        field_of_study="Engineering",
        year_of_study=2,
        institution_type=InstitutionType.PRIVATE,
        background_indicators=[BackgroundIndicator.RURAL],
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.NO
    )
    
    analysis = analyzer.analyze(profile)
    assert analysis.awareness_level == AwarenessLevel.HIGH


def test_multiple_background_indicators():
    """Test profile with multiple background indicators."""
    analyzer = ProfileAnalyzer()
    
    profile = StudentProfile(
        name="Test",
        age=20,
        education_level=EducationLevel.PG,
        degree="M.Tech",
        field_of_study="Mechanical Engineering",
        year_of_study=1,
        institution_type=InstitutionType.AUTONOMOUS,
        background_indicators=[
            BackgroundIndicator.RURAL,
            BackgroundIndicator.FINANCIAL_SUPPORT,
            BackgroundIndicator.MINORITY
        ],
        opportunity_goals=[OpportunityGoal.RESEARCH],
        missed_opportunities_before=MissedOpportunityFrequency.ONCE_OR_TWICE
    )
    
    analysis = analyzer.analyze(profile)
    
    # All background indicators should be in both characteristics and eligibility tags
    assert "Rural" in analysis.key_characteristics
    assert "Financial support" in analysis.key_characteristics
    assert "Minority" in analysis.key_characteristics
    assert len(analysis.eligibility_tags) == 3


def test_rural_first_gen_student():
    """Test analysis of rural, first-generation student profile."""
    analyzer = ProfileAnalyzer()
    
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
    
    # Verify rural and first-gen characteristics are captured
    assert "Rural" in analysis.key_characteristics
    assert "First-generation" in analysis.key_characteristics
    assert "Financial support" in analysis.key_characteristics
    assert "UG" in analysis.key_characteristics
    assert "Government" in analysis.key_characteristics
    
    # Verify eligibility tags include background indicators
    assert "Rural" in analysis.eligibility_tags
    assert "First-generation" in analysis.eligibility_tags
    assert "Financial support" in analysis.eligibility_tags
    
    # Verify low awareness level due to many missed opportunities
    assert analysis.awareness_level == AwarenessLevel.LOW
    
    # Verify scholarship goal is captured
    assert OpportunityGoal.SCHOLARSHIPS in analysis.priority_goals


def test_stem_student():
    """Test analysis of STEM student profile."""
    analyzer = ProfileAnalyzer()
    
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
    
    # Verify STEM field is captured
    assert "Physics" in analysis.key_characteristics
    assert "PG" in analysis.key_characteristics
    assert "Autonomous" in analysis.key_characteristics
    
    # Verify research and internship goals
    assert OpportunityGoal.RESEARCH in analysis.priority_goals
    assert OpportunityGoal.INTERNSHIPS in analysis.priority_goals
    
    # Verify medium awareness level
    assert analysis.awareness_level == AwarenessLevel.MEDIUM


def test_female_engineering_student():
    """Test analysis of female engineering student profile."""
    analyzer = ProfileAnalyzer()
    
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
    
    # Verify engineering field is captured
    assert "Computer Science" in analysis.key_characteristics
    assert "UG" in analysis.key_characteristics
    assert "Private" in analysis.key_characteristics
    
    # Verify first-generation tag
    assert "First-generation" in analysis.eligibility_tags
    
    # Verify goals
    assert OpportunityGoal.SCHOLARSHIPS in analysis.priority_goals
    assert OpportunityGoal.SKILLS in analysis.priority_goals
    
    # Verify low awareness
    assert analysis.awareness_level == AwarenessLevel.LOW


def test_disabled_student():
    """Test analysis of disabled student profile."""
    analyzer = ProfileAnalyzer()
    
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
    
    # Verify disabled indicator is captured
    assert "Disabled" in analysis.key_characteristics
    assert "Disabled" in analysis.eligibility_tags
    assert "Financial support" in analysis.eligibility_tags
    
    # Verify engineering field
    assert "Mechanical Engineering" in analysis.key_characteristics
    assert "UG" in analysis.key_characteristics
    
    # Verify low awareness
    assert analysis.awareness_level == AwarenessLevel.LOW


def test_private_institution_student():
    """Test analysis of private institution student profile."""
    analyzer = ProfileAnalyzer()
    
    profile = StudentProfile(
        name="Neha Gupta",
        age=20,
        education_level=EducationLevel.UG,
        degree="B.Com",
        field_of_study="Commerce",
        year_of_study=2,
        institution_type=InstitutionType.PRIVATE,
        background_indicators=[BackgroundIndicator.MINORITY],
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS, OpportunityGoal.GOVT_EXAMS],
        missed_opportunities_before=MissedOpportunityFrequency.NO
    )
    
    analysis = analyzer.analyze(profile)
    
    # Verify private institution is captured
    assert "Private" in analysis.key_characteristics
    assert "Commerce" in analysis.key_characteristics
    assert "UG" in analysis.key_characteristics
    
    # Verify minority tag
    assert "Minority" in analysis.eligibility_tags
    
    # Verify high awareness (never missed opportunities)
    assert analysis.awareness_level == AwarenessLevel.HIGH
    
    # Verify goals
    assert OpportunityGoal.SCHOLARSHIPS in analysis.priority_goals
    assert OpportunityGoal.GOVT_EXAMS in analysis.priority_goals


def test_phd_student():
    """Test analysis of PhD student profile."""
    analyzer = ProfileAnalyzer()
    
    profile = StudentProfile(
        name="Dr. Candidate",
        age=26,
        education_level=EducationLevel.PHD,
        degree="PhD",
        field_of_study="Chemistry",
        year_of_study=3,
        institution_type=InstitutionType.AUTONOMOUS,
        background_indicators=[BackgroundIndicator.RURAL],
        opportunity_goals=[OpportunityGoal.RESEARCH],
        missed_opportunities_before=MissedOpportunityFrequency.ONCE_OR_TWICE
    )
    
    analysis = analyzer.analyze(profile)
    
    # Verify PhD level is captured
    assert "PhD" in analysis.key_characteristics
    assert "Chemistry" in analysis.key_characteristics
    assert "Autonomous" in analysis.key_characteristics
    
    # Verify research goal
    assert OpportunityGoal.RESEARCH in analysis.priority_goals
    
    # Verify medium awareness
    assert analysis.awareness_level == AwarenessLevel.MEDIUM


def test_diploma_student():
    """Test analysis of diploma student profile."""
    analyzer = ProfileAnalyzer()
    
    profile = StudentProfile(
        name="Amit Kumar",
        age=18,
        education_level=EducationLevel.DIPLOMA,
        degree="Diploma",
        field_of_study="Electrical Engineering",
        year_of_study=2,
        institution_type=InstitutionType.GOVERNMENT,
        background_indicators=[
            BackgroundIndicator.RURAL,
            BackgroundIndicator.FINANCIAL_SUPPORT
        ],
        opportunity_goals=[OpportunityGoal.SKILLS, OpportunityGoal.SCHOLARSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES
    )
    
    analysis = analyzer.analyze(profile)
    
    # Verify diploma level is captured
    assert "Diploma" in analysis.key_characteristics
    assert "Electrical Engineering" in analysis.key_characteristics
    
    # Verify background indicators
    assert "Rural" in analysis.eligibility_tags
    assert "Financial support" in analysis.eligibility_tags
    
    # Verify low awareness
    assert analysis.awareness_level == AwarenessLevel.LOW


def test_student_with_all_goals():
    """Test analysis of student with all opportunity goals."""
    analyzer = ProfileAnalyzer()
    
    profile = StudentProfile(
        name="Multi Goal Student",
        age=21,
        education_level=EducationLevel.UG,
        degree="B.Tech",
        field_of_study="Information Technology",
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
    
    # Verify all goals are captured
    assert len(analysis.priority_goals) == 5
    assert OpportunityGoal.SCHOLARSHIPS in analysis.priority_goals
    assert OpportunityGoal.INTERNSHIPS in analysis.priority_goals
    assert OpportunityGoal.RESEARCH in analysis.priority_goals
    assert OpportunityGoal.SKILLS in analysis.priority_goals
    assert OpportunityGoal.GOVT_EXAMS in analysis.priority_goals
    
    # Verify medium awareness
    assert analysis.awareness_level == AwarenessLevel.MEDIUM


def test_open_university_student():
    """Test analysis of open university student profile."""
    analyzer = ProfileAnalyzer()
    
    profile = StudentProfile(
        name="Distance Learner",
        age=25,
        education_level=EducationLevel.UG,
        degree="BA",
        field_of_study="History",
        year_of_study=3,
        institution_type=InstitutionType.OPEN,
        background_indicators=[BackgroundIndicator.FINANCIAL_SUPPORT],
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES
    )
    
    analysis = analyzer.analyze(profile)
    
    # Verify open institution type is captured
    assert "Open" in analysis.key_characteristics
    assert "History" in analysis.key_characteristics
    
    # Verify financial support tag
    assert "Financial support" in analysis.eligibility_tags
    
    # Verify low awareness
    assert analysis.awareness_level == AwarenessLevel.LOW
