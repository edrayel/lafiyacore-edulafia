from __future__ import annotations
"""Proprietor repository for data access operations."""


from sqlalchemy.ext.asyncio import AsyncSession


class ProprietorRepository:
    """Repository for proprietor dashboard data aggregation.

    This repository does not own any models. It aggregates data
    from other modules to build the proprietor dashboard.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
