"""Profile analyzer component for SaarthiAI application."""
from typing import List
from saarthi_ai.models import (
    StudentProfile,
    ProfileAnalysis,
    AwarenessLevel,
    MissedOpportunityFrequency,
    OpportunityGoal,
    BackgroundIndicator
)


class ProfileAnalyzer:
    """Analyzes student profiles to extract key characteristics for matching."""
    
    def analyze(self, profile: StudentProfile) -> ProfileAnalysis:
        """
        Analyze a student profile to extract key characteristics.
        
        Args:
            profile: The student profile to analyze
            
        Returns:
            ProfileAnalysis containing characteristics, eligibility tags,
            awareness level, and priority goals
        """
        key_characteristics = self._extract_characteristics(profile)
        eligibility_tags = self._extract_eligibility_tags(profile)
        awareness_level = self._map_awareness_level(profile.missed_opportunities_before)
        priority_goals = profile.opportunity_goals
        
        return ProfileAnalysis(
            key_characteristics=key_characteristics,
            eligibility_tags=eligibility_tags,
            awareness_level=awareness_level,
            priority_goals=priority_goals
        )
    
    def _extract_characteristics(self, profile: StudentProfile) -> List[str]:
        """Extract key characteristics from the profile."""
        characteristics = []
        
        # Add education characteristics
        characteristics.append(profile.education_level.value)
        characteristics.append(profile.field_of_study)
        characteristics.append(profile.institution_type.value)
        
        # Add background characteristics
        for indicator in profile.background_indicators:
            characteristics.append(indicator.value)
        
        return characteristics
    
    def _extract_eligibility_tags(self, profile: StudentProfile) -> List[str]:
        """Extract eligibility tags from background indicators."""
        eligibility_tags = []
        
        for indicator in profile.background_indicators:
            eligibility_tags.append(indicator.value)
        
        return eligibility_tags
    
    def _map_awareness_level(
        self, 
        missed_opportunities: MissedOpportunityFrequency
    ) -> AwarenessLevel:
        """
        Map missed opportunities frequency to awareness level.
        
        Args:
            missed_opportunities: How often the student has missed opportunities
            
        Returns:
            Corresponding awareness level
        """
        if missed_opportunities == MissedOpportunityFrequency.YES_MANY_TIMES:
            return AwarenessLevel.LOW
        elif missed_opportunities == MissedOpportunityFrequency.ONCE_OR_TWICE:
            return AwarenessLevel.MEDIUM
        else:  # NO
            return AwarenessLevel.HIGH
