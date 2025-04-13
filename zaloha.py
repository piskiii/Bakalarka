from tkinter import *
from tkinter import messagebox
import customtkinter
from PIL import Image
import json
import os

window = customtkinter.CTk()
window.geometry("1040x720")
window.title("Program")
window.resizable("false","false")

#Pridanie funkcii pre zmenu frame
def Zmen1():
    tool_frame1.grid_forget()
    tool_frame3.grid_forget()
    tool_frame4.grid_forget()
    tool_frame2.grid(row=1, column=3, padx=10, pady=10, sticky=N + S)

def Zmen2():
    tool_frame2.grid_forget()
    tool_frame3.grid_forget()
    tool_frame4.grid_forget()
    tool_frame1.grid(row=1, column=3, padx=10, pady=10, sticky=N + S)

def Zmen3():
    tool_frame1.grid_forget()
    tool_frame2.grid_forget()
    tool_frame4.grid_forget()
    tool_frame3.grid(row=1, column=3, padx=10, pady=10, sticky=N + S)

def Zmen4():
    tool_frame1.grid_forget()
    tool_frame2.grid_forget()
    tool_frame3.grid_forget()
    tool_frame4.grid(row=1, column=3, padx=10, pady=10, sticky=N + S)

#Vytvorenie Frame
menu_frame = customtkinter.CTkFrame(window, height= 50)
menu_frame.grid(row = 0, column = 0, padx = 10, sticky = N+E+W)
main_frame = customtkinter.CTkFrame(window, width= 800, height= 650)
main_frame.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 10)
tool_frame2 = customtkinter.CTkScrollableFrame(window, width= 170)
tool_frame2.grid(row = 1, column = 3, padx = 10, pady = 10, sticky = N+S)
tool_frame1 = customtkinter.CTkScrollableFrame(window, width= 170)
tool_frame3 = customtkinter.CTkScrollableFrame(window, width= 170)
tool_frame4 = customtkinter.CTkScrollableFrame(window, width= 170)
ar_frame = customtkinter.CTkFrame(window, height= 50)
ar_frame.grid(row = 0, column = 3)

support1 = customtkinter.CTkImage(dark_image=Image.open("image/support1.jpg"), size=(60, 60))
line = customtkinter.CTkImage(dark_image=Image.open("image/line.jpg"), size=(60, 60))
arc = customtkinter.CTkImage(dark_image=Image.open("image/arc.jpg"), size=(60, 60))


#Canvas
canvas = Canvas(main_frame, bg="white", width= 1000, height= 800)
canvas.pack()

drawing_line_enabled = False

#zoznam na ulozenie ciar
lines = []
redo_lines = []
dim_lines = []
con_point = []

selected_line = None

# Pridanie premenných pre počiatočnú pozíciu a aktuálnu čiaru
start_x, start_y = None, None
current_line = None

# Pridanie premenných pre body
start_point = None
end_point = None

#funckia pre ulozenie platna
def save_canvas():
    canvas_data = []
    deselect_line()
    for line in lines:
        coords = canvas.coords(line)
        color = canvas.itemcget(line, 'fill')
        canvas_data.append({'coords': coords, 'color': color})
    with open('canvas_data.json', 'w') as f:
        json.dump(canvas_data, f)

#funkcia pre nacitanie platna
def load_canvas():
    global lines
    if not os.path.exists('canvas_data.json'):
        with open('canvas_data.json', 'w') as f:
            json.dump([], f)
    with open('canvas_data.json', 'r') as f:
        canvas_data = json.load(f)
    for item in canvas_data:
        line = canvas.create_line(item['coords'], fill=item['color'], width=3)
        lines.append(line)
        draw_dim_line(item['coords'][0], item['coords'][1], item['coords'][2], item['coords'][3])

