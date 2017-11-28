import unittest
from Menu import Main
from Usuario import Usuario
from prueba_orm import SetAll
from unittest.mock import Mock
from unittest.mock import MagicMock
from bs4 import BeautifulSoup
#~ from unittest.mock import patch
from StackEntryFeed import StackEntryFeed
from orm import *
import feedparser
import requests

class Testscraper(unittest.TestCase):
    
    def setUp(self):
        #~ self.u = MagicMock()
        self.mock_usuario = Mock(username = "Clemente", userid = 123,biografia = "Biografía", comunidades = "comunidades", linkusuario = "linkusuario", url = "https://stackoverflow.com/questions/16840409/how-to-list-containers-in-docker")
        self.u = Usuario(self.mock_usuario.url,self.mock_usuario.username,self.mock_usuario.userid)
        url_feed = './feed.xml'
        self.feedParser = feedparser.parse(url_feed)
        e = self.feedParser.entries            
        self.stackFeed = StackEntryFeed(e[0])
        self.m = Main
        self.orm = OrmFactory()
        self.mock_respuesta = Mock(idpregunta = 1234, respuesta = "Respuesta", fecha = "fecha", linkrespuesta = "linkrespuesta")
        self.mock_pregunta = Mock(question = "pregunta",explicacion = "Explicación",linkpregunta = "linkpregunta")

    #~ Pruebas unitarias del ORM
    def testORMFactoryAgregaUsuario(self):
        self.assertIsNone(self.orm.agregaUsuario(self.mock_usuario.username,self.mock_usuario.biografia,self.mock_usuario.comunidades,self.mock_usuario.userid,self.mock_usuario.linkusuario))
    
    def testORMFactoryAgregaRespuesta(self):
        self.assertIsNone(self.orm.agregaRespuesta(self.mock_respuesta.idpregunta,self.mock_respuesta.respuesta,self.mock_respuesta.fecha,self.mock_usuario.userid, self.mock_respuesta.linkrespuesta))
    
    def testORMFactoryAgregaPregunta(self):
        self.assertIsNone(self.orm.agregaPregunta(self.mock_respuesta.idpregunta,self.mock_pregunta.question,self.mock_pregunta.explicacion,self.mock_usuario.userid,self.mock_pregunta.linkpregunta))
    
    #~ Pruebas unitarias para la clase Usuario 
    def testUsuarioGetName(self):        
        self.assertEqual(self.u.get_username(), "Clemente")
    
    def testUsuarioGetId(self):
        self.assertEqual(self.u.get_userid(),123)
    
    def testUsuarioComunidades(self):
        self.assertEqual(self.u.get_comunidades(), [])
    
    def testStackEntryFeedGetUserName(self):
        self.assertEqual(self.stackFeed.get_username(),"w00t")
    
    def testStackEntryFeedGetEntryLink(self):
        self.assertEqual(self.stackFeed.get_entry_link(),"https://stackoverflow.com/q/16840409")
    
    def testStackEntryFeedGetId(self):
        self.assertEqual(self.stackFeed.get_id(),"16840409")
    
    def testStackEntryFeedGetSummaryDetail(self):
        self.assertIsInstance(self.stackFeed.get_summary_detail(),str)
    
    def testStackEntryFeedGetUserUri(self):
        self.assertEqual(self.stackFeed.get_user_uri(),"https://stackoverflow.com/users/124416")
    
    def testStackEntryFeedGetFechaPublicacion(self):
        self.assertEqual(self.stackFeed.get_fecha_publicacion(),"2013-05-30T15:41:46Z")
    
     #~ Pruebas de integración completa: caso 1: 
     #~ Probamos la aplicación con una página de stackoverflow, al ejecutarse correctamente devuelve None
    def test_scraper(self):
        self.assertIsNone(self.m.main(self,"https://stackoverflow.com/questions/16840409/how-to-list-containers-in-docker"))   
        
    #~ Pruebas de integración completa: caso 2: 
    #~ Cuando enviamos una página incorrecta nos arroja el error AttributeError
    def test_attr_error(self):
        with self.assertRaises(AttributeError):
            self.m.main(self, "https://docs.python.org/3/library/unittest.html")

        
if __name__ == '__main__':
    unittest.main()
    
    
    
