import { useEffect, useState } from 'react';
import { checkBookmark, createBookmark, deleteBookmark } from '../../api/client';
import { HiOutlineBookmark, HiBookmark } from 'react-icons/hi';

interface Props {
  itemType: 'lesson' | 'challenge' | 'project';
  itemId: string;
}

export default function BookmarkButton({ itemType, itemId }: Props) {
  const [bookmarked, setBookmarked] = useState(false);
  const [bookmarkId, setBookmarkId] = useState<number | null>(null);

  useEffect(() => {
    checkBookmark(itemType, itemId)
      .then((data) => {
        setBookmarked(data.bookmarked);
        setBookmarkId(data.id);
      })
      .catch(() => {});
  }, [itemType, itemId]);

  const toggle = async () => {
    try {
      if (bookmarked && bookmarkId) {
        await deleteBookmark(bookmarkId);
        setBookmarked(false);
        setBookmarkId(null);
      } else {
        const res = await createBookmark(itemType, itemId);
        setBookmarked(true);
        setBookmarkId(res.id);
      }
    } catch { /* silent */ }
  };

  return (
    <button
      onClick={toggle}
      className={`p-1.5 rounded-lg transition-colors ${
        bookmarked
          ? 'text-yellow-400 hover:text-yellow-300'
          : 'text-gray-500 hover:text-gray-300'
      }`}
      title={bookmarked ? 'Yer imini kaldir' : 'Yer imine ekle'}
    >
      {bookmarked ? <HiBookmark className="w-5 h-5" /> : <HiOutlineBookmark className="w-5 h-5" />}
    </button>
  );
}
