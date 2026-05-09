import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogOut, User as UserIcon, Heart, ShoppingBag, Users } from 'lucide-react';

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-valorant-black border-b border-valorant-red/20 py-4 px-6 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold text-valorant-red tracking-tighter hover:opacity-80 transition-opacity">
          VALORANT <span className="text-valorant-gray">WISHLIST</span>
        </Link>

        <div className="flex items-center space-x-6">
          {user ? (
            <>
              <Link to="/" className="hover:text-valorant-red transition-colors flex items-center gap-2">
                <ShoppingBag size={20} />
                <span>Skins</span>
              </Link>
              <Link to="/wishlist" className="hover:text-valorant-red transition-colors flex items-center gap-2">
                <Heart size={20} />
                <span>Wishlist</span>
              </Link>
              <Link to="/community" className="hover:text-valorant-red transition-colors flex items-center gap-2">
                <Users size={20} />
                <span>Community</span>
              </Link>
              <Link to="/profile" className="hover:text-valorant-red transition-colors flex items-center gap-2">
                <UserIcon size={20} />
                <span>Profile</span>
              </Link>
              <button
                onClick={handleLogout}
                className="hover:text-valorant-red transition-colors flex items-center gap-2"
              >
                <LogOut size={20} />
                <span>Logout</span>
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="hover:text-valorant-red transition-colors">Login</Link>
              <Link to="/register" className="bg-valorant-red text-white px-4 py-2 hover:bg-valorant-red/80 transition-all font-bold">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
