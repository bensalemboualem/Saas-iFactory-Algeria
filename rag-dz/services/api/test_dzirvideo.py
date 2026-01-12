"""
Dzir IA Video - End-to-End Testing Script
Test complete video generation pipeline
"""
import sys
import asyncio
import logging
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.engines import (
    get_video_engine,
    get_tts_engine,
    get_compositor
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_text_to_video():
    """Test Text-to-Video engine"""
    logger.info("=" * 60)
    logger.info("TEST 1: Text-to-Video Generation")
    logger.info("=" * 60)

    try:
        engine = get_video_engine(engine_type="zeroscope")  # Use Zeroscope for faster testing

        prompt = "Traditional Algerian restaurant in Alger, authentic decoration with zellige tiles, warm ambiance, couscous dishes on tables, cinematic lighting, 4K quality"

        logger.info(f"Generating video from prompt: {prompt[:50]}...")

        video_path = engine.generate_video(
            prompt=prompt,
            num_frames=24,
            fps=8,
            output_path=Path("/tmp/test_video_01.mp4")
        )

        logger.info(f"✅ Video generated successfully: {video_path}")
        logger.info(f"   Size: {video_path.stat().st_size / 1024 / 1024:.2f} MB")

        return video_path

    except Exception as e:
        logger.error(f"❌ Text-to-Video test failed: {str(e)}")
        raise


async def test_text_to_speech():
    """Test Text-to-Speech engine"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("TEST 2: Text-to-Speech Synthesis")
    logger.info("=" * 60)

    try:
        engine = get_tts_engine()

        # Test Arabic
        logger.info("Testing Arabic TTS...")
        text_ar = "مرحبا بكم في مطعم الجزائر. نقدم أفضل الأطباق التقليدية"

        audio_ar = engine.synthesize(
            text=text_ar,
            language="ar",
            output_path=Path("/tmp/test_audio_ar.wav")
        )

        logger.info(f"✅ Arabic TTS: {audio_ar}")
        logger.info(f"   Size: {audio_ar.stat().st_size / 1024:.2f} KB")

        # Test French
        logger.info("Testing French TTS...")
        text_fr = "Bienvenue au restaurant El Bahia. Découvrez notre cuisine traditionnelle algérienne."

        audio_fr = engine.synthesize(
            text=text_fr,
            language="fr",
            output_path=Path("/tmp/test_audio_fr.wav")
        )

        logger.info(f"✅ French TTS: {audio_fr}")
        logger.info(f"   Size: {audio_fr.stat().st_size / 1024:.2f} KB")

        return audio_ar, audio_fr

    except Exception as e:
        logger.error(f"❌ Text-to-Speech test failed: {str(e)}")
        raise


async def test_video_composition():
    """Test Video Composition"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("TEST 3: Video Composition")
    logger.info("=" * 60)

    try:
        compositor = get_compositor()

        # Create sample scenes (mock for testing)
        logger.info("Creating mock scenes for composition...")

        # In real scenario, these would be generated videos
        scene_videos = [
            Path("/tmp/test_video_01.mp4")  # From test 1
        ]

        # Compose video with audio
        logger.info("Composing final video...")

        final_video = compositor.compose_video(
            scene_videos=scene_videos,
            voiceover_audio=Path("/tmp/test_audio_ar.wav"),  # From test 2
            background_music=None,
            aspect_ratio="16:9",
            fps=30,
            add_watermark=True,
            watermark_text="Dzir IA Video - TEST",
            transitions="fade",
            output_path=Path("/tmp/test_final_video.mp4")
        )

        logger.info(f"✅ Video composed successfully: {final_video}")
        logger.info(f"   Size: {final_video.stat().st_size / 1024 / 1024:.2f} MB")

        # Generate thumbnail
        logger.info("Generating thumbnail...")
        thumbnail = compositor.create_thumbnail(
            video_path=final_video,
            timestamp=0.5
        )

        logger.info(f"✅ Thumbnail created: {thumbnail}")

        return final_video, thumbnail

    except Exception as e:
        logger.error(f"❌ Video composition test failed: {str(e)}")
        raise


async def test_full_pipeline():
    """Test complete video generation pipeline"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("TEST 4: Full Pipeline (End-to-End)")
    logger.info("=" * 60)

    try:
        # Simulate full generation request
        request = {
            "title": "Test Restaurant Alger",
            "script": "Bienvenue au restaurant El Bahia. Découvrez nos spécialités algériennes dans une ambiance authentique.",
            "template": "restaurant",
            "language": "fr",
            "format": "16:9",
            "duration": 3
        }

        logger.info(f"Request: {request}")

        # Step 1: Generate video scene
        logger.info("Step 1/3: Generating video scene...")
        video_engine = get_video_engine(engine_type="zeroscope")

        scene_video = video_engine.generate_video(
            prompt=f"Algerian restaurant, {request['script'][:50]}",
            num_frames=24,
            fps=8,
            output_path=Path("/tmp/pipeline_scene.mp4")
        )

        # Step 2: Generate voice-over
        logger.info("Step 2/3: Generating voice-over...")
        tts_engine = get_tts_engine()

        voiceover = tts_engine.synthesize(
            text=request["script"],
            language=request["language"],
            output_path=Path("/tmp/pipeline_voiceover.wav")
        )

        # Step 3: Compose final video
        logger.info("Step 3/3: Composing final video...")
        compositor = get_compositor()

        final_video = compositor.compose_video(
            scene_videos=[scene_video],
            voiceover_audio=voiceover,
            aspect_ratio=request["format"],
            fps=30,
            add_watermark=True,
            output_path=Path("/tmp/pipeline_final.mp4")
        )

        logger.info("")
        logger.info("✅ ✅ ✅ FULL PIPELINE TEST PASSED ✅ ✅ ✅")
        logger.info(f"Final video: {final_video}")
        logger.info(f"Size: {final_video.stat().st_size / 1024 / 1024:.2f} MB")

        return final_video

    except Exception as e:
        logger.error(f"❌ Full pipeline test failed: {str(e)}")
        raise


async def main():
    """Run all tests"""
    logger.info("=" * 60)
    logger.info("DZIR IA VIDEO - END-TO-END TESTING")
    logger.info("=" * 60)
    logger.info("")

    tests = [
        ("Text-to-Video", test_text_to_video),
        ("Text-to-Speech", test_text_to_speech),
        ("Video Composition", test_video_composition),
        ("Full Pipeline", test_full_pipeline)
    ]

    results = {}

    for test_name, test_func in tests:
        try:
            logger.info(f"Running: {test_name}...")
            result = await test_func()
            results[test_name] = {"status": "PASSED", "result": result}
        except Exception as e:
            results[test_name] = {"status": "FAILED", "error": str(e)}

    # Summary
    logger.info("")
    logger.info("=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)

    passed = sum(1 for r in results.values() if r["status"] == "PASSED")
    total = len(results)

    for test_name, result in results.items():
        status_emoji = "✅" if result["status"] == "PASSED" else "❌"
        logger.info(f"{status_emoji} {test_name}: {result['status']}")
        if result["status"] == "FAILED":
            logger.error(f"   Error: {result['error']}")

    logger.info("")
    logger.info(f"Results: {passed}/{total} tests passed")

    if passed == total:
        logger.info("🎉 ALL TESTS PASSED 🎉")
    else:
        logger.error(f"⚠️  {total - passed} tests failed")

    return passed == total


if __name__ == "__main__":
    import torch

    # Check CUDA
    logger.info(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        logger.info(f"CUDA device: {torch.cuda.get_device_name(0)}")
        logger.info(f"CUDA memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")

    # Run tests
    success = asyncio.run(main())

    sys.exit(0 if success else 1)
