import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { ErrorBoundary } from './components/common/ErrorBoundary';
import AppLayout from './components/layout/AppLayout';

const DashboardPage = lazy(() => import('./pages/DashboardPage'));
const ModuleListPage = lazy(() => import('./pages/ModuleListPage'));
const ModulePage = lazy(() => import('./pages/ModulePage'));
const LessonPage = lazy(() => import('./pages/LessonPage'));
const QuizPage = lazy(() => import('./pages/QuizPage'));
const ChallengePage = lazy(() => import('./pages/ChallengePage'));
const ChallengeListPage = lazy(() => import('./pages/ChallengeListPage'));
const ProjectListPage = lazy(() => import('./pages/ProjectListPage'));
const ProjectPage = lazy(() => import('./pages/ProjectPage'));
const ProgressPage = lazy(() => import('./pages/ProgressPage'));
const EnglishProgressPage = lazy(() => import('./pages/EnglishProgressPage'));
const ResourcesPage = lazy(() => import('./pages/ResourcesPage'));
const RoadmapPage = lazy(() => import('./pages/RoadmapPage'));
const CVGuidancePage = lazy(() => import('./pages/CVGuidancePage'));
const BookmarksPage = lazy(() => import('./pages/BookmarksPage'));
const LinkedInGuidePage = lazy(() => import('./pages/LinkedInGuidePage'));
const JobTrackerPage = lazy(() => import('./pages/JobTrackerPage'));
const AIToolsGuidePage = lazy(() => import('./pages/AIToolsGuidePage'));
const CVTemplatePage = lazy(() => import('./pages/CVTemplatePage'));
const JobSearchStrategyPage = lazy(() => import('./pages/JobSearchStrategyPage'));
const EmploymentGapGuidePage = lazy(() => import('./pages/EmploymentGapGuidePage'));

function NotFoundPage() {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center bg-gray-900 text-gray-300">
      <h1 className="text-6xl font-bold text-emerald-500 mb-4">404</h1>
      <p className="text-xl mb-6">Sayfa bulunamadi</p>
      <Link to="/" className="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors">
        Ana Sayfaya Don
      </Link>
    </div>
  );
}

export default function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <Suspense fallback={<div className="min-h-screen bg-gray-900 flex items-center justify-center"><div className="text-gray-400">Yukleniyor...</div></div>}>
          <Routes>
            <Route element={<AppLayout />}>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/modules" element={<ModuleListPage />} />
              <Route path="/module/:moduleId" element={<ModulePage />} />
              <Route path="/lesson/:lessonId" element={<LessonPage />} />
              <Route path="/quiz/:quizId" element={<QuizPage />} />
              <Route path="/challenges" element={<ChallengeListPage />} />
              <Route path="/challenge/:challengeId" element={<ChallengePage />} />
              <Route path="/projects" element={<ProjectListPage />} />
              <Route path="/project/:projectId" element={<ProjectPage />} />
              <Route path="/progress" element={<ProgressPage />} />
              <Route path="/english" element={<EnglishProgressPage />} />
              <Route path="/bookmarks" element={<BookmarksPage />} />
              <Route path="/cv-guide" element={<CVGuidancePage />} />
              <Route path="/linkedin-guide" element={<LinkedInGuidePage />} />
              <Route path="/job-tracker" element={<JobTrackerPage />} />
              <Route path="/cv-templates" element={<CVTemplatePage />} />
              <Route path="/job-search-strategy" element={<JobSearchStrategyPage />} />
              <Route path="/employment-gap-guide" element={<EmploymentGapGuidePage />} />
              <Route path="/ai-tools" element={<AIToolsGuidePage />} />
              <Route path="/resources" element={<ResourcesPage />} />
              <Route path="/roadmap" element={<RoadmapPage />} />
              <Route path="*" element={<NotFoundPage />} />
            </Route>
          </Routes>
        </Suspense>
        <Toaster position="bottom-right" toastOptions={{
          style: { background: '#1f2937', color: '#d1d5db', border: '1px solid #374151' },
          error: { duration: 5000 },
          success: { duration: 3000 },
        }} />
      </BrowserRouter>
    </ErrorBoundary>
  );
}
