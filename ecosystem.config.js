module.exports = {
  apps : [{
    name   : "automation-linkedin-congrats-my-connections",
    script : "__init__.py",
    interpreter: "python",
    autorestart: false, // Não reinicia após erro
    env_production: {
      ENVIRONMENT: "production",
      MY_ENV: "prod",
    },
  }]
}
