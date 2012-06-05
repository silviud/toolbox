#!/usr/bin/python 
"""
blurb: Nagios check output evaluation class as used in checkjsonURL.py
"""
class nagiosEval:
    """ called with warning, critical, match and value to compare
        example:
            from nagiosEval import nagiosEval
            data = 10
            w = int(50)
            c = int(100)
            m = None
            result = nagiosEval(value=data[obj], warning=w, critical=c, match=m)
            exitcode, statusmsg = result.evaluate()
            
            Supported Types:
            nagiosEval(value=(str|int|float), warning=(int|float|None), critical=(int|float|None), match=(int|float|str|None))
            
            remember to type your warning / critical  as float / int before calling!
    """
    
    def __init__(self,**kwargs):
        #print kwargs
        self.kwargs = kwargs
        self.match = None
        self.warning = None
        self.critical = None
        
        try:
            #self.object = self.kwargs['object']
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
                if self.value < self.critical:
                    return 2, "CRITICAL: " + str(self.value) 
                if self.value < self.warning:
                    return 1, "WARNING: " + str(self.value) 
                else:
                    return 0, "OK: " + str(self.value)
            elif self.critical > self.warning:
                if self.value < self.warning:
                    return 0, "OK: " + str(self.value)
                if self.value > self.critical:
                    return 2, "CRITICAL: " + str(self.value)
                if self.value > self.warning:
                    return 1, "WARNING: " + str(self.value)

        
        except ValueError, e:
            print "ERROR, match or warning / critical not in acceptable format"
            return 3, str(e)
 
