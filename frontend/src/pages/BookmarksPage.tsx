import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { getBookmarks, deleteBookmark } from '../api/client';
import { HiOutlineBookmark, HiOutlineTrash } from 'react-icons/hi';

interface BookmarkItem {
  id: number;
  item_type: string;
  item_id: string;
  title: string;
  link: string;
  note: string | null;
  created_at: string;
}

export default function BookmarksPage() {
  const [bookmarks, setBookmarks] = useState<BookmarkItem[]>([]);
  const [loading, setLoading] = useState(true);

  const load = () => {
    getBookmarks()
      .then(setBookmarks)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const handleDelete = async (id: number) => {
    try {
      await deleteBookmark(id);
      setBookmarks((prev) => prev.filter((b) => b.id !== id));
      toast.success('Yer imi silindi.');
    } catch (err) {
      toast.error('Yer imi silinemedi. Tekrar deneyin.');
    }
  };

  if (loading) return <div className="text-gray-400">Yükleniyor...</div>;

  const grouped = {
    lesson: bookmarks.filter((b) => b.item_type === 'lesson'),
    challenge: bookmarks.filter((b) => b.item_type === 'challenge'),
    project: bookmarks.filter((b) => b.item_type === 'project'),
  };

  const typeLabels: Record<string, { label: string; icon: string }> = {
    lesson: { label: 'Dersler', icon: '📖' },
    challenge: { label: 'Challenges', icon: '💻' },
    project: { label: 'Projeler', icon: '🏗️' },
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <HiOutlineBookmark className="w-6 h-6 text-yellow-400" />
        <h1 className="text-2xl font-bold text-white">Yer İmleri</h1>
        <span className="text-sm text-gray-400">({bookmarks.length})</span>
      </div>

      {bookmarks.length === 0 && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-8 text-center">
          <HiOutlineBookmark className="w-12 h-12 text-gray-600 mx-auto mb-3" />
          <p className="text-gray-400">Henüz yer imi eklemedin.</p>
          <p className="text-sm text-gray-600 mt-1">Ders, challenge veya proje sayfalarindaki yer imi butonunu kullan.</p>
        </div>
      )}

      {Object.entries(grouped).map(([type, items]) => {
        if (items.length === 0) return null;
        const { label, icon } = typeLabels[type] || { label: type, icon: '📌' };
        return (
          <div key={type}>
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">
              {icon} {label} ({items.length})
            </h2>
            <div className="space-y-2">
              {items.map((b) => (
                <div
                  key={b.id}
                  className="bg-gray-900 border border-gray-800 rounded-lg p-4 flex items-center justify-between hover:border-gray-700 transition-colors"
                >
                  <Link to={b.link} className="flex-1 min-w-0">
                    <p className="text-white font-medium truncate hover:text-blue-400 transition-colors">
                      {b.title}
                    </p>
                    {b.note && <p className="text-xs text-gray-400 mt-0.5">{b.note}</p>}
                    <p className="text-xs text-gray-600 mt-1">
                      {new Date(b.created_at).toLocaleDateString('tr-TR')}
                    </p>
                  </Link>
                  <button
                    onClick={() => handleDelete(b.id)}
                    className="ml-3 p-1.5 text-gray-600 hover:text-red-400 transition-colors"
                    title="Yer imini kaldir"
                  >
                    <HiOutlineTrash className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}
