# type: ignore
"""
The classic "Hello World!" program running in a Brainfuck interpreter embedded in an f-string.
"""


f'{(hw:="++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.")}{(bf:=lambda prgm:print(((pc:=0),(ti:=0),(t:=[0]*30000),(rs:=[]),(o:=""),(*(((char:=prgm[pc]),(((ti:=ti+1),(pc:=pc+1))if char==">"else(((ti:=ti-1),(pc:=pc+1))if char=="<"else(((t.__setitem__(ti,(t[ti]+1)&0xFF)),(pc:=pc+1))if char=="+"else(((t.__setitem__(ti,(t[ti]-1)&0xFF)),(pc:=pc+1))if char=="-"else(((o:=o+chr(t[ti])),(pc:=pc+1))if char=="."else(((t.__setitem__(ti,ord(input())%0xFF)),(pc:=pc+1))if char==","else(((rs.append(pc),(pc:=pc+1))if t[ti]!=0 else((bc:=1),(*(((pc:=pc+1),((bc:=bc+1)if prgm[pc]=="["else(bc:=bc-1)if prgm[pc]=="]"else...),(pc:=pc+1))for _ in iter(lambda:bool(bc),False)),)))if char=="["else((pc:=rs.pop())if char=="]"else...)))))))))for _ in iter(lambda:pc<len(prgm),False)),))[-1][-1][-1][0]))}{(bf(hw))}'
