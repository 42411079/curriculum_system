# scripts/import_sufe_from_json.py
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.models import University, Department, Major, Course, MajorCourse

def import_sufe_from_json():
    """从JSON文件导入上海财经大学数据"""
    db = SessionLocal()
    
    # 读取JSON文件
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                              "data", "sufe_data.json")
    
    if not os.path.exists(json_path):
        print(f"❌ JSON文件不存在: {json_path}")
        print("请先创建 data/sufe_data.json 文件")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    try:
        # 检查大学是否已存在
        existing_uni = db.query(University).filter(University.name == data["university"]["name"]).first()
        if existing_uni:
            print(f"⚠️ 大学已存在，跳过创建: {existing_uni.name}")
            sufe = existing_uni
        else:
            sufe = University(
                name=data["university"]["name"],
                short_name=data["university"]["short_name"],
                location=data["university"]["location"]
            )
            db.add(sufe)
            db.flush()
            print(f"✅ 创建大学: {sufe.name}")
        
        # 遍历学院和专业
        for dept_data in data["departments"]:
            existing_dept = db.query(Department).filter(
                Department.university_id == sufe.id,
                Department.name == dept_data["name"]
            ).first()
            
            if existing_dept:
                dept = existing_dept
                print(f"  ⚠️ 学院已存在: {dept.name}")
            else:
                dept = Department(
                    university_id=sufe.id,
                    name=dept_data["name"],
                    code=dept_data.get("code")
                )
                db.add(dept)
                db.flush()
                print(f"  ✅ 创建学院: {dept.name}")
            
            for major_data in dept_data["majors"]:
                existing_major = db.query(Major).filter(
                    Major.dept_id == dept.id,
                    Major.name == major_data["name"]
                ).first()
                
                if existing_major:
                    major = existing_major
                    print(f"    ⚠️ 专业已存在: {major.name}")
                else:
                    major = Major(
                        dept_id=dept.id,
                        name=major_data["name"],
                        total_credits=major_data["total_credits"],
                        duration_years=4
                    )
                    db.add(major)
                    db.flush()
                    print(f"    ✅ 创建专业: {major.name} (总学分{major.total_credits})")
                
                # 导入课程
                for course_data in major_data["courses"]:
                    existing_course = db.query(Course).filter(
                        Course.name == course_data["name"],
                        Course.college == dept.name
                    ).first()
                    
                    if existing_course:
                        print(f"      ⚠️ 课程已存在: {existing_course.name}")
                    else:
                        course = Course(
                            course_code=f"SUFE_{course_data['name'][:10]}",
                            name=course_data["name"],
                            credits=course_data["credits"],
                            hours=course_data["hours"],
                            course_type=course_data["type"],
                            semester=course_data["semester"],
                            college=dept.name
                        )
                        db.add(course)
                        db.flush()
                        print(f"      ✅ 创建课程: {course.name} ({course.credits}学分)")
                        
                        # 关联课程到专业
                        db.add(MajorCourse(
                            major_id=major.id,
                            course_id=course.id,
                            is_required=(course_data["type"] == "必修")
                        ))
        
        db.commit()
        print("\n🎉 上海财经大学数据导入完成！")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 导入失败: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import_sufe_from_json()