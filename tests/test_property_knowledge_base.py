"""
Property-based tests for knowledge base structure.

Feature: saarthi-ai-opportunity-finder
Property 6: Knowledge Base Structure Integrity
Validates: Requirements 5.2
"""
import pytest
from hypothesis import given, strategies as st
from saarthi_ai.knowledge_base import get_all_opportunities
from saarthi_ai.models import (
    Opportunity,
    EligibilityCriteria,
    EducationLevel,
    VisibilityLevel,
    ImpactLevel,
)


def test_property_knowledge_base_structure_integrity():
    """
    Property 6: Knowledge Base Structure Integrity.
    
    For any opportunity in the knowledge base, it must have defined eligibility
    criteria that includes at minimum the list of eligible education levels.
    
    Validates: Requirements 5.2
    """
    opportunities = get_all_opportunities()
    
    # Verify knowledge base is not empty
    assert len(opportunities) > 0, "Knowledge base is empty"
    
    for opportunity in opportunities:
        # Verify opportunity has all required fields
        assert opportunity.id is not None, f"Opportunity missing id: {opportunity}"
        assert opportunity.name is not None, f"Opportunity missing name: {opportunity}"
        assert opportunity.description is not None, f"Opportunity missing description: {opportunity}"
        assert opportunity.eligibility_criteria is not None, f"Opportunity missing eligibility_criteria: {opportunity}"
        assert opportunity.visibility_level is not None, f"Opportunity missing visibility_level: {opportunity}"
        assert opportunity.impact_level is not None, f"Opportunity missing impact_level: {opportunity}"
        assert opportunity.category is not None, f"Opportunity missing category: {opportunity}"
        
        # Verify eligibility criteria has required fields
        criteria = opportunity.eligibility_criteria
        assert criteria.education_levels is not None, \
            f"Opportunity {opportunity.name} has None education_levels"
        assert isinstance(criteria.education_levels, list), \
            f"Opportunity {opportunity.name} education_levels is not a list"
        assert len(criteria.education_levels) > 0, \
            f"Opportunity {opportunity.name} has empty education_levels list"
        
        # Verify all education levels are valid EducationLevel enum values
        for edu_level in criteria.education_levels:
            assert isinstance(edu_level, EducationLevel), \
                f"Opportunity {opportunity.name} has invalid education level: {edu_level}"
        
        # Verify optional fields are properly typed when present
        if criteria.fields_of_study is not None:
            assert isinstance(criteria.fields_of_study, list), \
                f"Opportunity {opportunity.name} fields_of_study is not a list"
        
        if criteria.institution_types is not None:
            assert isinstance(criteria.institution_types, list), \
                f"Opportunity {opportunity.name} institution_types is not a list"
        
        if criteria.background_requirements is not None:
            assert isinstance(criteria.background_requirements, list), \
                f"Opportunity {opportunity.name} background_requirements is not a list"
        
        # Verify boolean fields are properly typed
        assert isinstance(criteria.income_based, bool), \
            f"Opportunity {opportunity.name} income_based is not a boolean"
        assert isinstance(criteria.merit_based, bool), \
            f"Opportunity {opportunity.name} merit_based is not a boolean"
        
        # Verify visibility and impact levels are valid enum values
        assert isinstance(opportunity.visibility_level, VisibilityLevel), \
            f"Opportunity {opportunity.name} has invalid visibility_level: {opportunity.visibility_level}"
        assert isinstance(opportunity.impact_level, ImpactLevel), \
            f"Opportunity {opportunity.name} has invalid impact_level: {opportunity.impact_level}"


# Strategy for generating opportunities with valid structure
@st.composite
def valid_opportunity_strategy(draw):
    """Generate a valid opportunity with proper structure."""
    return Opportunity(
        id=draw(st.text(min_size=1, max_size=50).filter(lambda x: x.strip())),
        name=draw(st.text(min_size=1, max_size=100).filter(lambda x: x.strip())),
        description=draw(st.text(min_size=1, max_size=500).filter(lambda x: x.strip())),
        eligibility_criteria=EligibilityCriteria(
            education_levels=draw(st.lists(
                st.sampled_from(list(EducationLevel)),
                min_size=1,
                max_size=4
            )),
            fields_of_study=draw(st.one_of(
                st.none(),
                st.lists(st.text(min_size=1, max_size=50), min_size=1, max_size=5)
            )),
            institution_types=draw(st.one_of(st.none(), st.just([]))),
            background_requirements=draw(st.one_of(st.none(), st.just([]))),
            income_based=draw(st.booleans()),
            merit_based=draw(st.booleans()),
        ),
        visibility_level=draw(st.sampled_from(list(VisibilityLevel))),
        impact_level=draw(st.sampled_from(list(ImpactLevel))),
        category=draw(st.sampled_from(["Scholarship", "Internship", "Research", "Exam", "Program"])),
    )


@given(valid_opportunity_strategy())
def test_property_valid_opportunity_structure(opportunity):
    """
    Property 6: Knowledge Base Structure Integrity - Valid opportunities have required fields.
    
    For any opportunity with valid structure, it must have all required fields
    including non-empty education_levels list.
    
    Validates: Requirements 5.2
    """
    # Verify all required fields are present
    assert opportunity.id is not None and opportunity.id.strip()
    assert opportunity.name is not None and opportunity.name.strip()
    assert opportunity.description is not None and opportunity.description.strip()
    assert opportunity.eligibility_criteria is not None
    assert opportunity.visibility_level is not None
    assert opportunity.impact_level is not None
    assert opportunity.category is not None
    
    # Verify eligibility criteria structure
    criteria = opportunity.eligibility_criteria
    assert criteria.education_levels is not None
    assert isinstance(criteria.education_levels, list)
    assert len(criteria.education_levels) > 0
    
    # Verify all education levels are valid
    for edu_level in criteria.education_levels:
        assert isinstance(edu_level, EducationLevel)
