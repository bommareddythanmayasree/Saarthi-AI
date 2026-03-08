"""Opportunity knowledge base for SaarthiAI application."""
from typing import List
from saarthi_ai.models import (
    Opportunity,
    EligibilityCriteria,
    EducationLevel,
    InstitutionType,
    BackgroundIndicator,
    VisibilityLevel,
    ImpactLevel,
)


# Static opportunity knowledge base
OPPORTUNITIES: List[Opportunity] = [
    Opportunity(
        id="central-sector-scholarship",
        name="Central Sector Scholarship",
        description="Central government scholarship for undergraduate students from families with income below threshold",
        eligibility_criteria=EligibilityCriteria(
            education_levels=[EducationLevel.UG],
            fields_of_study=None,  # All fields
            institution_types=None,  # All institution types
            background_requirements=None,
            income_based=True,
            merit_based=False,
        ),
        visibility_level=VisibilityLevel.MEDIUM,
        impact_level=ImpactLevel.HIGH,
        category="Scholarship",
    ),
    Opportunity(
        id="aicte-pragati",
        name="AICTE Pragati",
        description="AICTE scholarship for female engineering students",
        eligibility_criteria=EligibilityCriteria(
            education_levels=[EducationLevel.UG],
            fields_of_study=["Engineering"],
            institution_types=None,
            background_requirements=None,
            income_based=False,
            merit_based=False,
        ),
        visibility_level=VisibilityLevel.LOW,
        impact_level=ImpactLevel.HIGH,
        category="Scholarship",
    ),
    Opportunity(
        id="aicte-saksham",
        name="AICTE Saksham",
        description="AICTE scholarship for disabled engineering students",
        eligibility_criteria=EligibilityCriteria(
            education_levels=[EducationLevel.UG],
            fields_of_study=["Engineering"],
            institution_types=None,
            background_requirements=[BackgroundIndicator.DISABLED],
            income_based=False,
            merit_based=False,
        ),
        visibility_level=VisibilityLevel.LOW,
        impact_level=ImpactLevel.HIGH,
        category="Scholarship",
    ),
    Opportunity(
        id="nptel-research-internship",
        name="NPTEL Research Internship",
        description="Research internship program for STEM students",
        eligibility_criteria=EligibilityCriteria(
            education_levels=[EducationLevel.UG, EducationLevel.PG],
            fields_of_study=["Engineering", "Science", "Mathematics", "Computer Science"],
            institution_types=None,
            background_requirements=None,
            income_based=False,
            merit_based=False,
        ),
        visibility_level=VisibilityLevel.MEDIUM,
        impact_level=ImpactLevel.MEDIUM,
        category="Internship",
    ),
    Opportunity(
        id="state-govt-merit-scholarship",
        name="State Government Merit Scholarships",
        description="Merit-based scholarships offered by state governments",
        eligibility_criteria=EligibilityCriteria(
            education_levels=[
                EducationLevel.DIPLOMA,
                EducationLevel.UG,
                EducationLevel.PG,
                EducationLevel.PHD,
            ],
            fields_of_study=None,  # All fields
            institution_types=None,  # All institution types
            background_requirements=None,
            income_based=False,
            merit_based=True,
        ),
        visibility_level=VisibilityLevel.LOW,
        impact_level=ImpactLevel.MEDIUM,
        category="Scholarship",
    ),
    Opportunity(
        id="moe-innovation-programs",
        name="Ministry of Education Innovation Programs",
        description="Innovation and skill development programs by Ministry of Education",
        eligibility_criteria=EligibilityCriteria(
            education_levels=[
                EducationLevel.DIPLOMA,
                EducationLevel.UG,
                EducationLevel.PG,
                EducationLevel.PHD,
            ],
            fields_of_study=None,  # All fields
            institution_types=None,  # All institution types
            background_requirements=None,
            income_based=False,
            merit_based=False,
        ),
        visibility_level=VisibilityLevel.LOW,
        impact_level=ImpactLevel.MEDIUM,
        category="Program",
    ),
]


def get_all_opportunities() -> List[Opportunity]:
    """
    Get all opportunities from the knowledge base.
    
    Returns:
        List of all opportunities
    """
    return OPPORTUNITIES.copy()


def get_opportunity_by_id(opportunity_id: str) -> Opportunity | None:
    """
    Get a specific opportunity by its ID.
    
    Args:
        opportunity_id: The unique identifier of the opportunity
        
    Returns:
        The opportunity if found, None otherwise
    """
    for opportunity in OPPORTUNITIES:
        if opportunity.id == opportunity_id:
            return opportunity
    return None


def get_opportunities_by_category(category: str) -> List[Opportunity]:
    """
    Get all opportunities in a specific category.
    
    Args:
        category: The category to filter by (e.g., "Scholarship", "Internship")
        
    Returns:
        List of opportunities in the specified category
    """
    return [opp for opp in OPPORTUNITIES if opp.category == category]


def get_opportunities_by_education_level(education_level: EducationLevel) -> List[Opportunity]:
    """
    Get all opportunities available for a specific education level.
    
    Args:
        education_level: The education level to filter by
        
    Returns:
        List of opportunities available for the education level
    """
    return [
        opp for opp in OPPORTUNITIES
        if education_level in opp.eligibility_criteria.education_levels
    ]
