import React, { useEffect, useState } from 'react';
import { userService } from '../api/services';
import Layout from '../components/Layout';
import { UserList, PaginatedResponse } from '../types';
import { User, ChevronLeft, ChevronRight, Search } from 'lucide-react';
import { Link } from 'react-router-dom';

const CommunityPage: React.FC = () => {
  const [data, setData] = useState<PaginatedResponse<UserList> | null>(null);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const size = 12;

  useEffect(() => {
    const fetchUsers = async () => {
      setLoading(true);
      try {
        const response = await userService.listUsers(page, size);
        setData(response);
      } catch (error) {
        console.error('Failed to fetch users:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, [page]);

  return (
    <Layout>
      <div className="mb-12">
        <h1 className="text-5xl font-bold uppercase tracking-tighter mb-2">Agent <span className="text-valorant-red">Community</span></h1>
        <p className="text-valorant-gray/60 italic">Connect with other agents and explore their collections.</p>
      </div>

      <div className="mb-8 relative max-w-md">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-valorant-gray/40">
          <Search size={18} />
        </div>
        <input
          type="text"
          placeholder="Search agents... (Coming soon)"
          disabled
          className="w-full bg-valorant-black border border-valorant-gray/10 p-3 pl-10 focus:border-valorant-red outline-none opacity-50 cursor-not-allowed"
        />
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {[...Array(8)].map((_, i) => (
            <div key={i} className="bg-valorant-black border border-valorant-gray/10 p-6 animate-pulse">
              <div className="w-16 h-16 bg-valorant-gray/10 mx-auto mb-4" />
              <div className="h-4 bg-valorant-gray/10 w-3/4 mx-auto mb-2" />
              <div className="h-3 bg-valorant-gray/10 w-1/2 mx-auto" />
            </div>
          ))}
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {data?.items.map((user) => (
              <Link 
                key={user.user_id} 
                to={`/community/${user.user_id}`}
                className="group bg-valorant-black border border-valorant-gray/10 p-6 text-center hover:border-valorant-red transition-all hover:translate-y-[-4px]"
              >
                <div className="w-16 h-16 bg-valorant-red/10 mx-auto mb-4 flex items-center justify-center text-valorant-red text-2xl font-bold uppercase border-2 border-valorant-red/20 group-hover:bg-valorant-red group-hover:text-white transition-all">
                  {user.username.substring(0, 2)}
                </div>
                <h3 className="text-xl font-bold mb-1 truncate">{user.display_name || user.username}</h3>
                <p className="text-valorant-red text-xs font-bold uppercase tracking-widest">@{user.username}</p>
                
                <div className="mt-6 pt-4 border-t border-valorant-gray/5 opacity-0 group-hover:opacity-100 transition-opacity">
                  <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-valorant-red flex items-center justify-center gap-1">
                    View Profile <ChevronRight size={12} />
                  </span>
                </div>
              </Link>
            ))}
          </div>

          {data && data.pages > 1 && (
            <div className="mt-12 flex justify-center items-center gap-4">
              <button
                onClick={() => setPage(prev => Math.max(prev - 1, 1))}
                disabled={page === 1}
                className="p-2 border border-valorant-gray/10 hover:border-valorant-red disabled:opacity-30 disabled:hover:border-valorant-gray/10 transition-all"
              >
                <ChevronLeft />
              </button>
              <div className="text-sm font-bold uppercase tracking-widest">
                Page <span className="text-valorant-red">{page}</span> of {data.pages}
              </div>
              <button
                onClick={() => setPage(prev => Math.min(prev + 1, data.pages))}
                disabled={page === data.pages}
                className="p-2 border border-valorant-gray/10 hover:border-valorant-red disabled:opacity-30 disabled:hover:border-valorant-gray/10 transition-all"
              >
                <ChevronRight />
              </button>
            </div>
          )}

          {data?.items.length === 0 && (
            <div className="text-center py-20 border border-dashed border-valorant-gray/10">
              <User size={48} className="mx-auto mb-4 text-valorant-gray/20" />
              <p className="text-valorant-gray/40 font-bold uppercase tracking-widest">No agents found.</p>
            </div>
          )}
        </>
      )}
    </Layout>
  );
};

export default CommunityPage;
