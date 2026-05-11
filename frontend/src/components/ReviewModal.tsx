import React, { useState, useEffect, useCallback } from 'react';
import { X, Star } from 'lucide-react';
import { reviewService } from '../api/services';
import { Review } from '../types';
import ReviewList from './ReviewList';

interface ReviewModalProps {
  skinId: string;
  skinName: string;
  userId: string;
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: (message: string) => void;
  onError?: (message: string) => void;
}

const ReviewModal: React.FC<ReviewModalProps> = ({
  skinId,
  skinName,
  userId,
  isOpen,
  onClose,
  onSuccess,
  onError
}) => {
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');
  const [isAnonymous, setIsAnonymous] = useState(false);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loadingReviews, setLoadingReviews] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const fetchReviews = useCallback(async () => {
    if (!skinId) return;
    setLoadingReviews(true);
    try {
      const data = await reviewService.getSkinReviews(skinId);
      setReviews(data);
    } catch (error) {
      if (import.meta.env.VITE_IS_DEV) console.error('Failed to fetch reviews', error);
    } finally {
      setLoadingReviews(false);
    }
  }, [skinId]);

  useEffect(() => {
    if (isOpen) {
      fetchReviews();
    }
  }, [isOpen, fetchReviews]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isSubmitting) return;

    setIsSubmitting(true);
    try {
      await reviewService.createReview({
        user_id: userId,
        item_id: skinId,
        rating,
        comment,
        is_anonymous: isAnonymous
      });

      setComment('');
      if (onSuccess) onSuccess('Review submitted successfully');

      await fetchReviews();
    } catch (error: any) {
      const msg = error.response?.data?.detail || 'Failed to submit review';
      if (onError) onError(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-valorant-dark/95 backdrop-blur-md">
      <div className="bg-valorant-black border border-valorant-red/30 w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col relative">
        <button onClick={onClose} className="absolute top-6 right-6 text-valorant-gray/50 hover:text-valorant-red z-10">
          <X size={24} />
        </button>

        <div className="p-8 grid grid-cols-1 lg:grid-cols-2 gap-12 overflow-y-auto">
          <div>
            <h2 className="text-3xl font-bold mb-2 uppercase tracking-tighter">Review Skin</h2>
            <p className="text-valorant-red font-bold mb-8 italic text-lg">{skinName}</p>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-bold uppercase mb-2">Your Rating</label>
                <div className="flex gap-2">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      type="button"
                      onClick={() => setRating(star)}
                      className={`p-1 transition-colors ${rating >= star ? 'text-yellow-400' : 'text-valorant-gray/20'}`}
                    >
                      <Star size={32} fill={rating >= star ? 'currentColor' : 'none'} />
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-bold uppercase mb-2">Your Thoughts</label>
                <textarea
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  className="w-full bg-valorant-dark border border-valorant-gray/10 p-4 focus:border-valorant-red outline-none min-h-[120px] transition-all"
                  placeholder="What do you think about this skin?"
                  required
                />
              </div>

              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  id="anonymous"
                  checked={isAnonymous}
                  onChange={(e) => setIsAnonymous(e.target.checked)}
                  className="w-5 h-5 accent-valorant-red cursor-pointer"
                />
                <label htmlFor="anonymous" className="text-sm font-bold uppercase cursor-pointer select-none">Post anonymously</label>
              </div>

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full bg-valorant-red text-white py-4 font-bold uppercase tracking-widest hover:bg-valorant-red/80 transition-all shadow-lg shadow-valorant-red/20 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? 'Submitting...' : 'Submit Review'}
              </button>
            </form>
          </div>

          <div className="border-t lg:border-t-0 lg:border-l border-valorant-gray/10 pt-8 lg:pt-0 lg:pl-12">
            <h3 className="text-xl font-bold mb-6 uppercase tracking-tighter flex items-center gap-2">
              Community <span className="text-valorant-red">Reviews</span>
              <span className="text-xs bg-valorant-gray/10 px-2 py-0.5 text-valorant-gray/60">{reviews.length}</span>
            </h3>
            <ReviewList reviews={reviews} loading={loadingReviews} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReviewModal;
