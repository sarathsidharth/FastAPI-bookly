from redis.asyncio import Redis
from src.config import settings

JTI_EXPIRY = 3600  # seconds

token_blocklist = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True,
)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name=jti,
        value="",
        ex=JTI_EXPIRY,
    )

async def token_in_blocklist(jti: str) -> bool:
    return await token_blocklist.exists(jti) == 1
