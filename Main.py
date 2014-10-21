#coding:utf-8


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
__switchCharSet__ = {'b', 'n', 't', '\'', '\"','\\'}
# 由ANSI标准定义的C语言关键字共32个：
__keywordSet__ = {'auto','double','int','struct','break','else','long','switch','case','enum',
				'register','typedef','char','extern','return','union','const','float','short','unsigned',
				'continue','for','signed','void','default','goto','sizeof','volatile','do','if',
				'while','static'
				}
__boardSet__ = {';',',', '(', ')', '.', '{', '}','[',']'}
console_msg=""
result=[]
__TOKENIZE_SUCCESS__ = 0
__TOKEN_ERROR__ = 1


def compilerFail(status):
	global mLine
	global mRow
	global buf
	global console_msg
	global currentState

	console_msg = console_msg + "编译于第 "+str(mRow)+" 行, 第 "+str(mLine)+" 列失败,因为:"+status+'\n'
	currentState='A'
	buf = ""


def tokenizer(ch):
	global buf
	global mLine
	global mRow
	global currentState
	global __letterSet__
	global __digitSet__
	global __blankCharSet__
	global __keywordSet__
	global console_msg
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
				console_msg = console_msg+'('+ch+' , 界符)\n'
				result.append(ch)
				currentState='A'
				return
			elif(ch=='$'):
				buf = buf + ch
				currentState='$'
			else:
				compilerFail('不可识别的字符')
				return

		##############     状态B         #################
		elif currentState == 'B':
			if(ch == '_' or ch in __letterSet__ or ch in __digitSet__):
				buf = buf+ch
				currentState = 'B'
				return
			else:#可接受状态
				if (buf in __keywordSet__):
					console_msg = console_msg + '('+buf+' , 关键字)\n'
					result.append(buf)
				else:
					console_msg = console_msg + '('+buf+' , 标识符)\n'
					result.append('IDN')
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
				console_msg = console_msg + '('+ buf + ' , 整数常量)\n'
				result.append('INUM')
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
			else:
				compilerFail('空白或无效的字符')
				return

		##############     状态E        #################
		elif currentState == 'E':
			if(ch=='\''):
				buf = buf+ch
				currentState = 'H'
				continue
			else:
				compilerFail('字符常量长度大于一')
				return

		##############     状态H        #################
		elif currentState == 'H':
			console_msg = console_msg + '(' + buf+ ' ,字符常量)\n'
			result.append['CH']
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
				compilerFail('无效的转义字符')		
				return	

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
				compilerFail('无效的转义字符')	
				return

		##############     状态J         #################
		elif currentState == 'J':
			console_msg = console_msg + '(' + buf+ ' ,字符串常量)\n'
			result.append('STR')
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
				console_msg = console_msg+'('+buf+' ,运算符)\n'
				result.append(buf)
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
		##############     状态M         #################
		elif currentState=='M':
			if(ch=='/'):
				currentState = 'N'
				return
			else:
				currentState='L'

		##############     状态N         #################
		elif currentState=='N':
			currentState = 'A'
			return

		##############     状态O         #################
		elif currentState=='O':
			if(ch=='\n'):
				currentState = 'A'
				return
			else:
				currentState='O'
				return

		##############     状态P         #################
		elif currentState=='P':
			if(ch in __digitSet__):
				buf = buf+ch
				currentState = 'Q'
				return
			else:
				compilerFail('无效的浮点数')
				return

		##############     状态Q         #################
		elif currentState=='Q':
			if(ch in __digitSet__):
				buf = buf+ch
				currentState='Q'
				return
			else:
				console_msg = console_msg+'('+buf+' , 浮点数常量)\n'
				result.append('FNUM')
				buf=""
				currentState='A'
				continue

		##############     状态A+         #################
		elif currentState=='A+':
			if(ch=='+' or ch=='='):
				buf = buf+ch
				currentState='B+'
				return
			else:
				console_msg = console_msg+'('+buf+' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B+         #################
		elif currentState=='B+':
			console_msg = console_msg+'('+buf+' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue

		##############     状态A-         #################
		elif currentState=='A-':
			if(ch=='-' or ch=='='):
				buf = buf+ch
				currentState='B-'
				return
			else:
				console_msg = console_msg+'('+buf+' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B-         #################
		elif currentState=='B-':
			console_msg = console_msg+'('+buf+' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue

		##############     状态A*         #################
		elif currentState=='A*':
			if(ch=='*' or ch=='='):
				buf = buf+ch
				currentState='B*'
				return
			else:
				console_msg = console_msg+'('+buf+' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B*         #################
		elif currentState=='B(':
			console_msg = console_msg+'('+buf+' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue

		##############     状态A&         #################
		elif currentState=='A&':
			if(ch=='&' or ch=='='):
				buf = buf+ch
				currentState='B&'
				return
			else:
				console_msg = console_msg+'('+buf+' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B&         #################
		elif currentState=='B&':
			console_msg = console_msg+'('+buf+' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue

		##############     状态A^         #################
		elif currentState=='A^':
			if(ch=='^' or ch=='='):
				buf = buf+ch
				currentState='B^'
				return
			else:
				console_msg = console_msg+ '('+buf+' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B^         #################
		elif currentState=='B^':
			console_msg = console_msg+'('+buf+' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue

		##############     状态A|         #################
		elif currentState=='A|':
			if(ch=='|' or ch=='='):
				buf = buf+ch
				currentState='B|'
				return
			else:
				console_msg = console_msg+ '('+buf+' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B|         #################
		elif currentState=='B|':
			console_msg = console_msg+'('+buf+' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue

		##############     状态A=         #################
		elif currentState=='A=':
			if(ch=='='):
				buf = buf+ch
				currentState='B='
				return
			else:
				console_msg = console_msg+ '('+buf+' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B=         #################
		elif currentState=='B=':
			console_msg = console_msg+'('+buf+' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue

		##############     状态A!         #################
		elif currentState=='A!':
			if(ch=='='):
				buf = buf+ch
				currentState='B!'
				return
			else:
				console_msg = console_msg+ '('+buf+' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B!         #################
		elif currentState=='B!':
			console_msg = console_msg+'('+buf+' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue

		##############     状态A>         #################
		elif currentState=='A>':
			if(ch=='='):
				buf = buf+ch
				currentState='B>'
				return
			else:
				console_msg = console_msg+ '('+buf+' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B>         #################
		elif currentState=='B!':
			console_msg = console_msg+'('+buf+' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue

		##############     状态A<         #################
		elif currentState=='A<':
			if(ch=='='):
				buf = buf+ch
				currentState='B<'
				return
			else:
				console_msg = console_msg+ '('+buf+' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B<         #################
		elif currentState=='B!':
			console_msg = console_msg+'('+buf+' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue
		
		##############     状态$         #################
		elif currentState=='$':
			console_msg = console_msg+'('+buf+' ,终结符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			return
		
		


def scanner(text):
	global mLine
	global mRow
	global buf
	global console_msg
	global currentState

	buf = ""
	console_msg = ""
	for i in xrange(0,len(text)):
		# console_msg=console_msg+'进入scanner\n'
		mLine = mLine+1
		tokenizer(text[i])
		if(text[i]=='\n'):
			mRow += 1
			mLine = 0
	tokenizer('$')
		
			
def main():
	global result,console_msg
	fp = open('code.c','r')
	scanner(fp.read())
# 	console_msg= console_msg+'($,结束符)\n'
# 	result.append('$')
	print(console_msg)
	print(result)
	return result
	

if __name__ == '__main__':
	main()
	