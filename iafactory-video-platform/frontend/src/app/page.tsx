'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import {
  Video,
  Wand2,
  FileText,
  Image,
  Music,
  Share2,
  Download,
  Loader2,
  AlertCircle
} from 'lucide-react'
import { api } from '@/lib/api'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import { useLanguage } from './providers'
import { t, Language } from '@/lib/i18n'

type GenerationStatus = 'idle' | 'creating' | 'generating' | 'completed' | 'error'

export default function Home() {
  const { language } = useLanguage()
  const [prompt, setPrompt] = useState('')
  const [duration, setDuration] = useState('60s')
  const [aspectRatio, setAspectRatio] = useState('16:9')
  const [style, setStyle] = useState('professional')
  const [status, setStatus] = useState<GenerationStatus>('idle')
  const [progress, setProgress] = useState(0)
  const [videoUrl, setVideoUrl] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [projectId, setProjectId] = useState<string | null>(null)
  const [currentPhase, setCurrentPhase] = useState<string>('')

  const isGenerating = status === 'creating' || status === 'generating'

  const getPhaseLabel = (phase: string, lang: Language): string => {
    const phaseMap: Record<string, string> = {
      'analysis': 'analyzing_prompt',
      'script': 'generating_script',
      'script_generation': 'generating_script',
      'image_generation': 'creating_images',
      'images': 'creating_images',
      'video': 'generating_video',
      'video_generation': 'generating_video',
      'audio': 'creating_voiceover',
      'audio_generation': 'creating_voiceover',
      'montage': 'final_editing',
      'rendering': 'final_render',
      'publish': 'preparing_publish'
    }
    const key = phaseMap[phase] || 'generating'
    return t(key, lang)
  }

  const handleGenerate = async () => {
    if (!prompt.trim()) return

    setStatus('creating')
    setProgress(0)
    setError(null)
    setVideoUrl(null)

    try {
      setProgress(10)
      console.log('[Video] Creating project with prompt:', prompt.slice(0, 50))

      const project = await api.projects.create({
        title: prompt.slice(0, 50),
        user_prompt: prompt,
        target_duration: duration,
        aspect_ratio: aspectRatio,
        style: style,
        language: language === 'darija' || language === 'amazigh' ? 'ar' : language,
        target_platforms: ['youtube']
      })

      console.log('[Video] Project created:', project)

      if (!project || !project.id) {
        throw new Error('Impossible de créer le projet. Vérifiez la connexion API.')
      }

      setProjectId(project.id)
      setProgress(20)
      setStatus('generating')

      await api.projects.startPipeline(project.id, { auto_publish: false })
      setProgress(30)

      let attempts = 0
      const maxAttempts = 360

      while (attempts < maxAttempts) {
        await new Promise(resolve => setTimeout(resolve, 5000))

        try {
          const statusResult = await api.projects.getStatus(project.id)
          const overallProgress = statusResult.progress?.overall || 0
          setProgress(30 + Math.floor(overallProgress * 0.7))
          setCurrentPhase(statusResult.current_phase || '')

          console.log('[Video] Status:', statusResult.status, 'Progress:', overallProgress, '%', 'Phase:', statusResult.current_phase)

          if (statusResult.status === 'completed') {
            const finalProject = await api.projects.get(project.id)
            if (finalProject.video_url) {
              setVideoUrl(finalProject.video_url)
            }
            setStatus('completed')
            setProgress(100)
            break
          } else if (statusResult.status === 'failed' || statusResult.status === 'error') {
            throw new Error('La génération a échoué. Veuillez réessayer.')
          }
        } catch (pollError) {
          console.error('Polling error:', pollError)
        }

        attempts++
      }

      if (attempts >= maxAttempts) {
        throw new Error('Timeout: La génération prend trop de temps (30 min max).')
      }

    } catch (err) {
      console.error('Generation error:', err)
      setError(err instanceof Error ? err.message : 'Erreur lors de la génération')
      setStatus('error')
    }
  }

  return (
    <>
      <Header />

      <main className="iaf-main bg-[var(--iaf-bg)]">
        {/* Hero Section */}
        <section className="max-w-4xl mx-auto px-4 py-20 text-center">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-5xl font-bold text-[var(--iaf-text-primary)] mb-6"
          >
            {t('hero_title', language)}
            <br />
            <span className="bg-gradient-to-r from-[#00a651] to-[#00c761] bg-clip-text text-transparent">
              {t('hero_title_highlight', language)}
            </span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-xl text-[var(--iaf-text-secondary)] mb-12"
          >
            {t('hero_subtitle', language)}
          </motion.p>

          {/* Main Input */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-[var(--iaf-surface)] backdrop-blur-sm rounded-2xl p-6 border border-[var(--iaf-border)]"
          >
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder={t('prompt_placeholder', language)}
              className="w-full h-32 bg-[var(--iaf-bg)] rounded-xl p-4 text-[var(--iaf-text-primary)] placeholder:text-[var(--iaf-text-muted)] resize-none border border-[var(--iaf-border)] focus:border-[#00a651] focus:outline-none transition"
              dir={language === 'ar' || language === 'darija' ? 'rtl' : 'ltr'}
            />

            {/* Options */}
            <div className="flex items-center justify-between mt-4 flex-wrap gap-4">
              <div className="flex items-center gap-4 flex-wrap">
                <select
                  value={duration}
                  onChange={(e) => setDuration(e.target.value)}
                  className="bg-[var(--iaf-bg)] text-[var(--iaf-text-secondary)] rounded-lg px-3 py-2 border border-[var(--iaf-border)] focus:outline-none focus:border-[#00a651]"
                >
                  <option value="60s">{t('duration_60s', language)}</option>
                  <option value="30s">{t('duration_30s', language)}</option>
                  <option value="15s">{t('duration_15s', language)}</option>
                  <option value="3min">{t('duration_3min', language)}</option>
                  <option value="10min">{t('duration_10min', language)}</option>
                </select>
                <select
                  value={aspectRatio}
                  onChange={(e) => setAspectRatio(e.target.value)}
                  className="bg-[var(--iaf-bg)] text-[var(--iaf-text-secondary)] rounded-lg px-3 py-2 border border-[var(--iaf-border)] focus:outline-none focus:border-[#00a651]"
                >
                  <option value="16:9">{t('ratio_16_9', language)}</option>
                  <option value="9:16">{t('ratio_9_16', language)}</option>
                  <option value="1:1">{t('ratio_1_1', language)}</option>
                </select>
                <select
                  value={style}
                  onChange={(e) => setStyle(e.target.value)}
                  className="bg-[var(--iaf-bg)] text-[var(--iaf-text-secondary)] rounded-lg px-3 py-2 border border-[var(--iaf-border)] focus:outline-none focus:border-[#00a651]"
                >
                  <option value="professional">{t('style_professional', language)}</option>
                  <option value="casual">{t('style_casual', language)}</option>
                  <option value="cinematic">{t('style_cinematic', language)}</option>
                  <option value="fun">{t('style_fun', language)}</option>
                </select>
              </div>
              <button
                onClick={handleGenerate}
                disabled={!prompt.trim() || isGenerating}
                className="bg-gradient-to-r from-[#00a651] to-[#00c761] hover:from-[#00c761] hover:to-[#00a651] text-white px-6 py-3 rounded-xl font-medium flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed transition shadow-lg hover:shadow-xl"
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    {status === 'creating' ? t('creating', language) : t('generating', language)}
                  </>
                ) : (
                  <>
                    <Wand2 className="w-5 h-5" />
                    {t('generate_video', language)}
                  </>
                )}
              </button>
            </div>

            {/* Progress Bar */}
            {isGenerating && (
              <div className="mt-6">
                <div className="flex justify-between text-sm text-[var(--iaf-text-secondary)] mb-2">
                  <span>
                    {status === 'creating'
                      ? t('creating_project', language)
                      : getPhaseLabel(currentPhase, language)}
                  </span>
                  <span>{progress}%</span>
                </div>
                <div className="w-full h-2 bg-[var(--iaf-border)] rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-gradient-to-r from-[#00a651] to-[#00c761]"
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    transition={{ duration: 0.5 }}
                  />
                </div>
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="mt-4 p-4 bg-red-500/20 border border-red-500/50 rounded-lg flex items-center gap-3">
                <AlertCircle className="w-5 h-5 text-red-400" />
                <span className="text-red-300">{error}</span>
              </div>
            )}

            {/* Video Result */}
            {status === 'completed' && videoUrl && (
              <div className="mt-6 p-4 bg-[#00a651]/20 border border-[#00a651]/50 rounded-lg">
                <h3 className="text-lg font-semibold text-[#00c761] mb-4">{t('video_success', language)}</h3>
                <video
                  src={videoUrl}
                  controls
                  className="w-full rounded-lg mb-4"
                />
                <a
                  href={videoUrl}
                  download
                  className="inline-flex items-center gap-2 bg-[#00a651] hover:bg-[#00c761] text-white px-4 py-2 rounded-lg transition"
                >
                  <Download className="w-4 h-4" />
                  {t('download_video', language)}
                </a>
              </div>
            )}
          </motion.div>
        </section>

        {/* Features */}
        <section className="max-w-6xl mx-auto px-4 py-16">
          <h2 className="text-2xl font-bold text-[var(--iaf-text-primary)] text-center mb-12">
            {t('pipeline_title', language)}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { icon: FileText, titleKey: 'feature_script', descKey: 'feature_script_desc', color: '#00a651' },
              { icon: Image, titleKey: 'feature_visuals', descKey: 'feature_visuals_desc', color: '#10b981' },
              { icon: Music, titleKey: 'feature_audio', descKey: 'feature_audio_desc', color: '#8b5cf6' },
              { icon: Share2, titleKey: 'feature_multiplatform', descKey: 'feature_multiplatform_desc', color: '#f59e0b' },
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + i * 0.1 }}
                className="bg-[var(--iaf-surface)] backdrop-blur-sm rounded-xl p-6 border border-[var(--iaf-border)] hover:border-[#00a651] transition"
              >
                <div
                  className="w-12 h-12 rounded-lg flex items-center justify-center mb-4"
                  style={{ backgroundColor: `${feature.color}20` }}
                >
                  <feature.icon className="w-6 h-6" style={{ color: feature.color }} />
                </div>
                <h3 className="text-lg font-semibold text-[var(--iaf-text-primary)] mb-2">
                  {t(feature.titleKey, language)}
                </h3>
                <p className="text-[var(--iaf-text-secondary)] text-sm">
                  {t(feature.descKey, language)}
                </p>
              </motion.div>
            ))}
          </div>
        </section>

        {/* AI Providers */}
        <section className="max-w-6xl mx-auto px-4 py-16">
          <h2 className="text-2xl font-bold text-[var(--iaf-text-primary)] text-center mb-4">
            {t('providers_title', language)}
          </h2>
          <p className="text-[var(--iaf-text-secondary)] text-center mb-12">
            {t('providers_subtitle', language)}
          </p>
          <div className="flex flex-wrap justify-center gap-8 opacity-60">
            {['OpenAI', 'Anthropic', 'ElevenLabs', 'Runway', 'HeyGen', 'Suno', 'Replicate', 'Groq'].map((provider) => (
              <div key={provider} className="text-[var(--iaf-text-secondary)] font-medium">
                {provider}
              </div>
            ))}
          </div>
        </section>
      </main>

      <Footer />
    </>
  )
}
