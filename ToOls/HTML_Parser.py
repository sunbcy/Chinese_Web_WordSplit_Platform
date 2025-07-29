# while(html_cnt):
#       for i in range(len(html_cnt)):
#           left=''
#           slack=''
#           # right=''
#           if html_cnt[i]=='<':
#               left=i
#           elif html_cnt[i]=='>':
#               if slack=='/' and html_cnt[1]=='/':
#                   elem=html_cnt[:i].lstrip()[2:]
#                   print(f"elem: {elem}")
#                   slack=''
#                   print(f'元素{elem}为elem_right！')
#               elif slack=='/' and html_cnt[i-1]=='/':# √
#                   elem=html_cnt[:i].lstrip().split(' ')[0].split('<')[1]
#                   print(f"elem: {elem}")
#                   slack=''
#                   print(f'元素{elem}为elem_half_left！')
#               else:
#                   if '<!' in html_cnt[:i]:
#                       print(f'注释: {html_cnt[:i+1]}')
#                   else: 
#                       if '<' in html_cnt[:i]:
#                           try:
#                               print(html_cnt[:i+1].lstrip())
#                               elem=html_cnt[:i].lstrip()[1:]
#                               print(f"elem: {elem}")
#                               print(f'元素{elem}为elem_left！')
#                           except Exception as e:
#                               print(html_cnt[:i])
#                               quit()
#               print(elem_dict)
#               if elem not in elem_dict.keys():
#                   elem_dict[i]=1
#               else:
#                   elem_dict[i]+=1
#               html_cnt=html_cnt[i:].lstrip()
#               break
#           elif html_cnt[i]=='/':
#               slack='/'
#           else:#other char
#               pass


# elem_container=[]
#   while(html_cnt):
#       head=html_cnt[0]
#       if head:#首字符不为空
#           if head=='>':
#               elem_container.append(head)
#               elem=''.join(elem_container)[elem_container.index('<'):]
#               if '/' in elem:
#                   if elem[1]=='/':
#                       elem=''
#                       # print('元素elem_right')
#                   else:
#                       # print('元素elem_half_left')
#                       elem=elem.split(' ')[0][1:]
#               else:
#                   # print('元素elem_left')
#                   if ' ' in elem:
#                       elem=elem.split(' ')[0][1:]
#                   else:
#                       elem=elem.split(' ')[0][1:-1]
#               # if elem:
#               #   print(' ',elem)
#               # break
#               if elem not in elem_dict.keys():
#                   elem_dict[elem]=1
#               else:
#                   elem_dict[elem]+=1
#               elem_container=[]
#               # while(elem_container):
#               #   elem_container.pop()
#           elif head=='!':
#               elem_container.append(head)
#               if elem_container[0]=='<':
#                   print('注释')
#           else:
#               elem_container.append(head)
#           html_cnt=html_cnt[1:]
#           # break
#       else:
#           pass

from html.parser import HTMLParser
from bs4 import BeautifulSoup
import time
elem_dict = {}
temp = []
stop_elems = ['br', 'hr', 'form', 'option', 'input', 'script', 'style', 'object', 'applet']


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        if tag not in stop_elems:
            if tag not in temp:
                temp.append(tag)
            else:
                if tag not in elem_dict.keys():
                    elem_dict[tag] = 2
                else:
                    elem_dict[tag] += 1
        else:
            pass


html_cnt = open('../TEMP/tophub.today.html', 'r', encoding='utf-8').read()


def HTML_Parser(html_cnt):  # count elems in html,get frequency
    output = ''
    blacklist = ['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script', 'style']
    parser = MyHTMLParser()
    parser.feed(html_cnt)
    soup = BeautifulSoup(html_cnt, 'lxml')
    head_tag = soup.head
    title_tag = head_tag.contents
    title = soup.title.string if soup.title else None
    print(title)
    # print(title_tag)
    # text=soup.find_all(text=True)
    # for t in text:
    #     if t.parent.name not in blacklist:
    #         output+='{} '.format(t)
    # print(output)
    return elem_dict

# start_time=time.time()
# html_elem_count=HTML_Parser(html_cnt)
# end_time=time.time()
# print(end_time-start_time,'s')


class Stack:
    def __init__(self):
        self.items = []

    def get(self):
        return self.items

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.size():
            return self.items.pop()
        else:
            return None

    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)


# print('网页元素统计',html_elem_count)
html1_cnt = open('../TEMP/test.html', 'r', encoding='utf-8').read()


class htmlparser:
    def __init__(self, input_html):
        self.input_html = input_html

    def check_tag(self):
        # print(self.input_html)
        stack1 = Stack()
        stack2 = Stack()
        temp = []
        for i in self.input_html:
            while i == '>':
                while stack1.size():
                    temp_a = stack1.pop()
                    print(temp_a)
                    if temp_a not in ['/', '<']:
                        temp.append(temp_a)
                break
            stack1.push(i)
            # if i!='>':
            #     stack1.push(i)
            # else:
            #     while stack1.get():
            #         while stack1.get()[0]!='<':
            #             stack1.pop()
            #         temp.append(stack1.pop())
        stack2.push(''.join(temp))
        return stack2.get()


a = htmlparser(html1_cnt)
print(a.check_tag())

# b=Stack()
# print(b.pop())