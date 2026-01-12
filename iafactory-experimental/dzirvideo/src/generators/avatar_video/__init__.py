"""
Avatar/Talking Head Video Generators
5 tools for creating AI avatars and talking head videos
"""

from .vidnoz import VidnozGenerator
from .deepbrain_ai import DeepBrainAIGenerator
from .elai_io import ElaiIOGenerator
from .heygen import HeyGenGenerator
from .synthesia import SynthesiaGenerator

__all__ = [
    "VidnozGenerator",
    "DeepBrainAIGenerator",
    "ElaiIOGenerator",
    "HeyGenGenerator",
    "SynthesiaGenerator",
]
