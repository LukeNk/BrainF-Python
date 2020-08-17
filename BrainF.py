#main

def option():
	print('Please select option:')
	print('[1] Convert BrainF input to Python file')

	while True:
		option = input('Your option:') 
		if option == '1':
			print('')
			bf_py()
		else:
			exit()

def bf_py():
	#the output indent is \t

	f_name = input('Your .py file name:')
	f = open('output/' + f_name +'.py', 'w+')
	data = input('Your BrainF code:')
	datal = len(data)

	#prepare .py file
	f.write('mem = [0]\n')
	f.write('cur = 0\n')

	#file building var
	x = 0
	b_cur = 0
	b_list = 0
	indent_l = 0
	indent = ''

	while x < datal:
		if data[x] == '+':
			f.write(indent + 'mem[cur] += 1\n')

		elif data[x] == '-':
			f.write(indent + 'mem[cur] -= 1\n')

		elif data[x] == '>':
			f.write(indent + 'cur += 1\n')
			b_cur += 1
			if b_cur > b_list:
				#because it will automatic create new memory slot, you should check to make sure you didn't create new memory slot to a loop
				#simple put >< before a loop to make it save
				f.write(indent + 'mem.append(0)\n')
				b_list += 1

		elif data[x] == '<':
			f.write(indent + 'cur -= 1\n')
			b_cur -= 1

		elif data[x] == ',':
			f.write(indent + 'mem[cur] = ord(input())\n')

		elif data[x] == '.':
			f.write(indent + 'print(chr(mem[cur]))\n')

		elif data[x] == '[':
			f.write(indent + 'while mem[cur] != 0:\n')
			indent += '\t'

		elif data[x] == ']':
			indent_l -= 1
			indent = ''
			y = 0
			while y <= indent_l:
				indent += '\t'
				y += 1

		else:
			f.write(indent + '#' + data[x] + '\n')

		x += 1

	f.close()
	print('File complied\nFile info:')
	print('Last cur position: {cur}\nMemory arrray len: {b_list}\n'.format(cur = b_cur, b_list = b_list))



option()