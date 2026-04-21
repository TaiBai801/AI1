from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
import json

from database import init_db, get_db, Participant, MatchResult
from matching import (
    calculate_personality, get_personality_description, 
    calculate_similarity, optimal_matching, 
    get_quiz_questions, get_all_interests
)

# 初始化数据库
init_db()

app = FastAPI(title="AI联谊匹配系统", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ 数据模型 ============

class QuizAnswer(BaseModel):
    question_id: int
    answer: str  # "A" 或 "B"

class ParticipantCreate(BaseModel):
    name: str
    student_id: str
    gender: Optional[str] = None
    quiz_answers: List[QuizAnswer]
    interests: List[str] = []

class MatchRequest(BaseModel):
    mode: str = "similar"  # "similar" 或 "complementary"

# ============ API路由 ============

@app.get("/")
def root():
    return {"message": "AI联谊匹配系统 API", "version": "1.0.0"}

@app.get("/api/quiz/questions")
def get_questions():
    """获取问卷题目"""
    return {"questions": get_quiz_questions()}

@app.get("/api/interests")
def get_interests():
    """获取所有可选兴趣标签"""
    return {"interests": get_all_interests()}

@app.post("/api/participants")
def create_participant(data: ParticipantCreate, db: Session = Depends(get_db)):
    """创建参与者并计算人格类型"""
    # 检查学号是否已存在
    existing = db.query(Participant).filter(Participant.student_id == data.student_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="该学号已报名")
    
    # 转换问卷答案格式
    answers_dict = {a.question_id: a.answer for a in data.quiz_answers}
    
    # 计算人格类型
    personality_type, dimension_scores = calculate_personality(answers_dict)
    
    # 创建参与者记录
    participant = Participant(
        name=data.name,
        student_id=data.student_id,
        gender=data.gender,
        quiz_answers=json.dumps(answers_dict),
        personality_type=personality_type,
        dimension_scores=json.dumps(dimension_scores),
        interests=json.dumps(data.interests)
    )
    
    db.add(participant)
    db.commit()
    db.refresh(participant)
    
    # 获取人格描述
    description = get_personality_description(personality_type)
    
    return {
        "id": participant.id,
        "name": participant.name,
        "personality_type": personality_type,
        "description": description,
        "dimension_scores": dimension_scores
    }

@app.get("/api/participants")
def list_participants(db: Session = Depends(get_db)):
    """获取所有参与者列表"""
    participants = db.query(Participant).all()
    return {"participants": [p.to_dict() for p in participants]}

@app.get("/api/participants/{participant_id}")
def get_participant(participant_id: int, db: Session = Depends(get_db)):
    """获取单个参与者详情"""
    participant = db.query(Participant).filter(Participant.id == participant_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="参与者不存在")
    
    description = get_personality_description(participant.personality_type)
    result = participant.to_dict()
    result["description"] = description
    return result

@app.delete("/api/participants/{participant_id}")
def delete_participant(participant_id: int, db: Session = Depends(get_db)):
    """删除参与者"""
    participant = db.query(Participant).filter(Participant.id == participant_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="参与者不存在")
    
    db.delete(participant)
    db.commit()
    return {"message": "删除成功"}

@app.post("/api/matching/run")
def run_matching(request: MatchRequest, db: Session = Depends(get_db)):
    """执行匹配算法"""
    # 获取所有未匹配的参与者
    participants = db.query(Participant).filter(Participant.is_matched == 0).all()
    
    if len(participants) < 2:
        raise HTTPException(status_code=400, detail="参与者数量不足，至少需要2人")
    
    # 执行最优匹配
    matches, unmatched = optimal_matching(participants, mode=request.mode)
    
    # 保存匹配结果到数据库
    for person_a, person_b, score, reason in matches:
        # 更新参与者匹配状态
        person_a.is_matched = 1
        person_a.matched_with = person_b.id
        person_a.match_score = score
        
        person_b.is_matched = 1
        person_b.matched_with = person_a.id
        person_b.match_score = score
        
        # 创建匹配记录
        match_record = MatchResult(
            participant_a_id=person_a.id,
            participant_b_id=person_b.id,
            match_score=score,
            match_reason=reason
        )
        db.add(match_record)
    
    db.commit()
    
    # 格式化返回结果
    results = []
    for person_a, person_b, score, reason in matches:
        results.append({
            "person_a": person_a.to_dict(),
            "person_b": person_b.to_dict(),
            "match_score": score,
            "match_reason": reason
        })
    
    return {
        "matches": results,
        "unmatched": [p.to_dict() for p in unmatched],
        "total_matched": len(matches) * 2,
        "total_unmatched": len(unmatched)
    }

@app.get("/api/matching/results")
def get_matching_results(db: Session = Depends(get_db)):
    """获取所有匹配结果"""
    # 获取已匹配的参与者
    matched = db.query(Participant).filter(Participant.is_matched == 1).all()
    
    # 按配对关系组织
    pairs = {}
    for p in matched:
        if p.matched_with:
            pair_key = tuple(sorted([p.id, p.matched_with]))
            if pair_key not in pairs:
                pairs[pair_key] = {"participants": [], "score": p.match_score}
            pairs[pair_key]["participants"].append(p.to_dict())
    
    # 格式化结果
    results = []
    for pair_key, data in pairs.items():
        if len(data["participants"]) == 2:
            results.append({
                "person_a": data["participants"][0],
                "person_b": data["participants"][1],
                "match_score": data["score"]
            })
    
    # 按匹配分数排序
    results.sort(key=lambda x: x["match_score"], reverse=True)
    
    return {"results": results}

@app.post("/api/matching/reset")
def reset_matching(db: Session = Depends(get_db)):
    """重置所有匹配结果"""
    # 清除所有匹配状态
    db.query(Participant).update({
        "is_matched": 0,
        "matched_with": None,
        "match_score": None
    })
    
    # 删除匹配记录
    db.query(MatchResult).delete()
    
    db.commit()
    return {"message": "匹配结果已重置"}

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """获取统计数据"""
    total = db.query(Participant).count()
    matched = db.query(Participant).filter(Participant.is_matched == 1).count()
    unmatched = total - matched
    
    # 人格类型分布
    personality_dist = {}
    for p in db.query(Participant).all():
        pt = p.personality_type
        personality_dist[pt] = personality_dist.get(pt, 0) + 1
    
    return {
        "total_participants": total,
        "matched": matched,
        "unmatched": unmatched,
        "match_rate": round(matched / total * 100, 2) if total > 0 else 0,
        "personality_distribution": personality_dist
    }

# 启动服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
