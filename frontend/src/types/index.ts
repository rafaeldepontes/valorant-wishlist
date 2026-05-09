export interface User {
  user_id: string;
  username: string;
  email: string;
  display_name?: string;
  favorite_weapon?: string;
  bio?: string;
  wishlist_count: number;
  status: string;
  created_at: string;
}

export interface UserList {
  user_id: string;
  username: string;
  display_name?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface Skin {
  weapon_name: string;
  skin_id: string;
  skin_name: string;
  image?: string;
}

export interface WishlistItem {
  user_id: string;
  item_id: string;
  notes?: string;
  priority: number;
  notify_on_sale: boolean;
  status: string;
  created_at: string;
  updated_at: string;
  weapon_name: string;
  skin_name: string;
  image?: string;
}

export interface Review {
  review_id: string;
  user_id?: string;
  username?: string;
  item_id: string;
  weapon_name: string;
  skin_name: string;
  rating: number;
  comment: string;
  is_anonymous: boolean;
  created_at: string;
  updated_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}
