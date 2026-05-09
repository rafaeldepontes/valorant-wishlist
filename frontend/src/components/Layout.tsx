import React from 'react';
import Navbar from './Navbar';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-valorant-dark text-valorant-gray">
      <Navbar />
      <main className="max-w-7xl mx-auto py-8 px-6">
        {children}
      </main>
    </div>
  );
};

export default Layout;
