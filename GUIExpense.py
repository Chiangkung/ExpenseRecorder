# GUIBasic2-Expense.py
from tkinter import *
from tkinter import ttk, messagebox
# ttk is theme of Tk
import csv
from datetime import datetime

GUI = Tk()
GUI.title('โปรแกรมบัยทึกค่าใช้จ่าย V.1.0 by Chiang') # Title of program
#GUI.geometry('720x650+50+0') # (+50+0) insert to specify fixed position on X-axis and Y-axis 

w = 720
h = 650
ws = GUI.winfo_screenwidth() #screen width
hs = GUI.winfo_screenheight() #screen hieght

x = (ws/2) - (w/2)
y = (hs/2) - (h/2)-100

GUI.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}') #:.0f คือไม่มีจุดทศนิยม

#B1 = Button(GUI,text='Hello')
#B1.pack(ipadx=50,ipady=10) # .pack() เป็นการติดปุ่มเข้ากับ GUI หลัก / ipadx คือการเพิ่มขนาดปุ่ม

#################MANU################
menubar = Menu(GUI)
GUI.config(menu=menubar) # GUI.config คือทำให้ file menu ไปแปะบน GUI หลัก

# File Menu
filemenu = Menu(menubar,tearoff=0) #tearoff ทำให้ไม่มีแถบ --- (ใช้เพื่อดึงเมนูแยกออกมาได้) ในเมนูย่อย
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export to Googlesheet')

# Help Menu
def About():
    print('About Manu')
    messagebox.showinfo('About','สวัสดีครับ โปรแกรมนี้คือโปรแกรมบันทึกข้อมูล\nสนใจบริจาคเราไหม?')

helpmenu = Menu(menubar)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)
# Donate Menu
donatemenu = Menu(menubar)
menubar.add_cascade(label='Donate',menu=donatemenu)

#####################################


Tab = ttk.Notebook(GUI)

T1 = Frame(Tab) #แท็บที่ 1 สามารถใส่ ',width=400,height=400' เพิ่มเข้าไปเพื่อกำหนดขนาด tab ได้
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1) #ใน() ใสเพื่อขยายขนาดของ tab ให้เต็ม

expenseicon = PhotoImage(file='expense.png') #.subsample(2) ใส่ต่อท้ายได้เพื่อย่อขนาดรูป

listicon = PhotoImage(file='list.png')

Tab.add(T1,text=f'{"Add Expense": ^{50}}', image=expenseicon,compound='top')
Tab.add(T2,text=f'{"Expense List": ^{50}}', image=listicon,compound='top')

F1 = Frame(T1) #ttk.LabelFrame
F1.place(x=200,y=50) # .place() ติดปุ่มโดยระบุตำแหน่ง .pack() for place in the middle

days = {'Mon':'จันทร์',
        'Tue':'อังคาร',
        'Wed':'พุธ',
        'Thu':'พฤหัสบดี',
        'Fri':'ศุกร์',
        'Sat':'เสาร์',
        'Sun':'อาทิตย์'}

def Save(event=None):
    expense = v_expense.get() # .get() คือดึงค่ามาจาก v_expense = StringVer()
    price = v_price.get()
    quantity = v_quantity.get()

    if expense == '':
        print('No Data')
        messagebox.showwarning('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
        return #return คือให้จบและออกจาก function ไม่ต้อง run ต่อที่เหลือ
    elif price == '':
        messagebox.showwarning('Error','กรุณากรอกข้อมูลราคา')
        return
    elif quantity == '':
        quantity = 1

    try:
        total = int(price)*int(quantity)
        
        print('รายการ: {}, ราคา: {} บาท'.format(expense,price))
        print('จำนวน: {} หน่วย, ยอดรวม: {} บาท'.format(quantity,total))
        text = 'รายการ: {}, ราคา: {} บาท\n'.format(expense,price)
        text = text + 'จำนวน: {} หน่วย, ยอดรวม: {} บาท'.format(quantity,total)
        v_result.set(text)

        # clear ข้อมูลเก่า
        v_expense.set('')
        v_price.set('')
        v_quantity.set('')
        # .set('') คือ clear ข้อมูลเก่า

        # บันทึกข้อมูลลง csv อย่าลืม import csv ด้วย
        today = datetime.now().strftime('%a') # days['Mon'] = 'จันทร์'
        print(today)
        stamp = datetime.now()
        dt = stamp.strftime('%Y-%m-%d-%H:%M:%S')
        transactionid = stamp.strftime('%Y%m%d%H%M%f')
        dt = days[today] + '-' + dt
        with open('savedata.csv','a',encoding='utf-8',newline='') as f:
            # with คือสั่งเปิด file แล้วปิดอัตโนมัติ
            # หลังชื่อ file ต้องระบุว่าจะทำอะไรกับ file ex. 'a' = append คือให้เพิ่มข้อมูล (or 'w', 'r')
            # encoding='utf-8' ใส่เพื่อให้บันทึกภาษาไทยได้
            # newline='' ทำให้ข้ิอมูลไม่มีบรรทัดว่าง
            fw = csv.writer(f) #สร้าง function สำหรับเขียนข้อมูล
            data = [transactionid,dt,expense,price,quantity,total]
            fw.writerow(data)

        # ทำให้เคอเซอร์กลับไปตำแหน่งช่องกรอก E1
        E1.focus()
        update_table()
        #update_record()
    except:
        print('ERROR')
        #messagebox แสดงได้ 3 แบบ
        #messagebox.showerror('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
        messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
        #messagebox.showinfo('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
        v_expense.set('')
        v_price.set('')
        v_quantity.set('')

# ทำให้สามารถกด Enter ได้
GUI.bind('<Return>',Save) # ต้องเพิ่มใน def Save(event=None) ด้วย
#GUI.bind เป็นการ check ว่ามีการกดปุ่มอะไรบ้าง ซึ่งปุ่ม <Return> = ปุ่ม Enter

FONT1 = (None,20) # None เปลี่ยนเป็น 'Angsana New'

# ------------Image-----------
walletlogo = PhotoImage(file='wallet.png')
logo = ttk.Label(F1,image=walletlogo)
logo.pack()

#-------------text 1-----------------------------

L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1).pack()
v_expense = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()
#-------------------------------------------------

