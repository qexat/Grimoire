# type: ignore
# ruff: noqa

"""
A beautiful fibonacci function written in the most clear and concise way.
"""

fib=(m:=globals(),(i:=lambda md:m.__setitem__(md,__import__(md)))("builtins"),i("sys"),J:=(U:="_","SIG")[1],j:=lambda *hx:U[True:].join(map(chr,hx)),p:=lambda v:v in {False,True},z:=builtins.__dict__[j(0x6C,0x65,0x6E)](()),t:=(s:=(m:=sys.modules)[U+j(115,105,103,110,97,108)],c:=m[U+j(99,111,100,101,99,115)],g:=m[j(98,117,105,108,116,105,110,115)].__dict__[j(105,110,116)],)[z].__dict__[J+g.__name__.upper()],_a:=lambda k:k.startswith(j(0o165,0o164,0o146)),tt:=list(filter(_a,c.__dict__.keys()))[(r:=~z)][t**t:t*(h:=r*(r+(z**z^r)))],ns:=t**getattr(s,j(95,95,100,105,99,116,95,95))[J+j(65,66,82,84)]+eval(tt),a:="".join(map(lambda n:chr(n+ns),x:=(eval("\x2A".join(tt)),h**t,t))),m.__setitem__(a,lambda n:n if p(n) else (y:=m[a])(n-t)+y(n+r)),l:=m[a],lambda n:print(l(n)))[-1]  # fmt: off

for i in range(10):
    fib(i)
