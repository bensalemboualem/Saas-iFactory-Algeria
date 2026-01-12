"""
Utilitaires de pagination pour l'API
"""
from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, Field
from math import ceil

T = TypeVar('T')


class PaginationParams(BaseModel):
    """Paramètres de pagination"""
    page: int = Field(default=1, ge=1, description="Numéro de page (commence à 1)")
    page_size: int = Field(default=20, ge=1, le=100, description="Taille de page (max 100)")

    @property
    def offset(self) -> int:
        """Calcule l'offset pour la DB"""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Alias pour page_size"""
        return self.page_size


class PageInfo(BaseModel):
    """Informations de pagination"""
    current_page: int
    page_size: int
    total_items: int
    total_pages: int
    has_previous: bool
    has_next: bool

    @classmethod
    def create(cls, page: int, page_size: int, total_items: int) -> "PageInfo":
        """Crée PageInfo depuis les paramètres"""
        total_pages = ceil(total_items / page_size) if page_size > 0 else 0
        return cls(
            current_page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
            has_previous=page > 1,
            has_next=page < total_pages
        )


class PaginatedResponse(BaseModel, Generic[T]):
    """Réponse paginée générique"""
    items: List[T]
    pagination: PageInfo

    @classmethod
    def create(
        cls,
        items: List[T],
        total_items: int,
        params: PaginationParams
    ) -> "PaginatedResponse[T]":
        """Crée une réponse paginée"""
        page_info = PageInfo.create(
            page=params.page,
            page_size=params.page_size,
            total_items=total_items
        )
        return cls(items=items, pagination=page_info)


class CursorPaginationParams(BaseModel):
    """Paramètres pour cursor-based pagination"""
    cursor: Optional[str] = Field(default=None, description="Cursor pour la page suivante")
    limit: int = Field(default=20, ge=1, le=100, description="Nombre d'items à retourner")


class CursorPageInfo(BaseModel):
    """Informations pour cursor-based pagination"""
    next_cursor: Optional[str] = None
    has_next: bool = False
    count: int = 0


class CursorPaginatedResponse(BaseModel, Generic[T]):
    """Réponse paginée avec curseur"""
    items: List[T]
    pagination: CursorPageInfo

    @classmethod
    def create(
        cls,
        items: List[T],
        next_cursor: Optional[str],
        has_next: bool
    ) -> "CursorPaginatedResponse[T]":
        """Crée une réponse paginée avec curseur"""
        return cls(
            items=items,
            pagination=CursorPageInfo(
                next_cursor=next_cursor,
                has_next=has_next,
                count=len(items)
            )
        )


def paginate_list(
    items: List[T],
    params: PaginationParams
) -> PaginatedResponse[T]:
    """
    Pagine une liste en mémoire

    Args:
        items: Liste complète des items
        params: Paramètres de pagination

    Returns:
        Réponse paginée
    """
    total = len(items)
    start = params.offset
    end = start + params.page_size

    paginated_items = items[start:end]

    return PaginatedResponse.create(
        items=paginated_items,
        total_items=total,
        params=params
    )
