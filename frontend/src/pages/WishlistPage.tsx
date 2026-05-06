import React, { useEffect, useState } from 'react';
import { wishlistService } from '../api/services';
import { WishlistItem } from '../types';
import Layout from '../components/Layout';
import Toast, { ToastType } from '../components/Toast';
import { useAuth } from '../context/AuthContext';
import { Trash2, AlertCircle, Clock } from 'lucide-react';

const WishlistPage: React.FC = () => {
  const [items, setItems] = useState<WishlistItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState<{ message: string; type: ToastType } | null>(null);
  const { user, refreshUser } = useAuth();

  const showToast = (message: string, type: ToastType = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  };

  useEffect(() => {
    const fetchWishlist = async () => {
      if (!user) return;
      try {
        const data = await wishlistService.getByUser(user.user_id);
        setItems(data);
      } catch (error) {
        console.error('Failed to fetch wishlist', error);
      } finally {
        setLoading(false);
      }
    };
    fetchWishlist();
  }, [user]);

  const handleRemove = async (itemId: string) => {
    if (!user) return;
    if (!window.confirm('Remove this item from your wishlist?')) return;

    try {
      await wishlistService.removeItem(user.user_id, itemId);
      setItems(items.filter(item => item.item_id !== itemId));
      await refreshUser();
      showToast('Item removed from wishlist', 'info');
    } catch (error) {
      showToast('Failed to remove item', 'error');
    }
  };

  const handleUpdateStatus = async (itemId: string, status: string) => {
    if (!user) return;
    try {
      await wishlistService.updateItem(user.user_id, itemId, { status });
      setItems(items.map(item => item.item_id === itemId ? { ...item, status } : item));
      showToast('Status updated');
    } catch (error) {
      showToast('Failed to update status', 'error');
    }
  };

  return (
    <Layout>
      <div className="mb-12">
        <h1 className="text-5xl font-bold uppercase tracking-tighter mb-2">Your <span className="text-valorant-red">Wishlist</span></h1>
        <p className="text-valorant-gray/60 italic">Track your most wanted skins and their status.</p>
      </div>

      {loading ? (
        <div className="space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="bg-valorant-black/40 border border-valorant-gray/10 p-6 h-32 animate-pulse"></div>
          ))}
        </div>
      ) : items.length === 0 ? (
        <div className="text-center py-20 bg-valorant-black/20 border border-dashed border-valorant-gray/10">
          <AlertCircle size={48} className="mx-auto mb-4 text-valorant-gray/20" />
          <p className="text-xl text-valorant-gray/40 font-bold uppercase tracking-widest">Your wishlist is empty</p>
        </div>
      ) : (
        <div className="space-y-4">
          {items.map((item) => (
            <div key={item.item_id} className="bg-valorant-black border border-valorant-gray/10 p-6 flex flex-col md:flex-row gap-6 items-center">
              <div className="w-full md:w-48 aspect-video bg-valorant-dark/60 p-2">
                {item.image && <img src={item.image} alt={item.skin_name} className="w-full h-full object-contain" />}
              </div>
              
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-bold bg-valorant-red/10 text-valorant-red px-2 py-0.5 uppercase tracking-tighter border border-valorant-red/20">
                    {item.weapon_name}
                  </span>
                  <span className="text-xs font-bold bg-valorant-gray/5 text-valorant-gray/60 px-2 py-0.5 uppercase tracking-tighter flex items-center gap-1">
                    <Clock size={12} />
                    Added {new Date(item.created_at).toLocaleDateString()}
                  </span>
                </div>
                <h2 className="text-2xl font-bold mb-2">{item.skin_name}</h2>
                {item.notes && <p className="text-sm text-valorant-gray/60 italic">"{item.notes}"</p>}
              </div>

              <div className="flex items-center gap-4 w-full md:w-auto">
                <select
                  value={item.status}
                  onChange={(e) => handleUpdateStatus(item.item_id, e.target.value)}
                  className="bg-valorant-dark border border-valorant-gray/10 p-2 text-sm font-bold uppercase outline-none focus:border-valorant-red"
                >
                  <option value="active">Active</option>
                  <option value="acquired">Acquired</option>
                  <option value="waiting">Waiting</option>
                </select>

                <button
                  onClick={() => handleRemove(item.item_id)}
                  className="p-2 text-valorant-gray/40 hover:text-valorant-red transition-colors"
                  title="Remove"
                >
                  <Trash2 size={24} />
                </button>
              </div>
            </div>
          ))}
        </div>
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

export default WishlistPage;
