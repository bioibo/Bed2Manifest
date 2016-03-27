#!/usr/bin/python3
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import re



def openfile():
	global bedfile
	bedfile = filedialog.askopenfilename(parent=root,defaultextension=".bed",filetypes=[("Bed Files","*.bed"),("All Files","*.*")])
	
	if bedfile == "":
		bedfile = None
	else:
		root.title(os.path.basename(bedfile)+ " - Bed2Manifest")
		bedPad.delete(1.0,END)
		fh=open(bedfile,"r")
		bedPad.insert(1.0,fh.read())
		fh.close()

def createmanifest():	

	if 'bedfile' in globals():
		global manifestfile
		global manifestfile2
		global manifestTitle
		global manifestHeader
		global includeheader
		manifestfile=bedPad.get(0.0,END)
		manifestfile=manifestfile.split("\n")
		manifestfile2=[]
		manifestHeader=[]
		
		for x in range(0,len(manifestfile)):
			if manifestfile[x].startswith("chr"):
				manifestfile2.append(manifestfile[x])
			else :
				manifestHeader.append(manifestfile[x])

		manifestfile=[]
		
		for x in range(0,len(manifestfile2)):
			manifestfile2[x]='\t'.join(manifestfile2[x].split('\t')[0:3])
			manifestfile.append(re.sub('\t','_',manifestfile2[x]))
			manifestfile[x]=manifestfile[x]+'\t'+ manifestfile2[x]+"\t"+upl.get()+"\t"+dpl.get()


		manifestfile='\n'.join(manifestfile)
		manifestHeader='\n'.join(manifestHeader)
		manifestHeader="[Header]\n"+manifestHeader
		
		if includeheader.get() == 0 :
			manifestHeader=""
		manifestTitle="[Regions]\nName	Chromosome	Amplicon Start	Amplicon End	Upstream Probe Length	Downstream Probe Length\n"
		manifestfile=manifestHeader+manifestTitle+manifestfile
		manifestPad.delete(1.0,END)
		manifestPad.insert(1.0,manifestfile)

	else:		
		messagebox.showinfo("No","Import a bed file first")

def savemanifest():
	manifest=filedialog.asksaveasfile(mode="w",defaultextension='.txt')
	textoutput=manifestPad.get(0.0,END)
	manifest.write(textoutput)
	manifest.close()

		
def about():
	messagebox.showinfo("Bed2Manifest","Bed2Manifest\n\nversion 1.6\n\ninfo: ibrahim.kisakesen@sem.com.tr")
root = Tk()
root.title("Bed2Manifest")

#menubar
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Import Bed",accelerator='Ctrl+O', command=openfile)
filemenu.add_separator()
filemenu.add_command(label="Save Manifest", command=savemanifest)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

toolmenu=Menu(menubar,tearoff=0)
toolmenu.add_command(label="Create Manifest", command=openfile)
toolmenu.add_separator()
toolmenu.add_command(label="About",command=about)
menubar.add_cascade(label="Tools",menu=toolmenu)




topframe=Frame(root,height=25,pady=5,padx=5)
topframe.pack(expand=NO,fill=X)
introtext=Label(topframe, text="Welcome to bed file to manifest file converter.",pady=5)
introtext.pack()

upstreamtext=Label(topframe,text="Upstream probe length:")
upstreamtext.pack(side=LEFT)

upl=Entry(topframe)
upl.pack(side=LEFT)
upl.insert(0,"0")

dpl=Entry(topframe)
dpl.pack(side=RIGHT)
dpl.insert(0,"0")

downstreamtext=Label(topframe,text="Downstream probe length:")
downstreamtext.pack(side=RIGHT)




middleframe=Frame(root,pady=5,padx=5)
middleframe.pack(expand=YES, fill=BOTH)

bedPad=Text(middleframe)
bedPad.pack(side=LEFT, expand=YES,fill=BOTH)
scroll=Scrollbar(bedPad)
bedPad.configure(yscrollcommand=scroll.set)
bedPad.configure(wrap=NONE)
scroll.config(command=bedPad.yview)
scroll.pack(side=RIGHT,fill=BOTH)

includeheader=IntVar()
incheader=Checkbutton(middleframe,text="Include Header Section",variable=includeheader)
incheader.pack(side=TOP)
incheader.var = includeheader
convertbutton=Button(middleframe,text="Create \n Manifest", command=createmanifest)
convertbutton.pack(side=LEFT)

manifestPad=Text(middleframe)
manifestPad.pack(side=LEFT, expand=YES,fill=BOTH)
scroll=Scrollbar(manifestPad)
manifestPad.configure(yscrollcommand=scroll.set)
manifestPad.configure(wrap=NONE)
scroll.config(command=manifestPad.yview)
scroll.pack(side=RIGHT,fill=BOTH)

root.config(menu=menubar)
root.mainloop()
