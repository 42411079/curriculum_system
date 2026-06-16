# -*- coding: utf-8 -*-
import re
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Major, Course, University, Department, MajorCourse

router = APIRouter(prefix="/nl", tags=["自然语言查询"])

@router.post("/query", summary="自然语言查询", description="用户可用中文提问，系统自动返回查询结果")
async def natural_language_query(
    question: str = Query(..., description="中文问题，如：计算机科学与技术专业有哪些必修课"),
    db: Session = Depends(get_db)
):
    """自然语言查询接口 - 用户可用中文提问"""
    q = question.lower()
    
    # 规则1：查询某专业的必修课
    if "专业" in q and "必修" in q:
        match = re.search(r'(.+?)专业', q)
        if match:
            major_name = match.group(1)
            major = db.query(Major).filter(Major.name.contains(major_name)).first()
            if major:
                courses = db.query(Course).join(MajorCourse).filter(
                    MajorCourse.major_id == major.id,
                    MajorCourse.is_required == True
                ).all()
                return {
                    "问题": question,
                    "查询类型": "专业必修课",
                    "专业": major.name,
                    "课程数量": len(courses),
                    "必修课程列表": [{"课程名称": c.name, "学分": c.credits} for c in courses]
                }
            else:
                return {"问题": question, "错误": f"未找到专业：{major_name}"}
    
    # 规则2：查询课程学分
    if "课程" in q and "学分" in q:
        match = re.search(r'(.+?)课程', q)
        if match:
            course_name = match.group(1)
            course = db.query(Course).filter(Course.name.contains(course_name)).first()
            if course:
                return {
                    "问题": question,
                    "查询类型": "课程信息",
                    "课程名称": course.name,
                    "学分": course.credits,
                    "学时": course.hours,
                    "课程类型": course.course_type
                }
            else:
                return {"问题": question, "错误": f"未找到课程：{course_name}"}
    
    # 规则3：查询专业总学分
    if "专业" in q and "总学分" in q:
        match = re.search(r'(.+?)专业', q)
        if match:
            major_name = match.group(1)
            major = db.query(Major).filter(Major.name.contains(major_name)).first()
            if major:
                return {
                    "问题": question,
                    "查询类型": "专业总学分",
                    "专业": major.name,
                    "总学分": major.total_credits
                }
            else:
                return {"问题": question, "错误": f"未找到专业：{major_name}"}
    
    # 规则4：跨校对比
    if "对比" in q and "专业" in q:
        match = re.search(r'对比(.+?)专业', q)
        if match:
            major_name = match.group(1)
            results = []
            universities = db.query(University).all()
            for uni in universities:
                major = db.query(Major).join(Department).join(University).filter(
                    University.id == uni.id,
                    Major.name.contains(major_name)
                ).first()
                if major:
                    course_count = db.query(MajorCourse).filter(MajorCourse.major_id == major.id).count()
                    results.append({
                        "大学": uni.name,
                        "专业": major.name,
                        "总学分": float(major.total_credits),
                        "课程数量": course_count
                    })
            if results:
                return {
                    "问题": question,
                    "查询类型": "跨校对比",
                    "对比结果": results
                }
            else:
                return {"问题": question, "错误": f"未找到专业对比数据：{major_name}"}
    
    # 默认：搜索课程
    courses = db.query(Course).filter(Course.name.contains(question)).limit(10).all()
    if courses:
        return {
            "问题": question,
            "查询类型": "课程搜索",
            "结果数量": len(courses),
            "课程列表": [{"课程名称": c.name, "课程代码": c.course_code, "学分": c.credits} for c in courses]
        }
    else:
        return {"问题": question, "错误": "未找到相关结果"}