from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text,Float
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import JSONB
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "app_schema"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_tickets: Mapped[list["Ticket"]] = relationship(
        "Ticket",
        back_populates="creator",
        foreign_keys="Ticket.created_by",
    )
    assigned_tickets: Mapped[list["Ticket"]] = relationship(
        "Ticket",
        back_populates="assignee",
        foreign_keys="Ticket.assigned_to",
    )
    uploaded_docs:Mapped[list["KnowledgeDoc"]]=relationship(
        "KnowledgeDoc",
        back_populates="uploader"
        
    )


class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = {"schema": "app_schema"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open")
    created_by: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("app_schema.users.id"),
        nullable=False,
    )
    assigned_to: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("app_schema.users.id"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    creator: Mapped["User"] = relationship(
        "User",
        back_populates="created_tickets",
        foreign_keys=[created_by],
    )
    assignee: Mapped["User | None"] = relationship(
        "User",
        back_populates="assigned_tickets",
        foreign_keys=[assigned_to],
    )
    predictions:Mapped["TicketPrediction"]=relationship(
        "TicketPrediction",
        back_populates="ticket",
        cascade="all, delete-orphan",
        uselist=False
    )
    
class TicketPrediction(Base):
    __tablename__="ticket_predictions"
    __table_args__={"schema":"app_schema"}
    
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    ticket_id:Mapped[int]=mapped_column(
        Integer,
        ForeignKey("app_schema.tickets.id"),
        nullable=False,
        unique=True,
    )
    ticket:Mapped["Ticket"]=relationship(
        "Ticket",back_populates="predictions"
    )
    priority:Mapped[str]=mapped_column(String(20),nullable=False,default="low")
    category:Mapped[str]=mapped_column(String(20),nullable=False)
    confidence:Mapped[float]=mapped_column(Float,nullable=False)
    model_name:Mapped[str]=mapped_column(String(20),nullable=False,default="Mistral")
    created_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        default = lambda:datetime.now(timezone.utc),
        nullable = False,)
    
class KnowledgeDoc(Base):
    __tablename__="knowledge_docs"
    __table_args__={"schema":"app_schema"}
    
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    title:Mapped[str]=mapped_column(String(255),nullable = False)
    source:Mapped[str]=mapped_column(String(255),nullable=False)
    content_type:Mapped[str]=mapped_column(String(6),nullable=False,default="txt")
    uploaded_by:Mapped[int]=mapped_column(Integer,ForeignKey("app_schema.users.id"),nullable=False)
    uploader:Mapped["User"]=relationship("User",back_populates="uploaded_docs")
    chunks: Mapped[list["DocChunk"]] = relationship(
        "DocChunk",
        back_populates="doc",
        cascade="all, delete-orphan",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
class DocChunk(Base):
    __tablename__="doc_chunks"
    __table_args__={"schema":"app_schema"}
    
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    doc_id:Mapped[int]=mapped_column(Integer,ForeignKey("app_schema.knowledge_docs.id"),index=True)
    chunk_index:Mapped[int]=mapped_column(Integer,nullable=False)
    text:Mapped[str]=mapped_column(Text,nullable=False)
    token_count:Mapped[int]=mapped_column(Integer,nullable=False)
    embedding:Mapped[list[float]]=mapped_column(Vector(768),nullable=False)
    doc: Mapped["KnowledgeDoc"] = relationship("KnowledgeDoc", back_populates="chunks")
    created_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        default = lambda : datetime.now(timezone.utc),
        nullable=False,
    )
class Log(Base):
    __tablename__="logs"
    __table_args__={"schema":"app_schema"}
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id:Mapped[int | None]=mapped_column(ForeignKey("app_schema.users.id"),nullable=True)
    ticket_id:Mapped[int]=mapped_column(ForeignKey("app_schema.tickets.id"),index=True,nullable=False)
    action:Mapped[str]=mapped_column(String(20),nullable=False,default="search")
    prompt:Mapped[str]=mapped_column(Text,nullable=False)
    response:Mapped[str]=mapped_column(Text,nullable=False)
    citations:Mapped[list[dict]]=mapped_column(JSONB,nullable=False,default=list)
    model_name:Mapped[str]=mapped_column(String,default="Mistral")
    input_tokens:Mapped[int]=mapped_column(Integer,nullable=True)
    output_tokens:Mapped[int]=mapped_column(Integer,nullable=True)
    created_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc))