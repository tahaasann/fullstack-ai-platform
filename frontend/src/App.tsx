import { lazy, Suspense, ReactNode } from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { ErrorBoundary } from './components/common/ErrorBoundary';
import { PageSkeleton } from './components/common/Skeleton';
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

function SafePage({ children }: { children: ReactNode }) {
  return (
    <ErrorBoundary>
      <Suspense fallback={<PageSkeleton />}>
        {children}
      </Suspense>
    </ErrorBoundary>
  );
}

function NotFoundPage() {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center text-gray-300">
      <h1 className="text-7xl font-bold text-emerald-500 mb-3">404</h1>
      <p className="text-xl mb-2">Aradığınız sayfa bulunamadı</p>
      <p className="text-sm text-gray-500 mb-8">
        Bu sayfa taşınmış, silinmiş veya hiç var olmamış olabilir.
      </p>
      <Link
        to="/"
        className="px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium"
      >
        Ana Sayfaya Don
      </Link>
    </div>
  );
}

export default function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <Suspense fallback={<div className="min-h-screen bg-gray-900 flex items-center justify-center"><PageSkeleton /></div>}>
          <Routes>
            <Route element={<AppLayout />}>
              <Route path="/" element={<SafePage><DashboardPage /></SafePage>} />
              <Route path="/modules" element={<SafePage><ModuleListPage /></SafePage>} />
              <Route path="/module/:moduleId" element={<SafePage><ModulePage /></SafePage>} />
              <Route path="/lesson/:lessonId" element={<SafePage><LessonPage /></SafePage>} />
              <Route path="/quiz/:quizId" element={<SafePage><QuizPage /></SafePage>} />
              <Route path="/challenges" element={<SafePage><ChallengeListPage /></SafePage>} />
              <Route path="/challenge/:challengeId" element={<SafePage><ChallengePage /></SafePage>} />
              <Route path="/projects" element={<SafePage><ProjectListPage /></SafePage>} />
              <Route path="/project/:projectId" element={<SafePage><ProjectPage /></SafePage>} />
              <Route path="/progress" element={<SafePage><ProgressPage /></SafePage>} />
              <Route path="/english" element={<SafePage><EnglishProgressPage /></SafePage>} />
              <Route path="/bookmarks" element={<SafePage><BookmarksPage /></SafePage>} />
              <Route path="/cv-guide" element={<SafePage><CVGuidancePage /></SafePage>} />
              <Route path="/linkedin-guide" element={<SafePage><LinkedInGuidePage /></SafePage>} />
              <Route path="/job-tracker" element={<SafePage><JobTrackerPage /></SafePage>} />
              <Route path="/cv-templates" element={<SafePage><CVTemplatePage /></SafePage>} />
              <Route path="/job-search-strategy" element={<SafePage><JobSearchStrategyPage /></SafePage>} />
              <Route path="/employment-gap-guide" element={<SafePage><EmploymentGapGuidePage /></SafePage>} />
              <Route path="/ai-tools" element={<SafePage><AIToolsGuidePage /></SafePage>} />
              <Route path="/resources" element={<SafePage><ResourcesPage /></SafePage>} />
              <Route path="/roadmap" element={<SafePage><RoadmapPage /></SafePage>} />
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
