import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  // If you're having CORS issues, you might need this
  async headers() {
    return [
      {
        source: '/:path',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '' }
        ],
      },
    ]
  }
};

export default nextConfig;