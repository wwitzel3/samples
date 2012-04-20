class AssignmentsController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('assignment', 'assignment')
    
    def update(self, id):
        """PUT /assignment/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('assignment', id=ID),
        #           method='put')
        # url('assignment', id=ID)
        c.profile = auth.profile_from_session()
        try:
            assignment = meta.Session.query(Assignment).filter_by(hash=id).one()
        except NoResultFound, e:
            c.message = 'No matching assignment was found.'
            return render('/assignment/exception.html')
        except MultipleResultsFound, e:
            c.message = 'Multiple matching assignments was found. Someone should do something.'
            return render('/assignment/exception.html')
    
        action = request.params.get('action', None)
        if action == 'remove':
            assignment.withdraw()
            c.message = 'You are no longer scheduled for this event.'
        elif action == 'signup':
            profile_hash = request.params.get('profile', None)
            profile = meta.Session.query(Profile).filter_by(hash=profile_hash).one()
            assignment.profile = profile
            assignment.accept()
            # user just clicked signup - i don't think we need to send an email here
            # they'll still get the reminder email
            #AssignmentNotificationEmail([assignment]).queue()
            c.message = 'You have been assigned to this event. Thank you!'
        elif action == 'accept':
            assignment.accept()
            c.message = 'Assignment accepted. Thank you!'
            
        c.event = assignment.event
        meta.Session.commit()
        return render('/assignment/update.html')