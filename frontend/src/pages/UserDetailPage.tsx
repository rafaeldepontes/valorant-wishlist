import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { userService, wishlistService, reviewService } from '../api/services';
import Layout from '../components/Layout';
import { User, WishlistItem, Review } from '../types';
import { Shield, ChevronLeft, Heart, MessageSquare, Star } from 'lucide-react';
import ReviewList from '../components/ReviewList';

const UserDetailPage: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const [userData, setUserData] = useState<User | null>(null);
  const [wishlist, setWishlist] = useState<WishlistItem[]>([]);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      if (!userId) return;
      setLoading(true);
      try {
        const [u, w, r] = await Promise.all([
          userService.getUser(userId),
          wishlistService.getByUser(userId),
          reviewService.getUserReviews(userId)
        ]);
        setUserData(u);
        setWishlist(w);
        setReviews(r);
      } catch (error) {
        if (import.meta.env.VITE_IS_DEV) console.error('Failed to fetch user details:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [userId]);

  if (loading) {
    return (
      <Layout>
        <div className="animate-pulse">
          <div className="h-12 bg-valorant-gray/10 w-1/3 mb-8" />
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="h-64 bg-valorant-gray/10" />
            <div className="lg:col-span-2 h-64 bg-valorant-gray/10" />
          </div>
        </div>
      </Layout>
    );
  }

  if (!userData) {
    return (
      <Layout>
        <div className="text-center py-20">
          <h2 className="text-3xl font-bold uppercase">Agent not found</h2>
          <Link to="/community" className="text-valorant-red font-bold uppercase mt-4 inline-block hover:underline">Back to Community</Link>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="mb-8">
        <Link to="/community" className="text-valorant-gray/40 hover:text-valorant-red flex items-center gap-1 text-xs font-bold uppercase tracking-widest transition-all mb-4">
          <ChevronLeft size={14} /> Back to Community
        </Link>
        <h1 className="text-5xl font-bold uppercase tracking-tighter mb-2">Agent <span className="text-valorant-red">Profile</span></h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-1">
          <div className="bg-valorant-black border border-valorant-gray/10 p-8 text-center sticky top-24">
            <div className="w-32 h-32 bg-valorant-red mx-auto mb-6 flex items-center justify-center text-white text-5xl font-bold uppercase tracking-tighter border-4 border-valorant-gray/10 shadow-xl shadow-valorant-red/10">
              {userData.username.substring(0, 2)}
            </div>
            <h2 className="text-2xl font-bold mb-1">{userData.display_name || userData.username}</h2>
            <p className="text-valorant-red font-bold text-sm uppercase tracking-widest mb-6">@{userData.username}</p>

            <div className="grid grid-cols-2 gap-4 text-sm font-bold uppercase border-t border-valorant-gray/10 pt-6 mb-6">
              <div>
                <p className="text-valorant-gray/40 mb-1">Status</p>
                <p className="text-green-500 flex items-center justify-center gap-1 text-xs">
                  <Shield size={12} /> {userData.status}
                </p>
              </div>
              <div>
                <p className="text-valorant-gray/40 mb-1">Wishlist</p>
                <p className="text-xs">{userData.wishlist_count} Items</p>
              </div>
            </div>

            {userData.favorite_weapon && (
              <div className="text-left mb-4">
                <p className="text-[10px] font-bold text-valorant-gray/40 uppercase tracking-widest mb-1">Favorite Weapon</p>
                <p className="text-sm font-bold">{userData.favorite_weapon}</p>
              </div>
            )}

            {userData.bio && (
              <div className="text-left">
                <p className="text-[10px] font-bold text-valorant-gray/40 uppercase tracking-widest mb-1">Bio</p>
                <p className="text-sm text-valorant-gray/80 italic line-clamp-4">{userData.bio}</p>
              </div>
            )}
          </div>
        </div>

        <div className="lg:col-span-2 space-y-12">
          {/* Wishlist Section */}
          <section>
            <div className="flex items-center gap-4 mb-6">
              <Heart className="text-valorant-red" fill="currentColor" size={24} />
              <h2 className="text-3xl font-bold uppercase tracking-tighter">Collection <span className="text-valorant-red">Wishlist</span></h2>
            </div>

            {wishlist.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {wishlist.map((item) => (
                  <div key={item.item_id} className="bg-valorant-black/40 border border-valorant-gray/10 p-4 flex gap-4">
                    <div className="w-24 h-24 bg-valorant-dark/60 flex-shrink-0">
                      {item.image ? (
                        <img src={item.image} alt={item.skin_name} className="w-full h-full object-contain" />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center text-[10px] font-bold text-valorant-gray/20">NO IMG</div>
                      )}
                    </div>
                    <div className="flex flex-col justify-center">
                      <p className="text-valorant-red font-bold text-[10px] uppercase">{item.weapon_name}</p>
                      <h3 className="text-lg font-bold leading-tight mb-1">{item.skin_name}</h3>
                      <div className="flex gap-1">
                        {[...Array(item.priority)].map((_, i) => (
                          <div key={i} className="w-2 h-2 bg-valorant-red rotate-45" />
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="py-12 text-center border border-dashed border-valorant-gray/10 text-valorant-gray/30 uppercase text-sm font-bold tracking-widest">
                Wishlist is empty
              </div>
            )}
          </section>

          {/* Reviews Section */}
          <section>
            <div className="flex items-center gap-4 mb-6">
              <MessageSquare className="text-valorant-red" size={24} />
              <h2 className="text-3xl font-bold uppercase tracking-tighter">Field <span className="text-valorant-red">Reports</span></h2>
            </div>

            <div className="bg-valorant-black border border-valorant-gray/10 p-6">
              <ReviewList reviews={reviews} loading={false} />
            </div>
          </section>
        </div>
      </div>
    </Layout>
  );
};

export default UserDetailPage;
