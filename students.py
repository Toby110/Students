#coding=utf-8
import tornado.web
import tornado.ioloop
import asyncio
import SqlDb as db
import json
settings = {
    "template_path": "template",
    "static_path": "static",
    "debug": "true",
}
sql = {
    "create": "create table if not exists whlxx(id text,name text,class text,age text)",
    "insert": "insert into whlxx(id,name,class,age) values(?,?,?,?)",
    "delete": "delete from whlxx where id=id",
    "update": "update whlxx set name="" where age=18",
    "squery": "select * from whlxx",
}


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        sdb = db.Mysql('students.db')
        s = sql['create']
        sdb.create_table(s)
        s = sql['squery']
        data = sdb.show(s)
        sdb.close()
        self.render('index.html', data=data)
    def post(self):
        post_data = self.request.body_arguments
        #post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        result=[]
        for x in post_data.keys():
            result.append(post_data.get(x)[0].decode("utf-8"))
        data=[tuple(result)]
        sdb = db.Mysql('students.db')
        s = sql['insert']
        sdb.add(s, data)
        sdb.close()

class DelHandler(tornado.web.RequestHandler):
    def post(self):
        post_data=self.request.body_arguments
        id=post_data['id'][0].decode("utf-8")
        sdb = db.Mysql('students.db')
        s = f"delete from whlxx where id={id}"
        sdb.rem(s)
        sdb.close()

       


def make_app():
    return tornado.web.Application([
        (r'/', IndexHandler),
        (r'/del', DelHandler),
    ], **settings
    )


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
