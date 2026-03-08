"""Unit tests for OpportunityMatcher component."""
import pytest
from saarthi_ai.opportunity_matcher import OpportunityMatcher
from saarthi_ai.models import (
    StudentProfile,
    ProfileAnalysis,
    Blindspot,
    Opportunity,
    EligibilityCriteria,
    EducationLevel,
    InstitutionType,
    BackgroundIndicator,
    OpportunityGoal,
    MissedOpportunityFrequency,
    AwarenessLevel,
    VisibilityLevel,
    ImpactLevel,
    MissProbability,
)


@pytest.fixture
def matcher():
    """Create an OpportunityMatcher instance."""
    return OpportunityMatcher()


@pytest.fixture
def sample_ug_engineering_profile():
    """Create a sample UG engineering student profile."""
    return StudentProfile(
        name="Test Student",
        age=20,
        education_level=EducationLevel.UG,
        degree="B.Tech",
        field_of_study="Engineering",
        year_of_study=2,
        institution_type=InstitutionType.GOVERNMENT,
        background_indicators=[BackgroundIndicator.FINANCIAL_SUPPORT],
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES,
        gender="Male",
        additional_context=None,
    )


@pytest.fixture
def sample_female_engineering_profile():
    """Create a sample female UG engineering student profile."""
    return StudentProfile(
        name="Test Student",
        age=20,
        education_level=EducationLevel.UG,
        degree="B.Tech",
        field_of_study="Engineering",
        year_of_study=2,
        institution_type=InstitutionType.GOVERNMENT,
        background_indicators=[BackgroundIndicator.RURAL],
        opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.ONCE_OR_TWICE,
        gender="Female",
        additional_context=None,
    )


@pytest.fixture
def sample_pg_stem_profile():
    """Create a sample PG STEM student profile."""
    return StudentProfile(
        name="Test Student",
        age=24,
        education_level=EducationLevel.PG,
        degree="M.Sc",
        field_of_study="Computer Science",
        year_of_study=1,
        institution_type=InstitutionType.AUTONOMOUS,
        background_indicators=[BackgroundIndicator.FIRST_GENERATION],
        opportunity_goals=[OpportunityGoal.RESEARCH, OpportunityGoal.INTERNSHIPS],
        missed_opportunities_before=MissedOpportunityFrequency.NO,
        gender=None,
        additional_context=None,
    )


@pytest.fixture
def sample_analysis_low_awareness():
    """Create a sample profile analysis with low awareness."""
    return ProfileAnalysis(
        key_characteristics=["UG", "Engineering", "Government"],
        eligibility_tags=["Financial support"],
        awareness_level=AwarenessLevel.LOW,
        priority_goals=[OpportunityGoal.SCHOLARSHIPS],
    )


@pytest.fixture
def sample_analysis_high_awareness():
    """Create a sample profile analysis with high awareness."""
    return ProfileAnalysis(
        key_characteristics=["PG", "Computer Science", "Autonomous"],
        eligibility_tags=["First-generation"],
        awareness_level=AwarenessLevel.HIGH,
        priority_goals=[OpportunityGoal.RESEARCH, OpportunityGoal.INTERNSHIPS],
    )


@pytest.fixture
def sample_blindspots():
    """Create sample blindspots."""
    return [
        Blindspot(
            category="Income-based Central Government Scholarships",
            reason="Many students don't know about central government scholarships",
            relevance_score=0.9,
        ),
        Blindspot(
            category="Research Internships and Programs",
            reason="STEM students often focus on placements",
            relevance_score=0.8,
        ),
        Blindspot(
            category="State-level Merit Scholarships",
            reason="State scholarships have poor visibility",
            relevance_score=0.7,
        ),
    ]


