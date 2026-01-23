'use client';

import Link from 'next/link';
import { useParams } from 'next/navigation';
import { useI18n } from '@/lib/i18n';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

const courseData: Record<string, {
  titleKey: string;
  descriptionKey: string;
  level: string;
  duration: string;
  students: number;
  rating: number;
  lessons: number;
  instructor: string;
  curriculum: { title: string; duration: string }[];
}> = {
  '1': {
    titleKey: 'category.ai',
    descriptionKey: 'app.description',
    level: 'beginner',
    duration: '20h',
    students: 1250,
    rating: 4.8,
    lessons: 24,
    instructor: 'Dr. Ahmed Benali',
    curriculum: [
      { title: 'Introduction to AI', duration: '45min' },
      { title: 'History of AI', duration: '30min' },
      { title: 'Types of AI', duration: '1h' },
      { title: 'AI Applications', duration: '1h 30min' },
      { title: 'Ethics in AI', duration: '45min' },
    ],
  },
  '2': {
    titleKey: 'category.ml',
    descriptionKey: 'app.description',
    level: 'intermediate',
    duration: '35h',
    students: 890,
    rating: 4.9,
    lessons: 42,
    instructor: 'Dr. Fatima Zerhouni',
    curriculum: [
      { title: 'ML Fundamentals', duration: '1h' },
      { title: 'Supervised Learning', duration: '2h' },
      { title: 'Unsupervised Learning', duration: '2h' },
      { title: 'Model Evaluation', duration: '1h 30min' },
      { title: 'Feature Engineering', duration: '1h 30min' },
    ],
  },
};

export default function CourseDetailPage() {
  const { t } = useI18n();
  const params = useParams();
  const courseId = params.id as string;
  const course = courseData[courseId] || courseData['1'];

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Header />

      <main className="flex-1 py-8 px-4">
        <div className="container mx-auto">
          {/* Breadcrumb */}
          <div className="flex items-center gap-2 text-sm text-muted-foreground mb-6">
            <Link href="/" className="hover:text-foreground transition-colors">
              {t('nav.home')}
            </Link>
            <span>/</span>
            <Link href="/courses" className="hover:text-foreground transition-colors">
              {t('nav.courses')}
            </Link>
            <span>/</span>
            <span className="text-foreground">{t(course.titleKey)}</span>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2">
              {/* Course Header */}
              <div className="aspect-video bg-muted rounded-xl flex items-center justify-center mb-6">
                <span className="text-6xl">📚</span>
              </div>

              <h1 className="text-3xl font-bold text-foreground mb-4">
                {t(course.titleKey)}
              </h1>

              <div className="flex flex-wrap items-center gap-4 mb-6 text-sm">
                <span className="px-3 py-1 rounded-full bg-primary/10 text-primary">
                  {t(`course.level.${course.level}`)}
                </span>
                <span className="text-muted-foreground">
                  {course.duration}
                </span>
                <span className="text-muted-foreground">
                  ⭐ {course.rating}
                </span>
                <span className="text-muted-foreground">
                  {course.students.toLocaleString()} {t('course.students')}
                </span>
              </div>

              {/* Tabs */}
              <div className="border-b border-border mb-6">
                <div className="flex gap-6">
                  <button className="pb-3 border-b-2 border-primary text-primary font-medium">
                    {t('course.description')}
                  </button>
                  <button className="pb-3 border-b-2 border-transparent text-muted-foreground hover:text-foreground transition-colors">
                    {t('course.curriculum')}
                  </button>
                  <button className="pb-3 border-b-2 border-transparent text-muted-foreground hover:text-foreground transition-colors">
                    {t('course.reviews')}
                  </button>
                </div>
              </div>

              {/* Description */}
              <div className="prose prose-neutral dark:prose-invert max-w-none">
                <p className="text-foreground">{t(course.descriptionKey)}</p>
                <p className="text-muted-foreground mt-4">
                  {t('app.tagline')}
                </p>
              </div>

              {/* Curriculum Preview */}
              <div className="mt-8">
                <h2 className="text-xl font-semibold text-foreground mb-4">
                  {t('course.curriculum')}
                </h2>
                <div className="space-y-3">
                  {course.curriculum.map((lesson, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between p-4 rounded-lg border border-border bg-card"
                    >
                      <div className="flex items-center gap-3">
                        <span className="w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center text-sm font-medium">
                          {index + 1}
                        </span>
                        <span className="text-foreground">{lesson.title}</span>
                      </div>
                      <span className="text-sm text-muted-foreground">
                        {lesson.duration}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Sidebar */}
            <div className="lg:col-span-1">
              <div className="sticky top-24 rounded-xl border border-border bg-card p-6">
                <div className="text-3xl font-bold text-foreground mb-4">
                  {t('courses.free')}
                </div>

                <button className="w-full py-3 rounded-lg bg-primary text-primary-foreground font-semibold hover:opacity-90 transition-opacity mb-4">
                  {t('course.enroll')}
                </button>

                <div className="space-y-4 text-sm">
                  <div className="flex items-center justify-between py-2 border-b border-border">
                    <span className="text-muted-foreground">{t('course.duration')}</span>
                    <span className="text-foreground font-medium">{course.duration}</span>
                  </div>
                  <div className="flex items-center justify-between py-2 border-b border-border">
                    <span className="text-muted-foreground">{t('course.lessons')}</span>
                    <span className="text-foreground font-medium">{course.lessons}</span>
                  </div>
                  <div className="flex items-center justify-between py-2 border-b border-border">
                    <span className="text-muted-foreground">{t('course.level')}</span>
                    <span className="text-foreground font-medium">{t(`course.level.${course.level}`)}</span>
                  </div>
                  <div className="flex items-center justify-between py-2 border-b border-border">
                    <span className="text-muted-foreground">{t('course.instructor')}</span>
                    <span className="text-foreground font-medium">{course.instructor}</span>
                  </div>
                  <div className="flex items-center justify-between py-2">
                    <span className="text-muted-foreground">{t('course.rating')}</span>
                    <span className="text-foreground font-medium">⭐ {course.rating}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
