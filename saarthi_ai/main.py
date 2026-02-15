"""Main entry point for SaarthiAI application."""
from saarthi_ai.application_controller import ApplicationController
from saarthi_ai.models import (
    StudentProfile,
    EducationLevel,
    InstitutionType,
    BackgroundIndicator,
    OpportunityGoal,
    MissedOpportunityFrequency,
)


def collect_student_input() -> StudentProfile:
    """
    Collect student information through console input.
    
    Returns:
        StudentProfile with collected information
    """
    print("\n" + "="*64)
    print("STUDENT INFORMATION FORM")
    print("="*64 + "\n")
    
    # Required fields
    name = input("Name *: ").strip()
    
    age_str = input("Age *: ").strip()
    try:
        age = int(age_str)
    except ValueError:
        age = 0  # Will fail validation
    
    print("\nEducation Level * (choose one):")
    print("  1. Diploma")
    print("  2. UG (Undergraduate)")
    print("  3. PG (Postgraduate)")
    print("  4. PhD")
    edu_choice = input("Enter number: ").strip()
    education_level_map = {
        "1": EducationLevel.DIPLOMA,
        "2": EducationLevel.UG,
        "3": EducationLevel.PG,
        "4": EducationLevel.PHD,
    }
    education_level = education_level_map.get(edu_choice, EducationLevel.UG)
    
    degree = input("\nDegree (e.g., B.Tech, B.Sc, M.Sc) *: ").strip()
    field_of_study = input("Field of Study (e.g., Computer Science, Engineering) *: ").strip()
    
    year_str = input("Year of Study *: ").strip()
    try:
        year_of_study = int(year_str)
    except ValueError:
        year_of_study = 0  # Will fail validation
    
    print("\nInstitution Type * (choose one):")
    print("  1. Government")
    print("  2. Private")
    print("  3. Autonomous")
    print("  4. Open")
    inst_choice = input("Enter number: ").strip()
    institution_type_map = {
        "1": InstitutionType.GOVERNMENT,
        "2": InstitutionType.PRIVATE,
        "3": InstitutionType.AUTONOMOUS,
        "4": InstitutionType.OPEN,
    }
    institution_type = institution_type_map.get(inst_choice, InstitutionType.GOVERNMENT)
    
    print("\nBackground Indicators * (select all that apply, comma-separated):")
    print("  1. Rural")
    print("  2. First-generation")
    print("  3. Financial support")
    print("  4. Disabled")
    print("  5. Minority")
    bg_choices = input("Enter numbers (e.g., 1,3): ").strip()
    background_map = {
        "1": BackgroundIndicator.RURAL,
        "2": BackgroundIndicator.FIRST_GENERATION,
        "3": BackgroundIndicator.FINANCIAL_SUPPORT,
        "4": BackgroundIndicator.DISABLED,
        "5": BackgroundIndicator.MINORITY,
    }
    background_indicators = []
    if bg_choices:
        for choice in bg_choices.split(","):
            choice = choice.strip()
            if choice in background_map:
                background_indicators.append(background_map[choice])
    
    print("\nOpportunity Goals * (select all that apply, comma-separated):")
    print("  1. Scholarships")
    print("  2. Internships")
    print("  3. Research")
    print("  4. Skills")
    print("  5. Govt Exams")
    goal_choices = input("Enter numbers (e.g., 1,2): ").strip()
    goal_map = {
        "1": OpportunityGoal.SCHOLARSHIPS,
        "2": OpportunityGoal.INTERNSHIPS,
        "3": OpportunityGoal.RESEARCH,
        "4": OpportunityGoal.SKILLS,
        "5": OpportunityGoal.GOVT_EXAMS,
    }
    opportunity_goals = []
    if goal_choices:
        for choice in goal_choices.split(","):
            choice = choice.strip()
            if choice in goal_map:
                opportunity_goals.append(goal_map[choice])
    
    print("\nHave you missed opportunities before? * (choose one):")
    print("  1. Yes, many times")
    print("  2. Once or twice")
    print("  3. No")
    missed_choice = input("Enter number: ").strip()
    missed_map = {
        "1": MissedOpportunityFrequency.YES_MANY_TIMES,
        "2": MissedOpportunityFrequency.ONCE_OR_TWICE,
        "3": MissedOpportunityFrequency.NO,
    }
    missed_opportunities_before = missed_map.get(missed_choice, MissedOpportunityFrequency.NO)
    
    # Optional fields
    gender = input("\nGender (optional): ").strip() or None
    additional_context = input("Additional Context (optional): ").strip() or None
    
    return StudentProfile(
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
        additional_context=additional_context,
    )


def main():
    """Main application entry point."""
    # Initialize controller
    controller = ApplicationController()
    
    # Screen 1: Welcome
    controller.start()
    input()  # Wait for user to press Enter
    
    # Screen 2: Form
    controller.display_form_screen()
    profile = collect_student_input()
    
    # Handle form submission
    result = controller.handle_form_submission(profile)
    
    # Check validation
    if not result['valid']:
        if 'error' in result:
            # System error
            controller.display_validation_errors(error_message=result['error'])
        elif 'invalid_fields' in result:
            # Invalid field values
            controller.display_validation_errors(invalid_fields=result['invalid_fields'])
        else:
            # Missing required fields
            controller.display_validation_errors(missing_fields=result['missing_fields'])
        print("\nPlease restart the application and provide all required information.")
        return
    
    # Screen 3: Profile Understanding
    input("\nPress Enter to see your profile summary...")
    controller.display_profile_understanding_screen(result['profile_summary'])
    
    # Screen 4: Blindspot Analysis
    input("Press Enter to see your opportunity blindspots...")
    controller.display_blindspot_analysis_screen(result['blindspots'])
    
    # Screen 5: Recommendations
    input("Press Enter to see your personalized recommendations...")
    controller.display_recommendations_screen(result['matches'])
    
    # Screen 6: Final Insight
    input("Press Enter to see your final insight...")
    controller.display_final_insight_screen(result['final_insight'])
    
    print("\nThank you for using SaarthiAI!")


if __name__ == "__main__":
    main()
