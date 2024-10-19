#Created by Michael Reju ALexander 19/10/2024

import flet as ft
from flet import View, Page, AppBar, ElevatedButton, Text, Container, Column
from flet import RouteChangeEvent, ViewPopEvent, CrossAxisAlignment, MainAxisAlignment
import csv
import mysql.connector as mc
import os
import ctypes
from ctypes import wintypes, windll

CSIDL_DESKTOP= 0

_SHGetFolderPath = windll.shell32.SHGetFolderPathW
_SHGetFolderPath.argtypes = [wintypes.HWND,
                            ctypes.c_int,
                            wintypes.HANDLE,
                            wintypes.DWORD, wintypes.LPCWSTR]

path_buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
result = _SHGetFolderPath(0, CSIDL_DESKTOP, 0, 0, path_buf)

desktop = path_buf.value 
a =""

def init(page:ft.Page):
    def button_clicked(e):
        global dbvalue
        global dbpass
        dbvalue = t1.value
        dbpass = t2.value
        page.window.close()
    page.window.center()
    page.window.to_front()
    
    t1 = ft.TextField(label="Enter the database name")
    t2 = ft.TextField(label="Enter the database password",password=True, can_reveal_password=True)
    page.add(Text(value="Please enter the necessary details:",size = 30),
             t1,
             t2,
             ElevatedButton(text="Submit", on_click=button_clicked)),
    page.vertical_alignment= MainAxisAlignment.CENTER,
    page.horizontal_alignment= CrossAxisAlignment.CENTER,
    page.spacing=30
    page.update()
        
ft.app(init)

