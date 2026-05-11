import React, { useEffect, useState } from 'react';
import { skinService, wishlistService, reviewService } from '../api/services';
import { Skin, WishlistItem } from '../types';
import SkinCard from '../components/SkinCard';
import Layout from '../components/Layout';
import ReviewModal from '../components/ReviewModal';
import Toast, { ToastType } from '../components/Toast';
import { useAuth } from '../context/AuthContext';
import { Search, ChevronLeft, ChevronRight } from 'lucide-react';

const SkinsPage: React.FC = () => {
  const [skins, setSkins] = useState<Skin[]>([]);
  const [filteredSkins, setFilteredSkins] = useState<Skin[]>([]);
  const [wishlistIds, setWishlistIds] = useState<Set<string>>(new Set());
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [selectedSkin, setSelectedSkin] = useState<Skin | null>(null);
  const [isReviewModalOpen, setIsReviewModalOpen] = useState(false);

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(10);

  // Toast state
  const [toast, setToast] = useState<{ message: string; type: ToastType } | null>(null);

  const { user, refreshUser } = useAuth();

  const showToast = (message: string, type: ToastType = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  };

  const fetchWishlist = async () => {
    if (!user) return;
    try {
      const data = await wishlistService.getByUser(user.user_id);
      setWishlistIds(new Set(data.map(item => item.item_id)));
    } catch (error) {
      if (import.meta.env.VITE_IS_DEV) console.error('Failed to fetch wishlist', error);
    }
  };

  useEffect(() => {
    const initData = async () => {
      setLoading(true);
      try {
        const data = await skinService.getAll();
        setSkins(data);
        setFilteredSkins(data);
        if (user) {
          await fetchWishlist();
        }
      } catch (error) {
        if (import.meta.env.VITE_IS_DEV) console.error('Failed to fetch skins', error);
        showToast('Failed to load skins', 'error');
      } finally {
        setLoading(false);
      }
    };
    initData();
  }, [user]);

  useEffect(() => {
    const results = skins.filter(skin =>
      skin.skin_name.toLowerCase().includes(search.toLowerCase()) ||
      skin.weapon_name.toLowerCase().includes(search.toLowerCase())
    );
    setFilteredSkins(results);
    setCurrentPage(1);
  }, [search, skins]);

  const handleAddToWishlist = async (skin: Skin) => {
    if (!user) return;
    try {
      await wishlistService.addItem({
        user_id: user.user_id,
        item_id: skin.skin_id,
      });
      setWishlistIds(prev => new Set([...Array.from(prev), skin.skin_id]));
      await refreshUser();
      showToast(`Added ${skin.skin_name} to wishlist`);
    } catch (error: any) {
      showToast(error.response?.data?.detail || 'Failed to add to wishlist', 'error');
    }
  };

  const handleRemoveFromWishlist = async (skinId: string) => {
    if (!user) return;
    try {
      await wishlistService.removeItem(user.user_id, skinId);
      setWishlistIds(prev => {
        const next = new Set(prev);
        next.delete(skinId);
        return next;
      });
      await refreshUser();
      showToast('Removed from wishlist', 'info');
    } catch (error: any) {
      showToast(error.response?.data?.detail || 'Failed to remove from wishlist', 'error');
    }
  };

  const handleOpenReview = (skin: Skin) => {
    setSelectedSkin(skin);
    setIsReviewModalOpen(true);
  };

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentSkins = filteredSkins.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(filteredSkins.length / itemsPerPage);

  const paginate = (pageNumber: number) => setCurrentPage(pageNumber);

  return (
    <Layout>
      <div className="mb-12">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8">
          <div>
            <h1 className="text-5xl font-bold uppercase tracking-tighter mb-4">Available <span className="text-valorant-red">Skins</span></h1>
            <div className="relative max-w-xl">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-valorant-gray/40" size={20} />
              <input
                type="text"
                placeholder="Search for skins or weapons..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full bg-valorant-black border border-valorant-gray/10 py-4 pl-12 pr-4 focus:border-valorant-red outline-none transition-all text-lg"
              />
            </div>
          </div>

          <div className="flex items-center gap-4">
            <span className="text-xs font-bold uppercase tracking-widest text-valorant-gray/40">Items per page</span>
            <div className="flex bg-valorant-black border border-valorant-gray/10 p-1">
              {[5, 10, 20].map(size => (
                <button
                  key={size}
                  onClick={() => {
                    setItemsPerPage(size);
                    setCurrentPage(1);
                  }}
                  className={`px-4 py-1 text-sm font-bold transition-all ${itemsPerPage === size ? 'bg-valorant-red text-white' : 'hover:bg-valorant-gray/5'}`}
                >
                  {size}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {[...Array(itemsPerPage)].map((_, i) => (
            <div key={i} className="bg-valorant-black/40 border border-valorant-gray/10 p-4 h-64 animate-pulse"></div>
          ))}
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-12">
            {currentSkins.map((skin) => (
              <SkinCard
                key={skin.skin_id}
                skin={skin}
                isInWishlist={wishlistIds.has(skin.skin_id)}
                onAddToWishlist={handleAddToWishlist}
                onRemoveFromWishlist={handleRemoveFromWishlist}
                onReview={handleOpenReview}
              />
            ))}
          </div>

          {/* Pagination Controls */}
          {totalPages > 1 && (
            <div className="flex justify-center items-center gap-2">
              <button
                onClick={() => paginate(Math.max(1, currentPage - 1))}
                disabled={currentPage === 1}
                className="p-2 bg-valorant-black border border-valorant-gray/10 disabled:opacity-20 hover:border-valorant-red transition-all"
              >
                <ChevronLeft size={20} />
              </button>

              <div className="flex gap-2">
                {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                  let pageNum;
                  if (totalPages <= 5) pageNum = i + 1;
                  else if (currentPage <= 3) pageNum = i + 1;
                  else if (currentPage >= totalPages - 2) pageNum = totalPages - 4 + i;
                  else pageNum = currentPage - 2 + i;

                  return (
                    <button
                      key={pageNum}
                      onClick={() => paginate(pageNum)}
                      className={`w-10 h-10 font-bold border transition-all ${currentPage === pageNum ? 'bg-valorant-red border-valorant-red text-white' : 'bg-valorant-black border-valorant-gray/10 hover:border-valorant-red/50'}`}
                    >
                      {pageNum}
                    </button>
                  );
                })}
              </div>

              <button
                onClick={() => paginate(Math.min(totalPages, currentPage + 1))}
                disabled={currentPage === totalPages}
                className="p-2 bg-valorant-black border border-valorant-gray/10 disabled:opacity-20 hover:border-valorant-red transition-all"
              >
                <ChevronRight size={20} />
              </button>
            </div>
          )}
          <p className="text-center mt-4 text-xs font-bold uppercase tracking-widest text-valorant-gray/20">
            Showing {indexOfFirstItem + 1} - {Math.min(indexOfLastItem, filteredSkins.length)} of {filteredSkins.length} Skins
          </p>
        </>
      )}

      {selectedSkin && user && (
        <ReviewModal
          isOpen={isReviewModalOpen}
          onClose={() => setIsReviewModalOpen(false)}
          skinId={selectedSkin.skin_id}
          skinName={selectedSkin.skin_name}
          userId={user.user_id}
          onSuccess={(msg) => showToast(msg)}
          onError={(msg) => showToast(msg, 'error')}
        />
      )}

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </Layout>
  );
};

export default SkinsPage;
