import os

#filein = open("../output_files/based_split.csv","r")
#fileout = open("./based_split.csv","w")

pathin = "../output_files/"

files = sorted(os.listdir("%s"%pathin))

arqs = len(files)

arq=0
for file in files:
	if "bias" in file or "weights" in file:
		arqs = arqs-1
		continue

	fileout = open("./out_%s"%file,"w")

	filein = open("%s/%s"%(pathin,file),"r")

	lines = filein.readlines()

	line=0
	i=0
	print("processando... (%s)"%file)
	while line != lines[-1]:
		line=lines[i];
		i+=1
		linha = line.strip("\n")

		try:
			cols = line.split(";")
			colf,colx,coly,colb,dummy = cols[-5],cols[-4],cols[-3],cols[-2],cols[10]
		except:
			continue
		
		linej = line
		j=i
		while linej != lines[-1]:
			linej=lines[j]
			j+=1

			try:
				cols = linej.split(";")
				colf2,colx2,coly2,colb2,colrd = cols[0],cols[1],cols[2],cols[3],cols[4]
			except:
				continue

			if ((colf == colf2) and (colx == colx2) and (coly == coly2)):
				if colb == colb2:
					linha = linha + "%s"%colrd
					break;
				elif (colb != colb2) and (colrd == "1"):
					linha = linha + "0"
					break;

			#if linej == lines[-1]:
				#print(linha)
				#print("EOF")

		fileout.write(linha)
		fileout.write("\n")
		fileout.close
	arq+=1
	print("Concluido %s de %s! (%s)\n"%(arq,arqs,file))
print("FIM! Concluidos %s de %s arquivos!"%(arq,arqs))