#funkcia pre kreslenie kotovacej ciary
def draw_dim_line(start_x, start_y, end_x, end_y):
    global  dim
    mid_x = (start_x + end_x) / 2
    mid_y = (start_y + end_y) / 2
    if start_x - end_x == 0:
        line3 = canvas.create_line(start_x-50, start_y, end_x-50, end_y, fill='black', width=2, arrow=BOTH)
        dim = abs(start_y - end_y)
        text = canvas.create_text(mid_x-60, mid_y, text=f"{int(dim)}", font=('Arial', 15), fill='black', angle = 90)
        line1 = canvas.create_line(start_x, start_y, start_x-50, start_y, fill='black', width=1)
        line2 = canvas.create_line(end_x, end_y, end_x-50, end_y, fill='black', width=1)
    else:
        line3 = canvas.create_line(start_x, start_y+50, end_x, end_y+50, fill='black', width=2, arrow=BOTH)
        dim = abs(start_x - end_x)
        text = canvas.create_text(mid_x, mid_y+40, text=f"{int(dim)}", font=('Arial', 15), fill='black')
        line1 = canvas.create_line(start_x, start_y, start_x, start_y+50, fill='black', width=1)
        line2 = canvas.create_line(end_x, end_y, end_x, end_y+50, fill='black', width=1)
    dim_lines.append((text, line1, line2, line3))

#funkcia na zmenu rozmeru ciary
def change_dim_line():
    move_point = None
    flag = False
    if selected_line:
        selected_coords = canvas.coords(selected_line)
        dialog = customtkinter.CTkInputDialog(text="Please enter the dimension:", title="Input Dimension")
        user_input = dialog.get_input()
        if user_input.isdigit() and user_input != "0":
            # Delete the selected line
            canvas.delete(selected_line)
            lines.remove(selected_line)
            for item in dim_lines[selected_line_position]:
                canvas.delete(item)
            dim_lines.pop(selected_line_position)
            # Change the dimension of the line
            for point in con_point:
                if (selected_coords[0], selected_coords[1]) == point:
                    move_point = selected_coords[0], selected_coords[1]
                elif (selected_coords[2], selected_coords[3]) == point:
                    move_point = selected_coords[2], selected_coords[3]
                    flag = True
            if selected_coords[0] - selected_coords[2] == 0:
                dif=abs(selected_coords[1]-selected_coords[3]) - int(user_input)
                if selected_coords[1] > selected_coords[3]:
                    selected_coords[3]+=dif
                else:
                    selected_coords[1]+=dif
            else:
                dif=abs(selected_coords[0]-selected_coords[2]) - int(user_input)
                if selected_coords[0] > selected_coords[2]:
                    selected_coords[2]+=dif
                else:
                    selected_coords[0]+=dif
            new_line = canvas.create_line(selected_coords, fill='black', width=3)
            lines.append(new_line)
            if move_point is not None and flag == False:
                cur_coords = canvas.coords(new_line)
                delta = move_point[0] - cur_coords[0], move_point[1] - cur_coords[1]
                canvas.move(new_line, delta[0], delta[1])
                selected_coords = canvas.coords(new_line)
            elif move_point is not None and flag == True:
                cur_coords = canvas.coords(new_line)
                delta = move_point[0] - cur_coords[2], move_point[1] - cur_coords[3]
                canvas.move(new_line, delta[0], delta[1])
                selected_coords = canvas.coords(new_line)
            draw_dim_line(selected_coords[0], selected_coords[1], selected_coords[2], selected_coords[3])

        else:
            messagebox.showerror("Error", "Please enter a valid number")
            change_dim_line()


# Pridanie funkcií pre kreslenie ciary
def start_draw_line(event):
    global start_x, start_y, current_line
    if drawing_line_enabled:
        start_x, start_y = event.x, event.y
        threshold = 40  # Define a threshold distance for snapping

        # Check if the starting point is near the end or start of an existing line
        for line in lines:
            coords = canvas.coords(line)
            start_point = (coords[0], coords[1])
            end_point = (coords[2], coords[3])

            if abs(start_x - start_point[0]) < threshold and abs(start_y - start_point[1]) < threshold:
                start_x, start_y = start_point
                con_point.append(start_point)
                break
            elif abs(start_x - end_point[0]) < threshold and abs(start_y - end_point[1]) < threshold:
                start_x, start_y = end_point
                con_point.append(end_point)
                break

        current_line = canvas.create_line(start_x, start_y, event.x, event.y, fill='black', width=3)

def draw_line(event):
    global current_line
    if drawing_line_enabled and current_line:
        if abs(event.x - start_x) > abs(event.y - start_y):
            # Kresli vodorovnú čiaru
            canvas.coords(current_line, start_x, start_y, event.x, start_y)
        else:
            # Kresli zvislú čiaru
            canvas.coords(current_line, start_x, start_y, start_x, event.y)

