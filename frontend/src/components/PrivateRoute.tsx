import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const PrivateRoute: React.FC = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="min-h-screen bg-valorant-dark flex items-center justify-center font-bold text-valorant-red text-2xl animate-pulse">LOADING...</div>;
  }

  return user ? <Outlet /> : <Navigate to="/login" />;
};

export default PrivateRoute;
