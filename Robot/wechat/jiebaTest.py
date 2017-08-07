#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
import jieba

jieba.add_word('此次航班胜负')
jieba.del_word('胜')
jieba.del_word('负')
se = jieba.lcut('此次航班胜负:3胜1负')
print se
