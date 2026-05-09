import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const RegisterPage: React.FC = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);

    try {
      await register({
        username: formData.username,
        email: formData.email,
        password: formData.password,
      });
      navigate('/login');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to register');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center p-4">
      <div className="bg-valorant-black border border-valorant-red/30 w-full max-w-md p-8">
        <h1 className="text-4xl font-bold mb-2 uppercase tracking-tighter">Register</h1>
        <p className="text-valorant-gray/60 mb-8">Create an account to track your favorite skins.</p>

        {error && (
          <div className="bg-valorant-red/10 border-l-4 border-valorant-red p-4 mb-6 text-valorant-red font-bold text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-bold uppercase mb-2">Username</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              className="w-full bg-valorant-dark border border-valorant-gray/10 p-3 focus:border-valorant-red outline-none transition-all"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-bold uppercase mb-2">Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="w-full bg-valorant-dark border border-valorant-gray/10 p-3 focus:border-valorant-red outline-none transition-all"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-bold uppercase mb-2">Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className="w-full bg-valorant-dark border border-valorant-gray/10 p-3 focus:border-valorant-red outline-none transition-all"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-bold uppercase mb-2">Confirm Password</label>
            <input
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              className="w-full bg-valorant-dark border border-valorant-gray/10 p-3 focus:border-valorant-red outline-none transition-all"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full bg-valorant-red text-white py-3 font-bold uppercase tracking-widest hover:bg-valorant-red/80 transition-all mt-4 ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            {loading ? 'Creating account...' : 'Register'}
          </button>
        </form>

        <p className="mt-8 text-center text-sm">
          Already have an account?{' '}
          <Link to="/login" className="text-valorant-red font-bold hover:underline">Login here</Link>
        </p>
      </div>
    </div>
  );
};

export default RegisterPage;
