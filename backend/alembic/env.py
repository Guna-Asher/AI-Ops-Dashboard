from app.db.base import Base
from app.db.models import incident  # ensures the model is loaded
from app.core.config import settings

# inside the run_migrations_offline function (or after imports), set the URL:
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# change target_metadata = None to:
target_metadata = Base.metadata