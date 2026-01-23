/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // PWA configuration will be added later
  images: {
    domains: ['flagcdn.com'], // For country flags
  },
};

module.exports = nextConfig;
