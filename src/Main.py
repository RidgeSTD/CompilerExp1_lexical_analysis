#coding:utf-8

import sys

buf = ""
mLine = 1
mRow = 0
currentState = 'A'
__letterSet__  = { 'a','b','c','d','e','f','g','h','i','j','k','l','m',
				'n','o','p','q','r','s','t','u','v','w','x','y','z',
				'A','B','C','D','E','F','G','H','I','J','K','L','M',
				'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',}
__digitSet__ = {'0','1','2','3','4','5','6','7','8','9'}
__blankCharSet__ = {' ', '\n', '\t'}
__switchCharSet__ = {'b', 'n', 't', '\'', '\"'}
__keywordSet__ = {'abstract','assert','booleanbreak','byte','case',
				'catch','char','class','const','continue','default','do',
				'double','else','enum','extends','final','finally','float',
				'for','goto','if','implements','import','instanceof','int',
				'interface','long','native','new','package','private','protected',
				'public','return','strictfp','short','static','super','switch',
				'synchronized','this','throw','throws','transient','try','void',
				'volatile','while'}
__boardSet__ = {';',',', '(', ')', '.'}
result=""
__TOKENIZE_SUCCESS__ = 0
__TOKEN_ERROR__ = 1


def compilerStop(status):
	global mLine
	global mRow
	if(status == 0):
		# TODO
		tmp = 1
	if(status == 1):
		print(result)
		print("编译于第 "+str(mRow)+" 行, 第 "+str(mLine)+" 列失败")
		sys.exit(0)


