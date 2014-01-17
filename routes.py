
ROOT = '/v1/testapi'

RESOURCES = [
    ( 'test1' , 'test.test1.Test1', {}, [
        ('aa','test.testa.TestA' ) ,
        ('bb','test.testa.TestB' )
    ]),
    ( 'test2' , 'test.test1.Test2') ,  # /
    ( 'test3' , None, {}, [
        ('aa','test.testa.TestA' ) ,
        ('bb','test.testa.TestB' )
    ]),
]
