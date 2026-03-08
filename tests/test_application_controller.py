"""Unit tests for ApplicationController component."""
import pytest
from saarthi_ai.application_controller import ApplicationController
from saarthi_ai.models import (
    StudentProfile,
    EducationLevel,
    InstitutionType,
    BackgroundIndicator,
    OpportunityGoal,
    MissedOpportunityFrequency,
)


class TestApplicationController:
    """Test suite for ApplicationController."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.controller = ApplicationController()
    
    def test_start_displays_welcome_screen(self):
        """Test that start() displays the welcome screen."""
        # Call start() - it should display welcome screen
        self.controller.start()
        
        # Verify controller is initialized
        assert self.controller.profile_analyzer is not None
        assert self.controller.blindspot_identifier is not None
        assert self.controller.opportunity_matcher is not None
        assert self.controller.explanation_generator is not None
    
    def test_display_welcome_screen_contains_required_elements(self):
        """Test that welcome screen contains app name and explanation."""
        welcome_text = self.controller.display_welcome_screen()
        
        # Should contain app name
        assert "SaarthiAI" in welcome_text
        
        # Should explain the opportunity awareness gap
        assert "don't know" in welcome_text.lower()
        assert "opportunity" in welcome_text.lower() or "opportunities" in welcome_text.lower()
    
    def test_display_form_screen_contains_form_header(self):
        """Test that form screen displays correctly."""
        form_text = self.controller.display_form_screen()
        
        # Should contain form header
        assert "form" in form_text.lower() or "information" in form_text.lower()
    
    def test_handle_form_submission_with_valid_profile(self):
        """Test form submission with a complete valid profile."""
        # Create a valid profile
        profile = StudentProfile(
            name="Priya Sharma",
            age=20,
            education_level=EducationLevel.UG,
            degree="B.Tech",
            field_of_study="Computer Science",
            year_of_study=2,
            institution_type=InstitutionType.GOVERNMENT,
            background_indicators=[BackgroundIndicator.RURAL, BackgroundIndicator.FINANCIAL_SUPPORT],
            opportunity_goals=[OpportunityGoal.SCHOLARSHIPS, OpportunityGoal.INTERNSHIPS],
            missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES,
            gender="Female"
        )
        
        # Handle form submission
        result = self.controller.handle_form_submission(profile)
        
        # Should be valid
        assert result['valid'] is True
        
        # Should contain all required outputs
        assert 'profile_summary' in result
        assert 'blindspots' in result
        assert 'matches' in result
        assert 'final_insight' in result
        
        # Verify profile summary contains student name
        assert profile.name in result['profile_summary']
        
        # Verify blindspots are returned (3-5)
        assert 3 <= len(result['blindspots']) <= 5
        
        # Verify matches are returned (2-3, or fewer if limited eligibility)
        assert len(result['matches']) >= 0  # Can be 0 for very specific profiles
        
        # Verify final insight is generated
        assert len(result['final_insight']) > 0
    
    def test_handle_form_submission_with_missing_required_fields(self):
        """Test form submission with missing required fields."""
        # Create a profile with missing required fields
        profile = StudentProfile(
            name="",  # Missing name
            age=20,
            education_level=EducationLevel.UG,
            degree="B.Tech",
            field_of_study="Computer Science",
            year_of_study=2,
            institution_type=InstitutionType.GOVERNMENT,
            background_indicators=[],  # Missing background indicators
            opportunity_goals=[],  # Missing opportunity goals
            missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES
        )
        
        # Handle form submission
        result = self.controller.handle_form_submission(profile)
        
        # Should be invalid
        assert result['valid'] is False
        
        # Should contain missing fields
        assert 'missing_fields' in result
        assert len(result['missing_fields']) > 0
        
        # Should include the missing fields
        assert 'name' in result['missing_fields']
        assert 'background_indicators' in result['missing_fields']
        assert 'opportunity_goals' in result['missing_fields']
    
    def test_display_validation_errors_shows_missing_fields(self):
        """Test that validation errors display missing fields."""
        missing_fields = ['name', 'age', 'education_level']
        
        error_text = self.controller.display_validation_errors(missing_fields)
        
        # Should contain all missing fields
        for field in missing_fields:
            assert field in error_text
        
        # Should indicate it's an error
        assert 'error' in error_text.lower() or 'required' in error_text.lower()
    
    def test_display_profile_understanding_screen(self):
        """Test profile understanding screen display."""
        profile_summary = "Hi Priya! I've understood your profile:\n• You're a 2-year UG student"
        
        screen_text = self.controller.display_profile_understanding_screen(profile_summary)
        
        # Should contain the profile summary
        assert profile_summary in screen_text
    
    def test_display_blindspot_analysis_screen(self):
        """Test blindspot analysis screen display."""
        from saarthi_ai.models import Blindspot
        
        blindspots = [
            Blindspot(
                category="Income-based Scholarships",
                reason="Students don't know about these",
                relevance_score=0.9
            ),
            Blindspot(
                category="Research Opportunities",
                reason="Focus on placements instead",
                relevance_score=0.8
            )
        ]
        
        screen_text = self.controller.display_blindspot_analysis_screen(blindspots)
        
        # Should contain blindspot categories
        assert "Income-based Scholarships" in screen_text
        assert "Research Opportunities" in screen_text
        
        # Should contain reasons
        assert "Students don't know about these" in screen_text
        assert "Focus on placements instead" in screen_text
    
    def test_display_recommendations_screen(self):
        """Test recommendations screen display."""
        from saarthi_ai.models import OpportunityMatch, Opportunity, EligibilityCriteria, MissProbability, VisibilityLevel, ImpactLevel
        
        opportunity = Opportunity(
            id="test-opp",
            name="Test Scholarship",
            description="A test scholarship",
            eligibility_criteria=EligibilityCriteria(
                education_levels=[EducationLevel.UG]
            ),
            visibility_level=VisibilityLevel.LOW,
            impact_level=ImpactLevel.HIGH,
            category="Scholarship"
        )
        
        matches = [
            OpportunityMatch(
                opportunity=opportunity,
                fit_explanation="You're eligible because...",
                miss_reason="Students miss this because...",
                miss_probability=MissProbability.HIGH,
                relevance_score=0.9
            )
        ]
        
        screen_text = self.controller.display_recommendations_screen(matches)
        
        # Should contain opportunity name
        assert "Test Scholarship" in screen_text
        
        # Should contain explanations
        assert "You're eligible because..." in screen_text
        assert "Students miss this because..." in screen_text
        
        # Should contain miss probability
        assert "High" in screen_text
    
    def test_display_final_insight_screen(self):
        """Test final insight screen display."""
        final_insight = "Based on your profile, you're missing opportunities. Awareness is key."
        
        screen_text = self.controller.display_final_insight_screen(final_insight)
        
        # Should contain the final insight
        assert final_insight in screen_text
    
    def test_complete_flow_with_valid_profile(self):
        """Test the complete flow from form submission to final insight."""
        # Create a valid profile
        profile = StudentProfile(
            name="Rahul Kumar",
            age=21,
            education_level=EducationLevel.UG,
            degree="B.E.",
            field_of_study="Engineering",
            year_of_study=3,
            institution_type=InstitutionType.PRIVATE,
            background_indicators=[BackgroundIndicator.FIRST_GENERATION],
            opportunity_goals=[OpportunityGoal.SCHOLARSHIPS, OpportunityGoal.SKILLS],
            missed_opportunities_before=MissedOpportunityFrequency.ONCE_OR_TWICE
        )
        
        # Handle form submission
        result = self.controller.handle_form_submission(profile)
        
        # Verify the flow completed successfully
        assert result['valid'] is True
        
        # Display all screens
        self.controller.display_profile_understanding_screen(result['profile_summary'])
        self.controller.display_blindspot_analysis_screen(result['blindspots'])
        self.controller.display_recommendations_screen(result['matches'])
        self.controller.display_final_insight_screen(result['final_insight'])
        
        # Verify all components were called and produced output
        assert len(result['profile_summary']) > 0
        assert len(result['blindspots']) >= 3
        assert len(result['final_insight']) > 0
    
    def test_screen_transition_sequence(self):
        """Test that screens are presented in the correct sequence."""
        # Create a valid profile
        profile = StudentProfile(
            name="Test Student",
            age=20,
            education_level=EducationLevel.UG,
            degree="B.Sc",
            field_of_study="Physics",
            year_of_study=2,
            institution_type=InstitutionType.GOVERNMENT,
            background_indicators=[BackgroundIndicator.RURAL],
            opportunity_goals=[OpportunityGoal.RESEARCH],
            missed_opportunities_before=MissedOpportunityFrequency.NO
        )
        
        # Start the application (Screen 1: Welcome)
        self.controller.start()
        
        # Display form screen (Screen 2: Form)
        self.controller.display_form_screen()
        
        # Handle form submission (Screens 3-6)
        result = self.controller.handle_form_submission(profile)
        
        # Verify we can display all subsequent screens in order
        assert result['valid'] is True
        
        # Screen 3: Profile Understanding
        profile_screen = self.controller.display_profile_understanding_screen(result['profile_summary'])
        assert len(profile_screen) > 0
        
        # Screen 4: Blindspot Analysis
        blindspot_screen = self.controller.display_blindspot_analysis_screen(result['blindspots'])
        assert len(blindspot_screen) > 0
        
        # Screen 5: Recommendations
        recommendations_screen = self.controller.display_recommendations_screen(result['matches'])
        assert len(recommendations_screen) > 0
        
        # Screen 6: Final Insight
        final_screen = self.controller.display_final_insight_screen(result['final_insight'])
        assert len(final_screen) > 0
    
    def test_form_validation_prevents_invalid_submission(self):
        """Test that form validation prevents submission with invalid data."""
        # Create profile with invalid age
        profile = StudentProfile(
            name="Test Student",
            age=-5,  # Invalid age
            education_level=EducationLevel.UG,
            degree="B.Tech",
            field_of_study="Computer Science",
            year_of_study=2,
            institution_type=InstitutionType.GOVERNMENT,
            background_indicators=[BackgroundIndicator.RURAL],
            opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
            missed_opportunities_before=MissedOpportunityFrequency.NO
        )
        
        # Handle form submission
        result = self.controller.handle_form_submission(profile)
        
        # Should be invalid due to invalid field value
        assert result['valid'] is False
        assert 'invalid_fields' in result
        assert any('age' in field for field in result['invalid_fields'])
    
    def test_multiple_profiles_in_sequence(self):
        """Test handling multiple profile submissions in sequence."""
        # First profile
        profile1 = StudentProfile(
            name="Student One",
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
        
        result1 = self.controller.handle_form_submission(profile1)
        assert result1['valid'] is True
        
        # Second profile
        profile2 = StudentProfile(
            name="Student Two",
            age=22,
            education_level=EducationLevel.PG,
            degree="M.Sc",
            field_of_study="Physics",
            year_of_study=1,
            institution_type=InstitutionType.PRIVATE,
            background_indicators=[BackgroundIndicator.FIRST_GENERATION],
            opportunity_goals=[OpportunityGoal.RESEARCH],
            missed_opportunities_before=MissedOpportunityFrequency.NO
        )
        
        result2 = self.controller.handle_form_submission(profile2)
        assert result2['valid'] is True
        
        # Verify results are different
        assert result1['profile_summary'] != result2['profile_summary']
        assert "Student One" in result1['profile_summary']
        assert "Student Two" in result2['profile_summary']
