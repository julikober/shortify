from datetime import datetime
import secrets
import string
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from models.link import LinkModels
import schemas.link as link_schema


class LinkCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def get_link_by_id(self, id: str):
        stmt = select(LinkModels).where(LinkModels.id == id)
        result = await self.db_session.execute(stmt)
        link = result.scalars().first()
        return link

    async def get_links(self) -> List[LinkModels]:
        stmt = select(LinkModels)
        result = await self.db_session.execute(stmt)
        links = result.scalars().all()
        return links

    async def increment_access_count(self, id: str):
        link = await self.get_link_by_id(id)
        if link:
            link.access_count = int(link.access_count) + 1
            link.last_access_time = datetime.utcnow()
            await self.db_session.commit()
            return True
        return False

    async def update_last_access_time(self, id: str):
        link = await self.get_link_by_id(id)
        if link:
            link.last_access_time = datetime.utcnow()
            await self.db_session.commit()
            return True
        return False

    async def get_link_by_short_url(self, short_url: str):
        stmt = select(LinkModels).where(LinkModels.short_url == short_url)
        result = await self.db_session.execute(stmt)
        link = result.scalars().first()
        return link

    async def get_link_by_url(self, url: str):
        stmt = select(LinkModels).where(LinkModels.url == url)
        result = await self.db_session.execute(stmt)
        link = result.scalars().first()
        return link

    async def get_access_count(self, id: str):
        link = await self.get_link_by_id(id)
        if link:
            return link.access_count
        return None

    async def get_last_access_time(self, id: str):
        link = await self.get_link_by_id(id)
        if link:
            return link.last_access_time
        return None

    async def get_analytics(self, id: str):
        """Get analytics for a specific link"""
        link = await self.get_link_by_id(id)
        if link:
            return {
                "id": link.id,
                "url": link.url,
                "short_url": link.short_url,
                "access_count": link.access_count,
                "create_time": link.create_time,
                "last_access_time": link.last_access_time,
            }
        return None

    def _generate_short_id(self, length: int = 6) -> str:
        """Generate a random short ID for the URL"""
        chars = string.ascii_letters + string.digits
        return "".join(secrets.choice(chars) for _ in range(length))

    async def create_link(
        self, url: str, custom_id: Optional[str] = None
    ) -> LinkModels:
        """Create a new short link"""
        # Check if the URL already exists
        existing_link = await self.get_link_by_url(url)
        if existing_link:
            return existing_link

        # Generate a unique ID if none provided
        if not custom_id:
            while True:
                link_id = self._generate_short_id()
                existing = await self.get_link_by_id(link_id)
                if not existing:
                    break
        else:
            link_id = custom_id
            existing = await self.get_link_by_id(link_id)
            if existing:
                return None  # Custom ID already in use

        # Create short URL
        short_url = f"/s/{link_id}"

        # Create link in database
        db_link = LinkModels(
            id=link_id,
            url=url,
            short_url=short_url,
        )
        self.db_session.add(db_link)
        await self.db_session.commit()
        return db_link

    async def update_link(self, id: str, url: str) -> bool:
        """Update a link's URL"""
        link = await self.get_link_by_id(id)
        if link:
            link.url = url
            await self.db_session.commit()
            return True
        return False

    async def delete_link(self, id: str) -> bool:
        """Delete a link"""
        link = await self.get_link_by_id(id)
        if link:
            await self.db_session.delete(link)
            await self.db_session.commit()
            return True
        return False
