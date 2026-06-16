# scripts/import_sufe.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.models import University, Department, Major, Course, MajorCourse

def import_sufe_data():
    """导入上海财经大学数据"""
    db = SessionLocal()
    
    try:
        # 1. 创建上海财经大学
        sufe = University(
            name="上海财经大学",
            short_name="SUFE",
            location="上海",
            website="https://www.sufe.edu.cn"
        )
        db.add(sufe)
        db.flush()
        print(f"✅ 创建大学: {sufe.name}")
        
        # 2. 创建学院
        cs_dept = Department(
            university_id=sufe.id,
            name="计算机与人工智能学院",
            code="CSAI"
        )
        fin_dept = Department(
            university_id=sufe.id,
            name="金融学院",
            code="FIN"
        )
        db.add_all([cs_dept, fin_dept])
        db.flush()
        
        # 3. 创建专业
        cs_major = Major(
            dept_id=cs_dept.id,
            name="计算机科学与技术",
            total_credits=158,
            duration_years=4
        )
        fin_major = Major(
            dept_id=fin_dept.id,
            name="金融学",
            total_credits=150,
            duration_years=4
        )
        db.add_all([cs_major, fin_major])
        db.flush()
        
        # 4. 上海财大课程数据
        sufe_courses = [
            # 计算机科学与技术专业课程
            {"code": "SUFE_CS101", "name": "高级程序设计与实验", "credits": 4, "hours": 64, "type": "必修", "semester": 1, "college": "计算机与人工智能学院"},
            {"code": "SUFE_CS102", "name": "数据结构与算法", "credits": 4, "hours": 64, "type": "必修", "semester": 2, "college": "计算机与人工智能学院"},
            {"code": "SUFE_CS201", "name": "计算机组成与系统结构", "credits": 3, "hours": 48, "type": "必修", "semester": 3, "college": "计算机与人工智能学院"},
            {"code": "SUFE_CS202", "name": "操作系统原理", "credits": 3, "hours": 48, "type": "必修", "semester": 4, "college": "计算机与人工智能学院"},
            {"code": "SUFE_CS301", "name": "数据库系统", "credits": 3, "hours": 48, "type": "必修", "semester": 5, "college": "计算机与人工智能学院"},
            {"code": "SUFE_CS302", "name": "计算机网络", "credits": 3, "hours": 48, "type": "必修", "semester": 5, "college": "计算机与人工智能学院"},
            {"code": "SUFE_CS401", "name": "软件工程", "credits": 3, "hours": 48, "type": "必修", "semester": 6, "college": "计算机与人工智能学院"},
            {"code": "SUFE_ECO201", "name": "经济学原理", "credits": 3, "hours": 48, "type": "必修", "semester": 2, "college": "经济学院"},
            {"code": "SUFE_ECO202", "name": "中级微观经济学", "credits": 3, "hours": 48, "type": "必修", "semester": 3, "college": "经济学院"},
            {"code": "SUFE_ECO203", "name": "中级宏观经济学", "credits": 3, "hours": 48, "type": "必修", "semester": 4, "college": "经济学院"},
            # 金融学专业课程
            {"code": "SUFE_FIN101", "name": "货币银行学", "credits": 3, "hours": 48, "type": "必修", "semester": 3, "college": "金融学院"},
            {"code": "SUFE_FIN102", "name": "公司金融", "credits": 3, "hours": 48, "type": "必修", "semester": 4, "college": "金融学院"},
            {"code": "SUFE_FIN103", "name": "投资学", "credits": 3, "hours": 48, "type": "必修", "semester": 4, "college": "金融学院"},
            {"code": "SUFE_FIN104", "name": "国际金融", "credits": 3, "hours": 48, "type": "必修", "semester": 5, "college": "金融学院"},
            {"code": "SUFE_FIN105", "name": "金融风险管理", "credits": 3, "hours": 48, "type": "必修", "semester": 5, "college": "金融学院"},
            {"code": "SUFE_FIN106", "name": "衍生金融工具", "credits": 3, "hours": 48, "type": "必修", "semester": 6, "college": "金融学院"},
            {"code": "SUFE_ACC101", "name": "会计学", "credits": 3, "hours": 48, "type": "必修", "semester": 2, "college": "会计学院"},
        ]
        
        course_objects = {}
        for cd in sufe_courses:
            course = Course(
                course_code=cd["code"],
                name=cd["name"],
                credits=cd["credits"],
                hours=cd["hours"],
                course_type=cd["type"],
                semester=cd["semester"],
                college=cd["college"]
            )
            db.add(course)
            course_objects[cd["code"]] = course
        db.flush()
        
        # 5. 关联课程到专业
        # 计算机专业课程
        cs_courses = ["SUFE_CS101", "SUFE_CS102", "SUFE_CS201", "SUFE_CS202", 
                      "SUFE_CS301", "SUFE_CS302", "SUFE_CS401", "SUFE_ECO201",
                      "SUFE_ECO202", "SUFE_ECO203"]
        for code in cs_courses:
            if code in course_objects:
                db.add(MajorCourse(major_id=cs_major.id, course_id=course_objects[code].id, is_required=True))
        
        # 金融学专业课程
        fin_courses = ["SUFE_FIN101", "SUFE_FIN102", "SUFE_FIN103", "SUFE_FIN104",
                       "SUFE_FIN105", "SUFE_FIN106", "SUFE_ACC101", "SUFE_ECO201",
                       "SUFE_ECO202"]
        for code in fin_courses:
            if code in course_objects:
                db.add(MajorCourse(major_id=fin_major.id, course_id=course_objects[code].id, is_required=True))
        
        db.commit()
        
        print(f"✅ 上海财经大学数据导入完成！")
        print(f"   - 计算机科学与技术: 必修{len(cs_courses)}门, 总学分{cs_major.total_credits}")
        print(f"   - 金融学: 必修{len(fin_courses)}门, 总学分{fin_major.total_credits}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 导入失败: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import_sufe_data()