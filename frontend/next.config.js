/** @type {import('next').NextConfig} */
const nextConfig = {
    output: 'standalone',
    async rewrites() {
        return [
            {
                source: '/api/:path*',
                destination: `${process.env.NEXT_API_URL}/:path*`,
            },
        ];
    }
};

module.exports = nextConfig;
