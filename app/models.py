from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, Boolean

metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("login", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("email", String),
    Column("is_active", Boolean),
    Column("is_superuser", Boolean),
    Column("is_verified", Boolean)
)

salary_data = Table(
    "salary_data",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("current_salaru", Integer),
    Column("increase_date", TIMESTAMP),
    Column("user_id", Integer, ForeignKey("user.id"))
)