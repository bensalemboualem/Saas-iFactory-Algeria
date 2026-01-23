"""
Text-to-Video Generators
20 tools for generating videos from text prompts
"""

from .wan_2_1 import WAN21Generator
from .kling_ai import KlingAIGenerator
from .pika_labs import PikaLabsGenerator
from .luma_dream import LumaDreamGenerator
from .hailuo_ai import HailuoAIGenerator
from .runway_gen4 import RunwayGen4Generator
from .veo_2 import Veo2Generator
from .sora import SoraGenerator
from .ltx_studio import LTXStudioGenerator
from .cogvideo import CogVideoGenerator
from .open_sora import OpenSoraGenerator
from .starryai_video import StarryAIVideoGenerator
from .hunyuan_video import HunyuanVideoGenerator
from .mochi_1 import Mochi1Generator
from .vidu_ai import ViduAIGenerator
from .pollo_ai import PolloAIGenerator
from .krea_video import KreaVideoGenerator
from .hailuo_2_3 import Hailuo23Generator
from .nano import NanoGenerator
from .banan_pro import BananProGenerator

__all__ = [
    "WAN21Generator",
    "KlingAIGenerator",
    "PikaLabsGenerator",
    "LumaDreamGenerator",
    "HailuoAIGenerator",
    "RunwayGen4Generator",
    "Veo2Generator",
    "SoraGenerator",
    "LTXStudioGenerator",
    "CogVideoGenerator",
    "OpenSoraGenerator",
    "StarryAIVideoGenerator",
    "HunyuanVideoGenerator",
    "Mochi1Generator",
    "ViduAIGenerator",
    "PolloAIGenerator",
    "KreaVideoGenerator",
    "Hailuo23Generator",
    "NanoGenerator",
    "BananProGenerator",
]
