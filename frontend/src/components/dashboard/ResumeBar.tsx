import { Link } from 'react-router-dom';
import { getLastPosition } from '../../hooks/useAutoResume';

export default function ResumeBar() {
  const lastPos = getLastPosition();

  if (!lastPos || lastPos.path === '/') return null;

  const timeAgo = getTimeAgo(lastPos.timestamp);

  return (
    <div className="bg-gradient-to-r from-emerald-600/20 to-teal-600/20 border border-emerald-500/30 rounded-xl p-4 flex items-center justify-between">
      <div className="flex items-center gap-3 min-w-0">
        <span className="text-xl shrink-0">📍</span>
        <div className="min-w-0">
          <p className="text-sm text-gray-300">Son kaldigin yer:</p>
          <p className="text-white font-medium truncate">{lastPos.title}</p>
          <p className="text-xs text-gray-400 mt-0.5">{timeAgo}</p>
        </div>
      </div>
      <Link
        to={lastPos.path}
        className="shrink-0 ml-4 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-sm font-medium transition-colors"
      >
        Devam Et
      </Link>
    </div>
  );
}

function getTimeAgo(timestamp: number): string {
  const diff = Date.now() - timestamp;
  const minutes = Math.floor(diff / 60000);
  if (minutes < 1) return 'az önce';
  if (minutes < 60) return `${minutes} dakika önce`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} saat önce`;
  const days = Math.floor(hours / 24);
  return `${days} gün önce`;
}
