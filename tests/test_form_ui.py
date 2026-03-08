"""Unit tests for form UI and input collection."""
import pytest
from unittest.mock import patch, MagicMock
from saarthi_ai.models import (
    StudentProfile,
    EducationLevel,
    InstitutionType,
    BackgroundIndicator,
    OpportunityGoal,
    MissedOpportunityFrequency,
)
from saarthi_ai.main import collect_student_input


class TestFormUI:
    """Test suite for form UI and input collection."""
    
    def test_collect_student_input_with_all_required_fields(self):
        """Test that form collects all required fields correctly."""
        # Mock user inputs for all required fields
        mock_inputs = [
            "Priya Sharma",  # name
            "20",  # age
            "2",  # education_level (UG)
            "B.Tech",  # degree
            "Computer Science",  # field_of_study
            "2",  # year_of_study
            "1",  # institution_type (Government)
            "1,3",  # background_indicators (Rural, Financial support)
            "1,2",  # opportunity_goals (Scholarships, Internships)
            "1",  # missed_opportunities_before (Yes many times)
            "Female",  # gender (optional)
            "I am interested in tech opportunities"  # additional_context (optional)
        ]
        
        with patch('builtins.input', side_effect=mock_inputs):
            profile = collect_student_input()
        
        # Verify all required fields are collected
        assert profile.name == "Priya Sharma"
        assert profile.age == 20
        assert profile.education_level == EducationLevel.UG
        assert profile.degree == "B.Tech"
        assert profile.field_of_study == "Computer Science"
        assert profile.year_of_study == 2
        assert profile.institution_type == InstitutionType.GOVERNMENT
        assert BackgroundIndicator.RURAL in profile.background_indicators
        assert BackgroundIndicator.FINANCIAL_SUPPORT in profile.background_indicators
        assert OpportunityGoal.SCHOLARSHIPS in profile.opportunity_goals
        assert OpportunityGoal.INTERNSHIPS in profile.opportunity_goals
        assert profile.missed_opportunities_before == MissedOpportunityFrequency.YES_MANY_TIMES
        
        # Verify optional fields are collected
        assert profile.gender == "Female"
        assert profile.additional_context == "I am interested in tech opportunities"
    
    def test_collect_student_input_with_only_required_fields(self):
        """Test that form works with only required fields (optional fields empty)."""
        # Mock user inputs with empty optional fields
        mock_inputs = [
            "Rahul Kumar",  # name
            "21",  # age
            "2",  # education_level (UG)
            "B.E.",  # degree
            "Engineering",  # field_of_study
            "3",  # year_of_study
            "2",  # institution_type (Private)
            "2",  # background_indicators (First-generation)
            "1",  # opportunity_goals (Scholarships)
            "2",  # missed_opportunities_before (Once or twice)
            "",  # gender (empty)
            ""  # additional_context (empty)
        ]
        
        with patch('builtins.input', side_effect=mock_inputs):
            profile = collect_student_input()
        
        # Verify required fields are collected
        assert profile.name == "Rahul Kumar"
        assert profile.age == 21
        assert profile.education_level == EducationLevel.UG
        assert profile.degree == "B.E."
        assert profile.field_of_study == "Engineering"
        assert profile.year_of_study == 3
        assert profile.institution_type == InstitutionType.PRIVATE
        assert BackgroundIndicator.FIRST_GENERATION in profile.background_indicators
        assert OpportunityGoal.SCHOLARSHIPS in profile.opportunity_goals
        assert profile.missed_opportunities_before == MissedOpportunityFrequency.ONCE_OR_TWICE
        
        # Verify optional fields are None
        assert profile.gender is None
        assert profile.additional_context is None
    
    def test_collect_student_input_with_multiple_background_indicators(self):
        """Test that form correctly handles multiple background indicators."""
        mock_inputs = [
            "Test Student",  # name
            "20",  # age
            "2",  # education_level (UG)
            "B.Sc",  # degree
            "Physics",  # field_of_study
            "2",  # year_of_study
            "1",  # institution_type (Government)
            "1,2,3,4,5",  # background_indicators (all options)
            "1",  # opportunity_goals (Scholarships)
            "3",  # missed_opportunities_before (No)
            "",  # gender
            ""  # additional_context
        ]
        
        with patch('builtins.input', side_effect=mock_inputs):
            profile = collect_student_input()
        
        # Verify all background indicators are collected
        assert len(profile.background_indicators) == 5
        assert BackgroundIndicator.RURAL in profile.background_indicators
        assert BackgroundIndicator.FIRST_GENERATION in profile.background_indicators
        assert BackgroundIndicator.FINANCIAL_SUPPORT in profile.background_indicators
        assert BackgroundIndicator.DISABLED in profile.background_indicators
        assert BackgroundIndicator.MINORITY in profile.background_indicators
    
    def test_collect_student_input_with_multiple_opportunity_goals(self):
        """Test that form correctly handles multiple opportunity goals."""
        mock_inputs = [
            "Test Student",  # name
            "20",  # age
            "2",  # education_level (UG)
            "B.Tech",  # degree
            "Computer Science",  # field_of_study
            "2",  # year_of_study
            "1",  # institution_type (Government)
            "1",  # background_indicators (Rural)
            "1,2,3,4,5",  # opportunity_goals (all options)
            "3",  # missed_opportunities_before (No)
            "",  # gender
            ""  # additional_context
        ]
        
        with patch('builtins.input', side_effect=mock_inputs):
            profile = collect_student_input()
        
        # Verify all opportunity goals are collected
        assert len(profile.opportunity_goals) == 5
        assert OpportunityGoal.SCHOLARSHIPS in profile.opportunity_goals
        assert OpportunityGoal.INTERNSHIPS in profile.opportunity_goals
        assert OpportunityGoal.RESEARCH in profile.opportunity_goals
        assert OpportunityGoal.SKILLS in profile.opportunity_goals
        assert OpportunityGoal.GOVT_EXAMS in profile.opportunity_goals
    
    def test_collect_student_input_with_different_education_levels(self):
        """Test that form handles all education level options."""
        education_levels = [
            ("1", EducationLevel.DIPLOMA),
            ("2", EducationLevel.UG),
            ("3", EducationLevel.PG),
            ("4", EducationLevel.PHD),
        ]
        
        for choice, expected_level in education_levels:
            mock_inputs = [
                "Test Student",  # name
                "20",  # age
                choice,  # education_level
                "B.Tech",  # degree
                "Computer Science",  # field_of_study
                "2",  # year_of_study
                "1",  # institution_type
                "1",  # background_indicators
                "1",  # opportunity_goals
                "3",  # missed_opportunities_before
                "",  # gender
                ""  # additional_context
            ]
            
            with patch('builtins.input', side_effect=mock_inputs):
                profile = collect_student_input()
            
            assert profile.education_level == expected_level
    
    def test_collect_student_input_with_different_institution_types(self):
        """Test that form handles all institution type options."""
        institution_types = [
            ("1", InstitutionType.GOVERNMENT),
            ("2", InstitutionType.PRIVATE),
            ("3", InstitutionType.AUTONOMOUS),
            ("4", InstitutionType.OPEN),
        ]
        
        for choice, expected_type in institution_types:
            mock_inputs = [
                "Test Student",  # name
                "20",  # age
                "2",  # education_level
                "B.Tech",  # degree
                "Computer Science",  # field_of_study
                "2",  # year_of_study
                choice,  # institution_type
                "1",  # background_indicators
                "1",  # opportunity_goals
                "3",  # missed_opportunities_before
                "",  # gender
                ""  # additional_context
            ]
            
            with patch('builtins.input', side_effect=mock_inputs):
                profile = collect_student_input()
            
            assert profile.institution_type == expected_type
    
    def test_collect_student_input_with_different_missed_opportunity_frequencies(self):
        """Test that form handles all missed opportunity frequency options."""
        frequencies = [
            ("1", MissedOpportunityFrequency.YES_MANY_TIMES),
            ("2", MissedOpportunityFrequency.ONCE_OR_TWICE),
            ("3", MissedOpportunityFrequency.NO),
        ]
        
        for choice, expected_frequency in frequencies:
            mock_inputs = [
                "Test Student",  # name
                "20",  # age
                "2",  # education_level
                "B.Tech",  # degree
                "Computer Science",  # field_of_study
                "2",  # year_of_study
                "1",  # institution_type
                "1",  # background_indicators
                "1",  # opportunity_goals
                choice,  # missed_opportunities_before
                "",  # gender
                ""  # additional_context
            ]
            
            with patch('builtins.input', side_effect=mock_inputs):
                profile = collect_student_input()
            
            assert profile.missed_opportunities_before == expected_frequency
    
    def test_collect_student_input_handles_invalid_age(self):
        """Test that form handles invalid age input gracefully."""
        mock_inputs = [
            "Test Student",  # name
            "invalid",  # age (invalid)
            "2",  # education_level
            "B.Tech",  # degree
            "Computer Science",  # field_of_study
            "2",  # year_of_study
            "1",  # institution_type
            "1",  # background_indicators
            "1",  # opportunity_goals
            "3",  # missed_opportunities_before
            "",  # gender
            ""  # additional_context
        ]
        
        with patch('builtins.input', side_effect=mock_inputs):
            profile = collect_student_input()
        
        # Invalid age should result in 0, which will fail validation
        assert profile.age == 0
        
        # Verify validation catches this
        is_valid, missing_fields = profile.validate()
        assert not is_valid
        assert 'age' in missing_fields
    
    def test_collect_student_input_handles_invalid_year_of_study(self):
        """Test that form handles invalid year of study input gracefully."""
        mock_inputs = [
            "Test Student",  # name
            "20",  # age
            "2",  # education_level
            "B.Tech",  # degree
            "Computer Science",  # field_of_study
            "invalid",  # year_of_study (invalid)
            "1",  # institution_type
            "1",  # background_indicators
            "1",  # opportunity_goals
            "3",  # missed_opportunities_before
            "",  # gender
            ""  # additional_context
        ]
        
        with patch('builtins.input', side_effect=mock_inputs):
            profile = collect_student_input()
        
        # Invalid year should result in 0, which will fail validation
        assert profile.year_of_study == 0
        
        # Verify validation catches this
        is_valid, missing_fields = profile.validate()
        assert not is_valid
        assert 'year_of_study' in missing_fields
    
    def test_collect_student_input_handles_empty_name(self):
        """Test that form handles empty name input."""
        mock_inputs = [
            "",  # name (empty)
            "20",  # age
            "2",  # education_level
            "B.Tech",  # degree
            "Computer Science",  # field_of_study
            "2",  # year_of_study
            "1",  # institution_type
            "1",  # background_indicators
            "1",  # opportunity_goals
            "3",  # missed_opportunities_before
            "",  # gender
            ""  # additional_context
        ]
        
        with patch('builtins.input', side_effect=mock_inputs):
            profile = collect_student_input()
        
        # Empty name should be stored as empty string
        assert profile.name == ""
        
        # Verify validation catches this
        is_valid, missing_fields = profile.validate()
        assert not is_valid
        assert 'name' in missing_fields
    
    def test_collect_student_input_handles_whitespace_only_fields(self):
        """Test that form handles whitespace-only input in text fields."""
        mock_inputs = [
            "   ",  # name (whitespace only)
            "20",  # age
            "2",  # education_level
            "   ",  # degree (whitespace only)
            "   ",  # field_of_study (whitespace only)
            "2",  # year_of_study
            "1",  # institution_type
            "1",  # background_indicators
            "1",  # opportunity_goals
            "3",  # missed_opportunities_before
            "",  # gender
            ""  # additional_context
        ]
        
        with patch('builtins.input', side_effect=mock_inputs):
            profile = collect_student_input()
        
        # Whitespace should be stripped, resulting in empty strings
        assert profile.name == ""
        assert profile.degree == ""
        assert profile.field_of_study == ""
        
        # Verify validation catches these
        is_valid, missing_fields = profile.validate()
        assert not is_valid
        assert 'name' in missing_fields
        assert 'degree' in missing_fields
        assert 'field_of_study' in missing_fields
    
    def test_collect_student_input_handles_invalid_enum_choices(self):
        """Test that form handles invalid enum choices with defaults."""
        mock_inputs = [
            "Test Student",  # name
            "20",  # age
            "99",  # education_level (invalid choice, should default to UG)
            "B.Tech",  # degree
            "Computer Science",  # field_of_study
            "2",  # year_of_study
            "99",  # institution_type (invalid choice, should default to Government)
            "1",  # background_indicators
            "1",  # opportunity_goals
            "99",  # missed_opportunities_before (invalid choice, should default to No)
            "",  # gender
            ""  # additional_context
        ]
        
        with patch('builtins.input', side_effect=mock_inputs):
            profile = collect_student_input()
        
        # Invalid choices should use defaults
        assert profile.education_level == EducationLevel.UG
        assert profile.institution_type == InstitutionType.GOVERNMENT
        assert profile.missed_opportunities_before == MissedOpportunityFrequency.NO
    
    def test_collect_student_input_handles_empty_background_indicators(self):
        """Test that form handles empty background indicators input."""
        mock_inputs = [
            "Test Student",  # name
            "20",  # age
            "2",  # education_level
            "B.Tech",  # degree
            "Computer Science",  # field_of_study
            "2",  # year_of_study
            "1",  # institution_type
            "",  # background_indicators (empty)
            "1",  # opportunity_goals
            "3",  # missed_opportunities_before
            "",  # gender
            ""  # additional_context
        ]
        
        with patch('builtins.input', side_effect=mock_inputs):
            profile = collect_student_input()
        
        # Empty background indicators should result in empty list
        assert profile.background_indicators == []
        
        # Verify validation catches this
        is_valid, missing_fields = profile.validate()
        assert not is_valid
        assert 'background_indicators' in missing_fields
    
    def test_collect_student_input_handles_empty_opportunity_goals(self):
        """Test that form handles empty opportunity goals input."""
        mock_inputs = [
            "Test Student",  # name
            "20",  # age
            "2",  # education_level
            "B.Tech",  # degree
            "Computer Science",  # field_of_study
            "2",  # year_of_study
            "1",  # institution_type
            "1",  # background_indicators
            "",  # opportunity_goals (empty)
            "3",  # missed_opportunities_before
            "",  # gender
            ""  # additional_context
        ]
        
        with patch('builtins.input', side_effect=mock_inputs):
            profile = collect_student_input()
        
        # Empty opportunity goals should result in empty list
        assert profile.opportunity_goals == []
        
        # Verify validation catches this
        is_valid, missing_fields = profile.validate()
        assert not is_valid
        assert 'opportunity_goals' in missing_fields
    
    def test_collect_student_input_handles_invalid_background_indicator_choices(self):
        """Test that form ignores invalid background indicator choices."""
        mock_inputs = [
            "Test Student",  # name
            "20",  # age
            "2",  # education_level
            "B.Tech",  # degree
            "Computer Science",  # field_of_study
            "2",  # year_of_study
            "1",  # institution_type
            "1,99,2",  # background_indicators (99 is invalid)
            "1",  # opportunity_goals
            "3",  # missed_opportunities_before
            "",  # gender
            ""  # additional_context
        ]
        
        with patch('builtins.input', side_effect=mock_inputs):
            profile = collect_student_input()
        
        # Should only include valid choices (1 and 2)
        assert len(profile.background_indicators) == 2
        assert BackgroundIndicator.RURAL in profile.background_indicators
        assert BackgroundIndicator.FIRST_GENERATION in profile.background_indicators
    
    def test_collect_student_input_handles_invalid_opportunity_goal_choices(self):
        """Test that form ignores invalid opportunity goal choices."""
        mock_inputs = [
            "Test Student",  # name
            "20",  # age
            "2",  # education_level
            "B.Tech",  # degree
            "Computer Science",  # field_of_study
            "2",  # year_of_study
            "1",  # institution_type
            "1",  # background_indicators
            "1,99,2",  # opportunity_goals (99 is invalid)
            "3",  # missed_opportunities_before
            "",  # gender
            ""  # additional_context
        ]
        
        with patch('builtins.input', side_effect=mock_inputs):
            profile = collect_student_input()
        
        # Should only include valid choices (1 and 2)
        assert len(profile.opportunity_goals) == 2
        assert OpportunityGoal.SCHOLARSHIPS in profile.opportunity_goals
        assert OpportunityGoal.INTERNSHIPS in profile.opportunity_goals
    
    def test_form_displays_required_field_markers(self):
        """Test that form displays asterisks for required fields."""
        mock_inputs = [
            "Test Student",  # name
            "20",  # age
            "2",  # education_level
            "B.Tech",  # degree
            "Computer Science",  # field_of_study
            "2",  # year_of_study
            "1",  # institution_type
            "1",  # background_indicators
            "1",  # opportunity_goals
            "3",  # missed_opportunities_before
            "",  # gender
            ""  # additional_context
        ]
        
        # Capture print output to verify form displays required field markers
        with patch('builtins.input', side_effect=mock_inputs):
            with patch('builtins.print') as mock_print:
                profile = collect_student_input()
                
                # Check that print was called (form was displayed)
                assert mock_print.called
                
                # Get all print calls
                print_calls = [str(call) for call in mock_print.call_args_list]
                print_output = ' '.join(print_calls)
                
                # Verify required field markers are present
                assert '*' in print_output or 'required' in print_output.lower()
    
    def test_form_validation_integration(self):
        """Test that form collection integrates with validation correctly."""
        # Test with valid complete profile
        valid_inputs = [
            "Priya Sharma",  # name
            "20",  # age
            "2",  # education_level
            "B.Tech",  # degree
            "Computer Science",  # field_of_study
            "2",  # year_of_study
            "1",  # institution_type
            "1",  # background_indicators
            "1",  # opportunity_goals
            "1",  # missed_opportunities_before
            "Female",  # gender
            ""  # additional_context
        ]
        
        with patch('builtins.input', side_effect=valid_inputs):
            profile = collect_student_input()
        
        # Verify profile passes validation
        is_valid, missing_fields = profile.validate()
        assert is_valid
        assert len(missing_fields) == 0
        
        # Test with invalid incomplete profile
        invalid_inputs = [
            "",  # name (empty)
            "invalid",  # age (invalid)
            "2",  # education_level
            "",  # degree (empty)
            "",  # field_of_study (empty)
            "invalid",  # year_of_study (invalid)
            "1",  # institution_type
            "",  # background_indicators (empty)
            "",  # opportunity_goals (empty)
            "3",  # missed_opportunities_before
            "",  # gender
            ""  # additional_context
        ]
        
        with patch('builtins.input', side_effect=invalid_inputs):
            profile = collect_student_input()
        
        # Verify profile fails validation
        is_valid, missing_fields = profile.validate()
        assert not is_valid
        assert len(missing_fields) > 0
        
        # Verify all expected missing fields are reported
        expected_missing = ['name', 'age', 'degree', 'field_of_study', 
                          'year_of_study', 'background_indicators', 'opportunity_goals']
        for field in expected_missing:
            assert field in missing_fields


