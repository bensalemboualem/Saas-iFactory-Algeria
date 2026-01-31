import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface User {
  id: string;
  email: string;
  name?: string;
  avatar?: string;
  provider?: 'email' | 'google' | 'github';
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  signup: (email: string, password: string, name?: string) => Promise<void>;
  loginWithGoogle: () => Promise<void>;
  loginWithGithub: () => Promise<void>;
}

// Gateway API URL
const GATEWAY_URL = import.meta.env.VITE_GATEWAY_URL || 'http://localhost:5191';

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
    // Redirection vers Google OAuth via Gateway
    window.location.href = `${GATEWAY_URL}/auth/google`;
  };

  const loginWithGithub = async () => {
    // Redirection vers GitHub OAuth via Gateway
    window.location.href = `${GATEWAY_URL}/auth/github`;
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
        loginWithGithub,
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
