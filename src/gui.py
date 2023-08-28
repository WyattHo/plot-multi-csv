import csv
import kernel
import tkinter as tk
from tkinter import filedialog
from tkinter import font
from tkinter import ttk


def openDir():
    dirName = filedialog.askopenfilename(title='Choose the directory')
    dirVariable.set(dirName)


def readCsv():
    # Clear items first
    for item in treeviewRead.get_children():
        treeviewRead.delete(item)

    # Read csv
    tgtFileName = dirVariable.get()
    with open(tgtFileName, 'r') as f:
        csvData = csv.DictReader(f)
        fieldNames = csvData.fieldnames
        treeviewRead['columns'] = fieldNames

        # Analyze best-fit width for each field
        for fieldName in fieldNames:
            maxWidths[fieldName] = len(fieldName)

        for rowIdx, rowData in enumerate(csvData):
            for fieldName in fieldNames:
                dataWidth = len(rowData[fieldName])

                if dataWidth > maxWidths[fieldName]:
                    maxWidths[fieldName] = dataWidth

        # Set fields
        for fieldName in fieldNames:
            treeviewRead.column(fieldName, anchor=tk.W, width=10*maxWidths[fieldName], stretch=0)
            treeviewRead.heading(fieldName, text=fieldName, anchor=tk.W)

        # Reset scrollbars
        scrollBarVerL.config(command=treeviewRead.yview)
        scrollBarHorL.config(command=treeviewRead.xview)
        
        # The entire file has been iterated at the first time,
        # so it is needed to seek to the beginning.
        f.seek(0)
        next(csvData)

        # Insert values
        for rowIdx, rowData in enumerate(csvData):
            values = [rowData[fieldName] for fieldName in fieldNames]
            treeviewRead.insert(parent='', index=rowIdx, values=values, tags=str(rowIdx))


def Draw():
    totalNum = len(treeviewRead.get_children())

    try:
        kernel.Draw(totalNum=totalNum, usedIdxList=usedIdxList)
    except Exception as e:
        tk.messagebox.showerror("Error", e.args[0])
        insertValues = False
    else:
        luckyGuy = usedIdxList[-1]
        insertValues = True

    # Set fields for treeviewDraw
    if treeviewDraw['columns'] != treeviewRead['columns']:
        treeviewDraw['columns'] = treeviewRead['columns']
    
        for fieldName in treeviewRead['columns']:
            treeviewDraw.column(fieldName, anchor=tk.W, width=10*maxWidths[fieldName], stretch=0)
            treeviewDraw.heading(fieldName, text=fieldName, anchor=tk.W)

        # Reset scrollbars
        scrollBarVerR.config(command=treeviewDraw.yview)
        scrollBarHorR.config(command=treeviewDraw.xview)

    # Insert values
    if insertValues:
        for idx, item in enumerate(treeviewRead.get_children()):
            if idx == luckyGuy:
                values = treeviewRead.item(item, 'values')
                treeviewDraw.insert(parent='', index=0, values=values, tags=str(idx))


