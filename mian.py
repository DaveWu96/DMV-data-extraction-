import os
import pandas
import fitz
file_name = []
result = []
import re
import numpy
# 查找目录
for root, dirs, files in os.walk('./data'):
        file_name = files
        break
result = []
for file in file_name:
    pdf = fitz.Document('./data/'+file)
    # 查找
    # 查找每一页面
    content = ''
    for i,pg in enumerate(range(0, pdf.pageCount)):
                            page = pdf[pg]
                            trans = fitz.Matrix(3.0, 3.0).preRotate(0)
                            # 提取文本
                            temp_content = page.get_textpage().extractText()
                            content += temp_content

    # 内容提取
    content = content.split('IS-Related Documents:')
    Document_Header = ''
    flag = 0
    for row in content:
        if not Document_Header:
            if 'CAD' in row:
                xxx = row[row.index('CAD'):]
                Document_Header = ''.join(xxx.split('\n')[0:2]).replace(' ','')
        flag += 1
        keys = {
            'Additional Information': 0,
            'Incident:': 0,
            'Disposition:': 0,
            'DRB:': 0,
            'Case:': 0,
            'Member Disposition:': 0,
            'IAD Discipline:': 0,
            'DRB Disposition:': 0,
            'DRB Discipline:': 0,
            'Synopsis:': 0,
            'Investigative Notes:': 0,
        }
        content_temp = []
        content_temp.append(file)
        content_temp.append(file+str(flag))
        content_temp.append(Document_Header)
        # 查找地址
        row = row.split('\n')
        row = [i.strip(' ') for i in row]
        # 查找地址
        for key in keys.keys():
            try:
                index = row.index(key)
            except BaseException:
                index = 0
            keys[key] = index
        # 添加IS
        if keys['Incident:'] == 0:
            break
        # if keys['Additional Information'] == 0 or (not row[keys['Additional Information']+1].isdigit()):
        for sss in row:
                if sss.isdigit():
                    content_temp.append(sss)
        # else:
        #     content_temp.append(row[keys['Additional Information']+1])

        index_list = list(keys.values())
        for i in range(1,len(index_list)-1):
            temp_c = ''
            if index_list[i+1]-index_list[i] == 1:
                content_temp.append(' ')
            else:
                for k in range(index_list[i]+1,index_list[i+1]):
                    temp_c += row[k]
                content_temp.append(temp_c)
        else:
            temp_c
            for k in range(index_list[-1] + 1, len(row)):
                temp_c += row[k]
            content_temp.append(temp_c)
        result.append(content_temp)
data = pandas.DataFrame(result)
data.to_excel('result.xlsx')
print("完成！！！！")
