'use client';

import Link from 'next/link';
import { useState } from 'react';
import { useI18n } from '@/lib/i18n';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

const courses = [
  {
    id: 1,
    titleKey: 'category.ai',
    descriptionKey: 'app.description',
    level: 'beginner',
    duration: '20h',
    students: 1250,
    rating: 4.8,
    lessons: 24,
    category: 'ai',
    free: false,
  },
  {
    id: 2,
    titleKey: 'category.ml',
    descriptionKey: 'app.description',
    level: 'intermediate',
    duration: '35h',
    students: 890,
    rating: 4.9,
    lessons: 42,
    category: 'ml',
    free: false,
  },
  {
    id: 3,
    titleKey: 'category.python',
    descriptionKey: 'app.description',
    level: 'beginner',
    duration: '15h',
    students: 2100,
    rating: 4.7,
    lessons: 18,
    category: 'python',
    free: true,
  },
  {
    id: 4,
    titleKey: 'category.dl',
    descriptionKey: 'app.description',
    level: 'advanced',
    duration: '45h',
    students: 560,
    rating: 4.9,
    lessons: 56,
    category: 'dl',
    free: false,
  },
  {
    id: 5,
    titleKey: 'category.nlp',
    descriptionKey: 'app.description',
    level: 'intermediate',
    duration: '30h',
    students: 720,
    rating: 4.8,
    lessons: 36,
    category: 'nlp',
    free: false,
  },
  {
    id: 6,
    titleKey: 'category.cv',
    descriptionKey: 'app.description',
    level: 'intermediate',
    duration: '28h',
    students: 640,
    rating: 4.7,
    lessons: 32,
    category: 'cv',
    free: true,
  },
];

const categories = ['all', 'ai', 'ml', 'dl', 'nlp', 'cv', 'python'];
const levels = ['all', 'beginner', 'intermediate', 'advanced'];

export default function CoursesPage() {
  const { t } = useI18n();
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedLevel, setSelectedLevel] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  const filteredCourses = courses.filter((course) => {
    const matchesCategory = selectedCategory === 'all' || course.category === selectedCategory;
    const matchesLevel = selectedLevel === 'all' || course.level === selectedLevel;
    const matchesSearch = t(course.titleKey).toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesLevel && matchesSearch;
  });

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Header />

      <main className="flex-1 py-8 px-4">
        <div className="container mx-auto">
          {/* Page Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-foreground mb-2">
              {t('courses.title')}
            </h1>
            <p className="text-muted-foreground">{t('app.description')}</p>
          </div>

          {/* Filters */}
          <div className="flex flex-col md:flex-row gap-4 mb-8">
            {/* Search */}
            <input
              type="text"
              placeholder={t('courses.search')}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1 px-4 py-2 rounded-lg border border-border bg-card text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            />

            {/* Category Filter */}
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-4 py-2 rounded-lg border border-border bg-card text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            >
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat === 'all' ? t('courses.all') : t(`category.${cat}`)}
                </option>
              ))}
            </select>

            {/* Level Filter */}
            <select
              value={selectedLevel}
              onChange={(e) => setSelectedLevel(e.target.value)}
              className="px-4 py-2 rounded-lg border border-border bg-card text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            >
              {levels.map((level) => (
                <option key={level} value={level}>
                  {level === 'all' ? t('course.level') : t(`course.level.${level}`)}
                </option>
              ))}
            </select>
          </div>

          {/* Course Grid */}
          {filteredCourses.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredCourses.map((course) => (
                <Link
                  key={course.id}
                  href={`/courses/${course.id}`}
                  className="group rounded-xl border border-border bg-card overflow-hidden hover:border-primary transition-colors"
                >
                  <div className="aspect-video bg-muted flex items-center justify-center relative">
                    <span className="text-5xl">📚</span>
                    {course.free && (
                      <span className="absolute top-2 right-2 px-2 py-1 rounded bg-success text-white text-xs font-medium">
                        {t('courses.free')}
                      </span>
                    )}
                  </div>
                  <div className="p-4">
                    <h3 className="text-lg font-semibold text-foreground group-hover:text-primary transition-colors">
                      {t(course.titleKey)}
                    </h3>
                    <p className="text-sm text-muted-foreground mt-1 line-clamp-2">
                      {t(course.descriptionKey)}
                    </p>
                    <div className="flex items-center gap-4 mt-3 text-sm text-muted-foreground">
                      <span className="px-2 py-0.5 rounded bg-muted">
                        {t(`course.level.${course.level}`)}
                      </span>
                      <span>{course.duration}</span>
                      <span>⭐ {course.rating}</span>
                    </div>
                    <div className="flex items-center justify-between mt-3 pt-3 border-t border-border text-sm text-muted-foreground">
                      <span>{course.lessons} {t('course.lessons')}</span>
                      <span>{course.students.toLocaleString()} {t('course.students')}</span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-muted-foreground">{t('courses.no_results')}</p>
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}
