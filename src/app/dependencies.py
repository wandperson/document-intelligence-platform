# Standard
from typing import Annotated

# Backend
from fastapi import Request, Depends

# Custom
from app.database import InMemoryRepo


def get_repository(request: Request) -> InMemoryRepo:
    return request.app.state.database


RepositoryDep = Annotated[InMemoryRepo, Depends(get_repository)]
