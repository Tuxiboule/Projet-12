import enum
from datetime import date, datetime
from sqlalchemy import String, func, ForeignKey, UniqueConstraint
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from settings import Base


class Department(enum.Enum):
    """
    Enum representing different departments of staff.
    """
    COMMERCIAL = 1
    SUPPORT = 2
    MANAGEMENT = 3


class Staff(Base):
    """
    Represents a staff member.
    """
    __tablename__ = "staff"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(300))
    password: Mapped[str] = mapped_column(String(500))
    department: Mapped[Department]
    clients: Mapped[List["Client"]] = relationship(back_populates="commercial_contact", lazy="selectin")
    contracts: Mapped[List["Contract"]] = relationship(back_populates="commercial_contact", lazy="selectin")
    events: Mapped[List["Event"]] = relationship(back_populates="support_contact", lazy="selectin")

    def __repr__(self) -> str:
        return f"Staff(id={self.id!r}, name={self.name!r}, first_name={self.first_name!r})"


class Client(Base):
    """
    Represents a client.
    """
    __tablename__ = "client"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    fullname: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(300), nullable=True)
    phone: Mapped[int]
    name_company: Mapped[str] = mapped_column(String(300))
    date_creation: Mapped[date] = mapped_column(insert_default=func.now())
    date_update: Mapped[date] = mapped_column(insert_default=func.now())
    commercial_contact_id = mapped_column(ForeignKey("staff.id"))
    commercial_contact = relationship("Staff", back_populates="clients")
    contracts: Mapped[List["Contract"]] = relationship(back_populates="client")
    events: Mapped[List["Event"]] = relationship(back_populates="client")

    def __repr__(self) -> str:
        return (
            f"Client(id:{self.id}, fullname : {self.fullname}, email : {self.email}, phone : {self.phone},"
            f"name_company : {self.name_company!r}, date_creation : {self.date_creation!r},"
            f"date_update : {self.date_update!r},"
            f"commercial_contact_id : {self.commercial_contact.name!r})"
        )


class Event(Base):
    """
    Represents an event.
    """
    __tablename__ = "event"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(500), unique=True)
    contract_id = mapped_column(ForeignKey("contract.id"))
    contract = relationship("Contract", back_populates="event")
    __table_args__ = (UniqueConstraint("contract_id"),)
    client_id = mapped_column(ForeignKey("client.id"))
    client = relationship("Client", back_populates="events")
    event_date_start: Mapped[datetime]
    event_date_end: Mapped[datetime]
    support_contact_id = mapped_column(ForeignKey("staff.id"), nullable=True, default=None)
    support_contact = relationship("Staff", back_populates="events")
    location: Mapped[str] = mapped_column(String(250))
    attendees: Mapped[int]
    notes: Mapped[str] = mapped_column(String(1000))

    def __repr__(self) -> str:
        return f"Event(id={self.id!r}, name={self.name!r}, location={self.location!r})"


class Contract(Base):
    """
    Represents a contract.
    """
    __tablename__ = "contract"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id = mapped_column(ForeignKey("client.id"))
    client = relationship("Client", back_populates="contracts")
    commercial_contact_id = mapped_column(ForeignKey("staff.id"))
    commercial_contact = relationship("Staff", back_populates="contracts")
    event: Mapped["Event"] = relationship(back_populates="contract")
    total_amount: Mapped[int]
    balance_due: Mapped[int]
    date_creation: Mapped[date] = mapped_column(insert_default=func.now())
    status: Mapped[bool]

    def __repr__(self) -> str:
        return f"Contract(id={self.id!r}, client.fullname={self.client.fullname!r}), event={self.event!r})"
