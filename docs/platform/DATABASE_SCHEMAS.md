# Schémas de Base de Données - IAFactory Platform Suite

**Version:** 2.0.0
**Dernière mise à jour:** Décembre 2024

---

## Vue d'ensemble

Ce document décrit les schémas de base de données pour tous les projets IAFactory.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DATABASES OVERVIEW                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │     ACADEMY     │  │     VIDEO       │  │      NEXUS      │              │
│  │   PostgreSQL    │  │   PostgreSQL    │  │   PostgreSQL    │              │
│  │    + Redis      │  │    + Redis      │  │ + Redis + Qdrant│              │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘              │
│                                                                              │
│  ┌─────────────────┐                                                        │
│  │  ONESTSCHOOLED  │                                                        │
│  │      MySQL      │                                                        │
│  └─────────────────┘                                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. IAFactory Academy

### Diagramme ER

```
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│      USERS       │       │     COURSES      │       │     MODULES      │
├──────────────────┤       ├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │       │ id (PK)          │
│ email            │       │ title            │       │ course_id (FK)   │
│ password_hash    │       │ description      │       │ title            │
│ name             │       │ instructor_id(FK)│       │ order            │
│ role             │       │ price            │       │ created_at       │
│ avatar_url       │       │ status           │       └────────┬─────────┘
│ created_at       │       │ thumbnail_url    │                │
│ updated_at       │       │ created_at       │                │
└────────┬─────────┘       └────────┬─────────┘                │
         │                          │                          │
         │                          │                          ▼
         │                          │            ┌──────────────────┐
         │                          │            │     LESSONS      │
         │                          │            ├──────────────────┤
         │                          │            │ id (PK)          │
         │                          │            │ module_id (FK)   │
         │                          │            │ title            │
         │                          │            │ content          │
         │                          │            │ video_url        │
         │                          │            │ duration         │
         │                          │            │ order            │
         │                          │            └──────────────────┘
         │                          │
         │    ┌─────────────────────┘
         │    │
         ▼    ▼
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│   ENROLLMENTS    │       │    PROGRESS      │       │   CERTIFICATES   │
├──────────────────┤       ├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │       │ id (PK)          │
│ user_id (FK)     │       │ enrollment_id(FK)│       │ enrollment_id(FK)│
│ course_id (FK)   │       │ lesson_id (FK)   │       │ certificate_url  │
│ status           │       │ completed        │       │ issued_at        │
│ enrolled_at      │       │ completed_at     │       │ uuid             │
│ completed_at     │       │ watch_time       │       └──────────────────┘
└──────────────────┘       └──────────────────┘

┌──────────────────┐       ┌──────────────────┐
│    PAYMENTS      │       │   RESOURCES      │
├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │
│ user_id (FK)     │       │ lesson_id (FK)   │
│ course_id (FK)   │       │ title            │
│ amount           │       │ type             │
│ currency         │       │ url              │
│ stripe_id        │       │ created_at       │
│ status           │       └──────────────────┘
│ created_at       │
└──────────────────┘
```

### Tables SQL

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'student',
    avatar_url VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    email_verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Courses
CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    instructor_id UUID REFERENCES users(id),
    price DECIMAL(10, 2) DEFAULT 0,
    currency VARCHAR(3) DEFAULT 'DZD',
    status VARCHAR(50) DEFAULT 'draft',
    thumbnail_url VARCHAR(500),
    level VARCHAR(50) DEFAULT 'beginner',
    language VARCHAR(10) DEFAULT 'fr',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_courses_instructor ON courses(instructor_id);
CREATE INDEX idx_courses_status ON courses(status);

-- Modules
CREATE TABLE modules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_modules_course ON modules(course_id);

-- Lessons
CREATE TABLE lessons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    module_id UUID REFERENCES modules(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    video_url VARCHAR(500),
    duration INTEGER DEFAULT 0,
    order_index INTEGER DEFAULT 0,
    is_preview BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_lessons_module ON lessons(module_id);

-- Enrollments
CREATE TABLE enrollments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    course_id UUID REFERENCES courses(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'active',
    enrolled_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    UNIQUE(user_id, course_id)
);

CREATE INDEX idx_enrollments_user ON enrollments(user_id);
CREATE INDEX idx_enrollments_course ON enrollments(course_id);

-- Progress
CREATE TABLE progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    enrollment_id UUID REFERENCES enrollments(id) ON DELETE CASCADE,
    lesson_id UUID REFERENCES lessons(id) ON DELETE CASCADE,
    completed BOOLEAN DEFAULT false,
    completed_at TIMESTAMP,
    watch_time INTEGER DEFAULT 0,
    UNIQUE(enrollment_id, lesson_id)
);

