#main
import os

def option():
	while True:
		print('Please select option:')
		print('[0] Exit')
		print('[1] Convert BrainF input to Python file')
		print('[2] Convert .bf file to .py file')

		option = input('Your option: ') 
		if option == '0':
			exit()
		elif option == '1':
			print('')
			in_py()
		elif option == '2':
			print('')
			bf_py()
		else:
			print('Wrong option (Please select the number)')

def in_py():
	#the output indent is \t

	f_name = input('Your .py file name:')
	f = open('output/' + f_name +'.py', 'w+')
	data = input('\nYour BrainF code:')

	#create .bf file
	a = open('output/' + f_name + '.bf', 'w+')
	a.write(data)
	a.close()

	#get output
	out, info = e_bf_py(data)
	f.write(out)
	print('')
	print(info)
	print('File size: ' + str(os.path.getsize('output/' + f_name + '.py')) + ' bytes' +'\n')

def bf_py():
	path = input('Please input your .bf file path: ')
	file_name = os.path.basename(path)
	f = open(path, 'r')
	out, info = e_bf_py(f.read())
	f.close()
	a = open('output/' + file_name[0:-3] + '.py', 'w+')
	a.write(out)
	print('')
	print(info)
	print('File size: ' + str(os.path.getsize('output/' + file_name[0:-3] + '.py')) + ' bytes' +'\n')

#Engines
def e_bf_py(data): #bf to py engine
	#Building var
	x = 0
	b_cur = 0
	b_list = 0
	indent_l = 0
	indent = ''
	output = ''
	datal = len(data)
	in_loop = 0 #0 mean not in any loop
	loop_new = 0 #mem slot need to create BEFORE enter the first loop

	#build prepare
	output += 'mem = [0]\n'
	output += 'cur = 0\n'

	while x < datal:
		if data[x] == '+':
			output += indent + 'mem[cur] += 1\n'

		elif data[x] == '-':
			output += indent + 'mem[cur] -= 1\n'

		elif data[x] == '>':
			#because it will automatic create new memory slot, you should check to make sure you didn't create new memory slot to a loop
			#simple put >< before a loop to make it save
			output += indent + 'cur += 1\n'
			b_cur += 1

			if (b_cur > b_list) and in_loop == 0:
				output += indent + 'mem.append(0)\n'
				b_list += 1
			elif (b_cur > b_list) and (in_loop != 0): #if in loop and new mem slot need to create
				loop_new += 1


		elif data[x] == '<':
			output += indent + 'cur -= 1\n'
			b_cur -= 1

		elif data[x] == ',':
			output += indent + 'mem[cur] = ord(input())\n'

		elif data[x] == '.':
			output += indent + 'print(chr(mem[cur]), end="")\n'

		elif data[x] == '[':
			if in_loop == 0: #if not in loop (first loop)
				output += indent + '{loop_data}\n' #write a {} so we can write data in later

			output += indent + 'while mem[cur] != 0:\n'
			indent_l += 1
			indent += '\t'
			in_loop += 1

		elif data[x] == ']':
			indent_l -= 1
			indent = ''
			y = 0
			while y <= indent_l:
				indent += '\t'
				y += 1

		else:
			output += indent + '#' + data[x] + '\n'

		x += 1

	#add loop_data about 
	y = 0
	loop_add = ''
	while y < loop_new:
		loop_add += 'mem.append(0)\n'
		y += 1

	outputf = output.format(loop_data = loop_add)

	info = 'Build completed\nBuild info:\nCharacter count: {char}\nLast cur position: {cur}\nMemory arrray len: {b_list}\nLoop level: {loops}'.format(char = x, cur = b_cur, b_list = b_list+1, loops = in_loop)
	return(outputf, info) #add loop data

option()
