# -*- coding: utf-8 -*-
from flask import Flask,jsonify,render_template,request
import os
import json
import jieba
from wash_html import wash_html

def Local_STOPWORDS_Init():#本地停用词文件初始化
    if 'Bcy_Stopwords' not in os.listdir(os.path.abspath('')):
        os.makedirs(os.path.join(os.path.abspath(''),'Bcy_Stopwords'))
    Bcy_Stopwords_Punctuations=open(os.path.join(os.path.abspath(''),'Bcy_Stopwords','Bcy_Stopwords_Punctuations'),'r',encoding='utf-8').read()
    Bcy_Stopwords_Punctuations=[i for i in Bcy_Stopwords_Punctuations.split('\n') if i]
    Bcy_Stopwords_Punctuations=list(set(Bcy_Stopwords_Punctuations))# 去重
    with open(os.path.join(os.path.abspath(''),'Bcy_Stopwords','Bcy_Stopwords_Punctuations'),'w',encoding='utf-8') as f:
        for i in Bcy_Stopwords_Punctuations:
            f.write(f"{i}\n")

def Local_ClassifiedFile_Init():#本地大类词汇分类文件初始化
    if 'Bcy_ClassifiedFile' not in os.listdir(os.path.abspath('')):
        os.makedirs(os.path.join(os.path.abspath(''),'Bcy_ClassifiedFile'))
    local_classified_list=os.listdir(os.path.join(os.path.abspath(''),'Bcy_ClassifiedFile'))

    Init_WordType=('App&网站名','公司名','国家','重要历史事件','车_品牌','Others')#可以在代码自定义添加一些分类，项目初始化时候自动生成!!!
    for i in Init_WordType:
        if i not in local_classified_list:
            a=open(os.path.join(os.path.abspath(''),'Bcy_ClassifiedFile',i),'w',encoding='utf-8')#新建一个初始化分类词的文件
            a.close()
    # 分类词文件去重
    for w in local_classified_list:
        Bcy_ClassifiedWords=open(os.path.join(os.path.abspath(''),'Bcy_ClassifiedFile',w),'r',encoding='utf-8').read()
        Bcy_ClassifiedWords=[i for i in Bcy_ClassifiedWords.split('\n') if i]
        Bcy_ClassifiedWords=list(set(Bcy_ClassifiedWords))# 去重
        with open(os.path.join(os.path.abspath(''),'Bcy_ClassifiedFile',w),'w',encoding='utf-8') as f:
            for i in Bcy_ClassifiedWords:
                # f.write(f"{i}\n")
                if i[-2:] != ' n':
                    # print(i.split(' ')[0])
                    f.write(f"{i} n\n")
                else:
                    f.write(f"{i}\n")

def convert(data):#返回分词后的字符串
    ret_list=[]
    seglist=jieba.cut(data,cut_all=True)
    # jieba.cut(data，cut_all=True)#全模式
    # jieba.cut(data，cut_all=False)#精准模式，默认模式
    # jieba.cut_for_search(data)#搜索引擎模式
    for i in seglist:
        if  i not in ret_list:#
            ret_list.append(i)
    return '/'.join(ret_list)

def wash_data():
    pass

app = Flask(__name__)#实例化app对象
 
# 配合网页停用词、大类词初始化加载
@app.route('/test_post/bb',methods=['GET'])#路由
def Web_STOPWORDS_Init():
    Bcy_STOPWORDS_list=os.listdir(os.path.join(os.path.abspath(''),'Bcy_Stopwords'))
    Bcy_ClassifiedFile_list=os.listdir(os.path.join(os.path.abspath(''),'Bcy_ClassifiedFile'))
    data={"output":Bcy_STOPWORDS_list+Bcy_ClassifiedFile_list}
    return json.dumps(data)

# 添加新类词
@app.route('/test_post/dd',methods=['POST'])
def Get_NewType_Word():
    NewType=request.form.get('newtype')
    Bcy_ClassifiedFile=os.listdir(os.path.join(os.path.abspath(''),'Bcy_ClassifiedFile'))
    if NewType not in Bcy_ClassifiedFile:
        a=open(os.path.join(os.path.abspath(''),'Bcy_ClassifiedFile',NewType),'w',encoding='utf-8')#新建一个该分类词的文件
        a.close()
        data={"ret_info":True}
    else:
        data={"ret_info":False}
    return json.dumps(data)

@app.route('/test_post/cc',methods=['GET','POST'])#路由
# 词库Type 新增按钮的值 New_word
def New_Word_submit():
    Type=request.form.get('type')
    New_word=request.form.get('new_word')
    if "Bcy_Stopwords" in Type:#如果web选中的类别是停用词
        Bcy_Class_path=os.path.join(os.path.abspath(''),'Bcy_Stopwords')
    else:#如果web选中的类别不是停用词
        Bcy_Class_path=os.path.join(os.path.abspath(''),'Bcy_ClassifiedFile')
        # Bcy_Stopwords_content_list=open(os.path.join(Bcy_Class_path,Type),'a+',encoding='utf-8').read()
    Bcy_Class_content_list=open(os.path.join(Bcy_Class_path,Type),'a+',encoding='utf-8').read()
    Bcy_Class_content_list=[i for i in Bcy_Class_content_list.split('\n') if i]
    if New_word not in Bcy_Class_content_list:
        with open(os.path.join(Bcy_Class_path,Type),'a',encoding='utf-8') as f:
            f.write(f"{New_word}\n")

    print(New_word,'添加到',Type)
    data={"ret_info":New_word+' 添加到 '+Type}
    return json.dumps(data)

# @app.route('/remove_btn/aa',methods=['GET','POST'])#路由 接受按钮的值
# def remove_btn():
#     Bcy_Stopwords_Punctuations=open(os.path.join(os.path.abspath(''),'Bcy_Stopwords','Bcy_Stopwords_Punctuations'),'a+',encoding='utf-8').read()
#     Bcy_Stopwords_Punctuations=[i for i in Bcy_Stopwords_Punctuations.split('\n') if i]
#     a=request.form.get('mydata')
#     print(a,'添加到Stopwords_Punctuations')
#     if a not in Bcy_Stopwords_Punctuations:
#         with open(os.path.join(os.path.abspath(''),'Bcy_Stopwords','Bcy_Stopwords_Punctuations'),'a',encoding='utf-8') as f:
#             f.write(f"{a}\n")
#     # want_data=wash_html(a)#提取网页中主要含有的汉字
#     data={"word":a,"output":a+' 成功加入Stopwords'}
#     # data={"word":a,"output":convert(want_data)}#清洗了一下，去除了HTML中不含文字的部分
#     # data={"word":a,"output":want_data}
#     return json.dumps(data)

@app.route('/test_post/nn',methods=['GET','POST'])#路由
def test_post():
    a=request.form.get('mydata')
    want_data=wash_html(a)#提取网页中主要含有的汉字
    # data={"word":a,"output":convert(a)}
    # data={"word":a,"output":convert(want_data)}#清洗了一下，去除了HTML中不含文字的部分
    data={"word":a,"output":want_data}
    return json.dumps(data)

@app.route('/')
def hello_world():
    return 'Hello World!'
 
@app.route('/index')
def index():
    return render_template('input_chinese.html')
 

if __name__ == '__main__':
    Local_STOPWORDS_Init()
    Local_ClassifiedFile_Init()
    app.run(host='0.0.0.0',#任何ip都可以访问
            port=5000,#端口
            debug=True
            )
    