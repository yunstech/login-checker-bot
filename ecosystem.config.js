module.exports = {
  apps: [
    {
      name: "fastapi-app",
      script: "uvicorn",
      args: "main:app --host 0.0.0.0 --port 6666",
      interpreter: "bash",
      exec_mode: "fork",
      autorestart: true,
      watch: false,
      max_memory_restart: "500M",
      env: {
        PYTHONUNBUFFERED: "1",
        ENVIRONMENT: "production",
      },
    },

    {
      name: "redis-server",
      script: "redis-server",
      args: "--port 6379",
      autorestart: true,
      watch: false,
      exec_mode: "fork",
      max_memory_restart: "300M",
    },

    {
      name: "rq-worker",
      script: "rq",
      args: "worker default",
      interpreter: "bash",
      exec_mode: "fork",
      autorestart: true,
      watch: false,
      max_memory_restart: "500M",
      env: {
        PYTHONUNBUFFERED: "1",
      },
    },
  ],
};
