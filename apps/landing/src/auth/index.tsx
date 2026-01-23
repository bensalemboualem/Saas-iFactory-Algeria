import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface User {
  id: string;
  email: string;
  name?: string;
  avatar?: string;
  provider?: 'email' | 'google' | 'facebook';
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  signup: (email: string, password: string, name?: string) => Promise<void>;
  loginWithGoogle: () => Promise<void>;
  loginWithFacebook: () => Promise<void>;
}

// Gateway API URL
const GATEWAY_URL = import.meta.env.VITE_GATEWAY_URL || 'http://localhost:3001';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for existing session
    const savedUser = localStorage.getItem('iaf_user');
    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser));
      } catch {
        localStorage.removeItem('iaf_user');
      }
    }
    setIsLoading(false);
  }, []);

  const saveUser = (userData: User) => {
    setUser(userData);
    localStorage.setItem('iaf_user', JSON.stringify(userData));
  };

  const login = async (email: string, _password: string) => {
    // TODO: Implement real auth with Gateway
    const mockUser: User = {
      id: crypto.randomUUID(),
      email,
      name: email.split('@')[0],
      provider: 'email',
    };
    saveUser(mockUser);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('iaf_user');
    localStorage.removeItem('iaf_token');
  };

  const signup = async (email: string, _password: string, name?: string) => {
    // TODO: Implement real signup with Gateway
    const mockUser: User = {
      id: crypto.randomUUID(),
      email,
      name: name || email.split('@')[0],
      provider: 'email',
    };
    saveUser(mockUser);
  };

  const loginWithGoogle = async () => {
    // TODO: Implement real Google OAuth with Gateway
    // For now, simulate a successful Google login
    // In production, this would redirect to: ${GATEWAY_URL}/auth/google
    const mockUser: User = {
      id: crypto.randomUUID(),
      email: 'user@gmail.com',
      name: 'Google User',
      avatar: 'https://lh3.googleusercontent.com/a/default-user',
      provider: 'google',
    };

    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 800));
    saveUser(mockUser);
  };

  const loginWithFacebook = async () => {
    // TODO: Implement real Facebook OAuth with Gateway
    // For now, simulate a successful Facebook login
    // In production, this would redirect to: ${GATEWAY_URL}/auth/facebook
    const mockUser: User = {
      id: crypto.randomUUID(),
      email: 'user@facebook.com',
      name: 'Facebook User',
      avatar: 'https://graph.facebook.com/default/picture',
      provider: 'facebook',
    };

    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 800));
    saveUser(mockUser);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        login,
        logout,
        signup,
        loginWithGoogle,
        loginWithFacebook,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
