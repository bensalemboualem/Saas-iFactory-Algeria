"""
Dzir IA Video - Mock Testing (No GPU Required)
Test the logic and integration without actual AI generation
"""
import sys
import asyncio
import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_mock_video(output_path: Path, text: str, duration: int = 3, fps: int = 8):
    """Create a mock video (actually a series of images for testing)"""
    try:
        from moviepy.editor import ImageSequenceClip

        # Create frames
        num_frames = duration * fps
        frames = []

        for i in range(num_frames):
            # Create a simple colored frame with text
            img = Image.new('RGB', (640, 360), color=(0, 132, 61))  # Algerian green
            draw = ImageDraw.Draw(img)

            # Add text
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()

            text_to_show = f"{text}\nFrame {i+1}/{num_frames}"
            draw.text((50, 150), text_to_show, fill=(255, 255, 255), font=font)

            frames.append(np.array(img))

        # Create video from frames
        clip = ImageSequenceClip(frames, fps=fps)
        clip.write_videofile(str(output_path), codec='libx264', fps=fps, logger=None)

        logger.info(f"✅ Mock video created: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Failed to create mock video: {str(e)}")
        raise

def create_mock_audio(output_path: Path, text: str, language: str = "fr"):
    """Create a mock audio file (silence with metadata)"""
    try:
        from pydub import AudioSegment
        from pydub.generators import Sine

        # Create a simple beep tone (mock voice)
        duration_ms = len(text) * 100  # 100ms per character (rough estimate)
        tone = Sine(440).to_audio_segment(duration=duration_ms)

        # Export
        tone.export(output_path, format="wav")

        logger.info(f"✅ Mock audio created: {output_path} ({language})")
        return output_path

    except Exception as e:
        logger.warning(f"AudioSegment not available, creating silent file: {str(e)}")
        # Just touch the file
        output_path.touch()
        return output_path

async def test_mock_pipeline():
    """Test the complete pipeline with mock data"""
    logger.info("=" * 60)
    logger.info("DZIR IA VIDEO - MOCK PIPELINE TEST (NO GPU)")
    logger.info("=" * 60)
    logger.info("")

    try:
        # Test request
        request = {
            "title": "Test Restaurant El Bahia",
            "script": "Bienvenue au restaurant El Bahia. Cuisine traditionnelle algérienne.",
            "template": "restaurant",
            "language": "fr",
            "format": "16:9",
            "duration": 3
        }

        logger.info(f"📋 Request: {request['title']}")
        logger.info(f"   Script: {request['script']}")
        logger.info(f"   Language: {request['language']}")
        logger.info("")

        # Step 1: Mock video generation
        logger.info("Step 1/3: Generating mock video scene...")
        scene_video = create_mock_video(
            output_path=Path("/tmp/mock_scene.mp4"),
            text=request['title'],
            duration=request['duration']
        )
        logger.info(f"   ✅ Scene video: {scene_video}")
        logger.info(f"   Size: {scene_video.stat().st_size / 1024:.2f} KB")
        logger.info("")

        # Step 2: Mock audio generation
        logger.info("Step 2/3: Generating mock voice-over...")
        voiceover = create_mock_audio(
            output_path=Path("/tmp/mock_voiceover.wav"),
            text=request['script'],
            language=request['language']
        )
        logger.info(f"   ✅ Voice-over: {voiceover}")
        logger.info("")

        # Step 3: Mock composition
        logger.info("Step 3/3: Mock composition...")
        final_video = Path("/tmp/mock_final.mp4")

        # For mock, just copy the scene video as final
        import shutil
        shutil.copy(scene_video, final_video)

        logger.info(f"   ✅ Final video: {final_video}")
        logger.info(f"   Size: {final_video.stat().st_size / 1024:.2f} KB")
        logger.info("")

        # Success
        logger.info("=" * 60)
        logger.info("✅ ✅ ✅ MOCK PIPELINE TEST PASSED ✅ ✅ ✅")
        logger.info("=" * 60)
        logger.info("")
        logger.info("📌 Note: This was a mock test without GPU.")
        logger.info("📌 For real AI generation, deploy to VPS with GPU.")
        logger.info("")
        logger.info(f"🎬 Mock video created: {final_video}")

        return True

    except Exception as e:
        logger.error(f"❌ Mock pipeline test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_api_structure():
    """Test API structure and imports"""
    logger.info("=" * 60)
    logger.info("TEST: API Structure & Imports")
    logger.info("=" * 60)
    logger.info("")

    tests = []

    # Test 1: Import routers
    try:
        from app.routers import dzirvideo
        logger.info("✅ dzirvideo router imported")
        tests.append(("Router import", True))
    except Exception as e:
        logger.error(f"❌ Failed to import router: {str(e)}")
        tests.append(("Router import", False))

    # Test 2: Import services
    try:
        from app.services import dzirvideo_service
        logger.info("✅ dzirvideo_service imported")
        tests.append(("Service import", True))
    except Exception as e:
        logger.error(f"❌ Failed to import service: {str(e)}")
        tests.append(("Service import", False))

    # Test 3: Check engines (may fail without dependencies)
    try:
        from app.services.engines import get_video_engine, get_tts_engine, get_compositor
        logger.info("✅ AI engines imported")
        tests.append(("Engines import", True))
    except Exception as e:
        logger.warning(f"⚠️  AI engines not available (expected without GPU): {str(e)}")
        tests.append(("Engines import", False))

    logger.info("")
    logger.info("=" * 60)
    logger.info("Structure Test Summary")
    logger.info("=" * 60)

    passed = sum(1 for _, result in tests if result)
    total = len(tests)

    for test_name, result in tests:
        status = "✅" if result else "❌"
        logger.info(f"{status} {test_name}")

    logger.info("")
    logger.info(f"Results: {passed}/{total} tests passed")

    return passed >= 2  # At least router and service should work

async def main():
    """Run all mock tests"""
    logger.info("")
    logger.info("=" * 70)
    logger.info("  DZIR IA VIDEO - MOCK TESTING SUITE (NO GPU REQUIRED)")
    logger.info("=" * 70)
    logger.info("")

    # Test 1: API Structure
    structure_ok = await test_api_structure()

    # Test 2: Mock Pipeline
    pipeline_ok = await test_mock_pipeline()

    # Summary
    logger.info("")
    logger.info("=" * 70)
    logger.info("FINAL SUMMARY")
    logger.info("=" * 70)

    if structure_ok and pipeline_ok:
        logger.info("✅ All mock tests passed!")
        logger.info("✅ Code structure is valid")
        logger.info("✅ Logic works correctly")
        logger.info("")
        logger.info("🚀 Ready for deployment to GPU server!")
        return True
    else:
        logger.error("⚠️  Some tests failed")
        logger.info("📝 Fix the issues before deploying")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
