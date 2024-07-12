from string import Template


sss = "ssss$name"
t = Template(sss)


print(t.substitute(name="zc"))
