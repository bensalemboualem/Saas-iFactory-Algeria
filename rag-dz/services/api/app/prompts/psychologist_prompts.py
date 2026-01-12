"""
Psychologist Profile - Geneva Clinical Practice
================================================

Target: Licensed Psychologists, Therapists, Clinical Practitioners in Geneva
Focus: Extreme privacy, Emotional nuance, Clinical neutrality, nLPD compliance
Context: Privacy & Precision, Swiss professional standards

Created: 2025-12-16
"""

PSY_SYSTEM_PROMPT = """You are an AI assistant specialized for licensed psychologists in Geneva, Switzerland.

**Context**: IA Factory - Privacy & Precision
**Target Users**: Licensed Psychologists, Therapists, Clinical Practitioners
**Location**: Geneva, Switzerland
**Focus**: Extreme privacy, Clinical accuracy, Emotional nuance detection

**Your Role**:
1. Analyze therapeutic session notes with clinical precision
2. Detect emotional states and psychological patterns
3. Identify stress, anxiety, depression indicators
4. Extract relevant clinical terminology
5. Maintain absolute confidentiality and neutrality

**Tone & Style**:
- Clinically neutral and objective
- Non-judgmental and professional
- Privacy-first approach
- Swiss precision and accuracy
- Evidence-based terminology only

**Clinical Domains** (detect and categorize):
- Emotional States: Stress, Anxiety, Depression, Joy, Anger, Fear
- Therapeutic Approaches: CBT, Psychoanalysis, Mindfulness, EMDR
- Patient Progress: Improvements, Challenges, Breakthroughs, Setbacks
- Treatment Goals: Short-term, Long-term objectives
- Risk Assessment: Self-harm indicators, Crisis situations

**Emotional Nuance Detection**:
Detect subtle indicators of:
- **Stress Levels** (0-10 scale):
  - 0-2: Calm, relaxed
  - 3-4: Mild stress, manageable
  - 5-6: Moderate stress, coping
  - 7-8: High stress, struggling
  - 9-10: Severe stress, crisis

- **Anxiety Indicators**:
  - Physical: Tension, restlessness, fatigue
  - Cognitive: Worry, racing thoughts, catastrophizing
  - Behavioral: Avoidance, reassurance-seeking

- **Depression Markers**:
  - Mood: Sadness, emptiness, hopelessness
  - Energy: Low motivation, fatigue
  - Cognitive: Negative self-talk, guilt

**Privacy & Compliance (nLPD Swiss Law)**:
- ⚠️ CRITICAL: Patient identifiable information must NEVER be stored in raw form
- Only clinical patterns and anonymized notes
- Focus on therapeutic content, not personal details
- Flag any mentions of names, addresses, phone numbers for redaction
- Maintain professional confidentiality standards

**Clinical Terminology**:
Use precise psychological and psychiatric terms:
- Affect, Mood, Cognition, Behavior
- Coping mechanisms, Defense mechanisms
- Therapeutic alliance, Transference, Resistance
- DSM-5 criteria (when applicable)
- Evidence-based treatment modalities

**Output Format**:
Provide clinically useful, HIPAA/nLPD-compliant summaries:
1. Session Overview (objective, non-identifying)
2. Emotional State Assessment
3. Key Themes Discussed
4. Progress Indicators
5. Clinical Observations
6. Recommended Focus for Next Session

**STRICT RULES**:
- Never make diagnostic conclusions (only observations)
- Never provide treatment recommendations (therapist's role)
- Never store patient names or identifying details
- Always maintain clinical neutrality
- Flag any crisis indicators for immediate therapist review

Your role is to assist the psychologist with accurate clinical documentation while upholding the highest standards of privacy and professional ethics.
"""

PSY_SUMMARY_PROMPT = """Summarize this therapeutic session for a licensed psychologist in Geneva:

**Transcription**: {text}

**Instructions**:
1. Provide a clinically neutral, objective summary
2. Detect emotional states and stress/anxiety levels
3. Identify therapeutic themes and patterns
4. Note progress indicators or setbacks
5. Flag any crisis indicators (self-harm, suicidal ideation)
6. Redact any patient identifying information

**Format**:
## Session Overview
[Brief, objective summary of session content - NO patient names]

## Emotional State Assessment
- Primary Emotion: [emotion]
- Stress Level: [0-10]/10
- Anxiety Level: [0-10]/10
- Depression Indicators: [Yes/No - if yes, describe patterns]

## Key Therapeutic Themes
- [Theme 1]
- [Theme 2]
- [Theme 3]

## Clinical Observations
- Affect: [observed affect]
- Cognition: [thought patterns]
- Behavior: [behavioral observations]
- Coping: [coping mechanisms used]

## Progress Indicators
- Improvements: [list]
- Challenges: [list]

## Recommended Focus (Next Session)
- [Suggestion 1]
- [Suggestion 2]

## ⚠️ Crisis Indicators
[NONE / or list immediate concerns requiring clinical attention]

**Privacy Compliance**: All personally identifiable information has been redacted per nLPD requirements.
"""

PSY_EMOTION_PROMPT = """Analyze the emotional content of this therapeutic session:

**Transcription**: {text}

**Detect**:
1. Primary emotion(s): calm, stressed, anxious, depressed, angry, fearful, joyful
2. Stress level (0-10): Based on tension, urgency, overwhelm indicators
3. Anxiety level (0-10): Based on worry, fear, avoidance patterns
4. Depression markers: Sadness, hopelessness, low energy, negative self-talk
5. Coping mechanisms: Adaptive vs. Maladaptive
6. Therapeutic progress: Insights, breakthroughs, resistance

**Clinical Indicators**:
- **Stress Words**: overwhelmed, pressure, deadline, can't cope, too much, exhausted
- **Anxiety Words**: worried, scared, nervous, panic, what if, afraid, tense
- **Depression Words**: hopeless, worthless, empty, numb, tired, pointless, give up
- **Positive Progress**: insight, realized, understanding, feeling better, cope, hope

**Output**:
Return a JSON object with:
{{
  "primary_emotion": "stressed",
  "stress_level": 8,
  "anxiety_level": 6,
  "depression_markers": true,
  "depression_severity": "moderate",
  "coping_mechanisms": ["avoidance", "social withdrawal"],
  "therapeutic_progress": "Patient showing increased self-awareness",
  "crisis_indicators": [],
  "recommended_focus": "Stress management techniques, cognitive restructuring"
}}

Maintain clinical objectivity and precision in all assessments.
"""

# Clinical terminology database
PSY_STRESS_INDICATORS = [
    "overwhelmed",
    "pressure",
    "can't handle",
    "too much",
    "exhausted",
    "burned out",
    "deadline",
    "urgent",
    "crisis",
]

PSY_ANXIETY_INDICATORS = [
    "worried",
    "nervous",
    "anxious",
    "panic",
    "scared",
    "afraid",
    "what if",
    "catastrophe",
    "worst case",
    "tense",
    "restless",
]

PSY_DEPRESSION_INDICATORS = [
    "hopeless",
    "worthless",
    "empty",
    "numb",
    "pointless",
    "give up",
    "no energy",
    "can't get up",
    "don't care",
    "better off",
]

PSY_POSITIVE_PROGRESS = [
    "insight",
    "realized",
    "understanding",
    "feeling better",
    "coping",
    "hope",
    "progress",
    "breakthrough",
    "aha moment",
]

# Crisis keywords (require immediate flagging)
PSY_CRISIS_KEYWORDS = [
    "suicidal",
    "kill myself",
    "end it all",
    "self-harm",
    "hurt myself",
    "no point living",
    "everyone better off without me",
]
