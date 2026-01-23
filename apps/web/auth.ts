import NextAuth from "next-auth"
import Credentials from "next-auth/providers/credentials"

// Ensure AUTH_SECRET is configured
if (!process.env.AUTH_SECRET) {
  throw new Error("AUTH_SECRET environment variable is required. Generate with: openssl rand -base64 32")
}

export const { handlers, auth, signIn, signOut } = NextAuth({
  secret: process.env.AUTH_SECRET,
  debug: process.env.NODE_ENV === "development",
  providers: [
    Credentials({
        name: "Credentials",
        credentials: {
            email: { label: "Email", type: "email" },
            password: { label: "Password", type: "password" },
        },
        authorize: async (credentials) => {
            // TODO: Implement real authentication against database
            // This is a placeholder - connect to your user database
            if (!credentials?.email || !credentials?.password) {
              return null
            }

            // Example: validate against database
            // const user = await prisma.user.findUnique({ where: { email: credentials.email } })
            // if (user && await bcrypt.compare(credentials.password, user.passwordHash)) {
            //   return { id: user.id, name: user.name, email: user.email }
            // }

            return null
        },
    }),
  ],
  pages: {
      signIn: '/login',
  }
})
