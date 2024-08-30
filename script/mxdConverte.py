# -*- coding: utf-8 -*-
# writer:wsh
# date: 30 11 2022
# description: 批量转换mxd版本

import arcpy
import os
import arcpy.mapping as mapping

# mxd所在文件夹
path = 'C:\Users\wsh\Desktop\mxds'
# 输出文件夹
output = r'C:/Users/wsh/Desktop/输出/'
# 指定转换版本，只能转
version = '10.3'

def checkPath(path):
    if not os.path.exists(path):
        os.makedirs(path)

def convertor(source, out):
    checkPath(out)
    print('-----------保存工程为' + version + '版本-----------')
    for f in os.listdir(source):
     if f[-3:].lower() == 'mxd':
         print('正在处理：' + f)
         mxd = mapping.MapDocument(os.path.join(source,f))
         mxd.saveACopy(out + f[:-4]+'_'+version+'.mxd',version)

    print('====================结束==========================')
    
if __name__ == '__main__':
    convertor(path, output)
