# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import University, Department, Major, Course, MajorCourse

router = APIRouter(prefix="/compare", tags=["跨校对比"])

@router.get("/test", summary="测试接口", description="测试跨校对比模块是否正常")
async def test():
    return {"message": "跨校对比模块工作正常"}

@router.get("/major-courses", summary="对比专业课程", description="对比相同专业在两所学校的课程设置异同")
async def compare_major_courses(
    major_name: str = Query(..., description="专业名称，如：计算机科学与技术"),
    university1: str = Query("西南财经大学", description="第一所大学"),
    university2: str = Query("上海财经大学", description="第二所大学"),
    db: Session = Depends(get_db)
):
    """对比相同专业在两所学校的课程设置异同"""
    
    def get_courses(univ_name: str, major: str):
        return db.query(
            Course.name, Course.credits, Course.course_code
        ).join(
            MajorCourse, Course.id == MajorCourse.course_id
        ).join(
            Major, MajorCourse.major_id == Major.id
        ).join(
            Department, Major.dept_id == Department.id
        ).join(
            University, Department.university_id == University.id
        ).filter(
            University.name == univ_name,
            Major.name.contains(major)
        ).all()
    
    swufe_courses = get_courses(university1, major_name)
    sufe_courses = get_courses(university2, major_name)
    
    swufe_set = {c.name for c in swufe_courses}
    sufe_set = {c.name for c in sufe_courses}
    
    return {
        "专业名称": major_name,
        "大学一": university1,
        "大学二": university2,
        "统计信息": {
            f"{university1}课程数": len(swufe_courses),
            f"{university2}课程数": len(sufe_courses),
            "共同课程数": len(swufe_set & sufe_set),
            f"仅在{university1}": len(swufe_set - sufe_set),
            f"仅在{university2}": len(sufe_set - swufe_set)
        },
        "共同课程": list(swufe_set & sufe_set),
        f"仅在{university1}的课程": list(swufe_set - sufe_set),
        f"仅在{university2}的课程": list(sufe_set - swufe_set)
    }

@router.get("/total-credits", summary="对比专业学分", description="对比两校同一专业的总学分要求")
async def compare_total_credits(
    major_name: str = Query(..., description="专业名称，如：计算机科学与技术"),
    university1: str = Query("西南财经大学", description="第一所大学"),
    university2: str = Query("上海财经大学", description="第二所大学"),
    db: Session = Depends(get_db)
):
    """对比两校同一专业的总学分要求"""
    
    results = []
    for univ in [university1, university2]:
        major = db.query(Major).join(
            Department, Major.dept_id == Department.id
        ).join(
            University, Department.university_id == University.id
        ).filter(
            University.name == univ,
            Major.name.contains(major_name)
        ).first()
        
        if major:
            course_count = db.query(MajorCourse).filter(MajorCourse.major_id == major.id).count()
            results.append({
                "大学": univ,
                "专业名称": major.name,
                "总学分": float(major.total_credits),
                "课程数量": course_count,
                "学制": f"{major.duration_years}年"
            })
    
    if len(results) < 2:
        return {
            "专业名称": major_name,
            "提示": "未找到两校的该专业信息",
            "已找到的信息": results
        }
    
    return {
        "专业名称": major_name,
        "对比结果": results,
        "学分差值": abs(results[0]['总学分'] - results[1]['总学分']),
        "分析": f"{results[0]['大学']}的{results[0]['专业名称']}专业总学分为{results[0]['总学分']}，"
                f"{results[1]['大学']}为{results[1]['总学分']}，相差{abs(results[0]['总学分'] - results[1]['总学分'])}学分"
    }