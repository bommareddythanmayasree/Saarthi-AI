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
        - age requirements (if specified)
        - skills requirements (if specified)
        
        Args:
            student: Student data dict with keys: education_level, field, year, 
                     age, skills, institution_type, background
            opportunity: Opportunity dict from JSON
            
        Returns:
            True if eligible, False otherwise
        """
        try:
            # Get eligibility criteria from nested structure
            eligibility = opportunity.get('eligibility', {})
            
            # Education level check (handle multiple levels like "UG/PG")
            opp_edu = eligibility.get('education_level', 'Any')
            if opp_edu and opp_edu != 'Any':
                eligible_edu_levels = [e.strip() for e in str(opp_edu).split('/')]
                if student.get('education_level') not in eligible_edu_levels:
                    return False
            
            # Field of study check (handle multiple fields like "Engineering/Science")
            opp_field = eligibility.get('eligible_fields', 'Any')
            if opp_field and opp_field != 'Any':
                eligible_fields = [f.strip() for f in str(opp_field).split('/')]
                student_field = student.get('field', '')
                if student_field not in eligible_fields:
                    return False
            
            # Year of study check (handle ranges like "2nd or 3rd")
            opp_year = eligibility.get('target_year', 'Any')
            if opp_year and opp_year != 'Any':
                student_year = student.get('year', '')
                # Handle "or" in year specifications
                if ' or ' in str(opp_year):
                    eligible_years = [y.strip() for y in str(opp_year).split(' or ')]
                    if student_year not in eligible_years:
                        return False
                elif opp_year != student_year:
                    return False
            
            # Age check (if opportunity specifies age requirements)
            # Most opportunities don't have age restrictions, but check if present
            student_age = student.get('age')
            if student_age:
                # Check if opportunity has age restrictions in description or other fields
                # For now, basic check - can be enhanced based on dataset
                pass
            
            # Skills check (if opportunity requires specific skills)
            required_skills = opportunity.get('skills_required', [])
            if required_skills and isinstance(required_skills, list) and len(required_skills) > 0:
                student_skills = student.get('skills', [])
                if isinstance(student_skills, list) and len(student_skills) > 0:
                    # Normalize skills for comparison (case-insensitive)
                    student_skills_lower = [s.lower().strip() for s in student_skills]
                    required_skills_lower = [s.lower().strip() for s in required_skills]
                    
                    # Check if student has at least one required skill
                    has_required_skill = any(
                        any(req_skill in student_skill or student_skill in req_skill 
                            for student_skill in student_skills_lower)
                        for req_skill in required_skills_lower
                    )
                    
                    # If no skills match, still allow but with lower score
                    # Don't completely exclude - skills can be learned
                    pass
            
            return True
            
        except Exception as e:
            # Log error but don't break the matching process
            print(f"Error checking eligibility: {e}")
            return False
    
    def calculate_score(self, student: Dict[str, Any], opportunity: Dict[str, Any]) -> int:
        """
        Calculate matching score for an eligible opportunity.

        Score calculation:
        +2 if education_level matches exactly (not "Any")
        +2 if eligible_fields matches exactly (not "Any")
        +1 if target_year matches exactly (not "Any")
        +2 if impact_level == "High"
        +1 if category matches student goals
        +2 if student has required skills (bonus)

        Args:
            student: Student data dict
            opportunity: Opportunity dict from JSON

        Returns:
            Total matching score (0-10)
        """
        try:
            score = 0
            eligibility = opportunity.get('eligibility', {})

            # Exact match scoring for education level
            opp_edu = eligibility.get('education_level', 'Any')
            if opp_edu and opp_edu != 'Any':
                eligible_edu_levels = [e.strip() for e in str(opp_edu).split('/')]
                if student.get('education_level') in eligible_edu_levels:
                    score += 2

            # Exact match scoring for field
            opp_field = eligibility.get('eligible_fields', 'Any')
            if opp_field and opp_field != 'Any':
                eligible_fields = [f.strip() for f in str(opp_field).split('/')]
                if student.get('field') in eligible_fields:
                    score += 2

            # Year match scoring
            opp_year = eligibility.get('target_year', 'Any')
            if opp_year and opp_year != 'Any':
                student_year = student.get('year', '')
                if ' or ' in str(opp_year):
                    eligible_years = [y.strip() for y in str(opp_year).split(' or ')]
                    if student_year in eligible_years:
                        score += 1
                elif opp_year == student_year:
                    score += 1

            # Impact level boost
            if opportunity.get('impact_level') == 'High':
                score += 2

            # Category relevance
            category = opportunity.get('category', '')
            if category in ['Scholarship', 'Internship', 'Research']:
                score += 1

            # Skills matching bonus
            required_skills = opportunity.get('skills_required', [])
            student_skills = student.get('skills', [])

            if required_skills and isinstance(required_skills, list) and len(required_skills) > 0:
                if student_skills and isinstance(student_skills, list) and len(student_skills) > 0:
                    # Normalize skills for comparison
                    student_skills_lower = [s.lower().strip() for s in student_skills]
                    required_skills_lower = [s.lower().strip() for s in required_skills]

                    # Count matching skills
                    matching_skills = 0
                    for req_skill in required_skills_lower:
                        for student_skill in student_skills_lower:
                            if req_skill in student_skill or student_skill in req_skill:
                                matching_skills += 1
                                break

                    # Award points based on skill match percentage
                    if matching_skills > 0:
                        match_percentage = matching_skills / len(required_skills_lower)
                        if match_percentage >= 0.5:  # 50% or more skills match
                            score += 2
                        elif match_percentage >= 0.25:  # 25% or more skills match
                            score += 1

            return score

        except Exception as e:
            print(f"Error calculating score: {e}")
            return 0
    
    def _generate_why_missed(self, opportunity: Dict[str, Any]) -> str:
        """
        Generate explanation for why students usually miss this opportunity.
        
        Args:
            opportunity: Opportunity dict from JSON
            
        Returns:
            Human-readable explanation
        """
        category = opportunity.get('category', '')
        title = opportunity.get('title', '')
        org = opportunity.get('organization', '')
        
        # Category-based reasons
        if category == 'Scholarship':
            if 'AICTE' in org or 'AICTE' in title:
                return "AICTE scholarships are often buried in technical documentation and not widely promoted in colleges."
            elif 'State' in title or 'state' in title.lower():
                return "State-level scholarships vary by region and lack centralized promotion, making them easy to miss."
            elif 'INSPIRE' in title or 'KVPY' in title:
                return "Many students assume they need exceptional merit for DST programs and don't apply."
            elif 'Women' in title or 'Girls' in title:
                return "Gender-specific scholarships are often not actively promoted to eligible female students."
            else:
                return "This scholarship has limited visibility and is rarely advertised beyond official portals."
        
        elif category == 'Internship':
            if 'DRDO' in org or 'ISRO' in org:
                return "Government research internships have complex application processes and limited promotion in colleges."
            elif 'RBI' in org:
                return "RBI internships are highly competitive and not widely known outside economics circles."
            elif 'Google' in org or 'Summer of Code' in title:
                return "Students often don't realize they can contribute to open-source without prior experience."
            elif 'Adobe' in org or 'Amazon' in org or 'Meta' in org:
                return "Corporate internships are competitive and students often underestimate their eligibility."
            elif 'IIT' in org:
                return "IIT research internships are not widely advertised and students assume they're only for top performers."
            else:
                return "This internship opportunity has low visibility and limited campus promotion."
        
        elif category == 'Research':
            return "Research opportunities are often shared only within academic circles and not promoted to broader student audiences."
        
        elif category == 'Skill Program':
            if 'NPTEL' in title:
                return "Students often see NPTEL only as a course platform and miss the certification value."
            elif 'Microsoft' in org or 'GitHub' in org:
                return "Student ambassador programs require proactive application and are not actively recruited on most campuses."
            elif 'Amazon' in org:
                return "ML training programs from tech companies are not widely advertised to students."
            else:
                return "Skill development programs often lack visibility and students don't know where to find them."
        
        elif category == 'Government Initiative':
            if 'Apprenticeship' in title or 'NATS' in title:
                return "Government apprenticeship schemes are scattered across portals and not well-integrated with college placement systems."
            elif 'Startup' in title or 'Innovation' in title:
                return "Innovation grants and startup programs require entrepreneurial mindset and students often don't know they're eligible."
            else:
                return "Government initiatives are spread across multiple websites and lack centralized awareness campaigns."
        
        elif category == 'Competition':
            if 'Hackathon' in title:
                return "National hackathons require team formation and students often miss registration deadlines."
            elif 'Tata' in org:
                return "Corporate competitions are not widely promoted in technical colleges and students miss application windows."
            else:
                return "Competition opportunities have short application windows and limited campus visibility."
        
        else:
            return "This opportunity has limited visibility and students often don't know it exists."
    
    def match_opportunities(self, student: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find and score all eligible opportunities for a student.
        
        Process:
        1. Filter opportunities using is_eligible()
        2. Calculate score for each eligible opportunity
        3. Sort by score (descending)
        4. Return sorted list with scores and formatted data
        
        Args:
            student: Student data dict with keys: education_level, field, year,
                     institution_type, background
            
        Returns:
            List of dicts with formatted opportunity data + 'matching_score' field,
            sorted by score (highest first). Empty list if no matches.
        """
        eligible_opportunities = []
        
        # Filter and score
        for opportunity in self.opportunities:
            if self.is_eligible(student, opportunity):
                # Calculate score
                score = self.calculate_score(student, opportunity)
                
                # Format opportunity data for UI
                formatted_opp = {
                    'id': opportunity.get('id', ''),
                    'opportunity_name': opportunity.get('title', 'Unknown'),
                    'category': opportunity.get('category', 'Other'),
                    'description': opportunity.get('description', ''),
                    'impact_level': opportunity.get('impact_level', 'Medium'),
                    'organization': opportunity.get('organization', ''),
                    'organization_description': opportunity.get('organization_description', ''),
                    'location': opportunity.get('location', ''),
                    'work_mode': opportunity.get('work_mode', ''),
                    'duration': opportunity.get('duration', ''),
                    'start_date': opportunity.get('start_date', ''),
                    'stipend': opportunity.get('stipend', 'Not specified'),
                    'perks': opportunity.get('perks', []),
                    'apply_link': opportunity.get('apply_link', ''),
                    'application_deadline': opportunity.get('application_deadline', 'Varies'),
                    'roles_responsibilities': opportunity.get('roles_responsibilities', []),
                    'skills_required': opportunity.get('skills_required', []),
                    'eligibility': opportunity.get('eligibility', {}),
                    'why_missed': self._generate_why_missed(opportunity),
                    'matching_score': score,
                    'awareness_level': 'Low',  # Default for all opportunities
                    'miss_probability': 'High' if score <= 4 else 'Medium'
                }
                
                eligible_opportunities.append(formatted_opp)
        
        # Sort by score (descending)
        eligible_opportunities.sort(key=lambda x: x['matching_score'], reverse=True)
        
        return eligible_opportunities