#-------------text 2-----------------------------

L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1).pack()
v_price = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()
#-------------------------------------------------

#-------------text 3-----------------------------

L = ttk.Label(F1,text='จำนวน (หน่วย)',font=FONT1).pack()
v_quantity = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT1)
E3.pack()
#-------------------------------------------------

#add picture for save icon
saveicon = PhotoImage(file='save.png')

B2 = ttk.Button(F1,text=f'{"Save": >{10}}',command=Save,image=saveicon,compound='left') # เอาปุ่ม B2 ซึ่งกำหนดขนาดได้ไปแปะบน F1 frame ซึ่งระบุตำแหน่งได้
B2.pack(ipadx=50,ipady=5,pady=20) 
'''
ipadx = expand button in x-axis
ipady = expand button in y-axis
pady = expand space of the button from the above item
'''

v_result = StringVar()
v_result.set('-------------ผลลัพธ์----------')
result = ttk.Label(F1, textvariable=v_result,font=FONT1,foreground='blue')
result.pack(pady=20)

#################TAB2###############
def read_csv():
    with open('savedata.csv',newline='',encoding='utf-8') as f:
        # use 'with' fn เพราะถ้าใช้แค่ 'open' จะต้อง 'close' ด้วย แต่ 'with' จะปิดให้อัตโนมัติ
        '''
        f = open('savedata.csv',newline='',encoding='utf-8')
        fr = csv.reader(f)
        f.close()
        '''
        fr = csv.reader(f)
        data = list(fr)
    return data
        # print(data)
        # print('--------------')
        # print(data[0][0])
        # for a,b,c,d,e in data:
        #     print(b)

'''
def update_record():
    getdata = read_csv()
    v_allrecord.set('')
    text = ''
    for d in getdata:
        txt = '{}---{}---{}---{}---{}\n'.format(d[0],d[1],d[2],d[3],d[4])
        text = text + txt 

    v_allrecord.set(text)

v_allrecord = StringVar()
v_allrecord.set('--------All Record----------')
Allrecord = ttk.Label(T2,textvariable=v_allrecord,font=(None,15),foreground='green')
Allrecord.pack(pady=20)
'''

