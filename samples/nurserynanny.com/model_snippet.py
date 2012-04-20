assignment_table = sa.Table("assignments", meta.metadata,
    sa.Column("id", sa.Integer, primary_key=True),                        
    sa.Column("profile_id", sa.Integer, sa.ForeignKey('profiles.id')),
    sa.Column("event_id", sa.Integer, sa.ForeignKey('events.id')),                        
    sa.Column("withdrawn_at", UTCDateTime),
    sa.Column("published_at", UTCDateTime),
    sa.Column("hash", sa.String(32)),
    sa.Column("auto_assignment_id", sa.Integer, sa.ForeignKey('auto_assignments.id')),
    sa.Column("emailed_at", UTCDateTime),
    sa.Column("reminded_at", UTCDateTime),
    sa.Column("accepted_at", UTCDateTime)
    )
    
class AssignmentExtension(orm.interfaces.MapperExtension):
    """Creates a.hash on first INSERT of Assignment a."""
    def after_insert(self, mapper, connection, instance):
        hash = hashlib.md5(str(instance.profile.id) +
                           instance.profile.account.email +
                           str(instance.event.id)).hexdigest()
        t = mapper.local_table
        connection.execute(t.update().where(and_(t.c.event_id==instance.event.id,
                                                 t.c.profile_id==instance.profile.id)).values(hash=hash))
        return orm.EXT_CONTINUE
        
orm.mapper(Assignment, assignment_table, extension=AssignmentExtension(), properties={
    'profile': orm.relation(Profile, backref='assignments'),
    'auto_assignment': orm.relation(AutoAssignment, backref='assignments')
})