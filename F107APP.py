import tkinter
import tkinter.filedialog as filedialog
import tkinter.messagebox as message
import F107

def but():
    dirpath = filedialog.askdirectory()
    S = F107.MyTest(dirpath)
    message.showinfo('当天的F107指数', S)
root=tkinter.Tk()
root.title('Calculate F107')#标题
root.geometry('300x100')#窗体大小
root.resizable(False, False)#固定窗体
tkinter.Button(root, text='选择文件夹，计算当天的F107指数',command=but).pack()
root.mainloop()