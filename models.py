from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Item(Base):
    __tablename__ = 'itens'
    id = Column(Integer, primary_key=True)
    descricao = Column(String, nullable=False)
    lance_inicial = Column(Float, nullable=False)
    tempo_leilao = Column(DateTime, default=datetime.utcnow() + timedelta(hours=1))
    lances = relationship("Lance", back_populates="item")

class Comprador(Base):
    __tablename__ = 'compradores'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)

class Lance(Base):
    __tablename__ = 'lances'
    id = Column(Integer, primary_key=True)
    valor = Column(Float, nullable=False)
    item_id = Column(Integer, ForeignKey('itens.id'), nullable=False)
    comprador_id = Column(Integer, ForeignKey('compradores.id'), nullable=False)
    item = relationship("Item", back_populates="lances")
    comprador = relationship("Comprador")
