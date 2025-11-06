module.exports = {
  apps: [
    {
      name: "fastapi-app",
      script: "./venv/bin/python",
      args: "-m uvicorn main:app --host 0.0.0.0 --port 8686",
      cwd: "/home/yunus/databreach/login-checker-bot",
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
      name: "rq-worker",
      script: "./venv/bin/rq",
      args: "worker",
      cwd: "/home/yunus/databreach/login-checker-bot",
      exec_mode: "fork",
      interpreter: "python",
      autorestart: true,
      watch: false,
      max_memory_restart: "500M",
      env: {
        PYTHONUNBUFFERED: "1",
      },
    },
  ],
};