def tokenizer(ch):
	global buf
	global mLine
	global mRow
	global currentState
	global __letterSet__
	global __digitSet__
	global __blankCharSet__
	global __keywordSet__
	global result
	global __TOKEN_ERROR__
	global __TOKENIZE_SUCCESS__

	while True:
		if currentState == 'A':
			if(ch==' ' or ch=='\n' or ch=='\t'):
				currentState = 'A'
				return
			elif(ch in __letterSet__ or ch=='_'):
				buf = buf + ch
				currentState = 'B'#标识符方向
				return
			elif(ch in __digitSet__):
				buf = buf + ch
				currentState = 'C'#整数
				return
			elif(ch == '\''):
				buf = buf + ch
				currentState = 'D'#字符常量
				return
			elif(ch == '\"'):
				buf = buf + ch
				currentState = 'G'#字符串常量
				return
			elif(ch == '/'):
				buf = buf + ch
				currentState = 'K'#不确定，先按照注释处理
				return
			# 下面是操作符识别
			elif(ch=='+'):
				buf = buf+ch
				currentState = 'A+'
				return
			elif(ch=='-'):
				buf = buf+ch
				currentState = 'A-'
				return
			elif(ch=='*'):
				buf = buf+ch
				currentState = 'A*'
				return
			elif(ch=='&'):
				buf = buf+ch
				currentState = 'A&'
				return
			elif(ch=='^'):
				buf = buf+ch
				currentState = 'A^'
				return
			elif(ch=='|'):
				buf = buf+ch
				currentState = 'A|'
				return
			elif(ch=='='):
				buf = buf+ch
				currentState = 'A='
				return
			elif(ch=='!'):
				buf = buf+ch
				currentState = 'A!'
				return
			elif(ch=='>'):
				buf = buf+ch
				currentState = 'A>'
				return
			elif(ch=='<'):
				buf = buf+ch
				currentState = 'A<'
				return
			elif(ch in __boardSet__):
				buf = ""
				result = result+'('+ch+', 界符)\n'
				currentState='A'
				return
			else:
				compilerStop(__TOKEN_ERROR__)
				return

		##############     状态B         #################
		elif currentState == 'B':
			if(ch == '_' or ch in __letterSet__ or ch in __digitSet__):
				buf = buf+ch
				currentState = 'B'
				return
			else:#可接受状态
				if (buf in __keywordSet__):
					result = result + '('+buf+', 关键字)\n'
				else:
					result = result + '('+buf+', 标识符)\n'
				buf = ""
				currentState = 'A'
				continue

		##############     状态C         #################

		elif currentState == 'C':
			if(ch in __digitSet__):
				buf = buf + ch
				currentState = 'C'
				return
			elif(ch=='.'):
				buf = buf+ch
				currentState = 'P'
				return
			else:#可接受状态
				result = result + '('+ buf + ', 整数常量)\n'
				buf = ""
				currentState = 'A'
				continue

		##############     状态D         #################
		elif currentState == 'D':
			if(ch!='\'' and ch!='\\'):
				buf = buf+ch
				currentState = 'E'
				return
			elif (ch!='\'' and ch=='\\'):
				buf = buf+ch
				currentState = 'F'
				return

		##############     状态E        #################
		elif currentState == 'E':
			if(ch=='\''):
				buf = buf+ch
				currentState = 'H'
				return
			else:
				compilerStop(__TOKEN_ERROR__)

		##############     状态EE        #################
		elif currentState == 'H':
			result = result + '(' + buf+ ',字符常量)\n'
			buf = ""
			currentState = 'A'
			return

		##############     状态F         #################
		elif currentState == 'F':
			if(ch in __switchCharSet__):
				buf = buf + ch
				currentState = 'E'
				return
			else:
				compilerStop(__TOKEN_ERROR__)			

		##############     状态G         #################
		elif currentState == 'G':
			if(ch!='\"' and ch!='\\'):
				buf = buf+ch
				currentState = 'G'
				return
			elif (ch!='\'' and ch=='\\'):
				buf = buf+ch
				currentState = 'I'
				return
			elif(ch=='\"'):
				buf = buf+ch
				currentState = 'J'

		##############     状态I         #################
		elif currentState == 'I':
			if(ch in __switchCharSet__):
				buf = buf+ch
				currentState = 'G'
				return
			else:
				compilerStop(__TOKEN_ERROR__)

		##############     状态J         #################
		elif currentState == 'J':
			result = result + '(' + buf+ ',字符串常量)\n'
			buf = ""
			currentState = 'A'
			return

		##############     状态K         #################
		elif currentState == 'K':
			if(ch=='*'):
				buf = buf[0:len(buf)-1]  #是注释，退去上一个/
				currentState = 'L'
				return
			elif(ch=='/'):#单行注释
				buf = buf[0:len(buf)-1]  #是注释，退去上一个/
				currentState = 'O'
				return
			elif(ch=='='):
				buf = buf+ch
				currentState = 'B='
				return
			else:
				result = result+'('+buf+',运算符)\n'
				buf = ""
				currentState = 'A'
				continue

		##############     状态L         #################
		elif currentState == 'L':
			if(ch != '*'):
				currentState = 'L'
				return
			elif(ch=='*'):
				currentState = 'M'
				return
		##############     状态L         #################
		elif currentState=='M':
			if(ch=='/'):
				currentState = 'N'
				return
			else:
				currentState='L'

		##############     状态L         #################
		elif currentState=='N':
			currentState = 'A'
			return
		##############     状态A+         #################
		elif currentState=='A+':
			if(ch=='+' or ch=='='):
				buf = buf+ch
				currentState='B+'
				return
			else:
				result = result+'('+buf+',操作符)\n'
				buf=""
				currentState = 'A'
				continue

		##############     状态B+         #################
		elif currentState=='B+':
			result = result+'('+buf+',操作符)\n'
			buf = ""
			currentState = 'A'
			return

		##############     状态A-         #################
		elif currentState=='A-':
			if(ch=='-' or ch=='='):
				buf = buf+ch
				currentState='B-'
				return
			else:
				result = result+'('+buf+',操作符)\n'
				buf=""
				currentState = 'A'
				continue

		##############     状态B-         #################
		elif currentState=='B-':
			result = result+'('+buf+',操作符)\n'
			buf = ""
			currentState = 'A'
			return

		##############     状态A*         #################
		elif currentState=='A*':
			if(ch=='*' or ch=='='):
				buf = buf+ch
				currentState='B*'
				return
			else:
				result = result+'('+buf+',操作符)\n'
				buf=""
				currentState = 'A'
				continue

		##############     状态B*         #################
		elif currentState=='B(':
			result = result+'('+buf+',操作符)\n'
			buf = ""
			currentState = 'A'
			return

		##############     状态A&         #################
		elif currentState=='A&':
			if(ch=='&' or ch=='='):
				buf = buf+ch
				currentState='B&'
				return
			else:
				result = result+'('+buf+',操作符)\n'
				buf=""
				currentState = 'A'
				continue

		##############     状态B+         #################
		elif currentState=='B&':
			result = result+'('+buf+',操作符)\n'
			buf = ""
			currentState = 'A'
			return

		##############     状态A^         #################
		elif currentState=='A^':
			if(ch=='^' or ch=='='):
				buf = buf+ch
				currentState='B^'
				return
			else:
				result = result+ '('+buf+',操作符)\n'
				buf=""
				currentState = 'A'
				continue

		##############     状态B^         #################
		elif currentState=='B^':
			result = result+'('+buf+',操作符)\n'
			buf = ""
			currentState = 'A'
			return

		##############     状态A|         #################
		elif currentState=='A|':
			if(ch=='|' or ch=='='):
				buf = buf+ch
				currentState='B|'
				return
			else:
				result = result+ '('+buf+',操作符)\n'
				buf=""
				currentState = 'A'
				continue

		##############     状态B|         #################
		elif currentState=='B|':
			result = result+'('+buf+',操作符)\n'
			buf = ""
			currentState = 'A'
			return

		##############     状态A=         #################
		elif currentState=='A=':
			if(ch=='='):
				buf = buf+ch
				currentState='B='
				return
			else:
				result = result+ '('+buf+',操作符)\n'
				buf=""
				currentState = 'A'
				continue

		##############     状态B=         #################
		elif currentState=='B=':
			result = result+'('+buf+',操作符)\n'
			buf = ""
			currentState = 'A'
			return

		##############     状态A!         #################
		elif currentState=='A!':
			if(ch=='='):
				buf = buf+ch
				currentState='B!'
				return
			else:
				result = result+ '('+buf+',操作符)\n'
				buf=""
				currentState = 'A'
				continue

		##############     状态B!         #################
		elif currentState=='B!':
			result = result+'('+buf+',操作符)\n'
			buf = ""
			currentState = 'A'
			return

		##############     状态A>         #################
		elif currentState=='A>':
			if(ch=='='):
				buf = buf+ch
				currentState='B>'
				return
			else:
				result = result+ '('+buf+',操作符)\n'
				buf=""
				currentState = 'A'
				continue

		##############     状态B>         #################
		elif currentState=='B!':
			result = result+'('+buf+',操作符)\n'
			buf = ""
			currentState = 'A'
			return

		##############     状态A<         #################
		elif currentState=='A<':
			if(ch=='='):
				buf = buf+ch
				currentState='B<'
				return
			else:
				result = result+ '('+buf+',操作符)\n'
				buf=""
				currentState = 'A'
				continue

		##############     状态B<         #################
		elif currentState=='B!':
			result = result+'('+buf+',操作符)\n'
			buf = ""
			currentState = 'A'
			return


def scanner(text):
	global mLine
	global mRow
	global buf
	global result

	buf = ""
	result = ""
	for i in xrange(0,len(text)):
		mLine += 1
		tokenizer(text[i])
		if(text[i]=='\n'):
			mRow += 1
			mLine = 0

if __name__ == '__main__':	
	scanner('System.out.println("fuck!");')
	print(result)