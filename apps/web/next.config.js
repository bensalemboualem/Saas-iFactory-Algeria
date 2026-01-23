/** @type {import('next').NextConfig} */
const nextConfig = {
    output: 'standalone',
    transpilePackages: ['@iafactory/tools-registry']
};

module.exports = nextConfig;
