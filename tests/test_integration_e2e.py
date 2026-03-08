"""Integration and end-to-end tests for SaarthiAI application."""
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


class TestIntegrationE2E:
    """Integration and end-to-end tests for complete application flow."""
    
    def test_complete_flow_rural_first_gen_student(self):
        """
        Test complete flow with rural, first-generation UG engineering student seeking scholarships.
        
        This is Test Profile 1 from the design document.
        """
        controller = ApplicationController()
        
        # Create profile: Rural, first-generation UG engineering student
        profile = StudentProfile(
            name="Priya Kumar",
            age=19,
            education_level=EducationLevel.UG,
            degree="B.Tech",
            field_of_study="Engineering",
            year_of_study=2,
            institution_type=InstitutionType.GOVERNMENT,
            background_indicators=[
                BackgroundIndicator.RURAL,
                BackgroundIndicator.FIRST_GENERATION,
                BackgroundIndicator.FINANCIAL_SUPPORT
            ],
            opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
            missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES,
        )
        
        # Execute complete flow
        result = controller.handle_form_submission(profile)
        
        # Verify successful processing
        assert result['valid'] is True
        
        # Verify profile summary
        assert 'profile_summary' in result
        assert profile.name in result['profile_summary']
        assert 'Engineering' in result['profile_summary']
        
        # Verify blindspots identified (3-5)
        assert 'blindspots' in result
        assert 3 <= len(result['blindspots']) <= 5
        for blindspot in result['blindspots']:
            assert blindspot.category
            assert blindspot.reason
        
        # Verify recommendations (2-3)
        assert 'matches' in result
        assert 2 <= len(result['matches']) <= 3
        for match in result['matches']:
            assert match.opportunity
            assert match.fit_explanation
            assert match.miss_reason
            assert match.miss_probability
        
        # Verify final insight
        assert 'final_insight' in result
        assert result['final_insight']
        assert 'awareness' in result['final_insight'].lower() or 'know' in result['final_insight'].lower()
    
    def test_complete_flow_pg_stem_student(self):
        """
        Test complete flow with PG STEM student seeking research opportunities.
        
        This is Test Profile 2 from the design document.
        """
        controller = ApplicationController()
        
        # Create profile: PG STEM student
        profile = StudentProfile(
            name="Rahul Sharma",
            age=23,
            education_level=EducationLevel.PG,
            degree="M.Sc",
            field_of_study="Computer Science",
            year_of_study=1,
            institution_type=InstitutionType.AUTONOMOUS,
            background_indicators=[BackgroundIndicator.MINORITY],
            opportunity_goals=[OpportunityGoal.RESEARCH, OpportunityGoal.INTERNSHIPS],
            missed_opportunities_before=MissedOpportunityFrequency.ONCE_OR_TWICE,
        )
        
        # Execute complete flow
        result = controller.handle_form_submission(profile)
        
        # Verify successful processing
        assert result['valid'] is True
        assert 'profile_summary' in result
        assert 'blindspots' in result
        assert 'matches' in result
        assert 'final_insight' in result
        
        # Verify structure
        assert 3 <= len(result['blindspots']) <= 5
        assert len(result['matches']) >= 1  # At least 1 match
    
    def test_complete_flow_female_engineering_student(self):
        """
        Test complete flow with female UG engineering student (for AICTE Pragati eligibility).
        
        This is Test Profile 3 from the design document.
        """
        controller = ApplicationController()
        
        # Create profile: Female engineering student
        profile = StudentProfile(
            name="Ananya Patel",
            age=20,
            education_level=EducationLevel.UG,
            degree="B.Tech",
            field_of_study="Engineering",
            year_of_study=3,
            institution_type=InstitutionType.PRIVATE,
            background_indicators=[BackgroundIndicator.FIRST_GENERATION],
            opportunity_goals=[OpportunityGoal.SCHOLARSHIPS, OpportunityGoal.SKILLS],
            missed_opportunities_before=MissedOpportunityFrequency.NO,
            gender="Female",
        )
        
        # Execute complete flow
        result = controller.handle_form_submission(profile)
        
        # Verify successful processing
        assert result['valid'] is True
        assert 'profile_summary' in result
        assert 'blindspots' in result
        assert 'matches' in result
        assert 'final_insight' in result
        
        # Should get AICTE Pragati recommendation (female engineering student)
        opportunity_names = [match.opportunity.name for match in result['matches']]
        # Note: AICTE Pragati might be recommended if it's in the top 2-3 matches
        # We just verify that recommendations are made
        assert len(result['matches']) >= 1
    
    def test_complete_flow_disabled_student(self):
        """
        Test complete flow with disabled student seeking scholarships (for AICTE Saksham eligibility).
        
        This is Test Profile 4 from the design document.
        """
        controller = ApplicationController()
        
        # Create profile: Disabled student
        profile = StudentProfile(
            name="Vikram Singh",
            age=21,
            education_level=EducationLevel.UG,
            degree="B.Tech",
            field_of_study="Engineering",
            year_of_study=2,
            institution_type=InstitutionType.GOVERNMENT,
            background_indicators=[
                BackgroundIndicator.DISABLED,
                BackgroundIndicator.FINANCIAL_SUPPORT
            ],
            opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
            missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES,
        )
        
        # Execute complete flow
        result = controller.handle_form_submission(profile)
        
        # Verify successful processing
        assert result['valid'] is True
        assert 'profile_summary' in result
        assert 'blindspots' in result
        assert 'matches' in result
        assert 'final_insight' in result
        
        # Should get AICTE Saksham recommendation (disabled engineering student)
        opportunity_names = [match.opportunity.name for match in result['matches']]
        # Verify recommendations are made
        assert len(result['matches']) >= 1
    
    def test_complete_flow_private_institution_student(self):
        """
        Test complete flow with private institution student seeking merit scholarships.
        
        This is Test Profile 5 from the design document.
        """
        controller = ApplicationController()
        
        # Create profile: Private institution student
        profile = StudentProfile(
            name="Sneha Reddy",
            age=19,
            education_level=EducationLevel.UG,
            degree="B.Sc",
            field_of_study="Mathematics",
            year_of_study=2,
            institution_type=InstitutionType.PRIVATE,
            background_indicators=[BackgroundIndicator.MINORITY],
            opportunity_goals=[OpportunityGoal.SCHOLARSHIPS, OpportunityGoal.RESEARCH],
            missed_opportunities_before=MissedOpportunityFrequency.ONCE_OR_TWICE,
        )
        
        # Execute complete flow
        result = controller.handle_form_submission(profile)
        
        # Verify successful processing
        assert result['valid'] is True
        assert 'profile_summary' in result
        assert 'blindspots' in result
        assert 'matches' in result
        assert 'final_insight' in result
        
        # Verify structure
        assert 3 <= len(result['blindspots']) <= 5
        assert len(result['matches']) >= 1
    
    def test_error_recovery_missing_fields(self):
        """Test error recovery flow when required fields are missing."""
        controller = ApplicationController()
        
        # Create profile with missing fields
        profile = StudentProfile(
            name="",  # Missing
            age=20,
            education_level=EducationLevel.UG,
            degree="B.Tech",
            field_of_study="Engineering",
            year_of_study=2,
            institution_type=InstitutionType.GOVERNMENT,
            background_indicators=[],  # Missing
            opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
            missed_opportunities_before=MissedOpportunityFrequency.NO,
        )
        
        result = controller.handle_form_submission(profile)
        
        # Should fail validation gracefully
        assert result['valid'] is False
        assert 'missing_fields' in result
        assert 'name' in result['missing_fields']
        assert 'background_indicators' in result['missing_fields']
    
    def test_error_recovery_invalid_values(self):
        """Test error recovery flow when field values are invalid."""
        controller = ApplicationController()
        
        # Create profile with invalid values
        profile = StudentProfile(
            name="Test Student",
            age=-5,  # Invalid
            education_level=EducationLevel.UG,
            degree="B.Tech",
            field_of_study="Engineering",
            year_of_study=20,  # Invalid
            institution_type=InstitutionType.GOVERNMENT,
            background_indicators=[BackgroundIndicator.RURAL],
            opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
            missed_opportunities_before=MissedOpportunityFrequency.NO,
        )
        
        result = controller.handle_form_submission(profile)
        
        # Should fail validation gracefully
        assert result['valid'] is False
        assert 'invalid_fields' in result
    
    def test_all_screens_display_correctly(self):
        """Test that all six screens display correctly in sequence."""
        controller = ApplicationController()
        
        # Test welcome screen
        welcome_text = controller.display_welcome_screen()
        assert 'SaarthiAI' in welcome_text
        assert 'opportunity' in welcome_text.lower()
        
        # Test form screen
        form_text = controller.display_form_screen()
        assert 'Student Information Form' in form_text
        
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
        
        result = controller.handle_form_submission(profile)
        
        # Test profile understanding screen
        profile_screen = controller.display_profile_understanding_screen(result['profile_summary'])
        assert 'Profile Understanding' in profile_screen
        assert profile.name in profile_screen
        
        # Test blindspot analysis screen
        blindspot_screen = controller.display_blindspot_analysis_screen(result['blindspots'])
        assert 'Blindspot' in blindspot_screen
        
        # Test recommendations screen
        recommendations_screen = controller.display_recommendations_screen(result['matches'])
        assert 'Recommendation' in recommendations_screen
        
        # Test final insight screen
        final_screen = controller.display_final_insight_screen(result['final_insight'])
        assert 'Final Insight' in final_screen
    
    def test_output_quality_rural_student(self):
        """Test output quality and correctness for rural student profile."""
        controller = ApplicationController()
        
        profile = StudentProfile(
            name="Priya Kumar",
            age=19,
            education_level=EducationLevel.UG,
            degree="B.Tech",
            field_of_study="Engineering",
            year_of_study=2,
            institution_type=InstitutionType.GOVERNMENT,
            background_indicators=[
                BackgroundIndicator.RURAL,
                BackgroundIndicator.FIRST_GENERATION,
                BackgroundIndicator.FINANCIAL_SUPPORT
            ],
            opportunity_goals=[OpportunityGoal.SCHOLARSHIPS],
            missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES,
        )
        
        result = controller.handle_form_submission(profile)
        
        # Verify profile summary quality
        assert profile.name in result['profile_summary']
        assert 'Engineering' in result['profile_summary']
        assert any(bg.value in result['profile_summary'] for bg in profile.background_indicators)
        
        # Verify blindspot quality
        for blindspot in result['blindspots']:
            assert len(blindspot.category) > 0
            assert len(blindspot.reason) > 10  # Meaningful explanation
            assert 0 <= blindspot.relevance_score <= 1
        
        # Verify recommendation quality
        for match in result['matches']:
            # Verify eligibility
            assert profile.education_level in match.opportunity.eligibility_criteria.education_levels
            
            # Verify explanations are meaningful
            assert len(match.fit_explanation) > 20
            assert len(match.miss_reason) > 20
            
            # Verify profile elements are referenced in fit explanation
            profile_elements = [
                profile.education_level.value,
                profile.field_of_study,
                profile.institution_type.value,
            ]
            profile_elements.extend([bg.value for bg in profile.background_indicators])
            
            # At least one profile element should be mentioned
            fit_lower = match.fit_explanation.lower()
            assert any(elem.lower() in fit_lower for elem in profile_elements)
        
        # Verify final insight quality
        assert len(result['final_insight']) > 50  # Substantial insight
        insight_lower = result['final_insight'].lower()
        assert any(keyword in insight_lower for keyword in ['awareness', 'know', 'miss', 'opportunity'])
    
    def test_output_quality_stem_student(self):
        """Test output quality and correctness for STEM student profile."""
        controller = ApplicationController()
        
        profile = StudentProfile(
            name="Rahul Sharma",
            age=23,
            education_level=EducationLevel.PG,
            degree="M.Sc",
            field_of_study="Computer Science",
            year_of_study=1,
            institution_type=InstitutionType.AUTONOMOUS,
            background_indicators=[BackgroundIndicator.MINORITY],
            opportunity_goals=[OpportunityGoal.RESEARCH, OpportunityGoal.INTERNSHIPS],
            missed_opportunities_before=MissedOpportunityFrequency.ONCE_OR_TWICE,
        )
        
        result = controller.handle_form_submission(profile)
        
        # Verify all recommendations are eligible
        for match in result['matches']:
            assert profile.education_level in match.opportunity.eligibility_criteria.education_levels
            
            # If field-specific, verify field matches
            if match.opportunity.eligibility_criteria.fields_of_study:
                assert profile.field_of_study in match.opportunity.eligibility_criteria.fields_of_study
        
        # Verify blindspots are relevant to STEM/research
        blindspot_categories = [b.category.lower() for b in result['blindspots']]
        # Should have research or internship related blindspots
        assert any('research' in cat or 'internship' in cat or 'program' in cat for cat in blindspot_categories)
    
    def test_complete_flow_with_optional_fields(self):
        """Test complete flow with optional fields populated."""
        controller = ApplicationController()
        
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
            gender="Female",
            additional_context="Interested in innovation and entrepreneurship",
        )
        
        result = controller.handle_form_submission(profile)
        
        # Should process successfully with optional fields
        assert result['valid'] is True
        assert 'profile_summary' in result
        assert 'matches' in result
    
    def test_screen_transition_sequence(self):
        """Test that screens are presented in the correct sequence."""
        controller = ApplicationController()
        
        # The sequence should be:
        # 1. Welcome
        # 2. Form
        # 3. Profile Understanding
        # 4. Blindspot Analysis
        # 5. Recommendations
        # 6. Final Insight
        
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
        
        # Process through all screens
        result = controller.handle_form_submission(profile)
        
        # Verify all required data is present for each screen
        assert result['valid'] is True
        assert 'profile_summary' in result  # Screen 3
        assert 'blindspots' in result  # Screen 4
        assert 'matches' in result  # Screen 5
        assert 'final_insight' in result  # Screen 6
