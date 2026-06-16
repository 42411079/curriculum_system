# app/models/models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class University(Base):
    __tablename__ = "university"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    short_name = Column(String(50))
    location = Column(String(100))
    website = Column(String(200))
    departments = relationship("Department", back_populates="university")

class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("university.id"), nullable=False)
    name = Column(String(100), nullable=False)
    code = Column(String(20))
    description = Column(Text)
    university = relationship("University", back_populates="departments")
    majors = relationship("Major", back_populates="department")

class Major(Base):
    __tablename__ = "major"
    id = Column(Integer, primary_key=True, index=True)
    dept_id = Column(Integer, ForeignKey("department.id"), nullable=False)
    name = Column(String(100), nullable=False)
    code = Column(String(20))
    total_credits = Column(Float, default=150.0)
    duration_years = Column(Integer, default=4)
    degree_type = Column(String(50))
    department = relationship("Department", back_populates="majors")
    major_courses = relationship("MajorCourse", back_populates="major", cascade="all, delete-orphan")

class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String(20), unique=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    english_name = Column(String(200))
    credits = Column(Float, nullable=False)
    hours = Column(Integer)
    course_type = Column(String(50))  # 必修/选修/限选
    category = Column(String(50))      # 通识课/专业课/实践课
    semester = Column(Integer)
    teaching_hours = Column(Integer)   # 课堂学时
    practice_hours = Column(Integer)   # 实践学时
    college = Column(String(100))
    major_courses = relationship("MajorCourse", back_populates="course", cascade="all, delete-orphan")

class MajorCourse(Base):
    __tablename__ = "major_course"
    id = Column(Integer, primary_key=True, index=True)
    major_id = Column(Integer, ForeignKey("major.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    is_required = Column(Boolean, default=True)
    recommended_semester = Column(Integer)
    major = relationship("Major", back_populates="major_courses")
    course = relationship("Course", back_populates="major_courses")
    __table_args__ = (UniqueConstraint('major_id', 'course_id', name='uq_major_course'),)