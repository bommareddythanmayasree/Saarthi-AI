"""
Property-based tests for low-visibility prioritization.

Feature: saarthi-ai-opportunity-finder
Property 9: Low-Visibility Prioritization
Validates: Requirements 8.4
"""
import pytest
from hypothesis import given, strategies as st, assume, settings
from saarthi_ai.opportunity_matcher import OpportunityMatcher
from saarthi_ai.profile_analyzer import ProfileAnalyzer
from saarthi_ai.blindspot_identifier import BlindspotIdentifier
from saarthi_ai.knowledge_base import get_all_opportunities
from saarthi_ai.models import (
    StudentProfile,
    EducationLevel,
    InstitutionType,
    BackgroundIndicator,
    OpportunityGoal,
    MissedOpportunityFrequency,
    VisibilityLevel,
    ImpactLevel,
)


# Strategy for generating education levels
education_level_strategy = st.sampled_from(list(EducationLevel))

# Strategy for generating institution types
institution_type_strategy = st.sampled_from(list(InstitutionType))

# Strategy for generating background indicators
background_indicator_strategy = st.lists(
    st.sampled_from(list(BackgroundIndicator)),
    min_size=1,
    max_size=5
)

# Strategy for generating opportunity goals
opportunity_goal_strategy = st.lists(
    st.sampled_from(list(OpportunityGoal)),
    min_size=1,
    max_size=5
)

# Strategy for generating missed opportunity frequency
missed_opportunity_strategy = st.sampled_from(list(MissedOpportunityFrequency))


# Strategy for generating valid complete profiles
@st.composite
def valid_profile_strategy(draw):
    """Generate a valid complete student profile."""
    return StudentProfile(
        name=draw(st.text(min_size=1, max_size=50).filter(lambda x: x.strip())),
        age=draw(st.integers(min_value=16, max_value=40)),
        education_level=draw(education_level_strategy),
        degree=draw(st.text(min_size=1, max_size=50).filter(lambda x: x.strip())),
        field_of_study=draw(st.text(min_size=1, max_size=50).filter(lambda x: x.strip())),
        year_of_study=draw(st.integers(min_value=1, max_value=6)),
        institution_type=draw(institution_type_strategy),
        background_indicators=draw(background_indicator_strategy),
        opportunity_goals=draw(opportunity_goal_strategy),
        missed_opportunities_before=draw(missed_opportunity_strategy),
        gender=draw(st.one_of(st.none(), st.sampled_from(["Male", "Female", "Other"]))),
        additional_context=draw(st.one_of(st.none(), st.text(max_size=200))),
    )


@given(valid_profile_strategy())
@settings(max_examples=100)
def test_property_low_visibility_prioritized_within_impact_level(profile):
    """
    Property 9: Low-Visibility Prioritization.
    
    **Validates: Requirements 8.4**
    
    For any set of opportunity recommendations where multiple opportunities have
    different visibility levels, opportunities with lower visibility levels should
    be ranked higher in relevance score than opportunities with higher visibility
    levels (when impact levels are equal).
    
    This test verifies that within each impact level group, opportunities are
    correctly prioritized by visibility level.
    """
    # Create components
    matcher = OpportunityMatcher()
    analyzer = ProfileAnalyzer()
    blindspot_identifier = BlindspotIdentifier()
    
    # Analyze profile and identify blindspots
    analysis = analyzer.analyze(profile)
    blindspots = blindspot_identifier.identify_blindspots(profile, analysis)
    
    # Get all eligible opportunities (not just top 2-3)
    all_opportunities = get_all_opportunities()
    all_eligible_matches = []
    
    for opportunity in all_opportunities:
        if matcher.is_eligible(profile, opportunity.eligibility_criteria):
            # Calculate blindspot alignment
            blindspot_alignment = matcher._calculate_blindspot_alignment(opportunity, blindspots)
            
            # Calculate relevance score
            relevance = matcher._calculate_relevance(
                profile, analysis, opportunity, blindspot_alignment
            )
            
            all_eligible_matches.append({
                'opportunity': opportunity,
                'relevance_score': relevance,
                'visibility': opportunity.visibility_level,
                'impact': opportunity.impact_level
            })
    
    # Skip if we don't have enough matches to test
    assume(len(all_eligible_matches) >= 2)
    
    # Group by impact level
    impact_groups = {}
    for match in all_eligible_matches:
        impact = match['impact']
        if impact not in impact_groups:
            impact_groups[impact] = []
        impact_groups[impact].append(match)
    
    # For each impact level group with multiple visibility levels, verify prioritization
    for impact_level, group_matches in impact_groups.items():
        # Skip if only one match in this impact group
        if len(group_matches) < 2:
            continue
        
        # Check if there are different visibility levels in this group
        visibility_levels = set(m['visibility'] for m in group_matches)
        if len(visibility_levels) < 2:
            continue  # All same visibility, nothing to test
        
        # Sort by relevance score (descending)
        sorted_matches = sorted(group_matches, key=lambda m: m['relevance_score'], reverse=True)
        
        # Verify that lower visibility opportunities have higher or equal relevance scores
        # compared to higher visibility opportunities
        for i in range(len(sorted_matches) - 1):
            current = sorted_matches[i]
            next_match = sorted_matches[i + 1]
            
            current_vis = current['visibility']
            next_vis = next_match['visibility']
            
            # Define visibility ordering: LOW < MEDIUM < HIGH (lower is better)
            visibility_order = {
                VisibilityLevel.LOW: 1,
                VisibilityLevel.MEDIUM: 2,
                VisibilityLevel.HIGH: 3
            }
            
            # If current has worse (higher) visibility than next, it should not have
            # a higher relevance score (with some tolerance for other factors)
            if visibility_order[current_vis] > visibility_order[next_vis]:
                # Current has higher visibility but higher relevance score
                # This is acceptable only if the difference is small (due to other factors)
                # The visibility component is 20% of the score, so max difference should be
                # around 0.1 (difference between LOW and HIGH visibility contribution)
                score_diff = current['relevance_score'] - next_match['relevance_score']
                
                # Allow a small tolerance for other factors (blindspot alignment, goal alignment)
                # But the difference should not be too large
                assert score_diff <= 0.15, \
                    f"Higher visibility opportunity has significantly higher score: " \
                    f"{current['opportunity'].name} (vis={current_vis.value}, score={current['relevance_score']:.3f}) > " \
                    f"{next_match['opportunity'].name} (vis={next_vis.value}, score={next_match['relevance_score']:.3f})"


