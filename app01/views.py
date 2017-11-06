from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse,render_to_response
from django.template import RequestContext
from app01 import models
import json

from app01.forms import UserForm
from .models import Student,Classes,BuyingItem,Transport_way,Clearance_sign

"""分页"""
from django.core.paginator import Paginator, EmptyPage,\
PageNotAnInteger

from django.db.models.loading import get_model

import time,datetime

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

    appname = 'app01'
    modelname = 'Student'
    modelobj = get_model(appname, modelname)
    fields = modelobj._meta.fields
    verbose_names = [elem.verbose_name for elem in fields]

    return render(request,'app01/students.html',{'stu_list':stu_list,'cls_list':cls_list,'verbose_names':verbose_names,'page': page,'pagenum':pagenum})
    
def buyingitems(request):
    item_list = models.BuyingItem.objects.all()
    trans_list = models.Transport_way.objects.all()
    sign_list = models.Clearance_sign.objects.all()
    pagenum = 40
    paginator = Paginator(item_list, pagenum) # 3 posts in each page
    page = request.GET.get('page')

    try:
        item_list_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        item_list_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        item_list_page = paginator.page(paginator.num_pages)


    appname = 'app01'
    modelname = 'BuyingItem'
    modelobj = get_model(appname, modelname)
    fields = modelobj._meta.fields
    verbose_names = [elem.verbose_name for elem in fields]


    return render(request,'app01/buyingitems.html',{'item_list_page':item_list_page,'trans_list':trans_list,'sign_list':sign_list,
                                                    'verbose_names':verbose_names,'page': page,'pagenum':pagenum})
 
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

__s_date = datetime.date (1899, 12, 31).toordinal() - 1
def getdate(date ):
    if isinstance(date , float ):
        date = int(date )
    d = datetime.date.fromordinal(__s_date + date )
    return d

def importExeclBuyingItem(request, format):
    from .forms import ImportFormBuyingItem
    if request.method == "POST":
        form = ImportFormBuyingItem(request.POST, request.FILES)
        if form.is_valid():
            import_file = request.FILES['import_file']
            from xlrd import open_workbook
            wb = open_workbook(file_contents=import_file.read())
            data = list()
            for s in wb.sheets():
                print('Sheet:', s.name)
                if s.name == "Sheet1":
                    for row in range(s.nrows):
                        values_list = []
                        for col in range(s.ncols):
                            values_list.append(s.cell(row, col).value)

                        if values_list[2] != "":
                            data.append(values_list)  #
            print('data')
            print(data)
            if len(data) > 1:
                ItemList = []
                num = 0
                for a in data:
                    if a[2] != "":
                        num = num + 1
                print(num)
                for i in range(num):
                    if i > 0:
                      aitem = data[i]
                      if data[i][2] != "":
                          if aitem[0] == "":
                              aitem[0] = 0
                          if aitem[4] == "":
                              aitem[4] = 0
                          if aitem[5] == "":
                              aitem[5] = 0
                          if aitem[6] == "":
                              aitem[6] = 0
                          if aitem[7] == "":
                              aitem[7] = 0
                          if aitem[8] == "":
                              aitem[8] = 0
                          if aitem[9] == "":
                              aitem[9] = 0
                          if aitem[10] == "":
                              aitem[10] = 0
                          if aitem[11] == "":
                              aitem[11] = 0
                          if aitem[12] == "":
                              aitem[12] = 0
                          if aitem[15] == "":
                              aitem[15] = 0
                          if aitem[16] == "":
                              aitem[16] = 0
                          if aitem[17] == "":
                              aitem[17] = 0
                          if aitem[18] == "":
                              aitem[18] = 0
                          if aitem[30] == "":
                              aitem[30] = 0
                          if aitem[31] == "":
                              aitem[31] = 0

                          atransport_way = Transport_way.objects.get(transport_way=aitem[28])
                          aclearance_sign = Clearance_sign.objects.get(clearance_sign=aitem[29])
                          # print('atiem20')
                          # print(aitem[20])
                          # timestr = "time" + str(aitem[20])
                          # print('timestr')
                          # print(timestr)
                          # t = time.strptime(timestr, "time%m/%d/%Y")
                          # aitem[20] = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday)
                          # timestr = "time" + str(aitem[21])
                          # t = time.strptime(timestr, "time%m/%d/%Y")
                          # aitem[21] = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday)
                          aitem[20] = getdate(aitem[20])
                          aitem[21] = getdate(aitem[21])
                          #t
                          #time.struct_time(tm_year=2017, tm_mon=10, tm_mday=17, tm_hour=0, tm_min=0, tm_sec=0,
                          #                 tm_wday=1, tm_yday=290, tm_isdst=-1)

                          ItemList.append(BuyingItem(no=aitem[0], item_no=aitem[1],choice_name=aitem[2], name=aitem[3],buying_price=aitem[4], face_price=aitem[5]
                              ,add_price=aitem[6], native_trans_fee=aitem[7],price=aitem[8], national_tran_fee=aitem[9], service_charge_rate=aitem[10]
                              ,service_charge_fee=aitem[11], profit=aitem[12], chinese_kind_name=aitem[13],english_name=aitem[14], weight = aitem[15], volume = aitem[16]
                              ,american_price = aitem[17], real_american_price = aitem[18], hs_code = aitem[19], upload_day = aitem[20], downshelf_day = aitem[21],
                              leftdays = aitem[22], buying_name = aitem[23], buying_url = aitem[24],status=aitem[25],korea_name=aitem[26],chinese_name=aitem[27],
                              transport_way_id = atransport_way,clearance_sign_id=aclearance_sign,tariff=aitem[30],add_express_fee=aitem[31]))
                if ItemList:
                    print('ItemList')
                    print(len(ItemList))
                    BuyingItem.objects.bulk_create(ItemList)
    else:
        form = ImportFormBuyingItem()
    return render_to_response("app01/form.html", locals(), context_instance=RequestContext(request))
#---采购基础资料
# NO        no
# 商品编号   item_no
# 选项      choice_name
# 商品名称   name
# 采购单价   buying_price
# 表面价     face_price
# 加减金额    add_price
# 国内运费    native_trans_fee
# 实际售价    price
# 国际物流费  national_tran_fee
# 平台手续费  service_charge_rate
# 手续费      service_charge_fee
# 利润       profit
# 中文品名    chinese_name
# 英文品名    english_name
# 重量        weight
# 体积        volume
# 美金单价     american_price
# 实际报关美金  real_american_price
# HS编码       hs_code
# 产品上传      upload_day
# 产品下架      downshelf_day
# 剩余日       leftdays
# 采购品名      buying_name
# 采购地址      buying_url
# 状态          status
# 韩文名        korea_name
# 中文名        chinese_name
# 货运方式    transport_way
# 通关符号    clearance_sign
# 关税       tariff
# 快递附加费  add_express_fee
# 运输公司    transport_company