def stop_draw_line(event):
    global start_x, start_y, current_line, start_xend, start_yend
    if drawing_line_enabled and current_line:
        if abs(event.x - start_x) > abs(event.y - start_y):
            # Kresli vodorovnú čiaru
            canvas.coords(current_line, start_x, start_y, event.x, start_y)
            draw_dim_line(start_x, start_y, event.x, start_y)
            start_xend = start_x
            start_yend = start_y + 50
        else:
            # Kresli zvislú čiaru
            canvas.coords(current_line, start_x, start_y, start_x, event.y)
            draw_dim_line(start_x, start_y, start_x, event.y)
        lines.append(current_line)
        current_line = None
    start_x, start_y = None, None

#funkcia na povolenie kreslenia ciary
def enable_line_drawing():
    deselect_line()
    canvas.bind('<Button-1>', start_draw_line)
    global drawing_line_enabled
    drawing_line_enabled = True

#funckie vratit spat a dopredu
def undo():
    if lines:
        line = lines.pop()
        coords = canvas.coords(line)
        canvas.delete(line)
        redo_lines.append(coords)
        if dim_lines:
            dim = dim_lines.pop()
            for item in dim:
                canvas.delete(item)

def redo():
    if redo_lines:
        coords = redo_lines.pop()
        new_line = canvas.create_line(coords, fill='black', width=3)
        lines.append(new_line)
        draw_dim_line(coords[0], coords[1], coords[2], coords[3])

#funkcia na označenie ciary
def select_line(event):
    global selected_line, selected_line_position
    item = canvas.find_closest(event.x, event.y)
    if item:
        if selected_line:
            canvas.itemconfig(selected_line, fill='black')
        selected_line = item[0]
        canvas.itemconfig(selected_line, fill='red')

        selected_coords = canvas.coords(selected_line)
        for index, line in enumerate(lines):
            if canvas.coords(line) == selected_coords:
                selected_line_position = index
                break

#funkcia na odznačenie ciary
def deselect_line():
    global selected_line
    if selected_line:
        canvas.itemconfig(selected_line, fill='black')
        selected_line = None

#bindovanie funkcie na označenie ciary
def bind_select():
    canvas.bind('<Button-1>', select_line)

# Funkcia na vymazanie všetkých objektov na plátne
def clear_canvas():
    global lines, redo_lines, dim_lines, selected_line
    # Clear all items from the canvas
    canvas.delete("all")
    # Reset the lists and selected line
    lines = []
    redo_lines = []
    dim_lines = []
    selected_line = None


# Bindovanie eventov pre myš
canvas.bind('<Button-1>', start_draw_line)
canvas.bind('<B1-Motion>', draw_line)
canvas.bind('<ButtonRelease-1>', stop_draw_line)


#buttons in tool_frame
button1 = customtkinter.CTkButton(tool_frame1, image=support1, text="")
button1.pack(padx=5, pady=5, ipady=10)
button2 = customtkinter.CTkButton(tool_frame1, image=support1, text="")
button2.pack(padx=5, pady=5, ipady=10)
button3 = customtkinter.CTkButton(tool_frame1, image=support1, text="")
button3.pack(padx=5, pady=5, ipady=10)
button4 = customtkinter.CTkButton(tool_frame1, image=support1, text="")
button4.pack(padx=5, pady=5, ipady=10)
button5 = customtkinter.CTkButton(tool_frame1, image=support1, text="")
button5.pack(padx=5, pady=5, ipady=10)
button6 = customtkinter.CTkButton(tool_frame1, image=support1, text="")
button6.pack(padx=5, pady=5, ipady=10)
button7 = customtkinter.CTkButton(tool_frame1, image=support1, text="")
button7.pack(padx=5, pady=5, ipady=10)
button8 = customtkinter.CTkButton(tool_frame1, image=support1, text="")
button8.pack(padx=5, pady=5, ipady=10)

button9 = customtkinter.CTkButton(tool_frame2, image=line, text="", command=enable_line_drawing)
button9.pack(padx=5, pady=5, ipady=10)
button9 = customtkinter.CTkButton(tool_frame2, image=arc, text="")
button9.pack(padx=5, pady=5, ipady=10)
button10 = customtkinter.CTkButton(tool_frame2, text="select" , command=bind_select)
button10.pack(padx=5, pady=5, ipady=10)

