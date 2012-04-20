class DiaryLoggingMapperExtension(orm.MapperExtension):
    def before_update(self, mapper, connection, instance):
        old_select = instance.__table__.select(instance.__table__.c.c_diary_taskid == instance.id)
        old_values = connection.execute(old_select).fetchone()
        new_values = instance.__dict__.copy()
        DiaryLog.log(old_values, new_values)
        
        return orm.EXT_CONTINUE

class Diary(Base):
    __tablename__ = 'c_diary'
    __table_args__ = (
        ForeignKeyConstraint(['c_diary_dept', 'c_diary_ref'],
                             ['secuadmin.ent_entity_master_tbl.ent_entity_type', 'secuadmin.ent_entity_master_tbl.ent_entity_id']), # secuadmin, secuadmin
        ForeignKeyConstraint(['c_diary_dept', 'c_diary_tasktype'], ['clmsadmin.c_drtask.c_diary_dept', 'clmsadmin.c_drtask.c_diary_tasktype']), # clmsadmin, clmsadmin
        ForeignKeyConstraint(['c_diary_notepad_key_seq', 'c_diary_notepad_no', 'c_diary_note_topic_seq'],
                             ['secuadmin.not_text_master_tbl.not_note_key_seq', 'secuadmin.not_text_master_tbl.not_notepad_num', 'secuadmin.not_text_master_tbl.not_note_topic_seq']), # secuadmin, secuadmin
        {'schema':'clmsadmin'} # clmsadmin
    )
    __mapper_args__ = {'extension': DiaryLoggingMapperExtension()}
    
    id = Column(u'c_diary_taskid', String(length=10), sa.schema.Sequence('c_diary_taskid_seq', optional=False), primary_key=True, nullable=False)
    entity_id = Column('c_diary_ref', String(length=10), nullable=False)
    user_id = Column('c_diary_user', Integer, ForeignKey('clmsadmin.c_user.cus_id')) # clmsadmin
    seq = Column(u'c_diary_seq', Integer, nullable=False)
    comment = Column('c_diary_comment', String(length=60))
    history = Column('c_diary_history', String(length=1))
    
    diary_dept = Column('c_diary_dept', String(length=3))
    diary_task_type = Column('c_diary_tasktype', String(length=20))