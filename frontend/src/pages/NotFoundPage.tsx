import React from 'react';
import { Link } from 'react-router-dom';

const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-valorant-dark text-valorant-gray">
      <div className="text-center max-w-lg">
        <h1 className="text-9xl font-black text-valorant-red mb-4 opacity-20 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 select-none pointer-events-none">404</h1>
        
        <div className="relative z-10">
          <h2 className="text-4xl font-bold mb-4 uppercase tracking-tighter">Mission Failed</h2>
          <p className="text-xl mb-8 text-valorant-gray/70">
            The page you're looking for has been defused or moved to another site.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/" 
              className="bg-valorant-red text-white px-8 py-3 font-bold uppercase tracking-widest hover:bg-valorant-red/80 transition-all border-r-4 border-b-4 border-white/20 active:translate-y-1 active:translate-x-1 active:border-none"
            >
              Return to Base
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotFoundPage;
