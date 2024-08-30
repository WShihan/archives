# -*- coding: utf-8 -*-
# writer:wsh
# date: 30 11 2022
# description: ����ת��mxd�汾

import arcpy
import os
import arcpy.mapping as mapping

# mxd�����ļ���
path = 'C:\Users\wsh\Desktop\mxds'
# ����ļ���
output = r'C:/Users/wsh/Desktop/���/'
# ָ��ת���汾��ֻ��ת
version = '10.3'

def checkPath(path):
    if not os.path.exists(path):
        os.makedirs(path)

def convertor(source, out):
    checkPath(out)
    print('-----------���湤��Ϊ' + version + '�汾-----------')
    for f in os.listdir(source):
     if f[-3:].lower() == 'mxd':
         print('���ڴ���' + f)
         mxd = mapping.MapDocument(os.path.join(source,f))
         mxd.saveACopy(out + f[:-4]+'_'+version+'.mxd',version)

    print('====================����==========================')
    
if __name__ == '__main__':
    convertor(path, output)