def Clear():
    usedIdxList.clear()
    for item in treeviewDraw.get_children():
        treeviewDraw.delete(item)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('LuckyGuy')
    root.resizable(width=0, height=0)
    root.configure()

    labelFont = font.Font(family='Helvetica', size=10)
    btnFont = font.Font(family='Helvetica', size=10)
    
    # frame up
    frameUp = tk.LabelFrame(root, text='Choose a csv source')
    frameUp.grid(row=0, column=0, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W)
    frameUp['font'] = labelFont
    
    frameUpUp = tk.Frame(frameUp)
    frameUpUp.grid(row=0, column=0)

    frameUpRight = tk.Frame(frameUp)
    frameUpRight.grid(row=0, column=1, rowspan=2)

    dirVariable = tk.StringVar()
    tgtDirStrEntry = tk.Entry(frameUpUp, width=50, textvariable=dirVariable)
    tgtDirStrEntry.grid(row=0, column=0, padx=5, pady=5)

    chooseBtn = tk.Button(frameUpRight, text='Choose', command=openDir, width=6)
    chooseBtn.grid(row=0, column=0, padx=5, pady=5, ipadx=1, ipady=1)
    chooseBtn['font'] = btnFont


    # frame down
    frameDw = tk.LabelFrame(root, text='Working area')
    frameDw.grid(row=1, column=0, padx=5, pady=5)
    frameDw.propagate(0)
    frameDw['font'] = labelFont
    
    ## frame down left 1
    frameDwLeft1 = tk.Frame(frameDw, width=250, height=300)
    frameDwLeft1.grid(row=0, column=0, padx=5, pady=5)
    frameDwLeft1.propagate(0)

    scrollBarVerL = tk.Scrollbar(frameDwLeft1)
    scrollBarVerL.pack(side=tk.RIGHT, fill=tk.Y)

    scrollBarHorL = tk.Scrollbar(frameDwLeft1, orient='horizontal')
    scrollBarHorL.pack(side=tk.BOTTOM, fill=tk.X)

    treeviewRead = ttk.Treeview(frameDwLeft1, 
                               yscrollcommand=scrollBarVerL.set, 
                               xscrollcommand=scrollBarHorL.set,
                               height=15)
    
    treeviewRead.pack(fill='both')
    treeviewRead.propagate(0)

    scrollBarVerL.config(command=treeviewRead.yview)
    scrollBarHorL.config(command=treeviewRead.xview)
    treeviewRead['columns'] = ('1', )
    treeviewRead['show'] = 'headings'

    treeviewRead.column('1')
    treeviewRead.heading('1', text='')
    
    ## frame down left 2
    frameDwLeft2 = tk.Frame(frameDw)
    frameDwLeft2.grid(row=1, column=0)
    frameDwLeft2.propagate(0)

    maxWidths = {}
    readBtn = tk.Button(frameDwLeft2, text='Read', command=readCsv, width=6)
    readBtn.grid(row=0, column=0, padx=5, pady=5, ipadx=1, ipady=1)
    readBtn['font'] = btnFont

    ## frame down right 1
    frameDwRight1 = tk.Frame(frameDw, width=250, height=300)
    frameDwRight1.grid(row=0, column=1, padx=5, pady=5)
    frameDwRight1.propagate(0)

    scrollBarVerR = tk.Scrollbar(frameDwRight1)
    scrollBarVerR.pack(side=tk.RIGHT, fill=tk.Y)

    scrollBarHorR = tk.Scrollbar(frameDwRight1, orient='horizontal')
    scrollBarHorR.pack(side=tk.BOTTOM, fill=tk.X)

    treeviewDraw = ttk.Treeview(frameDwRight1, 
                               yscrollcommand=scrollBarVerR.set, 
                               xscrollcommand=scrollBarHorR.set,
                               height=15)

    treeviewDraw.pack(fill='both')
    treeviewDraw.propagate(0)

    scrollBarVerR.config(command=treeviewDraw.yview)
    scrollBarHorR.config(command=treeviewDraw.xview)
    treeviewDraw['columns'] = ('1', )
    treeviewDraw['show'] = 'headings'

    treeviewDraw.column('1')
    treeviewDraw.heading('1', text='')

    ## frame down right 2
    frameDwRight2 = tk.Frame(frameDw)
    frameDwRight2.grid(row=1, column=1)

    usedIdxList = []
    clearState = False
    drawBtn = tk.Button(frameDwRight2, text='Draw', command=Draw, width=6)
    drawBtn.grid(row=0, column=0, padx=5, pady=5, ipadx=1, ipady=1)
    drawBtn['font'] = btnFont
    
    clearBtn = tk.Button(frameDwRight2, text='Clear', command=Clear, width=6)
    clearBtn.grid(row=0, column=1, padx=5, pady=5, ipadx=1, ipady=1)
    clearBtn['font'] = btnFont
    
    root.mainloop()
    