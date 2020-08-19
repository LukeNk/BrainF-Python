#main
import os

def option():
	while True:
		print('Please select option:')
		print('[0] Exit')
		print('[1] Convert BrainF input to Python file')
		print('[2] Convert .bf file to .py file')
		print('[3] BrainF interpreter')

		option = input('Your option: ') 
		if option == '0':
			exit()
		elif option == '1':
			print('')
			in_py()
		elif option == '2':
			print('')
			bf_py()
		elif option == '3':
			print('')
			bf_r()
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
	print('File size: ' + str(os.path.getsize('output/' + f_name + '.py')) + 'kb' + '\n')

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
	print('File size: ' + str(os.path.getsize('output/' + file_name[0:-3] + '.py')) + 'kb' +'\n')

def bf_r():
	print('BrainF interpreter')
	print('Write "!" to exit')

	while True:
		print('')
		src = input('')
		if "!" in src:
			break
		e_bf_r()



#Engines

def e_bf_py(data): #bf to py engine
	#Building var
	x = 0
	b_cur = 0 #cursor pos
	b_list = 0 #mem array len
	indent_l = 0 #indent level
	indent = '' #string contain indent
	output = '' #output
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
			output += indent + 'if cur >= len(mem):\n' #if cur is over the len(mem), add more mem
			output += indent + '\tmem.append(0)\n'

			b_cur += 1

			# if (b_cur > b_list) and in_loop == 0:
			# 	output += indent + 'mem.append(0)\n'
			# 	b_list += 1
			# elif (b_cur > b_list) and (in_loop != 0): #if in loop and new mem slot need to create
			# 	loop_new += 1


		elif data[x] == '<':
			output += indent + 'cur -= 1\n'
			b_cur -= 1

		elif data[x] == ',':
			output += indent + 'mem[cur] = ord(input())\n'

		elif data[x] == '.':
			output += indent + 'print(chr(mem[cur]), end="")\n'

		elif data[x] == '[':
			# if in_loop == 0: #if not in loop (first loop)
			# 	output += indent + '{loop_data}\n' #write a {} so we can write data in later

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
	return(output, info) #add loop data


def e_bf_r():
	source = input()
	import collections
	loop_ptrs = {}
	loop_stack = []
	for ptr, opcode in enumerate(source):
		if opcode == '[': loop_stack.append(ptr)
		if opcode == ']':
			if not loop_stack:
				source = source[:ptr]
				break
			sptr = loop_stack.pop()
			loop_ptrs[ptr], loop_ptrs[sptr] = sptr, ptr
	if loop_stack:
		raise SyntaxError ("unclosed loops at {}".format(loop_stack))
	mem = collections.defaultdict(int)
	cur = 0
	ptr = 0
	while ptr < len(source):
		opcode = source[ptr]
		if   opcode == '>': cur += 1
		elif opcode == '<': cur -= 1
		elif opcode == '+': mem[cur] += 1
		elif opcode == '-': mem[cur] -= 1
		elif opcode == ',': mem[cur] = input()
		elif opcode == '.': print(chr(mem[cur]), end='')
		elif (opcode == '[' and not mem[cur]) or (opcode == ']' and mem[cur]): 
			ptr = loop_ptrs[ptr]
		ptr += 1
	

if __name__ == "__main__":
	option()
