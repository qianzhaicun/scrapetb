from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse,render_to_response
from django.template import RequestContext
from app01 import models
import json

from app01.forms import UserForm
from .models import Student,Classes
"""分页"""


from django.core.paginator import Paginator, EmptyPage,\
PageNotAnInteger

class CustomPaginator(Paginator):
    def __init__(self,current_page,per_pager_num,*args,**kwargs):
        # per_pager_num  显示的页码数量
        self.current_page = int(current_page)
        self.per_pager_num = int(per_pager_num)
        super(CustomPaginator,self).__init__(*args,**kwargs)
    def pager_num_range(self):
        '''
        自定义显示页码数
        第一种：总页数小于显示的页码数
        第二种：总页数大于显示页数  根据当前页做判断  a 如果当前页大于显示页一半的时候  ，往右移一下
                                                b 如果当前页小于显示页的一半的时候，显示当前的页码数量
        第三种：当前页大于总页数
        :return:
        '''
        if self.num_pages < self.per_pager_num:
            return range(1,self.num_pages+1)
 
        half_part = int(self.per_pager_num/2)
        if self.current_page <= half_part:
            return range(1,self.per_pager_num+1)
 
        if (self.current_page+half_part) > self.num_pages:
            return range(self.num_pages-self.per_pager_num+1,self.num_pages)
        return range(self.current_page-half_part,self.current_page+half_part+1)
        
 
def users(request):
    user_list = models.UserInfo.objects.all()
    return render(request,'app01/users.html',{'user_list':user_list})
 
 
def add_user(request):
    if request.method == 'GET':
        obj = UserForm()
        return render(request,'app01/add_user.html',{'obj':obj})
    else:
        obj = UserForm(request.POST)
        if obj.is_valid():
            models.UserInfo.objects.create(**obj.cleaned_data)
            return redirect('/students/users/')
        else:
            return render(request,'app01/add_user.html',{'obj':obj})
 
 
def edit_user(request,nid):
    if request.method == "GET":
        data = models.UserInfo.objects.filter(id=nid).first()
        obj = UserForm({'username':data.username,'email':data.email})
        return render(request,'app01/edit_user.html',{'obj':obj,'nid':nid})
    else:
        obj = UserForm(request.POST)
        if obj.is_valid():
            models.UserInfo.objects.filter(id=nid).update(**obj.cleaned_data)
            return redirect('/students/users/')
        else:
            return render(request,'app01/edit_user.html',{'obj':obj,'nid':nid})
            



def students(request):
    cls_list = models.Classes.objects.all()
    stu_list = models.Student.objects.all()
    pagenum = 10
    paginator = Paginator(stu_list, pagenum) # 3 posts in each page
    page = request.GET.get('page')

    try:
        stu_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        stu_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        stu_list = paginator.page(paginator.num_pages)

    return render(request,'app01/students.html',{'stu_list':stu_list,'cls_list':cls_list,'page': page,'pagenum':pagenum})
    
    
 
def add_student(request):
    response = {'status':True,'message': None,'data':None}
    try:
        u = request.POST.get('username')
        a = request.POST.get('age')
        g = request.POST.get('gender')
        c = request.POST.get('cls_id')
        obj = models.Student.objects.create(
            username=u,
            age=a,
            gender=g,
            cs_id=c
        )
        response['data'] = obj.id
    except Exception as e:
        response['status'] = False
        response['message'] = '用户输入错误'
 
    result = json.dumps(response,ensure_ascii=False)
    return HttpResponse(result)
 
def del_student(request):
    ret = {'status': True}
    try:
        nid = request.GET.get('nid')
        models.Student.objects.filter(id=nid).delete()
    except Exception as e:
        ret['status'] = False
    return HttpResponse(json.dumps(ret))
 
def edit_student(request):
    response = {'code':1000, 'message': None}
    try:
        nid = request.POST.get('nid')
        user = request.POST.get('user')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        cls_id = request.POST.get('cls_id')
        models.Student.objects.filter(id=nid).update(
            username=user,
            age=age,
            gender=gender,
            cs_id=cls_id
        )
    except Exception as e:
        response['code'] = 1001
        response['message'] = str(e)
    return HttpResponse(json.dumps(response))
 
 
def test_ajax_list(request):
    print(request.POST.getlist('k'))
    return HttpResponse('...')
    
    
    
def export_xls(request):
    fields = ["id", "username", "age", "gender", "cs"]
    queryset = Student.objects.all()
    try:
        return export_xlwt(Student, queryset.values_list(*fields), fields)
    except Exception as e:
        raise e


def export_xlwt(model, values_list, fields):
    import xlwt
    from datetime import datetime, date
    modelname = model._meta.verbose_name_plural.lower()
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet(modelname)

    default_style = xlwt.Style.default_style
    datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
    date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')

    for j, f in enumerate(fields):
        sheet.write(0, j, fields[j])

    for row, rowdata in enumerate(values_list):
        for col, val in enumerate(rowdata):
            if isinstance(val, datetime):
                style = datetime_style
            elif isinstance(val, date):
                style = date_style
            else:
                style = default_style

            sheet.write(row + 1, col, val, style=style)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s.xls' % modelname
    book.save(response)
    return response
    
def importExecl(request, format):
    from .forms import ImportForm
    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            import_file = request.FILES['import_file']
            from xlrd import open_workbook
            wb = open_workbook(file_contents=import_file.read())
            data = list()
            for s in wb.sheets():
                print('Sheet:', s.name)
                for row in range(s.nrows):
                    values_list = []
                    for col in range(s.ncols):
                        values_list.append(s.cell(row, col).value)
                    data.append(values_list)  # 
                    print (values_list)
            if len(data) > 1:
                StudentList = []
                for i in range(len(data)):
                    if i > 0:
                      astudent = data[i]
                      aclass = Classes.objects.get(id=astudent[3])
                      StudentList.append(Student(username=astudent[0], age=astudent[1],gender=astudent[2],cs=aclass))
                if StudentList:
                    Student.objects.bulk_create(StudentList)
    else:
        form = ImportForm()
    return render_to_response("app01/form.html", locals(), context_instance=RequestContext(request))
    