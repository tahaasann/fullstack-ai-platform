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
      <div className="flex min-h-screen w-full">
        <Sidebar />
        <div className="flex-1 flex flex-col min-h-screen min-w-0">
          <TopBar />
          <main className="flex-1 p-6 overflow-y-auto">
            <Outlet />
          </main>
        </div>
      </div>
    </>
  );
}