# Table
L = ttk.Label(T2,text='ตารางแสดงผลลัพท์ทั้งหมด',font=FONT1).pack(pady=20)
header = ['รหัสรายการ','วัน-เวลา', 'รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resultable = ttk.Treeview(T2,columns=header,show='headings',height=20)
resultable.pack()

# for i in range(len(header)):
#     resultable.heading(header[i],text=header[i])

for h in header:
    resultable.heading(h,text=h)

headerwidth = [120,150,170,80,80,80]

for h,w in zip(header,headerwidth):
    resultable.column(h,width=w)

# resultable.insert('','end',value=['Mon','Water',30,5,150]) 
#'end' ใส่เพื่อให้ไปต่อท้ายตาราง

alltransaction = {}

def UpdateCSV():
    with open('savedata.csv','w',newline='',encoding='utf-8') as f:
        fw = csv.writer(f)
        # เตรียมข้อมูลจาก alltransaction ให้กลายเป็น list
        data = list(alltransaction.values())
        fw.writerows(data) # multiple line from nested list [[],[],[]]
        print('Table was updated')

def DeleteRecord(event=None):
    check = messagebox.askyesno('Confirm?','คุณต้องการลบข้อมูลใช่หรือไม่?')
    print('YES/NO:',check)

    if check == True:
        print('delete')
        select = resultable.selection()
        # print(select)
        data = resultable.item(select)
        data = data['values']
        transactionid = data[0]
        # print(transactionid)
        del alltransaction[str(transactionid)]
        # print(alltransaction)
        UpdateCSV()
        update_table()
    else:
        print('cancel')


BDelete = ttk.Button(T2,text='delete',command=DeleteRecord)
BDelete.place(x=50,y=520)

resultable.bind('<Delete>',DeleteRecord)

def update_table():
    resultable.delete(*resultable.get_children()) # ใส่ * แทน run for loop ได้
    # for c in resultable.get_children():
    #     resultable.delete(c)
    try:
        data = read_csv()
        for d in data:
            #create transaction data
            alltransaction[d[0]] = d # d[0] = transactionid
            resultable.insert('',0,value=d)
        print(alltransaction)
    except Exception as e:
        print('No File')
        print('ERROR:', e)

###########Right Click Manu###############
def EditRecord():
    POPUP = Toplevel() #คล้ายๆกับ TK()
    POPUP.title('Edit Record')
    #POPUP.geometry('500x400')
    w = 500
    h = 400
    ws = POPUP.winfo_screenwidth() #screen width
    hs = POPUP.winfo_screenheight() #screen hieght

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)-100

    POPUP.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}') #:.0f คือไม่มีจุดทศนิยม

    #-------------text 1-----------------------------
    L = ttk.Label(POPUP,text='รายการค่าใช้จ่าย',font=FONT1).pack()
    v_expense = StringVar()
    # StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
    E1 = ttk.Entry(POPUP,textvariable=v_expense,font=FONT1)
    E1.pack()
    #-------------------------------------------------

    #-------------text 2-----------------------------

    L = ttk.Label(POPUP,text='ราคา (บาท)',font=FONT1).pack()
    v_price = StringVar()
    # StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
    E2 = ttk.Entry(POPUP,textvariable=v_price,font=FONT1)
    E2.pack()
    #-------------------------------------------------

    #-------------text 3-----------------------------

    L = ttk.Label(POPUP,text='จำนวน (หน่วย)',font=FONT1).pack()
    v_quantity = StringVar()
    # StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
    E3 = ttk.Entry(POPUP,textvariable=v_quantity,font=FONT1)
    E3.pack()
    #-------------------------------------------------

    def Edit():
        # print(transactionid)
        # print(alltransaction)
        olddata = alltransaction[str(transactionid)]
        print('OLD:',olddata)
        v1 = v_expense.get()
        v2 = float(v_price.get())
        v3 = float(v_quantity.get())
        total = v2 * v3
        newdata = [olddata[0],olddata[1],v1,v2,v3,total]
        alltransaction[str(transactionid)] = newdata
        UpdateCSV()
        update_table()
        POPUP.destroy() # order to close POPUP



    #add picture for save icon
    saveicon = PhotoImage(file='save.png')

    B2 = ttk.Button(POPUP,text=f'{"Save": >{10}}',command=Edit,image=saveicon,compound='left') # เอาปุ่ม B2 ซึ่งกำหนดขนาดได้ไปแปะบน F1 frame ซึ่งระบุตำแหน่งได้
    B2.pack(ipadx=50,ipady=5,pady=20) 

    # get data in selected record
    select = resultable.selection()
    print(select)
    data = resultable.item(select)
    data = data['values']
    print(data)
    transactionid = data[0]
    # สั่งเซ็ตค่าเก่าไว้ตรงช่องกรอก
    v_expense.set(data[2])
    v_price.set(data[3])
    v_quantity.set(data[4])

    POPUP.mainloop()

rightclick = Menu(GUI,tearoff=0)
rightclick.add_command(label='Edit',command=EditRecord)
rightclick.add_command(label='Delete',command=DeleteRecord)

def menupopup(event):
    #print(event.x_root, event.y_root) #เป็นการระบุจุดที่ right click
    rightclick.post(event.x_root,event.y_root)

resultable.bind('<Button-3>', menupopup) #Buttn-3 คือ code of right click/bind คือมีผลเฉพาะตาราง




update_table()
print('GET CHILD:', resultable.get_children())
#GUI.bind('<Tab>',Lambda x: E2.focus())
GUI.mainloop() #เพื่อให้ program run loop ตลอดเวลา