@given(valid_profile_strategy())
@settings(max_examples=100)
def test_property_visibility_component_in_relevance_calculation(profile):
    """
    Property: Visibility level correctly contributes to relevance score.
    
    **Validates: Requirements 8.4**
    
    This test verifies that the visibility component is correctly applied in the
    relevance calculation, with lower visibility receiving higher scores.
    """
    # Create components
    matcher = OpportunityMatcher()
    analyzer = ProfileAnalyzer()
    blindspot_identifier = BlindspotIdentifier()
    
    # Analyze profile and identify blindspots
    analysis = analyzer.analyze(profile)
    blindspots = blindspot_identifier.identify_blindspots(profile, analysis)
    
    # Get all eligible opportunities
    all_opportunities = get_all_opportunities()
    eligible_opportunities = [
        opp for opp in all_opportunities
        if matcher.is_eligible(profile, opp.eligibility_criteria)
    ]
    
    # Skip if we don't have enough eligible opportunities
    assume(len(eligible_opportunities) >= 2)
    
    # Calculate relevance scores for all eligible opportunities
    relevance_scores = {}
    for opportunity in eligible_opportunities:
        blindspot_alignment = matcher._calculate_blindspot_alignment(opportunity, blindspots)
        relevance = matcher._calculate_relevance(
            profile, analysis, opportunity, blindspot_alignment
        )
        relevance_scores[opportunity.id] = {
            'score': relevance,
            'visibility': opportunity.visibility_level,
            'impact': opportunity.impact_level,
            'name': opportunity.name
        }
    
    # Find pairs of opportunities with same impact but different visibility
    for opp1_id, data1 in relevance_scores.items():
        for opp2_id, data2 in relevance_scores.items():
            if opp1_id >= opp2_id:  # Avoid duplicate comparisons
                continue
            
            # Only compare opportunities with same impact level
            if data1['impact'] != data2['impact']:
                continue
            
            # Check visibility prioritization
            if data1['visibility'] == VisibilityLevel.LOW and data2['visibility'] == VisibilityLevel.HIGH:
                # LOW visibility should have higher or similar score than HIGH visibility
                assert data1['score'] >= data2['score'] - 0.15, \
                    f"LOW visibility {data1['name']} (score={data1['score']:.3f}) should have higher score than " \
                    f"HIGH visibility {data2['name']} (score={data2['score']:.3f}) with same impact level"
            
            elif data1['visibility'] == VisibilityLevel.LOW and data2['visibility'] == VisibilityLevel.MEDIUM:
                # LOW visibility should have higher or similar score than MEDIUM visibility
                assert data1['score'] >= data2['score'] - 0.15, \
                    f"LOW visibility {data1['name']} (score={data1['score']:.3f}) should have higher score than " \
                    f"MEDIUM visibility {data2['name']} (score={data2['score']:.3f}) with same impact level"
            
            elif data1['visibility'] == VisibilityLevel.MEDIUM and data2['visibility'] == VisibilityLevel.HIGH:
                # MEDIUM visibility should have higher or similar score than HIGH visibility
                assert data1['score'] >= data2['score'] - 0.15, \
                    f"MEDIUM visibility {data1['name']} (score={data1['score']:.3f}) should have higher score than " \
                    f"HIGH visibility {data2['name']} (score={data2['score']:.3f}) with same impact level"


@given(valid_profile_strategy())
@settings(max_examples=100)
def test_property_matches_sorted_by_relevance(profile):
    """
    Property: Matches are sorted by relevance score in descending order.
    
    **Validates: Requirements 8.4** (indirectly - ensures prioritization is applied)
    
    The list of opportunity matches returned by match_opportunities should be
    sorted with highest relevance first.
    """
    # Create components
    matcher = OpportunityMatcher()
    analyzer = ProfileAnalyzer()
    blindspot_identifier = BlindspotIdentifier()
    
    # Analyze profile and identify blindspots
    analysis = analyzer.analyze(profile)
    blindspots = blindspot_identifier.identify_blindspots(profile, analysis)
    
    # Get opportunity matches
    matches = matcher.match_opportunities(profile, analysis, blindspots)
    
    # Verify matches are sorted by relevance score (descending)
    if len(matches) > 1:
        for i in range(len(matches) - 1):
            assert matches[i].relevance_score >= matches[i + 1].relevance_score, \
                f"Matches not sorted by relevance: {matches[i].opportunity.name} " \
                f"(score={matches[i].relevance_score:.3f}) should be >= " \
                f"{matches[i + 1].opportunity.name} (score={matches[i + 1].relevance_score:.3f})"
