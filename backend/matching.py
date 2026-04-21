import json
import numpy as np
from typing import List, Dict, Tuple
import networkx as nx

# ============ 问卷配置 ============

QUIZ_QUESTIONS = [
    # E/I 维度 (能量来源)
    {"id": 1, "dimension": "E_I", "text": "在社交场合中，你通常：", "optionA": {"text": "感到兴奋，喜欢成为焦点", "score": 1}, "optionB": {"text": "感到疲惫，更喜欢安静观察", "score": -1}},
    {"id": 2, "dimension": "E_I", "text": "周末你更倾向于：", "optionA": {"text": "和朋友聚会、参加活动", "score": 1}, "optionB": {"text": "独自在家看书或休息", "score": -1}},
    {"id": 3, "dimension": "E_I", "text": "认识新朋友时，你：", "optionA": {"text": "主动打招呼，很快熟络", "score": 1}, "optionB": {"text": "等待别人先开口，慢慢熟悉", "score": -1}},
    {"id": 4, "dimension": "E_I", "text": "你的能量来源主要是：", "optionA": {"text": "外部世界的人和活动", "score": 1}, "optionB": {"text": "内心的思考和独处", "score": -1}},
    {"id": 5, "dimension": "E_I", "text": "在团队讨论中，你：", "optionA": {"text": "积极发言，边说边想", "score": 1}, "optionB": {"text": "先思考清楚再表达", "score": -1}},
    
    # S/N 维度 (信息获取)
    {"id": 6, "dimension": "S_N", "text": "你更关注：", "optionA": {"text": "具体的事实和细节", "score": 1}, "optionB": {"text": "可能性和整体模式", "score": -1}},
    {"id": 7, "dimension": "S_N", "text": "学习新事物时，你更喜欢：", "optionA": {"text": "按部就班，从基础开始", "score": 1}, "optionB": {"text": "先了解整体框架", "score": -1}},
    {"id": 8, "dimension": "S_N", "text": "你更信任：", "optionA": {"text": "过去的经验和实际数据", "score": 1}, "optionB": {"text": "直觉和灵感", "score": -1}},
    {"id": 9, "dimension": "S_N", "text": "描述一件事时，你：", "optionA": {"text": "注重具体细节", "score": 1}, "optionB": {"text": "喜欢比喻和联想", "score": -1}},
    {"id": 10, "dimension": "S_N", "text": "你更感兴趣的是：", "optionA": {"text": "已经存在的事物", "score": 1}, "optionB": {"text": "未来可能的事物", "score": -1}},
    
    # T/F 维度 (决策方式)
    {"id": 11, "dimension": "T_F", "text": "做决定时，你更重视：", "optionA": {"text": "逻辑和客观分析", "score": 1}, "optionB": {"text": "价值观和他人感受", "score": -1}},
    {"id": 12, "dimension": "T_F", "text": "朋友向你倾诉烦恼，你会：", "optionA": {"text": "帮他分析问题，提供解决方案", "score": 1}, "optionB": {"text": "先倾听，给予情感支持", "score": -1}},
    {"id": 13, "dimension": "T_F", "text": "你更在意：", "optionA": {"text": "事情是否正确合理", "score": 1}, "optionB": {"text": "是否和谐，大家是否开心", "score": -1}},
    {"id": 14, "dimension": "T_F", "text": "评价一个方案时，你更看重：", "optionA": {"text": "效率和效果", "score": 1}, "optionB": {"text": "对人的影响", "score": -1}},
    {"id": 15, "dimension": "T_F", "text": "面对批评，你：", "optionA": {"text": "关注批评是否有道理", "score": 1}, "optionB": {"text": "在意对方的语气和态度", "score": -1}},
    
    # J/P 维度 (生活方式)
    {"id": 16, "dimension": "J_P", "text": "你的生活方式更偏向：", "optionA": {"text": "有计划、有条理", "score": 1}, "optionB": {"text": "灵活、随性", "score": -1}},
    {"id": 17, "dimension": "J_P", "text": "截止日期前，你通常：", "optionA": {"text": "提前完成，不喜欢临时赶工", "score": 1}, "optionB": {"text": "在压力下效率更高", "score": -1}},
    {"id": 18, "dimension": "J_P", "text": "旅行时，你更喜欢：", "optionA": {"text": "提前规划好行程", "score": 1}, "optionB": {"text": "边走边看，随机应变", "score": -1}},
    {"id": 19, "dimension": "J_P", "text": "你的桌面/房间通常是：", "optionA": {"text": "整洁有序", "score": 1}, "optionB": {"text": "有点凌乱但你知道东西在哪", "score": -1}},
    {"id": 20, "dimension": "J_P", "text": "面对变化，你：", "optionA": {"text": "需要一些时间适应", "score": 1}, "optionB": {"text": "觉得新鲜刺激", "score": -1}},
]

