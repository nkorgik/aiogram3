from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    MetaData,
    Numeric,
    String,
    Table,
    Text,
    func,
)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("telegram_id", BigInteger, nullable=False, unique=True, index=True),
    Column("username", String(255)),
    Column("full_name", String(255)),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
)

expenses = Table(
    "expenses",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("user_id", BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
    Column("amount", Numeric(12, 2), nullable=False),
    Column("category", String(64), nullable=False, index=True),
    Column("note", Text, default=""),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
)
