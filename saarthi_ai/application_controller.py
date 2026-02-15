"""Application controller for SaarthiAI application."""
from typing import List
from saarthi_ai.models import StudentProfile
from saarthi_ai.profile_analyzer import ProfileAnalyzer
from saarthi_ai.blindspot_identifier import BlindspotIdentifier
from saarthi_ai.opportunity_matcher import OpportunityMatcher
from saarthi_ai.explanation_generator import ExplanationGenerator
from saarthi_ai.knowledge_base import get_all_opportunities


class ApplicationController:
    """Orchestrates the six-screen flow of the SaarthiAI application."""
    
    def __init__(self):
        """Initialize the application controller with all required components."""
        self.profile_analyzer = ProfileAnalyzer()
        self.blindspot_identifier = BlindspotIdentifier()
        self.opportunity_matcher = OpportunityMatcher()
        self.explanation_generator = ExplanationGenerator()
    
    def start(self) -> None:
        """
        Start the application by displaying the welcome screen.
        
        This method displays the welcome screen with the app name "SaarthiAI"
        and an explanation of the opportunity awareness gap.
        
        Requirements: 1.1
        """
        self.display_welcome_screen()
    
    def handle_form_submission(self, profile: StudentProfile) -> dict:
        """
        Handle form submission by validating input and orchestrating the flow.
        
        This method:
        1. Validates the student profile
        2. If valid, proceeds through all screens in sequence:
           - Profile Understanding
           - Blindspot Analysis
           - Opportunity Recommendations
           - Final Insight
        3. Returns all results for display
        
        Args:
            profile: The student profile from the form submission
            
        Returns:
            Dictionary containing:
            - 'valid': Boolean indicating if profile is valid
            - 'missing_fields': List of missing required fields (if invalid)
            - 'invalid_fields': List of invalid field values (if invalid)
            - 'profile_summary': Profile summary text (if valid)
            - 'blindspots': List of Blindspot objects (if valid)
            - 'matches': List of OpportunityMatch objects (if valid)
            - 'final_insight': Final insight text (if valid)
            - 'error': Error message (if system error occurs)
            
        Requirements: 1.5, 1.6, 7.1, 7.2, 7.3
        """
        # First validate field values (before checking for missing fields)
        invalid_fields = self._validate_field_values(profile)
        if invalid_fields:
            return {
                'valid': False,
                'invalid_fields': invalid_fields
            }
        
        # Then validate required fields
        is_valid, missing_fields = profile.validate()
        
        if not is_valid:
            return {
                'valid': False,
                'missing_fields': missing_fields
            }
        
        # Check if knowledge base is empty
        opportunities = get_all_opportunities()
        if not opportunities:
            return {
                'valid': False,
                'error': 'System Error: Opportunity knowledge base is currently unavailable. Please try again later.'
            }
        
        try:
            # Profile Understanding (Screen 3)
            analysis = self.profile_analyzer.analyze(profile)
            profile_summary = self.explanation_generator.generate_profile_summary(profile)
            
            # Fallback for empty profile summary
            if not profile_summary or not profile_summary.strip():
                profile_summary = self._generate_fallback_profile_summary(profile)
            
            # Blindspot Analysis (Screen 4)
            blindspots = self.blindspot_identifier.identify_blindspots(profile, analysis)
            
            # Fallback for empty blindspots
            if not blindspots:
                blindspots = self._generate_fallback_blindspots(profile)
            
            # Opportunity Recommendations (Screen 5)
            matches = self.opportunity_matcher.match_opportunities(profile, analysis, blindspots)
            
            # Handle no eligible opportunities scenario
            if not matches:
                return {
                    'valid': True,
                    'profile_summary': profile_summary,
                    'blindspots': blindspots,
                    'matches': [],
                    'final_insight': self._generate_no_matches_insight(profile),
                    'no_matches': True
                }
            
            # Final Insight (Screen 6)
            final_insight = self.explanation_generator.generate_final_insight(
                profile, blindspots, matches
            )
            
            # Fallback for empty final insight
            if not final_insight or not final_insight.strip():
                final_insight = self._generate_fallback_final_insight(profile, matches)
            
            return {
                'valid': True,
                'profile_summary': profile_summary,
                'blindspots': blindspots,
                'matches': matches,
                'final_insight': final_insight
            }
        
        except Exception as e:
            # Log the error (in production, use proper logging)
            print(f"Error during processing: {str(e)}")
            return {
                'valid': False,
                'error': 'An unexpected error occurred while processing your profile. Please try again.'
            }
    
    def _validate_field_values(self, profile: StudentProfile) -> List[str]:
        """
        Validate field values for correctness.
        
        Args:
            profile: The student profile to validate
            
        Returns:
            List of invalid field descriptions
        """
        invalid_fields = []
        
        # Validate age
        if profile.age is not None and profile.age < 0:
            invalid_fields.append("age (must be positive)")
        
        if profile.age is not None and profile.age > 150:
            invalid_fields.append("age (must be realistic)")
        
        # Validate year of study
        if profile.year_of_study is not None and profile.year_of_study < 0:
            invalid_fields.append("year_of_study (must be positive)")
        
        if profile.year_of_study is not None and profile.year_of_study > 10:
            invalid_fields.append("year_of_study (must be realistic)")
        
        return invalid_fields
    
    def _generate_fallback_profile_summary(self, profile: StudentProfile) -> str:
        """
        Generate a fallback profile summary using templates.
        
        Args:
            profile: The student profile
            
        Returns:
            Template-based profile summary
        """
        summary = f"Hi {profile.name}! I've understood your profile:\n\n"
        summary += f"• You're a {profile.year_of_study}-year {profile.education_level.value} student\n"
        summary += f"• Studying {profile.degree} in {profile.field_of_study}\n"
        summary += f"• At a {profile.institution_type.value} institution\n"
        
        if profile.background_indicators:
            bg_str = ', '.join([bg.value for bg in profile.background_indicators])
            summary += f"• Background: {bg_str}\n"
        
        if profile.opportunity_goals:
            goals_str = ', '.join([goal.value for goal in profile.opportunity_goals])
            summary += f"• Looking for: {goals_str}\n"
        
        return summary
    
    def _generate_fallback_blindspots(self, profile: StudentProfile) -> List:
        """
        Generate fallback blindspots using templates.
        
        Args:
            profile: The student profile
            
        Returns:
            List of basic Blindspot objects
        """
        from saarthi_ai.models import Blindspot
        
        blindspots = [
            Blindspot(
                category="Government Scholarships",
                reason="Many students don't know about government scholarships available for their profile",
                relevance_score=0.8
            ),
            Blindspot(
                category="Research and Internship Programs",
                reason="Students often focus on placements and miss research opportunities",
                relevance_score=0.7
            ),
            Blindspot(
                category="Skill Development Programs",
                reason="Skill programs are often buried in government websites with poor outreach",
                relevance_score=0.6
            )
        ]
        
        return blindspots
    
    def _generate_fallback_final_insight(self, profile: StudentProfile, matches: List) -> str:
        """
        Generate a fallback final insight using templates.
        
        Args:
            profile: The student profile
            matches: List of opportunity matches
            
        Returns:
            Template-based final insight
        """
        insight = f"Based on your profile, you're likely missing out on several opportunities that match your background. "
        insight += "The main barrier isn't your eligibility—it's simply not knowing these exist. "
        insight += "Take a moment to explore each recommendation—you're already eligible! "
        insight += "Awareness is the first step to opportunity."
        
        return insight
    
    def _generate_no_matches_insight(self, profile: StudentProfile) -> str:
        """
        Generate insight message when no opportunities match.
        
        Args:
            profile: The student profile
            
        Returns:
            Message explaining no current matches
        """
        insight = f"Hi {profile.name}, based on your current profile, we don't have specific opportunities "
        insight += "in our knowledge base that match your eligibility criteria right now. "
        insight += "This doesn't mean opportunities don't exist—it means our current database is limited. "
        insight += "We recommend checking back later as we continuously update our opportunity database. "
        insight += "In the meantime, explore the blindspot categories we identified—they can guide your own research!"
        
        return insight
    
    def display_welcome_screen(self) -> str:
        """
        Display the welcome screen with app name and explanation.
        
        Returns:
            The welcome screen text
            
        Requirements: 1.1
        """
        welcome_text = """
╔════════════════════════════════════════════════════════════════╗
║                         SaarthiAI                              ║
║              AI-Powered Opportunity Discovery                  ║
╚════════════════════════════════════════════════════════════════╝

Welcome to SaarthiAI!

Many students miss out on scholarships, internships, and programs they're 
eligible for—not because they don't qualify, but simply because they don't 
know these opportunities exist.

This is the "I don't know what I don't know" gap.

SaarthiAI helps you discover opportunities you're likely missing by:
• Understanding your unique profile
• Identifying your opportunity blindspots
• Recommending specific programs you're eligible for
• Explaining why you might have missed them

Let's discover what opportunities are waiting for you!

Press Enter to start...
"""
        print(welcome_text)
        return welcome_text
    
    def display_form_screen(self) -> str:
        """
        Display the student information form screen.
        
        Returns:
            The form screen text
            
        Requirements: 1.2, 1.3, 1.4
        """
        form_text = """
╔════════════════════════════════════════════════════════════════╗
║                   Student Information Form                     ║
╚════════════════════════════════════════════════════════════════╝

Please provide the following information so we can understand your profile
and identify relevant opportunities.

Required fields are marked with *

"""
        print(form_text)
        return form_text
    
    def display_validation_errors(self, missing_fields: List[str] = None, invalid_fields: List[str] = None, error_message: str = None) -> str:
        """
        Display validation errors for missing or invalid fields, or system errors.
        
        Args:
            missing_fields: List of field names that are missing (optional)
            invalid_fields: List of field descriptions that are invalid (optional)
            error_message: System error message (optional)
            
        Returns:
            The validation error text
            
        Requirements: 1.6
        """
        error_text = """
╔════════════════════════════════════════════════════════════════╗
║                      Validation Error                          ║
╚════════════════════════════════════════════════════════════════╝

"""
        
        if error_message:
            error_text += f"{error_message}\n\n"
        
        if missing_fields:
            error_text += "Please complete the following required fields:\n\n"
            for field in missing_fields:
                error_text += f"  • {field}\n"
            error_text += "\n"
        
        if invalid_fields:
            error_text += "Please correct the following invalid fields:\n\n"
            for field in invalid_fields:
                error_text += f"  • {field}\n"
            error_text += "\n"
        
        if missing_fields or invalid_fields:
            error_text += "Please fill in all required fields correctly and submit again.\n"
        
        print(error_text)
        return error_text
    
    def display_profile_understanding_screen(self, profile_summary: str) -> str:
        """
        Display the profile understanding screen.
        
        Args:
            profile_summary: The generated profile summary text
            
        Returns:
            The profile understanding screen text
            
        Requirements: 2.1, 2.2, 2.3, 7.2
        """
        screen_text = f"""
╔════════════════════════════════════════════════════════════════╗
║                   Profile Understanding                        ║
╚════════════════════════════════════════════════════════════════╝

{profile_summary}

Great! Now let me analyze what opportunities you might be missing...

"""
        print(screen_text)
        return screen_text
    
    def display_blindspot_analysis_screen(self, blindspots) -> str:
        """
        Display the blindspot analysis screen.
        
        Args:
            blindspots: List of Blindspot objects
            
        Returns:
            The blindspot analysis screen text
            
        Requirements: 3.1, 3.2, 3.4, 7.2
        """
        screen_text = """
╔════════════════════════════════════════════════════════════════╗
║                   Opportunity Blindspots                       ║
╚════════════════════════════════════════════════════════════════╝

Based on your profile, here are the types of opportunities you're likely 
missing:

"""
        for i, blindspot in enumerate(blindspots, 1):
            screen_text += f"{i}. {blindspot.category}\n"
            screen_text += f"   Why you might miss this: {blindspot.reason}\n\n"
        
        screen_text += "Now let me find specific opportunities for you...\n\n"
        
        print(screen_text)
        return screen_text
    
    def display_recommendations_screen(self, matches) -> str:
        """
        Display the opportunity recommendations screen.
        
        Args:
            matches: List of OpportunityMatch objects (can be empty)
            
        Returns:
            The recommendations screen text
            
        Requirements: 4.1, 4.2, 4.3, 4.4, 7.2
        """
        screen_text = """
╔════════════════════════════════════════════════════════════════╗
║                  Opportunity Recommendations                   ║
╚════════════════════════════════════════════════════════════════╝

"""
        
        if not matches:
            screen_text += """We couldn't find specific opportunities in our current database that match 
your eligibility criteria. This doesn't mean opportunities don't exist—our 
database is limited and continuously being updated.

We recommend:
• Checking back later as we add more opportunities
• Using the blindspot categories we identified to guide your own research
• Exploring government scholarship portals and your institution's resources

"""
        else:
            screen_text += """Here are specific opportunities you're eligible for but likely don't know 
about:

"""
            for i, match in enumerate(matches, 1):
                screen_text += f"{i}. {match.opportunity.name}\n"
                screen_text += f"   {match.opportunity.description}\n\n"
                screen_text += f"   Why it fits you: {match.fit_explanation}\n\n"
                screen_text += f"   Why you might have missed it: {match.miss_reason}\n\n"
                screen_text += f"   Miss Probability: {match.miss_probability.value}\n\n"
                screen_text += "   " + "─" * 60 + "\n\n"
        
        print(screen_text)
        return screen_text
    
    def display_final_insight_screen(self, final_insight: str) -> str:
        """
        Display the final insight screen.
        
        Args:
            final_insight: The generated final insight text
            
        Returns:
            The final insight screen text
            
        Requirements: 6.1, 6.2, 6.3, 6.4, 7.2
        """
        screen_text = f"""
╔════════════════════════════════════════════════════════════════╗
║                        Final Insight                           ║
╚════════════════════════════════════════════════════════════════╝

{final_insight}

Thank you for using SaarthiAI! We hope you discover opportunities that 
transform your journey.

"""
        print(screen_text)
        return screen_text
