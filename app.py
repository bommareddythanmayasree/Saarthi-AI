"""
Production-ready Flask web application for SaarthiAI.
"""
from flask import Flask, render_template, request, jsonify, session
from saarthi_ai.application_controller import ApplicationController
from saarthi_ai.json_matcher import JSONOpportunityMatcher
from saarthi_ai.models import (
    StudentProfile,
    EducationLevel,
    InstitutionType,
    BackgroundIndicator,
    OpportunityGoal,
    MissedOpportunityFrequency,
)
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Initialize controller and JSON matcher
controller = ApplicationController()
json_matcher = JSONOpportunityMatcher()


@app.route('/')
def index():
    """Home page with welcome screen."""
    return render_template('index.html')


@app.route('/login')
def login():
    """Login page."""
    return render_template('login.html')


@app.route('/signup')
def signup():
    """Signup page - redirects to form for now."""
    return render_template('login.html')


@app.route('/form')
def form():
    """Student information form page."""
    return render_template('form.html')


@app.route('/api/submit', methods=['POST'])
def submit_form():
    """Handle form submission and return results."""
    try:
        data = request.json
        
        # Parse background indicators
        background_indicators = []
        for bg in data.get('background_indicators', []):
            try:
                background_indicators.append(BackgroundIndicator(bg))
            except ValueError:
                pass
        
        # Parse opportunity goals
        opportunity_goals = []
        for goal in data.get('opportunity_goals', []):
            try:
                opportunity_goals.append(OpportunityGoal(goal))
            except ValueError:
                pass
        
        # Create student profile
        profile = StudentProfile(
            name=data.get('name', '').strip(),
            age=int(data.get('age', 0)) if data.get('age') else 0,
            education_level=EducationLevel(data.get('education_level', 'UG')),
            degree=data.get('degree', '').strip(),
            field_of_study=data.get('field_of_study', '').strip(),
            year_of_study=int(data.get('year_of_study', 0)) if data.get('year_of_study') else 0,
            institution_type=InstitutionType(data.get('institution_type', 'Government')),
            background_indicators=background_indicators,
            opportunity_goals=opportunity_goals,
            missed_opportunities_before=MissedOpportunityFrequency(
                data.get('missed_opportunities_before', 'No')
            ),
            gender=data.get('gender', '').strip() or None,
            additional_context=data.get('additional_context', '').strip() or None,
        )
        
        # Process the profile with original controller for blindspots
        result = controller.handle_form_submission(profile)
        
        # Format the response
        if not result['valid']:
            return jsonify({
                'success': False,
                'error': result.get('error'),
                'missing_fields': result.get('missing_fields', []),
                'invalid_fields': result.get('invalid_fields', [])
            }), 400
        
        # Prepare student data for JSON matcher
        student_data = {
            'education_level': profile.education_level.value,
            'field': _normalize_field_of_study(profile.field_of_study),
            'year': _convert_year_to_string(profile.year_of_study),
            'institution_type': profile.institution_type.value,
            'background': _get_primary_background(background_indicators, profile.gender)
        }
        
        # Match opportunities using JSON matcher
        matched_opportunities = json_matcher.match_opportunities(student_data)
        
        # Format blindspots
        blindspots_data = [
            {
                'category': b.category,
                'reason': b.reason,
                'relevance_score': b.relevance_score
            }
            for b in result['blindspots']
        ]
        
        # Format matched opportunities for UI
        if matched_opportunities:
            matches_data = [
                {
                    'name': opp['opportunity_name'],
                    'category': opp['category'],
                    'description': opp['description'],
                    'impact_level': opp['impact_level'],
                    'why_missed': opp['why_missed'],
                    'matching_score': opp['matching_score'],
                    'awareness_level': opp.get('awareness_level', 'Medium'),
                    'miss_probability': opp.get('miss_probability', 'Medium')
                }
                for opp in matched_opportunities
            ]
            
            return jsonify({
                'success': True,
                'profile_summary': result['profile_summary'],
                'blindspots': blindspots_data,
                'matches': matches_data,
                'final_insight': result['final_insight'],
                'no_matches': False
            })
        else:
            # No matches found
            return jsonify({
                'success': True,
                'profile_summary': result['profile_summary'],
                'blindspots': blindspots_data,
                'matches': [],
                'final_insight': "No hidden opportunities found for your profile yet. Saarthi AI will notify you when new ones match.",
                'no_matches': True
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500


def _convert_year_to_string(year: int) -> str:
    """Convert numeric year to string format used in JSON (1st, 2nd, 3rd, Final, Any)."""
    if year == 1:
        return '1st'
    elif year == 2:
        return '2nd'
    elif year == 3:
        return '3rd'
    elif year >= 4:
        return 'Final'
    else:
        return 'Any'


def _normalize_field_of_study(field: str) -> str:
    """
    Normalize field of study to match JSON format.
    Maps various field names to standard categories in opportunities.json.
    """
    field_lower = field.lower().strip()
    
    # Engineering variations
    if any(term in field_lower for term in ['engineering', 'engineer', 'tech', 'b.tech', 'btech']):
        return 'Engineering'
    
    # Science variations
    if any(term in field_lower for term in ['science', 'physics', 'chemistry', 'biology', 'bsc', 'b.sc']):
        return 'Science'
    
    # Commerce variations
    if any(term in field_lower for term in ['commerce', 'bcom', 'b.com', 'accounting', 'finance']):
        return 'Commerce'
    
    # Computer Science (subset of Engineering but sometimes separate)
    if any(term in field_lower for term in ['computer', 'cs', 'it', 'information technology']):
        return 'Engineering'
    
    # Return original if no match (will match "Any" fields)
    return field


def _get_primary_background(background_indicators: list, gender: str = None) -> str:
    """
    Get primary background indicator for matching.
    Maps BackgroundIndicator enum to JSON format.
    
    Args:
        background_indicators: List of BackgroundIndicator enums
        gender: Student's gender (to check for Women category)
    """
    # Check for Women first (highest priority for gender-specific scholarships)
    if gender and gender.lower() == 'female':
        return 'Women'
    
    if not background_indicators:
        return 'Any'
    
    # Priority mapping for other backgrounds
    priority_map = {
        BackgroundIndicator.FINANCIAL_SUPPORT: 'Financial Need',
        BackgroundIndicator.FIRST_GENERATION: 'Financial Need',
        BackgroundIndicator.RURAL: 'Rural',
        BackgroundIndicator.DISABLED: 'Any',  # Specific scholarships handle this
        BackgroundIndicator.MINORITY: 'Any'
    }
    
    # Return first matching priority
    for indicator in background_indicators:
        if indicator in priority_map:
            mapped = priority_map[indicator]
            if mapped != 'Any':
                return mapped
    
    return 'Any'


@app.route('/results')
def results():
    """Results page showing all insights."""
    return render_template('results.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
