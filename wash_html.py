from lxml import etree
import json
import time
import os
import re
import jieba
import jieba.posseg

def convert2list(data):#输入字符串,返回分词后的列表
    ret_list=[]
    seglist=jieba.cut(data,cut_all=True)
    # jieba.cut(data，cut_all=True)#全模式
    # jieba.cut(data，cut_all=False)#精准模式，默认模式
    # jieba.cut_for_search(data)#搜索引擎模式
    for i in seglist:
        if  i not in ret_list:#i not in fuhao_list and
            ret_list.append(i)
    return ret_list#'/'.join(ret_list)

def load_local_worddict():
    # # 加载本地的词语分类
    user_dict_path=os.path.join(os.path.abspath(''),'Bcy_ClassifiedFile')
    user_dict_list=os.listdir(user_dict_path)
    word_content=set()
    for i in user_dict_list:
        word_content|=set(open(os.path.join(user_dict_path,i),'r',encoding='utf-8').read().split('\n'))
        # jieba.load_userdict(os.path.join(user_dict_path,i))
    # print(word_content)
    jieba.load_userdict(word_content)
    print('本地词加载完成')

saved_speechpart_list=set('n ng nr nrfg nrt ns nt nz v vd vg vi vn vq eng'.split())#名词 动词 英文
def word_cut2partofspeech(text):
    ret_list=[]
    # outstr=''
    sentence=text.strip()
    seg_lig = jieba.posseg.cut(sentence)
    for w in seg_lig:
        if w.flag not in saved_speechpart_list:
            pass
        else:
            if w.word not in ret_list:
                # yield w.word
                ret_list.append(w.word)
                # outstr+="{}/{},".format(w.word,w.flag)
        # print ("{}_{},".format(w.word,w.flag))
    return ret_list

def generate_local_json4web(url,web_info):
    # 本地生成json备份web提取的文字
    if 'washed_html' not in os.listdir(os.path.abspath('')):
        os.makedirs('washed_html')
    if url:
        save_name=url+'_'+time.strftime('%Y%m%d%H%M%S')+'.json'
    else:
        save_name=time.strftime('%Y%m%d%H%M%S')+'.json'
    save_name=os.path.join(os.path.abspath(''),'washed_html',save_name)
    with open(save_name,'w',encoding='utf-8') as f:
        f.write(json.dumps(web_info,indent=2,ensure_ascii=False))

