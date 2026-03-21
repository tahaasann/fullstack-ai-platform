import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import TopBar from './TopBar';
import { Toaster } from 'react-hot-toast';
import useAutoResume from '../../hooks/useAutoResume';

export default function AppLayout() {
  useAutoResume();

  return (
    <>
      <Toaster position="top-right" toastOptions={{
        style: { background: '#1f2937', color: '#f3f4f6', border: '1px solid #374151' }
      }} />
      <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-50 focus:bg-gray-800 focus:text-white focus:px-4 focus:py-2 focus:rounded">
        İçeriğe atla
      </a>
      <div className="flex min-h-screen w-full">
        <Sidebar />
        <div className="flex-1 flex flex-col min-h-screen min-w-0">
          <TopBar />
          <main id="main-content" className="flex-1 p-6 overflow-y-auto">
            <Outlet />
          </main>
        </div>
      </div>
    </>
  );
}
