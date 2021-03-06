# _*_coding: utf-8_*_

import json

from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse
# from django.forms.models import model_to_dict
from django.core import serializers

from goods.models import Goods
from django.http import HttpResponse

from .models import Goods


class GoodsListView(View):
    def get(self, request):
        """
        显示商品列表
        :param request:
        :return:
        """
        json_list = []

        goods = Goods.objects.all()[:10]
        # for good in goods:
        # json_dict = {}
        # json_dict['name'] = good.name
        # json_dict['category'] = good.category.name
        # json_dict['market_price'] = good.market_price

        # json_dict = model_to_dict(good)
        # json_list.append(json_dict)

        json_data = serializers.serialize('json', goods)
        json_data = json.loads(json_data)

        # return HttpResponse(json_data, content_type="application/json")
        return JsonResponse(json_data, safe=False)
        for good in goods:
            json_dict = {}
            json_dict['name'] = good.name
            json_dict['category'] = good.category.name
            json_dict['market_price'] = good.market_price
            json_list.append(json_dict)

        return HttpResponse(json.dumps(json_list), content_type="application/json")

