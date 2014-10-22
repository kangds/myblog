# -*- coding: UTF-8 -*-

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from pymongo import Connection

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
        (r'/', FirstHandler),
        (r'/index', IndexHandler),
        (r'/article', CommitHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), ""),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,        
     ) 
     #定义settings字典

        #conn = Connection("localhost",27017) ,
        conn = Connection()
        self.db = conn ["blog"]
        #self.db.blog =conn["noun1"]
        tornado.web.Application.__init__(self,handlers,**settings)
        
    
class FirstHandler(tornado.web.RequestHandler):           
    def get(self):
        coll = self.application.db.blog
        article_doc = coll.find()
        self.render('first.html',article_doc=article_doc)

    def post(self):
        noun1 = self.get_argument('noun1','')
        blog1 = self.get_argument("blog1",'')
        commit = self.get_argument('commit','') 
        coll = self.application.db.blog
        article_doc = coll.find_one({"title":"noun1"})
        if article_doc:
                 article_doc.article = blog1
                 article_doc.title = noun1
                 article_doc.commit = commit
                 coll.save(article_doc)
        else:
                 article_doc = {'title':noun1,'article':blog1,'commit':commit}
                 coll.insert(article_doc)
                 del article_doc["_id"]
                 self.write(article_doc)     
        self.render('first.html',title=noun1, article=blog1,commit= commit,)            
                

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        coll = self.application.db.blog
        article_doc = coll.find_one({"title":"noun1"})
        blog1 = self.get_argument('blog1','')
        noun1 = self.get_argument('noun1','')
        self.render('index.html',title=noun1,article=blog1)
    def post(self):
        coll = self.application.db.blog
        article_doc = coll.find_one({"title":"noun1"})
        blog1 = self.get_argument('blog1','')
        noun1 = self.get_argument('noun1','')
        self.render('index.html',title=noun1,article=blog1)


class CommitHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1','')
        blog1 = self.get_argument('blog1','')
        commit = self.get_argument('commit','')
        coll = self.application.db.blog
        article_doc = coll.find_one({"title":noun1})
        if article_doc:
                 article_doc['article'] = blog1
                 article_doc['title'] = noun1
                 article_doc ['commit'] = commit
                 coll.save(article_doc)
                 print coll
                 self.redirect('/')
        else:
                 article_doc = {'title':noun1,'article':blog1,'commit':commit}
                 coll.insert(article_doc)
                 # del article_doc["_id"]
                 self.render('article.html', title=noun1, article=blog1,commit=commit )
    def get(self):
        noun1 = self.get_argument('noun1','')
        blog1 = self.get_argument('blog1','')
        commit = self.get_argument('commit','')
        self.render('article.html', title=noun1, article=blog1, commit=commit)

if __name__ == '__main__':
    print ('systerm started ...')
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
