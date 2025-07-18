/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable experimental features for better performance
  experimental: {
    optimizePackageImports: ['lucide-react'],
  },
  
  // Configure webpack for better PDF handling
  webpack: (config) => {
    // Handle PDF files
    config.module.rules.push({
      test: /\.pdf$/,
      type: 'asset/resource',
    });
    
    return config;
  },
  
  // Security headers
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
        ],
      },
    ];
  },
  
  // Image optimization
  images: {
    formats: ['image/webp', 'image/avif'],
  },
  
  // Enable static exports if needed
  // output: 'export',
  // trailingSlash: true,
};

module.exports = nextConfig;