def main(page:ft.Page):
    def Reconvert(a,x):
        con=mc.connect(host="localhost",user="root",password=dbpass,database = dbvalue)
        curs = con.cursor()
        F = []
        H = []
        with open(a,'r') as F2:
            csv_read=csv.reader(F2)
            for i in csv_read:
                F.append(i)

        def Table(F,k):
            d = 0
            L = F[0]
            J = F[-1]
            w = F[-2][1]
            h = "Create table {} (".format(k)
            for i in L:
                h = h + i + " " + J[d] + ","
                d += 1
            h = h.rstrip(",")
            h = h + ")"
            
            curs.execute(h)
            curs.execute("Alter table {} add PRIMARY KEY({})".format(k,w))

        Table(F,x)
        A = F[-1]
        
        Y = F[1:-2]
        
        k = len(F[0])
        for i in Y:
            for j in range(k):
                if "int" in A[j]:
                    r = i[j]
                    H.append(int(r))
                else:
                    r =  str(i[j]) 
                    H.append(r)
            l = "insert into {} values("
            
            for y in range(k):
                if type(H[y]) is int:
                    l = l + str(H[y]) + ","
                else:
                    l = l + "'" + H[y] + "'" + ","
            l = l.rstrip(",") 
            l = l + ")"
            H = []
            curs.execute(l.format(x))
            con.commit()
        print("Your table is complete")

    def Convert(data,a,desktop):
        def Primary(a):
            k = 0
            A = []
            P = []
            curs.execute("desc {}".format(a))
            data=curs.fetchall()
            for i in data:
                if i[3] == "PRI":
                    b = i[0]
                    z = i[1]
                A.append(i[1])
                P.append(i[0])
                k += 1
            con.close()
            return b,z,k,A,P
        con=mc.connect(host="localhost",user="root",password=dbpass,database = dbvalue)
        curs = con.cursor()
        b = Primary(a)
        P = b[4]
        A = b[3]
        o = b[0]
        os.makedirs(os.path.dirname(desktop), exist_ok=True)
        with open(desktop,'w',newline='') as F:
            csv_writer=csv.writer(F,delimiter=',')
            csv_writer.writerow(P)
            for j in data:
                csv_writer.writerow(j)
            csv_writer.writerow([a,o,""])
            csv_writer.writerow(A)
        with open(desktop,'r') as F2:
            csv_read=csv.reader(F2)
            for i in csv_read:
                print(i)

    page.title = "MySQL Conversion"
    page.window.center()
    page.window.to_front()
    def pick_files_result(e: ft.FilePickerResultEvent):
            selected_files.value = (
                ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
            )
            selected_files.size = 15
            global a 
            for f in pick_files_dialog.result.files:
                 a = f.path
            selected_files.update()
            continuing.text= "Continue?"
            continuing.visible = True
            continuing.on_click = lambda _:page.go('/table')
            continuing.update()
            
    def click(e):
        global a
        h = tb.value
        Reconvert(a,h)
        End.value = "The table has been created!"
        End.update()
    
    def submit(e):
        B2.on_click = lambda _:page.go('/Limbo')
        B2.update()
        global value4
        value4 = tb1.value

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()
    continuing = ft.ElevatedButton(text= " ",visible=False)
    tb = ft.TextField(label="Enter",on_submit=click)
    tb1 = ft.TextField(label="Enter table name",on_change=submit)
    page.overlay.append(pick_files_dialog)
    End = ft.Text(value="Enter the new table name",size = 50)
    B2 = ElevatedButton("Submit")


    def route_change(e : RouteChangeEvent) -> None:
        page.views.clear()
        
        page.views.append(
            View(
                route = '/',
                controls=[
                    AppBar(title=Text("Home"),bgcolor='indigo'),
                    Text(value = "What would you like to do?",size=50),
                    ElevatedButton(
                        content = Container(
                            content = Column(
                                [
                                    Text(value ="""
                                         
              Convert

                                          """,size=30)
                                ],
                            ),
                        ),on_click=lambda _:page.go('/Convert')
                    ),
                    ElevatedButton(
                        content = Container(
                            content = Column(
                                [
                                    Text(value ="""
                                         
              Reconvert

                                          """,size=30)
                                ],
                            ),
                        ),on_click=lambda _:page.go('/Reconvert')
                    )
                ],
                vertical_alignment= MainAxisAlignment.CENTER,
                horizontal_alignment= CrossAxisAlignment.CENTER,
                spacing=26
            )    
        )
        

        if page.route == '/Convert':
            page.views.append(
                View(
                    route = '/Convert',
                    controls=[
                        AppBar(title=Text("Convert"),bgcolor='blue'),
                        Text(value = "Please enter the table name",size=50),
                        tb1,
                        B2
                    ],
                    vertical_alignment= MainAxisAlignment.CENTER,
                    horizontal_alignment= CrossAxisAlignment.CENTER,
                    spacing=26
                )    
            )
        elif page.route == '/Reconvert':
            page.views.append(
                View(
                    route = '/Reconvert',
                    controls=[
                        AppBar(title=Text("Reconvert"),bgcolor='blue'),
                        Text(value = "Please select your .csv file",size=50),
                        ElevatedButton(
                             "Open file explorer",
                             icon=ft.icons.UPLOAD_FILE,
                             on_click=lambda _: pick_files_dialog.pick_files(
                                  allow_multiple=False
                             ),
                        ),
                        selected_files,
                        continuing,
                    ],
                    vertical_alignment= MainAxisAlignment.CENTER,
                    horizontal_alignment= CrossAxisAlignment.CENTER,
                    spacing=26
                )    
            )
        elif page.route == '/table':
            page.views.append(
                View(
                    route = '/table',
                    controls=[
                        AppBar(title=Text("Please enter table name"),bgcolor='blue'),
                        End,
                        tb,
                        
                    ],
                    vertical_alignment= MainAxisAlignment.CENTER,
                    horizontal_alignment= CrossAxisAlignment.CENTER,
                    spacing=26
                )    
            )

        elif page.route == '/Limbo':
            while True:
                try:
                    print(value4)
                    curs.execute("Select * from {}".format(value4))
                    data = curs.fetchall()
                    break
                except:
                    con=mc.connect(host="localhost",user="root",password=dbpass,database = dbvalue)
                    curs = con.cursor()
                    continue
            
            Convert(data,value4,desktop + '/{}'.format(value4) + '.csv')
            page.views.append(
                View(
                    route = '/Limbo',
                    controls=[
                        AppBar(title=Text("Enter table name"),bgcolor='blue'),
                        Text(value = "Your table has been converted to .csv",size = 30),
                        Text(value = "Please find your file on the desktop", size = 30)
                    ],
                    vertical_alignment= MainAxisAlignment.CENTER,
                    horizontal_alignment= CrossAxisAlignment.CENTER,
                    spacing=26
                )    
            )
        
        page.update()
    def view_pop(e: ViewPopEvent) -> None:
        page.views.pop()
        top_view: View = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

con=mc.connect(host="localhost",user="root",password=dbpass,database = dbvalue)
curs = con.cursor()

if __name__ == '__main__':

    ft.app(target=main)