import api from '../client';
import { User, Skin, WishlistItem, Review, TokenResponse, PaginatedResponse, UserList } from '../../types';

export const authService = {
  login: async (data: any): Promise<TokenResponse> => {
    const response = await api.post<TokenResponse>('/auth/login', data);
    return response.data;
  },
  register: async (data: any): Promise<User> => {
    const response = await api.post<User>('/auth/register', data);
    return response.data;
  },
  logout: async (): Promise<void> => {
    await api.post('/auth/logout');
  },
};

export const userService = {
  getMe: async (): Promise<User> => {
    const response = await api.get<User>('/users/me');
    return response.data;
  },
  getUser: async (userId: string): Promise<User> => {
    const response = await api.get<User>(`/users/${userId}`);
    return response.data;
  },
  listUsers: async (page: number = 1, size: number = 10): Promise<PaginatedResponse<UserList>> => {
    const response = await api.get<PaginatedResponse<UserList>>(`/users?page=${page}&size=${size}`);
    return response.data;
  },
  updateProfile: async (userId: string, data: any): Promise<User> => {
    const response = await api.patch<User>(`/users/${userId}`, data);
    return response.data;
  },
};

export const skinService = {
  getAll: async (): Promise<Skin[]> => {
    const response = await api.get<Skin[]>('/skins');
    return response.data;
  },
};

export const wishlistService = {
  getByUser: async (userId: string): Promise<WishlistItem[]> => {
    const response = await api.get<WishlistItem[]>(`/wishlist/${userId}`);
    return response.data;
  },
  addItem: async (data: any): Promise<WishlistItem> => {
    const response = await api.post<WishlistItem>('/wishlist', data);
    return response.data;
  },
  updateItem: async (userId: string, itemId: string, data: any): Promise<WishlistItem> => {
    const response = await api.patch<WishlistItem>(`/wishlist/${userId}/${itemId}`, data);
    return response.data;
  },
  removeItem: async (userId: string, itemId: string): Promise<void> => {
    await api.delete(`/wishlist/${userId}/${itemId}`);
  },
};

export const reviewService = {
  getSkinReviews: async (itemId: string): Promise<Review[]> => {
    const response = await api.get<Review[]>(`/reviews/skin/${itemId}`);
    return response.data;
  },
  getUserReviews: async (userId: string): Promise<Review[]> => {
    const response = await api.get<Review[]>(`/reviews/user/${userId}`);
    return response.data;
  },
  createReview: async (data: any): Promise<Review> => {
    const response = await api.post<Review>('/reviews', data);
    return response.data;
  },
  updateReview: async (reviewId: string, data: any): Promise<Review> => {
    const response = await api.patch<Review>(`/reviews/${reviewId}`, data);
    return response.data;
  },
  deleteReview: async (reviewId: string): Promise<void> => {
    await api.delete(`/reviews/${reviewId}`);
  },
};