CREATE INDEX idx_progress_enrollment ON progress(enrollment_id);

-- Payments
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    course_id UUID REFERENCES courses(id),
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'DZD',
    provider VARCHAR(50) DEFAULT 'stripe',
    provider_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending',
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_payments_user ON payments(user_id);
CREATE INDEX idx_payments_status ON payments(status);

-- Certificates
CREATE TABLE certificates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    enrollment_id UUID REFERENCES enrollments(id) ON DELETE CASCADE,
    certificate_uuid VARCHAR(100) UNIQUE,
    certificate_url VARCHAR(500),
    issued_at TIMESTAMP DEFAULT NOW()
);
```

---

## 2. IAFactory Video Platform

### Diagramme ER

```
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│      USERS       │       │    PROJECTS      │       │     ASSETS       │
├──────────────────┤       ├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │       │ id (PK)          │
│ email            │◄──────│ user_id (FK)     │       │ project_id (FK)  │
│ password_hash    │       │ title            │       │ type             │
│ name             │       │ description      │       │ provider         │
│ api_key          │       │ prompt           │       │ prompt           │
│ created_at       │       │ status           │       │ file_path        │
└──────────────────┘       │ config (JSONB)   │       │ metadata (JSONB) │
                           │ created_at       │       │ created_at       │
                           └────────┬─────────┘       └──────────────────┘
                                    │
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         │                          │                          │
         ▼                          ▼                          ▼
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│     SCRIPTS      │       │    TIMELINES     │       │   PUBLICATIONS   │
├──────────────────┤       ├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │       │ id (PK)          │
│ project_id (FK)  │       │ project_id (FK)  │       │ project_id (FK)  │
│ content (JSONB)  │       │ duration_ms      │       │ platform         │
│ scenes (JSONB)   │       │ tracks (JSONB)   │       │ platform_id      │
│ version          │       │ render_status    │       │ status           │
│ created_at       │       │ output_path      │       │ published_at     │
└──────────────────┘       │ created_at       │       │ analytics (JSONB)│
                           └──────────────────┘       └──────────────────┘

┌──────────────────┐       ┌──────────────────┐
│   RENDER_JOBS    │       │ PLATFORM_TOKENS  │
├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │
│ timeline_id (FK) │       │ user_id (FK)     │
│ status           │       │ platform         │
│ progress         │       │ access_token     │
│ output_url       │       │ refresh_token    │
│ started_at       │       │ expires_at       │
│ completed_at     │       │ created_at       │
└──────────────────┘       └──────────────────┘
```

### Tables SQL

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    api_key VARCHAR(100) UNIQUE,
    plan VARCHAR(50) DEFAULT 'free',
    credits INTEGER DEFAULT 100,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Projects
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    prompt TEXT,
    status VARCHAR(50) DEFAULT 'draft',
    config JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_projects_user ON projects(user_id);
CREATE INDEX idx_projects_status ON projects(status);

-- Assets
CREATE TABLE assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    provider VARCHAR(100),
    prompt TEXT,
    file_path VARCHAR(500),
    file_size BIGINT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_assets_project ON assets(project_id);
CREATE INDEX idx_assets_type ON assets(type);

-- Scripts
CREATE TABLE scripts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    content JSONB NOT NULL,
    scenes JSONB DEFAULT '[]',
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Timelines
CREATE TABLE timelines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    duration_ms INTEGER,
    tracks JSONB DEFAULT '[]',
    render_status VARCHAR(50) DEFAULT 'draft',
    output_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Render Jobs
CREATE TABLE render_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timeline_id UUID REFERENCES timelines(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'queued',
    progress INTEGER DEFAULT 0,
    output_url VARCHAR(500),
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_render_jobs_status ON render_jobs(status);

-- Publications
CREATE TABLE publications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    platform_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending',
    config JSONB DEFAULT '{}',
    published_at TIMESTAMP,
    analytics JSONB DEFAULT '{}'
);

-- Platform Tokens (OAuth)
CREATE TABLE platform_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, platform)
);
```

---

## 3. RAG-DZ / Nexus

### Diagramme ER

