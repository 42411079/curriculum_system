# scripts/init_db.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, SessionLocal, Base
from app.models.models import University, Department, Major, Course, MajorCourse

def init_database():
    """创建所有表"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建成功")

def import_swufe_data():
    """导入西南财经大学完整数据"""
    db = SessionLocal()
    
    try:
        # 1. 创建西南财经大学
        swufe = University(name="西南财经大学", short_name="SWUFE", location="四川成都", website="https://www.swufe.edu.cn")
        db.add(swufe)
        db.flush()
        print(f"✅ 创建大学: {swufe.name}")
        
        # 2. 创建学院
        departments = [
            {"name": "计算机与人工智能学院", "code": "CSAI"},
            {"name": "金融学院", "code": "FIN"},
            {"name": "经济学院", "code": "ECO"},
            {"name": "会计学院", "code": "ACC"},
            {"name": "统计学院", "code": "STAT"},
            {"name": "工商管理学院", "code": "BA"},
            {"name": "数学学院", "code": "MATH"},
            {"name": "法学院", "code": "LAW"},
            {"name": "财政税务学院", "code": "PUB"},
            {"name": "国际商学院", "code": "IBS"},
            {"name": "外国语学院", "code": "FLC"},
            {"name": "公共管理学院", "code": "PA"},
            {"name": "人文与艺术学院", "code": "HUM"},
        ]
        
        dept_objects = {}
        for dept in departments:
            d = Department(university_id=swufe.id, name=dept["name"], code=dept["code"])
            db.add(d)
            dept_objects[dept["name"]] = d
        db.flush()
        print(f"✅ 创建 {len(departments)} 个学院")
        
        # 3. 创建专业
        majors_data = [
            # 计算机与人工智能学院
            {"dept": "计算机与人工智能学院", "name": "计算机科学与技术", "code": "080901", "total_credits": 155},
            {"dept": "计算机与人工智能学院", "name": "人工智能", "code": "080717T", "total_credits": 152},
            {"dept": "计算机与人工智能学院", "name": "网络空间安全", "code": "080911TK", "total_credits": 152},
            # 金融学院
            {"dept": "金融学院", "name": "金融学", "code": "020301K", "total_credits": 152},
            {"dept": "金融学院", "name": "金融工程", "code": "020302", "total_credits": 152},
            {"dept": "金融学院", "name": "金融科技", "code": "020310T", "total_credits": 154},
            {"dept": "金融学院", "name": "精算学", "code": "020308T", "total_credits": 152},
            {"dept": "金融学院", "name": "信用管理", "code": "020306T", "total_credits": 152},
            {"dept": "金融学院", "name": "投资学", "code": "020304", "total_credits": 152},
            {"dept": "金融学院", "name": "保险学", "code": "020303", "total_credits": 151},
            # 经济学院
            {"dept": "经济学院", "name": "经济学", "code": "020101", "total_credits": 155},
            {"dept": "经济学院", "name": "数字经济", "code": "020109T", "total_credits": 153},
            # 会计学院
            {"dept": "会计学院", "name": "会计学", "code": "120203K", "total_credits": 144},
            {"dept": "会计学院", "name": "财务管理", "code": "120204", "total_credits": 144},
            {"dept": "会计学院", "name": "审计学", "code": "120207", "total_credits": 144},
            # 统计学院
            {"dept": "统计学院", "name": "统计学", "code": "071201", "total_credits": 145},
            {"dept": "统计学院", "name": "数据科学与大数据技术", "code": "080910T", "total_credits": 145},
            {"dept": "统计学院", "name": "经济统计学", "code": "020102", "total_credits": 149},
            # 工商管理学院
            {"dept": "工商管理学院", "name": "工商管理", "code": "120201K", "total_credits": 151},
            {"dept": "工商管理学院", "name": "市场营销", "code": "120202", "total_credits": 151},
            {"dept": "工商管理学院", "name": "人力资源管理", "code": "120206", "total_credits": 151},
            {"dept": "工商管理学院", "name": "供应链管理", "code": "120604T", "total_credits": 151},
            {"dept": "工商管理学院", "name": "旅游管理", "code": "120901K", "total_credits": 151},
            # 数学学院
            {"dept": "数学学院", "name": "金融数学", "code": "020305T", "total_credits": 151},
            {"dept": "数学学院", "name": "数学与应用数学", "code": "070101", "total_credits": 148},
            # 法学院
            {"dept": "法学院", "name": "法学", "code": "030101K", "total_credits": 148},
            # 财政税务学院
            {"dept": "财政税务学院", "name": "财政学", "code": "020201K", "total_credits": 148},
            {"dept": "财政税务学院", "name": "税收学", "code": "020202", "total_credits": 148},
            # 国际商学院
            {"dept": "国际商学院", "name": "国际商务", "code": "120205", "total_credits": 150},
            {"dept": "国际商学院", "name": "国际经济与贸易", "code": "020401", "total_credits": 150},
            # 外国语学院
            {"dept": "外国语学院", "name": "英语", "code": "050201", "total_credits": 151},
            {"dept": "外国语学院", "name": "商务英语", "code": "050262", "total_credits": 151},
            {"dept": "外国语学院", "name": "西班牙语", "code": "050205", "total_credits": 153},
            # 公共管理学院
            {"dept": "公共管理学院", "name": "行政管理", "code": "120402", "total_credits": 152},
            {"dept": "公共管理学院", "name": "劳动与社会保障", "code": "120403", "total_credits": 152},
            # 人文与艺术学院
            {"dept": "人文与艺术学院", "name": "汉语言文学", "code": "050101", "total_credits": 152},
            {"dept": "人文与艺术学院", "name": "数字媒体艺术", "code": "130508", "total_credits": 151},
            {"dept": "人文与艺术学院", "name": "网络与新媒体", "code": "050306T", "total_credits": 149},
            {"dept": "人文与艺术学院", "name": "新闻学", "code": "050301", "total_credits": 149},
        ]
        
        major_objects = {}
        for m in majors_data:
            major = Major(
                dept_id=dept_objects[m["dept"]].id,
                name=m["name"],
                code=m["code"],
                total_credits=m["total_credits"],
                duration_years=4
            )
            db.add(major)
            major_objects[m["name"]] = major
        db.flush()
        print(f"✅ 创建 {len(majors_data)} 个专业")
        
        # 4. 课程数据（基于PDF完整提取）
        courses_data = [
            # ===== 数学类基础课 =====
            {"code": "MAT514", "name": "数学分析I（理科）", "credits": 6, "hours": 102, "type": "必修", "semester": 1, "college": "数学学院"},
            {"code": "MAT515", "name": "数学分析II（理科）", "credits": 6, "hours": 102, "type": "必修", "semester": 2, "college": "数学学院"},
            {"code": "MAT506", "name": "高等代数I（理科）", "credits": 4, "hours": 68, "type": "必修", "semester": 1, "college": "数学学院"},
            {"code": "MAT507", "name": "高等代数II（理科）", "credits": 4, "hours": 68, "type": "必修", "semester": 2, "college": "数学学院"},
            {"code": "MAT324", "name": "概率论（理科）", "credits": 4, "hours": 68, "type": "必修", "semester": 3, "college": "数学学院"},
            {"code": "MAT516", "name": "数学分析III（理科）", "credits": 5, "hours": 85, "type": "必修", "semester": 3, "college": "数学学院"},
            {"code": "MAT513", "name": "数理统计", "credits": 3, "hours": 51, "type": "必修", "semester": 4, "college": "数学学院"},
            {"code": "MAT301", "name": "高等数学I", "credits": 5, "hours": 85, "type": "必修", "semester": 1, "college": "数学学院"},
            {"code": "MAT302", "name": "高等数学II", "credits": 5, "hours": 85, "type": "必修", "semester": 2, "college": "数学学院"},
            {"code": "MAT211", "name": "线性代数", "credits": 3, "hours": 51, "type": "必修", "semester": 2, "college": "数学学院"},
            {"code": "MAT328", "name": "概率论与数理统计B", "credits": 4, "hours": 68, "type": "必修", "semester": 3, "college": "统计学院"},
            {"code": "MAT327", "name": "概率论与数理统计A", "credits": 5, "hours": 85, "type": "必修", "semester": 3, "college": "数学学院"},
            
            # ===== 计算机类课程 =====
            {"code": "CST117", "name": "程序设计（C语言）", "credits": 3, "hours": 51, "type": "必修", "semester": 1, "college": "计算机与人工智能学院"},
            {"code": "CST124", "name": "数据结构（C语言）", "credits": 3, "hours": 51, "type": "必修", "semester": 2, "college": "计算机与人工智能学院"},
            {"code": "CST116", "name": "面向对象程序设计(JAVA SE)", "credits": 3, "hours": 51, "type": "必修", "semester": 3, "college": "计算机与人工智能学院"},
            {"code": "CST118", "name": "离散数学", "credits": 3, "hours": 51, "type": "必修", "semester": 2, "college": "计算机与人工智能学院"},
            {"code": "CST207", "name": "算法分析与设计", "credits": 3, "hours": 51, "type": "必修", "semester": 3, "college": "计算机与人工智能学院"},
            {"code": "CST205", "name": "数据库原理与应用", "credits": 3, "hours": 51, "type": "必修", "semester": 4, "college": "计算机与人工智能学院"},
            {"code": "CST203", "name": "计算机网络", "credits": 3, "hours": 51, "type": "必修", "semester": 5, "college": "计算机与人工智能学院"},
            {"code": "FIT403", "name": "计算机组成原理", "credits": 3, "hours": 51, "type": "必修", "semester": 4, "college": "计算机与人工智能学院"},
            {"code": "CST204", "name": "操作系统", "credits": 3, "hours": 51, "type": "必修", "semester": 5, "college": "计算机与人工智能学院"},
            {"code": "DSC321", "name": "机器学习与数据挖掘", "credits": 4, "hours": 68, "type": "必修", "semester": 4, "college": "计算机与人工智能学院"},
            {"code": "DSC401", "name": "深度学习", "credits": 3, "hours": 51, "type": "必修", "semester": 5, "college": "计算机与人工智能学院"},
            {"code": "CST308", "name": "自然语言处理", "credits": 3, "hours": 51, "type": "必修", "semester": 6, "college": "计算机与人工智能学院"},
            {"code": "CST201", "name": "数字逻辑电路", "credits": 3, "hours": 51, "type": "选修", "semester": 3, "college": "计算机与人工智能学院"},
            {"code": "CST322", "name": "软件工程", "credits": 3, "hours": 51, "type": "必修", "semester": 5, "college": "计算机与人工智能学院"},
            {"code": "CST327", "name": "大数据技术", "credits": 3, "hours": 51, "type": "选修", "semester": 6, "college": "计算机与人工智能学院"},
            {"code": "CST332", "name": "现代密码学", "credits": 3, "hours": 51, "type": "选修", "semester": 3, "college": "计算机与人工智能学院"},
            {"code": "CST333", "name": "网络安全原理与实践", "credits": 3, "hours": 51, "type": "选修", "semester": 5, "college": "计算机与人工智能学院"},
            {"code": "CST326", "name": "区块链技术", "credits": 3, "hours": 51, "type": "选修", "semester": 6, "college": "计算机与人工智能学院"},
            {"code": "DSC202", "name": "数据可视化", "credits": 3, "hours": 51, "type": "选修", "semester": 5, "college": "计算机与人工智能学院"},
            {"code": "CST302", "name": "数字图像处理", "credits": 3, "hours": 51, "type": "选修", "semester": 6, "college": "计算机与人工智能学院"},
            {"code": "CST344", "name": "机器视觉", "credits": 3, "hours": 51, "type": "选修", "semester": 6, "college": "计算机与人工智能学院"},
            
            # ===== 经济/金融类课程 =====
            {"code": "ECO101", "name": "微观经济学", "credits": 3, "hours": 51, "type": "必修", "semester": 1, "college": "经济学院"},
            {"code": "ECO102", "name": "宏观经济学", "credits": 3, "hours": 51, "type": "必修", "semester": 2, "college": "经济学院"},
            {"code": "ECO100", "name": "政治经济学", "credits": 3, "hours": 51, "type": "必修", "semester": 1, "college": "经济学院"},
            {"code": "FIN200", "name": "货币金融学", "credits": 3, "hours": 51, "type": "必修", "semester": 3, "college": "金融学院"},
            {"code": "FIN303", "name": "公司金融", "credits": 3, "hours": 51, "type": "必修", "semester": 3, "college": "金融学院"},
            {"code": "FIN304", "name": "投资学", "credits": 3, "hours": 51, "type": "必修", "semester": 4, "college": "金融学院"},
            {"code": "BST300", "name": "计量经济学", "credits": 3, "hours": 51, "type": "必修", "semester": 5, "college": "统计学院"},
            {"code": "ACC200", "name": "会计学", "credits": 3, "hours": 51, "type": "必修", "semester": 2, "college": "会计学院"},
            {"code": "FEG401", "name": "衍生金融工具", "credits": 3, "hours": 51, "type": "必修", "semester": 6, "college": "金融学院"},
            {"code": "FEG404", "name": "金融风险管理", "credits": 3, "hours": 51, "type": "必修", "semester": 5, "college": "金融学院"},
            {"code": "FEG403", "name": "金融计量学", "credits": 3, "hours": 51, "type": "必修", "semester": 6, "college": "金融学院"},
            {"code": "FIN305", "name": "国际金融学", "credits": 3, "hours": 51, "type": "必修", "semester": 5, "college": "金融学院"},
            
            # ===== 通识课 =====
            {"code": "IPT102", "name": "中国近现代史纲要", "credits": 3, "hours": 51, "type": "必修", "semester": 2, "college": "马克思主义学院"},
            {"code": "IPT107", "name": "思想道德与法治", "credits": 3, "hours": 51, "type": "必修", "semester": 1, "college": "马克思主义学院"},
            {"code": "IPT103", "name": "马克思主义基本原理", "credits": 3, "hours": 51, "type": "必修", "semester": 3, "college": "马克思主义学院"},
            {"code": "IPT104", "name": "毛泽东思想和中国特色社会主义理论体系概论", "credits": 3, "hours": 51, "type": "必修", "semester": 4, "college": "马克思主义学院"},
            {"code": "IPT109", "name": "习近平新时代中国特色社会主义思想概论", "credits": 3, "hours": 51, "type": "必修", "semester": 5, "college": "马克思主义学院"},
            {"code": "IPT205", "name": "形势与政策", "credits": 2, "hours": 64, "type": "必修", "semester": 1, "college": "马克思主义学院"},
            {"code": "ENG103", "name": "综合英语III", "credits": 2, "hours": 34, "type": "必修", "semester": 1, "college": "外国语学院"},
            {"code": "ENG125", "name": "听说写能力训练", "credits": 2, "hours": 34, "type": "必修", "semester": 1, "college": "外国语学院"},
            {"code": "PED100", "name": "体育I", "credits": 1, "hours": 36, "type": "限选", "semester": 1, "college": "体育学院"},
            {"code": "PED200", "name": "体育II", "credits": 1, "hours": 36, "type": "限选", "semester": 2, "college": "体育学院"},
            {"code": "PED300", "name": "体育III", "credits": 1, "hours": 36, "type": "限选", "semester": 3, "college": "体育学院"},
            {"code": "PED400", "name": "体育IV", "credits": 1, "hours": 36, "type": "限选", "semester": 4, "college": "体育学院"},
            {"code": "JOB100", "name": "大学生职业生涯规划与创业基础", "credits": 2, "hours": 34, "type": "必修", "semester": 3, "college": "学生职业规划与就业指导中心"},
            {"code": "MTT101", "name": "军事理论", "credits": 2, "hours": 36, "type": "必修", "semester": 2, "college": "武装部"},
            {"code": "MTT201", "name": "国家安全教育", "credits": 1, "hours": 16, "type": "必修", "semester": 2, "college": "武装部"},
            {"code": "HUM104", "name": "大学生心理健康与人生发展", "credits": 2, "hours": 34, "type": "必修", "semester": 2, "college": "心理健康教育中心"},
        ]
        
        course_objects = {}
        for cd in courses_data:
            existing = db.query(Course).filter(Course.course_code == cd["code"]).first()
            if not existing:
                course = Course(
                    course_code=cd["code"],
                    name=cd["name"],
                    credits=cd["credits"],
                    hours=cd.get("hours"),
                    course_type=cd["type"],
                    semester=cd.get("semester"),
                    college=cd.get("college")
                )
                db.add(course)
                course_objects[cd["code"]] = course
            else:
                course_objects[cd["code"]] = existing
        db.flush()
        print(f"✅ 导入 {len(courses_data)} 门课程")
        
        # 5. 关联课程到专业（专业-课程映射）
        major_course_mapping = {
            "计算机科学与技术": {
                "required": [
                    "MAT514", "MAT515", "MAT506", "MAT507", "MAT324", "MAT516", "MAT513",
                    "CST117", "CST124", "CST116", "CST118", "CST207", "CST205", "CST203",
                    "FIT403", "CST204", "DSC321", "DSC401", "CST308", "CST322",
                    "ECO101", "ECO102", "ECO100", "FIN200", "ACC200"
                ],
                "elective": ["CST201", "CST327", "CST332", "CST333", "CST326", "DSC202", "CST302"]
            },
            "金融学": {
                "required": ["ECO101", "ECO102", "ECO100", "ACC200", "BST300", "FIN200", "FIN303", "FIN304", "FEG401", "FEG404", "FEG403", "FIN305"],
                "elective": []
            },
            "经济学": {
                "required": ["ECO101", "ECO102", "ECO100", "BST300", "FIN200"],
                "elective": []
            },
            "会计学": {
                "required": ["ECO101", "ECO102", "ACC200", "ECO100"],
                "elective": []
            },
        }
        
        for major_name, mapping in major_course_mapping.items():
            if major_name in major_objects:
                major = major_objects[major_name]
                for code in mapping["required"]:
                    if code in course_objects:
                        db.add(MajorCourse(major_id=major.id, course_id=course_objects[code].id, is_required=True))
                for code in mapping["elective"]:
                    if code in course_objects:
                        db.add(MajorCourse(major_id=major.id, course_id=course_objects[code].id, is_required=False))
        
        db.commit()
        
        # 统计
        for major_name in ["计算机科学与技术", "金融学", "经济学", "会计学"]:
            if major_name in major_objects:
                major = major_objects[major_name]
                req_count = db.query(MajorCourse).filter(MajorCourse.major_id == major.id, MajorCourse.is_required == True).count()
                elec_count = db.query(MajorCourse).filter(MajorCourse.major_id == major.id, MajorCourse.is_required == False).count()
                print(f"  ✅ {major_name}: 必修{req_count}门, 选修{elec_count}门, 总学分{major.total_credits}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 导入失败: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
    import_swufe_data()