from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.core.exceptions import NotFoundException
from app.models.document import Document, DocumentType
from app.models.faq import FAQ, FAQCategory


class DocumentService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, document_data: Dict[str, Any]) -> Document:
        document = Document(**document_data)
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def get_by_id(self, document_id: str) -> Document:
        document = self.db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise NotFoundException("Document", document_id)
        return document

    def get_all(
        self,
        page: int = 1,
        size: int = 20,
        document_type: Optional[str] = None,
        is_processed: Optional[bool] = None,
    ) -> Dict[str, Any]:
        query = self.db.query(Document)

        if document_type:
            query = query.filter(Document.document_type == document_type)

        if is_processed is not None:
            query = query.filter(Document.is_processed == is_processed)

        total = query.count()
        documents = query.order_by(Document.created_at.desc()).offset((page - 1) * size).limit(size).all()

        return {
            "documents": documents,
            "total": total,
            "page": page,
            "size": size,
        }

    def update(self, document_id: str, update_data: Dict[str, Any]) -> Document:
        document = self.get_by_id(document_id)
        for field, value in update_data.items():
            setattr(document, field, value)
        self.db.commit()
        self.db.refresh(document)
        return document

    def delete(self, document_id: str) -> bool:
        document = self.get_by_id(document_id)
        self.db.delete(document)
        self.db.commit()
        return True


class FAQService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, faq_data: Dict[str, Any]) -> FAQ:
        faq = FAQ(**faq_data)
        self.db.add(faq)
        self.db.commit()
        self.db.refresh(faq)
        return faq

    def get_by_id(self, faq_id: str) -> FAQ:
        faq = self.db.query(FAQ).filter(FAQ.id == faq_id).first()
        if not faq:
            raise NotFoundException("FAQ", faq_id)
        return faq

    def get_all(
        self,
        page: int = 1,
        size: int = 20,
        category: Optional[str] = None,
        is_published: Optional[bool] = None,
        is_featured: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        query = self.db.query(FAQ)

        if category:
            query = query.filter(FAQ.category == category)

        if is_published is not None:
            query = query.filter(FAQ.is_published == is_published)

        if is_featured is not None:
            query = query.filter(FAQ.is_featured == is_featured)

        if search:
            query = query.filter(
                or_(
                    FAQ.question.ilike(f"%{search}%"),
                    FAQ.answer.ilike(f"%{search}%"),
                )
            )

        total = query.count()
        faqs = query.order_by(FAQ.sort_order, FAQ.created_at.desc()).offset((page - 1) * size).limit(size).all()

        return {
            "faqs": faqs,
            "total": total,
            "page": page,
            "size": size,
        }

    def update(self, faq_id: str, update_data: Dict[str, Any]) -> FAQ:
        faq = self.get_by_id(faq_id)
        for field, value in update_data.items():
            setattr(faq, field, value)
        self.db.commit()
        self.db.refresh(faq)
        return faq

    def delete(self, faq_id: str) -> bool:
        faq = self.get_by_id(faq_id)
        self.db.delete(faq)
        self.db.commit()
        return True

    def get_categories(self) -> List[str]:
        return [c.value for c in FAQCategory]