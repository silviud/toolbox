#!/usr/bin/python 
class nagiosEval:
    """ called with warning, critical, match and value to compare
        example:
            import urllib, simplejson
            from nagiosEval import nagiosEval
            data = simplejson.load(urllib.urlopen("http://someurl/somejsonservlet"))
            obj = "SomeJsonField" 
            w = int(50)
            c = int(100)
            m = None
            result = nagiosEval(object=obj, value=data[obj], warning=w, critical=c, match=m)
            exitcode, statusmsg = result.evaluate()
            
            Supported Types:
            nagiosEval(object=str, value=(str|int|float), warning=(int|float), critical=(int|float), match=(int|float|str))
            
            remember to type your warning / critical  as float / int before calling!
    """
    
    def __init__(self,**kwargs):
        #print kwargs
        self.kwargs = kwargs
        self.match = None
        self.warning = None
        self.critical = None
        
        try:
            self.object = self.kwargs['object']
            try:
                self.value = self.kwargs['value']
                try:
                    self.warning = self.kwargs['warning']
                except:
                    pass
                try:
                    self.critical = self.kwargs['critical']
                except:
                    pass
                try:
                    self.match = self.kwargs['match']
                except:
                    pass
            except Exception, e:
                raise
        except Exception, e:
            raise
       
        
    def evaluate(self):                     
        try:
            if self.match:
                if str(self.value).encode('utf-8') != self.match.encode('utf-8'):
                   return 2, "CRITICAL: " + str(self.value)
                else:
                    return 0, "OK: " + str(self.value)
            elif self.warning > self.critical:
                if self.value < self.warning:
                   return 1, "WARNING: " + str(self.value) 
                else:
                   return 0, "OK: " + str(self.value)
        
        except ValueError, e:
            print "ERROR, match or warning / critical not in acceptable format"
            return 3, str(e)
 
