"""
Schema do banco de dados para o CanalAutomatizado
Inclui tabelas para templates, análises, cortes e histórico de downloads
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, JSON, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class VideoDownload(Base):
    """Registro de downloads de vídeos"""
    __tablename__ = "video_downloads"
    
    id = Column(String, primary_key=True)
    video_url = Column(String, nullable=False)
    video_title = Column(String, nullable=False)
    video_channel = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)  # em bytes
    quality = Column(String)  # ex: "720p", "1080p", "best"
    duration = Column(Integer)  # em segundos
    downloaded_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="completed")  # completed, failed, pending


class VideoTemplate(Base):
    """Templates para automação de criação de vídeos"""
    __tablename__ = "video_templates"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)  # ex: "intro", "outro", "transição"
    config = Column(JSON)  # Configurações do template
    thumbnail = Column(String)  # URL da thumbnail
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class VideoClip(Base):
    """Cortes/clips de vídeos"""
    __tablename__ = "video_clips"
    
    id = Column(String, primary_key=True)
    video_download_id = Column(String, ForeignKey("video_downloads.id"))
    title = Column(String, nullable=False)
    start_time = Column(Integer)  # em segundos
    end_time = Column(Integer)  # em segundos
    duration = Column(Integer)  # em segundos
    file_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_exported = Column(Boolean, default=False)


class VideoAnalytics(Base):
    """Análises e métricas de desempenho dos vídeos"""
    __tablename__ = "video_analytics"
    
    id = Column(String, primary_key=True)
    video_download_id = Column(String, ForeignKey("video_downloads.id"))
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    watch_time = Column(Integer, default=0)  # em segundos
    engagement_rate = Column(Float, default=0.0)  # em percentual
    click_through_rate = Column(Float, default=0.0)  # em percentual
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class VideoProject(Base):
    """Projetos de vídeos agrupados"""
    __tablename__ = "video_projects"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="active")  # active, archived, completed
    template_id = Column(String, ForeignKey("video_templates.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AutomationTask(Base):
    """Tarefas de automação de criação de vídeos"""
    __tablename__ = "automation_tasks"
    
    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("video_projects.id"))
    task_type = Column(String)  # ex: "create_intro", "add_music", "export"
    status = Column(String, default="pending")  # pending, running, completed, failed
    config = Column(JSON)  # Configurações específicas da tarefa
    result = Column(JSON)  # Resultado da execução
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    error_message = Column(Text)
