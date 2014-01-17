class Test1(object):

    def index(self, request):
        return { 'called' : 'index' }

    def show(self, request):
        id = request.args['id'] 
        return { 'called' : 'show', 'id' : id }
