import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login({ username, password });
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center p-4">
      <div className="bg-valorant-black border border-valorant-red/30 w-full max-w-md p-8">
        <h1 className="text-4xl font-bold mb-2 uppercase tracking-tighter">Login</h1>
        <p className="text-valorant-gray/60 mb-8">Enter your credentials to access your wishlist.</p>

        {error && (
          <div className="bg-valorant-red/10 border-l-4 border-valorant-red p-4 mb-6 text-valorant-red font-bold text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-bold uppercase mb-2">Username or Email</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-valorant-dark border border-valorant-gray/10 p-3 focus:border-valorant-red outline-none transition-all"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-bold uppercase mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-valorant-dark border border-valorant-gray/10 p-3 focus:border-valorant-red outline-none transition-all"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full bg-valorant-red text-white py-3 font-bold uppercase tracking-widest hover:bg-valorant-red/80 transition-all ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <p className="mt-8 text-center text-sm">
          Don't have an account?{' '}
          <Link to="/register" className="text-valorant-red font-bold hover:underline">Register now</Link>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
