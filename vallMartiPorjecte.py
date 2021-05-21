from tkinter import * #importem les llibreries del Tkinter
from tkinter import ttk
from PIL import ImageTk, Image


from subprocess import PIPE, Popen #importem les funcions de sistema
import subprocess
import threading # llibraria x separaar procesos
import time




import pyautogui as pya #llibreria enviar tecles
import pyperclip 


import webbrowser # llibreria per obrir explorador



"""
Funció que s'executa en clicar el boto "botoDescarregaFitxer".
- Executa la comanda sshpass per fer un scp al servidor remot autenticant-se
amb una contrasenya que perquè no es vegi en el codi la tenim en el fitxer
contraseny.txt del mateix directori on executem aquest codi.
- Captura la sortida de la comanda sshpass i la posa en un widget tipus Text i 
si la transferència ha estat exitosa també hi posa el contingut del fitxer transferit."

"""


"""
responsive imatge
def resizer(*args):
	t2 = threading.Thread(target=resizer1, args=[]).start() # aixo arregla problemes importants i millora bastnat considerablement el rendiment i al fer comandes pots seguir treballant en tot el programa

def resizer1(*args):
	global x,y,resize_image,im,img,logo,xA,finestra
	
	time.sleep(3)
	x = logo.winfo_width()
	y = logo.winfo_height()
	resize_image = im.resize((x, y))
	img = ImageTk.PhotoImage(resize_image)
	logo = Label(marc6,image=img)
	logo.grid(column=1, row=0, sticky='nsew')
	resp = 1
"""




def tancar(*args):
	try:
		proces.kill()
	except:
		pass
	try:
		m.destroy()
	except:
		pass
	try:
		finestra.destroy()
	except:
		pass
	try:
		i.destroy()
	except:
		pass

	sys.exit()




def popup_destroy(*args):
	try:
		m.destroy()
	except:
		pass


def informacio():
	programa.select(6)

def about():
	webbrowser.open('https://wiki.martivall.cat') # ip wiki

def ajuda():
	webbrowser.open('https://martivall.cat') # ip wordpres

def cut():
	pya.hotkey('ctrl', 'x')

def copia():
	pya.hotkey('ctrl', 'c')

def enganxa():
	pya.hotkey('ctrl', 'v')


def popup(event):
	global m

	m = Menu(finestra, tearoff = 0)# pk no apareixi ratlla a
	m.add_command(label ="retalla", command=cut)
	m.add_command(label ="copia", command=copia)
	m.add_command(label ="enganxa", command=enganxa)
	m.add_separator()
	m.add_command(label ="informació", command=informacio)
	m.add_command(label ="ajuda", command=ajuda)
	m.add_command(label="about us", command=about)
	m.add_separator()
	m.add_command(label ="canviar servidor", command=lambda: principi(1))
	m.add_command(label ="sortir", command=tancar)
	try:
		m.tk_popup(event.x_root, event.y_root)
	finally:
		m.grab_release()


def terminal(*args):
	t1 = threading.Thread(target=terminal1, args=[]).start() # aixo arregla problemes importants i millora bastnat considerablement el rendiment i al fer comandes pots seguir treballant en tot el programa

def terminal1():
	global terminalText1,terminalText2, tag, textpwd, pwdtext, usuari, IP, proces

	terminalText2.tag_config("comand", background="black", foreground="yellow", selectbackground="green", selectforegroun="white") 
	terminalText2.tag_config("result", background="black", foreground="white", selectbackground="green", selectforegroun="white")
	terminalText2.tag_config("pwdT", background="black", foreground="brown", selectbackground="green", selectforegroun="white")
	terminalText2.tag_config("error", background="black", foreground="red", selectbackground="green", selectforegroun="white")

	#print(terminalText1.get(1.0,"end"))
	#print(len(terminalText1.get(1.0,"end")))
	if len(terminalText1.get(1.0,"end")) < 2 or terminalText1.get(1.0) == '\n':
		terminalText1.delete(1.0,"end")
		text="Introduïu alguna comanda siusplau\n"
		terminalText2.insert(END,text, "error")

	else:

		try:
			proces.kill()
		except:
			pass

		text1 = terminalText1.get(1.0,END)
		#print(text1)
		if text1[-2] == '\n':
			text1 = text1[:-1]
		terminalText2.insert(END,"$ "+text1, "comand")
		terminalText1.delete(1.0,"end")

		comanda = text1.split()

		proces=subprocess.Popen(['sshpass','-p', contra, 'ssh', usuari + '@' + IP]+['cd', '']+textpwd+['','&&', '']+comanda+['', '&&', 'pwd']+comanda,stdout=PIPE,stderr=PIPE, stdin=PIPE)

		# prototip de petar procesos al cert temps

		#petar procesos si tarden molt
		pKillejat = False
		#posar boto x activar/desactivar aquesta opcio i unaltra boto d matr procesos
		"""
		start = time.time()
		while proces.poll() == None:
			stop = time.time()
			if (stop - start) >= 20: # sec x petar
				pKillejat = True
				#proces.kill()
				proces.terminate()
		"""

		tproces=proces.stdout.read()
		proces.stdout.close()


		textError=proces.stderr.read()
		proces.stderr.close() # tanquem la tuberia

		#proces.wait()


		if not textError:
			# arreglar surtida
			textBo=tproces.decode()
			# x poder treballar amb el resultat
			textpwdSplit = textBo.split()
			if pKillejat == False:
				# agafar l'ultim resultat
				textpwdstr = textpwdSplit[-1]
				#print(textpwdstr)
				Comprovacio = textpwdstr[0] # x arreglar un bug en comandes complexes o al matar proces anterior
				if Comprovacio[0] == "/":
					textpwd = []
					textpwd.append(textpwdstr) # afegir l'ultim resultat a la llista x aillar el resultat de pwd i aixi poder anar sempre aki i set guuardi el lloc
				else:
					textpwdstr = ''.join(textpwd)
			else:
				textpwdstr = ''.join(textpwd)
			pwdtext= '#### '+ usuari + '@'+ IP + ':' + textpwdstr + ' ####\n'# + text
			"""
			num =0
			for x in text:
				if x == "\n":
					num += 1
					print(num)
			num2=0
			cont=0
			for y in text:
				cont += 1
				if y =="\n":
					num2 +=1
				if num2 == num:
					del text[cont]
			"""


			#text = textpwdSplit[-1:] + textpwdSplit[:-1]

			#text = ''.join(textl)

		else:
			textError=textError.decode()
			textpwdstr = ''.join(textpwd)
			pwdtext= '#### '+ usuari + '@'+ IP + ':' + textpwdstr + ' ####\n'# + text



		try:
			terminalText2.insert(END,pwdtext, "pwdT")
		except:
			pass
		try:
			terminalText2.insert(END,textBo, "result")
		except:
			pass
		try:
			terminalText2.insert(END,textError, "error")
		except:
			pass
	terminalText2.see("end")


