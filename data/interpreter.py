#brainF interpreter

def e_bf_r(source):
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
	e_bf_r("
