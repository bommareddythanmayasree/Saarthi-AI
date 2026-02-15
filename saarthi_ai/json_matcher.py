"""
JSON-based opportunity matcher for SaarthiAI.
Loads opportunities from data/oppurtunities.json and matches based on exact criteria.
"""
import json
import os
from typing import List, Dict, Any


class JSONOpportunityMatcher:
    """Matches student profiles to opportunities from JSON dataset."""
    
    def __init__(self, json_path: str = None):
        """
        Initialize the matcher with opportunities from JSON file.
        
        Args:
            json_path: Path to opportunities.json file. If None, uses default path.
        """
        if json_path is None:
            # Default path relative to project root
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            json_path = os.path.join(base_dir, 'data', 'oppurtunities.json')
        
        self.opportunities = self._load_opportunities(json_path)
    
    def _load_opportunities(self, json_path: str) -> List[Dict[str, Any]]:
        """Load opportunities from JSON file."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Opportunities file not found at {json_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"Warning: Error parsing JSON file: {e}")
            return []
    
    def is_eligible(self, student: Dict[str, Any], opportunity: Dict[str, Any]) -> bool:
        """
        Check if student is eligible for an opportunity.
        
        Returns true only if ALL conditions match:
        - education_level matches OR is "Any"
        - eligible_fields matches OR is "Any"
        - target_year matches OR is "Any"
        - institution_type matches OR is "Any"
        - background_priority matches OR is "Any"
        
        Args:
            student: Student data dict with keys: education_level, field, year, 
                     institution_type, background
            opportunity: Opportunity dict from JSON
            
        Returns:
            True if eligible, False otherwise
        """
        # Education level check
        opp_edu = opportunity.get('education_level', 'Any')
        if opp_edu != 'Any' and opp_edu != student.get('education_level'):
            return False
        
        # Field of study check
        opp_field = opportunity.get('eligible_fields', 'Any')
        if opp_field != 'Any' and opp_field != student.get('field'):
            return False
        
        # Year of study check
        opp_year = opportunity.get('target_year', 'Any')
        if opp_year != 'Any' and opp_year != student.get('year'):
            return False
        
        # Institution type check
        opp_inst = opportunity.get('institution_type', 'Any')
        if opp_inst != 'Any' and opp_inst != student.get('institution_type'):
            return False
        
        # Background priority check
        opp_bg = opportunity.get('background_priority', 'Any')
        if opp_bg != 'Any' and opp_bg != student.get('background'):
            return False
        
        return True
    
    def calculate_score(self, student: Dict[str, Any], opportunity: Dict[str, Any]) -> int:
        """
        Calculate matching score for an eligible opportunity.
        
        Score calculation:
        +1 if education_level matches exactly (not "Any")
        +1 if eligible_fields matches exactly (not "Any")
        +1 if target_year matches exactly (not "Any")
        +1 if institution_type matches exactly (not "Any")
        +1 if background_priority matches exactly (not "Any")
        
        Blindspot Boost:
        +1 if awareness_level == "Low"
        +1 if miss_probability == "High"
        
        Args:
            student: Student data dict
            opportunity: Opportunity dict from JSON
            
        Returns:
            Total matching score (0-7)
        """
        score = 0
        
        # Exact match scoring
        opp_edu = opportunity.get('education_level', 'Any')
        if opp_edu != 'Any' and opp_edu == student.get('education_level'):
            score += 1
        
        opp_field = opportunity.get('eligible_fields', 'Any')
        if opp_field != 'Any' and opp_field == student.get('field'):
            score += 1
        
        opp_year = opportunity.get('target_year', 'Any')
        if opp_year != 'Any' and opp_year == student.get('year'):
            score += 1
        
        opp_inst = opportunity.get('institution_type', 'Any')
        if opp_inst != 'Any' and opp_inst == student.get('institution_type'):
            score += 1
        
        opp_bg = opportunity.get('background_priority', 'Any')
        if opp_bg != 'Any' and opp_bg == student.get('background'):
            score += 1
        
        # Blindspot boost
        if opportunity.get('awareness_level') == 'Low':
            score += 1
        
        if opportunity.get('miss_probability') == 'High':
            score += 1
        
        return score
    
    def match_opportunities(self, student: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find and score all eligible opportunities for a student.
        
        Process:
        1. Filter opportunities using is_eligible()
        2. Calculate score for each eligible opportunity
        3. Sort by score (descending)
        4. Return sorted list with scores
        
        Args:
            student: Student data dict with keys: education_level, field, year,
                     institution_type, background
            
        Returns:
            List of dicts with opportunity data + 'matching_score' field,
            sorted by score (highest first). Empty list if no matches.
        """
        eligible_opportunities = []
        
        # Filter and score
        for opportunity in self.opportunities:
            if self.is_eligible(student, opportunity):
                # Create a copy with the score
                opp_with_score = opportunity.copy()
                opp_with_score['matching_score'] = self.calculate_score(student, opportunity)
                eligible_opportunities.append(opp_with_score)
        
        # Sort by score (descending)
        eligible_opportunities.sort(key=lambda x: x['matching_score'], reverse=True)
        
        return eligible_opportunities
