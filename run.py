# run.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import queries, compare, nl_query

app = FastAPI(
    title="培养方案数据库系统",
    version="1.0.0",
    description="""
    ## 西南财经大学人才培养方案数据库系统
    
    ### 子模块A：基础查询功能
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
    """
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册所有路由
app.include_router(queries.router)      # 基础查询接口
app.include_router(compare.router)      # 跨校对比接口
app.include_router(nl_query.router)     # 自然语言查询接口

@app.get("/")
async def root():
    return {
        "message": "培养方案数据库系统API",
        "version": "1.0.0",
        "modules": {
            "基础查询": "/api/queries",
            "跨校对比": "/api/compare",
            "自然语言查询": "/api/nl/query"
        },
        "endpoints": {
            "专业必修课": "/api/queries/major/{major_id}/required-courses",
            "课程信息": "/api/queries/course/{course_code}",
            "专业总学分": "/api/queries/major/{major_id}/total-credits",
            "开设课程的专业": "/api/queries/course/{course_code}/majors",
            "学院专业概览": "/api/queries/department/{dept_id}/overview",
            "课程搜索": "/api/queries/courses/search?keyword=数据",
            "专业列表": "/api/queries/majors",
            "学院列表": "/api/queries/departments",
            "跨校对比-课程": "/api/compare/major-courses?major_name=计算机科学与技术",
            "跨校对比-学分": "/api/compare/total-credits?major_name=计算机科学与技术",
            "自然语言查询": "POST /api/nl/query?question=计算机专业有哪些必修课"
        }
    }

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)