def enviarArx():
	global ex3Text2, ex3Text1

	# x no liarla
	if len(ex3Text1.get(1.0,"end")) < 20:
		text="\nAgafa el fitxer de configuració del apache siusplau\n"
		ex3Text2.insert(END,text)
	else:
		punter = open("apache2.conf","w")
		punter.write(ex3Text1.get(1.0,"end"))
		punter.close()
		proces=Popen(['sshpass','-p', contra, 'scp', 'apache2.conf', usuari + '@' + IP+':/etc/apache2/'],
			stdout=PIPE,stderr=PIPE, stdin=PIPE)

		finestra.after(300) # un sleep pk doni temps a ke s'actualiitzi la informació dels sistemes

		tproces=proces.stdout.read()
		proces.stdout.close()

		textError=proces.stderr.read()
		proces.stderr.close() # tanquem la tuberia

		if not textError:
			text="### Pasant l'arxiu al servidor ###\n"+str(tproces.decode()+"\n#### Arxiu pasat al servidor satisfactoriament #####\n")

		else:
			text="######\n"+str(textError.decode()+"\n######\n")
			
		ex3Text2.insert(END,text)


		proces=Popen(['sshpass','-p', contra, 'ssh', usuari + '@' + IP]+['systemctl','restart', 'apache2'],
		stdout=PIPE,stderr=PIPE, stdin=PIPE)

		finestra.after(300) # un sleep pk doni temps a ke s'actualiitzi la informació dels sistemes

		tproces=proces.stdout.read()
		proces.stdout.close()

		textError=proces.stderr.read()
		proces.stderr.close() # tanquem la tuberia

		if not textError:
			text="### Reiniciant apache ###\n"+str(tproces.decode()+"\n#### apache reiniciat correctament #####\n")

		else:
			text="### Reiniciant apache ###\n"+str(textError.decode()+"\n### error al reiniciar l'apache ###\n")
			
		ex3Text2.insert(END,text)




def agafarArx():
	global ex3Text1

	proces=Popen(['sshpass','-p', contra, 'ssh', usuari + '@' + IP]+['cat','/etc/apache2/apache2.conf'],
		stdout=PIPE,stderr=PIPE, stdin=PIPE)


	tproces=proces.stdout.read()
	proces.stdout.close()

	textError=proces.stderr.read()
	proces.stderr.close() # tanquem la tuberia

	if not textError:
		text=str(tproces.decode())

	else:
		text=str(textError.decode())
		
	ex3Text1.delete(1.0,"end")
	ex3Text1.insert(END,text)

def pasarArxApache():
	
	proces=Popen(['sshpass','-p', contra,
			'scp',ex2Entry.get() ,usuari+'@'+IP+':/etc/apache2/apache2.conf'],
			stdout=PIPE,stderr=PIPE, stdin=PIPE)

	proces=Popen(['sshpass','-p', contra, 'ssh', usuari + '@' + IP]+['systemctl','restart', 'apache2'],
	stdout=PIPE,stderr=PIPE, stdin=PIPE)

	finestra.after(300) # un sleep pk doni temps a ke s'actualiitzi la informació dels sistemes

	tproces=proces.stdout.read()
	proces.stdout.close()

	textError=proces.stderr.read()
	proces.stderr.close() # tanquem la tuberia

	if not textError:
		text="### Reiniciant apache ###\n"+str(tproces.decode()+"\n#########\n")

	else:
		text="### Reiniciant apache ###\n"+str(textError.decode()+"\n######\n")
		
	ex2Text.insert(END,text)
	#print(ex2Text.get(1.0,END))


def pasarConfApache():

	global ex1Entry

	process=Popen(['sshpass','-p', contra, 'ssh', usuari + '@' + IP]+['echo', ex1Entry.get(), '>>', '/etc/apache2/apache2.conf'],
		stdout=PIPE,stderr=PIPE, stdin=PIPE)

	finestra.after(300) # un sleep pk doni temps a ke s'actualiitzi la informació dels sistemes


	proces=Popen(['sshpass','-p', contra, 'ssh', usuari + '@' + IP]+['cat','/etc/apache2/apache2.conf'],
		stdout=PIPE,stderr=PIPE, stdin=PIPE)

	finestra.after(300) # un sleep pk doni temps a ke s'actualiitzi la informació dels sistemes

	tproces=proces.stdout.read()
	proces.stdout.close()

	finestra.after(300) # un sleep pk doni temps a ke s'actualiitzi la informació dels sistemes

	textError=proces.stderr.read()
	proces.stderr.close() # tanquem la tuberia

	if not textError:
		text="######\n"+str(tproces.decode()+"\n#########\n")

	else:
		text=textError

	ex1Text.insert(END,text)

	proces=Popen(['sshpass','-p', contra, 'ssh', usuari + '@' + IP]+['systemctl','restart', 'apache2'],
	stdout=PIPE,stderr=PIPE, stdin=PIPE)

	finestra.after(300) # un sleep pk doni temps a ke s'actualiitzi la informació dels sistemes


	tproces=proces.stdout.read()
	proces.stdout.close()

	textError=proces.stderr.read()
	proces.stderr.close() # tanquem la tuberia

	if not textError:
		text="### Reiniciant apache ###\n"+str(tproces.decode()+"\n#########\n")

	else:
		text="### Reiniciant apache ###\n"+str(textError.decode()+"\n######\n")
		
	ex1Text.insert(END,text)





	"""
	textError=proces.stderr.read()
	proces.stderr.close() # tanquem la tuberia
	textOK=proces.stdout.read()
	proces.stdout.close()# tanquem la tuberia
	if not textError:





		p_cat=Popen(['cat', 'interfaces'],stdout=PIPE,stderr=PIPE, stdin=PIPE)

		t_cat=p_cat.stdout.read()
		p_cat.stdout.close()# tanquem la tuberia
		text="######\nFitxer descarregat correctament\n"+str(t_cat.decode())+"\n######\n"

	else:
		text=textError

	"""



