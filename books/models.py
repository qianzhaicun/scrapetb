# Create your models here.
from django.db import models

class DahlBookManager(models.Manager):
    def get_queryset(self):
        return super(DahlBookManager,self).get_queryset().filter(authors='AA')

class BookManager(models.Manager):
    def title_count(self,keyword):
        return self.filter(title__icontains=keyword).count()

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()
    
    class Meta:
        ordering = ["-name"]
    
    def __str__(self):
        return self.name
class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    salutation = models.CharField(max_length=10)
    
    def __str__(self):
        return '%s %s ' % (self.first_name,self.last_name)
class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()
    objects = BookManager()#默认的管理器
    dahl_objects = DahlBookManager()# 专门查询Dash的管理器
    
    def __str_(self):
        return self.title
        
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()

    def baby_boomer_status(self):
        import datetime
        if self.birth_date < datetime.date(1945,8,1):
            return "Pre-boomer"
        elif self.birth_date < datetime.date(1965,1,1):
            return "Baby boomer"
        else:
            return "Post-boomer"

    def _get_full_name(self):
        return '%s %s' % (self.first_name,self.last_name)
        
    full_name = property(_get_full_name)
    
class PollManager(models.Manager):
    def with_counts(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
        SELECT p.id, p.question, p.poll_date, COUNT(*)
FROM books_opinionpoll p, books_response r
WHERE p.id = r.poll_id
GROUP BY p.id, p.question, p.poll_date
ORDER BY p.poll_date DESC
        """)
        result_list=[]
        for row in cursor.fetchall():
            p = self.model(id=row[0],question=row[1],poll_date=row[2])
            p.num_responses = row[3]
            result_list.append(p)
        cursor.close()    
        return result_list
        
class OpinionPoll(models.Model):
    question = models.CharField(max_length=200)
    poll_date = models.DateField()
    objects = PollManager()
    
class Response(models.Model):
    poll = models.ForeignKey(OpinionPoll)
    person_name = models.CharField(max_length=50)
    response = models.TextField()
 
from django.db import connection
cursor = connection.cursor()
def dictfetchall(cursor):
    desc = cursor.description
    cursor.close() 
    return [
        dict(zip([col[0] for col in desc],row))
        for row in cursor.fetchall()
    ]
def getrawdict(sql):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute(sql)
    cursor.close() 
    return dictfetchall(cursor)
        




        