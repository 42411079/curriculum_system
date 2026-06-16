# app/api/queries.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func
from typing import List, Optional
from app.core.database import get_db
from app.models.models import University, Department, Major, Course, MajorCourse

router = APIRouter(prefix="/queries", tags=["查询接口"])

# ========== 查询1: 查询某专业的必修课列表 ==========
@router.get("/major/{major_id}/required-courses")
async def get_required_courses(major_id: int, db: Session = Depends(get_db)):
    """查询某专业的必修课列表"""
    major = db.query(Major).filter(Major.id == major_id).first()
    if not major:
        raise HTTPException(status_code=404, detail="专业不存在")
    
    courses = db.query(Course).join(MajorCourse).filter(
        MajorCourse.major_id == major_id,
        MajorCourse.is_required == True
    ).order_by(Course.semester, Course.course_code).all()
    
    # 计算总学分
    total_credits = sum(c.credits for c in courses)
    
    return {
        "major_id": major.id,
        "major_name": major.name,
        "total_credits_required": float(major.total_credits),
        "calculated_credits": total_credits,
        "course_count": len(courses),
        "courses": [
            {
                "course_code": c.course_code,
                "name": c.name,
                "credits": c.credits,
                "hours": c.hours,
                "course_type": c.course_type,
                "semester": c.semester,
                "college": c.college
            } for c in courses
        ]
    }

# ========== 查询2: 查询某门课程的学分、学时信息 ==========
@router.get("/course/{course_identifier}")
async def get_course_info(course_identifier: str, db: Session = Depends(get_db)):
    """查询某门课程的学分、学时信息（支持课程代码或名称）"""
    course = db.query(Course).filter(
        or_(
            Course.course_code == course_identifier,
            Course.name.ilike(f"%{course_identifier}%")
        )
    ).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    return {
        "course_code": course.course_code,
        "name": course.name,
        "credits": course.credits,
        "hours": course.hours,
        "course_type": course.course_type,
        "semester": course.semester,
        "college": course.college,
        "category": course.category
    }

# ========== 查询3: 查询某专业的总学分要求 ==========
@router.get("/major/{major_id}/total-credits")
async def get_major_credits(major_id: int, db: Session = Depends(get_db)):
    """查询某专业的总学分要求"""
    major = db.query(Major).filter(Major.id == major_id).first()
    if not major:
        raise HTTPException(status_code=404, detail="专业不存在")
    
    # 统计已修学分
    stats = db.query(
        func.sum(Course.credits).label("total"),
        func.count(Course.id).label("course_count")
    ).join(MajorCourse).filter(MajorCourse.major_id == major_id).first()
    
    return {
        "major_id": major.id,
        "major_name": major.name,
        "total_credits_required": float(major.total_credits),
        "current_courses_total_credits": float(stats.total or 0),
        "courses_count": stats.course_count or 0,
        "duration_years": major.duration_years,
        "degree_type": major.degree_type
    }

# ========== 查询4: 查询开设某门课程的所有专业 ==========
@router.get("/course/{course_identifier}/majors")
async def get_majors_by_course(course_identifier: str, db: Session = Depends(get_db)):
    """查询开设某门课程的所有专业"""
    course = db.query(Course).filter(
        or_(
            Course.course_code == course_identifier,
            Course.name.ilike(f"%{course_identifier}%")
        )
    ).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    results = db.query(
        Major.id,
        Major.name.label("major_name"),
        Department.name.label("dept_name"),
        University.name.label("university_name"),
        Major.total_credits,
        MajorCourse.is_required,
        MajorCourse.recommended_semester
    ).join(
        MajorCourse, Major.id == MajorCourse.major_id
    ).join(
        Department, Major.dept_id == Department.id
    ).join(
        University, Department.university_id == University.id
    ).filter(
        MajorCourse.course_id == course.id
    ).all()
    
    return {
        "course_code": course.course_code,
        "course_name": course.name,
        "total_majors": len(results),
        "majors": [
            {
                "major_id": r.id,
                "major_name": r.major_name,
                "dept_name": r.dept_name,
                "university": r.university_name,
                "total_credits": float(r.total_credits),
                "is_required": r.is_required,
                "recommended_semester": r.recommended_semester
            } for r in results
        ]
    }

# ========== 查询5: 查询某学院下所有专业的培养方案概览 ==========
@router.get("/department/{dept_id}/overview")
async def get_department_overview(dept_id: int, db: Session = Depends(get_db)):
    """查询某学院下所有专业的培养方案概览"""
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="学院不存在")
    
    majors = db.query(Major).filter(Major.dept_id == dept_id).all()
    
    result = []
    for major in majors:
        # 统计课程信息（修复：不使用cast）
        total_courses = db.query(MajorCourse).filter(MajorCourse.major_id == major.id).count()
        required_count = db.query(MajorCourse).filter(
            MajorCourse.major_id == major.id,
            MajorCourse.is_required == True
        ).count()
        
        result.append({
            "major_id": major.id,
            "major_name": major.name,
            "major_code": major.code,
            "total_credits": float(major.total_credits),
            "duration_years": major.duration_years,
            "total_courses": total_courses,
            "required_courses": required_count,
            "elective_courses": total_courses - required_count
        })
    
    return {
        "department_id": dept_id,
        "department_name": dept.name,
        "department_code": dept.code,
        "total_majors": len(result),
        "majors": result
    }
# ========== 查询6: 支持关键词模糊搜索课程名称 ==========
@router.get("/courses/search")
async def search_courses(
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """关键词模糊搜索课程名称（支持分页）"""
    offset = (page - 1) * page_size
    
    # 搜索课程
    query = db.query(Course).filter(
        or_(
            Course.name.ilike(f"%{keyword}%"),
            Course.course_code.ilike(f"%{keyword}%")
        )
    )
    
    total = query.count()
    courses = query.offset(offset).limit(page_size).all()
    
    return {
        "keyword": keyword,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "courses": [
            {
                "course_code": c.course_code,
                "name": c.name,
                "credits": c.credits,
                "hours": c.hours,
                "course_type": c.course_type,
                "semester": c.semester,
                "college": c.college
            } for c in courses
        ]
    }

# ========== 辅助接口：获取所有专业列表 ==========
@router.get("/majors")
async def get_all_majors(db: Session = Depends(get_db)):
    """获取所有专业列表"""
    majors = db.query(Major).all()
    return [
        {
            "id": m.id,
            "name": m.name,
            "dept_name": m.department.name if m.department else None,
            "total_credits": float(m.total_credits)
        } for m in majors
    ]

# ========== 辅助接口：获取所有学院列表 ==========
@router.get("/departments")
async def get_all_departments(db: Session = Depends(get_db)):
    """获取所有学院列表"""
    depts = db.query(Department).all()
    return [
        {
            "id": d.id,
            "name": d.name,
            "code": d.code,
            "university": d.university.name if d.university else None
        } for d in depts
    ]