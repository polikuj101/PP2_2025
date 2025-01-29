class time:
    def __init__ (self,h,m,s):
        self.h = int(h)
        self.m = int(m)
        self.s = int(s)
    def __str__(self):
        if(self.m < 10):
            self.m = "0"+str(self.m)
        if(self.h < 10):
            self.h = "0"+str(self.h)
        if(self.s < 10):
            self.s = "0"+str(self.s)
        return f"{self.h}:{self.m}:{self.s}"
        
    def inc_sec(self,x):
        self.s = int(self.s) +x
        plus_m = 0
        plus_h = 0
        if(int(self.s) > 59):
            plus_m= int(plus_m) + int(self.s)//60
            self.s = int(self.s)%60
        self.m = int(self.m) + plus_m
        if(int(self.m) > 59):
            plus_h = int(plus_h) + int(self.m)//60
            self.m = int(self.m)%60
        if(int(self.h) > 23):
            self.h = int(self.h)%24
        
a = time(12,5,9)
print(a)
a.inc_sec(52)
print(a)