def descarregaCarpeta():
	carpeta = ruta2.get()
	print(carpeta)
	proces=Popen(['sshpass','-p', contra,
			'scp','-r',usuari+'@'+IP+':'+carpeta,'.'],
			stdout=PIPE,stderr=PIPE, stdin=PIPE)
	
	textError=proces.stderr.read()
	proces.stderr.close() # tanquem la tuberia
	textOK=proces.stdout.read()
	proces.stdout.close()# tanquem la tuberia
	if not textError:

		carpetaS = carpeta.split('/')
		carpetaR = carpetaS[-1]

		if carpetaR == '':
			carpetaR = carpetaS[-2] # pk printegi sempre be en el format acavat en /

		p_cat=Popen(['tree', carpetaR],stdout=PIPE,stderr=PIPE, stdin=PIPE)

		t_cat=p_cat.stdout.read()
		p_cat.stdout.close()# tanquem la tuberia
		text="######\nCarpeta descarregada correctament\n"+str(t_cat.decode())+"\n######\n"

	else:
		text=textError

	T2.insert(END,text) # posem el resultat de la comanda en el widget Text



def descarregaFitxer():
	fitxer = ruta1.get()
	proces=Popen(['sshpass','-p', contra,
			'scp',usuari+'@'+IP+':'+fitxer,'.'],
			stdout=PIPE,stderr=PIPE, stdin=PIPE)
	
	textError=proces.stderr.read()
	proces.stderr.close() # tanquem la tuberia
	textOK=proces.stdout.read()
	proces.stdout.close()# tanquem la tuberia
	if not textError:
		fitxerS = fitxer.split('/')
		fitxerR = fitxerS[-1]

		p_cat=Popen(['cat', fitxerR],stdout=PIPE,stderr=PIPE, stdin=PIPE)

		t_cat=p_cat.stdout.read()
		p_cat.stdout.close()# tanquem la tuberia
		text="######\nFitxer descarregat correctament######\n\n######\n"+str(t_cat.decode())+"\n######\n"

	else:
		text=textError

	T.insert(END,text) # posem el resultat de la comanda en el widget Text


def start(widget,servei):
	t3 = threading.Thread(target=start1, args=(widget,servei)).start() # aixo arregla problemes importants i millora bastnat considerablement el rendiment i al fer comandes pots seguir treballant en tot el programa


def start1(widget,servei):
	logsText.tag_config("comand", background="black", foreground="yellow", selectbackground="green", selectforegroun="white") 
	logsText.tag_config("result", background="black", foreground="white", selectbackground="green", selectforegroun="white")
	logsText.tag_config("error", background="black", foreground="red", selectbackground="green", selectforegroun="white")
	
	logsText.insert(END,"$ "+"systemctl start "+ servei+"\n", "comand")
	
	widget.configure(background="gray")
	proces=subprocess.Popen(['sshpass','-p', contra, 'ssh', 'root' + '@' + IP]+['systemctl', 'start',servei],stdout=PIPE,stderr=PIPE, stdin=PIPE)

	tproces=proces.stdout.read()
	proces.stdout.close()

	textError=proces.stderr.read()
	proces.stderr.close() # tanquem la tuberia

	if not textError:
		textBo=tproces.decode()
		#print(textBo)
		logsText.insert(END,textBo, "result")


	else:
		textError=textError.decode()
		#print(textError)
		logsText.insert(END,textError, "error")


	proces=subprocess.Popen(['sshpass','-p', contra, 'ssh', 'root' + '@' + IP]+['systemctl', 'show','--property','LoadState,ActiveState',servei],stdout=PIPE,stderr=PIPE, stdin=PIPE)

	t5 = threading.Thread(target=refresh1, args=(widget,servei)).start() # aixo arregla problemes importants i millora bastnat considerablement el rendiment i al fer comandes pots seguir treballant en tot el programa



def stop(widget,servei):
	t4 = threading.Thread(target=stop1, args=(widget,servei)).start() # aixo arregla problemes importants i millora bastnat considerablement el rendiment i al fer comandes pots seguir treballant en tot el programa


def stop1(widget,servei):
	logsText.tag_config("comand", background="black", foreground="yellow", selectbackground="green", selectforegroun="white") 
	logsText.tag_config("result", background="black", foreground="white", selectbackground="green", selectforegroun="white")
	logsText.tag_config("error", background="black", foreground="red", selectbackground="green", selectforegroun="white")
	
	logsText.insert(END,"$ "+"systemctl start "+ servei+"\n", "comand")
	
	widget.configure(background="gray")
	proces=subprocess.Popen(['sshpass','-p', contra, 'ssh', 'root' + '@' + IP]+['systemctl', 'stop',servei],stdout=PIPE,stderr=PIPE, stdin=PIPE)

	tproces=proces.stdout.read()
	proces.stdout.close()

	textError=proces.stderr.read()
	proces.stderr.close() # tanquem la tuberia

	if not textError:
		textBo=tproces.decode()
		#print(textBo)
		logsText.insert(END,textBo, "result")


	else:
		textError=textError.decode()
		#print(textError)
		logsText.insert(END,textError, "error")


	proces=subprocess.Popen(['sshpass','-p', contra, 'ssh', 'root' + '@' + IP]+['systemctl', 'show','--property','LoadState,ActiveState',servei],stdout=PIPE,stderr=PIPE, stdin=PIPE)

	t5 = threading.Thread(target=refresh1, args=(widget,servei)).start() # aixo arregla problemes importants i millora bastnat considerablement el rendiment i al fer comandes pots seguir treballant en tot el programa



def restart(widget,servei):
	t4 = threading.Thread(target=restart1, args=(widget,servei)).start() # aixo arregla problemes importants i millora bastnat considerablement el rendiment i al fer comandes pots seguir treballant en tot el programa


def restart1(widget,servei):
	logsText.tag_config("comand", background="black", foreground="yellow", selectbackground="green", selectforegroun="white") 
	logsText.tag_config("result", background="black", foreground="white", selectbackground="green", selectforegroun="white")
	logsText.tag_config("error", background="black", foreground="red", selectbackground="green", selectforegroun="white")
	
	logsText.insert(END,"$ "+"systemctl start "+ servei+"\n", "comand")
	
	widget.configure(background="gray")
	proces=subprocess.Popen(['sshpass','-p', contra, 'ssh', 'root' + '@' + IP]+['systemctl', 'restart',servei],stdout=PIPE,stderr=PIPE, stdin=PIPE)

	tproces=proces.stdout.read()
	proces.stdout.close()

	textError=proces.stderr.read()
	proces.stderr.close() # tanquem la tuberia

	if not textError:
		textBo=tproces.decode()
		#print(textBo)
		logsText.insert(END,textBo, "result")


	else:
		textError=textError.decode()
		#print(textError)
		logsText.insert(END,textError, "error")
	
	t5 = threading.Thread(target=refresh1, args=(widget,servei)).start() # aixo arregla problemes importants i millora bastnat considerablement el rendiment i al fer comandes pots seguir treballant en tot el programa

def refresh(widget,servei):
	t7 = threading.Thread(target=refresh1, args=(widget,servei)).start() # aixo arregla problemes importants i millora bastnat considerablement el rendiment i al fer comandes pots seguir treballant en tot el programa


