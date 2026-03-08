"""
Production-ready Flask web application for SaarthiAI.

This module provides a web interface for the SaarthiAI opportunity discovery system.
"""
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import secrets
import logging
from datetime import datetime

from saarthi_ai.application_controller import ApplicationController
from saarthi_ai.models import (
    StudentProfile,
    EducationLevel,
    InstitutionType,
    BackgroundIndicator,
    OpportunityGoal,
    MissedOpportunityFrequency,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asct