class TestFormUIRequirements:
    """Test suite specifically for task 10 requirements."""
    
    def test_requirement_1_3_collects_all_required_fields(self):
        """
        Test Requirement 1.3: Form collects all required fields.
        
        Required fields: name, age, education_level, degree, field_of_study,
        year_of_study, institution_type, background_indicators, opportunity_goals,
        missed_opportunities_before
        """
        mock_inputs = [
            "Test Student",  # name
            "20",  # age
            "2",  # education_level
            "B.Tech",  # degree
            "Computer Science",  # field_of_study
            "2",  # year_of_study
            "1",  # institution_type
            "1",  # background_indicators
            "1",  # opportunity_goals
            "3",  # missed_opportunities_before
            "",  # gender
            ""  # additional_context
        ]
        
        with patch('builtins.input', side_effect=mock_inputs):
            profile = collect_student_input()
        
        # Verify all required fields are present
        assert profile.name is not None
        assert profile.age is not None
        assert profile.education_level is not None
        assert profile.degree is not None
        assert profile.field_of_study is not None
        assert profile.year_of_study is not None
        assert profile.institution_type is not None
        assert profile.background_indicators is not None
        assert profile.opportunity_goals is not None
        assert profile.missed_opportunities_before is not None
    
    def test_requirement_1_4_collects_optional_fields(self):
        """
        Test Requirement 1.4: Form collects optional fields.
        
        Optional fields: gender, additional_context
        """
        mock_inputs = [
            "Test Student",  # name
            "20",  # age
            "2",  # education_level
            "B.Tech",  # degree
            "Computer Science",  # field_of_study
            "2",  # year_of_study
            "1",  # institution_type
            "1",  # background_indicators
            "1",  # opportunity_goals
            "3",  # missed_opportunities_before
            "Female",  # gender (optional)
            "I am interested in AI"  # additional_context (optional)
        ]
        
        with patch('builtins.input', side_effect=mock_inputs):
            profile = collect_student_input()
        
        # Verify optional fields are collected
        assert profile.gender == "Female"
        assert profile.additional_context == "I am interested in AI"
    
    def test_requirement_1_5_accepts_complete_submission(self):
        """
        Test Requirement 1.5: Form accepts submission with all required fields.
        """
        mock_inputs = [
            "Test Student",  # name
            "20",  # age
            "2",  # education_level
            "B.Tech",  # degree
            "Computer Science",  # field_of_study
            "2",  # year_of_study
            "1",  # institution_type
            "1",  # background_indicators
            "1",  # opportunity_goals
            "3",  # missed_opportunities_before
            "",  # gender
            ""  # additional_context
        ]
        
        with patch('builtins.input', side_effect=mock_inputs):
            profile = collect_student_input()
        
        # Verify profile is valid
        is_valid, missing_fields = profile.validate()
        assert is_valid
        assert len(missing_fields) == 0
    
    def test_requirement_1_6_prevents_incomplete_submission(self):
        """
        Test Requirement 1.6: Form validation prevents submission with missing fields
        and indicates which fields are required.
        """
        # Create profile with missing fields
        mock_inputs = [
            "",  # name (missing)
            "20",  # age
            "2",  # education_level
            "",  # degree (missing)
            "Computer Science",  # field_of_study
            "2",  # year_of_study
            "1",  # institution_type
            "",  # background_indicators (missing)
            "1",  # opportunity_goals
            "3",  # missed_opportunities_before
            "",  # gender
            ""  # additional_context
        ]
        
        with patch('builtins.input', side_effect=mock_inputs):
            profile = collect_student_input()
        
        # Verify profile is invalid
        is_valid, missing_fields = profile.validate()
        assert not is_valid
        
        # Verify specific missing fields are indicated
        assert 'name' in missing_fields
        assert 'degree' in missing_fields
        assert 'background_indicators' in missing_fields
        
        # Verify the validation provides specific field information
        assert len(missing_fields) > 0
        for field in missing_fields:
            assert isinstance(field, str)
            assert len(field) > 0
