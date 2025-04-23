from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import RedirectResponse
from typing import List, Optional

from auth.action import get_current_user
from crud.link import LinkCRUD
from crud.dependencies import get_link_crud
import schemas.link as link_schema
import schemas.user as user_schema

router = APIRouter(tags=["links"])


@router.get("/links", response_model=List[link_schema.Base])
async def get_links(db: LinkCRUD = Depends(get_link_crud)):
    """Get all links"""
    return await db.get_links()


@router.get("/links/{link_id}", response_model=link_schema.Base)
async def get_link(link_id: str, db: LinkCRUD = Depends(get_link_crud)):
    """Get a specific link by ID"""
    link = await db.get_link_by_id(link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@router.post("/links", response_model=link_schema.Base, status_code=status.HTTP_201_CREATED)
async def create_link(
    url: str, 
    custom_id: Optional[str] = None,
    current_user: user_schema.Base = Depends(get_current_user),
    db: LinkCRUD = Depends(get_link_crud)
):
    """Create a new short link"""
    link = await db.create_link(url, custom_id)
    if not link:
        raise HTTPException(status_code=400, detail="Failed to create link. Custom ID may already be in use.")
    return link


@router.put("/links/{link_id}", response_model=link_schema.Base)
async def update_link(
    link_id: str, 
    url: str,
    current_user: user_schema.Base = Depends(get_current_user),
    db: LinkCRUD = Depends(get_link_crud)
):
    """Update a link's URL"""
    success = await db.update_link(link_id, url)
    if not success:
        raise HTTPException(status_code=404, detail="Link not found")
    return await db.get_link_by_id(link_id)


@router.delete("/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_link(
    link_id: str,
    current_user: user_schema.Base = Depends(get_current_user),
    db: LinkCRUD = Depends(get_link_crud)
):
    """Delete a link"""
    success = await db.delete_link(link_id)
    if not success:
        raise HTTPException(status_code=404, detail="Link not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/s/{short_id}")
async def redirect_to_url(short_id: str, request: Request, db: LinkCRUD = Depends(get_link_crud)):
    """Redirect to the original URL and track the access"""
    link = await db.get_link_by_id(short_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    # Increment access count
    await db.increment_access_count(short_id)
    
    # Redirect to the original URL
    return RedirectResponse(link.url)


@router.get("/links/{link_id}/analytics")
async def get_link_analytics(
    link_id: str,
    current_user: user_schema.Base = Depends(get_current_user),
    db: LinkCRUD = Depends(get_link_crud)
):
    """Get analytics for a specific link"""
    analytics = await db.get_analytics(link_id)
    if not analytics:
        raise HTTPException(status_code=404, detail="Link not found")
    return analytics