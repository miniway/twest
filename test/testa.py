
class TestA(object):

    CONTENT_TYPE = 'application/xml'

    def index(self, request):
        return { 'TestA'  : request.args.get('test1_id','orphan') }

    def show(self, request):
        return  {'root':
                    {'TestA show'  : request.args.get('test1_id','no_parent'),
                     'TestA show2'  : request.args['id'] }
                   }
