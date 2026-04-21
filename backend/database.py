from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

Base = declarative_base()

class Participant(Base):
    """参与者表"""
    __tablename__ = "participants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    student_id = Column(String(50), unique=True, nullable=False)
    gender = Column(String(10), nullable=True)
    
    # 问卷答案 (JSON格式存储)
    quiz_answers = Column(Text, nullable=False)  # JSON字符串
    
    # 人格类型 (如: ENFJ, ISTP)
    personality_type = Column(String(4), nullable=False)
    
    # 各维度得分 (JSON格式)
    dimension_scores = Column(Text, nullable=False)  # {"E_I": 0.7, "S_N": -0.3, ...}
    
    # 兴趣标签
    interests = Column(Text, nullable=True)  # JSON数组 ["游戏", "音乐", "运动"]
    
    # 匹配状态
    is_matched = Column(Integer, default=0)  # 0=未匹配, 1=已匹配
    matched_with = Column(Integer, nullable=True)  # 匹配对象ID
    match_score = Column(Float, nullable=True)  # 匹配分数
    
    created_at = Column(DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "student_id": self.student_id,
            "gender": self.gender,
            "quiz_answers": json.loads(self.quiz_answers),
            "personality_type": self.personality_type,
            "dimension_scores": json.loads(self.dimension_scores),
            "interests": json.loads(self.interests) if self.interests else [],
            "is_matched": bool(self.is_matched),
            "matched_with": self.matched_with,
            "match_score": self.match_score,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class MatchResult(Base):
    """匹配结果表"""
    __tablename__ = "match_results"
    
    id = Column(Integer, primary_key=True, index=True)
    participant_a_id = Column(Integer, nullable=False)
    participant_b_id = Column(Integer, nullable=False)
    match_score = Column(Float, nullable=False)
    match_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

# 数据库连接
engine = create_engine("sqlite:///./matchmaking.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """初始化数据库"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
