# New models to append to models.py

class OrganizationalUnit(Base):
    __tablename__ = "organizational_units"

    id = Column(String, primary_key=True, default=generate_uuid)
    institution_id = Column(String, ForeignKey("institutions.id"))
    parent_id = Column(String, ForeignKey("organizational_units.id"), nullable=True)
    unit_type = Column(String, nullable=False)  # Enum: UnitType
    name = Column(String, nullable=False)
    code = Column(String, nullable=True)
    revenue = Column(Integer, default=0)  # 매출
    headcount = Column(Integer, default=0)  # 인원

    institution = relationship("Institution", back_populates="organizational_units")
    parent = relationship("OrganizationalUnit", remote_side=[id], backref="children")

class TaskDependency(Base):
    __tablename__ = "task_dependencies"

    id = Column(String, primary_key=True, default=generate_uuid)
    source_task_id = Column(String, ForeignKey("job_tasks.id"))
    target_task_id = Column(String, ForeignKey("job_tasks.id"))
    dependency_type = Column(String, default=DependencyType.RELATED)

    source_task = relationship("JobTask", foreign_keys=[source_task_id], back_populates="source_dependencies")
    target_task = relationship("JobTask", foreign_keys=[target_task_id], back_populates="target_dependencies")

class JobImprovement(Base):
    __tablename__ = "job_improvements"

    id = Column(String, primary_key=True, default=generate_uuid)
    job_id = Column(String, ForeignKey("jobs.id"))
    current_job_description = Column(Text, nullable=True)
    improvement_suggestion = Column(Text, nullable=False)
    status = Column(String, default=ImprovementStatus.PROPOSED)
    created_by = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