class TestEligibilityChecking:
    """Tests for is_eligible method."""
    
    def test_eligible_education_level(self, matcher, sample_ug_engineering_profile):
        """Test eligibility check for education level."""
        criteria = EligibilityCriteria(
            education_levels=[EducationLevel.UG],
        )
        assert matcher.is_eligible(sample_ug_engineering_profile, criteria)
    
    def test_ineligible_education_level(self, matcher, sample_ug_engineering_profile):
        """Test ineligibility for wrong education level."""
        criteria = EligibilityCriteria(
            education_levels=[EducationLevel.PG, EducationLevel.PHD],
        )
        assert not matcher.is_eligible(sample_ug_engineering_profile, criteria)
    
    def test_eligible_field_of_study(self, matcher, sample_ug_engineering_profile):
        """Test eligibility check for field of study."""
        criteria = EligibilityCriteria(
            education_levels=[EducationLevel.UG],
            fields_of_study=["Engineering", "Computer Science"],
        )
        assert matcher.is_eligible(sample_ug_engineering_profile, criteria)
    
    def test_ineligible_field_of_study(self, matcher, sample_ug_engineering_profile):
        """Test ineligibility for wrong field of study."""
        criteria = EligibilityCriteria(
            education_levels=[EducationLevel.UG],
            fields_of_study=["Medicine", "Law"],
        )
        assert not matcher.is_eligible(sample_ug_engineering_profile, criteria)
    
    def test_eligible_no_field_restriction(self, matcher, sample_ug_engineering_profile):
        """Test eligibility when field of study is not restricted."""
        criteria = EligibilityCriteria(
            education_levels=[EducationLevel.UG],
            fields_of_study=None,  # All fields allowed
        )
        assert matcher.is_eligible(sample_ug_engineering_profile, criteria)
    
    def test_eligible_institution_type(self, matcher, sample_ug_engineering_profile):
        """Test eligibility check for institution type."""
        criteria = EligibilityCriteria(
            education_levels=[EducationLevel.UG],
            institution_types=[InstitutionType.GOVERNMENT, InstitutionType.AUTONOMOUS],
        )
        assert matcher.is_eligible(sample_ug_engineering_profile, criteria)
    
    def test_ineligible_institution_type(self, matcher, sample_ug_engineering_profile):
        """Test ineligibility for wrong institution type."""
        criteria = EligibilityCriteria(
            education_levels=[EducationLevel.UG],
            institution_types=[InstitutionType.PRIVATE],
        )
        assert not matcher.is_eligible(sample_ug_engineering_profile, criteria)
    
    def test_eligible_background_requirement(self, matcher, sample_ug_engineering_profile):
        """Test eligibility check for background requirements."""
        criteria = EligibilityCriteria(
            education_levels=[EducationLevel.UG],
            background_requirements=[BackgroundIndicator.FINANCIAL_SUPPORT, BackgroundIndicator.RURAL],
        )
        assert matcher.is_eligible(sample_ug_engineering_profile, criteria)
    
    def test_ineligible_background_requirement(self, matcher, sample_ug_engineering_profile):
        """Test ineligibility for missing background requirements."""
        criteria = EligibilityCriteria(
            education_levels=[EducationLevel.UG],
            background_requirements=[BackgroundIndicator.DISABLED],
        )
        assert not matcher.is_eligible(sample_ug_engineering_profile, criteria)
    
    def test_eligible_no_background_restriction(self, matcher, sample_ug_engineering_profile):
        """Test eligibility when background is not restricted."""
        criteria = EligibilityCriteria(
            education_levels=[EducationLevel.UG],
            background_requirements=None,  # No background requirements
        )
        assert matcher.is_eligible(sample_ug_engineering_profile, criteria)


class TestMissProbabilityCalculation:
    """Tests for calculate_miss_probability method."""
    
    def test_low_visibility_high_miss_probability(self, matcher):
        """Test that low visibility always results in high miss probability."""
        assert matcher.calculate_miss_probability(
            VisibilityLevel.LOW, AwarenessLevel.LOW
        ) == MissProbability.HIGH
        
        assert matcher.calculate_miss_probability(
            VisibilityLevel.LOW, AwarenessLevel.MEDIUM
        ) == MissProbability.HIGH
        
        assert matcher.calculate_miss_probability(
            VisibilityLevel.LOW, AwarenessLevel.HIGH
        ) == MissProbability.HIGH
    
    def test_medium_visibility_low_awareness(self, matcher):
        """Test medium visibility with low awareness results in high miss probability."""
        assert matcher.calculate_miss_probability(
            VisibilityLevel.MEDIUM, AwarenessLevel.LOW
        ) == MissProbability.HIGH
    
    def test_medium_visibility_medium_awareness(self, matcher):
        """Test medium visibility with medium awareness results in medium miss probability."""
        assert matcher.calculate_miss_probability(
            VisibilityLevel.MEDIUM, AwarenessLevel.MEDIUM
        ) == MissProbability.MEDIUM
    
    def test_medium_visibility_high_awareness(self, matcher):
        """Test medium visibility with high awareness results in low miss probability."""
        assert matcher.calculate_miss_probability(
            VisibilityLevel.MEDIUM, AwarenessLevel.HIGH
        ) == MissProbability.LOW
    
    def test_high_visibility_low_awareness(self, matcher):
        """Test high visibility with low awareness results in medium miss probability."""
        assert matcher.calculate_miss_probability(
            VisibilityLevel.HIGH, AwarenessLevel.LOW
        ) == MissProbability.MEDIUM
    
    def test_high_visibility_medium_awareness(self, matcher):
        """Test high visibility with medium awareness results in low miss probability."""
        assert matcher.calculate_miss_probability(
            VisibilityLevel.HIGH, AwarenessLevel.MEDIUM
        ) == MissProbability.LOW
    
    def test_high_visibility_high_awareness(self, matcher):
        """Test high visibility with high awareness results in low miss probability."""
        assert matcher.calculate_miss_probability(
            VisibilityLevel.HIGH, AwarenessLevel.HIGH
        ) == MissProbability.LOW


