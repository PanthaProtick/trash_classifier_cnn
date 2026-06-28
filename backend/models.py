from sqlalchemy import (
    Column,
    String,
    Boolean,
    Numeric,
    DateTime,
    ForeignKey,
    Index,
    Enum,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

Base = declarative_base()


class TrashLabel(str, enum.Enum):
    """Enum for trash classification labels"""
    CARDBOARD = "cardboard"
    GLASS = "glass"
    METAL = "metal"
    PAPER = "paper"
    PLASTIC = "plastic"
    TRASH = "trash"


class User(Base):
    """User model for storing user information"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clerk_user_id = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # Relationships
    images = relationship("Image", back_populates="user", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, clerk_user_id={self.clerk_user_id})>"


class Model(Base):
    """Model metadata for ML models"""
    __tablename__ = "models"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version = Column(String, nullable=False, unique=True)
    model_path = Column(String, nullable=False)
    trained_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)

    # Relationships
    predictions = relationship("Prediction", back_populates="model")

    # Indexes
    __table_args__ = (
        Index("idx_models_active", "is_active"),
    )

    def __repr__(self):
        return f"<Model(id={self.id}, version={self.version}, is_active={self.is_active})>"


class Image(Base):
    """Image model for storing uploaded images"""
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    image_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="images")
    predictions = relationship("Prediction", back_populates="image", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="image", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index("idx_images_user", "user_id"),
    )

    def __repr__(self):
        return f"<Image(id={self.id}, user_id={self.user_id}, image_path={self.image_path})>"


class Prediction(Base):
    """Prediction model for storing model predictions"""
    __tablename__ = "predictions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_id = Column(UUID(as_uuid=True), ForeignKey("images.id", ondelete="CASCADE"), nullable=False)
    model_id = Column(UUID(as_uuid=True), ForeignKey("models.id", ondelete="RESTRICT"), nullable=False)
    predicted_label = Column(Enum(TrashLabel), nullable=False)
    confidence = Column(Numeric(precision=5, scale=4), nullable=False)
    predicted_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # Relationships
    image = relationship("Image", back_populates="predictions")
    model = relationship("Model", back_populates="predictions")

    # Indexes
    __table_args__ = (
        Index("idx_predictions_image", "image_id"),
        Index("idx_predictions_model", "model_id"),
        Index("idx_predictions_latest", "image_id", "predicted_at"),
    )

    def __repr__(self):
        return f"<Prediction(id={self.id}, image_id={self.image_id}, predicted_label={self.predicted_label}, confidence={self.confidence})>"


class Feedback(Base):
    """Feedback model for storing user corrections/feedback"""
    __tablename__ = "feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_id = Column(UUID(as_uuid=True), ForeignKey("images.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    corrected_label = Column(Enum(TrashLabel), nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # Relationships
    image = relationship("Image", back_populates="feedback")
    user = relationship("User", back_populates="feedback")

    # Indexes
    __table_args__ = (
        Index("idx_feedback_image", "image_id"),
        Index("idx_feedback_user", "user_id"),
        Index("idx_feedback_latest", "image_id", "created_at"),
    )

    def __repr__(self):
        return f"<Feedback(id={self.id}, image_id={self.image_id}, corrected_label={self.corrected_label})>"
