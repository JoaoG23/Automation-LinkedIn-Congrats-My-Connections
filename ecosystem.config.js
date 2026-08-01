module.exports = {
  apps: [
    {
      name: "automation-linkedin-congrats-my-connections",
      script: "main.py",
      interpreter: "python",
      autorestart: false,
      watch: false,
      env: {
        ENVIRONMENT: "development",
        MY_ENV: "dev",
        PYTHONUNBUFFERED: "1",
        PYTHONIOENCODING: "UTF-8"
      },
      env_production: {
        ENVIRONMENT: "production",
        MY_ENV: "prod",
        PYTHONUNBUFFERED: "1",
        PYTHONIOENCODING: "UTF-8"
      }
    }
  ]
};
