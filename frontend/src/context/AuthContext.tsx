import React, { createContext, useContext, useState, useEffect } from 'react';
import { User } from '../types';
import { authService, userService } from '../api/services';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (data: any) => Promise<void>;
  register: (data: any) => Promise<void>;
  logout: () => Promise<void>;
  updateUser: (data: Partial<User>) => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchUserData = async () => {
    try {
      const userData = await userService.getMe();
      setUser(userData);
    } catch (error) {
      if (import.meta.env.VITE_IS_DEV) console.error('Failed to fetch user', error);
      setUser(null);
    }
  };

  useEffect(() => {
    const initAuth = async () => {
      await fetchUserData();
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (data: any) => {
    await authService.login(data);
    await fetchUserData();
  };

  const register = async (data: any) => {
    await authService.register(data);
  };

  const logout = async () => {
    try {
      await authService.logout();
    } catch (error) {
      if (import.meta.env.VITE_IS_DEV) console.error('Logout failed', error);
    } finally {
      setUser(null);
    }
  };

  const updateUser = (data: Partial<User>) => {
    if (user) {
      setUser({ ...user, ...data });
    }
  };

  const refreshUser = async () => {
    await fetchUserData();
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, updateUser, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
