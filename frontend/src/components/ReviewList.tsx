import React from 'react';
import { Review } from '../types';
import { Star, User } from 'lucide-react';

interface ReviewListProps {
  reviews: Review[];
  loading: boolean;
}

const ReviewList: React.FC<ReviewListProps> = ({ reviews, loading }) => {
  if (loading) return <div className="text-center py-4 animate-pulse uppercase font-bold text-xs tracking-widest opacity-50">Loading reviews...</div>;
  
  if (reviews.length === 0) return <div className="text-center py-8 text-valorant-gray/30 italic text-sm border border-dashed border-valorant-gray/10 uppercase tracking-widest">No reviews yet. Be the first!</div>;

  return (
    <div className="space-y-4 max-h-[300px] overflow-y-auto pr-2 custom-scrollbar">
      {reviews.map((review) => (
        <div key={review.review_id} className="bg-valorant-dark/40 border border-valorant-gray/5 p-4">
          <div className="flex justify-between items-start mb-2">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-valorant-red/20 rounded-full flex items-center justify-center text-valorant-red">
                <User size={12} />
              </div>
              <span className="text-xs font-bold uppercase tracking-wider">
                {review.is_anonymous ? 'Anonymous Agent' : review.username}
              </span>
            </div>
            <div className="flex text-yellow-500">
              {[...Array(5)].map((_, i) => (
                <Star key={i} size={10} fill={i < review.rating ? 'currentColor' : 'none'} />
              ))}
            </div>
          </div>
          <p className="text-sm text-valorant-gray/80 italic">"{review.comment}"</p>
          <p className="text-[10px] text-valorant-gray/30 mt-2 uppercase">{new Date(review.created_at).toLocaleDateString()}</p>
        </div>
      ))}
    </div>
  );
};

export default ReviewList;