```
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│      USERS       │       │    PROJECTS      │       │   COLLECTIONS    │
├──────────────────┤       ├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │       │ id (PK)          │
│ email            │◄──────│ user_id (FK)     │       │ user_id (FK)     │
│ password_hash    │       │ name             │       │ name             │
│ name             │       │ type             │       │ description      │
│ role             │       │ config (JSONB)   │       │ embedding_model  │
│ api_key          │       │ created_at       │       │ created_at       │
│ created_at       │       └──────────────────┘       └────────┬─────────┘
└────────┬─────────┘                                           │
         │                                                      │
         │                                                      ▼
         │                 ┌──────────────────┐       ┌──────────────────┐
         │                 │    DOCUMENTS     │       │     CHUNKS       │
         │                 ├──────────────────┤       ├──────────────────┤
         │                 │ id (PK)          │       │ id (PK)          │
         │                 │ collection_id(FK)│◄──────│ document_id (FK) │
         │                 │ filename         │       │ content          │
         │                 │ file_path        │       │ embedding        │
         │                 │ file_size        │       │ metadata (JSONB) │
         │                 │ mime_type        │       │ page_number      │
         │                 │ status           │       │ created_at       │
         │                 │ metadata (JSONB) │       └──────────────────┘
         │                 │ created_at       │
         │                 └──────────────────┘
         │
         │
         ▼
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│    API_KEYS      │       │     TASKS        │       │    SESSIONS      │
├──────────────────┤       ├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │       │ id (PK)          │
│ user_id (FK)     │       │ user_id (FK)     │       │ user_id (FK)     │
│ key_hash         │       │ project_id (FK)  │       │ agent_type       │
│ name             │       │ type             │       │ messages (JSONB) │
│ permissions      │       │ status           │       │ context (JSONB)  │
│ rate_limit       │       │ input (JSONB)    │       │ created_at       │
│ expires_at       │       │ output (JSONB)   │       │ updated_at       │
│ created_at       │       │ created_at       │       └──────────────────┘
│ last_used_at     │       │ completed_at     │
└──────────────────┘       └──────────────────┘

┌──────────────────┐       ┌──────────────────┐
│     PAYMENTS     │       │    USAGE_LOGS    │
├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │
│ user_id (FK)     │       │ user_id (FK)     │
│ amount           │       │ endpoint         │
│ currency         │       │ tokens_used      │
│ provider         │       │ model            │
│ provider_id      │       │ cost_usd         │
│ status           │       │ created_at       │
│ created_at       │       └──────────────────┘
└──────────────────┘
```

### Tables SQL

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    plan VARCHAR(50) DEFAULT 'free',
    api_key VARCHAR(100) UNIQUE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Projects
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(50) DEFAULT 'general',
    config JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Collections (for RAG)
CREATE TABLE collections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    embedding_model VARCHAR(100) DEFAULT 'text-embedding-3-small',
    vector_dimension INTEGER DEFAULT 1536,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, name)
);

-- Documents
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    collection_id UUID REFERENCES collections(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500),
    file_size BIGINT,
    mime_type VARCHAR(100),
    status VARCHAR(50) DEFAULT 'pending',
    pages INTEGER,
    chunks_count INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_documents_collection ON documents(collection_id);
CREATE INDEX idx_documents_status ON documents(status);

-- Chunks (stored in PostgreSQL, embeddings in Qdrant)
CREATE TABLE chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    page_number INTEGER,
    chunk_index INTEGER,
    token_count INTEGER,
    metadata JSONB DEFAULT '{}',
    qdrant_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_chunks_document ON chunks(document_id);

-- API Keys
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    key_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    permissions JSONB DEFAULT '["read", "write"]',
    rate_limit INTEGER DEFAULT 1000,
    expires_at TIMESTAMP,
    last_used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_api_keys_user ON api_keys(user_id);

-- Tasks
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    project_id UUID REFERENCES projects(id),
    type VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    priority INTEGER DEFAULT 0,
    input JSONB,
    output JSONB,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_user ON tasks(user_id);

-- Sessions (Agent conversations)
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    agent_type VARCHAR(100) NOT NULL,
    messages JSONB DEFAULT '[]',
    context JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_sessions_user ON sessions(user_id);

-- Payments (Chargily)
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'DZD',
    provider VARCHAR(50) DEFAULT 'chargily',
    provider_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Usage Logs
