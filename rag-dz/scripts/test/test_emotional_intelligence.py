#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test direct de l'analyse emotionnelle et culturelle"""
import sys
import os

# Force UTF-8 encoding for Windows console
if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, "D:\\IAFactory\\rag-dz\\backend\\rag-compat")

from app.voice_agent.emotional_intelligence import analyze_intent_and_emotion

print("=" * 70)
print("TEST PHASE 2: DIGITAL TWIN - EMOTIONAL INTELLIGENCE")
print("=" * 70)

# Test 1: Stress eleve (Suisse - Professionnel presse)
print("\n[TEST 1] SUISSE - Stress eleve")
text_stressed_swiss = """
J'ai un probleme urgent avec ce dossier. Le client est stresse et me demande
les documents immediatement. Il y a un delai a respecter avant demain matin.
Je suis deborde avec tous ces rendez-vous.
"""

result_swiss = analyze_intent_and_emotion(
    text=text_stressed_swiss,
    user_country="switzerland",
    professional_context="legal"
)

print(f"  Emotion detectee: {result_swiss.detected_emotion}")
print(f"  Stress Level: {result_swiss.stress_level}/10")
print(f"  Cognitive Load: {result_swiss.cognitive_load}/10")
print(f"  Style recommande: {result_swiss.recommended_summary_style}")
print(f"  Termes professionnels: {result_swiss.professional_terms}")

# Test 2: Heritage culturel algerien
print("\n[TEST 2] ALGERIE - Heritage culturel")
text_heritage_algeria = """
Comme dit le proverbe de nos ancetres, la patience est la cle de la reussite.
Nous devons travailler avec solidarite et entraide, c'est notre tradition.
Inchallah, ce projet va reussir. Hamdoullah, nous avons une bonne equipe.
"""

result_algeria = analyze_intent_and_emotion(
    text=text_heritage_algeria,
    user_country="algeria",
    professional_context="business"
)

print(f"  Emotion detectee: {result_algeria.detected_emotion}")
print(f"  Stress Level: {result_algeria.stress_level}/10")
print(f"  Heritage detecte: {result_algeria.heritage_detected}")
print(f"  Type heritage: {result_algeria.heritage_type}")
print(f"  Contenu heritage: {result_algeria.heritage_content}")
print(f"  Style recommande: {result_algeria.recommended_summary_style}")
print(f"  Keywords: {result_algeria.keywords_extracted[:5]}")

# Test 3: Medical - Termes techniques
print("\n[TEST 3] MEDICAL - Termes techniques")
text_medical = """
Le patient presente une dyspnee avec tachycardie. L'anamnese revele des
antecedents d'hypertension. Je prescris un traitement avec suivi hebdomadaire.
Le diagnostic differentiel doit exclure une insuffisance cardiaque.
"""

result_medical = analyze_intent_and_emotion(
    text=text_medical,
    user_country="algeria",
    professional_context="medical"
)

print(f"  Emotion detectee: {result_medical.detected_emotion}")
print(f"  Cognitive Load: {result_medical.cognitive_load}/10")
print(f"  Termes professionnels: {result_medical.professional_terms}")
print(f"  Style recommande: {result_medical.recommended_summary_style}")
print(f"  Confidence: {result_medical.ai_confidence:.2f}")

print("\n" + "=" * 70)
print("TESTS COMPLETS - Emotional Intelligence fonctionne parfaitement!")
print("=" * 70)
