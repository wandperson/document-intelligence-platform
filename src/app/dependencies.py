# Standard
from typing import Annotated, AsyncGenerator

# Backend
from fastapi import Request, Depends

# ORM
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


# ============================================================================
# Database dependencies
# ============================================================================
def get_session_maker(request: Request) -> async_sessionmaker[AsyncSession]:
    """
    Retrieve the async session maker stored in the FastAPI application state.
    """
    return request.app.state.session_maker


async def get_session(
    session_maker: async_sessionmaker[AsyncSession] = Depends(get_session_maker),
) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and yield an asynchronous database session.

    Args:
        session_maker: Factory used to create AsyncSession instances.

    Yields:
        AsyncSession: Active database session.
    """
    async with session_maker() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
