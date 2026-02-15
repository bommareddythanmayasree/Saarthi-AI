"""Blindspot identifier component for SaarthiAI application."""
from typing import List
from saarthi_ai.models import (
    StudentProfile,
    ProfileAnalysis,
    Blindspot,
    OpportunityGoal,
    BackgroundIndicator,
    EducationLevel,
    InstitutionType
)


class BlindspotIdentifier:
    """Identifies opportunity categories the student is likely unaware of."""
    
    # STEM fields for research opportunity identification
    STEM_FIELDS = [
        "Computer Science", "Engineering", "Mathematics", "Physics", 
        "Chemistry", "Biology", "Statistics", "Data Science",
        "Information Technology", "Electronics", "Mechanical",
        "Civil", "Chemical", "Biotechnology"
    ]
    
    def identify_blindspots(
        self, 
        profile: StudentProfile, 
        analysis: ProfileAnalysis
    ) -> List[Blindspot]:
        """
        Identify opportunity blindspots based on student profile and analysis.
        
        Args:
            profile: The student profile
            analysis: The profile analysis containing characteristics and tags
            
        Returns:
            List of 3-5 blindspots with categories, reasons, and relevance scores
        """
        blindspots = []
        
        # Rule 1: Income-based scholarships for eligible students
        if self._has_financial_background(analysis.eligibility_tags) and \
           OpportunityGoal.SCHOLARSHIPS in analysis.priority_goals:
            blindspots.append(Blindspot(
                category="Income-based Central Government Scholarships",
                reason="Many students don't know about central government scholarships that don't require high merit",
                relevance_score=0.9
            ))
        
        # Rule 2: Research opportunities for STEM students
        if self._is_stem_field(profile.field_of_study) and \
           profile.education_level in [EducationLevel.UG, EducationLevel.PG]:
            blindspots.append(Blindspot(
                category="Research Internships and Programs",
                reason="STEM students often focus on placements and miss research opportunities from national platforms",
                relevance_score=0.8
            ))
        
        # Rule 3: State-level merit scholarships
        if profile.institution_type in [InstitutionType.GOVERNMENT, InstitutionType.AUTONOMOUS] and \
           OpportunityGoal.SCHOLARSHIPS in analysis.priority_goals:
            blindspots.append(Blindspot(
                category="State-level Merit Scholarships",
                reason="State scholarships have poor visibility compared to national programs",
                relevance_score=0.7
            ))
        
        # Rule 4: Gender/disability-specific programs
        if self._has_special_category(profile.gender, analysis.eligibility_tags):
            blindspots.append(Blindspot(
                category="Category-specific Technical Scholarships",
                reason="Technical scholarships for specific categories are often under-promoted in colleges",
                relevance_score=0.85
            ))
        
        # Rule 5: Innovation and skill programs
        if OpportunityGoal.SKILLS in analysis.priority_goals or \
           self._mentions_innovation(profile.additional_context):
            blindspots.append(Blindspot(
                category="Government Innovation and Skill Programs",
                reason="Innovation programs are often buried in government websites with poor outreach",
                relevance_score=0.6
            ))
        
        # Rule 6: Internship opportunities (fallback for general profiles)
        if OpportunityGoal.INTERNSHIPS in analysis.priority_goals:
            blindspots.append(Blindspot(
                category="Industry and Government Internships",
                reason="Many internship programs beyond campus placements remain unknown to students",
                relevance_score=0.65
            ))
        
        # Rule 7: Government exam preparation resources (fallback)
        if OpportunityGoal.GOVT_EXAMS in analysis.priority_goals:
            blindspots.append(Blindspot(
                category="Government Exam Preparation Resources",
                reason="Free government resources for exam preparation are often overlooked",
                relevance_score=0.55
            ))
        
        # Rule 8: Research opportunities for non-STEM (fallback)
        if OpportunityGoal.RESEARCH in analysis.priority_goals and not self._is_stem_field(profile.field_of_study):
            blindspots.append(Blindspot(
                category="Interdisciplinary Research Programs",
                reason="Research opportunities exist beyond traditional STEM fields but are rarely promoted",
                relevance_score=0.58
            ))
        
        # Fallback rules to ensure minimum count of 3 blindspots
        # Rule 9: General scholarship opportunities (fallback to ensure minimum count)
        if len(blindspots) < 3 and OpportunityGoal.SCHOLARSHIPS in analysis.priority_goals:
            blindspots.append(Blindspot(
                category="Merit and Need-based Scholarships",
                reason="Many scholarship programs exist beyond the well-known ones, but lack awareness",
                relevance_score=0.5
            ))
        
        # Rule 10: Skill development programs (fallback to ensure minimum count)
        if len(blindspots) < 3:
            blindspots.append(Blindspot(
                category="Skill Development and Certification Programs",
                reason="Free skill development programs from government and institutions often go unnoticed",
                relevance_score=0.45
            ))
        
        # Rule 11: Academic enhancement programs (fallback to ensure minimum count)
        if len(blindspots) < 3:
            blindspots.append(Blindspot(
                category="Academic Enhancement Programs",
                reason="Programs for academic growth beyond regular curriculum are rarely promoted",
                relevance_score=0.4
            ))
        
        # Rule 12: Career guidance programs (final fallback)
        if len(blindspots) < 3:
            blindspots.append(Blindspot(
                category="Career Guidance and Mentorship Programs",
                reason="Structured career guidance programs from institutions and government are underutilized",
                relevance_score=0.35
            ))
        
        # Sort by relevance score (descending)
        blindspots.sort(key=lambda b: b.relevance_score, reverse=True)
        
        # Ensure we always return between 3 and 5 blindspots
        # If we have fewer than 3, this is a bug in our rules
        if len(blindspots) < 3:
            raise ValueError(f"Implementation error: Only {len(blindspots)} blindspots generated, minimum is 3")
        
        # Return top 3-5 blindspots
        return blindspots[:5]
    
    def _has_financial_background(self, eligibility_tags: List[str]) -> bool:
        """Check if student has financial support background."""
        return BackgroundIndicator.FINANCIAL_SUPPORT.value in eligibility_tags
    
    def _is_stem_field(self, field_of_study: str) -> bool:
        """Check if field of study is STEM-related."""
        field_lower = field_of_study.lower()
        return any(stem.lower() in field_lower for stem in self.STEM_FIELDS)
    
    def _has_special_category(
        self, 
        gender: str | None, 
        eligibility_tags: List[str]
    ) -> bool:
        """Check if student belongs to special category (female or disabled)."""
        # Check for female gender
        if gender and gender.lower() in ["female", "woman", "f"]:
            return True
        
        # Check for disabled background
        if BackgroundIndicator.DISABLED.value in eligibility_tags:
            return True
        
        return False
    
    def _mentions_innovation(self, additional_context: str | None) -> bool:
        """Check if additional context mentions innovation."""
        if not additional_context:
            return False
        
        innovation_keywords = ["innovation", "innovate", "innovative", "startup", "entrepreneur"]
        context_lower = additional_context.lower()
        return any(keyword in context_lower for keyword in innovation_keywords)
