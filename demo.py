"""Demo script for SaarthiAI application."""
from saarthi_ai.application_controller import ApplicationController
from saarthi_ai.models import (
    StudentProfile,
    EducationLevel,
    InstitutionType,
    BackgroundIndicator,
    OpportunityGoal,
    MissedOpportunityFrequency,
)


def demo_application():
    """Run a demonstration of the SaarthiAI application."""
    print("\n" + "="*70)
    print("SAARTHI AI - DEMONSTRATION")
    print("="*70 + "\n")
    
    # Initialize controller
    controller = ApplicationController()
    
    # Screen 1: Welcome
    print("SCREEN 1: WELCOME")
    print("-" * 70)
    controller.start()
    print("\n[User presses Enter]\n")
    
    # Screen 2: Form
    print("SCREEN 2: FORM")
    print("-" * 70)
    controller.display_form_screen()
    print("[User fills in the form...]\n")
    
    # Create a sample profile
    profile = StudentProfile(
        name="Priya Sharma",
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
            OpportunityGoal.INTERNSHIPS
        ],
        missed_opportunities_before=MissedOpportunityFrequency.YES_MANY_TIMES,
        gender="Female"
    )
    
    # Handle form submission
    result = controller.handle_form_submission(profile)
    
    if not result['valid']:
        print("ERROR: Form validation failed!")
        controller.display_validation_errors(result['missing_fields'])
        return
    
    print("[Form submitted successfully]\n")
    
    # Screen 3: Profile Understanding
    print("SCREEN 3: PROFILE UNDERSTANDING")
    print("-" * 70)
    controller.display_profile_understanding_screen(result['profile_summary'])
    print("[Automatically proceeding to next screen...]\n")
    
    # Screen 4: Blindspot Analysis
    print("SCREEN 4: BLINDSPOT ANALYSIS")
    print("-" * 70)
    controller.display_blindspot_analysis_screen(result['blindspots'])
    print("[Automatically proceeding to next screen...]\n")
    
    # Screen 5: Recommendations
    print("SCREEN 5: OPPORTUNITY RECOMMENDATIONS")
    print("-" * 70)
    controller.display_recommendations_screen(result['matches'])
    print("[Automatically proceeding to next screen...]\n")
    
    # Screen 6: Final Insight
    print("SCREEN 6: FINAL INSIGHT")
    print("-" * 70)
    controller.display_final_insight_screen(result['final_insight'])
    
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70 + "\n")
    
    # Print summary
    print("SUMMARY:")
    print(f"  • Profile analyzed: {profile.name}")
    print(f"  • Blindspots identified: {len(result['blindspots'])}")
    print(f"  • Opportunities recommended: {len(result['matches'])}")
    print(f"  • All screens displayed successfully!")
    print()


if __name__ == "__main__":
    demo_application()