class TestMatchOpportunities:
    """Tests for match_opportunities method."""
    
    def test_returns_2_to_3_matches(
        self, matcher, sample_ug_engineering_profile, 
        sample_analysis_low_awareness, sample_blindspots
    ):
        """Test that match_opportunities returns 2-3 matches."""
        matches = matcher.match_opportunities(
            sample_ug_engineering_profile,
            sample_analysis_low_awareness,
            sample_blindspots,
        )
        
        assert len(matches) >= 2, "Should return at least 2 matches"
        assert len(matches) <= 3, "Should return at most 3 matches"
    
    def test_filters_ineligible_opportunities(
        self, matcher, sample_pg_stem_profile,
        sample_analysis_high_awareness, sample_blindspots
    ):
        """Test that ineligible opportunities are filtered out."""
        matches = matcher.match_opportunities(
            sample_pg_stem_profile,
            sample_analysis_high_awareness,
            sample_blindspots,
        )
        
        # PG student should not get UG-only opportunities
        for match in matches:
            assert sample_pg_stem_profile.education_level in match.opportunity.eligibility_criteria.education_levels
    
    def test_match_has_required_fields(
        self, matcher, sample_ug_engineering_profile,
        sample_analysis_low_awareness, sample_blindspots
    ):
        """Test that each match has all required fields."""
        matches = matcher.match_opportunities(
            sample_ug_engineering_profile,
            sample_analysis_low_awareness,
            sample_blindspots,
        )
        
        for match in matches:
            assert match.opportunity is not None
            assert match.fit_explanation is not None
            assert len(match.fit_explanation) > 0
            assert match.miss_reason is not None
            assert len(match.miss_reason) > 0
            assert match.miss_probability in [
                MissProbability.HIGH, MissProbability.MEDIUM, MissProbability.LOW
            ]
            assert match.relevance_score >= 0.0
            assert match.relevance_score <= 1.0
    
    def test_matches_sorted_by_relevance(
        self, matcher, sample_ug_engineering_profile,
        sample_analysis_low_awareness, sample_blindspots
    ):
        """Test that matches are sorted by relevance score in descending order."""
        matches = matcher.match_opportunities(
            sample_ug_engineering_profile,
            sample_analysis_low_awareness,
            sample_blindspots,
        )
        
        if len(matches) > 1:
            for i in range(len(matches) - 1):
                assert matches[i].relevance_score >= matches[i + 1].relevance_score
    
    def test_female_engineering_student_gets_pragati(
        self, matcher, sample_female_engineering_profile,
        sample_analysis_low_awareness
    ):
        """Test that female engineering students get AICTE Pragati recommendation."""
        blindspots = [
            Blindspot(
                category="Category-specific Technical Scholarships",
                reason="Programs like AICTE Pragati are under-promoted",
                relevance_score=0.85,
            ),
        ]
        
        matches = matcher.match_opportunities(
            sample_female_engineering_profile,
            sample_analysis_low_awareness,
            blindspots,
        )
        
        # Check if AICTE Pragati is in the matches
        pragati_found = any(
            "Pragati" in match.opportunity.name for match in matches
        )
        assert pragati_found, "Female engineering student should get AICTE Pragati recommendation"
    
    def test_fit_explanation_references_profile(
        self, matcher, sample_ug_engineering_profile,
        sample_analysis_low_awareness, sample_blindspots
    ):
        """Test that fit explanations reference elements from the student's profile."""
        matches = matcher.match_opportunities(
            sample_ug_engineering_profile,
            sample_analysis_low_awareness,
            sample_blindspots,
        )
        
        for match in matches:
            explanation_lower = match.fit_explanation.lower()
            
            # Should reference at least one profile element
            profile_elements = [
                sample_ug_engineering_profile.education_level.value.lower(),
                sample_ug_engineering_profile.field_of_study.lower(),
                sample_ug_engineering_profile.institution_type.value.lower(),
            ]
            
            # Add background indicators
            for bg in sample_ug_engineering_profile.background_indicators:
                profile_elements.append(bg.value.lower())
            
            # Check if any profile element is mentioned
            has_reference = any(
                element in explanation_lower for element in profile_elements
            )
            
            assert has_reference, f"Fit explanation should reference profile elements: {match.fit_explanation}"
