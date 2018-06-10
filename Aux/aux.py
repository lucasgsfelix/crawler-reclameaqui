def leitura():
	
	arq = open("links_proibidos", "r")
	info = arq.read()
	info = info.split('\n')
	arq.close()
	i=1
	while(i<len(info)):
		if info[i] == info[i-1]:
			info.pop(i-1)
			i=i-1
		i=i+1

	arq = open("links_proibidos", "w")

	i=0
	while(i<len(info)):

		if i<len(info)-2:
			arq.write(info[i]+'\n')
		else:
			arq.write(info[i])

		i=i+1

	arq.close()

leitura()

