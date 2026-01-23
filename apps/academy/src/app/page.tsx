'use client';

import Link from 'next/link';
import { useI18n } from '@/lib/i18n';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

const featuredCourses = [
  {
    id: 1,
    titleKey: 'category.ai',
    level: 'beginner',
    duration: '20h',
    students: 1250,
    rating: 4.8,
    image: '/courses/ai-basics.jpg',
  },
  {
    id: 2,
    titleKey: 'category.ml',
    level: 'intermediate',
    duration: '35h',
    students: 890,
    rating: 4.9,
    image: '/courses/ml-fundamentals.jpg',
  },
  {
    id: 3,
    titleKey: 'category.python',
    level: 'beginner',
    duration: '15h',
    students: 2100,
    rating: 4.7,
    image: '/courses/python-ai.jpg',
  },
];

export default function HomePage() {
  const { t } = useI18n();

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Header />

      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative py-20 px-4 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-transparent to-secondary/10" />
          <div className="container mx-auto relative z-10">
            <div className="max-w-3xl mx-auto text-center">
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-foreground mb-6">
                {t('home.hero.title')}
              </h1>
              <p className="text-xl text-muted-foreground mb-8">
                {t('home.hero.subtitle')}
              </p>
              <Link
                href="/courses"
                className="inline-flex px-8 py-4 rounded-lg bg-primary text-primary-foreground font-semibold text-lg hover:opacity-90 transition-opacity"
              >
                {t('home.hero.cta')}
              </Link>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-16 px-4 bg-card">
          <div className="container mx-auto">
            <h2 className="text-3xl font-bold text-center text-foreground mb-12">
              {t('home.features.title')}
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {[
                { key: 'experts', icon: '🎓' },
                { key: 'practical', icon: '💻' },
                { key: 'certificate', icon: '📜' },
                { key: 'community', icon: '🤝' },
              ].map((feature) => (
                <div
                  key={feature.key}
                  className="p-6 rounded-xl bg-background border border-border text-center hover:border-primary transition-colors"
                >
                  <div className="text-4xl mb-4">{feature.icon}</div>
                  <h3 className="text-lg font-semibold text-foreground">
                    {t(`home.feature.${feature.key}`)}
                  </h3>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Featured Courses */}
        <section className="py-16 px-4">
          <div className="container mx-auto">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-3xl font-bold text-foreground">
                {t('courses.popular')}
              </h2>
              <Link
                href="/courses"
                className="text-primary hover:underline font-medium"
              >
                {t('action.view_all')} →
              </Link>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {featuredCourses.map((course) => (
                <Link
                  key={course.id}
                  href={`/courses/${course.id}`}
                  className="group rounded-xl border border-border bg-card overflow-hidden hover:border-primary transition-colors"
                >
                  <div className="aspect-video bg-muted flex items-center justify-center">
                    <span className="text-4xl">📚</span>
                  </div>
                  <div className="p-4">
                    <h3 className="text-lg font-semibold text-foreground group-hover:text-primary transition-colors">
                      {t(course.titleKey)}
                    </h3>
                    <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
                      <span>{t(`course.level.${course.level}`)}</span>
                      <span>•</span>
                      <span>{course.duration}</span>
                      <span>•</span>
                      <span>⭐ {course.rating}</span>
                    </div>
                    <div className="mt-3 text-sm text-muted-foreground">
                      {course.students.toLocaleString()} {t('course.students')}
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16 px-4 bg-primary">
          <div className="container mx-auto text-center">
            <h2 className="text-3xl font-bold text-primary-foreground mb-4">
              {t('home.hero.title')}
            </h2>
            <p className="text-primary-foreground/80 mb-8 max-w-2xl mx-auto">
              {t('app.description')}
            </p>
            <Link
              href="/register"
              className="inline-flex px-8 py-4 rounded-lg bg-background text-foreground font-semibold hover:opacity-90 transition-opacity"
            >
              {t('auth.register')}
            </Link>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
