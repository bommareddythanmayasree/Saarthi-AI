"""Opportunity matcher component for SaarthiAI application."""
from typing import List
from saarthi_ai.models import (
    StudentProfile,
    ProfileAnalysis,
    Blindspot,
    Opportunity,
    OpportunityMatch,
    EligibilityCriteria,
    MissProbability,
    AwarenessLevel,
    VisibilityLevel,
    BackgroundIndicator,
    OpportunityGoal
)
from saarthi_ai.knowledge_base import get_all_opportunities


class OpportunityMatcher:
    """Matches student profiles to specific opportunities from the knowledge base."""
    
    def match_opportunities(
        self,
        profile: StudentProfile,
        analysis: ProfileAnalysis,
        blindspots: List[Blindspot]
    ) -> List[OpportunityMatch]:
        """
        Match student profile to opportunities from the knowledge base.
        
        Args:
            profile: The student profile
            analysis: The profile analysis
            blindspots: The identified blindspots
            
        Returns:
            List of 2-3 OpportunityMatch objects with explanations and miss probability
        """
        # First pass: collect all eligible opportunities with their scores
        all_eligible_matches = []
        opportunities = get_all_opportunities()
        
        for opportunity in opportunities:
            # Check eligibility
            if not self.is_eligible(profile, opportunity.eligibility_criteria):
                continue
            
            # Calculate blindspot alignment
            blindspot_alignment = self._calculate_blindspot_alignment(opportunity, blindspots)
            
            # Calculate relevance score
            relevance = self._calculate_relevance(
                profile, analysis, opportunity, blindspot_alignment
            )
            
            # Generate explanations
            fit_explanation = self._generate_fit_explanation(profile, opportunity)
            miss_reason = self._generate_miss_reason(opportunity, analysis.awareness_level)
            miss_probability = self.calculate_miss_probability(
                opportunity.visibility_level, analysis.awareness_level
            )
            
            all_eligible_matches.append(OpportunityMatch(
                opportunity=opportunity,
                fit_explanation=fit_explanation,
                miss_reason=miss_reason,
                miss_probability=miss_probability,
                relevance_score=relevance
            ))
        
        # Sort by relevance score (descending)
        all_eligible_matches.sort(key=lambda m: m.relevance_score, reverse=True)
        
        # If we have fewer than 2 eligible matches, return all we have
        # This can happen with very specific profiles (e.g., Diploma students)
        if len(all_eligible_matches) < 2:
            return all_eligible_matches
        
        # Return top 2-3 matches
        return all_eligible_matches[:min(3, len(all_eligible_matches))]
    
    def is_eligible(
        self,
        profile: StudentProfile,
        criteria: EligibilityCriteria
    ) -> bool:
        """
        Check if a student profile meets eligibility criteria.
        
        Args:
            profile: The student profile
            criteria: The eligibility criteria to check
            
        Returns:
            True if the profile meets all criteria, False otherwise
        """
        # Check education level
        if profile.education_level not in criteria.education_levels:
            return False
        
        # Check field of study (if specified)
        if criteria.fields_of_study is not None:
            if profile.field_of_study not in criteria.fields_of_study:
                return False
        
        # Check institution type (if specified)
        if criteria.institution_types is not None:
            if profile.institution_type not in criteria.institution_types:
                return False
        
        # Check background requirements (if specified)
        if criteria.background_requirements is not None:
            # Student must have at least one of the required background indicators
            if not any(req in profile.background_indicators for req in criteria.background_requirements):
                return False
        
        return True
    
    def calculate_miss_probability(
        self,
        visibility_level: VisibilityLevel,
        awareness_level: AwarenessLevel
    ) -> MissProbability:
        """
        Calculate miss probability based on visibility and awareness levels.
        
        Args:
            visibility_level: The opportunity's visibility level
            awareness_level: The student's awareness level
            
        Returns:
            Miss probability rating (High, Medium, or Low)
        """
        # Low visibility opportunities have high miss probability
        if visibility_level == VisibilityLevel.LOW:
            return MissProbability.HIGH
        
        # Students with low awareness miss medium visibility opportunities
        if visibility_level == VisibilityLevel.MEDIUM:
            if awareness_level == AwarenessLevel.LOW:
                return MissProbability.HIGH
            elif awareness_level == AwarenessLevel.MEDIUM:
                return MissProbability.MEDIUM
            else:  # HIGH awareness
                return MissProbability.LOW
        
        # High visibility opportunities
        if awareness_level == AwarenessLevel.LOW:
            return MissProbability.MEDIUM
        else:
            return MissProbability.LOW
    
    def _calculate_blindspot_alignment(
        self,
        opportunity: Opportunity,
        blindspots: List[Blindspot]
    ) -> float:
        """
        Calculate how well an opportunity aligns with identified blindspots.
        
        Args:
            opportunity: The opportunity to check
            blindspots: The list of identified blindspots
            
        Returns:
            Alignment score between 0 and 1
        """
        max_alignment = 0.0
        
        # Check if opportunity category appears in any blindspot category
        for blindspot in blindspots:
            category_lower = blindspot.category.lower()
            opp_category_lower = opportunity.category.lower()
            opp_name_lower = opportunity.name.lower()
            
            # Direct category match
            if opp_category_lower in category_lower:
                max_alignment = max(max_alignment, blindspot.relevance_score)
            
            # Check for keyword matches
            if "scholarship" in category_lower and opp_category_lower == "scholarship":
                max_alignment = max(max_alignment, blindspot.relevance_score)
            
            if "research" in category_lower and opp_category_lower == "internship":
                max_alignment = max(max_alignment, blindspot.relevance_score * 0.9)
            
            if "innovation" in category_lower and opp_category_lower == "program":
                max_alignment = max(max_alignment, blindspot.relevance_score * 0.9)
            
            if "internship" in category_lower and opp_category_lower == "internship":
                max_alignment = max(max_alignment, blindspot.relevance_score)
            
            if "program" in category_lower and opp_category_lower == "program":
                max_alignment = max(max_alignment, blindspot.relevance_score)
            
            # Check for specific program mentions
            if "aicte" in opp_name_lower and "category-specific" in category_lower:
                max_alignment = max(max_alignment, blindspot.relevance_score)
            
            if "central" in opp_name_lower and "income-based" in category_lower:
                max_alignment = max(max_alignment, blindspot.relevance_score)
            
            if "state" in opp_name_lower and "state" in category_lower:
                max_alignment = max(max_alignment, blindspot.relevance_score)
            
            if "nptel" in opp_name_lower and "research" in category_lower:
                max_alignment = max(max_alignment, blindspot.relevance_score)
            
            if "ministry" in opp_name_lower and "innovation" in category_lower:
                max_alignment = max(max_alignment, blindspot.relevance_score)
            
            # Broader matches for better coverage
            if "skill" in category_lower and opp_category_lower == "program":
                max_alignment = max(max_alignment, blindspot.relevance_score * 0.7)
            
            if "merit" in category_lower and opportunity.eligibility_criteria.merit_based:
                max_alignment = max(max_alignment, blindspot.relevance_score * 0.8)
        
        # If no strong alignment found, return a base score to ensure some opportunities pass through
        # This ensures we can always return at least 2-3 matches for eligible students
        return max(max_alignment, 0.3)
    
    def _calculate_relevance(
        self,
        profile: StudentProfile,
        analysis: ProfileAnalysis,
        opportunity: Opportunity,
        blindspot_alignment: float
    ) -> float:
        """
        Calculate overall relevance score for an opportunity.
        
        Args:
            profile: The student profile
            analysis: The profile analysis
            opportunity: The opportunity
            blindspot_alignment: The blindspot alignment score
            
        Returns:
            Relevance score between 0 and 1
        """
        score = 0.0
        
        # Blindspot alignment is the primary factor (40% weight)
        score += blindspot_alignment * 0.4
        
        # Impact level (30% weight)
        if opportunity.impact_level.value == "High":
            score += 0.3
        elif opportunity.impact_level.value == "Medium":
            score += 0.2
        else:
            score += 0.1
        
        # Visibility level - prioritize low visibility (20% weight)
        if opportunity.visibility_level == VisibilityLevel.LOW:
            score += 0.2
        elif opportunity.visibility_level == VisibilityLevel.MEDIUM:
            score += 0.15
        else:
            score += 0.1
        
        # Goal alignment (10% weight)
        opportunity_category_to_goal = {
            "Scholarship": OpportunityGoal.SCHOLARSHIPS,
            "Internship": OpportunityGoal.INTERNSHIPS,
            "Program": OpportunityGoal.SKILLS,
        }
        
        if opportunity.category in opportunity_category_to_goal:
            goal = opportunity_category_to_goal[opportunity.category]
            if goal in analysis.priority_goals:
                score += 0.1
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _generate_fit_explanation(
        self,
        profile: StudentProfile,
        opportunity: Opportunity
    ) -> str:
        """
        Generate explanation for why the opportunity fits the student's profile.
        
        Args:
            profile: The student profile
            opportunity: The opportunity
            
        Returns:
            Human-readable fit explanation
        """
        explanations = []
        
        # Education level match
        explanations.append(
            f"You're a {profile.education_level.value} student, which matches the eligibility"
        )
        
        # Field of study match (if specific)
        if opportunity.eligibility_criteria.fields_of_study is not None:
            explanations.append(
                f"your {profile.field_of_study} background aligns with the program requirements"
            )
        
        # Background indicators match
        if opportunity.eligibility_criteria.background_requirements is not None:
            matching_backgrounds = [
                bg for bg in profile.background_indicators
                if bg in opportunity.eligibility_criteria.background_requirements
            ]
            if matching_backgrounds:
                bg_str = ', '.join([bg.value for bg in matching_backgrounds])
                explanations.append(
                    f"your background ({bg_str}) makes you eligible for this targeted program"
                )
        
        # Income-based opportunities
        if opportunity.eligibility_criteria.income_based:
            if BackgroundIndicator.FINANCIAL_SUPPORT in profile.background_indicators:
                explanations.append(
                    "this income-based program is designed for students needing financial support"
                )
        
        # Merit-based opportunities
        if opportunity.eligibility_criteria.merit_based:
            explanations.append(
                "this merit-based program recognizes academic achievement"
            )
        
        # Join explanations
        if len(explanations) == 1:
            return explanations[0] + "."
        elif len(explanations) == 2:
            return explanations[0] + ", and " + explanations[1] + "."
        else:
            return ", ".join(explanations[:-1]) + ", and " + explanations[-1] + "."
    
    def _generate_miss_reason(
        self,
        opportunity: Opportunity,
        awareness_level: AwarenessLevel
    ) -> str:
        """
        Generate explanation for why students usually miss this opportunity.
        
        Args:
            opportunity: The opportunity
            awareness_level: The student's awareness level
            
        Returns:
            Human-readable miss reason
        """
        reasons = []
        
        # Visibility-based reasons
        if opportunity.visibility_level == VisibilityLevel.LOW:
            reasons.append("this program has very low visibility and is rarely promoted in colleges")
        elif opportunity.visibility_level == VisibilityLevel.MEDIUM:
            reasons.append("this program is not widely advertised beyond official government portals")
        
        # Category-specific reasons
        if "AICTE" in opportunity.name:
            reasons.append("AICTE programs are often buried in technical documentation")
        elif "State" in opportunity.name:
            reasons.append("state-level programs vary by region and lack centralized promotion")
        elif "NPTEL" in opportunity.name:
            reasons.append("students often see NPTEL only as a course platform, not for internships")
        elif "Ministry" in opportunity.name:
            reasons.append("ministry programs are scattered across multiple websites")
        elif "Central Sector" in opportunity.name:
            reasons.append("many students assume they need high merit for central scholarships")
        
        # Awareness-based reasons
        if awareness_level == AwarenessLevel.LOW:
            reasons.append("students with limited opportunity awareness often miss such programs")
        
        # Join reasons
        if len(reasons) == 0:
            return "Students often miss this opportunity due to lack of awareness."
        elif len(reasons) == 1:
            return "Students usually miss this because " + reasons[0] + "."
        else:
            return "Students usually miss this because " + " and ".join(reasons) + "."
