"""Data models for SaarthiAI application."""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class EducationLevel(Enum):
    """Education level enumeration."""
    DIPLOMA = "Diploma"
    UG = "UG"
    PG = "PG"
    PHD = "PhD"


class InstitutionType(Enum):
    """Institution type enumeration."""
    GOVERNMENT = "Government"
    PRIVATE = "Private"
    AUTONOMOUS = "Autonomous"
    OPEN = "Open"


class BackgroundIndicator(Enum):
    """Background indicator enumeration."""
    RURAL = "Rural"
    FIRST_GENERATION = "First-generation"
    FINANCIAL_SUPPORT = "Financial support"
    DISABLED = "Disabled"
    MINORITY = "Minority"


class OpportunityGoal(Enum):
    """Opportunity goal enumeration."""
    SCHOLARSHIPS = "Scholarships"
    INTERNSHIPS = "Internships"
    RESEARCH = "Research"
    SKILLS = "Skills"
    GOVT_EXAMS = "Govt Exams"


class MissedOpportunityFrequency(Enum):
    """Missed opportunity frequency enumeration."""
    YES_MANY_TIMES = "Yes many times"
    ONCE_OR_TWICE = "Once or twice"
    NO = "No"


class MissProbability(Enum):
    """Miss probability enumeration."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class VisibilityLevel(Enum):
    """Visibility level enumeration."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class ImpactLevel(Enum):
    """Impact level enumeration."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class AwarenessLevel(Enum):
    """Awareness level enumeration."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass
class StudentProfile:
    """Student profile data model."""
    # Required fields
    name: str
    age: int
    education_level: EducationLevel
    degree: str
    field_of_study: str
    year_of_study: int
    institution_type: InstitutionType
    background_indicators: List[BackgroundIndicator]
    opportunity_goals: List[OpportunityGoal]
    missed_opportunities_before: MissedOpportunityFrequency
    
    # Optional fields
    gender: Optional[str] = None
    additional_context: Optional[str] = None

    def validate(self) -> tuple[bool, List[str]]:
        """
        Validate the student profile.
        
        Returns:
            Tuple of (is_valid, list_of_missing_fields)
        """
        missing_fields = []
        
        # Check required fields
        if not self.name or not self.name.strip():
            missing_fields.append("name")
        
        if self.age is None or self.age <= 0:
            missing_fields.append("age")
        
        if self.education_level is None:
            missing_fields.append("education_level")
        
        if not self.degree or not self.degree.strip():
            missing_fields.append("degree")
        
        if not self.field_of_study or not self.field_of_study.strip():
            missing_fields.append("field_of_study")
        
        if self.year_of_study is None or self.year_of_study <= 0:
            missing_fields.append("year_of_study")
        
        if self.institution_type is None:
            missing_fields.append("institution_type")
        
        # Background indicators are optional - students may not have any special background
        
        if not self.opportunity_goals:
            missing_fields.append("opportunity_goals")
        
        if self.missed_opportunities_before is None:
            missing_fields.append("missed_opportunities_before")
        
        return len(missing_fields) == 0, missing_fields


@dataclass
class EligibilityCriteria:
    """Eligibility criteria for opportunities."""
    education_levels: List[EducationLevel]
    fields_of_study: Optional[List[str]] = None
    institution_types: Optional[List[InstitutionType]] = None
    background_requirements: Optional[List[BackgroundIndicator]] = None
    income_based: bool = False
    merit_based: bool = False


@dataclass
class Opportunity:
    """Opportunity data model."""
    id: str
    name: str
    description: str
    eligibility_criteria: EligibilityCriteria
    visibility_level: VisibilityLevel
    impact_level: ImpactLevel
    category: str


@dataclass
class Blindspot:
    """Blindspot data model."""
    category: str
    reason: str
    relevance_score: float


@dataclass
class OpportunityMatch:
    """Opportunity match data model."""
    opportunity: Opportunity
    fit_explanation: str
    miss_reason: str
    miss_probability: MissProbability
    relevance_score: float


@dataclass
class ProfileAnalysis:
    """Profile analysis data model."""
    key_characteristics: List[str]
    eligibility_tags: List[str]
    awareness_level: AwarenessLevel
    priority_goals: List[OpportunityGoal]