def wash_html(data,url=''):#提取网页中主要含有的汉字
    Bcy_Stopwords_Punctuations=open(os.path.join(os.path.abspath(''),'Bcy_Stopwords','Bcy_Stopwords_Punctuations'),'r',encoding='utf-8').read()
    Bcy_Stopwords_Punctuations=[i for i in Bcy_Stopwords_Punctuations.split('\n') if i]
    web_info={'url':url,'title':'','meta_keywords_description':[],'a_text':[],'a_anchor':[],'text':[],'anchor':[]}
    load_local_worddict()
    collect_words_list=[]
    # print(data)
    html=etree.HTML(data) #初始化生成一个XPath解析对象
    result=etree.tostring(html,encoding='utf-8')   #解析对象输出代码
    all_nodes=html.xpath('//*')
    # print(all_nodes)
    for node in all_nodes:
        node_content=(etree.tostring(node,pretty_print=True)).decode('utf-8')
        #首先去掉 (style)，(script)，(applet>等与网页内容无关的HTML源码
        if ('<script' in node_content and '</script>' in node_content) or ('<script src="' in node_content and '.js' in node_content) or ('<style' in node_content and '</style>' in node_content) or ('<applet' in node_content and '</applet>' in node_content):
            pass
        # elif ('<style' in node_content and '</style>' in node_content):
        #     pass
        # elif ('<applet' in node_content and '</applet>' in node_content):
        #     pass
        # meta标签用来描述一个HTML网页文档的属性，其中的网页描述 、关键词等属性与网页内容具有很强的相关性。
        # 提取meta
        elif ('<meta' in node_content and 'name="keywo' in node_content) or ('<meta' in node_content and 'name="description"' in node_content):
            str_in_meta=node.attrib.get('content')
            web_info['meta_keywords_description'].append(str_in_meta)
            # for i in word_cut2partofspeech(str_in_meta):
            #     if i not in collect_words_list:
            #         collect_words_list.append(i)
        # 提取title
        elif ('<title' in node_content and '</title>' in node_content):
            web_info['title']=node.text
            # for i in word_cut2partofspeech(node.text):
            #     if i not in collect_words_list:
            #         collect_words_list.append(i)
        # 提取li中的text/li中的p的text/li中的a的text
        elif ('<li' in node_content and (node.text!="" or node.xpath('p//text()')!=[] or node.xpath('a//text()')!=[])):#
            if node.text is not None and node.text.replace(' ','').replace('\n','').replace('\t','') !='':#字符串
                str_li_text=node.text.replace(' ','').replace('\n','').replace('\t','')#去掉空格 去掉回车
                web_info['text'].append(str_li_text)
                # for i in word_cut2partofspeech(str_li_text):
                #     if i not in collect_words_list:
                #         collect_words_list.append(i)
                # pass
            elif node.xpath('p//text()'):#列表
                list_li_p_text=node.xpath('p//text()')
                for j in list_li_p_text:
                    web_info['text'].append(j)
                    # for i in word_cut2partofspeech(j):
                    #     if i not in collect_words_list:
                    #         collect_words_list.append(i)
                # pass
            elif node.xpath('a//text()'):#列表
                list_li_a_text=node.xpath('a//text()')
                list_li_a_href=node.xpath('a//@href')
                for j in list_li_a_text:
                    if j.replace(' ','').replace('\n','').replace('\t',''):#去掉空格后不为空
                        web_info['a_text'].append(j.replace(' ','').replace('\n','').replace('\t',''))
                    # for i in word_cut2partofspeech(j):
                    #     if i not in collect_words_list:
                    #         collect_words_list.append(i)
                for j in list_li_a_href:
                    web_info['a_anchor'].append(j)
                # pass
            else:
                pass
        # 提取div中的text
        elif ('<div ' in node_content and node.text is not None and node.text.replace(' ','').replace('\n','').replace('\t','')!=''):
            str_in_div_text=node.text.replace(' ','').replace('\n','').replace('\t','')
            web_info['text'].append(str_in_div_text)
            # for i in word_cut2partofspeech(node.text.replace(' ','').replace('\n','').replace('\t','')):
            #     if i not in collect_words_list:
            #         collect_words_list.append(i)

            # print(node.text.replace(' ','').replace('\n',''))
            # pass
        # 提取div中的text/div中的p的text/div中的span的text
        elif ('<div ' in node_content and (node.xpath('p//text()')!=[] or node.xpath('span//text()')!=[])):
            if node.xpath('p//text()'):
                list_div_p_text=node.xpath('p//text()')
                if list_div_p_text:
                    for j in list_div_p_text:
                        web_info['text'].append(j)
                        # for i in word_cut2partofspeech(j):
                        #     if i not in collect_words_list:
                        #         collect_words_list.append(i)
            elif node.xpath('span//text()'):
                list_div_span_text=node.xpath('span//text()')
                if list_div_span_text:
                    for j in list_div_span_text:
                        if j.isdigit():
                            pass
                        else:
                            web_info['text'].append(j)
                            # for i in word_cut2partofspeech(j):
                            #     if i not in collect_words_list:
                            #         collect_words_list.append(i)
            else:
                pass
        else:
            # print(node_content)
            pass

    # generate_local_json4web(url,web_info)# 本地生成json备份web提取的文字

    show_info_json={}

    #1 TITLE
    # print('title',web_info['title'])
    title_dict={}
    title_list=[]
    title_dict[web_info['title']]=[i for i in word_cut2partofspeech(web_info['title']) if i not in Bcy_Stopwords_Punctuations]#过滤停用词标点符号
    title_list.append(title_dict)
    show_info_json['title']=title_list
    # print(title_dict)

    #2 META
    # print('meta',web_info['meta_keywords_description'])
    meta_list=[]
    for w in web_info['meta_keywords_description']:
        meta_dict={}
        meta_dict[w]=[i for i in word_cut2partofspeech(w) if i not in Bcy_Stopwords_Punctuations]#过滤停用词标点符号
        meta_list.append(meta_dict)
    show_info_json['meta']=meta_list
    # print(meta_dict)

    #3 A_TEST
    # print('a_text',web_info['a_text'])
    
    a_text_list=[]
    for w in web_info['a_text']:
        a_text_dict={}
        if len(w)>6:
            a_text_dict[w]=[i for i in word_cut2partofspeech(w) if i not in Bcy_Stopwords_Punctuations]#过滤停用词标点符号
        else:
            a_text_dict[w]=[w]
        a_text_list.append(a_text_dict) 
    show_info_json['a_text']=a_text_list
    # print(a_text_dict)

    #4 text 大段文字
    # print('text',web_info['text'])
    
    text_list=[]
    for w in web_info['text']:
        text_dict={}
        if len(w)>6:
            text_dict[w]=[i for i in word_cut2partofspeech(w) if i not in Bcy_Stopwords_Punctuations]#过滤停用词标点符号
        else:
            temp_text=[i for i in word_cut2partofspeech(w) if i not in Bcy_Stopwords_Punctuations]
            if w not in temp_text:
                temp_text.append(w)
            text_dict[w]=temp_text
        text_list.append(text_dict)
    show_info_json['text']=text_list
    # print(text_dict)

    print(json.dumps(show_info_json,ensure_ascii=False))
    # print(type(json.dumps(show_info_json)))
    # return '/'.join(collect_words_list)#返回一个巨大的列表
    return json.dumps(show_info_json,ensure_ascii=False)