def refresh1(widget,servei):
	logsText.tag_config("comand", background="black", foreground="yellow", selectbackground="green", selectforegroun="white") 
	logsText.tag_config("result", background="black", foreground="white", selectbackground="green", selectforegroun="white")
	logsText.tag_config("error", background="black", foreground="red", selectbackground="green", selectforegroun="white")
	
	logsText.insert(END,"$ "+"systemctl show --property LoadState,ActiveState "+ servei+"\n", "comand")


	proces=subprocess.Popen(['sshpass','-p', contra, 'ssh', 'root' + '@' + IP]+['systemctl', 'show','--property','LoadState,ActiveState',servei],stdout=PIPE,stderr=PIPE, stdin=PIPE)

	tproces=proces.stdout.read()
	proces.stdout.close()

	textError=proces.stderr.read()
	proces.stderr.close() # tanquem la tuberia

	if not textError:
		textBo=tproces.decode()
		#print(textBo)
		logsText.insert(END,textBo, "result")
		texta= textBo.split()
		#print(texta)
		if texta[0]=="LoadState=not-found" and texta[1]=="ActiveState=inactive":
			widget.configure(background="gray")
		
		if texta[0]=="LoadState=loaded" and texta[1]=="ActiveState=inactive":
			widget.configure(background="red")

		if texta[0]=="LoadState=loaded" and texta[1]=="ActiveState=active":
			widget.configure(background="green")
		logsText.see("end")


	else:
		textError=textError.decode()
		#print(textError)
		logsText.insert(END,textError, "error")
		logsText.see("end")


def refreshAll():
	widget=[apacheE,webminE,bindE, sshE,dhcpE,nfsE,ftpE]
	servei=['apache2','webmin','bind9','ssh','isc-dhcp-server','nfs-kernel-server','vsftpd']
	nu=0
	for x in servei:
		t = threading.Thread(target=refresh1, args=(widget[nu],servei[nu])).start() # aixo arregla problemes importants i millora bastnat considerablement el rendiment i al fer comandes pots seguir treballant en tot el programa
		nu +=1

	"""
	terminalText2.tag_config("comand", background="black", foreground="yellow", selectbackground="green", selectforegroun="white") 
	terminalText2.tag_config("result", background="black", foreground="white", selectbackground="green", selectforegroun="white")
	terminalText2.tag_config("pwdT", background="black", foreground="brown", selectbackground="green", selectforegroun="white")
	terminalText2.tag_config("error", background="black", foreground="red", selectbackground="green", selectforegroun="white")
		terminalText2.insert(END,text, "error")
		try:
			terminalText2.insert(END,pwdtext, "pwdT")
		except:
			pass
		try:
			terminalText2.insert(END,textBo, "result")
		except:
			pass
		try:
			terminalText2.insert(END,textError, "error")
		except:
			pass
	terminalText2.see("end")

	"""



def select(*args):
	p = programa.index(programa.select())
	p += 1
	try:
		programa.select(p)
	except:
		programa.select(0)

def sel0(*args):
	programa.select(0)

def sel1(*args):
	programa.select(1)

def sel2(*args):
	programa.select(2)

def sel3(*args):
	programa.select(3)

def sel4(*args):
	programa.select(4)

def sel5(*args):
	programa.select(5)

def selectN(N):
	x = (N.char) #coretgeix variable introduida x teclat amb l'event
	N = int(x) # agafa el número net introduit x teclat
	N -= 1
	programa.select(N)


def principi(n):
	# demana ip i contrasenya a una finestra a part
	global i
	i = Tk()
	i.title("Servidor remot")
	#i.iconbitmap(f"@logo2.xbm")
	i.geometry("300x200")
	global txip, txc, tusr
	#programa = ""

	if n == 1:
		finestra.destroy() # truc x petar finestra i ke no peti res
	ip = Label(i, text="IP: ")
	txip = Entry(i)
	txip.insert(0, "10.33.160.85")
	usr = Label(i, text="Usuari: ")
	tusr = Entry(i)
	tusr.insert(0, "martivall")
	c = Label(i, text="Contrasenya: ")
	txc = Entry(i,show="*")
	txc.insert(0, "q1az/Q1AZ")
	ok = Button(i, text="Fet", command=aplicacio)


	ip.grid(column=0, row=0, sticky="nsew")
	txip.grid(column=1, row=0, sticky="nsew")
	usr.grid(column=0, row=1, sticky="nsew")
	tusr.grid(column=1, row=1, sticky="nsew")
	c.grid(column=0, row=2, sticky="nsew")
	txc.grid(column=1, row=2, sticky="nsew")
	ok.grid(column=0, row=3, sticky="nsew", columnspan=2)

	Grid.rowconfigure(i, 0, weight=1)
	Grid.rowconfigure(i, 1, weight=1)
	Grid.rowconfigure(i, 2, weight=1)
	Grid.rowconfigure(i, 3, weight=1)
	Grid.columnconfigure(i, 0, weight=1)
	Grid.columnconfigure(i, 1, weight=1)
	i.bind('<Escape>', tancar)# al premer esc tancar programa
	i.bind('<Return>', aplicacio)


	i.mainloop()