#buttons in menu
button_menu1 = customtkinter.CTkButton(menu_frame, text="Výpočet", width= 105)
button_menu1.grid(row=0, column=0, padx = 5, pady = 5, ipady = 10)
button_menu2 = customtkinter.CTkButton(menu_frame, text="Ulož", command=save_canvas, width= 105)
button_menu2.grid(row=0, column=1, padx = 5, pady = 5, ipady = 10)
button_menu3 = customtkinter.CTkButton(menu_frame, text="Zmeň rozmer", width= 105, command=change_dim_line)
button_menu3.grid(row=0, column=2, padx = 5, pady = 5, ipady = 10)
button_menu4 = customtkinter.CTkButton(menu_frame, text="podpory", command=Zmen2, width= 105)
button_menu4.grid(row=0, column=3, padx = 5, pady = 5, ipady = 10)
button_menu5 = customtkinter.CTkButton(menu_frame, text="prúty", command=Zmen1, width= 105)
button_menu5.grid(row=0, column=4, padx = 5, pady = 5, ipady = 10)
button_menu6 = customtkinter.CTkButton(menu_frame, text="sily", command=Zmen3, width= 105)
button_menu6.grid(row=0, column=5, padx = 5, pady = 5, ipady = 10)
button_menu7 = customtkinter.CTkButton(menu_frame, text="momenty", command=Zmen4, width= 105)
button_menu7.grid(row=0, column=6, padx = 5, pady = 5, ipady = 10)

#AR buttons
button_AR1 = customtkinter.CTkButton(ar_frame, text="dozadu", width= 10, height= 15, command=undo)
button_AR1.grid(row=0, column=0, padx = 5, pady = 5, ipady = 10)
button_AR2 = customtkinter.CTkButton(ar_frame, text="dopredu", width= 10, height= 15, command=redo)
button_AR2.grid(row=0, column=1, padx = 5, pady = 5, ipady = 10)
button_AR3 = customtkinter.CTkButton(ar_frame, text="vymaž", width= 10, height= 15, command=clear_canvas)
button_AR3.grid(row=0, column=2, padx = 5, pady = 5, ipady = 10)

#nacitanie platna
load_canvas()

window.mainloop()


"""""
    # Upravená časť pre pridanie horizontálnych a vertikálnych súradníc
    comb_hor = [[] for _ in range(len(lines))]
    comb_ver = [[] for _ in range(len(lines))]

    l = 0
    for line_obj in lines:
        coords = canvas.coords(line_obj)  # Získanie súradníc prútu z plátna
        start = (coords[0], coords[1])
        end = (coords[2], coords[3])
        beam_type, direction = identify_beam_type_and_direction(start, end)

        # Pre horizontálny prút kontrolujeme horizontálne súradnice
        if beam_type == 'horizontal':
            for hor in combinated_hor:
                if min(start[0], end[0]) <= hor <= max(start[0], end[0]):
                    if hor not in comb_hor[l]:  # Pridáme len, ak už nie je prítomné
                        comb_hor[l].append(hor)

        # Pre vertikálny prút kontrolujeme vertikálne súradnice
        elif beam_type == 'vertical':
            for ver in combinated_ver:
                if min(start[1], end[1]) <= ver <= max(start[1], end[1]):
                    if ver not in comb_ver[l]:  # Pridáme len, ak už nie je prítomné
                        comb_ver[l].append(ver)
        l += 1

    # Triedenie hodnôt v každom vnútornom zozname pre prehľadnosť
    for i in range(len(comb_hor)):
        comb_hor[i] = sorted(set(comb_hor[i]))  # Odstránenie duplicitných hodnôt a zoradenie
    for i in range(len(comb_ver)):
        comb_ver[i] = sorted(set(comb_ver[i]))  # Odstránenie duplicitných hodnôt a zoradenie

    # Aktualizácia comb_ver: odstránenie hodnôt, ktoré nepatria k aktuálnemu prútu
    for i in range(len(lines)):
        coords = canvas.coords(lines[i])  # Získame súradnice prútu
        start_y = min(coords[1], coords[3])
        end_y = max(coords[1], coords[3])
        comb_ver[i] = [ver for ver in comb_ver[i] if start_y <= ver <= end_y]

    # Odstránenie prázdnych vnútorných zoznamov
    comb_hor = [item for item in comb_hor if item]
    comb_ver = [item for item in comb_ver if item]

    # Výstup výsledkov
    print("comb_hor:", comb_hor)
    print("comb_ver:", comb_ver)

"""""

