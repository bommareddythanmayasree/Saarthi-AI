# Requirements Document

## Introduction

SaarthiAI is an AI-powered opportunity discovery platform designed to help students identify scholarships, internships, research programs, and government initiatives they are eligible for but unaware of. The platform addresses the "I don't know what I don't know" problem by analyzing student profiles and surfacing low-visibility opportunities that students often miss due to poor promotion or lack of guidance.

## Glossary

- **Platform**: The SaarthiAI opportunity discovery system
- **Student**: A user seeking educational and career opportunities
- **Opportunity**: A scholarship, internship, research program, or government initiative
- **Student_Profile**: A structured representation of a student's academic background, skills, interests, and eligibility criteria
- **Recommendation**: A suggested opportunity matched to a student's profile
- **Eligibility_Criteria**: Requirements that must be met to qualify for an opportunity
- **Awareness_Blindspot**: An opportunity a student is eligible for but unaware of
- **Explainability**: A human-readable explanation of why an opportunity was recommended
- **Opportunity_Database**: The collection of all opportunities tracked by the platform

## Requirements

### Requirement 1: Student Profile Management

**User Story:** As a student, I want to create and maintain my profile, so that the platform can accurately match me with relevant opportunities.

#### Acceptance Criteria

1. WHEN a student creates a profile, THE Platform SHALL collect academic background, skills, interests, location, and demographic information
2. WHEN a student updates their profile, THE Platform SHALL persist the changes immediately
3. THE Platform SHALL validate all profile data against defined schemas before storage
4. WHEN profile data is incomplete, THE Platform SHALL identify missing fields that limit matching accuracy
5. THE Platform SHALL support multiple educational levels (high school, undergraduate, graduate, doctoral)

### Requirement 2: Opportunity Data Collection

**User Story:** As a platform administrator, I want to maintain a comprehensive database of opportunities, so that students can discover relevant options.

#### Acceptance Criteria

1. THE Platform SHALL store opportunity details including title, description, eligibility criteria, deadlines, benefits, and application requirements
2. WHEN an opportunity is added, THE Platform SHALL validate all required fields are present
3. THE Platform SHALL support categorization of opportunities by type (scholarship, internship, research program, government initiative)
4. WHEN an opportunity deadline passes, THE Platform SHALL mark the opportunity as expired
5. THE Platform SHALL track opportunity metadata including source, visibility level, and historical application data

### Requirement 3: Intelligent Opportunity Matching

**User Story:** As a student, I want the platform to identify opportunities I'm eligible for, so that I don't miss relevant options due to lack of awareness.

#### Acceptance Criteria

1. WHEN a student profile is complete, THE Platform SHALL analyze eligibility against all active opportunities
2. THE Platform SHALL match students to opportunities based on academic qualifications, skills, interests, location, and demographic criteria
3. WHEN multiple opportunities match a student, THE Platform SHALL rank them by relevance score
4. THE Platform SHALL identify awareness blindspots by surfacing low-visibility opportunities
5. WHEN eligibility criteria are partially met, THE Platform SHALL calculate a match confidence score

### Requirement 4: Explainable Recommendations

**User Story:** As a student, I want to understand why opportunities were recommended to me, so that I can trust the platform's suggestions and make informed decisions.

#### Acceptance Criteria

1. WHEN an opportunity is recommended, THE Platform SHALL provide a human-readable explanation of the match
2. THE Platform SHALL highlight which profile attributes contributed to the recommendation
3. THE Platform SHALL indicate which eligibility criteria the student meets
4. WHEN eligibility is partial, THE Platform SHALL explain what requirements are missing
5. THE Platform SHALL display the relevance score and its contributing factors

### Requirement 5: Opportunity Discovery Interface

**User Story:** As a student, I want to browse and search recommended opportunities, so that I can explore options that match my goals.

#### Acceptance Criteria

1. WHEN a student views their dashboard, THE Platform SHALL display personalized opportunity recommendations
2. THE Platform SHALL support filtering opportunities by type, deadline, location, and benefit amount
3. WHEN a student searches for opportunities, THE Platform SHALL return results ranked by relevance
4. THE Platform SHALL display key opportunity details including deadline, benefits, and match explanation
5. WHEN a student selects an opportunity, THE Platform SHALL show complete details and application requirements

### Requirement 6: Deadline and Notification Management

**User Story:** As a student, I want to be notified about upcoming deadlines and new opportunities, so that I don't miss application windows.

#### Acceptance Criteria

1. WHEN a new opportunity matching a student's profile is added, THE Platform SHALL notify the student
2. WHEN an opportunity deadline is approaching, THE Platform SHALL send reminder notifications
3. THE Platform SHALL allow students to configure notification preferences (email, in-app, frequency)
4. WHEN a student saves an opportunity, THE Platform SHALL track it and provide deadline reminders
5. THE Platform SHALL send notifications at configurable intervals before deadlines (7 days, 3 days, 1 day)

### Requirement 7: Opportunity Tracking

**User Story:** As a student, I want to track opportunities I'm interested in and my application status, so that I can manage my application process effectively.

#### Acceptance Criteria

1. WHEN a student saves an opportunity, THE Platform SHALL add it to their tracked opportunities list
2. THE Platform SHALL allow students to mark application status (not started, in progress, submitted, accepted, rejected)
3. WHEN a student updates application status, THE Platform SHALL persist the change immediately
4. THE Platform SHALL display all tracked opportunities with their current status and deadlines
5. WHEN an opportunity is removed from tracking, THE Platform SHALL stop sending related notifications

### Requirement 8: Profile-Based Eligibility Analysis

**User Story:** As a student, I want to see which eligibility criteria I meet for each opportunity, so that I can assess my chances and identify gaps.

#### Acceptance Criteria

1. WHEN a student views an opportunity, THE Platform SHALL display all eligibility criteria
2. THE Platform SHALL indicate which criteria the student meets based on their profile
3. THE Platform SHALL highlight criteria the student does not meet
4. WHEN eligibility criteria include ranges (GPA, age), THE Platform SHALL validate the student's values against those ranges
5. THE Platform SHALL calculate an overall eligibility percentage for each opportunity

### Requirement 9: Data Privacy and Security

**User Story:** As a student, I want my personal information to be secure and private, so that I can trust the platform with sensitive data.

#### Acceptance Criteria

1. THE Platform SHALL encrypt all student profile data at rest
2. THE Platform SHALL encrypt all data transmissions using TLS
3. WHEN a student deletes their account, THE Platform SHALL remove all personal data within 30 days
4. THE Platform SHALL not share student data with third parties without explicit consent
5. THE Platform SHALL implement authentication and authorization for all user actions

### Requirement 10: Search and Discovery

**User Story:** As a student, I want to search for opportunities beyond recommendations, so that I can explore additional options proactively.

#### Acceptance Criteria

1. THE Platform SHALL support keyword search across opportunity titles, descriptions, and requirements
2. WHEN a student searches, THE Platform SHALL return results ranked by relevance and match score
3. THE Platform SHALL support advanced filters (opportunity type, location, deadline range, benefit amount)
4. WHEN search results are displayed, THE Platform SHALL show match explanations for each result
5. THE Platform SHALL allow students to save search queries for future use
