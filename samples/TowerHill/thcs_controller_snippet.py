class NoteController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('note', 'note')
    
    @jsonify
    def index(self, format='json'):
        """GET /note: All items in the collection"""
        # url('note')
        
        try:
            form_result = forms.NoteGetForm.to_python(request.params)
        except formencode.validators.Invalid, error:
            return {'results':0, 'status':Status.ERROR, 'type':ErrorType.FORMENCODE, 'message':'invalid: %s' % error}
        
        user = meta.Session.query(User).get(form_result.get('user_id'))
        if not user:
            return {'results':0, 'status':Status.ERROR, 'type':ErrorType.DATABASE, 'message':'No user found for ID (%s)' % form_result.get('user_id')}

        entity = meta.Session.query(Entity).get((form_result.get('entity_type'), form_result.get('entity_id')))
        if not entity:
            return {'results':0, 'status':Status.ERROR, 'type':ErrorType.DATABASE, 'message':'No entity found for ID (%s)' % (form_result.get('entity_id'))}
  
        authorized_types = user.permissions.filter_by(entity_type=form_result.get('entity_type')).filter_by(view_note_ind='Y') 
        
        notes = meta.Session.query(Note).filter_by(notepad_num=entity.notepad_num).filter(Note.type.in_(at.notepad_type for at in authorized_types))
        if form_result.get('topic_seq'):
            notes = notes.filter_by(topic_seq=form_result.get('topic_seq'))
        if form_result.get('note_seq'):
            notes = notes.filter_by(note_seq=form_result.get('note_seq'))
        notes = notes.order_by(Note.date.desc()).order_by(Note.time.desc())
            
        response_result = {'results': notes.count(), 'rows': []}
        for note in notes:
            response_result['rows'].append({
                'id':note.id,
                'tseq':note.topic_seq,
                'entity_id':entity.id,
                'nseq':note.note_seq,
                'name':note.author.name(),
                'date':tools.gettime(note.date, note.time),
                'type':note.type_desc,
                'topic':note.topic.description,
                'text':note.text.replace('\n','<br/>'), # TODO: better solution for this
                'attachments': [
                     {'id':document.key, 'desc': document.description}
                     for document in note.documents
                 ]
            })   
        return response_result