"""""
    # Získanie súradníc prútov
    for line in lines:
        coords = canvas.coords(line)
        coords_c.append(coords)
        if coords[1] == coords[3]:
            combinated_hor.append(coords[0])
            combinated_hor.append(coords[2])
        else:
            combinated_ver.append(coords[1])
            combinated_ver.append(coords[3])

        for force in force_obj:
            force = canvas.coords(force)
            if min(coords[0],coords[2])<=force[0]<=max(coords[0],coords[2]):
                force_c.append(force)
                combinated_hor.append(force[0])
            elif min(coords[1],coords[3])<=force[1]<=max(coords[1],coords[3]):
                force_c.append(force)
                combinated_ver.append(force[1])

            size_c += 1

        for sup in sup_obj:
            sup = canvas.coords(sup)
            if min(coords[0],coords[2])<=sup[0]<=max(coords[0],coords[2]):
                combinated_hor.append(sup[0])
                sup_obj_c.append(sup)
            elif min(coords[1], coords[3]) <= sup[1] <= max(coords[1], coords[3]):
                combinated_ver.append(sup[1])
                sup_obj_c.append(sup)
            if sup != coords_c:
                size_c += 1


        for moment in M_dot:
            if min(coords[0],coords[2])<=moment[0]<=max(coords[0],coords[2]):
                combinated_hor.append(moment[0])
            elif min(coords[1], coords[3]) <= moment[1] <= max(coords[1], coords[3]):
                combinated_ver.append(moment[1])

        i = 0
        for lin_force in force_linear:
            if (min(coords[0],coords[2])<=lin_force[0]<=max(coords[0],coords[2]) or min(coords[0],coords[2])<=lin_force[2]<=max(coords[0],coords[2])):
                if (force_linear_mag[i][1] > force_linear_mag[i][0]):
                    linear_mag = float(force_linear_mag[i][0]) * abs(lin_force[0] - lin_force[2]) + (
                                float(force_linear_mag[i][1]) * abs(lin_force[0] - lin_force[2])) / 2
                    sum_force_y = sum_force_y + linear_mag
                    ay_lin = 2 * abs(lin_force[0] - lin_force[2]) / 3 + lin_force[0]
                elif (force_linear_mag[i][1] < force_linear_mag[i][0]):
                    linear_mag = float(force_linear_mag[i][1]) * abs(lin_force[0] - lin_force[2]) + (
                                float(force_linear_mag[i][0]) * abs(lin_force[0] - lin_force[2])) / 2
                    sum_force_y = sum_force_y - linear_mag
                    ay_lin = abs(lin_force[0] - lin_force[2]) / 3 + lin_force[0]
                elif (force_linear_mag[i][1] == force_linear_mag[i][0]):
                    linear_mag = float(force_linear_mag[i][0]) * abs(lin_force[0] - lin_force[2])
                    sum_force_y = sum_force_y + linear_mag
                    ay_lin = abs(lin_force[0] - lin_force[2]) / 2 + lin_force[0]

                k = (float(force_linear_mag[i][1]) - float(force_linear_mag[i][0])) / abs(lin_force[0] - lin_force[2])
                c = float(force_linear_mag[i][0]) - k * lin_force[0]

                combinated_hor.append(lin_force[0])
                combinated_hor.append(lin_force[2])
            elif (min(coords[1], coords[3]) <= lin_force[1] <= max(coords[1], coords[3]) or min(coords[1], coords[3]) <= lin_force[3] <= max(coords[1], coords[3])):
                if (force_linear_mag[i][1] > force_linear_mag[i][0]):
                    linear_mag = float(force_linear_mag[i][0]) * abs(lin_force[1] - lin_force[3]) + (
                            float(force_linear_mag[i][1]) * abs(lin_force[1] - lin_force[3])) / 2
                    sum_force_x = sum_force_x + linear_mag
                    ax_lin = 2 * abs(lin_force[1] - lin_force[3]) / 3 + lin_force[1]
                elif (force_linear_mag[i][1] < force_linear_mag[i][0]):
                    linear_mag = float(force_linear_mag[i][1]) * abs(lin_force[1] - lin_force[3]) + (
                            float(force_linear_mag[i][0]) * abs(lin_force[1] - lin_force[3])) / 2
                    sum_force_x = sum_force_x - linear_mag
                    ax_lin = abs(lin_force[1] - lin_force[3]) / 3 + lin_force[1]
                elif (force_linear_mag[i][1] == force_linear_mag[i][0]):
                    linear_mag = float(force_linear_mag[i][0]) * abs(lin_force[1] - lin_force[3])
                    sum_force_x = sum_force_x + linear_mag
                    ax_lin = abs(lin_force[1] - lin_force[3]) / 2 + lin_force[1]
                combinated_ver.append(lin_force[1])
                combinated_ver.append(lin_force[3])
            i += 1
        """


