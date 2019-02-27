from django.shortcuts import render,HttpResponseRedirect,redirect
from . forms import HouseChoiceForm
from django.http import  HttpResponse,JsonResponse
import requests
from bs4 import BeautifulSoup
import json
import lxml
import re
from .models import HouseInfo
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your views here.

base_url = "https://xa.lianjia.com/ershoufang/"

def house_index(request):
    form = HouseChoiceForm()
    house_list = HouseInfo.objects.all().order_by('-add_date')
    if house_list:
        paginator = Paginator(house_list,20)
        page = request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return render(request,'home_link/index.html',{
                                                            'form':form,
                                                            'page_obj':page_obj,
                                                            'paginator':paginator,
                                                            'is_paginated':True
                                                        })
    else:
        return render(request,'home_link/index.html',{'form':form})


def house_spider(request):
    if request.method == 'POST':
        form = HouseChoiceForm(data=request.POST)
        if form.is_valid():
            district = form.cleaned_data["district"]
            price = form.cleaned_data["price"]
            bedroom = form.cleaned_data["bedroom"]

            # 验证post请求的数据
            # return JsonResponse({"district":district,
            #               'price':price,
            #               'bedroom':bedroom
            #
            # })

            url = base_url + "{}/{}{}".format(district,price,bedroom)

            # 下面开始爬取
            home_spider = HomeLinkSpider(url)
            home_spider.get_all_page()
            home_spider.parse_page()
            home_spider.save_data_to_model()
            # return JsonResponse({"district":district,
            #               'price':price,
            #               'bedroom':bedroom
            #
            # })
            return  redirect("/home_link/")
    else:
        form = HouseChoiceForm(data=request.POST)
        return render(request,'home_link/index.html',{'form':form})
        # return HttpResponse("该请求为get")

class HomeLinkSpider(object):
    def __init__(self,url):
        self.headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Host':'xa.lianjia.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
        }
        self.url = url
        self.data = list()


    def get_all_page(self):
        response = requests.get(url=self.url,headers=self.headers)
        if response.status_code == 200:
            soup =  BeautifulSoup(response.text,'html.parser')
            a = soup.select('.page-box.house-lst-page-box')
            # max_page = eval(a[0].attrs["page-data"]["totalPage"])
            max_page = json.loads(a[0].attrs["page-data"])["totalPage"]
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print(max_page)
            return max_page
        else:
            print("请求失败 status:{}".format(response.status_code))

    def parse_page(self):
        max_page = self.get_all_page()
        # for i in range(1,max_page+1):
        for i in range(1,max_page+1):
            url = "{}pg{}/".format(self.url,i)
            response = requests.get(url=url,headers=self.headers)
            # print(response.text)
            soup = BeautifulSoup(response.text,'lxml')
            ul = soup.find_all(name='ul',class_='sellListContent')
            li_list = ul[0].select('li')
            # title = li_list[0].select('.info.clear .title a')[0].get_text()
            # print(li_list[0])
            # print(title)
            for li in li_list:
                detail = dict()
                detail['title'] = li.select('.info.clear .title a')[0].get_text()

                house_info = li.select('.houseInfo')[0].get_text()
                house_info_list = house_info.split('|')

                detail['house'] = house_info_list[0]
                detail['bedroom'] = house_info_list[1]
                detail['area'] = house_info_list[2]
                detail['direction'] = house_info_list[3]

                position_info = li.select('.positionInfo')[0].get_text().split(' - ')

                floor_pattern = re.compile('\d+')
                match1 = re.search(floor_pattern,position_info[0])
                if match1:
                    detail['floor'] = match1.group()
                else:
                    detail['floor'] = "未知"
                    
                year_pattern = re.compile(r'\d{4}')
                match2 = re.search(year_pattern, position_info[0])  # 从字符串任意位置匹配
                if match2:
                    detail['year'] = match2.group()
                else:
                    detail['year'] = "未知"
                detail['location'] = position_info[1]

                # 650万，匹配650
                price_pattern = re.compile(r'\d+')
                total_price = li.select('div[class="totalPrice"]')[0].get_text()
                detail['total_price'] = re.search(price_pattern, total_price).group()

                # 单价64182元/平米， 匹配64182
                unit_price = li.select('div[class="unitPrice"]')[0].get_text()
                detail['unit_price'] = re.search(price_pattern, unit_price).group()
                self.data.append(detail)
        # print(self.data)
    def save_data_to_model(self):
        for item in self.data:
            new_item = HouseInfo()
            new_item.title = item['title']
            new_item.house = item['house']
            new_item.bedroom = item['bedroom']
            new_item.area = item['area']
            new_item.direction = item['direction']
            new_item.floor = item['floor']
            new_item.year = item['year']
            new_item.location = item['location']
            new_item.total_price = item['total_price']
            new_item.unit_price = item['unit_price']
            new_item.save()
