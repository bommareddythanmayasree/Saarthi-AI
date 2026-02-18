# 🚀 Saarthi AI  
### Guiding students to opportunities they didn’t know existed.

Saarthi AI is an AI-powered Opportunity Discovery Platform designed to identify awareness blindspots and help students uncover scholarships, internships, research programs, skill initiatives, and government schemes they are eligible for — but often unaware of.

Unlike traditional portals that only list opportunities, Saarthi AI first detects what students are likely unaware of, and then generates explainable, personalized recommendations.

---

# 📌 Problem Statement

Many students miss high-impact opportunities not because they lack eligibility, but because they lack awareness.

This creates an **Awareness Inequality Gap**, especially affecting:

- Rural students  
- First-generation learners  
- Government college students  
- Financially constrained students  

Students often rely on:
- WhatsApp groups  
- Friends and seniors  
- Limited college notices  

As a result, they miss scholarships, internships, and programs simply because they didn’t know they existed.

> Saarthi AI addresses the “I don’t know what I don’t know” problem.

---

# 💡 Solution Overview

Saarthi AI follows a structured AI reasoning pipeline:

1. Collect structured student information  
2. Generate a student profile object  
3. Identify opportunity blindspots  
4. Match low-visibility opportunities  
5. Generate explainable recommendations  
6. Provide a personalized insight summary  

The system focuses on **awareness-first discovery**, not just eligibility filtering.

---

# 🧠 Core Capabilities

- ✔ AI-based Blindspot Detection  
- ✔ Personalized Opportunity Matching  
- ✔ Explainable Recommendation Generation  
- ✔ Low-Awareness Opportunity Prioritization  
- ✔ Inclusive and Accessible UI Design  
- ✔ Lightweight Hackathon-Ready Architecture  

---

# 🖥️ Application Flow

1. **Landing Page** – Product introduction and call-to-action  
2. **Login Page** – Secure access or guest mode  
3. **Student Information Form** – Google-form-style structured input  
4. **AI Results Dashboard (Single Screen)**:
   - Profile Understanding  
   - Blindspot Analysis  
   - Recommended Opportunities  
   - Final Insight Summary  

---

# 🏗️ System Architecture

## 🔹 High-Level Architecture

|---------------|
|Student UI (Form Interface)| 
|Student Profile Structuring Module |
| Blindspot Detection Engine |
| Opportunity Dataset (Curated Mock Data) |
| Recommendation & Explainability Layer |
| AI Results Dashboard |


---

## 🔹 Process Flow

Student Input
      ↓
Profile Structuring
      ↓
Blindspot Identification
      ↓
Eligibility Filtering
      ↓
Low-Awareness Prioritization
      ↓
Explainable Recommendation Generation
      ↓
Personalized Insight Output
---

# 🧩 Core Modules
## 1️⃣ Student Profile Generator
Converts form inputs into structured profile:

{
  "name": "",
  "age": "",
  "education_level": "",
  "degree": "",
  "field": "",
  "year": "",
  "institution_type": "",
  "background": [],
  "goals": [],
  "missed_before": "",
  "additional_context": ""
}
---
## 2️⃣ Blindspot Detection Engine (Core Innovation)

The Blindspot Detection Engine is the central innovation of Saarthi AI.  
Instead of directly listing opportunities, the system first identifies categories of opportunities that a student is likely unaware of.

This detection is based on:

- Background indicators (rural, first-generation, financial need, etc.)
- Awareness signals (history of missing opportunities)
- Institution type (government, private, etc.)
- Exposure patterns (how students typically receive information)
- Historical miss indicators

Based on these signals, the system identifies blindspot categories such as:

- Government Scholarships
- Short-Window Internships
- Low-Promotion Skill Programs
- Region-Specific Schemes
- Research Initiatives

This ensures the platform focuses on awareness gaps rather than simple eligibility filtering.

---

## 3️⃣ Opportunity Matching Engine

The Opportunity Matching Engine filters and ranks opportunities from a curated dataset using structured eligibility and prioritization logic.

Filtering is based on:

- Education level
- Field compatibility
- Background prioritization
- Goal alignment
- Awareness level
- Miss probability

The final selection prioritizes:

> **Low Awareness + High Impact + Eligibility Match**

This ensures students are shown opportunities that are both relevant and commonly overlooked.

---

## 4️⃣ Explainability Layer

Saarthi AI does not generate black-box recommendations.

For each recommended opportunity, the system clearly explains:

- Why it fits the student
- Why students usually miss it
- Miss Probability (High / Medium / Low)
- Suggested next steps
This transparent approach builds trust and ensures students understand not just what to apply for, but why it matters.

---

## 🎨 MVP Screenshots
<img width="1920" height="2602" alt="SaarthiAI-Discover-Opportunities-You-Didn-t-Know-Existed (1)" src="https://github.com/user-attachments/assets/ba58eac2-a893-43b2-b1c3-64edc03dcf72" />

---

## 🚀 Future Enhancements

   a.Real-time opportunity ingestion
   b.Automated government portal scraping
   c.Deadline tracking system
   d.Personalized reminders
   e.State-wise recommendation engine
   f.Multi-language support
---
## Live Demo Link: https://saarthi-ai-t3y3.onrender.com
