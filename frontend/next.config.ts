import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  images: {
    domains: ["localhost", "agentops.ai"],
  },
};

export default nextConfig;
