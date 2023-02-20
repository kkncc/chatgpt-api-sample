# -*- coding: utf-8 -*-
from . import v1


# pa防火墙外部动态IP列表
@v1.app_errorhandler(404)
def page_not_found(e):
	return '404'
