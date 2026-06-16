```markdown
# 培养方案数据库系统

西南财经大学2024级本科人才培养方案数据库系统

## 项目简介

本项目针对西南财经大学2024级本科生人才培养方案，设计并实现了一个完整的培养方案数据库系统。系统包含两个子模块：子模块A实现了培养方案数据的存储及6项核心查询功能；子模块B整合了上海财经大学培养方案数据，实现了跨校对比分析和自然语言查询接口。

## 功能列表

### 子模块A：基础查询
- 查询某专业的必修课列表
- 查询某门课程的学分、学时信息
- 查询某专业的总学分要求
- 查询开设某门课程的所有专业
- 查询某学院下所有专业的培养方案概览
- 关键词模糊搜索课程名称

### 子模块B：跨校对比分析
- 对比两校同一专业的课程设置异同
- 对比两校同一专业的总学分要求

### 子模块C：自然语言查询
- 用户可用中文提问，系统自动返回查询结果
  - 例如："计算机科学与技术专业有哪些必修课"
  - 例如："数据结构课程有多少学分"
  - 例如："对比计算机科学与技术专业"

## 技术栈

| 层级 | 技术 |
|------|------|
| Web框架 | FastAPI |
| ORM | SQLAlchemy |
| 数据库 | SQLite |
| 语言 | Python 3.10 |

## 数据库设计

### ER图

```
University ──< Department ──< Major ──< MajorCourse >── Course
```

### 核心表结构

| 表名 | 说明 |
|------|------|
| university | 大学信息 |
| department | 学院信息 |
| major | 专业信息 |
| course | 课程信息 |
| major_course | 专业-课程关联表 |

## 环境要求

- Python 3.9+
- Anaconda（推荐）
- SQLite（Python内置）

## 安装与运行

### 1. 克隆仓库

```bash
git clone https://github.com/42411079/curriculum_system.git
cd curriculum_system
```

### 2. 创建并激活虚拟环境

```bash
conda create -n curriculum python=3.10 -y
conda activate curriculum
```

### 3. 安装依赖

```bash
pip install fastapi uvicorn sqlalchemy
```

### 4. 初始化数据库

```bash
python scripts/init_db.py
```

### 5. 导入上海财经大学数据

```bash
python scripts/import_sufe.py
```

### 6. 启动服务

```bash
python run.py
```

### 7. 访问API文档

打开浏览器访问：http://localhost:8000/docs

## API接口列表

| 接口 | 方法 | 说明 |
|------|------|------|
| `/queries/major/{id}/required-courses` | GET | 查询专业必修课 |
| `/queries/course/{identifier}` | GET | 查询课程学分学时 |
| `/queries/major/{id}/total-credits` | GET | 查询专业总学分 |
| `/queries/course/{identifier}/majors` | GET | 查询开设课程的专业 |
| `/queries/department/{id}/overview` | GET | 查询学院专业概览 |
| `/queries/courses/search` | GET | 关键词搜索课程 |
| `/compare/major-courses` | GET | 跨校对比课程 |
| `/compare/total-credits` | GET | 跨校对比学分 |
| `/nl/query` | POST | 自然语言查询 |

## 测试示例

### 1. 查询计算机专业必修课
```
GET /queries/major/1/required-courses
```

### 2. 查询课程信息
```
GET /queries/course/数据结构
```

### 3. 关键词搜索
```
GET /queries/courses/search?keyword=数据
```

### 4. 跨校对比
```
GET /compare/major-courses?major_name=计算机科学与技术
```

### 5. 自然语言查询
```
POST /nl/query
question=计算机科学与技术专业有哪些必修课
```

## 数据统计

| 实体 | 数量 |
|------|------|
| 大学 | 2所 |
| 学院 | 15个 |
| 专业 | 39个 |
| 课程 | 61门 |
| 专业-课程关联 | 120+条 |

## 项目结构

```
curriculum_system/
├── run.py                      # 启动入口
├── app/
│   ├── api/
│   │   ├── queries.py          # 基础查询接口
│   │   ├── compare.py          # 跨校对比接口
│   │   └── nl_query.py         # 自然语言查询接口
│   ├── core/
│   │   ├── config.py           # 配置文件
│   │   └── database.py         # 数据库连接
│   └── models/
│       └── models.py           # 数据模型
├── scripts/
│   ├── init_db.py              # 数据库初始化
│   └── import_sufe.py          # 上海财大数据导入
├── data/
│   └── sufe_data.json          # 上海财大JSON数据
└── curriculum.db               # SQLite数据库
```

## 作者

- GitHub: [42411079](https://github.com/42411079)

## 许可证

MIT License
```

---

## 使用步骤

1. 打开您的GitHub仓库：
   https://github.com/42411079/curriculum_system

2. 点击 `README.md` 文件

3. 点击右上角的 ✏️ **铅笔图标**

4. **删除原有内容**，粘贴上面的完整内容

5. 点击页面底部的 **Commit changes...**

6. 选择 **Commit directly to the main branch**

7. 点击 **Commit changes**

完成后刷新页面，就能看到完整的README了！
