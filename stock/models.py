from django.db import models

class user(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=32,unique=True)
    pwd = models.CharField(max_length=32) 
    status = models.IntegerField(max_length=1)
    cash = models.FloatField(max_length=4)
    ip = models.CharField(max_length=16)
    date_lastlogin = models.DateTimeField() 
    date_create = models.DateTimeField()
    
    def __unicode__(self):
        return "%s %d %f %s %s %s" % (self.userid,self.status,self.cash,self.ip,self.date_lastlogin,self.date_create)
    
class log(models.Model):
    id = models.AutoField(primary_key=True)
    
    
    operation = models.IntegerField(max_length=1)
    
    code = models.CharField(max_length=16)
    num = models.IntegerField(max_length=4)
    price = models.FloatField(max_length=4)
    
    date_create = models.DateTimeField()
    def __unicode__(self):
        return "%d %s %d %f" % (self.operation,self.code,self.num,self.price)
    
class stocks(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(user)
    
    code = models.CharField(max_length=16)
    num = models.IntegerField(max_length=4)
    price = models.FloatField(max_length=4)
    
    date_create = models.DateTimeField()
    
    def __unicode__(self):
        return "%s %d %f %s" % (self.code,self.num,self.price,self.date_create)
    
class watch(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(user)
    
    code = models.IntegerField(max_length=4)

    def __unicode__(self):
        return "%d" % (self.code)
