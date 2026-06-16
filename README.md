# 📚 培养方案数据库系统

> 西南财经大学2024级本科人才培养方案数据库系统

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-green.svg)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3.0-orange.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 项目简介

本项目针对**西南财经大学2024级本科生人才培养方案**，设计并实现了一个完整的培养方案数据库系统。

系统包含两个子模块：

- **子模块A**：实现了培养方案数据的存储及6项核心查询功能
- **子模块B**：整合了上海财经大学培养方案数据，实现了跨校对比分析和自然语言查询接口

---

## ✨ 功能列表

### 子模块A：基础查询

| 序号 | 功能 | 说明 |
|------|------|------|
| 1 | 查询某专业的必修课列表 | 获取指定专业的所有必修课程 |
| 2 | 查询某门课程的学分、学时信息 | 获取课程的详细教学信息 |
| 3 | 查询某专业的总学分要求 | 获取专业的毕业学分要求 |
| 4 | 查询开设某门课程的所有专业 | 查找哪些专业开设了指定课程 |
| 5 | 查询某学院下所有专业的培养方案概览 | 查看学院的完整专业布局 |
| 6 | 关键词模糊搜索课程名称 | 快速查找包含关键词的课程 |

### 子模块B：跨校对比分析

- ✅ 对比两校同一专业的课程设置异同
- ✅ 对比两校同一专业的总学分要求

### 子模块C：自然语言查询

用户可用中文提问，系统自动返回查询结果：

```bash
"计算机科学与技术专业有哪些必修课"
"数据结构课程有多少学分"
"对比计算机科学与技术专业"
🛠️ 技术栈
层级	技术	版本
Web框架	FastAPI	0.128.0
ORM	SQLAlchemy	2.0+
数据库	SQLite	3.0+
语言	Python	3.10
环境管理	Anaconda	-
🗄️ 数据库设计
ER图
text
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  University │────<│  Department │────<│    Major    │
│  id (PK)    │     │  id (PK)    │     │  id (PK)    │
│  name       │     │  university_id(FK) │  dept_id(FK)│
│  short_name │     │  name       │     │  name       │
│  location   │     │  code       │     │ total_credits│
└─────────────┘     └─────────────┘     └──────┬──────┘
                                                 │
                                                 │
                    ┌────────────────────────────┼────────────────────────────┐
                    │                            │                            │
                    ▼                            ▼                            ▼
          ┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
          │   MajorCourse   │          │     Course      │          │  CoursePrereq   │
          │   id (PK)       │          │   id (PK)       │          │   id (PK)       │
          │   major_id(FK)  │──────────│   course_code   │          │   course_id(FK) │
          │   course_id(FK) │          │   name          │          │   prereq_id(FK) │
          │   is_required   │          │   credits       │          │   type          │
          │   semester      │          │   hours         │          └─────────────────┘
          └─────────────────┘          │   course_type   │
                                       └─────────────────┘
核心表结构
表名	说明	主键	外键
university	大学信息	id	-
department	学院信息	id	university_id
major	专业信息	id	dept_id
course	课程信息	id	-
major_course	专业-课程关联表	id	major_id, course_id
约束设计
主键：各表的 id 字段，自增整数

外键：保证数据引用完整性，级联删除

唯一约束：university.name、(university_id, department.name)、(major_id, course_id)

检查约束：credits > 0、hours >= 0

💻 环境要求
Python 3.9 或更高版本

Anaconda（推荐，用于环境管理）

SQLite（Python内置）

操作系统：Windows / macOS / Linux

🚀 安装与运行
1. 克隆仓库
bash
git clone https://github.com/42411079/curriculum_system.git
cd curriculum_system
2. 创建并激活虚拟环境
bash
conda create -n curriculum python=3.10 -y
conda activate curriculum
3. 安装依赖
bash
pip install fastapi uvicorn sqlalchemy
4. 初始化数据库
bash
python scripts/init_db.py
预期输出：

text
✅ 数据库表创建成功
✅ 创建大学: 西南财经大学
✅ 创建 13 个学院
✅ 创建 39 个专业
✅ 导入 61 门课程
5. 导入上海财经大学数据
bash
python scripts/import_sufe.py
6. 启动服务
bash
python run.py
预期输出：

text
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
7. 访问API文档
打开浏览器访问：http://localhost:8000/docs

📡 API接口列表
接口	方法	说明
/queries/major/{id}/required-courses	GET	查询专业必修课
/queries/course/{identifier}	GET	查询课程学分学时
/queries/major/{id}/total-credits	GET	查询专业总学分
/queries/course/{identifier}/majors	GET	查询开设课程的专业
/queries/department/{id}/overview	GET	查询学院专业概览
/queries/courses/search	GET	关键词搜索课程
/compare/major-courses	GET	跨校对比课程
/compare/total-credits	GET	跨校对比学分
/nl/query	POST	自然语言查询
🧪 测试示例
1. 查询计算机专业必修课
bash
GET /queries/major/1/required-courses
2. 查询课程信息
bash
GET /queries/course/数据结构
3. 关键词搜索
bash
GET /queries/courses/search?keyword=数据
4. 跨校对比
bash
GET /compare/major-courses?major_name=计算机科学与技术
5. 自然语言查询
bash
POST /nl/query
question=计算机科学与技术专业有哪些必修课
📊 数据统计
实体	数量
🏛️ 大学	2所
📚 学院	15个
🎓 专业	39个
📖 课程	61门
🔗 专业-课程关联	120+条
📁 项目结构
text
curriculum_system/
├── 📄 run.py                      # 启动入口
├── 📁 app/
│   ├── 📁 api/
│   │   ├── 📄 queries.py          # 基础查询接口
│   │   ├── 📄 compare.py          # 跨校对比接口
│   │   └── 📄 nl_query.py         # 自然语言查询接口
│   ├── 📁 core/
│   │   ├── 📄 config.py           # 配置文件
│   │   └── 📄 database.py         # 数据库连接
│   └── 📁 models/
│       └── 📄 models.py           # 数据模型
├── 📁 scripts/
│   ├── 📄 init_db.py              # 数据库初始化
│   └── 📄 import_sufe.py          # 上海财大数据导入
├── 📁 data/
│   └── 📄 sufe_data.json          # 上海财大JSON数据
└── 📄 curriculum.db               # SQLite数据库
👨‍💻 作者
GitHub：@42411079

📄 许可证
本项目采用 MIT License 开源许可证。
