
class TestA(object):

    CONTENT_TYPE = 'application/xml'

    def index(self, request):
        return { 'TestA'  : request.args['test1_id'] }

    def show(self, request):
        return { 'TestA show'  : request.args['test1_id'], 
        'TestA show2'  : request.args['id'] }
