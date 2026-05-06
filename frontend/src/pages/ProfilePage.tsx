import React, { useState } from 'react';
import { userService } from '../api/services';
import Layout from '../components/Layout';
import { useAuth } from '../context/AuthContext';
import { User, Mail, Shield, Save } from 'lucide-react';

const ProfilePage: React.FC = () => {
  const { user, updateUser } = useAuth();
  const [formData, setFormData] = useState({
    display_name: user?.display_name || '',
    bio: user?.bio || '',
    favorite_weapon: user?.favorite_weapon || '',
    email: user?.email || '',
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) return;
    
    setLoading(true);
    setMessage({ type: '', text: '' });

    try {
      const updatedUser = await userService.updateProfile(user.user_id, formData);
      updateUser(updatedUser);
      setMessage({ type: 'success', text: 'Profile updated successfully!' });
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to update profile' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="mb-12">
        <h1 className="text-5xl font-bold uppercase tracking-tighter mb-2">Agent <span className="text-valorant-red">Profile</span></h1>
        <p className="text-valorant-gray/60 italic">Customize your identity in the skin network.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-1">
          <div className="bg-valorant-black border border-valorant-gray/10 p-8 text-center">
            <div className="w-32 h-32 bg-valorant-red mx-auto mb-6 flex items-center justify-center text-white text-5xl font-bold uppercase tracking-tighter border-4 border-valorant-gray/10 shadow-xl shadow-valorant-red/10">
              {user?.username.substring(0, 2)}
            </div>
            <h2 className="text-2xl font-bold mb-1">{user?.display_name || user?.username}</h2>
            <p className="text-valorant-red font-bold text-sm uppercase tracking-widest mb-6">@{user?.username}</p>
            
            <div className="grid grid-cols-2 gap-4 text-sm font-bold uppercase border-t border-valorant-gray/10 pt-6">
              <div>
                <p className="text-valorant-gray/40 mb-1">Status</p>
                <p className="text-green-500 flex items-center justify-center gap-1">
                  <Shield size={14} />
                  Active
                </p>
              </div>
              <div>
                <p className="text-valorant-gray/40 mb-1">Wishlist</p>
                <p>{user?.wishlist_count || 0} Items</p>
              </div>
            </div>
          </div>
        </div>

        <div className="lg:col-span-2">
          <form onSubmit={handleSubmit} className="bg-valorant-black border border-valorant-gray/10 p-8 space-y-6">
            {message.text && (
              <div className={`p-4 font-bold text-sm ${message.type === 'success' ? 'bg-green-500/10 border-l-4 border-green-500 text-green-500' : 'bg-valorant-red/10 border-l-4 border-valorant-red text-valorant-red'}`}>
                {message.text}
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-bold uppercase mb-2 flex items-center gap-2">
                  <User size={16} /> Display Name
                </label>
                <input
                  type="text"
                  name="display_name"
                  value={formData.display_name}
                  onChange={handleChange}
                  className="w-full bg-valorant-dark border border-valorant-gray/10 p-3 focus:border-valorant-red outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-bold uppercase mb-2 flex items-center gap-2">
                  <Mail size={16} /> Email Address
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full bg-valorant-dark border border-valorant-gray/10 p-3 focus:border-valorant-red outline-none"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-bold uppercase mb-2">Favorite Weapon</label>
              <input
                type="text"
                name="favorite_weapon"
                value={formData.favorite_weapon}
                onChange={handleChange}
                placeholder="e.g. Vandal, Operator"
                className="w-full bg-valorant-dark border border-valorant-gray/10 p-3 focus:border-valorant-red outline-none"
              />
            </div>

            <div>
              <label className="block text-sm font-bold uppercase mb-2">Agent Bio</label>
              <textarea
                name="bio"
                value={formData.bio}
                onChange={handleChange}
                className="w-full bg-valorant-dark border border-valorant-gray/10 p-3 focus:border-valorant-red outline-none min-h-[120px]"
                placeholder="Tell us about your Valorant journey..."
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="flex items-center justify-center gap-2 bg-valorant-red text-white px-8 py-3 font-bold uppercase tracking-widest hover:bg-valorant-red/80 transition-all ml-auto w-full md:w-auto"
            >
              <Save size={18} />
              {loading ? 'Saving...' : 'Save Changes'}
            </button>
          </form>
        </div>
      </div>
    </Layout>
  );
};

export default ProfilePage;
