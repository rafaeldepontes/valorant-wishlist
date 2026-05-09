import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './components/PrivateRoute';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import SkinsPage from './pages/SkinsPage';
import WishlistPage from './pages/WishlistPage';
import ProfilePage from './pages/ProfilePage';
import CommunityPage from './pages/CommunityPage';
import UserDetailPage from './pages/UserDetailPage';
import NotFoundPage from './pages/NotFoundPage';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-valorant-dark text-valorant-gray">
          <Routes>
            {/* Public Routes */}
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />

            {/* Private Routes */}
            <Route element={<PrivateRoute />}>
              <Route path="/" element={<SkinsPage />} />
              <Route path="/wishlist" element={<WishlistPage />} />
              <Route path="/community" element={<CommunityPage />} />
              <Route path="/community/:userId" element={<UserDetailPage />} />
              <Route path="/profile" element={<ProfilePage />} />
            </Route>

            {/* Catch-all Route */}
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
