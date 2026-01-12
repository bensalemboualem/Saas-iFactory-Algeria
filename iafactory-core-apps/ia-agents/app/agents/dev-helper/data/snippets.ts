export interface CodeSnippet {
  id: string;
  name: string;
  description: string;
  code: string;
  language: string;
  category: 'react' | 'nextjs' | 'nodejs' | 'python' | 'typescript' | 'utils';
  tags: string[];
}

export const SNIPPETS: CodeSnippet[] = [
  // React Hooks
  {
    id: 'use-local-storage',
    name: 'useLocalStorage Hook',
    description: 'Custom hook pour persister state dans localStorage',
    language: 'typescript',
    category: 'react',
    tags: ['hooks', 'localStorage', 'custom-hook'],
    code: `function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    const saved = localStorage.getItem(key);
    return saved ? JSON.parse(saved) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}

// Usage
const [user, setUser] = useLocalStorage('user', null);`,
  },
  {
    id: 'use-debounce',
    name: 'useDebounce Hook',
    description: 'Debounce une valeur (utile pour search)',
    language: 'typescript',
    category: 'react',
    tags: ['hooks', 'debounce', 'performance'],
    code: `function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
const debouncedSearch = useDebounce(searchTerm, 500);`,
  },
  {
    id: 'use-fetch',
    name: 'useFetch Hook',
    description: 'Hook pour fetch data avec loading/error states',
    language: 'typescript',
    category: 'react',
    tags: ['hooks', 'fetch', 'api'],
    code: `function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    fetch(url)
      .then(res => {
        if (!res.ok) throw new Error('Network response was not ok');
        return res.json();
      })
      .then(data => {
        if (!cancelled) {
          setData(data);
          setLoading(false);
        }
      })
      .catch(err => {
        if (!cancelled) {
          setError(err.message);
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [url]);

  return { data, loading, error };
}

// Usage
const { data, loading, error } = useFetch('/api/users');`,
  },

  // Next.js
  {
    id: 'nextjs-api-route',
    name: 'Next.js API Route',
    description: 'Template API route avec error handling',
    language: 'typescript',
    category: 'nextjs',
    tags: ['api', 'route', 'error-handling'],
    code: `import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  try {
    // Your logic here
    const data = { message: 'Success' };

    return NextResponse.json(data);
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();

    // Validate input
    if (!body.name) {
      return NextResponse.json(
        { error: 'Name is required' },
        { status: 400 }
      );
    }

    // Your logic here

    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}`,
  },
  {
    id: 'nextjs-server-action',
    name: 'Next.js Server Action',
    description: 'Server action avec validation',
    language: 'typescript',
    category: 'nextjs',
    tags: ['server-action', 'form'],
    code: `'use server';

import { z } from 'zod';
import { revalidatePath } from 'next/cache';

const schema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

export async function createUser(formData: FormData) {
  const validatedFields = schema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
  });

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    };
  }

  try {
    // Database operation here

    revalidatePath('/users');
    return { success: true };
  } catch (error) {
    return { error: 'Failed to create user' };
  }
}`,
  },

  // API Calls
  {
    id: 'fetch-post',
    name: 'Fetch POST Request',
    description: 'POST avec JSON et error handling',
    language: 'javascript',
    category: 'utils',
    tags: ['fetch', 'api', 'post'],
    code: `async function postData(url, data) {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(\`HTTP error! status: \${response.status}\`);
    }

    return await response.json();
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
}

// Usage
const result = await postData('/api/users', {
  name: 'John',
  email: 'john@example.com'
});`,
  },
  {
    id: 'fetch-with-retry',
    name: 'Fetch with Retry',
    description: 'Fetch avec retry automatique',
    language: 'typescript',
    category: 'utils',
    tags: ['fetch', 'retry', 'resilience'],
    code: `async function fetchWithRetry<T>(
  url: string,
  options = {},
  retries = 3
): Promise<T> {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url, options);

      if (!response.ok) {
        throw new Error(\`HTTP \${response.status}\`);
      }

      return await response.json();
    } catch (error) {
      const isLastAttempt = i === retries - 1;

      if (isLastAttempt) throw error;

      // Exponential backoff
      const delay = 1000 * Math.pow(2, i);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw new Error('Retry failed');
}`,
  },

  // TypeScript
  {
    id: 'typescript-utility-types',
    name: 'TypeScript Utility Types',
    description: 'Utility types courants',
    language: 'typescript',
    category: 'typescript',
    tags: ['types', 'utility'],
    code: `// Partial - Tous les champs optionnels
type PartialUser = Partial<User>;

// Required - Tous les champs obligatoires
type RequiredUser = Required<User>;

// Pick - Sélectionner certains champs
type UserPreview = Pick<User, 'id' | 'name'>;

// Omit - Exclure certains champs
type UserWithoutPassword = Omit<User, 'password'>;

// Record - Object avec clés typées
type UserRoles = Record<string, 'admin' | 'user'>;

// Readonly - Tous les champs en lecture seule
type ReadonlyUser = Readonly<User>;

// ReturnType - Type de retour d'une fonction
type Result = ReturnType<typeof myFunction>;`,
  },
  {
    id: 'typescript-generic-api',
    name: 'Generic API Response Type',
    description: 'Type générique pour API responses',
    language: 'typescript',
    category: 'typescript',
    tags: ['types', 'generics', 'api'],
    code: `interface ApiResponse<T> {
  data: T | null;
  error: string | null;
  loading: boolean;
}

interface ApiSuccess<T> {
  success: true;
  data: T;
}

interface ApiError {
  success: false;
  error: string;
}

type ApiResult<T> = ApiSuccess<T> | ApiError;

// Usage
async function fetchUser(id: string): Promise<ApiResult<User>> {
  try {
    const response = await fetch(\`/api/users/\${id}\`);
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    };
  }
}`,
  },

  // Node.js / Express
  {
    id: 'express-middleware',
    name: 'Express Middleware',
    description: 'Middleware Express avec error handling',
    language: 'javascript',
    category: 'nodejs',
    tags: ['express', 'middleware'],
    code: `// Auth middleware
const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
};

// Error handling middleware
const errorHandler = (err, req, res, next) => {
  console.error(err.stack);

  res.status(err.status || 500).json({
    error: err.message || 'Internal Server Error',
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
};

// Usage
app.use(authMiddleware);
app.use(errorHandler);`,
  },

  // Python
  {
    id: 'fastapi-endpoint',
    name: 'FastAPI Endpoint',
    description: 'Endpoint FastAPI avec validation',
    language: 'python',
    category: 'python',
    tags: ['fastapi', 'api', 'pydantic'],
    code: `from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

class User(BaseModel):
    name: str
    email: EmailStr
    age: int | None = None

@app.post("/users")
async def create_user(user: User):
    try:
        # Your logic here
        return {"message": "User created", "user": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # Your logic here
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user`,
  },

  // Utils
  {
    id: 'sleep-promise',
    name: 'Sleep Promise',
    description: 'Fonction sleep avec Promise',
    language: 'javascript',
    category: 'utils',
    tags: ['promise', 'async', 'utility'],
    code: `const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// Usage
await sleep(1000); // Wait 1 second
console.log('Waited!');

// Alternative avec abort
function sleep(ms, signal) {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(resolve, ms);
    signal?.addEventListener('abort', () => {
      clearTimeout(timeout);
      reject(new Error('Aborted'));
    });
  });
}`,
  },
  {
    id: 'format-currency',
    name: 'Format Currency',
    description: 'Formater montant en DA (Dinar Algérien)',
    language: 'javascript',
    category: 'utils',
    tags: ['format', 'currency', 'algeria'],
    code: `function formatCurrency(amount, currency = 'DZD') {
  return new Intl.NumberFormat('fr-DZ', {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 0,
  }).format(amount);
}

// Usage
formatCurrency(2500); // "2 500 DA"
formatCurrency(1000000); // "1 000 000 DA"

// Alternative simple
function formatDA(amount) {
  return amount.toLocaleString('fr-DZ') + ' DA';
}`,
  },
  {
    id: 'debounce-function',
    name: 'Debounce Function',
    description: 'Debounce pour limiter appels fonction',
    language: 'javascript',
    category: 'utils',
    tags: ['debounce', 'performance', 'utility'],
    code: `function debounce(func, delay) {
  let timeoutId;

  return function (...args) {
    clearTimeout(timeoutId);

    timeoutId = setTimeout(() => {
      func.apply(this, args);
    }, delay);
  };
}

// Usage
const handleSearch = debounce((query) => {
  console.log('Searching for:', query);
  // API call here
}, 500);

// TypeScript version
function debounce<T extends (...args: any[]) => any>(
  func: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: NodeJS.Timeout;

  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
}`,
  },
];