"""""
    # Konverzia zoznamov na NumPy array
    coords_c = np.array(coords_c, dtype=np.float32).flatten()
    force_c = np.array(force_c, dtype=np.float32).flatten()
    sup_obj_c = np.array(sup_obj_c, dtype=np.float32).flatten()
    force_mag = np.array(force_mag, dtype=np.float32)
    sup_obj_ind = np.array(sup_obj_ind, dtype=np.int32)
    force_angle = np.array(force_angle, dtype=np.int32)
    x = np.array(x, dtype=np.float32)
    lin_mag_c = np.array(force_linear_mag, dtype=np.float32)
    lin_force = np.array(lin_force, dtype=np.float32)

    # Počet prútov
    num_lines = len(coords_c) // 4
    num_force = len(force_c) // 4
    num_sup = len(sup_obj_c) // 2

    # Vytvorenie poľa na ukladanie dĺžok
    lengths_array = np.zeros(num_lines*4, dtype=np.float32)
    lengths_array_c = np.zeros(num_force*5, dtype=np.float32)
    lengths_array_sup = np.zeros(num_sup*3, dtype=np.float32)


    # Načítanie knižnice
    calc_lib = ctypes.CDLL('C:\\Users\\palko\\CLionProjects\\untitled\\calc.dll')

    # Definovanie typov argumentov
    calc_lib.calculate_lengths.argtypes = (
        ctypes.POINTER(ctypes.c_float),  # coords_c
        ctypes.c_int,                    # num_lines
        ctypes.POINTER(ctypes.c_float),  # lengths_array
        ctypes.POINTER(ctypes.c_float),   # force_c
        ctypes.c_int,                    # num_force
        ctypes.POINTER(ctypes.c_float),   # lengths_array_c
        ctypes.POINTER(ctypes.c_float),   # force_mag
        ctypes.POINTER(ctypes.c_float),   # sup_obj_c
        ctypes.c_int,                    # num_sup
        ctypes.POINTER(ctypes.c_float),  # lengths_array_sup
        ctypes.POINTER(ctypes.c_int),   # sup_obj_ind
        ctypes.POINTER(ctypes.c_int),     # force_angle
        ctypes.c_int,                    # size_c
        ctypes.POINTER(ctypes.c_float),  # X
        ctypes.c_float,                  # k
        ctypes.c_float,                  # c
        ctypes.POINTER(ctypes.c_float),   # mag
        ctypes.POINTER(ctypes.c_float)   # lin_force
    )
    # Zavolanie C funkcie s argumentmi
    calc_lib.calculate_lengths(
        coords_c.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        num_lines,
        lengths_array.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        force_c.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        num_force,
        lengths_array_c.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        force_mag.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        sup_obj_c.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        num_sup,
        lengths_array_sup.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        sup_obj_ind.ctypes.data_as(ctypes.POINTER(ctypes.c_int)),
        force_angle.ctypes.data_as(ctypes.POINTER(ctypes.c_int)),
        size_c,
        x.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        k,
        c,
        lin_mag_c.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        lin_force.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    )

    # Výstup dĺžok prútov
    print("Súradnice prútov:", lengths_array)
    print("Súradnice sil:", lengths_array_c)
    print("Podpory:", lengths_array_sup)
    print("lineárne sily:", lin_mag_c)
"""






