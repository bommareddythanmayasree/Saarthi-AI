"""Unit tests for error handling in SaarthiAI application."""
import pytest
from unittest.mock import patch, MagicMock
from saarthi_ai.application_controller import ApplicationController
from saarthi_ai.models import (
    StudentProfile,
    EducationLevel,
    InstitutionType,
    BackgroundIndicator,
    OpportunityGoal,
    MissedOpportunityFrequency,
)


class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_missing_required_fields_error(self):
        """Test that missing required fields are properly detected and reported."""
        controller = ApplicationController()
        
        # Create profile with missing required fields
        profile = StudentProfile(
            name="",  # Missing name
            age=0,  # Invalid age
            education_level=EducationLevel.UG,
            degree="",  # Missing degree
            field_of_study="Computer Science",
            year_of_study=2,
            institution_type=InstitutionType.GOVERNMENT,
            background_indicators=[],  # Missing background indicators
            opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
            missed_opportunities_before=MissedOpportunityFrequency.NO,
        )
        
        result = controller.handle_form_submission(profile)
        
        assert result['valid'] is False
        assert 'missing_fields' in result
        assert 'name' in result['missing_fields']
        assert 'age' in result['missing_fields']
        assert 'degree' in result['missing_fields']
        assert 'background_indicators' in result['missing_fields']
    
    def test_invalid_field_values_error(self):
        """Test that invalid field values are properly detected and reported."""
        controller = ApplicationController()
        
        # Create profile with invalid field values
        profile = StudentProfile(
            name="Test Student",
            age=-5,  # Negative age
            education_level=EducationLevel.UG,
            degree="B.Tech",
            field_of_study="Computer Science",
            year_of_study=15,  # Unrealistic year
            institution_type=InstitutionType.GOVERNMENT,
            background_indicators=[BackgroundIndicator.RURAL],
            opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
            missed_opportunities_before=MissedOpportunityFrequency.NO,
        )
        
        result = controller.handle_form_submission(profile)
        
        assert result['valid'] is False
        assert 'invalid_fields' in result
        assert any('age' in field for field in result['invalid_fields'])
        assert any('year_of_study' in field for field in result['invalid_fields'])
    
    def test_empty_knowledge_base_error(self):
        """Test error handling when knowledge base is empty."""
        controller = ApplicationController()
        
        # Create valid profile
        profile = StudentProfile(
            name="Test Student",
            age=20,
            education_level=EducationLevel.UG,
            degree="B.Tech",
            field_of_study="Computer Science",
            year_of_study=2,
            institution_type=InstitutionType.GOVERNMENT,
            background_indicators=[BackgroundIndicator.RURAL],
            opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
            missed_opportunities_before=MissedOpportunityFrequency.NO,
        )
        
        # Mock empty knowledge base
        with patch('saarthi_ai.application_controller.get_all_opportunities', return_value=[]):
            result = controller.handle_form_submission(profile)
        
        assert result['valid'] is False
        assert 'error' in result
        assert 'knowledge base' in result['error'].lower() or 'unavailable' in result['error'].lower()
    
    def test_no_eligible_opportunities_scenario(self):
        """Test handling when no opportunities match the student profile."""
        controller = ApplicationController()
        
        # Create profile that won't match any opportunities
        # Using a PhD student in a very specific field
        profile = StudentProfile(
            name="Test Student",
            age=28,
            education_level=EducationLevel.PHD,
            degree="PhD",
            field_of_study="Quantum Physics",
            year_of_study=3,
            institution_type=InstitutionType.PRIVATE,
            background_indicators=[BackgroundIndicator.MINORITY],
            opportunity_goals=[OpportunityGoal.RESEARCH],
            missed_opportunities_before=MissedOpportunityFrequency.NO,
        )
        
        # Mock opportunity matcher to return no matches
        with patch.object(controller.opportunity_matcher, 'match_opportunities', return_value=[]):
            result = controller.handle_form_submission(profile)
        
        assert result['valid'] is True
        assert result['matches'] == []
        assert 'no_matches' in result or 'final_insight' in result
        # Should still have profile summary and blindspots
        assert 'profile_summary' in result
        assert 'blindspots' in result
    
    def test_ai_generation_failure_fallback(self):
        """Test fallback template-based explanations when AI generation fails."""
        controller = ApplicationController()
        
        # Create valid profile
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
            missed_opportunities_before=MissedOpportunityFrequency.NO,
        )
        
        # Mock explanation generator to return empty strings
        with patch.object(controller.explanation_generator, 'generate_profile_summary', return_value=""):
            result = controller.handle_form_submission(profile)
        
        # Should use fallback and still succeed
        assert result['valid'] is True
        assert 'profile_summary' in result
        assert result['profile_summary']  # Should not be empty due to fallback
        assert profile.name in result['profile_summary']
    
    def test_fallback_blindspots_generation(self):
        """Test fallback blindspot generation when identifier returns empty list."""
        controller = ApplicationController()
        
        # Create valid profile
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
            missed_opportunities_before=MissedOpportunityFrequency.NO,
        )
        
        # Mock blindspot identifier to return empty list
        with patch.object(controller.blindspot_identifier, 'identify_blindspots', return_value=[]):
            result = controller.handle_form_submission(profile)
        
        # Should use fallback blindspots
        assert result['valid'] is True
        assert 'blindspots' in result
        assert len(result['blindspots']) > 0  # Should have fallback blindspots
    
    def test_fallback_final_insight_generation(self):
        """Test fallback final insight generation when generator returns empty string."""
        controller = ApplicationController()
        
        # Create valid profile
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
            missed_opportunities_before=MissedOpportunityFrequency.NO,
        )
        
        # Mock final insight generator to return empty string
        with patch.object(controller.explanation_generator, 'generate_final_insight', return_value=""):
            result = controller.handle_form_submission(profile)
        
        # Should use fallback and still succeed
        assert result['valid'] is True
        assert 'final_insight' in result
        assert result['final_insight']  # Should not be empty due to fallback
        assert 'awareness' in result['final_insight'].lower() or 'opportunity' in result['final_insight'].lower()
    
    def test_exception_handling_during_processing(self):
        """Test that exceptions during processing are caught and handled gracefully."""
        controller = ApplicationController()
        
        # Create valid profile
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
            missed_opportunities_before=MissedOpportunityFrequency.NO,
        )
        
        # Mock profile analyzer to raise an exception
        with patch.object(controller.profile_analyzer, 'analyze', side_effect=Exception("Test error")):
            result = controller.handle_form_submission(profile)
        
        # Should handle exception gracefully
        assert result['valid'] is False
        assert 'error' in result
        assert 'error' in result['error'].lower()
    
    def test_display_validation_errors_with_missing_fields(self):
        """Test display of validation errors for missing fields."""
        controller = ApplicationController()
        
        missing_fields = ['name', 'age', 'degree']
        error_text = controller.display_validation_errors(missing_fields=missing_fields)
        
        assert 'Validation Error' in error_text
        assert 'name' in error_text
        assert 'age' in error_text
        assert 'degree' in error_text
    
    def test_display_validation_errors_with_invalid_fields(self):
        """Test display of validation errors for invalid fields."""
        controller = ApplicationController()
        
        invalid_fields = ['age (must be positive)', 'year_of_study (must be realistic)']
        error_text = controller.display_validation_errors(invalid_fields=invalid_fields)
        
        assert 'Validation Error' in error_text
        assert 'age (must be positive)' in error_text
        assert 'year_of_study (must be realistic)' in error_text
    
    def test_display_validation_errors_with_system_error(self):
        """Test display of system error messages."""
        controller = ApplicationController()
        
        error_message = "System Error: Knowledge base unavailable"
        error_text = controller.display_validation_errors(error_message=error_message)
        
        assert 'Validation Error' in error_text
        assert error_message in error_text
    
    def test_display_recommendations_with_empty_matches(self):
        """Test display of recommendations screen when no matches are found."""
        controller = ApplicationController()
        
        screen_text = controller.display_recommendations_screen([])
        
        assert 'Opportunity Recommendations' in screen_text
        assert 'couldn\'t find' in screen_text.lower() or 'no' in screen_text.lower()
        assert 'checking back' in screen_text.lower() or 'database' in screen_text.lower()
    
    def test_validate_field_values_with_negative_age(self):
        """Test field value validation with negative age."""
        controller = ApplicationController()
        
        profile = StudentProfile(
            name="Test",
            age=-5,
            education_level=EducationLevel.UG,
            degree="B.Tech",
            field_of_study="CS",
            year_of_study=2,
            institution_type=InstitutionType.GOVERNMENT,
            background_indicators=[BackgroundIndicator.RURAL],
            opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
            missed_opportunities_before=MissedOpportunityFrequency.NO,
        )
        
        invalid_fields = controller._validate_field_values(profile)
        
        assert len(invalid_fields) > 0
        assert any('age' in field for field in invalid_fields)
    
    def test_validate_field_values_with_unrealistic_year(self):
        """Test field value validation with unrealistic year of study."""
        controller = ApplicationController()
        
        profile = StudentProfile(
            name="Test",
            age=20,
            education_level=EducationLevel.UG,
            degree="B.Tech",
            field_of_study="CS",
            year_of_study=15,
            institution_type=InstitutionType.GOVERNMENT,
            background_indicators=[BackgroundIndicator.RURAL],
            opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
            missed_opportunities_before=MissedOpportunityFrequency.NO,
        )
        
        invalid_fields = controller._validate_field_values(profile)
        
        assert len(invalid_fields) > 0
        assert any('year_of_study' in field for field in invalid_fields)
    
    def test_no_matches_insight_generation(self):
        """Test generation of insight message when no opportunities match."""
        controller = ApplicationController()
        
        profile = StudentProfile(
            name="Test Student",
            age=20,
            education_level=EducationLevel.UG,
            degree="B.Tech",
            field_of_study="CS",
            year_of_study=2,
            institution_type=InstitutionType.GOVERNMENT,
            background_indicators=[BackgroundIndicator.RURAL],
            opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
            missed_opportunities_before=MissedOpportunityFrequency.NO,
        )
        
        insight = controller._generate_no_matches_insight(profile)
        
        assert profile.name in insight
        assert 'database' in insight.lower() or 'knowledge base' in insight.lower()
        assert 'checking back' in insight.lower() or 'later' in insight.lower()