# 兴趣标签及其权重
INTEREST_WEIGHTS = {
    "游戏": 10,
    "音乐": 8,
    "运动": 7,
    "读书": 6,
    "二次元": 9,
    "美食": 7,
    "旅行": 8,
    "电影": 7,
    "摄影": 6,
    "编程": 8,
    "绘画": 7,
    "舞蹈": 7,
    "桌游": 8,
    "剧本杀": 9,
    "密室逃脱": 8,
    "K歌": 7,
    "露营": 7,
    "健身": 6,
    "瑜伽": 5,
    "烘焙": 6,
    "咖啡": 5,
    "宠物": 6,
    "手工": 5,
    "写作": 5,
}

# ============ 人格分析函数 ============

def calculate_personality(answers: Dict[int, str]) -> Tuple[str, Dict[str, float]]:
    """
    根据问卷答案计算人格类型
    
    Args:
        answers: {question_id: "A" or "B"}
    
    Returns:
        (personality_type, dimension_scores)
        personality_type: 如 "ENFJ"
        dimension_scores: {"E_I": 0.6, "S_N": -0.2, ...}
    """
    dimension_scores = {"E_I": 0, "S_N": 0, "T_F": 0, "J_P": 0}
    dimension_counts = {"E_I": 0, "S_N": 0, "T_F": 0, "J_P": 0}
    
    for question in QUIZ_QUESTIONS:
        qid = question["id"]
        dimension = question["dimension"]
        
        if qid in answers:
            answer = answers[qid]
            if answer == "A":
                dimension_scores[dimension] += question["optionA"]["score"]
            else:
                dimension_scores[dimension] += question["optionB"]["score"]
            dimension_counts[dimension] += 1
    
    # 归一化到 [-1, 1] 范围
    for dim in dimension_scores:
        if dimension_counts[dim] > 0:
            dimension_scores[dim] = dimension_scores[dim] / dimension_counts[dim]
    
    # 确定人格类型
    personality = ""
    personality += "E" if dimension_scores["E_I"] >= 0 else "I"
    personality += "S" if dimension_scores["S_N"] >= 0 else "N"
    personality += "T" if dimension_scores["T_F"] >= 0 else "F"
    personality += "J" if dimension_scores["J_P"] >= 0 else "P"
    
    return personality, dimension_scores


def get_personality_description(personality_type: str) -> Dict:
    """获取人格类型描述"""
    descriptions = {
        "ISTJ": {"title": "检查者", "traits": ["可靠", "实际", "有条理"], "best_match": ["ESFP", "ESTP"]},
        "ISFJ": {"title": "保护者", "traits": ["温暖", "负责", "细心"], "best_match": ["ESFP", "ESTP"]},
        "INFJ": {"title": "提倡者", "traits": ["理想主义", "洞察力强", "有创造力"], "best_match": ["ENFP", "ENTP"]},
        "INTJ": {"title": "建筑师", "traits": ["独立", "有远见", "战略性思维"], "best_match": ["ENFP", "ENTP"]},
        "ISTP": {"title": "鉴赏家", "traits": ["灵活", "理性", "善于解决问题"], "best_match": ["ESFJ", "ESTJ"]},
        "ISFP": {"title": "探险家", "traits": ["艺术气质", "敏感", "活在当下"], "best_match": ["ESFJ", "ESTJ"]},
        "INFP": {"title": "调停者", "traits": ["理想主义", "共情能力强", "有创造力"], "best_match": ["ENFJ", "ENTJ"]},
        "INTP": {"title": "逻辑学家", "traits": ["好奇", "分析能力强", "客观"], "best_match": ["ENFJ", "ENTJ"]},
        "ESTP": {"title": "企业家", "traits": ["活力充沛", "务实", "善于应变"], "best_match": ["ISFJ", "ISTJ"]},
        "ESFP": {"title": "表演者", "traits": ["热情", "友好", "喜欢社交"], "best_match": ["ISFJ", "ISTJ"]},
        "ENFP": {"title": "竞选者", "traits": ["热情洋溢", "有创意", "善于激励"], "best_match": ["INFJ", "INTJ"]},
        "ENTP": {"title": "辩论家", "traits": ["聪明", "好奇", "喜欢挑战"], "best_match": ["INFJ", "INTJ"]},
        "ESTJ": {"title": "总经理", "traits": ["组织能力强", "果断", "实际"], "best_match": ["ISFP", "ISTP"]},
        "ESFJ": {"title": "执政官", "traits": ["热心", "有责任心", "善于合作"], "best_match": ["ISFP", "ISTP"]},
        "ENFJ": {"title": "主人公", "traits": ["有魅力", "有同理心", "善于领导"], "best_match": ["INFP", "INTP"]},
        "ENTJ": {"title": "指挥官", "traits": ["果断", "有远见", "天生的领导者"], "best_match": ["INFP", "INTP"]},
    }
    return descriptions.get(personality_type, {"title": "未知类型", "traits": [], "best_match": []})


# ============ 匹配算法 ============

