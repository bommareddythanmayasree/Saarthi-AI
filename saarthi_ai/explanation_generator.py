"""Explanation generator component for SaarthiAI application."""
from saarthi_ai.models import StudentProfile, MissedOpportunityFrequency


class ExplanationGenerator:
    """Generates human-readable explanations for recommendations."""

    def generate_profile_summary(self, profile: StudentProfile) -> str:
        """
        Generate a bullet-point summary of the student's profile.

        Args:
            profile: The student profile to summarize

        Returns:
            A formatted string containing the profile summary
        """
        summary = f"Hi {profile.name}! I've understood your profile:\n\n"
        summary += f"• You're a {profile.year_of_study}-year {profile.education_level.value} student\n"
        summary += f"• Studying {profile.degree} in {profile.field_of_study}\n"
        summary += f"• At a {profile.institution_type.value} institution\n"

        if len(profile.background_indicators) > 0:
            background_str = ', '.join([indicator.value for indicator in profile.background_indicators])
            summary += f"• Background: {background_str}\n"

        goals_str = ', '.join([goal.value for goal in profile.opportunity_goals])
        summary += f"• Looking for: {goals_str}\n"

        return summary

    def generate_final_insight(self, profile, blindspots, matches) -> str:
        """
        Generate a final insight summary for the student.

        Creates a 3-4 sentence summary that:
        - Explains what kind of opportunities the student is missing
        - Emphasizes awareness as the main barrier
        - Includes a practical, motivating suggestion
        - Uses a positive and encouraging tone
        - Tailors suggestions based on missed_opportunities_before frequency

        Args:
            profile: The student profile (StudentProfile)
            blindspots: List of identified blindspots (List[Blindspot])
            matches: List of opportunity matches (List[OpportunityMatch])

        Returns:
            A formatted string containing the final insight (3-4 sentences)
        """
        insight = f"Based on your profile, you're likely missing out on "

        # Identify common theme from blindspots
        categories = [b.category for b in blindspots]
        category_str = ' '.join(categories).lower()

        # Determine what type of opportunities they're missing
        if "scholarship" in category_str:
            insight += "several scholarship opportunities that match your background. "
        elif "research" in category_str or "internship" in category_str:
            insight += "opportunities in research, internships, and programs beyond the classroom. "
        else:
            insight += "valuable opportunities that align with your goals and background. "

        # Emphasize awareness as the barrier (Requirement 6.3)
        insight += "The main barrier isn't your eligibility—it's simply not knowing these exist. "

        # Add motivating suggestion tailored to missed_opportunities_before (Requirement 6.4)
        if profile.missed_opportunities_before == MissedOpportunityFrequency.YES_MANY_TIMES:
            insight += "Start by exploring the recommendations above, and consider setting up alerts for similar programs. "
        elif profile.missed_opportunities_before == MissedOpportunityFrequency.ONCE_OR_TWICE:
            insight += "Take a moment to explore each recommendation—you're already eligible! "
        else:  # NO
            insight += "Now that you're aware, take action on these opportunities—you're already qualified! "

        # Closing motivational statement
        insight += "Awareness is the first step to opportunity."

        return insight