def aplicacio(*args):
	global IP
	global contra
	global usuari
	IP = txip.get()
	contra = txc.get()
	usuari = tusr.get()
	i.destroy()
	global finestra, programa,marc6

	finestra=Tk()#creem la finestra
	finestra.title(f"{usuari}-{IP}")
	#finestra.iconbitmap('@logo.xbm')


	# creem un widget que ens permetre fer pestanyes
	programa = ttk.Notebook(finestra)
	programa.grid(column=0, row=0, sticky="wens")


	menu = Menu(finestra)
	finestra.config(menu=menu,pady=5)

	menuAp = Menu(menu, tearoff=0)
	menuAp.add_command(label ="canviar servidor", command=lambda: principi(1))
	menuAp.add_command(label ="sortir", command=tancar)

	menuEd = Menu(menu, tearoff=0)
	menuEd.add_command(label="retalla", command=cut)
	menuEd.add_command(label="copia", command=copia)
	menuEd.add_command(label="enganxa", command=enganxa)

	menuAj = Menu(menu, tearoff=0)
	menuAj.add_command(label="informació", command=informacio)
	menuAj.add_command(label="ajuda", command=ajuda)
	menuAj.add_command(label="about us", command=about)


	menu.add_cascade(label="Aplicació", menu=menuAp)
	menu.add_cascade(label="Editar", menu=menuEd)
	menu.add_cascade(label="Ajuda", menu=menuAj)


	# creem la primera pestanya fent referencia el widget anterior

	marc0 = Frame(programa)
	marc0.grid(column=0, row=0, sticky="nesw")


	marc1=Frame(programa)#creem el marc que contindrà tots els widgets
	#definim la graella (grid) que ens permetrà posar els widgets en files i columnes
	marc1.grid(column=0, row=0, sticky="nesw")


	# creen la 3a pestanya que és on anirà aquest programa
	marc2 = Frame(programa)
	marc2.grid(column=0, row=0, sticky="nesw")


	marc3 = Frame(programa)
	marc3.grid(column=0, row=0, sticky="nesw")

	marc4 = Frame(programa)
	marc4.grid(column=0, row=0, sticky="nesw")

	marc5 = Frame(programa)
	marc5.grid(column=0, row=0, sticky="nesw")

	marc6 = Frame(programa)
	marc6.grid(column=0, row=0, sticky="nesw")
	# creem la pestanya que ens surtira a dalt com una pestanya
	# daquesta manera ja tenim el programa fet anteriorment d'intre una pestanya
	# i ja no molestara
	programa.add(marc0, text="Panell de serveis")
	programa.add(marc1, text="Descarregues")
	programa.add(marc2, text="Enviar configuració directament Apache")
	programa.add(marc3, text="Enviar configuració apache")
	programa.add(marc4, text="Editar arxiu Apache")
	programa.add(marc5, text="Terminal")
	programa.add(marc6, text="Informació")

	#Panell de serveis
	global logsText, apacheE, webminE,bindE,sshE,dhcpE,nfsE,ftpE

	titol = Label(marc0, text="Administrador de servidors\nControlador de serveis", font=24)
	titol.grid(column=0, row=0)

	serveis = LabelFrame(marc0, text="Serveis", font=24)
	serveis.grid(column=0, row=1, sticky='wens')


	serveisE = Label(serveis, text="Estat", font=20)
	serveisE.grid(column=0, row=0, sticky='wens')

	serveisS = Label(serveis, text="Servei", font=20)
	serveisS.grid(column=1, row=0, sticky='wens')

	serveisA = Label(serveis, text="Accions", font=20)
	serveisA.grid(column=2, row=0, columnspan=2, sticky='wens')

	refreshTot = Button(serveis, text="Refrescar tot", command=refreshAll)
	refreshTot.grid(column=3, row=0, columnspan=2)

	pu=ttk.Separator(serveis,orient='horizontal')
	pu.grid(column=0, row=1, sticky='ew', columnspan=6)

	#
	apacheE = Frame(serveis, width=20, height=20, background="gray")
	apacheE.grid(column=0, row=2)

	apacheS = Label(serveis, text="Apache")
	apacheS.grid(column=1, row=2)

	apacheA1 = Button(serveis, text="Start", command=lambda widget=apacheE,servei="apache2":start(widget,servei))
	apacheA1.grid(column=2, row=2)

	apacheA2 = Button(serveis, text="Stop", command=lambda widget=apacheE,servei="apache2":stop(widget,servei))
	apacheA2.grid(column=3, row=2)

	apacheA3 = Button(serveis, text="Restart", command=lambda widget=apacheE,servei="apache2":restart(widget,servei))
	apacheA3.grid(column=4, row=2)

	apacheA4 = Button(serveis, text="Refresh", command=lambda widget=apacheE,servei="apache2":refresh(widget,servei))
	apacheA4.grid(column=5, row=2)
	#
	webminE = Frame(serveis, width=20, height=20, background="gray")
	webminE.grid(column=0, row=3)

	webminS = Label(serveis, text="Webmin")
	webminS.grid(column=1, row=3)

	webminA1 = Button(serveis, text="Start", command=lambda widget=webminE,servei="webmin":start(widget,servei))
	webminA1.grid(column=2, row=3)

	webminA2 = Button(serveis, text="Stop", command=lambda widget=webminE,servei="webmin":stop(widget,servei))
	webminA2.grid(column=3, row=3)

	webminA3 = Button(serveis, text="Restart", command=lambda widget=webminE,servei="webmin":restart(widget,servei))
	webminA3.grid(column=4, row=3)

	webminA4 = Button(serveis, text="Refresh", command=lambda widget=webminE,servei="webmin":refresh(widget,servei))
	webminA4.grid(column=5, row=3)
	#
	bindE = Frame(serveis, width=20, height=20, background="gray")
	bindE.grid(column=0, row=4)

	bindS = Label(serveis, text="bind")
	bindS.grid(column=1, row=4)

	bindA1 = Button(serveis, text="Start", command=lambda widget=bindE,servei="bind9":start(widget,servei))
	bindA1.grid(column=2, row=4)

	bindA2 = Button(serveis, text="Stop", command=lambda widget=bindE,servei="bind9":stop(widget,servei))
	bindA2.grid(column=3, row=4)

	bindA3 = Button(serveis, text="Restart", command=lambda widget=bindE,servei="bind9":restart(widget,servei))
	bindA3.grid(column=4, row=4)

	bindA4 = Button(serveis, text="Refresh", command=lambda widget=bindE,servei="bind9":refresh(widget,servei))
	bindA4.grid(column=5, row=4)
	#
	sshE = Frame(serveis, width=20, height=20, background="gray")
	sshE.grid(column=0, row=5)

	sshS = Label(serveis, text="ssh")
	sshS.grid(column=1, row=5)

	ssh1 = Button(serveis, text="Start", command=lambda widget=sshE,servei="ssh":start(widget,servei))
	ssh1.grid(column=2, row=5)

	ssh2 = Button(serveis, text="Stop", command=lambda widget=sshE,servei="ssh":stop(widget,servei))
	ssh2.grid(column=3, row=5)

	sshA3 = Button(serveis, text="Restart", command=lambda widget=sshE,servei="ssh":restart(widget,servei))
	sshA3.grid(column=4, row=5)

	ssh4 = Button(serveis, text="Refresh", command=lambda widget=sshE,servei="ssh":refresh(widget,servei))
	ssh4.grid(column=5, row=5)
	#isc-dhcp-server
	dhcpE = Frame(serveis, width=20, height=20, background="gray")
	dhcpE.grid(column=0, row=6)

	dhcpS = Label(serveis, text="dhcp")
	dhcpS.grid(column=1, row=6)

	dhcp1 = Button(serveis, text="Start", command=lambda widget=dhcpE,servei="isc-dhcp-server":start(widget,servei))
	dhcp1.grid(column=2, row=6)

	dhcp2 = Button(serveis, text="Stop", command=lambda widget=dhcpE,servei="isc-dhcp-server":stop(widget,servei))
	dhcp2.grid(column=3, row=6)

	dhcpA3 = Button(serveis, text="Restart", command=lambda widget=dhcpE,servei="isc-dhcp-server":restart(widget,servei))
	dhcpA3.grid(column=4, row=6)

	dhcp4 = Button(serveis, text="Refresh", command=lambda widget=dhcpE,servei="isc-dhcp-server":refresh(widget,servei))
	dhcp4.grid(column=5, row=6)
	#nfs-kernel-server
	nfsE = Frame(serveis, width=20, height=20, background="gray")
	nfsE.grid(column=0, row=7)

	nfsS = Label(serveis, text="nfs")
	nfsS.grid(column=1, row=7)

	nfs1 = Button(serveis, text="Start", command=lambda widget=nfsE,servei="nfs-kernel-server":start(widget,servei))
	nfs1.grid(column=2, row=7)

	nfs2 = Button(serveis, text="Stop", command=lambda widget=nfsE,servei="nfs-kernel-server":stop(widget,servei))
	nfs2.grid(column=3, row=7)

	nfsA3 = Button(serveis, text="Restart", command=lambda widget=nfsE,servei="nfs-kernel-server":restart(widget,servei))
	nfsA3.grid(column=4, row=7)

	nfsp4 = Button(serveis, text="Refresh", command=lambda widget=nfsE,servei="nfs-kernel-server":refresh(widget,servei))
	nfsp4.grid(column=5, row=7)
	#vsftpd
	ftpE = Frame(serveis, width=20, height=20, background="gray")
	ftpE.grid(column=0, row=7)

	ftpS = Label(serveis, text="ftp")
	ftpS.grid(column=1, row=7)

	ftp1 = Button(serveis, text="Start", command=lambda widget=ftpE,servei="vsftpd":start(widget,servei))
	ftp1.grid(column=2, row=7)

	ftp2 = Button(serveis, text="Stop", command=lambda widget=ftpE,servei="vsftpd":stop(widget,servei))
	ftp2.grid(column=3, row=7)

	ftpA3 = Button(serveis, text="Restart", command=lambda widget=ftpE,servei="vsftpd":restart(widget,servei))
	ftpA3.grid(column=4, row=7)

	ftpp4 = Button(serveis, text="Refresh", command=lambda widget=ftpE,servei="vsftpd":refresh(widget,servei))
	ftpp4.grid(column=5, row=7)

	logsText = Text(marc0, selectbackground="green", selectforegroun="white", background="black", foreground="white", insertbackground='white')
	logsText.grid(row=2, column=0, sticky="nsew", padx=20)

	logsS=Scrollbar(marc0, orient="vertical", command=logsText.yview) #Barra de desplaçament
	logsSH=Scrollbar(marc0, orient="horizontal", command=logsText.yview) #Barra de desplaçament
	

	logsS.grid(column=1, row=2, sticky='ns', padx=5, pady=5)
	logsSH.grid(column=0, row=3, sticky='we', padx=5, pady=5)

	logsText.config(yscrollcommand=logsS.set)#assignem l'scrollbar al widget Text
	logsText.config(xscrollcommand=logsSH.set)#assignem l'scrollbar al widget Text

	
	refreshAll()


	Grid.rowconfigure(marc0, 3, weight=1)
	Grid.rowconfigure(marc0, 2, weight=1)
	Grid.rowconfigure(marc0, 1, weight=1)
	Grid.rowconfigure(marc0, 0, weight=0)
	Grid.columnconfigure(marc0, 0, weight=1)
	Grid.columnconfigure(marc0, 1, weight=0)

	Grid.rowconfigure(serveis, 6, weight=1)
	Grid.rowconfigure(serveis, 4, weight=1)
	Grid.rowconfigure(serveis, 4, weight=1)
	Grid.rowconfigure(serveis, 3, weight=1)
	Grid.rowconfigure(serveis, 2, weight=1)
	Grid.rowconfigure(serveis, 1, weight=1)
	Grid.rowconfigure(serveis, 0, weight=1)
	Grid.columnconfigure(serveis, 0, weight=1)
	Grid.columnconfigure(serveis, 1, weight=1)
	Grid.columnconfigure(serveis, 2, weight=1)
	Grid.columnconfigure(serveis, 3, weight=1)
	Grid.columnconfigure(serveis, 4, weight=1)
	Grid.columnconfigure(serveis, 5, weight=1)

	#pestanya 0	

	global T
	global T2
	global ruta1,ruta2

	L1 = Label(marc1, text="Introduïu Fitxer per escarregar", pady=30)
	L1.grid(column=0,row=0)
	L2 = Label(marc1, text="Introduïu Carpeta per escarregar", pady=30)
	L2.grid(column=2,row=0)

	ruta1 = Entry(marc1)
	ruta1.grid(column=0,row=1)

	ruta2 = Entry(marc1)
	ruta2.grid(column=2,row=1)

	T=Text(marc1,height=25,width=100) #Creem el widget tipus Text
	T2 = Text(marc1,height=25,width=100)
	S=Scrollbar(marc1, orient="vertical", command=T.yview) #Barra de desplaçament
	SH=Scrollbar(marc1, orient="horizontal", command=T.yview) #Barra de desplaçament
	S2=Scrollbar(marc1, orient="vertical", command=T2.yview) #Barra de desplaçament
	SH2=Scrollbar(marc1, orient="horizontal", command=T2.yview) #Barra de desplaçament
	T.grid(column=0, row=3, sticky='wens', padx=5, pady=5)
	T2.grid(column=2, row=3, sticky='wens', padx=5, pady=5)
	S.grid(column=1, row=3, sticky='ns', padx=5, pady=5)
	SH.grid(column=0, row=4, sticky='we', padx=5, pady=5)
	S2.grid(column=3, row=3, sticky='ns', padx=5, pady=5)
	SH2.grid(column=2, row=4, sticky='we', padx=5, pady=5)
	T.config(yscrollcommand=S.set)#assignem l'scrollbar al widget Text
	T.config(xscrollcommand=SH.set)#assignem l'scrollbar al widget Text
	T2.config(yscrollcommand=S2.set)#assignem l'scrollbar al widget Text
	T2.config(xscrollcommand=SH2.set)#assignem l'scrollbar al widget Text
	#creem i col·loquem els botons de sortir i llistar directori
	botoDescarregaFitxer=ttk.Button(marc1,text="Descarrega Fitxer",command=descarregaFitxer)
	botoDescarregaCarpeta=ttk.Button(marc1,text="Descarrega Interfaces",command=descarregaCarpeta)
	botoDescarregaFitxer.grid(column=0, row=2, padx=5, pady=5)
	botoDescarregaCarpeta.grid(column=2, row=2, padx=5, pady=5)


	boto=ttk.Button(marc1,text="SORTIR",command=quit)
	boto.grid(column=2, row=5, padx=5, pady=5, columnspan=3)


	canviar=ttk.Button(marc1,text="Canviar servidor",command=lambda: principi(1))
	canviar.grid(column=0, row=5, padx=5, pady=5, columnspan=2)



	# Pestanya 1

	global ex1Text, ex1Entry

	ex1 = Label(marc2, text="Afegeix el contingut de una Entry en el fitxer de configuració d'un servidor i reinicia el servei en la màquina remota")
	ex1.grid(row=0, column=0, sticky="w", padx=20, pady=20)

	ex1Entry = Entry(marc2)
	ex1Entry.grid(row=1, column=0, sticky="nsew")

	ex1Buto = Button(marc2, text="enviar el text a la configuració del apache", command=pasarConfApache)
	ex1Buto.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)

	ex1Label2 = Label(marc2, text="Terminal")
	ex1Label2.grid(row=0, column=1, sticky="w", padx=20, pady=20)

	ex1Text = Text(marc2)
	ex1Text.grid(row=1, column=1, sticky="nsew", padx=20)

	ex1S=Scrollbar(marc2, orient="vertical", command=ex1Text.yview) #Barra de desplaçament
	ex1SH=Scrollbar(marc2, orient="horizontal", command=ex1Text.yview) #Barra de desplaçament
	

	ex1S.grid(column=2, row=1, sticky='ns', padx=5, pady=5)
	ex1SH.grid(column=1, row=2, sticky='we', padx=5, pady=5)

	ex1Text.config(yscrollcommand=ex1S.set)#assignem l'scrollbar al widget Text
	ex1Text.config(xscrollcommand=ex1SH.set)#assignem l'scrollbar al widget Text



	# Pestanya 2

	global ex2Text, ex2Entry

	ex2 = Label(marc3, text="Envia tot un fitxer de configuració nou al servidor remot i en reinicia el servei.")
	ex2.grid(row=0, column=0, sticky="w", padx=50, pady=20)

	ex2Entry = Entry(marc3)
	ex2Entry.grid(row=1, column=0, sticky="ew", padx=100)

	ex2Entry.insert(0, "apache2.conf")

	ex2Buto = Button(marc3, text="enviar el text a la configuració del apache", command=pasarArxApache)
	ex2Buto.grid(row=2, column=0, sticky="nsew")



	ex2Label2 = Label(marc3, text="Terminal")
	ex2Label2.grid(row=0, column=1, sticky="w", padx=20, pady=20)

	ex2Text = Text(marc3)
	ex2Text.grid(row=1, column=1, sticky="nsew", padx=20)

	ex2S=Scrollbar(marc3, orient="vertical", command=ex2Text.yview) #Barra de desplaçament
	ex2SH=Scrollbar(marc3, orient="horizontal", command=ex2Text.yview) #Barra de desplaçament
	

	ex2S.grid(column=2, row=1, sticky='ns', padx=5, pady=5)
	ex2SH.grid(column=1, row=2, sticky='we', padx=5, pady=5)

	ex2Text.config(yscrollcommand=ex2S.set)#assignem l'scrollbar al widget Text
	ex2Text.config(xscrollcommand=ex2SH.set)#assignem l'scrollbar al widget Text



	# Pestanya 3
	global ex3Text1, ex3Text2
	ex3 = Label(marc4, text="Descarrega un fitxer de configuració del servidor, \nte'l mostra en una Entry i quan l'has modificat el torna a enviar al servidor reiniciant després el servei.")
	ex3.grid(row=0, column=0, sticky="w", padx=50, pady=20)

	ex3Buto1 = Button(marc4, text="Agafar l'arxiu de configuració", command=agafarArx)
	ex3Buto1.grid(row=1, column=0, sticky="nsew")

	ex3_2 = Label(marc4, text="Arxiu de configuració")
	ex3_2.grid(row=2, column=0, sticky="w", padx=50, pady=20)

	ex3Text1 = Text(marc4)
	ex3Text1.grid(row=3, column=0, sticky="nsew", padx=20)

	ex3S1=Scrollbar(marc4, orient="vertical", command=ex3Text1.yview) #Barra de desplaçament
	ex3SH1=Scrollbar(marc4, orient="horizontal", command=ex3Text1.yview) #Barra de desplaçament
	

	ex3S1.grid(column=1, row=3, sticky='ns', padx=5, pady=5)
	ex3SH1.grid(column=0, row=4, sticky='we', padx=5, pady=5)

	ex3Text1.config(yscrollcommand=ex3S1.set)#assignem l'scrollbar al widget Text
	ex3Text1.config(xscrollcommand=ex3SH1.set)#assignem l'scrollbar al widget Text

	ex3Buto2 = Button(marc4, text="Enviar l'arxiu de configuració", command=enviarArx )
	ex3Buto2.grid(row=5, column=0, sticky="nsew")

	ex3Label3 = Label(marc4, text="Terminal")
	ex3Label3.grid(row=2, column=2, sticky="w", padx=20, pady=20)

	ex3Text2 = Text(marc4)
	ex3Text2.grid(row=3, column=2, sticky="nsew", padx=20)

	ex3S2=Scrollbar(marc4, orient="vertical", command=ex3Text2.yview) #Barra de desplaçament
	ex3SH2=Scrollbar(marc4, orient="horizontal", command=ex3Text2.yview) #Barra de desplaçament
	
	ex3S2.grid(column=3, row=3, sticky='ns', padx=5, pady=5)
	ex3SH2.grid(column=2, row=4, sticky='we', padx=5, pady=5)

	ex3Text2.config(yscrollcommand=ex3S2.set)#assignem l'scrollbar al widget Text
	ex3Text2.config(xscrollcommand=ex3SH2.set)#assignem l'scrollbar al widget Text



	# terminal
	global terminalText1, terminalText2, textpwd

	textpwd = ['.']

	terminalLabel1 = Label(marc5, text="Introduïu comades")
	terminalLabel1.grid(row=0, column=0, sticky="w", padx=20, pady=20)

	terminalText1 = Text(marc5, selectbackground="green", selectforegroun="white", background="black", foreground="white", insertbackground='white')
	terminalText1.grid(row=1, column=0, sticky="nsew", padx=20)

	terminalS1=Scrollbar(marc5, orient="vertical", command=terminalText1.yview) #Barra de desplaçament
	terminalSH1=Scrollbar(marc5, orient="horizontal", command=terminalText1.yview) #Barra de desplaçament
	

	terminalS1.grid(column=1, row=1, sticky='ns', padx=5, pady=5)
	terminalSH1.grid(column=0, row=2, sticky='we', padx=5, pady=5)

	terminalText1.config(yscrollcommand=terminalS1.set)#assignem l'scrollbar al widget Text
	terminalText1.config(xscrollcommand=terminalSH1.set)#assignem l'scrollbar al widget Text

	terminalButo1 = Button(marc5, text="enviar", command=terminal)
	terminalButo1.grid(row=3, column=0)


	terminalLabel2 = Label(marc5, text="Terminal remota")
	terminalLabel2.grid(row=0, column=2, sticky="w", padx=20, pady=20)

	terminalText2 = Text(marc5, background="black")
	terminalText2.grid(row=1, column=2, sticky="nsew", padx=20)

	terminalS2=Scrollbar(marc5, orient="vertical", command=terminalText2.yview) #Barra de desplaçament
	terminalSH2=Scrollbar(marc5, orient="horizontal", command=terminalText2.yview) #Barra de desplaçament
	

	terminalS2.grid(column=3, row=1, sticky='ns', padx=5, pady=5)
	terminalSH2.grid(column=2, row=2, sticky='we', padx=5, pady=5)

	terminalText2.config(yscrollcommand=terminalS2.set)#assignem l'scrollbar al widget Text
	terminalText2.config(xscrollcommand=terminalSH2.set)#assignem l'scrollbar al widget Text

	# Informacio
	global x,y,resize_image,im,img,logo,xA

	infoText1 = Label(marc6, text="Aplicació gestors de servidors\nInformació:", font=24)
	infoText1.grid(column=0, row=0)
	
	infoText2 = Label(marc6, text="Panell de Serveis:\ncontrolar serveis", font=24)
	infoText2.grid(column=0, row=1)

	infoText3 = Label(marc6, text="Descarregues:\ndescarregar fitxers o carpetes", font=24)
	infoText3.grid(column=0, row=2)
	
	infoText4 = Label(marc6, text="Enviar configuracó directament apache", font=24)
	infoText4.grid(column=0, row=3)

	infoText5 = Label(marc6, text="Envia arxiu apache2.conf", font=24)
	infoText5.grid(column=0, row=4)

	infoText6 = Label(marc6, text="Editar arxiu apache2.conf", font=24)
	infoText6.grid(column=0, row=5)

	infoText7 = Label(marc6, text="Terminal per fer comandes lliurament", font=24)
	infoText7.grid(column=0, row=6)

	im = Image.open("logo.png")
	resize_image = im.resize((600, 600))
	img = ImageTk.PhotoImage(resize_image)
	logo = Label(marc6, image=img)
	logo.grid(column=1, row=0, sticky='nsew', rowspan=6)


	#responsivejem tots els components creats anteriorment

	Grid.columnconfigure(finestra, 0, weight=1)
	Grid.rowconfigure(finestra, 0, weight=1)

	Grid.columnconfigure(programa, 0, weight=1)
	Grid.rowconfigure(programa, 0, weight=1)


	Grid.rowconfigure(marc1, 2, weight=1)
	Grid.rowconfigure(marc1, 3, weight=1)
	Grid.rowconfigure(marc1, 1, weight=1)

	Grid.columnconfigure(marc1, 1, weight=1)
	Grid.columnconfigure(marc1, 0, weight=1)
	Grid.columnconfigure(marc1, 2, weight=1)
	Grid.columnconfigure(marc1, 3, weight=1)

	Grid.rowconfigure(marc2, 0, weight=0) # fent proves pk la pestanya 2 quedi millor
	Grid.rowconfigure(marc2, 1, weight=4)
	Grid.rowconfigure(marc2, 2, weight=1)
	Grid.columnconfigure(marc2, 0, weight=1)
	Grid.columnconfigure(marc2, 1, weight=1)
	Grid.columnconfigure(marc2, 2, weight=1)


	Grid.rowconfigure(marc3, 0, weight=0)
	Grid.rowconfigure(marc3, 1, weight=1)
	Grid.rowconfigure(marc3, 2, weight=1)
	Grid.columnconfigure(marc3, 0, weight=1)
	Grid.columnconfigure(marc3, 1, weight=1)
	Grid.columnconfigure(marc3, 2, weight=1)

	Grid.rowconfigure(marc4, 0, weight=0)
	Grid.rowconfigure(marc4, 1, weight=1)
	Grid.rowconfigure(marc4, 2, weight=1)
	Grid.rowconfigure(marc4, 3, weight=1)
	Grid.rowconfigure(marc4, 4, weight=1)
	Grid.rowconfigure(marc4, 5, weight=1)
	Grid.columnconfigure(marc4, 0, weight=1)
	Grid.columnconfigure(marc4, 1, weight=1)
	Grid.columnconfigure(marc4, 2, weight=1)
	Grid.columnconfigure(marc4, 3, weight=1)

	Grid.rowconfigure(marc5, 0, weight=0)
	Grid.rowconfigure(marc5, 1, weight=1)
	Grid.rowconfigure(marc5, 2, weight=1)
	Grid.rowconfigure(marc5, 3, weight=1)
	Grid.columnconfigure(marc5, 0, weight=1)
	Grid.columnconfigure(marc5, 1, weight=1)
	Grid.columnconfigure(marc5, 2, weight=1)
	Grid.columnconfigure(marc5, 3, weight=1)


	Grid.rowconfigure(marc6, 0, weight=1)
	Grid.rowconfigure(marc6, 1, weight=1)
	Grid.rowconfigure(marc6, 2, weight=1)
	Grid.rowconfigure(marc6, 3, weight=1)
	Grid.rowconfigure(marc6, 4, weight=1)
	Grid.rowconfigure(marc6, 5, weight=1)
	Grid.rowconfigure(marc6, 6, weight=1)
	Grid.columnconfigure(marc6, 0, weight=1)
	Grid.columnconfigure(marc6, 1, weight=1)


	finestra.bind('<Escape>', tancar)# al premer esc tancar programa

	terminalText1.bind('<Return>', terminal)
	finestra.bind('<Tab>', select) # controls de pestanyes
	finestra.bind('<Alt_L>1', selectN) # lambda N=1: selectN(N)
	finestra.bind('<Alt_L>2', selectN)
	finestra.bind('<Alt_L>3', selectN)
	finestra.bind('<Alt_L>4', selectN)
	finestra.bind('<Alt_L>5', selectN)
	finestra.bind('<Alt_L>6', selectN)
	finestra.bind('<Alt_L>7', selectN)


	infoText2.bind("<Button-1>", sel0)
	infoText3.bind("<Button-1>", sel1)
	infoText4.bind("<Button-1>", sel2)
	infoText5.bind("<Button-1>", sel3)
	infoText6.bind("<Button-1>", sel4)
	infoText7.bind("<Button-1>", sel5)
	
	#finestra.bind(f"{w}", lambda w=w: num(w))


	finestra.bind("<Button-3>", popup)
	finestra.bind("<Button-1>", popup_destroy)


	#logo.bind('<Configure>', resizer)


	finestra.mainloop()




#Codi principal
principi(0)