def calculate_similarity(person_a, person_b, mode: str = "similar") -> float:
    """
    计算两个人的匹配相似度
    
    Args:
        person_a: Participant对象
        person_b: Participant对象
        mode: "similar"(同好) 或 "complementary"(互补)
    
    Returns:
        匹配分数 (0-100)
    """
    score = 0.0
    
    # 1. 人格类型相似度 (40分)
    dim_a = json.loads(person_a.dimension_scores)
    dim_b = json.loads(person_b.dimension_scores)
    
    if mode == "similar":
        # 同好模式：维度越接近分数越高
        personality_sim = 0
        for dim in ["E_I", "S_N", "T_F", "J_P"]:
            diff = abs(dim_a[dim] - dim_b[dim])
            personality_sim += (1 - diff) * 10  # 每维度最高10分
    else:
        # 互补模式：维度差异适中分数最高
        personality_sim = 0
        for dim in ["E_I", "S_N", "T_F", "J_P"]:
            diff = abs(dim_a[dim] - dim_b[dim])
            # 差异在0.5-1.0之间得分最高
            if 0.3 <= diff <= 0.8:
                personality_sim += 10
            else:
                personality_sim += (1 - abs(diff - 0.5)) * 10
    
    score += min(personality_sim, 40)
    
    # 2. 兴趣标签匹配度 (40分)
    interests_a = set(json.loads(person_a.interests)) if person_a.interests else set()
    interests_b = set(json.loads(person_b.interests)) if person_b.interests else set()
    
    if interests_a and interests_b:
        common = interests_a & interests_b
        total_weight = sum(INTEREST_WEIGHTS.get(i, 5) for i in common)
        max_possible = min(sum(INTEREST_WEIGHTS.get(i, 5) for i in interests_a),
                          sum(INTEREST_WEIGHTS.get(i, 5) for i in interests_b))
        if max_possible > 0:
            interest_score = (total_weight / max_possible) * 40
            score += min(interest_score, 40)
    
    # 3. 最佳人格类型匹配 (20分)
    desc_a = get_personality_description(person_a.personality_type)
    desc_b = get_personality_description(person_b.personality_type)
    
    if person_b.personality_type in desc_a.get("best_match", []):
        score += 20
    elif person_a.personality_type in desc_b.get("best_match", []):
        score += 20
    
    return round(score, 2)


def generate_match_reason(person_a, person_b) -> str:
    """生成匹配理由"""
    reasons = []
    
    # 人格类型匹配
    desc_a = get_personality_description(person_a.personality_type)
    desc_b = get_personality_description(person_b.personality_type)
    
    if person_b.personality_type in desc_a.get("best_match", []):
        reasons.append(f"{person_a.personality_type}与{person_b.personality_type}是经典互补组合")
    
    # 共同兴趣
    interests_a = set(json.loads(person_a.interests)) if person_a.interests else set()
    interests_b = set(json.loads(person_b.interests)) if person_b.interests else set()
    common = interests_a & interests_b
    
    if common:
        interests_str = "、".join(list(common)[:3])
        reasons.append(f"共同爱好：{interests_str}")
    
    # 维度互补/相似分析
    dim_a = json.loads(person_a.dimension_scores)
    dim_b = json.loads(person_b.dimension_scores)
    
    dim_names = {"E_I": "社交能量", "S_N": "认知方式", "T_F": "决策风格", "J_P": "生活态度"}
    
    for dim, name in dim_names.items():
        diff = abs(dim_a[dim] - dim_b[dim])
        if diff < 0.3:
            reasons.append(f"{name}高度一致")
        elif diff > 0.7:
            reasons.append(f"{name}互补")
    
    return "；".join(reasons) if reasons else "缘分使然"


def optimal_matching(participants: List, mode: str = "similar") -> List[Tuple]:
    """
    使用最大权匹配算法进行最优配对
    
    Args:
        participants: 参与者列表
        mode: "similar" 或 "complementary"
    
    Returns:
        [(person_a, person_b, score, reason), ...]
    """
    n = len(participants)
    if n < 2:
        return []
    
    # 构建完全图
    G = nx.Graph()
    
    # 添加所有参与者作为节点
    for p in participants:
        G.add_node(p.id, person=p)
    
    # 添加边（带权重）
    for i in range(n):
        for j in range(i + 1, n):
            score = calculate_similarity(participants[i], participants[j], mode)
            G.add_edge(participants[i].id, participants[j].id, weight=score)
    
    # 使用最大权匹配算法
    matching = nx.max_weight_matching(G, maxcardinality=True, weight="weight")
    
    # 整理结果
    results = []
    matched_ids = set()
    
    for id_a, id_b in matching:
        person_a = G.nodes[id_a]["person"]
        person_b = G.nodes[id_b]["person"]
        score = G[id_a][id_b]["weight"]
        reason = generate_match_reason(person_a, person_b)
        
        results.append((person_a, person_b, score, reason))
        matched_ids.add(id_a)
        matched_ids.add(id_b)
    
    # 处理未匹配的人（如果人数是奇数）
    unmatched = [p for p in participants if p.id not in matched_ids]
    
    return results, unmatched


# ============ 辅助函数 ============

def get_all_interests() -> List[str]:
    """获取所有可选兴趣标签"""
    return list(INTEREST_WEIGHTS.keys())

def get_quiz_questions() -> List[Dict]:
    """获取问卷题目"""
    return QUIZ_QUESTIONS
