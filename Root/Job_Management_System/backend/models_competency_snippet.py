
# --- 2.12 Competency Model ---
class Competency(Base):
    __tablename__ = "competencies"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True) # e.g. Technical, Leadership
    
    job_links = relationship("JobCompetency", back_populates="competency")
    user_links = relationship("UserCompetency", back_populates="competency")

class JobCompetency(Base):
    __tablename__ = "job_competencies"
    id = Column(String, primary_key=True, default=generate_uuid)
    job_position_id = Column(String, ForeignKey("job_positions.id"))
    competency_id = Column(String, ForeignKey("competencies.id"))
    required_level = Column(Integer, default=1) # 1-5
    weight = Column(Float, default=1.0)
    
    position = relationship("JobPosition", back_populates="required_competencies")
    competency = relationship("Competency", back_populates="job_links")

class UserCompetency(Base):
    __tablename__ = "user_competencies"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    competency_id = Column(String, ForeignKey("competencies.id"))
    current_level = Column(Integer, default=1) # 1-5
    evaluated_at = Column(Date, default=func.now())
    
    user = relationship("User", back_populates="competencies")
    competency = relationship("Competency", back_populates="user_links")
