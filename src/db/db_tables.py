from sqlalchemy import  String, Column, Date, ForeignKey
from sqlalchemy.orm import relationship

from .engine import Base



class WelderTable(Base):
    __tablename__ = "welders_table"
    kleymo = Column(String(4), primary_key=True)
    full_name = Column(String(), nullable=True)
    birthday = Column(Date(), nullable=True)
    passport_id = Column(String(), nullable=True)
    certifications = relationship("WelderCertificationTable", backref="welder")
    ndts = relationship("NDTSummaryTable", backref="welder")



class WelderCertificationTable(Base):
    __tablename__ = "certifications_table"
    kleymo = Column(String(4), ForeignKey("welders_table.kleymo"))
    certification_id = Column(String(), nullable=False, primary_key=True)
    job_title = Column(String(), nullable=True)
    certification_number = Column(String(), nullable=True)
    certification_date = Column(Date(), nullable=True)
    expiration_date = Column(Date(), nullable=True)
    renewal_date = Column(Date(), nullable=True)
    insert = Column(String(), nullable=True)
    certification_type = Column(String(), nullable=True)
    company = Column(String(), nullable=True)
    gtd = Column(String(), nullable=True)
    method = Column(String(), nullable=True)
    details_type = Column(String(), nullable=True)
    joint_type = Column(String(), nullable=True)
    groups_materials_for_welding = Column(String(), nullable=True)
    welding_materials = Column(String(), nullable=True)
    details_thikness = Column(String(), nullable=True)
    outer_diameter = Column(String(), nullable=True)
    welding_position = Column(String(), nullable=True)
    connection_type = Column(String(), nullable=True)
    rod_diameter = Column(String(), nullable=True)
    rod_axis_position = Column(String(), nullable=True)
    weld_type = Column(String(), nullable=True)
    joint_layer = Column(String(), nullable=True)
    sdr = Column(String(), nullable=True)
    automation_level = Column(String(), nullable=True)
    details_diameter = Column(String(), nullable=True)
    welding_equipment = Column(String(), nullable=True)



class NDTSummaryTable(Base):
    __tablename__ = "ndt_summary"
    
    sicil_number = Column(String(), nullable=True)
    kleymo = Column(String(4), ForeignKey("welders_table.kleymo"))
    birthday = Column(Date(), nullable=True)
    passport_number = Column(String(), nullable=True)
    nation = Column(String(), nullable=True)
    comp = Column(String(), nullable=True)
    subcon = Column(String(), nullable=True)
    project = Column(String(), nullable=True)
    latest_welding_date = Column(Date(), nullable=True)
    total_weld_1 = Column(String(), nullable=True)
    total_ndt_1 = Column(String(), nullable=True)
    total_accepted_1 = Column(String(), nullable=True)
    total_repair_1 = Column(String(), nullable=True)
    repair_status_1 = Column(String(), nullable=True)
    total_weld_2 = Column(String(), nullable=True)
    total_ndt_2 = Column(String(), nullable=True)
    total_accepted_2 = Column(String(), nullable=True)
    total_repair_2 = Column(String(), nullable=True)
    repair_status_2 = Column(String(), nullable=True)
    total_weld_3 = Column(String(), nullable=True)
    total_ndt_3 = Column(String(), nullable=True)
    total_accepted_3 = Column(String(), nullable=True)
    total_repair_3 = Column(String(), nullable=True)
    repair_status_3 = Column(String(), nullable=True)
    ndt_id = Column(String(), primary_key=True)



class NDTTable(Base):
    __tablename__ = "ndt"
    
    sicil_number = Column(String(), nullable=True)
    kleymo = Column(String(4), ForeignKey("welders_table.kleymo"))
    birthday = Column(Date(), nullable=True)
    passport_number = Column(String(), nullable=True)
    nation = Column(String(), nullable=True)
    comp = Column(String(), nullable=True)
    subcon = Column(String(), nullable=True)
    project = Column(String(), nullable=True)
    latest_welding_date = Column(Date(), nullable=True)
    total_weld_1 = Column(String(), nullable=True)
    total_ndt_1 = Column(String(), nullable=True)
    total_accepted_1 = Column(String(), nullable=True)
    total_repair_1 = Column(String(), nullable=True)
    repair_status_1 = Column(String(), nullable=True)
    total_weld_2 = Column(String(), nullable=True)
    total_ndt_2 = Column(String(), nullable=True)
    total_accepted_2 = Column(String(), nullable=True)
    total_repair_2 = Column(String(), nullable=True)
    repair_status_2 = Column(String(), nullable=True)
    total_weld_3 = Column(String(), nullable=True)
    total_ndt_3 = Column(String(), nullable=True)
    total_accepted_3 = Column(String(), nullable=True)
    total_repair_3 = Column(String(), nullable=True)
    repair_status_3 = Column(String(), nullable=True)
    ndt_id = Column(String(), primary_key=True)
