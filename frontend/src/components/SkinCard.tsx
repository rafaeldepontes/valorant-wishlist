import React from 'react';
import { Skin } from '../types';
import { Heart, MessageSquare } from 'lucide-react';

interface SkinCardProps {
  skin: Skin;
  isInWishlist: boolean;
  onAddToWishlist: (skin: Skin) => void;
  onRemoveFromWishlist: (skinId: string) => void;
  onReview: (skin: Skin) => void;
}

const SkinCard: React.FC<SkinCardProps> = ({ skin, isInWishlist, onAddToWishlist, onRemoveFromWishlist, onReview }) => {
  return (
    <div className="bg-valorant-black/40 border border-valorant-gray/10 hover:border-valorant-red/40 transition-all p-4 group flex flex-col h-full">
      <div className="aspect-video relative overflow-hidden bg-valorant-dark/60 mb-4">
        {skin.image ? (
          <img
            src={skin.image}
            alt={skin.skin_name}
            className="w-full h-full object-contain group-hover:scale-110 transition-transform duration-500"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-valorant-gray/20 font-bold">
            NO IMAGE
          </div>
        )}
      </div>
      
      <div className="mt-auto">
        <h3 className="text-valorant-red font-bold text-sm uppercase tracking-wider">{skin.weapon_name}</h3>
        <h2 className="text-xl font-bold truncate mb-4">{skin.skin_name}</h2>
        
        <div className="flex gap-2">
          {isInWishlist ? (
            <button
              onClick={() => onRemoveFromWishlist(skin.skin_id)}
              className="flex-1 flex items-center justify-center gap-2 bg-valorant-red text-white hover:bg-valorant-red/80 transition-all py-2 text-sm font-bold uppercase"
            >
              REMOVE
            </button>
          ) : (
            <button
              onClick={() => onAddToWishlist(skin)}
              className="flex-1 flex items-center justify-center gap-2 bg-valorant-gray/10 hover:bg-valorant-red hover:text-white transition-all py-2 text-sm font-bold uppercase"
            >
              <Heart size={16} />
              Wishlist
            </button>
          )}
          <button
            onClick={() => onReview(skin)}
            className="flex items-center justify-center bg-valorant-gray/10 hover:bg-valorant-gray/20 transition-all p-2"
            title="Review"
          >
            <MessageSquare size={16} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default SkinCard;
