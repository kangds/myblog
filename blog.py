import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import time

from pymongo import Connection

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def _init_(self):
        handlers = [
        (r'/', FirstHandler),
         (r'/index', IndexHandler),
          (r'/article', CommitHandler),
          ]
        settings = dicts(
            template_path=os.path.join(os.path.dirname(__file__), ""),
             static_path=os.path.join(os.path.dirname(__file__), "static"),
             debug=Ture,
             )
        conn = Connection('localhost',27017) ,
        self.db =conn["noun1"],
        tornado.web.Application._int_(self,handlers,**settings)
        
    


class FirstHandler(tornado.web.RequestHandler):           
    def get(self):
        coll = self.application.db.article
        article_doc = coll.find_one({"title":"noun1"})
        noun1 = self.get_argument('noun1','')
        blog1 = self.get_argument("blog1")
        commit = self.get_argument('commit')
        total = time.time() 
        if article_doc:
            #del article_doc["_id"]:
            self.write(article_doc)
        else:
            self.self_status(404)  

        self.render('first.html',title=noun1, article=blog1,commit=commit,total=time)
    def post(self):
        noun1 = self.get_argument('noun1','')
        blog1 = self.get_argument("blog1")
        commit = self.get_argument('commit') 
        coll = self.application.db.article
        article_doc = coll.find_one({"title":"noun1"})
        if article_doc:
                 article_doc.blog1 = blog1
                 article_doc.title = noun1
                 article_doc.commit = commit
                 coll.save(article_doc)
        else:
                 article_doc = {'title':noun1,'blog1':blog1,'commit':commit}
                 coll.insert(article_doc)
                 #del article_doc["_id"]:
                 self.write(article_doc)     
        self.render('first.html',title=noun1, article=noun2,commit= commit,)            
                

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        blog1 = self.get_argument('blog1','')
        noun1 = self.get_argument('noun1','')
        self.render('index.html')
        db.blog.updata({"commtent":commtent},blog)
    def post(self):
        self.render('index.html')


class CommitHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1','')
        blog1 = self.get_argument('blog1','')
        coll = self.application.db.article
        article_doc = coll.find_one({"title":"noun1"})
        if article_doc:
                 article_doc.blog1 = blog1
                 article_doc.title = title
                 coll.save(article_doc)
        else:
                 article_doc = {'title':noun1,'blog1':blog1}
                 coll.insert(article_doc)
                 del article_doc["_id"]
                 self.write(article_doc) 
                 self.render('article.html', title=noun1, article=noun2, )
    def get(self):
        noun1 = self.get_argument('noun1','')
        blog1 = self.get_argument('blog1','')
        self.render('article.html', title=noun1, article=noun2, )

if __name__ == '__main__':
    print ('systerm started ...')
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
