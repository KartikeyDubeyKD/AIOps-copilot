const config = {
  // API Configuration
  API_BASE: import.meta.env.VITE_API_URL || " https://aiops-copilot.onrender.com",
  
  // Environment
  ENV: import.meta.env.VITE_ENV || "",
  
  // Feature flags (optional)
  FEATURES: {
    DOCKER_DEPLOYMENT: true,
    LOG_ANALYSIS: true,
    AI_RECOMMENDATIONS: true
  }
};

export default config;