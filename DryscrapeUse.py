import webkit_server
import dryscrape

class wrapDryscrape(object):
    def __init__(self, baseUrl, imageLoad = True, loginUrl = 0, username = 0, userpassword = 0):
        self.__baseUrl = baseUrl
        self.__loginUrl = loginUrl
        self.__username = username
        self.__userpassword = userpassword
        self.__relogCounter = 0
        self.__server = None
        self.__session = None
        self.__imageLoad = imageLoad
        self.__login()

    def __baseLogin(self):
        if self.__server is not None:
            self.__server.kill()
        if self.__server is None:
            dryscrape.start_xvfb()
        self.__server = webkit_server.Server()
        server_conn = webkit_server.ServerConnection(server=self.__server)
        driver = dryscrape.driver.webkit.Driver(connection=server_conn)
        self.__session = dryscrape.Session(driver=driver)
        if not self.__imageLoad:
            self.__session.set_attribute('auto_load_images', False)
        self.__session.wait_timeout = 20
        if (self.__loginUrl != 0):
            self.__session.visit(self.__loginUrl)
            name = self.__session.at_xpath('//*[@name="username"]')
            name.set(self.__username)
            password = self.__session.at_xpath('//*[@name="password"]')
            password.set(self.__userpassword)
            name.form().submit()
        self.__relogCounter = 0
    
    def __visit(self, *specification):
        trys = 1
        if (self.__relogCounter >= 10):
            self.__login()
        while (trys < 10):
            try:
                self.__session.visit(self.__baseUrl.format(*specification))
                self.__relogCounter += 1
                break
            except:
                trys += 1
                self.__login()
                self.__relogCounter = 0
                if (trys >= 10):
                    raise NoVisit(self.__baseUrl.format(*specification))

    def __login(self):
        loginTrys = 1
        self.__session = None
        while self.__session is None:
            try:
                self.__baseLogin()
            except:
                if (loginTrys >= 10):
                    raise NoLogin(self.__loginUrl)
                loginTrys += 1
        self.__relogCounter = 0

    def grepCode(self, *specification):
        self.__visit(*specification)
        response = self.__session.body()
        code = response.encode('ascii','ignore') 
        return(code)

class NoLogin(BaseException):
    def __init__(self, loginUrl):
        self.loginUrl = loginUrl

    def str(self):
        return u"No login on {loginUrl} possible".format(loginUrl = self.loginUrl)

class NoVisit(BaseException):
    def __init__(self, url):
        self.url = url

    def str(self):
        return u"Can't get Code from {url}".format(url = self.url)

