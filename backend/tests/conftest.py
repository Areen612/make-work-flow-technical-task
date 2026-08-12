import os


# The endpoint tests replace the database dependency and do not need PostgreSQL,
# but application configuration is validated when the modules are imported.
os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("FRONTEND_ORIGIN", "http://localhost:5173")