CREATE TABLE usage_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    api_key_id UUID REFERENCES api_keys(id),
    endpoint VARCHAR(255),
    method VARCHAR(10),
    tokens_used INTEGER DEFAULT 0,
    model VARCHAR(100),
    cost_usd DECIMAL(10, 6),
    response_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_usage_logs_user ON usage_logs(user_id);
CREATE INDEX idx_usage_logs_created ON usage_logs(created_at);
```

---

## 4. OneStSchooled (MySQL)

### Tables Principales

```sql
-- Users (multi-role)
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role_id BIGINT UNSIGNED,
    school_id BIGINT UNSIGNED,
    is_active BOOLEAN DEFAULT TRUE,
    email_verified_at TIMESTAMP NULL,
    remember_token VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Schools
CREATE TABLE schools (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    phone VARCHAR(50),
    email VARCHAR(255),
    logo_path VARCHAR(500),
    settings JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Students
CREATE TABLE students (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED,
    school_id BIGINT UNSIGNED,
    class_id BIGINT UNSIGNED,
    registration_number VARCHAR(100),
    date_of_birth DATE,
    gender ENUM('male', 'female'),
    address TEXT,
    parent_id BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (school_id) REFERENCES schools(id),
    FOREIGN KEY (class_id) REFERENCES classes(id)
);

-- Classes
CREATE TABLE classes (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    school_id BIGINT UNSIGNED,
    name VARCHAR(255) NOT NULL,
    level VARCHAR(50),
    section VARCHAR(50),
    capacity INT DEFAULT 30,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id)
);

-- Subjects
CREATE TABLE subjects (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    school_id BIGINT UNSIGNED,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50),
    credits INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id)
);

-- Teachers
CREATE TABLE teachers (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED,
    school_id BIGINT UNSIGNED,
    employee_id VARCHAR(100),
    qualification TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (school_id) REFERENCES schools(id)
);

-- Exams
CREATE TABLE exams (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    school_id BIGINT UNSIGNED,
    name VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE,
    term VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id)
);

-- Grades
CREATE TABLE grades (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT UNSIGNED,
    exam_id BIGINT UNSIGNED,
    subject_id BIGINT UNSIGNED,
    marks DECIMAL(5, 2),
    grade VARCHAR(10),
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (exam_id) REFERENCES exams(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
);

-- Attendance
CREATE TABLE attendance (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT UNSIGNED,
    class_id BIGINT UNSIGNED,
    date DATE NOT NULL,
    status ENUM('present', 'absent', 'late', 'excused'),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (class_id) REFERENCES classes(id)
);

-- Fees
CREATE TABLE fees (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT UNSIGNED,
    school_id BIGINT UNSIGNED,
    amount DECIMAL(10, 2) NOT NULL,
    type VARCHAR(100),
    due_date DATE,
    status ENUM('pending', 'paid', 'overdue'),
    paid_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (school_id) REFERENCES schools(id)
);

-- Payments
CREATE TABLE payments (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    fee_id BIGINT UNSIGNED,
    amount DECIMAL(10, 2) NOT NULL,
    method VARCHAR(50),
    reference VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fee_id) REFERENCES fees(id)
);
```

---

## Index Recommandés

### Performance Queries Fréquentes

```sql
-- Academy
CREATE INDEX idx_enrollments_lookup ON enrollments(user_id, course_id);
CREATE INDEX idx_progress_lookup ON progress(enrollment_id, completed);

-- Video
CREATE INDEX idx_projects_search ON projects(user_id, status, created_at);
CREATE INDEX idx_assets_search ON assets(project_id, type);

-- Nexus
CREATE INDEX idx_chunks_search ON chunks(document_id, qdrant_id);
CREATE INDEX idx_usage_report ON usage_logs(user_id, created_at, endpoint);

-- OneStSchooled
CREATE INDEX idx_attendance_date ON attendance(class_id, date);
CREATE INDEX idx_grades_exam ON grades(exam_id, student_id);
```

---

## Migrations

### Commandes par Projet

```bash
# Academy (Alembic)
cd iafactory-academy/backend
alembic upgrade head
alembic revision --autogenerate -m "Description"

# Video Platform (Alembic)
cd iafactory-video-platform/backend
alembic upgrade head

# RAG-DZ (Alembic)
cd rag-dz/services/api
alembic upgrade head

# OneStSchooled (Laravel)
cd onestschooled
php artisan migrate
php artisan migrate:fresh --seed
```

---

*Schémas de base de données IAFactory - Décembre 2024*
