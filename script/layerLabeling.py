# -*- coding: utf-8 -*-
# writer: wsh
# date: 22:23 1 12 2022
# description: 批量修改图层标注的字体大小、颜色，其他属性未查阅

import arcpy

mxd = arcpy.mapping.MapDocument('CURRENT')
layers = arcpy.mapping.ListLayers(mxd)

# 必须先按顺序设置每一个图层的label展示字段
labelArr = ['name', 'FID']
# 字体颜色
rgb = [0, 77, 168]
# 字体大小
fontSize = 10
preExpression = "<CLR red='%s' green='%s'  blue='%s'><FNT size='%s'>" % (rgb[0], rgb[1], rgb[2], fontSize)

for i in range(len(layers)):
    lyr = layers[i]
    if lyr.supports('LABELCLASSES'):
        for lblCls in lyr.labelClasses:
            lblCls.expression = '"{}" + [{}] +  "{}"'.format(preExpression, labelArr[i], "</FNT></CLR>")
            lblCls.showClassLabels = True
            lyr.showLabels = True
            
# 修改后刷新
arcpy.RefreshActiveView()
