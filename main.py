import traceback
from tkinter import *
from tkinter import messagebox, Scale, HORIZONTAL, ttk
import customtkinter
from customtkinter import CTkToplevel
from PIL import Image, ImageTk
import json
import math
import os

import numpy as np
import matplotlib.pyplot as plt
import ctypes
import collections
from collections import defaultdict


window = customtkinter.CTk()
window.geometry("1280x720")
customtkinter.set_widget_scaling(1)  # widget dimensions and text size
customtkinter.set_window_scaling(1)  # window geometry dimensions
window.title("VVU")
window.resizable("True","True")
window.minsize(1024, 768)

window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(3, weight=0)

#Pridanie funkcii pre zmenu frame
def Zmen1():
    tool_frame1.grid_forget()
    tool_frame3.grid_forget()
    tool_frame2.grid(row=1, column=3, padx=10, pady=10, sticky=N + S)

def Zmen2():
    tool_frame2.grid_forget()
    tool_frame3.grid_forget()
    tool_frame1.grid(row=1, column=3, padx=10, pady=10, sticky=N + S)

def Zmen3():
    tool_frame1.grid_forget()
    tool_frame2.grid_forget()
    tool_frame3.grid(row=1, column=3, padx=10, pady=10, sticky=N + S)

#Vytvorenie Frame
menu_frame = customtkinter.CTkFrame(window, height= 30)
menu_frame.grid(row = 0, column = 0, padx = 10, sticky = N+E+W)
main_frame = customtkinter.CTkFrame(window, width= 800, height= 650)
main_frame.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 10)
tool_frame2 = customtkinter.CTkScrollableFrame(window, width= 170)
tool_frame2.grid(row = 1, column = 3, padx = 10, pady = 10, sticky = N+S)
tool_frame1 = customtkinter.CTkScrollableFrame(window, width= 170)
tool_frame3 = customtkinter.CTkScrollableFrame(window, width= 170)
ar_frame = customtkinter.CTkFrame(window, height= 30)
ar_frame.grid(row = 0, column = 3)

menu_frame.grid_columnconfigure(0, weight=1)
menu_frame.grid_columnconfigure(1, weight=1)
menu_frame.grid_columnconfigure(2, weight=1)
menu_frame.grid_columnconfigure(3, weight=1)
menu_frame.grid_columnconfigure(4, weight=1)
menu_frame.grid_columnconfigure(5, weight=1)
menu_frame.grid_columnconfigure(6, weight=1)
menu_frame.grid_columnconfigure(7, weight=1)

support1 = customtkinter.CTkImage(dark_image=Image.open("image/sup1.jpg"), size=(50, 50))
support2 = customtkinter.CTkImage(dark_image=Image.open("image/sup2.jpg"), size=(50, 50))
support3 = customtkinter.CTkImage(dark_image=Image.open("image/sup3.jpg"), size=(50, 50))
support4 = customtkinter.CTkImage(dark_image=Image.open("image/sup4.jpg"), size=(50, 50))
support5 = customtkinter.CTkImage(dark_image=Image.open("image/sup5.jpg"), size=(50, 50))
line = customtkinter.CTkImage(dark_image=Image.open("image/line.jpg"), size=(60, 60))
arc_1 = customtkinter.CTkImage(dark_image=Image.open("image/arc1.jpg"), size=(60, 60))
arc_2 = customtkinter.CTkImage(dark_image=Image.open("image/arc2.jpg"), size=(60, 60))
arc_3 = customtkinter.CTkImage(dark_image=Image.open("image/arc3.jpg"), size=(60, 60))
arc_4 = customtkinter.CTkImage(dark_image=Image.open("image/arc4.jpg"), size=(60, 60))
force = customtkinter.CTkImage(dark_image=Image.open("image/force.jpg"), size=(60, 60))
save = customtkinter.CTkImage(dark_image=Image.open("image/save.png"), size=(30, 30))
calculate = customtkinter.CTkImage(dark_image=Image.open("image/calculate.png"), size=(30, 30))
change_dimension = customtkinter.CTkImage(dark_image=Image.open("image/change_dimension.png"), size=(30, 30))
undo_image = customtkinter.CTkImage(dark_image=Image.open("image/undo.png"), size=(30, 30))
redo_image = customtkinter.CTkImage(dark_image=Image.open("image/redo.png"), size=(30, 30))
delete_image = customtkinter.CTkImage(dark_image=Image.open("image/delete.png"), size=(30, 30))
beam_image = customtkinter.CTkImage(dark_image=Image.open("image/beam.png"), size=(30, 30))
select_image = customtkinter.CTkImage(dark_image=Image.open("image/select.png"), size=(30, 30))
move_image = customtkinter.CTkImage(dark_image=Image.open("image/move.png"), size=(30, 30))
linear_force = customtkinter.CTkImage(dark_image=Image.open("image/linear.png"), size=(100, 60))
moment_image = customtkinter.CTkImage(dark_image=Image.open("image/moment.png"), size=(60, 60))

#Canvas
canvas = Canvas(main_frame, bg="white", width= 5000, height= 5000)
canvas.pack(expand = YES, fill = BOTH)

drawing_line_enabled = False
drawing_arc_enabled = False

# premenne pre current line a obluk
current_dim_arc = None
change_dim_flag = False
current_dim_line = None

#zoznam na ulozenie ciar
lines = []
redo_lines = []
redo_angles = []
dim_lines = []
con_point = []

#zoznam na ulozenie oblukov
arcs = []
dim_arcs = []

# Pridanie premenných pre podporu
sup_obj = []
sup_obj_image = []
sup_obj_ind = []
sup_angle = 0
place_support_flag = False
sup_x, sup_y = None, None

# Pridanie premenných pre silu
force_obj = []
force_mag = []
force_linear = []
force_linear_mag = []
force_angle = []
place_force_flag = False
force_counter = 0

M_dot = []
M_mag = []
moment_counter = 0
place_moment_flag = False

# Pridanie premenných pre označenú čiaru a oblúk
selected_line = None
selected_arc = None
selected_image = None
selected_line_position = None
selected_arc_position = None
selected_image_position = None

# Pridanie premenných pre počiatočnú pozíciu a aktuálnu čiaru
start_x, start_y = None, None
current_line = None
start_xend, start_yend = None, None
current_arc = None

# Pridanie premenných pre body
start_point = None
end_point = None

# Pridanie premenných pre označený oblúk
ind = 0
start_arc = None
end_arc = None

delete_flag = False

order = []
redo_order = []

size_c = 0

#body na prutoch
combinated_hor = []
combinated_ver = []

force_c = []
sup_obj_c = []

ay_lin = []
ax_lin = []
linear_mag_y = []
linear_mag_x = []
sum_force_x = 0
sum_force_y = 0

calc_points = defaultdict(list)

support_image_dict = {}

#funckia pre ulozenie platna
def save_canvas():
    canvas_data_line = []
    canvas_data_arc = []
    deselect_line()
    for line in lines:
        coords = canvas.coords(line)
        color = canvas.itemcget(line, 'fill')
        canvas_data_line.append({'coords': coords, 'color': color})
    for arc in arcs:
        coords = canvas.coords(arc)
        start = canvas.itemcget(arc, 'start')
        extent = canvas.itemcget(arc, 'extent')
        canvas_data_arc.append({'coords': coords, 'start': start, 'extent': extent})
    with open('canvas_data_line.json', 'w') as f:
        json.dump(canvas_data_line, f)
    with open('canvas_data_arc.json', 'w') as f:
        json.dump(canvas_data_arc, f)

#funkcia pre nacitanie platna
def load_canvas():
    global lines, arcs, ind
    if not os.path.exists('canvas_data_line.json'):
        with open('canvas_data_line.json', 'w') as f:
            json.dump([], f)
    with open('canvas_data_line.json', 'r') as f:
        canvas_data_line = json.load(f)
    for item in canvas_data_line:
        line = canvas.create_line(item['coords'], fill=item['color'], width=3)
        lines.append(line)
        draw_dim_line(item['coords'][0], item['coords'][1], item['coords'][2], item['coords'][3])

    if not os.path.exists('canvas_data_arc.json'):
        with open('canvas_data_arc.json', 'w') as f:
            json.dump([], f)
    with open('canvas_data_arc.json', 'r') as f:
        canvas_data_arc = json.load(f)
    for item in canvas_data_arc:
        start = item.get('start', '')
        extent = item.get('extent', '')
        if start and extent:
            start_arc = int(float(start))
            extent_arc = int(float(extent))
            arc = canvas.create_arc(item['coords'], outline='black', width=3, style=ARC, start=start_arc,
                                    extent=extent_arc)
            arcs.append(arc)
            if int(start_arc) == 270:
                ind = 1
            elif int(start_arc) == 0:
                ind = 2
            elif int(start_arc) == 90:
                ind = 3
            elif int(start_arc) == 180:
                ind = 4
            draw_dim_arc(item['coords'][0], item['coords'][1], item['coords'][2], item['coords'][3])


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
    new_dim_line = (text, line1, line2, line3)
    dim_lines.append(new_dim_line)

#funkcia pre kreslenie kotovacej oblukovej ciary
def draw_dim_arc(start_x, start_y, end_x, end_y):
    global dim, ind, current_dim_arc

    text_arc, line_arc = None, None
    mid_x = (start_x + end_x) / 2
    mid_y = (start_y + end_y) / 2
    dim = abs(end_x - start_x)/2
    Theta = 45
    if ind == 1:
        mid_arc_x = mid_x + dim * math.cos(math.radians(Theta))
        mid_arc_y = mid_y + dim * math.sin(math.radians(Theta))
        text_arc = canvas.create_text((mid_x+mid_arc_x)/2, (mid_y+mid_arc_y)/2-15, text=f"R{int(dim)}", font=('Arial', 15), fill='black', angle=Theta-90)
        line_arc = canvas.create_line(mid_x, mid_y, mid_arc_x, mid_arc_y, fill='black', width=1, arrow=LAST)
    elif ind == 2:
        mid_arc_x = mid_x + dim * math.cos(math.radians(Theta))
        mid_arc_y = mid_y - dim * math.sin(math.radians(Theta))
        text_arc = canvas.create_text((mid_x+mid_arc_x)/2, (mid_y+mid_arc_y)/2-15, text=f"R{int(dim)}", font=('Arial', 15), fill='black', angle=Theta)
        line_arc = canvas.create_line(mid_x, mid_y, mid_arc_x, mid_arc_y, fill='black', width=1, arrow=LAST)
    elif ind == 3:
        mid_arc_x = mid_x - dim * math.cos(math.radians(Theta))
        mid_arc_y = mid_y - dim * math.sin(math.radians(Theta))
        text_arc = canvas.create_text((mid_x+mid_arc_x)/2, (mid_y+mid_arc_y)/2-15, text=f"R{int(dim)}", font=('Arial', 15), fill='black', angle=Theta-90)
        line_arc = canvas.create_line(mid_x, mid_y, mid_arc_x, mid_arc_y, fill='black', width=1, arrow=LAST)
    elif ind == 4:
        mid_arc_x = mid_x - dim * math.cos(math.radians(Theta))
        mid_arc_y = mid_y + dim * math.sin(math.radians(Theta))
        text_arc = canvas.create_text((mid_x+mid_arc_x)/2, (mid_y+mid_arc_y)/2-15, text=f"R{int(dim)}", font=('Arial', 15), fill='black', angle=Theta)
        line_arc = canvas.create_line(mid_x, mid_y, mid_arc_x, mid_arc_y, fill='black', width=1, arrow=LAST)
    dim_arcs.append((text_arc, line_arc))
    return(text_arc, line_arc)

#funkcia na zmenu rozmeru ciary
def change_dim_line():
    global ind, change_dim_flag
    move_point = None
    flag = False
    if not selected_line and not selected_arc:
        change_dim_flag = True
        canvas.bind('<Button-1>', select_line)
    if selected_line:
        selected_coords = canvas.coords(selected_line)
        dialog = customtkinter.CTkInputDialog(text="Please enter the dimension:", title="Input Dimension")
        user_input = dialog.get_input()
        if user_input.isdigit() and user_input != "0":
            #pridanie dolezitych bodov
            if selected_coords[1] == selected_coords[3]:
                combinated_hor.remove(canvas.coords(selected_line)[0])
                combinated_hor.remove(canvas.coords(selected_line)[2])
                for beam in calc_points["horizontal"]:
                    if beam["coords"] == selected_coords:  # Porovnáme súradnice
                        calc_points["horizontal"].remove(beam)
            else:
                combinated_ver.remove(canvas.coords(selected_line)[1])
                combinated_ver.remove(canvas.coords(selected_line)[3])
                for beam in calc_points["vertical"]:
                    if beam["coords"] == selected_coords:  # Porovnáme súradnice
                        calc_points["vertical"].remove(beam)

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
                if (selected_coords[2], selected_coords[3]) == point:
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
        if selected_coords[1] == selected_coords[3]:
            combinated_hor.append(canvas.coords(new_line)[0])
            combinated_hor.append(canvas.coords(new_line)[2])
            calc_points["horizontal"].append({
                "coords": canvas.coords(new_line),
                "supports": [],
                "supports_index": [],
                "forces": [],
                "forces_mag": [],
                "forces_angle": [],
                "linear_forces": [],
                "linear_forces_mag": [],
                "moments": [],
                "moments_mag": []
            })
        else:
            combinated_ver.append(canvas.coords(new_line)[1])
            combinated_ver.append(canvas.coords(new_line)[3])
            calc_points["vertical"].append({
                "coords": canvas.coords(new_line),
                "supports": [],
                "supports_index": [],
                "forces": [],
                "forces_mag": [],
                "forces_angle": [],
                "linear_forces": [],
                "linear_forces_mag": [],
                "moments": [],
                "moments_mag": []
            })
        deselect_line()
        canvas.unbind('<Button-1>')
        print(calc_points)

    elif selected_arc:
        selected_coords = canvas.coords(selected_arc)
        start_arc = int(float(canvas.itemcget(selected_arc, 'start')))
        end_arc = canvas.itemcget(selected_arc, 'extent')
        dialog = customtkinter.CTkInputDialog(text="Please enter the diameter:", title="Input Diameter")
        user_input = dialog.get_input()
        if user_input.isdigit() and user_input != "0":
            # Delete the selected line
            canvas.delete(selected_arc)
            arcs.remove(selected_arc)
            for item in dim_arcs[selected_arc_position]:
                canvas.delete(item)
            dim_arcs.pop(selected_arc_position)

            if int(start_arc) == 270:
                ind = 1
            elif int(start_arc) == 0:
                ind = 2
            elif int(start_arc) == 90:
                ind = 3
            elif int(start_arc) == 180:
                ind = 4
            for point in con_point:
                if (selected_coords[0], selected_coords[1]) == point:
                    move_point = selected_coords[0], selected_coords[1]
                elif (selected_coords[2], selected_coords[3]) == point:
                    move_point = selected_coords[2], selected_coords[3]
                    flag = True

            if ind == 1 or ind == 4:
                dif = (abs(selected_coords[1] - selected_coords[3]) - 2*int(user_input))
                selected_coords[1] +=dif
                dif = (abs(selected_coords[0] - selected_coords[2]) - 2*int(user_input))
                selected_coords[0] += dif/2
                selected_coords[2] -= dif/2
                new_arc = canvas.create_arc(selected_coords, outline='black', width=3, style=ARC, start=start_arc, extent=end_arc)
                arcs.append(new_arc)
            elif ind ==2:
                dif = (abs(selected_coords[0] - selected_coords[2]) - 2*int(user_input))
                selected_coords[0] += dif
                dif = (abs(selected_coords[1] - selected_coords[3]) - 2*int(user_input))
                selected_coords[1] += dif/2
                selected_coords[3] -= dif/2
                new_arc = canvas.create_arc(selected_coords, outline='black', width=3, style=ARC, start=start_arc, extent=end_arc)
                arcs.append(new_arc)
            elif ind == 3:
                dif = (abs(selected_coords[2] - selected_coords[0]) - 2*int(user_input))
                selected_coords[2] -= dif
                dif = (abs(selected_coords[1] - selected_coords[3]) - 2*int(user_input))
                selected_coords[3] -= dif/2
                selected_coords[1] += dif/2
                new_arc = canvas.create_arc(selected_coords, outline='black', width=3, style=ARC, start=start_arc, extent=end_arc)
                arcs.append(new_arc)

            if move_point is not None and flag == False:
                cur_coords = canvas.coords(new_arc)
                delta = move_point[0] - cur_coords[0], move_point[1] - cur_coords[1]
                canvas.move(new_arc, delta[0], delta[1])
                selected_coords = canvas.coords(new_arc)
            elif move_point is not None and flag == True:
                cur_coords = canvas.coords(new_arc)
                delta = move_point[0] - cur_coords[2], move_point[1] - cur_coords[3]
                canvas.move(new_arc, delta[0], delta[1])
                selected_coords = canvas.coords(new_arc)
            draw_dim_arc(selected_coords[0], selected_coords[1], selected_coords[2], selected_coords[3])
        else:
            messagebox.showerror("Error", "Please enter a valid number")
            change_dim_line()
        deselect_line()
        canvas.unbind('<Button-1>')
    canvas.update()

# Pridanie funkcií pre kreslenie ciary
def start_draw_line(event):
    global start_x, start_y, current_line
    if drawing_line_enabled:
        start_x, start_y = event.x, event.y
        threshold = 40  # Definovanie vzdialenosti pre prichytenie

        # kontrola ci je zaciatocny bod blizko konca alebo zaciatku existujucej ciary
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

        for arc in arcs:
            coords = canvas.coords(arc)
            start_c = canvas.itemcget(arc, 'start')
            start_arc_c = int(float(start_c))

            if start_arc_c == 270:
                start_point = ((coords[0] + coords[2]) / 2, coords[3])
                end_point = (coords[2], (coords[3] + coords[1]) / 2)
            elif start_arc_c == 0:
                start_point = (coords[2], (coords[1] + coords[3]) / 2)
                end_point = ((coords[0] + coords[2]) / 2, coords[1])
            elif start_arc_c == 90:
                start_point = (coords[0], (coords[1]+coords[3])/2)
                end_point = ((coords[0]+coords[2])/2, coords[1])
            elif start_arc_c == 180:
                start_point = ((coords[0]+coords[2])/2, coords[3])
                end_point = (coords[0], (coords[1]+coords[3])/2)

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
    global current_line, current_dim_line
    if drawing_line_enabled and current_line:
        if abs(event.x - start_x) > abs(event.y - start_y):
            # Kresli vodorovnú čiaru
            canvas.coords(current_line, start_x, start_y, event.x, start_y)
        else:
            # Kresli zvislú čiaru
            canvas.coords(current_line, start_x, start_y, start_x, event.y)

def stop_draw_line(event):
    global start_x, start_y, current_line, start_xend, start_yend, order
    if drawing_line_enabled and current_line:
        if abs(event.x - start_x) > abs(event.y - start_y):
            # Kresli vodorovnú čiaru
            canvas.coords(current_line, start_x, start_y, event.x, start_y)
            draw_dim_line(start_x, start_y, event.x, start_y)
            start_xend = start_x
            start_yend = start_y + 50
            coords_calc = canvas.coords(current_line)
            combinated_hor.append(coords_calc[0])
            combinated_hor.append(coords_calc[2])
            calc_points["horizontal"].append({
                "coords": coords_calc,
                "supports": [],
                "supports_index": [],
                "forces": [],
                "forces_mag": [],
                "forces_angle": [],
                "linear_forces": [],
                "linear_forces_mag": [],
                "moments": [],
                "moments_mag": []
            })
        else:
            # Kresli zvislú čiaru
            canvas.coords(current_line, start_x, start_y, start_x, event.y)
            draw_dim_line(start_x, start_y, start_x, event.y)
            coords_calc = canvas.coords(current_line)
            combinated_ver.append(coords_calc[1])
            combinated_ver.append(coords_calc[3])
            calc_points["vertical"].append({
                "coords": coords_calc,
                "supports": [],
                "supports_index": [],
                "forces": [],
                "forces_mag": [],
                "forces_angle": [],
                "linear_forces": [],
                "linear_forces_mag": [],
                "moments": [],
                "moments_mag": []
            })
        lines.append(current_line)
        current_line = None
    start_x, start_y = None, None
    order.append("line")

# Pridanie funkcií pre kreslenie oblúka
def start_draw_arc(event):
    global start_x, start_y, current_arc, start_arc, end_arc, ind
    if ind == 1:
        start_arc = -90
        end_arc = 90
    elif ind == 2:
        start_arc = 0
        end_arc = 90
    elif ind == 3:
        start_arc = 90
        end_arc = 90
    elif ind == 4:
        start_arc = 180
        end_arc = 90


    if drawing_arc_enabled:
        start_x, start_y = event.x, event.y
        threshold = 40
        # kontrola ci je zaciatocny bod blizko konca alebo zaciatku existujucej ciary
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

        for arc in arcs:
            coords = canvas.coords(arc)
            start_c = canvas.itemcget(arc, 'start')
            start_arc_c = int(float(start_c))

            if start_arc_c == 270:
                start_point = ((coords[0] + coords[2]) / 2, coords[3])
                end_point = (coords[2], (coords[3] + coords[1]) / 2)
            elif start_arc_c == 0:
                start_point = (coords[2], (coords[1] + coords[3]) / 2)
                end_point = ((coords[0] + coords[2]) / 2, coords[1])
            elif start_arc_c == 90:
                start_point = (coords[0], (coords[1]+coords[3])/2)
                end_point = ((coords[0]+coords[2])/2, coords[1])
            elif start_arc_c == 180:
                start_point = ((coords[0]+coords[2])/2, coords[3])
                end_point = (coords[0], (coords[1]+coords[3])/2)

            if abs(start_x - start_point[0]) < threshold and abs(start_y - start_point[1]) < threshold:
                start_x, start_y = start_point
                con_point.append(start_point)
                break
            elif abs(start_x - end_point[0]) < threshold and abs(start_y - end_point[1]) < threshold:
                start_x, start_y = end_point
                con_point.append(end_point)
                break
        current_arc = canvas.create_arc(start_x, start_y, start_x, start_y, outline='black', width=3, style=ARC, start=start_arc, extent=end_arc)

def draw_arc(event):
    global current_arc, ind, current_dim_arc
    if drawing_arc_enabled and current_arc:
        # Vymazat sucastnu oblukovu kotu
        if current_dim_arc:
            canvas.delete(current_dim_arc[0])
            canvas.delete(current_dim_arc[1])
            current_dim_arc = None

        radius = abs(event.x - start_x)
        side_length = 2 * radius
        if ind == 1 or ind == 4:
            x0 = start_x - radius
            y0 = start_y - radius
            x1 = start_x + radius
            y1 = start_y
            y0 = start_y - side_length
        elif ind == 3:
            x0 = start_x
            y0 = start_y - radius
            x1 = start_x + side_length
            y1 = start_y + radius
        elif ind == 2:
            x0 = start_x - side_length
            y0 = start_y - radius
            x1 = start_x
            y1 = start_y + radius
        canvas.coords(current_arc, x0, y0, x1, y1)
        #current_dim_arc = draw_dim_arc(x0, y0, x1, y1)

def stop_draw_arc(event):
    global start_x, start_y, current_arc, current_dim_arc, order
    if drawing_arc_enabled and current_arc:
        arcs.append(current_arc)
        coords_arc = canvas.coords(current_arc)
        draw_dim_arc(coords_arc[0], coords_arc[1], coords_arc[2], coords_arc[3])
        current_arc = None
    start_x, start_y = None, None
    order.append("arc")

#funkcia na povolenie kreslenia ciary
def enable_line_drawing():
    deselect_line()
    canvas.bind('<Button-1>', start_draw_line)
    canvas.bind('<B1-Motion>', draw_line)
    canvas.bind('<ButtonRelease-1>', stop_draw_line)
    global drawing_line_enabled, drawing_arc_enabled
    drawing_arc_enabled = False
    drawing_line_enabled = True

#funkcia na povolenie kreslenia obluka
def enable_arc_drawing():
    deselect_line()
    canvas.unbind('<Button-1>')
    canvas.unbind('<B1-Motion>')
    canvas.unbind('<ButtonRelease-1>')
    canvas.bind('<Button-1>', start_draw_arc)
    canvas.bind('<B1-Motion>', draw_arc)
    canvas.bind('<ButtonRelease-1>', stop_draw_arc)
    global drawing_arc_enabled, drawing_line_enabled
    drawing_arc_enabled = True
    drawing_line_enabled = False

#funkcie pre definovanie obluka
def arc1():
    global ind
    ind = 1
    enable_arc_drawing()
def arc2():
    global ind
    ind = 2
    enable_arc_drawing()
def arc3():
    global ind
    ind = 3
    enable_arc_drawing()
def arc4():
    global ind
    ind = 4
    enable_arc_drawing()

#funckie vratit spat a dopredu
def undo():
    if order:
        if order[-1] == "line":
            order.pop()
            redo_order.append("line")
            line = lines.pop()
            coords = canvas.coords(line)
            canvas.delete(line)
            redo_lines.append(coords)
            if dim_lines:
                dim = dim_lines.pop()
                for item in dim:
                    canvas.delete(item)
        elif order[-1] == "arc":
            order.pop()
            redo_order.append("arc")
            arc = arcs.pop()
            start_arc = int(float(canvas.itemcget(arc, 'start')))
            coords = canvas.coords(arc)
            canvas.delete(arc)
            redo_lines.append(coords)
            redo_angles.append(start_arc)
            if dim_arcs:
                dim = dim_arcs.pop()
                for item in dim:
                    canvas.delete(item)

def redo():
    global ind
    if redo_order:
        if redo_order[-1] == "line":
            redo_order.pop()
            coords = redo_lines.pop()
            new_line = canvas.create_line(coords, fill='black', width=3)
            lines.append(new_line)
            draw_dim_line(coords[0], coords[1], coords[2], coords[3])
        elif redo_order[-1] == "arc":
            redo_order.pop()
            coords = redo_lines.pop()
            start_arc = redo_angles.pop()
            if int(start_arc) == 270:
                ind = 1
            elif int(start_arc) == 0:
                ind = 2
            elif int(start_arc) == 90:
                ind = 3
            elif int(start_arc) == 180:
                ind = 4
            new_arc = canvas.create_arc(coords, outline='black', width=3, style=ARC, start=start_arc, extent=90)
            arcs.append(new_arc)
            draw_dim_arc(coords[0], coords[1], coords[2], coords[3])

#funkcia na označenie ciary
def select_line(event):
    global selected_line, selected_line_position, selected_arc, place_support_flag, change_dim_flag, place_force_flag, selected_image, \
        selected_arc_position, selected_image_position, delete_flag, place_moment_flag
    item = canvas.find_closest(event.x, event.y)
    if item:
        item_type = canvas.type(item)
        if selected_line:
            canvas.itemconfig(selected_line, fill='black')
        if selected_arc:
            canvas.itemconfig(selected_arc, outline='black')

        if item_type == 'line':
            selected_line = item[0]
            canvas.itemconfig(selected_line, fill='red')
            selected_coords = canvas.coords(selected_line)
            for index, line in enumerate(lines):
                if canvas.coords(line) == selected_coords:
                    selected_line_position = index
                    break
            selected_arc = None
        elif item_type == 'arc':
            selected_arc = item[0]
            canvas.itemconfig(selected_arc, outline='red')
            selected_coords = canvas.coords(selected_arc)
            selected_line = None
            for index, arc in enumerate(arcs):
                if canvas.coords(arc) == selected_coords:
                    selected_arc_position = index
                    break
        elif item_type == 'image':
            if item[0] in sup_obj:
                selected_image = item[0]
            elif item[0] in force_obj:
                selected_image = item[0]
                selected_coords = canvas.coords(selected_image)
                for index, forc in enumerate(force_obj):
                    if canvas.coords(forc) == selected_coords:
                        selected_image_position = index
                        break
        if place_support_flag:
            place_support_flag = False
            delete_flag = False
            place_force_flag = False
            place_moment_flag = False
            change_dim_flag = False
            place_support_window()
        if delete_flag:
            delete_flag = False
            place_support_flag = False
            place_force_flag = False
            place_moment_flag = False
            change_dim_flag = False
            window.bind('<Delete>', lambda event: clear_canvas())
        if place_force_flag:
            place_force_flag = False
            place_support_flag = False
            delete_flag = False
            place_moment_flag = False
            change_dim_flag = False
            place_force_window()
        if place_moment_flag:
            place_moment_flag = False
            place_support_flag = False
            delete_flag = False
            place_force_flag = False
            change_dim_flag = False
            place_moment_window()
        if change_dim_flag:
            change_dim_flag = False
            place_support_flag = False
            delete_flag = False
            place_force_flag = False
            place_moment_flag = False
            change_dim_line()

#funkcia na odznačenie ciary
def deselect_line():
    global selected_line, selected_arc
    window.unbind('<Delete>')
    if selected_line:
        canvas.itemconfig(selected_line, fill='black')
        selected_line = None
    if selected_arc:
        canvas.itemconfig(selected_arc, outline='black')
        selected_arc = None

#bindovanie funkcie na označenie ciary
def bind_select():
    global delete_flag
    delete_flag = True
    canvas.unbind("<ButtonPress-1>")
    canvas.unbind("<B1-Motion>")
    canvas.bind('<Button-1>', select_line)

# Funkcia na vymazanie všetkých objektov na plátne
def clear_canvas():
    global lines, redo_lines, dim_lines, selected_line, arcs, dim_arcs, selected_arc, con_point, sup_obj, force_obj, force_mag, selected_image, selected_arc_position, selected_image_position
    window.unbind('<Delete>')
    if not selected_line and not selected_arc and not selected_image:
        result = messagebox.askyesno("", "Vymazať všetky objekty na plátne?")
        if result:
            # Vymaž všetky objekty na plátne
            canvas.delete("all")
            # Vymaž všetky zoznamy
            selected_line = None
            lines.clear()
            arcs.clear()
            dim_lines.clear()
            dim_arcs.clear()
            redo_lines.clear()
            con_point.clear()
            sup_obj.clear()
            force_obj.clear()
            force_mag.clear()
            selected_image = None
            selected_arc_position = None
            selected_image_position = None
    else:
        if selected_line:
            for index, line in enumerate(lines):
                if selected_line == line:
                    selected_line_position = index
                    break
            for item in dim_lines[selected_line_position]:
                canvas.delete(item)
            canvas.delete(selected_line)
            selected_line = None
        if selected_arc:
            if selected_arc_position is not None:
                if selected_arc_position < len(dim_arcs):
                    for item in dim_arcs[selected_arc_position]:
                        canvas.delete(item)
                    dim_arcs.pop(selected_arc_position)
            arcs.remove(selected_arc)
            canvas.delete(selected_arc)
            selected_arc = None
        if selected_image:
            if selected_image in sup_obj:
                sup_obj.remove(selected_image)
                canvas.delete(selected_image)
                selected_image = None
            elif selected_image in force_obj:


                #if selected_image_position is not None:
                    #for item in force_mag[selected_image_position]:
                    #    canvas.delete(item)
                    #force_mag.pop(selected_image_position)

                
                force_obj.remove(selected_image)
                canvas.delete(selected_image)
                selected_image = None

#funkcie na pohyb po obrazovke
def scroll_left(event):
    canvas.move("all", 40, 0)
    canvas.update()
def scroll_right(event):
    canvas.move("all", -40, 0)
    canvas.update()
def scroll_up(event):
    canvas.move("all", 0, 40)
    canvas.update()
def scroll_down(event):
    canvas.move("all",0,-40)
    canvas.update()

def scroll_bind():
    window.bind("<Left>", scroll_left)
    window.bind("<Right>", scroll_right)
    window.bind("<Up>", scroll_up)
    window.bind("<Down>", scroll_down)
scroll_bind()

def scroll_unbind():
    window.unbind("<Left>")
    window.unbind("<Right>")
    window.unbind("<Up>")
    window.unbind("<Down>")

# Funkcia na vytvorenie podpory
def place_support():
    global place_support_flag, support1, resized_support1_image, support1_1, sup_index, sup_x, sup_y, sup_toplevel, updated_angle, arc_sup_scale,\
        Theta, sup_obj_image, sup_obj_ind, sup_angle
    scroll_bind()
    if selected_line:
        rotated_support1_image = resized_support1_image.rotate(updated_angle)
        support1_1 = ImageTk.PhotoImage(rotated_support1_image)
        sup = canvas.create_image(sup_x,sup_y, image=support1_1)
        if sup_index == 2:
            sup_angle = updated_angle
        canvas.tag_lower(sup)
        sup_obj_image.append(support1_1)
        sup_obj.append(sup)
        sup_obj_c.append(canvas.coords(sup))
        sup_obj_ind.append(sup_index)
        coords_line_sup = canvas.coords(selected_line)
        if coords_line_sup[1] == coords_line_sup[3]:
            combinated_hor.append(canvas.coords(sup)[0])
            for beam in calc_points["horizontal"]:
                if beam["coords"] == coords_line_sup:  # Porovnanie súradníc
                    beam["supports"].append(canvas.coords(sup))
                    beam["supports_index"].append(sup_index)
        else:
            combinated_ver.append(canvas.coords(sup)[1])
            for beam in calc_points["vertical"]:
                if beam["coords"] == coords_line_sup:  # Porovnanie súradníc
                    beam["supports"].append(canvas.coords(sup))
                    beam["supports_index"].append(sup_index)
        print(calc_points)
        sup_toplevel.destroy()

        deselect_line()
    if selected_arc:
        end_x, end_y = canvas.coords(selected_arc)[2], canvas.coords(selected_arc)[3]
        start_x, start_y = canvas.coords(selected_arc)[0], canvas.coords(selected_arc)[1]
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2

        radius = abs(end_x - start_x) / 2
        if ind == 1:
            mid_arc_x = mid_x + radius * math.cos(math.radians(Theta))
            mid_arc_y = mid_y + radius * math.sin(math.radians(Theta))
            sup_x, sup_y = mid_arc_x, mid_arc_y
        elif ind == 2:
            mid_arc_x = mid_x + radius * math.cos(math.radians(Theta))
            mid_arc_y = mid_y - radius * math.sin(math.radians(Theta))
            sup_y, sup_x = mid_arc_x, mid_arc_y
        elif ind == 3:
            mid_arc_x = mid_x - radius * math.cos(math.radians(Theta))
            mid_arc_y = mid_y - radius * math.sin(math.radians(Theta))
            sup_x, sup_y = mid_arc_x, mid_arc_y
        elif ind == 4:
            mid_arc_x = mid_x - radius * math.cos(math.radians(Theta))
            mid_arc_y = mid_y + radius * math.sin(math.radians(Theta))
            sup_x, sup_y = mid_arc_x, mid_arc_y

        rotated_support1_image = resized_support1_image.rotate(updated_angle)
        support1_1 = ImageTk.PhotoImage(rotated_support1_image)
        sup = canvas.create_image(sup_x, sup_y, image=support1_1)
        if sup_index == 2:
            sup_angle = updated_angle
        canvas.tag_lower(sup)
        sup_obj.append(support1_1)
        sup_obj.append(sup)
        sup_toplevel.destroy()
        deselect_line()
    print("combinated", combinated_ver)

#funkcie pre zlovenie podpory
def sup1():
    global support1, resized_support1_image, support1_1, sup_index
    support1_image = Image.open("image/sup1.jpg")
    resized_support1_image = support1_image.resize((45, 45))
    support1_1 = ImageTk.PhotoImage(resized_support1_image)
    sup_index = 1
    place_support_window()

def sup2():
    global support1, resized_support1_image, support1_1, sup_index
    support1_image = Image.open("image/sup2.jpg")
    resized_support1_image = support1_image.resize((45, 45))
    support1_1 = ImageTk.PhotoImage(resized_support1_image)
    sup_index = 2
    place_support_window()

def sup3():
    global support1, resized_support1_image, support1_1, sup_index
    support1_image = Image.open("image/sup3.jpg")
    resized_support1_image = support1_image.resize((45, 45))
    support1_1 = ImageTk.PhotoImage(resized_support1_image)
    sup_index = 3
    place_support_window()

def sup4():
    global support1, resized_support1_image, support1_1, sup_index
    support1_image = Image.open("image/sup4.jpg")
    resized_support1_image = support1_image.resize((45, 45))
    support1_1 = ImageTk.PhotoImage(resized_support1_image)
    sup_index = 4
    place_support_window()

def sup5():
    global support1, resized_support1_image, support1_1, sup_index
    support1_image = Image.open("image/sup5.jpg")
    resized_support1_image = support1_image.resize((45, 45))
    support1_1 = ImageTk.PhotoImage(resized_support1_image)
    sup_index = 5
    place_support_window()

#funkcia na vytvorenie sily
def place_force():
    global place_force_flag, force1, resized_force1_image, force1_1, start_force_x, start_force_y, end_x_adj, end_y_adj, forc_mag, force_counter,\
        orientation, linear_angle_sin, linear_angle_cos, end_mag_y, start_mag_y, updated_angle,a,b,sum_force_y,linear_mag_y,sum_force_x,linear_mag_x
    scroll_bind()
    if selected_line:
        coords_line_force = canvas.coords(selected_line)
        if force_index == 1:
            force = canvas.create_line(start_force_x, start_force_y, end_x_adj, end_y_adj, width=7, arrow=LAST,arrowshape=(20, 30, 10))
            if orientation == "vertical":
                if end_x_adj < start_force_x:
                    text_x = end_x_adj - 20
                else:
                    text_x = start_force_x - 20
                force_text = canvas.create_text(text_x, start_force_y, text=f"F{force_counter}={forc_mag}N", font=('Arial', 15), fill='darkred', angle=90)
                force_angle.append(int(updated_angle) + 90)
                combinated_ver.append(canvas.coords(force)[1])
                for beam in calc_points["vertical"]:
                    if beam["coords"] == coords_line_force:  # Porovnanie súradníc
                        beam["forces"].append([canvas.coords(force)[0], canvas.coords(force)[1]])
                        beam["forces_mag"].append(forc_mag)
                        beam["forces_angle"].append(int(updated_angle) + 90)

            elif orientation == "horizontal":
                if end_y_adj < start_force_y:
                    text_y = end_y_adj - 20
                else:
                    text_y = start_force_y - 20
                force_text = canvas.create_text(start_force_x, text_y, text=f"F{force_counter}={forc_mag}N",font=('Arial', 15), fill='darkred', angle=0)
                force_angle.append(int(updated_angle))
                combinated_hor.append(canvas.coords(force)[0])
                for beam in calc_points["horizontal"]:
                    if beam["coords"] == coords_line_force:  # Porovnanie súradníc
                        beam["forces"].append([canvas.coords(force)[0], canvas.coords(force)[1]])
                        beam["forces_mag"].append(forc_mag)
                        beam["forces_angle"].append(int(updated_angle))
            print(calc_points)
            force_obj.append(force)
            force_c.append(canvas.coords(force))
            force_mag.append(forc_mag)
            force_toplevel.destroy()
            deselect_line()
            print("combinated", combinated_ver)
        elif force_index == 2:

            if orientation == "horizontal":
                start_linear_x = val_start + sel_coords[0]
                start_linear_y = sel_coords[1] - (60 * linear_angle_cos) * start_mag_y + (60 * linear_angle_sin) * start_mag_y
                end_linear_x = sel_coords[2] - val_end
                end_linear_y = sel_coords[3] - (60 * linear_angle_cos) * end_mag_y + (60 * linear_angle_sin) * end_mag_y
                canvas.create_line(start_linear_x, start_linear_y, start_linear_x, sel_coords[1], width=5, arrow=LAST, arrowshape=(10, 7, 4))
                canvas.create_line(end_linear_x, end_linear_y, end_linear_x, sel_coords[3], width=5, arrow=LAST, arrowshape=(10, 7, 4))
                canvas.create_line(start_linear_x, start_linear_y, end_linear_x, end_linear_y, width=4, arrowshape=(10, 7, 4))

                a = (end_linear_y - start_linear_y) / (end_linear_x - start_linear_x)
                b = start_linear_y - a * start_linear_x

                linear_x = start_linear_x + 30

                linear_force_texts = canvas.create_text(start_linear_x,start_linear_y - (20 * linear_angle_cos) + (20 * linear_angle_sin),
                                                              text=f"{mag_start_text}N/mm", font=('Arial', 15),fill='darkred')
                if mag_start_text != mag_end_text:
                    linear_force_texte = canvas.create_text(end_linear_x,end_linear_y - (20 * linear_angle_cos) + (20 * linear_angle_sin),
                                                                  text=f"{mag_end_text}N/mm", font=('Arial', 15),fill='darkred')
                while linear_x < end_linear_x:
                    linear_y = a * linear_x + b
                    linear_forc = canvas.create_line(linear_x, linear_y, linear_x, sel_coords[1], width=5, arrow=LAST,arrowshape=(10, 7, 4))
                    canvas.tag_lower(linear_forc)
                    linear_force.append(linear_forc)
                    linear_x += 30

                sign_y = -1 if end_linear_y > sel_coords[
                    1] else 1  # štandardne by to malo byť -1 keď ide smerom dole (kladné zaťaženie)

                start_mag_signed = sign_y * int(mag_start_text)

                linear_mag_y.append(float(start_mag_signed) * abs(start_linear_x - end_linear_x))
                sum_force_y += linear_mag_y[-1]
                ay_lin.append(abs(start_linear_x - end_linear_x) / 2 + start_linear_x)

                force_linear.append((start_linear_x, start_linear_y, end_linear_x, end_linear_y))
                combinated_hor.append(start_linear_x)
                combinated_hor.append(end_linear_x)
                force_linear_mag.append((mag_start_text, mag_end_text))
                for beam in calc_points["horizontal"]:
                    if beam["coords"] == coords_line_force:  # Porovnanie súradníc
                        sign_y = -1 if end_linear_y > sel_coords[1] else 1  # štandardne by to malo byť -1 keď ide smerom dole (kladné zaťaženie)

                        start_mag_signed = sign_y * int(mag_start_text)
                        end_mag_signed = sign_y * int(mag_end_text)
                        beam["linear_forces"].append([start_linear_x,end_linear_x,end_linear_y])
                        beam["linear_forces_mag"].append([start_mag_signed, end_mag_signed])
                        print(calc_points)

                force_toplevel.destroy()
                deselect_line()

            if orientation == "vertical":
                if sel_coords[1] < sel_coords[3]:  # prút ide zhora nadol
                    start_linear_x = sel_coords[0] - (60 * linear_angle_sin) * start_mag_y + (
                                60 * linear_angle_cos) * start_mag_y
                    start_linear_y = sel_coords[1] + val_start

                    end_linear_x = sel_coords[2] - (60 * linear_angle_sin) * end_mag_y + (
                                60 * linear_angle_cos) * end_mag_y
                    end_linear_y = sel_coords[3] - val_end
                else:  # prút ide zdola nahor
                    start_linear_x = sel_coords[0] - (60 * linear_angle_sin) * start_mag_y + (
                                60 * linear_angle_cos) * start_mag_y
                    start_linear_y = sel_coords[1] - val_start

                    end_linear_x = sel_coords[2] - (60 * linear_angle_sin) * end_mag_y + (
                                60 * linear_angle_cos) * end_mag_y
                    end_linear_y = sel_coords[3] + val_end

                canvas.create_line(start_linear_x, start_linear_y, sel_coords[0], start_linear_y, width=5,arrow=LAST, arrowshape=(10, 7, 4))
                canvas.create_line(end_linear_x, end_linear_y, sel_coords[2], end_linear_y, width=5, arrow=LAST,arrowshape=(10, 7, 4))

                canvas.create_line(start_linear_x, start_linear_y, end_linear_x, end_linear_y, width=4,arrowshape=(10, 7, 4))

                a = (end_linear_x - start_linear_x) / (end_linear_y - start_linear_y)
                b = start_linear_x - a * start_linear_y

                linear_y = start_linear_y + 30

                linear_force_texts = canvas.create_text(start_linear_x - (20 * linear_angle_sin) + (20 * linear_angle_cos), start_linear_y - 20,
                    text=f"{mag_start_text}N/mm", font=('Arial', 15), fill='darkred')

                if mag_start_text != mag_end_text:
                    linear_force_texte = canvas.create_text(end_linear_x - (20 * linear_angle_sin) + (20 * linear_angle_cos), end_linear_y + 20,
                            text=f"{mag_end_text}N/mm", font=('Arial', 15), fill='darkred')

                while linear_y < end_linear_y:
                    linear_x = a * linear_y + b
                    linear_forc = canvas.create_line(linear_x, linear_y, sel_coords[0], linear_y, width=5, arrow=LAST,arrowshape=(10, 7, 4))
                    canvas.tag_lower(linear_forc)
                    linear_y += 30

                sign_x = 1 if end_linear_x > sel_coords[0] else -1
                start_mag_signed = sign_x * int(mag_start_text)
                end_mag_signed = sign_x * int(mag_end_text)

                # Výpočet veľkosti sily pre statickú rovnováhu
                linear_mag_x.append(abs(start_linear_y - end_linear_y) * start_mag_signed)
                sum_force_x -= linear_mag_x[-1]
                ax_lin.append(abs(start_linear_y - end_linear_y) / 2 + start_linear_y)

                # Zápis do dátovej štruktúry
                force_linear.append((start_linear_x, start_linear_y, end_linear_x, end_linear_y))
                combinated_ver.append(start_linear_y)
                combinated_ver.append(end_linear_y)
                force_linear_mag.append((start_mag_signed, end_mag_signed))

                for beam in calc_points["vertical"]:
                    if beam["coords"] == coords_line_force:
                        sign_x = 1 if end_linear_x > sel_coords[0] else -1
                        start_mag_signed = sign_x * int(mag_start_text)
                        end_mag_signed = sign_x * int(mag_end_text)

                        beam["linear_forces"].append([start_linear_y, end_linear_y, end_linear_x])
                        beam["linear_forces_mag"].append([start_mag_signed, end_mag_signed])
                        print("ssssssssssssssssssssssss",beam["linear_forces_mag"])

                force_toplevel.destroy()
                deselect_line()
            print("combinated", combinated_ver)

    if selected_arc:
        start_x = canvas.coords(selected_arc)[0]
        start_y = canvas.coords(selected_arc)[1]
        end_x = canvas.coords(selected_arc)[2]
        end_y = canvas.coords(selected_arc)[3]
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        dim = abs(end_x - start_x) / 2
        if ind == 1:
            mid_arc_x = mid_x + dim * math.cos(math.radians(Theta))
            mid_arc_y = mid_y + dim * math.sin(math.radians(Theta))
            forc_x, forc_y = mid_arc_x, mid_arc_y
        elif ind == 2:
            mid_arc_x = mid_x + dim * math.cos(math.radians(Theta))
            mid_arc_y = mid_y - dim * math.sin(math.radians(Theta))
            forc_x, forc_y = mid_arc_x, mid_arc_y
        elif ind == 3:
            mid_arc_x = mid_x - dim * math.cos(math.radians(Theta))
            mid_arc_y = mid_y - dim * math.sin(math.radians(Theta))
            forc_x, forc_y = mid_arc_x, mid_arc_y
        elif ind == 4:
            mid_arc_x = mid_x - dim * math.cos(math.radians(Theta))
            mid_arc_y = mid_y + dim * math.sin(math.radians(Theta))
            forc_x, forc_y = mid_arc_x, mid_arc_y
        start_x_adj, start_y_adj = mid_arc_x + math.sin(math.radians(updated_angle)) * 50, mid_arc_y + math.cos(math.radians(updated_angle)) * 50
        force = canvas.create_line(start_x_adj,start_y_adj,mid_arc_x,mid_arc_y, width=7, arrow=LAST,arrowshape=(20, 30, 10))
        if start_y_adj < mid_arc_y:
            text_y = start_y_adj - 20
        else:
            text_y = mid_arc_y - 20
        force_text = canvas.create_text(start_x_adj, text_y, text=f"F{force_counter}={forc_mag}N",font=('Arial', 15), fill='darkred')
        force_obj.append(force)
        force_mag.append((forc_mag, force_text))
        force_toplevel.destroy()
        deselect_line()

#funkcia na zvolenie sily
def force1():
    global force_index
    force_index = 1
    place_force_window()

def force2():
    global force_index
    force_index = 2
    place_force_window()

def place_support_window():
    global place_support_flag, selected_line, selected_arc, sel_coords, support1_1, sup_toplevel, sup_index, updated_angle, arc_sup_scale, ind
    scroll_unbind()
    def update_label(val):
        global sel_coords, sup_x, sup_y, updated_angle
        value.delete(0, END)
        value.insert(0, int(float(val)))
        if sup_index != 4:
            updated_angle = int(entry_angle.get())


        rotated_support1_image = resized_support1_image.rotate(updated_angle)
        support1_1 = ImageTk.PhotoImage(rotated_support1_image)
        support_canvas.support1_1 = support1_1
        val = int(float(val))/line_sup_scale
        if orientation == "horizontal":
            sup_window = support_canvas.create_image(val + start_x, start_y, image=support1_1)
            if sel_coords[0] < sel_coords[2]:
                sup_x = val*line_sup_scale + sel_coords[0]
                sup_y = sel_coords[1]
            else:
                sup_x = val*line_sup_scale + sel_coords[2]
                sup_y = sel_coords[1]
        if orientation == "vertical":
            sup_window = support_canvas.create_image(start_x, start_y + val, image=support1_1)
            if sel_coords[1] < sel_coords[3]:
                sup_x = sel_coords[0]
                sup_y = sel_coords[1] + val*line_sup_scale
            else:
                sup_x = sel_coords[0]
                sup_y = sel_coords[3] + val*line_sup_scale
        support_canvas.tag_lower(sup_window)

    def update_label_arc(val):
        global sel_coords, sup_x, sup_y, updated_angle, dim, Theta
        value.delete(0, END)
        value.insert(0, int(float(val)))
        if sup_index != 4:
            updated_angle = int(entry_angle.get())
        rotated_support1_image = resized_support1_image.rotate(updated_angle)
        support1_1 = ImageTk.PhotoImage(rotated_support1_image)
        support_canvas.support1_1 = support1_1
        start_arc = int(float(canvas.itemcget(selected_arc, 'start')))
        if int(start_arc) == 270:
            ind = 1
        elif int(start_arc) == 0:
            ind = 2
        elif int(start_arc) == 90:
            ind = 3
        elif int(start_arc) == 180:
            ind = 4


        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2

        radius = abs(end_x - start_x) / 2
        Theta = int(float(val))
        if ind == 1:
            mid_arc_x = mid_x + radius * math.cos(math.radians(Theta))
            mid_arc_y = mid_y + radius * math.sin(math.radians(Theta))
            sup_x, sup_y = mid_arc_x, mid_arc_y
        elif ind == 2:
            mid_arc_x = mid_x + radius * math.cos(math.radians(Theta))
            mid_arc_y = mid_y - radius * math.sin(math.radians(Theta))
            sup_x, sup_y = mid_arc_x, mid_arc_y
        elif ind == 3:
            mid_arc_x = mid_x - radius * math.cos(math.radians(Theta))
            mid_arc_y = mid_y - radius * math.sin(math.radians(Theta))
            sup_x, sup_y = mid_arc_x, mid_arc_y
        elif ind == 4:
            mid_arc_x = mid_x - radius * math.cos(math.radians(Theta))
            mid_arc_y = mid_y + radius * math.sin(math.radians(Theta))
            sup_x, sup_y = mid_arc_x, mid_arc_y
        sup_window = support_canvas.create_image(sup_x, sup_y, image=support1_1)
        support_canvas.tag_lower(sup_window)

    def fix_sup_zero():
        global sup_x, sup_y, updated_angle, ind, Theta
        Theta = 90
        if selected_line:
            updated_angle = 0
            rotated_support1_image = resized_support1_image
            support1_1 = ImageTk.PhotoImage(rotated_support1_image)
            support_canvas.support1_1 = support1_1
            sup_window = support_canvas.create_image(start_x, start_y, image=support1_1)
            support_canvas.tag_lower(sup_window)
            if sel_coords[0] < sel_coords[2]:
                sup_x, sup_y = sel_coords[0], sel_coords[1]
            else:
                sup_x, sup_y = sel_coords[2], sel_coords[3]


        else:
            if ind == 1:
                updated_angle = 0
                rotated_support1_image = resized_support1_image
                support1_1 = ImageTk.PhotoImage(rotated_support1_image)
                support_canvas.support1_1 = support1_1
                sup_window = support_canvas.create_image((start_x+end_x)/2, end_y, image=support1_1)
                support_canvas.tag_lower(sup_window)

            if ind == 2:
                updated_angle = 90
                rotated_support1_image = resized_support1_image.rotate(90)
                support1_1 = ImageTk.PhotoImage(rotated_support1_image)
                support_canvas.support1_1 = support1_1
                sup_window = support_canvas.create_image(end_x, (start_y+end_y)/2, image=support1_1)
                support_canvas.tag_lower(sup_window)

            if ind == 3:
                updated_angle = 90
                rotated_support1_image = resized_support1_image.rotate(90)
                support1_1 = ImageTk.PhotoImage(rotated_support1_image)
                support_canvas.support1_1 = support1_1
                sup_window = support_canvas.create_image(start_x, (start_y+end_y)/2, image=support1_1)
                support_canvas.tag_lower(sup_window)

            if ind == 4:
                updated_angle = 180
                rotated_support1_image = resized_support1_image.rotate(180)
                support1_1 = ImageTk.PhotoImage(rotated_support1_image)
                support_canvas.support1_1 = support1_1
                sup_window = support_canvas.create_image((start_x + end_x) / 2, end_y, image=support1_1)
                support_canvas.tag_lower(sup_window)


    def fix_sup_end():
        global sup_x, sup_y, updated_angle, Theta
        Theta = 0
        if selected_line:
            updated_angle = 180
            rotated_support1_image = resized_support1_image.rotate(180)
            support1_1 = ImageTk.PhotoImage(rotated_support1_image)
            support_canvas.support1_1 = support1_1
            sup_window = support_canvas.create_image(end_x, end_y, image=support1_1)
            support_canvas.tag_lower(sup_window)
            if sel_coords[0] < sel_coords[2]:
                sup_x, sup_y = sel_coords[2], sel_coords[3]
            else:
                sup_x, sup_y = sel_coords[0], sel_coords[1]

        else:
            if ind == 1:
                updated_angle = -90
                rotated_support1_image = resized_support1_image.rotate(-90)
                support1_1 = ImageTk.PhotoImage(rotated_support1_image)
                support_canvas.support1_1 = support1_1
                sup_window = support_canvas.create_image(end_x, (end_y+start_y)/2, image=support1_1)
                support_canvas.tag_lower(sup_window)

            if ind == 2:
                updated_angle = 0
                rotated_support1_image = resized_support1_image
                support1_1 = ImageTk.PhotoImage(rotated_support1_image)
                support_canvas.support1_1 = support1_1
                sup_window = support_canvas.create_image((end_x+start_x)/2, start_y, image=support1_1)
                support_canvas.tag_lower(sup_window)

            if ind == 3:
                updated_angle = 180
                rotated_support1_image = resized_support1_image.rotate(180)
                support1_1 = ImageTk.PhotoImage(rotated_support1_image)
                support_canvas.support1_1 = support1_1
                sup_window = support_canvas.create_image((end_x+start_x)/2, start_y, image=support1_1)
                support_canvas.tag_lower(sup_window)

            if ind == 4:
                updated_angle = -90
                rotated_support1_image = resized_support1_image.rotate(-90)
                support1_1 = ImageTk.PhotoImage(rotated_support1_image)
                support_canvas.support1_1 = support1_1
                sup_window = support_canvas.create_image(start_x, (end_y+start_y)/2, image=support1_1)
                support_canvas.tag_lower(sup_window)

    def update(event):
        updated_value = int(value.get())
        scale.set(updated_value)

    if not selected_line and not selected_arc:
        place_support_flag = True
        canvas.bind('<Button-1>', select_line)
    if selected_line:
        sel_coords = canvas.coords(selected_line)
        dim_coords_x = abs(sel_coords[0] - sel_coords[2])
        dim_coords_y = abs(sel_coords[1] - sel_coords[3])

        sup_toplevel = CTkToplevel(window)
        sup_toplevel.title("")
        sup_toplevel.geometry("400x400")
        sup_toplevel.attributes("-topmost", True)
        sup_toplevel.resizable("False", "False")
        style = ttk.Style()
        style.configure("TScale", background="black", troughcolor="blue")
        style.configure("TLabel", background="black", troughcolor="blue", foreground="lightblue")

        support_canvas = Canvas(sup_toplevel, width=475, height=300, bg='white')
        support_canvas.grid(row=0, column=0, padx=10, pady=10, sticky=E + W + N)

        if dim_coords_x > 2000 or dim_coords_y > 1000:
            line_sup_scale = 8
            dim_coords_x /= 8
            dim_coords_y /= 8
        elif dim_coords_x > 1500 or dim_coords_y > 1000:
            line_sup_scale = 6
            dim_coords_x /= 6
            dim_coords_y /= 6
        elif dim_coords_x > 1000 or dim_coords_y > 750:
            line_sup_scale = 4
            dim_coords_x /= 4
            dim_coords_y /= 4
        elif dim_coords_x > 600 or dim_coords_y > 500:
            line_sup_scale = 3
            dim_coords_x /= 3
            dim_coords_y /= 3
        elif dim_coords_x > 250 or dim_coords_y > 250:
            line_sup_scale = 2
            dim_coords_x /= 2
            dim_coords_y /= 2
        else:
            line_sup_scale = 1

        center_x = 237.5
        center_y = 150

        if sel_coords[1] == sel_coords[3]:
            start_x = center_x - dim_coords_x / 2
            start_y = center_y
            end_x = center_x + dim_coords_x / 2
            end_y = center_y
            support_canvas.create_line(start_x,start_y,end_x,end_y, fill='black',width=3)
            orientation = "horizontal"
        if sel_coords[0] == sel_coords[2]:
            start_x = center_x
            start_y = center_y - dim_coords_y / 2
            end_x = center_x
            end_y = center_y + dim_coords_y / 2
            support_canvas.create_line(start_x,start_y,end_x,end_y, fill='black',width=3)
            orientation = "vertical"

        if sup_index != 3:
            value = Entry(sup_toplevel, text="0", font=('Arial', 15,), justify=CENTER, width=6)
            value.grid(row=1, column=0)
            value.insert(0, "0")
            scale = ttk.Scale(sup_toplevel, from_=0, to=(dim_coords_x+dim_coords_y)*line_sup_scale, orient=HORIZONTAL, command=update_label, length=450)
            scale.grid(row=2, column=0, padx = 10, pady = 10)
            if sup_index == 4 and orientation == "vertical":
                updated_angle = 90
            elif sup_index != 4:
                Angle_label = ttk.Label(sup_toplevel, text="Natočenie podpory:", font=('Arial', 15,))
                Angle_label.grid(row=3, column=0, padx=10, pady=0, sticky=W + S)
                entry_angle = ttk.Entry(sup_toplevel, width=30)
                entry_angle.grid(row=4, column=0, padx = 10, pady = 10, ipady = 5, sticky = W)
                entry_angle.insert(0, "0")
                entry_angle.bind("<Return>", update)
            value.delete(0, END)
            value.insert(0, "0")
            value.bind("<Return>", update)
            update("")
        elif sup_index == 3:
            start_button = customtkinter.CTkButton(sup_toplevel, text="0", height=40, command=fix_sup_zero)
            start_button.grid(row=1, column=0, padx=10, pady=10, sticky=W + S)
            end_button = customtkinter.CTkButton(sup_toplevel, text="END", height=40, command=fix_sup_end)
            end_button.grid(row=1, column=0, padx=10, pady=10, sticky=E + S)
        support_button = customtkinter.CTkButton(sup_toplevel, text="Vytvor podporu", height=40, command=place_support)
        support_button.grid(row=4, column=0, padx=10, pady=10, sticky=E + S)
        sup_toplevel.bind("<Destroy>", lambda event: deselect_line())

    if selected_arc:
        sup_toplevel = CTkToplevel(window)
        sup_toplevel.title("")
        sup_toplevel.geometry("400x400")
        sup_toplevel.attributes("-topmost", True)
        sup_toplevel.resizable("False", "False")
        style = ttk.Style()
        style.configure("TScale", background="black", troughcolor="blue")
        style.configure("TLabel", background="black", troughcolor="blue", foreground="lightblue")

        support_canvas = Canvas(sup_toplevel, width=475, height=300, bg='white')
        support_canvas.grid(row=0, column=0, padx=10, pady=10, sticky=E + W + N)

        start_x = canvas.coords(selected_arc)[0]
        start_y = canvas.coords(selected_arc)[1]
        end_x = canvas.coords(selected_arc)[2]
        end_y = canvas.coords(selected_arc)[3]

        center_x = 237.5
        center_y = 150
        dim = abs(end_x - start_x)

        if dim > 2000:
            arc_sup_scale = 15
            dim /= 15
        elif dim > 1500:
            arc_sup_scale = 10
            dim /= 10
        elif dim > 300:
            arc_sup_scale = 3
            dim /= 3
        elif dim > 250:
            arc_sup_scale = 2
            dim /= 2
        elif dim > 200:
            arc_sup_scale = 1.5
            dim /= 1.5
        else:
            arc_sup_scale = 1

        start_x = center_x - dim / 2
        start_y = center_y - dim / 2
        end_x = center_x + dim / 2
        end_y = center_y + dim / 2
        start_arc = int(float(canvas.itemcget(selected_arc, 'start')))

        if int(start_arc) == 270:
            ind = 1
        elif int(start_arc) == 0:
            ind = 2
        elif int(start_arc) == 90:
            ind = 3
        elif int(start_arc) == 180:
            ind = 4

        support_canvas.create_arc(start_x, start_y, end_x, end_y, outline='black', width=3, style=ARC, start=start_arc, extent=90)

        if sup_index != 3 and sup_index != 4:
            value = Entry(sup_toplevel, text="0", font=('Arial', 15,), justify=CENTER, width=6)
            value.grid(row=1, column=0)
            value.insert(0, "0")
            scale = ttk.Scale(sup_toplevel, from_=0, to=90,orient=HORIZONTAL, length=450, command=update_label_arc)
            scale.grid(row=2, column=0, padx=10, pady=10)
            Angle_label = ttk.Label(sup_toplevel, text="Natočenie podpory:", font=('Arial', 15,))
            Angle_label.grid(row=3, column=0, padx=10, pady=0, sticky=W + S)
            entry_angle = ttk.Entry(sup_toplevel, width=30)
            entry_angle.grid(row=4, column=0, padx=10, pady=10, ipady=5, sticky=W)
            entry_angle.insert(0, "0")
            value.delete(0, END)
            value.insert(0, "0")
            value.bind("<Return>", update)
            entry_angle.bind("<Return>", update)
            update("")
        elif sup_index == 3 or sup_index == 4:
            start_button = customtkinter.CTkButton(sup_toplevel, text="0", height=40, command=fix_sup_zero)
            start_button.grid(row=1, column=0, padx=10, pady=10, sticky=W + S)
            end_button = customtkinter.CTkButton(sup_toplevel, text="END", height=40, command=fix_sup_end)
            end_button.grid(row=1, column=0, padx=10, pady=10, sticky=E + S)
        support_button = customtkinter.CTkButton(sup_toplevel, text="Vytvor podporu", height=40, command=place_support)
        support_button.grid(row=4, column=0, padx=10, pady=10, sticky=E + S)
        sup_toplevel.bind("<Destroy>", lambda event: deselect_line())

def place_force_window():
    global place_force_flag, sel_coords, force_window, force_toplevel, force_text, force_counter, \
        orientation, val_start, val_end, linear_force, val_start_adj, val_end_adj, linear_angle, mag_start_text, mag_end_text
    scroll_unbind()
    if not selected_line and not selected_arc:
        place_force_flag = True
        canvas.bind('<Button-1>', select_line)
    force_window = None
    force_text = None

    def update_label(val):
        global sel_coords, sup_x, sup_y, updated_angle, force_window, force_text, force_counter, start_force_x, start_force_y, end_x_adj, end_y_adj, forc_mag
        value.delete(0, END)
        value.insert(0, int(float(val)))
        updated_angle = int(entry_angle.get())
        val = int(float(val))/line_force_scale
        forc_mag = int(float(entry_mag.get()))
        if force_window:
            force_canvas.delete(force_window)
        if force_text:
            force_canvas.delete(force_text)
        if orientation == "horizontal":
            start_x_adj, start_y_adj = val + start_x + math.sin(math.radians(updated_angle))*50, start_y+math.cos(math.radians(updated_angle))*50
            force_window = force_canvas.create_line(val + start_x, start_y,start_x_adj,start_y_adj, width=7, arrow=LAST, arrowshape=(20, 30, 10))

            if start_y_adj < start_y:
                text_y = start_y_adj - 20
            else:
                text_y = start_y - 20
            force_text = force_canvas.create_text(val + start_x, text_y, text=f"F{force_counter}={entry_mag.get()}N", font=('Arial', 15), fill='darkred')

            if sel_coords[0] < sel_coords[2]:
                start_force_x = val*line_force_scale + sel_coords[0]
                start_force_y = sel_coords[1]
                end_x_adj, end_y_adj = start_force_x + math.sin(math.radians(updated_angle)) * 50, start_force_y + math.cos(math.radians(updated_angle)) * 50
            else:
                start_force_x = val*line_force_scale + sel_coords[2]
                start_force_y = sel_coords[1]
                end_x_adj, end_y_adj = start_force_x + math.sin(math.radians(updated_angle)) * 50, start_force_y + math.cos(math.radians(updated_angle)) * 50

        elif orientation == "vertical":
            start_x_adj, start_y_adj =start_x + math.cos(math.radians(updated_angle)) * 50, val + start_y - math.sin(math.radians(updated_angle)) * 50
            force_window = force_canvas.create_line(start_x, start_y + val, start_x_adj, start_y_adj, width=10, arrow=LAST, arrowshape=(20, 30, 10))

            if start_x_adj < start_x:
                text_x = start_x + 20
            else:
                text_x = start_x_adj + 20
            force_text = force_canvas.create_text(text_x, val + start_y , text=f"F{force_counter}={entry_mag.get()}N", font=('Arial', 15), fill='darkred', angle=90)

            if sel_coords[1] < sel_coords[3]:
                start_force_x = sel_coords[0]
                start_force_y = sel_coords[1] + val*line_force_scale
                end_x_adj, end_y_adj = start_force_x + math.cos(math.radians(updated_angle)) * 50, start_force_y - math.sin(math.radians(updated_angle)) * 50
            else:
                start_force_x = sel_coords[0]
                start_force_y = sel_coords[3] + val*line_force_scale
                end_x_adj, end_y_adj = start_force_x + math.cos(math.radians(updated_angle)) * 50, start_force_y - math.sin(math.radians(updated_angle)) * 50

        force_canvas.tag_lower(force_window)

    def update_label_arc(val):
        global sel_coords, sup_x, sup_y, updated_angle, dim, Theta, force_window, force_text, forc_mag
        value.delete(0, END)
        value.insert(0, int(float(val)))
        forc_mag = int(float(entry_mag.get()))

        if force_window:
            force_canvas.delete(force_window)
        if force_text:
            force_canvas.delete(force_text)

        start_arc = int(float(canvas.itemcget(selected_arc, 'start')))
        if int(start_arc) == 270:
            ind = 1
        elif int(start_arc) == 0:
            ind = 2
        elif int(start_arc) == 90:
            ind = 3
        elif int(start_arc) == 180:
            ind = 4
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        radius = abs(end_x - start_x) / 2
        Theta = int(float(val))
        updated_angle = int(entry_angle.get())
        if ind == 1:
            mid_arc_x = mid_x + radius * math.cos(math.radians(Theta))
            mid_arc_y = mid_y + radius * math.sin(math.radians(Theta))
        elif ind == 2:
            mid_arc_x = mid_x + radius * math.cos(math.radians(Theta))
            mid_arc_y = mid_y - radius * math.sin(math.radians(Theta))
        elif ind == 3:
            mid_arc_x = mid_x - radius * math.cos(math.radians(Theta))
            mid_arc_y = mid_y - radius * math.sin(math.radians(Theta))
        elif ind == 4:
            mid_arc_x = mid_x - radius * math.cos(math.radians(Theta))
            mid_arc_y = mid_y + radius * math.sin(math.radians(Theta))

        start_x_adj, start_y_adj = mid_arc_x + math.sin(math.radians(updated_angle)) * 50, mid_arc_y + math.cos(math.radians(updated_angle)) * 50
        force_window = force_canvas.create_line(start_x_adj, start_y_adj, mid_arc_x, mid_arc_y, width=7, arrow=LAST,arrowshape=(20, 30, 10))
        if start_y_adj < mid_arc_y:
            text_y = start_y_adj - 20
        else:
            text_y = mid_arc_y - 20
        force_text = force_canvas.create_text(start_x_adj, text_y, text=f"F{force_counter}={entry_mag.get()}N",font=('Arial', 15), fill='darkred')

    def update(event):
        updated_value = int(value.get())
        scale.set(updated_value)

    def turn_linear():
        global linear_angle
        if linear_angle == 0:
            linear_angle = 90
        else:
            linear_angle = 0
        scale_start.set(val_start)

    def draw_lin_force():
        global val_start, val_end, linear_force, start_x_adj, start_y_adj, val_start_adj, val_end_adj, linear_angle, mag_start_text, mag_end_text, \
            linear_angle_cos, linear_angle_sin, start_mag_y, end_mag_y
        mag_start_val = float(mag_start_text)
        mag_end_val = float(mag_end_text)

        if mag_start_val == 0:
            start_mag_y = 0
        else:
            start_mag_y = 1
        if mag_end_val == 0:
            end_mag_y = 0
        else:
            end_mag_y = 1

        if abs(mag_start_val - mag_end_val) > 1000:
            mag_y_ind = 0.1
        elif abs(mag_start_val - mag_end_val) > 500:
            mag_y_ind = 0.3
        elif abs(mag_start_val - mag_end_val) > 100:
            mag_y_ind = 0.4
        else:
            mag_y_ind = 0.5

        if mag_start_val > mag_end_val and mag_end_val != 0:
            end_mag_y = mag_y_ind
        elif mag_end_val > mag_start_val and mag_start_val != 0:
            start_mag_y = mag_y_ind

        gap = 30
        linear_angle_cos = math.cos(math.radians(linear_angle))
        linear_angle_sin = math.sin(math.radians(linear_angle))
        if orientation == "horizontal":
            linear_x = start_x + val_start_adj + gap
            x1_hor = start_x + val_start_adj
            x2_hor = end_x - val_end_adj
            y1_hor = start_y - (50 * linear_angle_cos) * start_mag_y + (50 * linear_angle_sin) * start_mag_y
            y2_hor = start_y - (50 * linear_angle_cos) * end_mag_y + (50 * linear_angle_sin) * end_mag_y
            linear_force_start = force_canvas.create_line(start_x + val_start_adj,start_y - (50 * linear_angle_cos) * start_mag_y + (50 * linear_angle_sin) * start_mag_y,
                                                          start_x + val_start_adj, start_y, width=7, arrow=LAST,arrowshape=(10, 7, 4))
            linear_force_end = force_canvas.create_line(end_x - val_end_adj,start_y - (50 * linear_angle_cos) * end_mag_y + (50 * linear_angle_sin) * end_mag_y,
                                                        end_x - val_end_adj, start_y, width=7, arrow=LAST,arrowshape=(10, 7, 4))
            linear_force_line = force_canvas.create_line(x1_hor, y1_hor, x2_hor, y2_hor, width=5)

            a = (y2_hor - y1_hor) / (x2_hor - x1_hor)
            b = y1_hor - a * x1_hor

            linear_force_texts = force_canvas.create_text(start_x + val_start_adj,start_y - (70 * linear_angle_cos) + (70 * linear_angle_sin),
                                                          text=f"{mag_start_text}N/mm", font=('Arial', 15),fill='darkred')
            if mag_start_text != mag_end_text:
                linear_force_texte = force_canvas.create_text(end_x - val_end_adj, start_y - (70 * linear_angle_cos) + (70 * linear_angle_sin),
                                                              text=f"{mag_end_text}N/mm", font=('Arial', 15),fill='darkred')
                linear_force.append(linear_force_texte)

            while linear_x < end_x - val_end_adj:
                linear_y = a * linear_x + b
                linear_force.append(force_canvas.create_line(linear_x, linear_y, linear_x, start_y, width=7, arrow=LAST,arrowshape=(10, 7, 4)))
                linear_x += gap

        elif orientation == "vertical":
            linear_y = start_y + val_start_adj + gap
            x1_ver = start_x - (50 * linear_angle_sin) * start_mag_y + (50 * linear_angle_cos) * start_mag_y
            x2_ver = start_x - (50 * linear_angle_sin) * end_mag_y + (50 * linear_angle_cos) * end_mag_y
            y1_ver = start_y + val_start_adj
            y2_ver = end_y - val_end_adj

            linear_force_start = force_canvas.create_line(
                start_x - (50 * linear_angle_sin) * start_mag_y + (50 * linear_angle_cos) * start_mag_y,
                start_y + val_start_adj, start_x, start_y + val_start_adj, width=7, arrow=LAST, arrowshape=(10, 7, 4))
            linear_force_end = force_canvas.create_line(
                start_x - (50 * linear_angle_sin) * end_mag_y + (50 * linear_angle_cos) * end_mag_y,
                end_y - val_end_adj, start_x, end_y - val_end_adj, width=7, arrow=LAST, arrowshape=(10, 7, 4))

            a = (x2_ver - x1_ver) / (y2_ver - y1_ver)
            b = x1_ver - a * y1_ver

            linear_force_line = force_canvas.create_line(x1_ver, y1_ver, x2_ver, y2_ver, width=5)

            linear_force_texts = force_canvas.create_text(start_x - (70 * linear_angle_sin) + (70 * linear_angle_cos),start_y + val_start_adj - 12,
                                                          text=f"{mag_start_text}N/mm", font=('Arial', 15),fill='darkred')

            if mag_start_text != mag_end_text:
                linear_force_texte = force_canvas.create_text(
                    start_x - (70 * linear_angle_sin) + (70 * linear_angle_cos),
                    end_y - val_end_adj + 12, text=f"{mag_end_text}N/mm", font=('Arial', 15), fill='darkred')
                linear_force.append(linear_force_texte)

            while linear_y < end_y - val_end_adj:
                linear_x = a * linear_y + b
                linear_force.append(force_canvas.create_line(linear_x, linear_y, start_x, linear_y, width=7, arrow=LAST,arrowshape=(10, 7, 4)))
                linear_y += gap

        linear_force.append(linear_force_start)
        linear_force.append(linear_force_end)
        linear_force.append(linear_force_line)
        linear_force.append(linear_force_texts)

    def update1(event):
        global mag_start_text, mag_end_text
        mag_start_text = mag_start.get()
        mag_end_text = mag_end.get()
        updated_value = int(value_start.get())
        scale_start.set(updated_value)
        updated_value = int(value_end.get())
        scale_end.set(updated_value)

    def update_label1(val):
        global val_start, val_end, linear_force, val_start_adj
        value_start.delete(0, END)
        val_start = int(float(val))
        if val_start > lenght_force_line - val_end - 1:
            val_start = lenght_force_line - val_end - 1
        value_start.insert(0, val_start)
        val_start_adj = val_start / line_force_scale
        for item in linear_force:
            force_canvas.delete(item)
        linear_force.clear()
        draw_lin_force()

    def update_label2(val):
        global val_start, val_end, val_end_adj, linear_force
        value_end.delete(0, END)
        val_end = int(float(val))
        if lenght_force_line - val_end - 1 < val_start:
            val_end = lenght_force_line - val_start - 1
        value_end.insert(0, val_end)
        val_end_adj = val_end / line_force_scale
        for item in linear_force:
            force_canvas.delete(item)
        linear_force.clear()
        draw_lin_force()

    if selected_line:
        sel_coords = canvas.coords(selected_line)
        dim_coords_x = abs(sel_coords[0] - sel_coords[2])
        dim_coords_y = abs(sel_coords[1] - sel_coords[3])
        force_toplevel = CTkToplevel(window)
        force_toplevel.title("")
        force_toplevel.geometry("400x400")
        force_toplevel.attributes("-topmost", True)
        force_toplevel.resizable("False", "False")
        style = ttk.Style()
        style.configure("TScale", background="black", troughcolor="blue")
        style.configure("TLabel", background="black", troughcolor="blue", foreground="lightblue")
        if force_index == 1:
            force_canvas = Canvas(force_toplevel, width=475, height=300, bg='white')
            force_canvas.grid(row=0, column=0, padx=10, pady=10, sticky=E + W + N)
        if force_index == 2:
            force_canvas = Canvas(force_toplevel, width=475, height=300, bg='white')
            force_canvas.grid(row=0, column=0, columnspan = 2, padx=10, pady=10, sticky=E + W + N)

        if dim_coords_x > 2000 or dim_coords_y > 1000:
            line_force_scale = 8
            dim_coords_x /= 8
            dim_coords_y /= 8
        elif dim_coords_x > 1500 or dim_coords_y > 1000:
            line_force_scale = 6
            dim_coords_x /= 6
            dim_coords_y /= 6
        elif dim_coords_x > 1000 or dim_coords_y > 750:
            line_force_scale = 4
            dim_coords_x /= 4
            dim_coords_y /= 4
        elif dim_coords_x > 600 or dim_coords_y > 500:
            line_force_scale = 3
            dim_coords_x /= 3
            dim_coords_y /= 3
        elif dim_coords_x > 250 or dim_coords_y > 250:
            line_force_scale = 2
            dim_coords_x /= 2
            dim_coords_y /= 2
        else:
            line_force_scale = 1

        center_x = 237.5
        center_y = 150

        if sel_coords[1] == sel_coords[3]:
            start_x = center_x - dim_coords_x / 2
            start_y = center_y
            end_x = center_x + dim_coords_x / 2
            end_y = center_y
            force_canvas.create_line(start_x,start_y,end_x,end_y, fill='black',width=3)
            orientation = "horizontal"
            if force_index == 1:
                force_counter += 1
        if sel_coords[0] == sel_coords[2]:
            start_x = center_x
            start_y = center_y - dim_coords_y / 2
            end_x = center_x
            end_y = center_y + dim_coords_y / 2
            force_canvas.create_line(start_x,start_y,end_x,end_y, fill='black',width=3)
            orientation = "vertical"
            if force_index == 1:
                force_counter += 1

        if force_index ==1:
            value = Entry(force_toplevel, text="0", font=('Arial', 15,), justify=CENTER, width=6)
            value.grid(row=1, column=0)
            value.insert(0, "0")
            scale = ttk.Scale(force_toplevel, from_=0, to=(dim_coords_x + dim_coords_y) * line_force_scale, orient=HORIZONTAL,command=update_label, length=450)
            scale.grid(row=2, column=0, padx=10, pady=10)
            Angle_label = ttk.Label(force_toplevel, text="Natočenie sily:", font=('Arial', 12,))
            Angle_label.grid(row=3, column=0, padx=10, pady=0, sticky=W + S)
            entry_angle = ttk.Entry(force_toplevel, width=20)
            entry_angle.grid(row=4, column=0, padx=10, pady=10, ipady=5, sticky=W)
            entry_angle.insert(0, "0")
            Mag_label = ttk.Label(force_toplevel, text="Sila:", font=('Arial', 12,))
            Mag_label.grid(row=3, column=0, padx=10, pady=0, sticky= S)
            entry_mag = ttk.Entry(force_toplevel, width=20)
            entry_mag.grid(row=4, column=0, padx=10, pady=10, ipady=5)
            entry_mag.insert(0, "0")
            value.delete(0, END)
            value.insert(0, "0")
            value.bind("<Return>", update)
            entry_mag.bind("<Return>", update)
            entry_angle.bind("<Return>", update)
            force_button = customtkinter.CTkButton(force_toplevel, text="Vytvor silu", height=40, width= 50 ,command=place_force)
            force_button.grid(row=4, column=0, padx=10, pady=10, sticky=E + S)
            force_toplevel.bind("<Destroy>", lambda event: deselect_line())
            update("")

        elif force_index == 2:

            val_start = 0
            val_end = 0
            val_start_adj = val_start / line_force_scale
            val_end_adj = val_end / line_force_scale
            linear_force = []
            linear_angle = 0
            mag_start_text,mag_end_text = 200,200

            value_start = Entry(force_toplevel, font=('Arial', 15), justify=CENTER, width=6)
            value_start.grid(row=1, column=0, padx=15, sticky=W + E)
            value_start.insert(0, "0")

            value_end = Entry(force_toplevel, font=('Arial', 15), justify=CENTER, width=6)
            value_end.grid(row=1, column=1, padx=15, sticky=W + E)
            value_end.insert(0, int((dim_coords_x + dim_coords_y) * line_force_scale))

            lenght_force_line = int((dim_coords_x + dim_coords_y) * line_force_scale)

            value_start.bind("<Return>", update1)
            value_end.bind("<Return>", update1)

            scale_start = ttk.Scale(force_toplevel, from_=0, to=(dim_coords_x + dim_coords_y) * line_force_scale,orient=HORIZONTAL, command=update_label1, length=225)
            scale_start.grid(row=2, column=0, padx=10, pady=10, sticky=E)

            scale_end = ttk.Scale(force_toplevel, from_=(dim_coords_x + dim_coords_y) * line_force_scale, to=0,orient=HORIZONTAL, command=update_label2, length=225)
            scale_end.grid(row=2, column=1, padx=10, pady=10, sticky=W)
            value_end.delete(0, END)
            scale_end.set(0)

            linear_angle_button = customtkinter.CTkButton(force_toplevel, text="otoč", height=40, width=50, command=turn_linear)
            linear_angle_button.grid(row=4, column=0, padx=10, pady=10, sticky=W)

            mag_start = Entry(force_toplevel, font=('Arial', 15), justify=CENTER, width=6)
            mag_start.grid(row=3, column=0, padx=15, sticky=W + E)
            mag_start.insert(0, "200")
            mag_end = Entry(force_toplevel, font=('Arial', 15), justify=CENTER, width=6)
            mag_end.grid(row=3, column=1, padx=15, sticky=W + E)
            mag_end.insert(0, "200")

            add_linear = customtkinter.CTkButton(force_toplevel, text="Vytvor silu", height=40, width=50, command=place_force)
            add_linear.grid(row=4, column=1, padx=10, pady=10, sticky=E)

            mag_start.bind("<Return>", update1)
            mag_end.bind("<Return>", update1)


            force_toplevel.bind("<Destroy>", lambda event: deselect_line())

    if selected_arc:
        force_toplevel = CTkToplevel(window)
        force_toplevel.title("")
        force_toplevel.geometry("400x400")
        force_toplevel.attributes("-topmost", True)
        force_toplevel.resizable("False", "False")
        style = ttk.Style()
        style.configure("TScale", background="black", troughcolor="blue")
        style.configure("TLabel", background="black", troughcolor="blue", foreground="lightblue")

        force_canvas = Canvas(force_toplevel, width=475, height=300, bg='white')
        force_canvas.grid(row=0, column=0, padx=10, pady=10, sticky=E + W + N)

        start_x = canvas.coords(selected_arc)[0]
        start_y = canvas.coords(selected_arc)[1]
        end_x = canvas.coords(selected_arc)[2]
        end_y = canvas.coords(selected_arc)[3]

        center_x = 237.5
        center_y = 150
        dim = abs(end_x - start_x)

        if dim > 2000:
            arc_force_scale = 15
            dim /= 15
        elif dim > 1500:
            arc_force_scale = 10
            dim /= 10
        elif dim > 300:
            arc_force_scale = 3
            dim /= 3
        elif dim > 250:
            arc_force_scale = 2
            dim /= 2
        elif dim > 200:
            arc_force_scale = 1.5
            dim /= 1.5
        else:
            arc_force_scale = 1

        start_x = center_x - dim / 2
        start_y = center_y - dim / 2
        end_x = center_x + dim / 2
        end_y = center_y + dim / 2
        start_arc = int(float(canvas.itemcget(selected_arc, 'start')))
        force_counter += 1

        force_canvas.create_arc(start_x, start_y, end_x, end_y, outline='black', width=3, style=ARC, start=start_arc, extent=90)

        value = Entry(force_toplevel, text="0", font=('Arial', 15,), justify=CENTER, width=6)
        value.grid(row=1, column=0)
        value.insert(0, "0")
        scale = ttk.Scale(force_toplevel, from_=0, to=90, orient=HORIZONTAL, length=450, command=update_label_arc)
        scale.grid(row=2, column=0, padx=10, pady=10)
        Angle_label = ttk.Label(force_toplevel, text="Natočenie sily:", font=('Arial', 12,))
        Angle_label.grid(row=3, column=0, padx=10, pady=0, sticky=W + S)
        entry_angle = ttk.Entry(force_toplevel, width=20)
        entry_angle.grid(row=4, column=0, padx=10, pady=10, ipady=5, sticky=W)
        entry_angle.insert(0, "0")
        Mag_label = ttk.Label(force_toplevel, text="Sila:", font=('Arial', 12,))
        Mag_label.grid(row=3, column=0, padx=10, pady=0, sticky=S)
        entry_mag = ttk.Entry(force_toplevel, width=20)
        entry_mag.grid(row=4, column=0, padx=10, pady=10, ipady=5)
        entry_mag.insert(0, "0")
        value.delete(0, END)
        value.insert(0, "0")
        value.bind("<Return>", update)
        entry_mag.bind("<Return>", update)
        entry_angle.bind("<Return>", update)
        force_button = customtkinter.CTkButton(force_toplevel, text="Vytvor silu", height=40, width=50,command=place_force)
        force_button.grid(row=4, column=0, padx=10, pady=10, sticky=E + S)
        force_toplevel.bind("<Destroy>", lambda event: deselect_line())
        update("")

def place_moment():
    global moment_mag,moment_position,sel_coords,M_dot,M_mag,moment_counter,moment_orientation
    if selected_line:
        coords_line_moment = canvas.coords(selected_line)
        if orientation == "horizontal":
            if sel_coords[0]>sel_coords[2]:
                sel_coords[0] = sel_coords[2]
            if moment_orientation == 0:
                moment_window = canvas.create_arc(moment_position + sel_coords[0] - 50, sel_coords[1] - 50, moment_position + sel_coords[0] + 50, sel_coords[1] + 50,
                                                         outline='black', width=3, style=ARC, start=30, extent=150)

                moment_window_line = canvas.create_line(moment_position + sel_coords[0] - 48, sel_coords[1] + 7, moment_position + sel_coords[0] - 48, sel_coords[1] + 8,
                                                           fill='black', width=1, arrow=LAST, arrowshape=(20, 25, 10))
            if moment_orientation == 1:
                moment_window = canvas.create_arc(moment_position + sel_coords[0] - 50, sel_coords[1] - 50,
                                                  moment_position + sel_coords[0] + 50, sel_coords[1] + 50,
                                                  outline='black', width=3, style=ARC, start=0, extent=150)

                moment_window_line = canvas.create_line(moment_position + sel_coords[0] + 48, sel_coords[1] + 7,
                                                        moment_position + sel_coords[0] + 48, sel_coords[1] + 8,
                                                        fill='black', width=1, arrow=LAST, arrowshape=(20, 25, 10))
            moment_text = canvas.create_text(moment_position + sel_coords[0], sel_coords[1] - 60, text=f"M{moment_counter}={moment_mag}Nm",
                                                    font=('Arial', 15), fill='darkred')
            moment_dot = canvas.create_oval(moment_position + sel_coords[0] - 4, sel_coords[1] - 4, moment_position + sel_coords[0] + 4, sel_coords[1] + 4, fill='red')
            combinated_hor.append(canvas.coords(moment_dot)[0]+4)
            for beam in calc_points["horizontal"]:
                if beam["coords"] == coords_line_moment:  # Porovnanie súradníc
                    beam["moments"].append([canvas.coords(moment_dot)[0] + 4, canvas.coords(moment_dot)[1] + 4])
                    if moment_orientation == 0:
                        beam["moments_mag"].append(int(moment_mag))
                    else:
                        beam["moments_mag"].append(-int(moment_mag))

            print("combinated", combinated_hor)
        if orientation == "vertical":
            if sel_coords[1]>sel_coords[3]:
                sel_coords[1] = sel_coords[3]
            if moment_orientation == 0:
                moment_window = canvas.create_arc( sel_coords[0] - 50, moment_position +sel_coords[1] - 50,
                                                  sel_coords[0] + 50,moment_position + sel_coords[1] + 50,
                                                  outline='black', width=3, style=ARC, start=30, extent=150)

                moment_window_line = canvas.create_line(sel_coords[0] - 48, moment_position +sel_coords[1] + 7,
                                                         sel_coords[0] - 48, moment_position +sel_coords[1] + 8,
                                                        fill='black', width=1, arrow=LAST, arrowshape=(20, 25, 10))
            if moment_orientation == 1:
                moment_window = canvas.create_arc(sel_coords[0] - 50, moment_position + sel_coords[1] - 50,
                                                  sel_coords[0] + 50, moment_position + sel_coords[1] + 50,
                                                  outline='black', width=3, style=ARC, start=0, extent=150)

                moment_window_line = canvas.create_line(sel_coords[0] + 48, moment_position + sel_coords[1] + 7,
                                                        sel_coords[0] + 48, moment_position + sel_coords[1] + 8,
                                                        fill='black', width=1, arrow=LAST, arrowshape=(20, 25, 10))

            moment_text = canvas.create_text( sel_coords[0],moment_position + sel_coords[1] - 60,
                                             text=f"M{moment_counter}={moment_mag}Nm",
                                             font=('Arial', 15), fill='darkred')
            moment_dot = canvas.create_oval( sel_coords[0] - 4,moment_position + sel_coords[1] - 4,
                                             sel_coords[0] + 4, moment_position +sel_coords[1] + 4, fill='red')
            combinated_ver.append(canvas.coords(moment_dot)[1])
            for beam in calc_points["vertical"]:
                if beam["coords"] == coords_line_moment:  # Porovnanie súradníc
                    beam["moments"].append([canvas.coords(moment_dot)[0] + 4, canvas.coords(moment_dot)[1] + 4])
                    if moment_orientation == 0:
                        beam["moments_mag"].append(int(moment_mag))
                    else:
                        beam["moments_mag"].append(-int(moment_mag))
        M_dot.append((canvas.coords(moment_dot)[0] + 4, canvas.coords(moment_dot)[1] + 4))
        if moment_orientation == 0:
            M_mag.append(int(moment_mag))
        else:
            M_mag.append(-int(moment_mag))

    moment_toplevel.destroy()
    deselect_line()

def place_moment_window():
    global place_moment_flag, sel_coords, moment_window, moment_toplevel, moment_text, moment_counter,orientation,\
        moment_window_line, moment_dot,line_force_scale,moment_counter,moment_orientation
    scroll_unbind()
    moment_orientation = 0
    if not selected_line and not selected_arc:
        place_moment_flag = True
        canvas.bind('<Button-1>', select_line)
    moment_window = None
    moment_window_line = None
    moment_text = None
    moment_dot = None
    def update_label(val):
        global sel_coords, moment_window, moment_text, end_x_adj, end_y_adj, moment_window_line, moment_dot,moment_mag,\
            moment_position,line_force_scale, moment_orientation
        value.delete(0, END)
        value.insert(0, int(float(val)))
        val = int(float(val)) / line_force_scale
        moment_position = val * line_force_scale
        if moment_window:
            moment_canvas.delete(moment_window)
        if moment_window_line:
            moment_canvas.delete(moment_window_line)
        if moment_text:
            moment_canvas.delete(moment_text)
        if moment_dot:
            moment_canvas.delete(moment_dot)
        updated_angle = 0
        if orientation == "horizontal":

            if moment_orientation == 0:
                moment_window = moment_canvas.create_arc(val + start_x-50, start_y-50,val + start_x+50,start_y+50, outline='black', width=3, style=ARC, start=30, extent=150)
                moment_window_line = moment_canvas.create_line(val + start_x-48,start_y+7,val + start_x-48,start_y+8, fill='black', width=1, arrow=LAST, arrowshape=(20, 25, 10))
            if moment_orientation == 1:
                moment_window = moment_canvas.create_arc(val + start_x - 50, start_y - 50, val + start_x + 50,start_y + 50, outline='black', width=3, style=ARC, start=0,extent=150)
                moment_window_line = moment_canvas.create_line(val + start_x + 48, start_y + 7, val + start_x + 48,start_y + 8, fill='black', width=1, arrow=LAST,arrowshape=(20, 25, 10))
            moment_text = moment_canvas.create_text(val + start_x, start_y - 60,text=f"M{moment_counter}={entry_mag.get()}Nm", font=('Arial', 15),fill='darkred')
            moment_dot = moment_canvas.create_oval(val + start_x - 4, start_y - 4, val + start_x + 4, start_y + 4,fill='red')
            moment_mag = entry_mag.get()

            if sel_coords[0] < sel_coords[2]:
                start_moment_x = val*line_force_scale + sel_coords[0]
                start_moment_y = sel_coords[1]
                end_x_adj, end_y_adj = start_moment_x + math.sin(math.radians(updated_angle)) * 50, start_moment_y + math.cos(math.radians(updated_angle)) * 50
            else:
                start_moment_x = val*line_force_scale + sel_coords[2]
                start_moment_y = sel_coords[1]
                end_x_adj, end_y_adj = start_moment_x + math.sin(math.radians(updated_angle)) * 50, start_moment_y + math.cos(math.radians(updated_angle)) * 50

        elif orientation == "vertical":

            if moment_orientation == 0:
                moment_window = moment_canvas.create_arc(start_x - 50, val +start_y - 50, start_x + 50, val + start_y + 50,outline='black', width=3, style=ARC, start=30, extent=150)
                moment_window_line = moment_canvas.create_line(start_x - 48,val + start_y + 7, start_x - 48,val +start_y + 8, fill='black', width=1, arrow=LAST,arrowshape=(20, 25, 10))
            if moment_orientation == 1:
                moment_window = moment_canvas.create_arc(start_x - 50, val + start_y - 50, start_x + 50,val + start_y + 50, outline='black', width=3, style=ARC,start=0, extent=150)
                moment_window_line = moment_canvas.create_line(start_x + 48, val + start_y + 7, start_x + 48,val + start_y + 8, fill='black', width=1, arrow=LAST,arrowshape=(20, 25, 10))
            moment_text = moment_canvas.create_text(start_x, val +start_y - 60,text=f"M{moment_counter}={entry_mag.get()}Nm", font=('Arial', 15),fill='darkred')
            moment_dot = moment_canvas.create_oval( start_x - 4, val +start_y - 4,start_x + 4, val + start_y + 4,fill='red')
            moment_mag = entry_mag.get()

            if sel_coords[1] < sel_coords[3]:
                start_moment_x = sel_coords[0]
                start_moment_y = val * line_force_scale + sel_coords[1]
                end_x_adj, end_y_adj = start_moment_x + math.sin(math.radians(updated_angle)) * 50, start_moment_y + math.cos(math.radians(updated_angle)) * 50
            else:
                start_moment_x = sel_coords[2]
                start_moment_y = val * line_force_scale + sel_coords[1]
                end_x_adj, end_y_adj = start_moment_x + math.sin(math.radians(updated_angle)) * 50, start_moment_y + math.cos(math.radians(updated_angle)) * 50



    def update(event):
        updated_value = int(value.get())
        scale.set(updated_value)

    def change_orient():
        global moment_orientation
        if moment_orientation == 0:
            moment_orientation = 1
        else:
            moment_orientation = 0
        update("")

    if selected_line:
        sel_coords = canvas.coords(selected_line)
        dim_coords_x = abs(sel_coords[0] - sel_coords[2])
        dim_coords_y = abs(sel_coords[1] - sel_coords[3])
        moment_toplevel = CTkToplevel(window)
        moment_toplevel.title("")
        moment_toplevel.geometry("400x400")
        moment_toplevel.attributes("-topmost", True)
        moment_toplevel.resizable("False", "False")
        style = ttk.Style()
        style.configure("TScale", background="black", troughcolor="blue")
        style.configure("TLabel", background="black", troughcolor="blue", foreground="lightblue")
        moment_canvas = Canvas(moment_toplevel, width=475, height=300, bg='white')
        moment_canvas.grid(row=0, column=0, padx=10, pady=10, sticky=E + W + N)

        if dim_coords_x > 2000 or dim_coords_y > 1000:
            line_force_scale = 8
            dim_coords_x /= 8
            dim_coords_y /= 8
        elif dim_coords_x > 1500 or dim_coords_y > 1000:
            line_force_scale = 6
            dim_coords_x /= 6
            dim_coords_y /= 6
        elif dim_coords_x > 1000 or dim_coords_y > 750:
            line_force_scale = 4
            dim_coords_x /= 4
            dim_coords_y /= 4
        elif dim_coords_x > 600 or dim_coords_y > 500:
            line_force_scale = 3
            dim_coords_x /= 3
            dim_coords_y /= 3
        elif dim_coords_x > 250 or dim_coords_y > 250:
            line_force_scale = 2
            dim_coords_x /= 2
            dim_coords_y /= 2
        else:
            line_force_scale = 1

        center_x = 237.5
        center_y = 150

        if sel_coords[1] == sel_coords[3]:
            start_x = center_x - dim_coords_x / 2
            start_y = center_y
            end_x = center_x + dim_coords_x / 2
            end_y = center_y
            moment_canvas.create_line(start_x, start_y, end_x, end_y, fill='black', width=3)
            orientation = "horizontal"
        if sel_coords[0] == sel_coords[2]:
            start_x = center_x
            start_y = center_y - dim_coords_y / 2
            end_x = center_x
            end_y = center_y + dim_coords_y / 2
            moment_canvas.create_line(start_x, start_y, end_x, end_y, fill='black', width=3)
            orientation = "vertical"

        value = Entry(moment_toplevel, text="0", font=('Arial', 15,), justify=CENTER, width=6)
        value.grid(row=1, column=0)
        value.insert(0, "0")
        scale = ttk.Scale(moment_toplevel, from_=0, to=(dim_coords_x + dim_coords_y) * line_force_scale,
                          orient=HORIZONTAL, command=update_label, length=450)
        scale.grid(row=2, column=0, padx=10, pady=10)
        Mag_label = ttk.Label(moment_toplevel, text="Moment:", font=('Arial', 12,))
        Mag_label.grid(row=3, column=0, padx=10, pady=0, sticky=S)
        entry_mag = ttk.Entry(moment_toplevel, width=20)
        entry_mag.grid(row=4, column=0, padx=10, pady=10, ipady=5)
        entry_mag.insert(0, "0")
        value.delete(0, END)
        value.insert(0, "0")
        value.bind("<Return>", update)
        entry_mag.bind("<Return>", update)
        moment_button = customtkinter.CTkButton(moment_toplevel, text="Vytvor moment", height=40, width=50,
                                               command=place_moment)
        moment_button.grid(row=4, column=0, padx=10, pady=10, sticky=E + S)
        change_orientation = customtkinter.CTkButton(moment_toplevel, text="Zmen orientáciu", height=40, width=50, command=change_orient)
        change_orientation.grid(row=4, column=0, padx=10, pady=10, sticky=W + S)
        moment_toplevel.bind("<Destroy>", lambda event: deselect_line())
        moment_counter += 1
        update("")


def calc():
    global lines, force_obj, force_mag, sup_obj, sup_obj_ind, force_angle, size_c, force_linear, force_linear_mag,c,k,sup_angle\
        , force_c, filtered_0_hor,sum_force_y,sum_force_x,linear_mag_y,con_point,arcs,T_all,M_all,N_all,T_all_ver,M_all_ver,N_all_ver,x_coords,y_coords,lines_sorted


    coords_c = []
    dlzky_usekov = []
    k = 0
    c = 0
    C_values = []
    D_values = [0, 0]
    C_values_ver = []
    D_values_ver = [0, 0]
    sup_flag = 0 #zistinie ktory sup ind je na ktorej strane
    x_flag = 0 #priradenie prvku x k podpore

    def identify_beam_type_and_direction(start, end):
        if start[1] == end[1]:  # Horizontálny prút
            if start[0] < end[0]:
                return "horizontal", "right"
            else:
                return "horizontal", "left"
        elif start[0] == end[0]:  # Vertikálny prút
            if start[1] < end[1]:
                return "vertical", "down"
            else:
                return "vertical", "up"
        else:  # Oblúk
            return "arc", None

    # Vytvoríme mapu prepojení prútov k jednotlivým bodom
    connections = defaultdict(list)

    # Pridanie prútov do connections
    for line_obj in lines:
        coords = canvas.coords(line_obj)
        start = (coords[0], coords[1])
        end = (coords[2], coords[3])
        beam_type, direction = identify_beam_type_and_direction(start, end)  # Identifikácia typu a smeru prúta
        connections[start].append((start, end, beam_type, direction))
        connections[end].append((start, end, beam_type, direction))

    # Pridanie oblúkov do connections
    for arc in arcs:
        arc_coords = canvas.coords(arc)
        arc_start = (arc_coords[0], arc_coords[1])
        arc_end = (arc_coords[2], arc_coords[3])
        beam_type, direction = identify_beam_type_and_direction(arc_start, arc_end)  # Identifikácia oblúka
        connections[arc_start].append((arc_start, arc_end, beam_type, direction))
        connections[arc_end].append((arc_start, arc_end, beam_type, direction))

    # Extrahovanie všetkých prútov zo connections
    all_connections = []
    for value in connections.values():
        all_connections.extend(value)

    # Normalizácia bodov a odstránenie duplicít
    lines_normalized = {
        (min(line[0], line[1]), max(line[0], line[1]), line[2], line[3]) for line in all_connections
    }

    # Triedenie podľa najmenšieho bodu
    lines_sorted = sorted(lines_normalized, key=lambda line: (line[0], line[1]))

    def update_beam_direction(prev_end, curr_start, curr_end):
        if prev_end == curr_start:
            if curr_start[1] == curr_end[1]:  # Horizontálny prút
                if curr_start[0] < curr_end[0]:
                    return "right"
                elif curr_start[0] > curr_end[0]:
                    return "left"
            elif curr_start[0] == curr_end[0]:  # Vertikálny prút
                if curr_start[1] < curr_end[1]:
                    return "down"
                elif curr_start[1] > curr_end[1]:
                    return "up"
        elif prev_end == curr_end:
            if curr_end[1] == curr_start[1]:  # Horizontálny prút
                if curr_end[0] < curr_start[0]:
                    return "left"
                elif curr_end[0] > curr_start[0]:
                    return "right"
            elif curr_end[0] == curr_start[0]:  # Vertikálny prút
                if curr_end[1] < curr_start[1]:
                    return "up"
                elif curr_end[1] > curr_start[1]:
                    return "down"

    # Prechádzanie zoradených prútov
    lines_updated = []  # Nový zoznam pre aktualizované prúty

    previous_beam = None
    for current_beam in lines_sorted:
        start, end, beam_type, _ = current_beam
        if previous_beam is None:
            # Iniciálna identifikácia pre prvý prút
            # Urč smer na základe voľného konca
            if len(connections[start]) == 1:  # Ak je start voľný
                direction = identify_beam_type_and_direction(start, end)[1]
            elif len(connections[end]) == 1:  # Ak je end voľný
                direction = identify_beam_type_and_direction(end, start)[1]
            else:
                direction = identify_beam_type_and_direction(start, end)[1]
        else:
            prev_start, prev_end, _, prev_direction = previous_beam

            # Kontrola, či nový prút nadväzuje na predchádzajúci
            if prev_end == start:
                direction = update_beam_direction(prev_end, start, end)
            elif prev_end == end:
                direction = update_beam_direction(prev_end, end, start)
            elif prev_start == start:
                direction = update_beam_direction(prev_start, start, end)
            elif prev_start == end:
                direction = update_beam_direction(prev_start, end, start)

        # Aktualizácia hodnoty smeru a uloženie prúta do lines_updated
        updated_beam = (start, end, beam_type, direction)
        lines_updated.append(updated_beam)

        # Nastavenie current_beam ako previous_beam pre ďalšiu iteráciu
        previous_beam = updated_beam

    # Výstup v požadovanom formáte
    for line in lines_sorted:
        print(f"Prut: {line}")
    for line in lines_updated:
        print(f"Prut_upd: {line}")

    lines_sorted = lines_updated

    segments_hor = []  # Pre horizontálne prúty
    segments_ver = []  # Pre vertikálne prúty
    unique_hor = []
    unique_ver = []
    num_segments_hor = []
    num_segments_ver = []


    # Prejdi všetky prúty a zhromaždi body pre každý prút osobitne
    for beam in calc_points["horizontal"]:
        start_x, _, end_x, _ = beam["coords"]
        segments_hor = [start_x, end_x]

        # Zhromaždi podporu, sily, lineárne sily a momenty pre tento prút
        for support in beam["supports"]:
            segments_hor.append(support[0])
        for force in beam["forces"]:
            segments_hor.append(force[0])
        for linear in beam["linear_forces"]:
            segments_hor.extend([linear[0], linear[1]])
        for moment in beam["moments"]:
            segments_hor.append(moment[0])

        # Nájsť smer prútu z lines_updated
        beam_direction = None
        for line in lines_updated:
            print("beam dir", beam_direction)
            if (line[0] == (start_x, beam["coords"][1]) and line[1] == (end_x, beam["coords"][3])) or (line[0] == (end_x, beam["coords"][3]) and line[1] == (start_x, beam["coords"][1])):
                beam_direction = line[3]  # predpokladám, že smer je na 4. pozícii (napr. 'right', 'left', 'up', 'down')
                print("beam dir",beam_direction)
                break

        if beam_direction == "right":
            unique_hor.append(sorted(set(segments_hor)))  # vzostupné zoradenie
            num_segments_hor.extend(sorted(set(segments_hor)))
        elif beam_direction == "left":
            unique_hor.append(sorted(set(segments_hor), reverse=True))  # zostupné zoradenie
            num_segments_hor.extend(sorted(set(segments_hor)))

        print("uniqueeeeeeeee",unique_hor)
        # Pridaj unikátne segmenty do celkového zoznamu segmentov pre neskoršie použitie, ak je potrebné

    for beam in calc_points["vertical"]:
        _, start_y, _, end_y = beam["coords"]
        segments_ver = [start_y, end_y]

        # Zhromaždi podporu, sily, lineárne sily a momenty pre tento prút
        for support in beam["supports"]:
            segments_ver.append(support[1])
        for force in beam["forces"]:
            segments_ver.append(force[1])
        for linear in beam["linear_forces"]:
            segments_ver.extend([linear[0], linear[1]])
        for moment in beam["moments"]:
            segments_ver.append(moment[1])

        # Nájsť smer prútu z lines_updated
        beam_direction = None
        for line in lines_updated:
            print("beam dir", beam_direction)
            if (line[0] == (beam["coords"][0], start_y) and line[1] == (beam["coords"][2], end_y)) or (
                    line[0] == (beam["coords"][2], end_y) and line[1] == (beam["coords"][0], start_y)):
                beam_direction = line[3]  # predpokladám, že smer je na 4. pozícii (napr. 'up', 'down')
                print("beam dir", beam_direction)
                break

        # Urči smer prútu a zoradiť segmenty pre tento konkrétny prút
        if beam_direction == "up":
            unique_ver.append(sorted(set(segments_ver), reverse=True))  # vzostupné zoradenie
            num_segments_ver.extend(sorted(set(segments_ver)))
        elif beam_direction == "down":
            unique_ver.append(sorted(set(segments_ver)))  # zostupné zoradenie
            num_segments_ver.extend(sorted(set(segments_ver)))


    #uprav up,down podmienka prut predtym right left a nasledne revesre!!!!!!!!!!!!!!!!!

    num_segments = len(num_segments_hor) + len(num_segments_ver) - len(lines_updated)
    print("segments_hor,segments_ver",segments_hor,segments_ver,num_segments)
    q_seg = [0] * (num_segments+1)
    F_seg = [0] * (num_segments+1)
    F_x_seg = [0] * (num_segments+1)
    M_seg = [0] * (num_segments+1)
    R_seg = [0] * (num_segments+1)
    R_x_seg = [0] * (num_segments+1)
    segment_pos = 0

    # Prechádzaj prúty v poradí definovanom v lines_updated
    for line in lines_updated:
        # Zisti, či ide o horizontálny alebo vertikálny prút
        start_coords, end_coords, beam_type, direction = line
        if beam_type == 'horizontal':
            # Nájsť zodpovedajúci prút v calc_points["horizontal"]
            for l, beam in enumerate(calc_points["horizontal"]):
                start_x, start_y, end_x, _ = beam["coords"]
                if (start_coords == (start_x, start_y) and end_coords == (end_x, start_y)) or \
                        (start_coords == (end_x, start_y) and end_coords == (start_x, start_y)):
                    segments_subset = unique_hor[l]
                    for i in range(len(segments_subset) - 1):
                        # Iterácia cez segmenty prútu
                        for idx, linear in enumerate(beam["linear_forces"]):
                            linear_start = linear[0]
                            linear_end = linear[1]
                            if segments_subset[i + 1] > linear_start and segments_subset[i] < linear_end and linear[2] - 60 <= start_y <= linear[2] + 60:
                                q_magnitude = beam["linear_forces_mag"][idx][0]

                                # Ak je smer opačný (napr. zospodu), zmeň znamienko
                                #if linear[2] > start_y:
                                 #   q_magnitude *= -1

                                q_seg[segment_pos] += q_magnitude
                        for idx, force in enumerate(beam["forces"]):
                            if segments_subset[i] == force[0] and force[1] == start_y:
                                force_angle_seg = beam["forces_angle"][idx]
                                F_seg[segment_pos] += beam["forces_mag"][idx] * -round(
                                    math.cos(math.radians(force_angle_seg)), 2)
                                F_x_seg[segment_pos] += beam["forces_mag"][idx] * round(
                                    math.sin(math.radians(force_angle_seg)), 2)
                            elif end_x == force[0] and force[1] == start_y:
                                force_angle_seg = beam["forces_angle"][idx]
                                #F_seg[segment_pos+1] += beam["forces_mag"][idx] * -round(
                                    #math.cos(math.radians(force_angle_seg)), 2)
                                #F_x_seg[segment_pos+1] += beam["forces_mag"][idx] * round(
                                    #math.sin(math.radians(force_angle_seg)), 2)
                        for idx, moment in enumerate(beam["moments"]):
                            if segments_subset[i] == moment[0] and moment[1] == start_y:
                                M_seg[segment_pos] += beam["moments_mag"][idx]
                            elif end_x == moment[0] and moment[1] == start_y:
                                M_seg[segment_pos+1] += beam["moments_mag"][idx]
                        for idx, support in enumerate(beam["supports"]):
                            if segments_subset[i] == support[0] and support[1] == start_y:
                                if beam["supports_index"][idx] == 1:
                                    R_seg[segment_pos] = "sup1"
                                    R_x_seg[segment_pos] = "sup1"
                                elif beam["supports_index"][idx] == 2:
                                    R_seg[segment_pos] = "sup2"
                                elif beam["supports_index"][idx] == 3:
                                    R_seg[segment_pos] = "sup3"
                                    R_x_seg[segment_pos] = "sup3"
                        segment_pos += 1

        elif beam_type == 'vertical':
            # Nájsť zodpovedajúci prút v calc_points["vertical"]
            for l, beam in enumerate(calc_points["vertical"]):
                start_x, start_y, _, end_y = beam["coords"]
                if (start_coords == (start_x, start_y) and end_coords == (start_x, end_y)) or \
                        (start_coords == (start_x, end_y) and end_coords == (start_x, start_y)):

                    segments_subset = unique_ver[l]
                    for i in range(len(segments_subset) - 1):
                        # Iterácia cez segmenty prútu
                        for idx, linear in enumerate(beam["linear_forces"]):
                            if segments_subset[i + 1] > linear[0] and segments_subset[i] < linear[1] and abs(
                                    start_x - linear[2]) <= 60:
                                q_seg[segment_pos] += beam["linear_forces_mag"][idx][0]
                        for idx, force in enumerate(beam["forces"]):
                            if segments_subset[i] == force[1] and force[0] == start_x:
                                force_angle_seg = beam["forces_angle"][idx]
                                F_seg[segment_pos] += beam["forces_mag"][idx] * -round(
                                    math.cos(math.radians(force_angle_seg)), 2)
                                F_x_seg[segment_pos] += beam["forces_mag"][idx] * round(
                                    math.sin(math.radians(force_angle_seg)), 2)
                                print("Pridávam silu na ver na", F_seg, F_x_seg, segment_pos)
                        for idx, moment in enumerate(beam["moments"]):
                            if segments_subset[i] == moment[1] and moment[0] == start_x:
                                M_seg[segment_pos] += beam["moments_mag"][idx]
                        for idx, support in enumerate(beam["supports"]):
                            if segments_subset[i] == support[1] and support[0] == start_x:
                                if beam["supports_index"][idx] == 1:
                                    R_seg[segment_pos] = "sup1"
                                    R_x_seg[segment_pos] = "sup1"
                                elif beam["supports_index"][idx] == 2:
                                    R_seg[segment_pos] = "sup2"
                                elif beam["supports_index"][idx] == 3:
                                    R_seg[segment_pos] = "sup3"
                                    R_x_seg[segment_pos] = "sup3"

                        segment_pos += 1

    # Vypis vyslednych hodnot pre kontrolu
    print("ccc",calc_points)
    print("q_seg:", q_seg)
    print("F_seg:", F_seg)
    print("F_x_seg:", F_x_seg)
    print("M_seg:", M_seg)
    print("R_seg:", R_seg)
    print("Rx_seg:", R_x_seg)

    # rozdelenie pre urcenie x[n] k podporam
    if sup_obj_ind[0] != 3:
        x_ver_flag = 0
        x_flag = 1
        # Kontrola pre horizontálne alebo vertikálne prúty
        if (sup_obj_c[0][0] < sup_obj_c[1][0] or sup_obj_c[0][1] > sup_obj_c[1][1]) and sup_obj_ind[0] == 1:
            sup_flag = 2
            print("Tady 1")

        elif (sup_obj_c[0][0] > sup_obj_c[1][0] or sup_obj_c[0][1] < sup_obj_c[1][1]) and sup_obj_ind[0] == 2:
            sup_flag = 2
            sup_obj_c[0], sup_obj_c[1] = sup_obj_c[1], sup_obj_c[0]
            sup_obj_ind[0], sup_obj_ind[1] = sup_obj_ind[1], sup_obj_ind[0]
            print("Tady 2")

        elif (sup_obj_c[0][0] > sup_obj_c[1][0] or sup_obj_c[0][1] < sup_obj_c[1][1]) and sup_obj_ind[0] == 1:
            sup_flag = 1
            sup_obj_c[0], sup_obj_c[1] = sup_obj_c[1], sup_obj_c[0]
            sup_obj_ind[0], sup_obj_ind[1] = sup_obj_ind[1], sup_obj_ind[0]
            print("Tady 3")

        elif (sup_obj_c[0][0] < sup_obj_c[1][0] or sup_obj_c[0][1] > sup_obj_c[1][1]) and sup_obj_ind[0] == 2:
            sup_flag = 1
            print("Tady 4")

    i = 0
    for mag in force_mag:
        #x
        sum_force_x = sum_force_x + mag*math.sin(math.radians(force_angle[i]))
        #y
        sum_force_y = sum_force_y + mag*math.cos(math.radians(force_angle[i]))
        i +=1


    #ziskanie dolezitych bodov na horizontalnych prutoch
    element_count_hor = {}
    for element in combinated_hor:
        element_tuple = tuple(element) if isinstance(element, list) else element
        if element_tuple in element_count_hor:
            element_count_hor[element_tuple] += 1
        else:
            element_count_hor[element_tuple] = 1

    filtered = [element for element in combinated_hor if
                       element_count_hor[tuple(element) if isinstance(element, list) else element] == 1]


    for element, count in element_count_hor.items():
        if count > 1:
            filtered.append(list(element) if isinstance(element, tuple) else element)

    filtered.sort()
    if filtered:
        first_element = filtered[0]
        last_element = filtered[-1]

    # ziskanie dolezitych bodov na verikalnych prutoch
    element_count_ver = {}

    for element in combinated_ver:
        element_tuple = tuple(element) if isinstance(element, list) else element
        if element_tuple in element_count_ver:
            element_count_ver[element_tuple] += 1
        else:
            element_count_ver[element_tuple] = 1

    filtered_ver = [element for element in combinated_ver if
                       element_count_ver[tuple(element) if isinstance(element, list) else element] == 1]

    for element, count in element_count_ver.items():
        if count > 1:
            filtered_ver.append(list(element) if isinstance(element, tuple) else element)

    filtered_ver.sort()
    if filtered_ver:
        first_element_ver = filtered_ver[0]
        last_element_ver = filtered_ver[-1]



    q_usekov = [0] * (len(filtered))
    q_usekov_ver = [0] * (len(filtered_ver) - 1)
    if force_linear and force_linear_mag:
        for q_idx, q in enumerate(force_linear):
            q_start_x = q[0]
            q_end_x = q[2]
            q_start_y = q[1]
            q_end_y = q[3]
            print("q_start_y a q_end_y",q_start_y,q_end_y)

            #DOROB znamienko na prehodenie orient
            q_value = int(force_linear_mag[q_idx][0])

            for i in range(len(filtered) - 1):
                start_x = filtered[i]
                if q_start_x <= start_x < q_end_x:
                    q_usekov[i] += q_value

            for i in range(len(filtered_ver) - 1):
                start_y = filtered_ver[i]
                print("start_y",start_y)
                if q_start_y <= start_y < q_end_y:
                    q_usekov_ver[i] += q_value






    F_usekov = [0] * (len(filtered))
    F_x_usekov = [0] * (len(filtered))
    F_end = 0

    F_usekov_ver = [0] * (len(filtered_ver))
    F_x_usekov_ver = [0] * (len(filtered_ver))
    F_end_ver = 0
    M_usekov_ver = [0] * (len(filtered_ver))
    for j in range(len(lines_sorted)):
        if force_c and force_mag:
            for f_idx, f in enumerate(force_c):
                force_x = f[0]  # Použijeme hodnotu x1 z force_c
                force_y = f[1]
                force_y_value = round(-np.cos(np.radians(force_angle[f_idx]))*force_mag[f_idx],5)  # Získame hodnotu sily
                force_x_value = round(-np.sin(np.radians(force_angle[f_idx]))*force_mag[f_idx],5)

                if lines_sorted[j][2] == "horizontal":
                    for i in range(len(filtered) - 1):
                        start_x = filtered[i]
                        end_x = filtered[i + 1]
                        start = lines_sorted[j][0]
                        if force_y==start[1]:
                            if filtered:
                                if start_x != filtered[0] or lines_sorted[j - 1][2] != "vertical":
                                    # Kontrola, či sa sila nachádza na začiatku úseku
                                    if force_x == start_x:
                                        F_usekov[i] += force_y_value
                                        F_x_usekov[i] += force_x_value
                                        force_y_value, force_x_value = 0,0
                                        break
                                    if (i == len(filtered) - 2 and force_x == end_x):
                                        F_end += force_y_value
                if lines_sorted[j][2] == "vertical":
                    for i in range(len(filtered_ver) - 1):
                        start_x = filtered_ver[i]
                        end_x = filtered_ver[i + 1]
                        start = lines_sorted[j][0]
                        if force_x == start[0]:
                            if filtered_ver:
                                if start_x != filtered_ver[0] or lines_sorted[j-1][2] != "horizontal":
                                    # Kontrola, či sa sila nachádza na začiatku úseku
                                    if force_y == start_x:
                                        F_usekov_ver[i] += force_y_value
                                        F_x_usekov_ver[i] += force_x_value
                                        force_y_value, force_x_value = 0,0
                                        break
                                    if (i == len(filtered) - 2 and force_x == end_x):
                                        F_end_ver += force_y_value

    M_usekov = [0] * (len(filtered))
    if M_dot and M_mag:
        for m_idx, m in enumerate(M_dot):
            moment_x = m[0]
            moment_y = m[1]-4
            moment_value = M_mag[m_idx]

            for i in range(len(filtered) - 1):
                start_x = filtered[i]
                if moment_x == start_x:
                    M_usekov[i] += moment_value

            for i in range(len(filtered_ver) - 1):
                start_y = filtered_ver[i]
                if moment_y == start_y:
                    M_usekov_ver[i] += moment_value

    filtered_0_hor = [element - first_element for element in filtered]
    filtered_0_ver = [element - first_element_ver for element in filtered_ver]
    filtered_0_hor_left = [abs(element - last_element) for element in filtered]
    filtered_0_hor_left.reverse()
    filtered_0_ver_up = [abs(element - last_element_ver) for element in filtered_ver]
    filtered_0_ver_up.reverse()
    filtered_ver_up = [element + first_element_ver for element in filtered_0_ver_up]

    pocet_usekov = len(filtered_0_hor) - 1

    for i in range(pocet_usekov):
        dlzka = filtered_0_hor[i + 1] - filtered_0_hor[i]
        dlzky_usekov.append(dlzka)

    R_usekov_ver = [0] * (len(filtered_0_ver) - 1)
    R_y_usekov = [0] * (len(filtered_0_ver) - 1)

    row_index = 0
    A = np.zeros((3,3))
    b = np.zeros(3)
    b[0] = -sum_force_x
    b[1] = sum_force_y

    if sup_index !=3:
        if sup_obj_ind[0]==1:
            A_a = sup_obj_c[1][0]-sup_obj_c[0][0]
            A_b = sup_obj_c[0][1]-sup_obj_c[1][1]
            print("aa ab",A_a,A_b)
        elif sup_obj_ind[1]==1:
            A_a = sup_obj_c[0][0]-sup_obj_c[1][0]
            A_b = sup_obj_c[1][1]-sup_obj_c[0][1]
            print("aa ab",A_a,A_b)
        i = 0

        A[0,0] = 1
        A[0,1] = 0
        A[1,1] = 1
        A[1,0] = 0
        A[2,0] = 0
        A[2,1] = 0
        A[0,2] = -np.sin(math.radians(sup_angle))
        A[1,2] = np.cos(math.radians(sup_angle))
        A[2,2] = A_a*np.cos(math.radians(sup_angle)) + A_b*np.sin(math.radians(sup_angle))

        moment = 0
        for M in M_mag:
            moment +=M

        for force in force_c:
            force_x = force_mag[i] * np.sin(np.radians(force_angle[i]))
            force_y = force_mag[i] * np.cos(np.radians(force_angle[i]))
            if sup_obj_ind[0] == 1:
                moment -= (force[0] - sup_obj_c[0][0]) * force_y - (force[1] - sup_obj_c[0][1]) * force_x
            elif sup_obj_ind[1] == 1:
                moment -= (force[0] - sup_obj_c[1][0]) * force_y - (force[1] - sup_obj_c[1][1]) * force_x
            i += 1
        i = 0
        for linear in force_linear:
            if sup_obj_c[0][0] < sup_obj_c[1][0] and ay_lin:
                moment -= (ay_lin[i] - sup_obj_c[0][0]) * linear_mag_y[i]
            elif sup_obj_c[0][0] > sup_obj_c[1][0] and ay_lin:
                moment -= (ay_lin[i] - sup_obj_c[1][0]) * linear_mag_y[i]
            if sup_obj_c[0][1] < sup_obj_c[1][1] and ax_lin:
                moment -= (ax_lin[i] - sup_obj_c[0][1]) * linear_mag_x[i]
            elif sup_obj_c[0][1] > sup_obj_c[1][1] and ax_lin:
                moment -= (ax_lin[i] - sup_obj_c[1][1]) * linear_mag_x[i]
            i += 1

        b[2] = -moment
    i = 0
    if sup_index == 3:
        A[0, 0] = 1
        A[0, 1] = 0
        A[0, 2] = 0
        A[1, 0] = 0
        A[1, 1] = 1
        A[1, 2] = 0
        A[2, 0] = 0
        A[2, 1] = 0
        A[2, 2] = 1

        moment = 0
        for M in M_mag:
            moment += M
        for force in force_c:
            force_x = force_mag[i] * np.sin(np.radians(force_angle[i]))
            force_y = force_mag[i] * np.cos(np.radians(force_angle[i]))
            moment -= (force[0] - sup_obj_c[0][0]) * force_y + (force[1] - sup_obj_c[0][1]) * force_x
            i += 1
        i = 0
        for linear in force_linear:
            moment -= (ay_lin[i] - sup_obj_c[0][0]) * linear_mag_y[i]
            i += 1

        b[2] = -moment

    print("A", A)
    print("b", b)
    x = np.linalg.solve(A, b)
    x = [round(element, 5) for element in x]
    print("X ",x)

    #if sup_angle>0 and sup_angle <180:
        #x[2] *=-1
    print("sup_angle",sup_angle)
    for idx,seg in enumerate(R_seg):
        if R_seg[idx] == "sup1":
            R_seg[idx] = x[1]
            R_x_seg[idx] = x[0]
        elif R_seg[idx] == "sup2":
            R_seg[idx] = round(x[2] * math.cos(math.radians(sup_angle)),5)
            R_x_seg[idx] = round(-x[2] * math.sin(math.radians(sup_angle)),5)

    print("R_segggg",R_seg,R_x_seg)
    R_usekov = [0] * (len(filtered))
    R_x_usekov = [0] * (len(filtered))
    R_x_usekov_ver = [0] * (len(filtered_ver))
    fil_ver = filtered_ver


    for i, support in enumerate(sup_obj_c):
        position_x = support[0]
        position_y = support[1]
        sup_ind = sup_obj_ind[i]
        for k in range(len(lines_sorted)):
            start, end, beam_type, direction = lines_sorted[k]
            start_x_b, start_y_b = start
            end_x_b, end_y_b = end
            # Identifikácia typu podpory
            if sup_ind == 1:
                # Rotational support
                reaction_force_x = x[0]
                reaction_force_y = x[1]
            elif sup_ind == 2:
                # Rotational sliding support
                reaction_force_y = round(x[2] * math.cos(math.radians(sup_angle)),5)
                reaction_force_x = round(-x[2] * math.sin(math.radians(sup_angle)),5)
            elif sup_ind == 3:
                # Fully constrained support
                reaction_force_x = x[0]
                reaction_force_y = x[1]
                reaction_moment = x[2]

            if lines_sorted[k][3] == "up":
                fil_ver = filtered_ver_up
                fil_ver.reverse()
            elif lines_sorted[k][3] == "down":
                fil_ver = filtered_ver
            # Priradenie k vertikálnemu prútu
            for j in range(len(fil_ver) - 1):
                start_y = fil_ver[j]
                end_y = fil_ver[j + 1]

                # Kontrola, či podpora patrí k vertikálnemu prútu
                if start_y == position_y:
                    if start_x_b == position_x == end_x_b:
                        if sup_ind != 3:
                            # Reakčné sily pre rotacnú podporu na vertikálnom prúte
                            if lines_sorted[k][3] == "up":
                                R_usekov_ver[j] -= reaction_force_x
                                R_x_usekov_ver[j] -= reaction_force_y
                            else:
                                R_usekov_ver[j] += reaction_force_x
                                R_x_usekov_ver[j] += reaction_force_y
                            reaction_force_x = 0
                        elif sup_ind == 3:
                            # Pridanie momentu, ak existuje
                            R_usekov_ver[j] += reaction_force_y
                            R_x_usekov_ver[j] += reaction_force_x
                            M_usekov[j] += reaction_moment
                        if end_y == position_y:
                            R_usekov_ver[j] += reaction_force_y
                            M_usekov[j] -= reaction_moment

            # Priradenie k horizontálnemu prútu
            for j in range(len(filtered) - 1):
                start_x = filtered[j]
                end_x = filtered[j + 1]

                # Kontrola, či podpora patrí k horizontálnemu prútu
                if start_x == position_x:
                    if start_y_b == position_y == end_y_b:
                        if sup_ind != 3:
                            # Reakčné sily pre posuvnú podporu na horizontálnom prúte
                            R_usekov[j] += reaction_force_y
                            R_x_usekov[j] += reaction_force_x
                            reaction_force_x = 0
                        elif sup_ind == 3:
                            # Pridanie momentu, ak existuje
                            R_usekov[j] += reaction_force_y
                            R_x_usekov[j] += reaction_force_x
                            M_usekov[j] += reaction_moment
                        if end_x == position_x:
                            R_usekov[j] += reaction_force_y
                            M_usekov[j] -= reaction_moment

    N_all = []
    T_all = []
    M_all = []
    x_all = []
    x_coords = []
    B = 0
    C = 0
    D = 0

    N_all_ver = []
    T_all_ver = []
    M_all_ver = []
    y_all = []
    y_coords = []
    B_y = 0
    C_y = 0
    D_y = 0

    new_i = 0
    hor_idx = 0
    ver_idx = 0
    start_graph_hor = 0
    start_graph_ver = 0

    x_offset = 0
    y_offset = 0

    num_beams_hor = len(calc_points["horizontal"])
    num_beams_ver = len(calc_points["vertical"])
    num_beams = num_beams_hor + num_beams_ver

    fig, axs = plt.subplots(3, num_beams, figsize=(16, 16))

    for k in range(len(lines_sorted)):
        if hor_idx<len(unique_hor):
            beam_seg_hor = unique_hor[hor_idx]
        if ver_idx<len(unique_ver):
            beam_seg_ver = unique_ver[ver_idx]
        if lines_sorted[k][2] == "horizontal":
            hor_idx +=1
            # Výpočet pre jednotlivé úseky
            if N_all_ver and T_all_ver and M_all_ver and lines_sorted[k-1][2]=="vertical" and k>0:
                if lines_sorted[k][3] == "right" and lines_sorted[k-1][3] == "up":
                    C = -N_all_ver[-1][-1]
                    B = T_all_ver[-1][-1]
                elif lines_sorted[k][3] == "right" and lines_sorted[k-1][3] == "down":
                    C = N_all_ver[-1][-1]
                    B = -T_all_ver[-1][-1]
                else:
                    C = N_all_ver[-1][-1]
                D = M_all_ver[-1][-1]

            elif N_all and T_all and M_all and lines_sorted[k-1][2]=="horizontal":
                C = T_all[-1][-1]
                B = N_all[-1][-1]
                D = M_all[-1][-1]
                print("11111111111",C,B,D)
            for i in range(len(beam_seg_hor) - 1):
                print("new hor i",new_i,i)
                start_x = beam_seg_hor[i]
                if i < len(beam_seg_hor):
                    end_x = beam_seg_hor[i+1]
                else:
                    end_x = beam_seg_hor[-1]
                if lines_sorted[k][3] == "right" and lines_sorted[k - 1][3] == "up" and k>0:
                    q = q_seg[i + new_i]
                    B += R_x_seg[i + new_i]
                    B -= F_x_seg[i + new_i]
                    C += R_seg[i + new_i]
                    C += F_seg[i + new_i]
                    D -= M_seg[i + new_i]
                elif lines_sorted[k][3] == "right" and lines_sorted[k - 1][3] == "down" and k>0:
                    q = q_seg[i + new_i]
                    B += R_x_seg[i + new_i]
                    B += F_x_seg[i + new_i]
                    C += R_seg[i + new_i]
                    C += F_seg[i + new_i]
                    D -= M_seg[i + new_i]
                else:
                    q = q_seg[i + new_i]
                    B -= R_x_seg[i + new_i]
                    B -= F_x_seg[i + new_i]
                    C += R_seg[i + new_i]
                    C += F_seg[i + new_i]
                    D -= M_seg[i + new_i]


                x = np.linspace(start_x, end_x, 100)
                x_calc = np.linspace(0, (end_x - start_x), 100)
                N = np.full_like(x_calc, B)
                T = -q * x_calc + C  # Výpočet napätia
                M = -q * (x_calc ** 2) / 2 + C * x_calc + D

                x_graph = np.linspace(x_offset, (end_x - start_x) + x_offset, 100)
                x_offset = x_graph[-1]

                # Uložíme hodnoty pre graf
                N_all.append(N)
                T_all.append(T)
                M_all.append(M)
                x_all.append(x_graph)
                x_coords.append(x)

                # Hodnota M na konci aktuálneho úseku sa stáva D pre ďalší úsek
                B = N_all[-1][-1]
                C = T_all[-1][-1]
                D = M_all[-1][-1]
                print("B,C,D", B, C, D)


            if len(lines_sorted) != 1:
                # Horizontálne úseky
                for i in range(start_graph_hor,len(T_all)):
                    axs[0, k].plot(x_all[i], T_all[i], label=f'Úsek {i + 1} (T) - Horizontálny')
                axs[0, k].set_xlabel('Pozícia x')
                axs[0, k].set_ylabel('Napätie T')
                #axs[0, k].set_title('Graf napätia T po horizontálnych úsekoch')
                axs[0, k].legend()
                axs[0, k].grid(True)

                for i in range(start_graph_hor,len(M_all)):
                    axs[1, k].plot(x_all[i], M_all[i], label=f'Úsek {i + 1} (M) - Horizontálny')
                axs[1, k].set_xlabel('Pozícia x')
                axs[1, k].set_ylabel('Moment M')
                #axs[1, k].set_title('Graf momentu M po horizontálnych úsekoch')
                axs[1, k].legend()
                axs[1, k].grid(True)

                for i in range(start_graph_hor,len(N_all)):
                    axs[2, k].plot(x_all[i], N_all[i], label=f'Úsek {i + 1} (N) - Horizontálny')
                axs[2, k].set_xlabel('Pozícia x')
                axs[2, k].set_ylabel('Normálová sila N')
                #axs[2, k].set_title('Graf normálovej sily N po horizontálnych úsekoch')
                axs[2, k].legend()
                axs[2, k].grid(True)

                start_graph_hor = len(T_all)
            else:
                # Graf pre napätie T
                for i in range(start_graph_hor, len(T_all)):
                    axs[0].plot(x_all[i], T_all[i], label=f'Úsek {i + 1} (T) - Horizontálny')
                axs[0].set_xlabel("Pozícia x")
                axs[0].set_ylabel("Napätie T")
               # axs[0].set_title("Horizontálny prút - Napätie T")
                axs[0].legend()
                axs[0].grid(True)

                # Graf pre moment M
                for i in range(start_graph_hor, len(M_all)):
                    axs[1].plot(x_all[i], M_all[i], label=f'Úsek {i + 1} (M) - Horizontálny', color="orange")
                axs[1].set_xlabel("Pozícia x")
                axs[1].set_ylabel("Moment M")
                #axs[1].set_title("Horizontálny prút - Moment M")
                axs[1].legend()
                axs[1].grid(True)

                # Graf pre normálovú silu N
                for i in range(start_graph_hor, len(N_all)):
                    axs[2].plot(x_all[i], N_all[i], label=f'Úsek {i + 1} (N) - Horizontálny', color="green")
                axs[2].set_xlabel("Pozícia x")
                axs[2].set_ylabel("Normálová sila N")
                #axs[2].set_title("Horizontálny prút - Normálová sila N")
                axs[2].legend()
                axs[2].grid(True)

            new_i += len(beam_seg_hor) - 1

        elif lines_sorted[k][2] == "vertical":
            if N_all and T_all and M_all and lines_sorted[k-1][2]=="horizontal":
                if lines_sorted[k][3] == "down" and lines_sorted[k-1][3] == "right" and k>0:
                    C_y = -N_all[-1][-1]
                    B_y = T_all[-1][-1]
                    D_y = M_all[-1][-1]
                elif lines_sorted[k][3] == "up" and lines_sorted[k-1][3] == "right" and k>0:
                    C_y = N_all[-1][-1]
                    B_y = -T_all[-1][-1]
                    D_y = M_all[-1][-1]

                print("C_y",C_y)
                print("B_y", B_y)
                print("C", C)
                print("B", B)
                print("D_y", D_y)

            for i in range(len(beam_seg_ver) - 1):
                start_y = beam_seg_ver[i]
                if i < len(beam_seg_ver):
                    end_y = beam_seg_ver[i + 1]
                else:
                    end_y = beam_seg_ver[-1]


                temp_start = lines_sorted[k][1]
                temp_end = lines_sorted[k][0]
                temp_lenght = abs(temp_start[1] - temp_end[1])

                if lines_sorted[k][3] == "up":
                    q = -q_seg[i + new_i]
                    C_y -= F_x_seg[i + new_i]
                    C_y -= R_x_seg[i + new_i]
                    B_y -= F_seg[i + new_i]
                    B_y -= R_seg[i + new_i]
                else:
                    q = q_seg[i + new_i]
                    C_y += F_x_seg[i + new_i]
                    C_y += R_x_seg[i + new_i]
                    B_y += F_seg[i + new_i]
                    B_y += R_seg[i + new_i]
                D_y -= M_seg[i + new_i]

                # Výpočet normálovej sily (N_y), smykovej sily (T_y) a momentu (M_y) vo vertikálnom prúte
                y = np.linspace(start_y, end_y, 100)
                y_calc = np.linspace(0, abs(end_y - start_y), 100)

                if lines_sorted[k][3] == "up":
                    y_calc = y_calc[::-1]

                N_y = np.full_like(y_calc, B_y)
                T_y = -q * y_calc + C_y
                M_y = -q * (y_calc ** 2) / 2 + C_y * y_calc + D_y  # Moment


                y_graph = np.linspace(y_offset, abs(end_y-start_y) + y_offset, 100)
                y_offset = y_graph[-1]

                if lines_sorted[k][3] == "up":
                    M_y = M_y[::-1]
                    T_y = T_y[::-1]
                    N_y = N_y[::-1]

                # Uloženie výsledkov pre grafy
                N_all_ver.append(N_y)
                T_all_ver.append(T_y)
                M_all_ver.append(M_y)
                y_all.append(y_graph)
                y_coords.append(y)

                # Aktualizácia konštánt pre ďalší úsek
                C_y = T_all_ver[-1][-1]
                B_y = N_all_ver[-1][-1]
                D_y = M_all_ver[-1][-1]


            if len(lines_sorted) != 1:
                # Vertikálne úseky (pravý stĺpec)
                for i in range(start_graph_ver,len(T_all_ver)):
                    axs[0, k].plot(y_all[i], T_all_ver[i], label=f'Úsek {i + 1} (T) - Vertikálny')
                axs[0, k].set_xlabel('Pozícia y')
                axs[0, k].set_ylabel('Napätie T')
                #axs[0, k].set_title('Graf napätia T po vertikálnych úsekoch')
                axs[0, k].legend()
                axs[0, k].grid(True)

                for i in range(start_graph_ver,len(M_all_ver)):
                    axs[1, k].plot(y_all[i], M_all_ver[i], label=f'Úsek {i + 1} (M) - Vertikálny')
                axs[1, k].set_xlabel('Pozícia y')
                axs[1, k].set_ylabel('Moment M')
                #axs[1, k].set_title('Graf momentu M po vertikálnych úsekoch')
                axs[1, k].legend()
                axs[1, k].grid(True)

                for i in range(start_graph_ver,len(N_all_ver)):
                    axs[2, k].plot(y_all[i], N_all_ver[i], label=f'Úsek {i + 1} (N) - Vertikálny')
                axs[2, k].set_xlabel('Pozícia y')
                axs[2, k].set_ylabel('Normálová sila N')
                #axs[2, k].set_title('Graf normálovej sily N po vertikálnych úsekoch')
                axs[2, k].legend()
                axs[2, k].grid(True)

                start_graph_ver = len(y_all)

            else:
                # Graf pre napätie T (vertikálny prút)
                for i in range(start_graph_ver, len(T_all_ver)):
                    axs[0].plot(y_all[i], T_all_ver[i], label=f'Úsek {i + 1} (T) - Vertikálny')
                axs[0].set_xlabel("Pozícia y")
                axs[0].set_ylabel("Napätie T")
                #axs[0].set_title("Vertikálny prút - Napätie T")
                axs[0].legend()
                axs[0].grid(True)

                # Graf pre moment M (vertikálny prút)
                for i in range(start_graph_ver, len(M_all_ver)):
                    axs[1].plot(y_all[i], M_all_ver[i], label=f'Úsek {i + 1} (M) - Vertikálny', color="orange")
                axs[1].set_xlabel("Pozícia y")
                axs[1].set_ylabel("Moment M")
                #axs[1].set_title("Vertikálny prút - Moment M")
                axs[1].legend()
                axs[1].grid(True)

                # Graf pre normálovú silu N (vertikálny prút)
                for i in range(start_graph_ver, len(N_all_ver)):
                    axs[2].plot(y_all[i], N_all_ver[i], label=f'Úsek {i + 1} (N) - Vertikálny', color="green")
                axs[2].set_xlabel("Pozícia y")
                axs[2].set_ylabel("Normálová sila N")
                #axs[2].set_title("Vertikálny prút - Normálová sila N")
                axs[2].legend()
                axs[2].grid(True)

            new_i += len(beam_seg_ver) - 1

    with open('data.txt', 'w') as file:
        file.write(f"pocet_usekov: {pocet_usekov}\n")

        # Dĺžky úsekov
        file.write("dlzky_usekov:\n")
        for i, dlzka in enumerate(dlzky_usekov, start=1):
            file.write(f"  dlzka_useku_{i}: {dlzka}\n")

        # q pre každý úsek
        file.write("q_useky:\n")
        for i, q in enumerate(q_usekov, start=1):
            file.write(f"  q_usek_{i}: {q}\n")

        # Sily pre každý úsek
        file.write("F_useky:\n")
        for i, F in enumerate(F_usekov, start=1):
            file.write(f"  F_usek_{i}: {F}\n")

        file.write(f"  Sila na konci: {F_end}\n")

        file.write("F_x_useky:\n")
        for i, F in enumerate(F_x_usekov, start=1):
            file.write(f"  F_x_usek_{i}: {F}\n")

        file.write("Sily v podporach:\n")
        file.write(f"  FAx: {x[0]}\n")
        file.write(f"  FAy: {x[1]}\n")
        file.write(f"  FB: {x[2]}\n")

        file.write("R_useky:\n")
        for i, F in enumerate(R_usekov, start=1):
            file.write(f"  R_usek_{i}: {F}\n")

        file.write("Rx_useky:\n")
        for i, F in enumerate(R_x_usekov, start=1):
            file.write(f"  Rx_usek_{i}: {F}\n")

        file.write("M_useky:\n")
        for i, F in enumerate(M_usekov, start=1):
            file.write(f"  M_usek_{i}: {F}\n")

        file.write(f"pocet_usekov: {len(filtered_ver)-1}\n")

        # q pre každý úsek
        file.write("q_useky:\n")
        for i, q in enumerate(q_usekov_ver, start=1):
            file.write(f"  q_usek_{i}: {q}\n")

        # Sily pre každý úsek
        file.write("F_useky:\n")
        for i, F in enumerate(F_usekov_ver, start=1):
            file.write(f"  F_usek_{i}: {F}\n")

        file.write(f"  Sila na konci: {F_end_ver}\n")

        file.write("F_x_useky:\n")
        for i, F in enumerate(F_x_usekov_ver, start=1):
            file.write(f"  F_x_usek_{i}: {F}\n")

        file.write("R_useky:\n")
        for i, F in enumerate(R_usekov_ver, start=1):
            file.write(f"  R_usek_{i}: {F}\n")

        file.write("M_useky:\n")
        for i, F in enumerate(M_usekov_ver, start=1):
            file.write(f"  M_usek_{i}: {F}\n")

    plt.tight_layout()
    plt.show()

def graph():
    global lines,T_all,M_all,N_all,T_all_ver,M_all_ver,N_all_ver,x_coords,y_coords,lines_sorted,canvas,sup_angle,calc_points,support_image_dict

    print(lines_sorted)
    if T_all:
        T_all = [[x * -1 for x in sublist] for sublist in T_all]
        M_all = [[x * -1 for x in sublist] for sublist in M_all]
        N_all = [[x * -1 for x in sublist] for sublist in N_all]
    if T_all_ver:
        T_all_ver = [[x * -1 for x in sublist] for sublist in T_all_ver]
        M_all_ver = [[x * -1 for x in sublist] for sublist in M_all_ver]
        N_all_ver = [[x * -1 for x in sublist] for sublist in N_all_ver]

    x2_old = None
    y2_old = None
    line_counter = 0
    support_images_refs = []

    # Vytvorenie nového okna
    window_graph = customtkinter.CTk()
    window_graph.geometry("1280x720")
    window_graph.title("Graph Window")

    # Nastavenie mriežky pre okno (window_graph)
    window_graph.grid_rowconfigure(0, weight=1)
    window_graph.grid_rowconfigure(1, weight=1)
    window_graph.grid_columnconfigure(0, weight=1)
    window_graph.grid_columnconfigure(1, weight=1)

    # Vytvorenie 4 plátien s menšou veľkosťou (môžeš upraviť podľa potreby)
    graph_canvas = Canvas(window_graph, bg="white", width=2500, height=2500)
    graph_canvas.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    graph_canvas_M = Canvas(window_graph, bg="white", width=2500, height=2500)
    graph_canvas_M.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    graph_canvas_N = Canvas(window_graph, bg="white", width=2500, height=2500)
    graph_canvas_N.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

    graph_canvas_O = Canvas(window_graph, bg="white", width=2500, height=2500)
    graph_canvas_O.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)


    def setup_canvas_zoom(canvas):
        canvas.canvas_center_x = 0
        canvas.canvas_center_y = 0
        canvas.bind("<MouseWheel>", on_mousewheel)
        canvas.bind("<Configure>", on_configure)

    def on_mousewheel(event):
        canvas = event.widget
        if event.delta > 0:
            zoom(canvas, 1.1)
        else:
            zoom(canvas, 0.9)

    def on_configure(event):
        canvas = event.widget
        canvas.canvas_center_x = event.width / 2
        canvas.canvas_center_y = event.height / 2
        center_objects_on_canvas(canvas)

    def zoom(canvas, factor):
        cx = canvas.canvas_center_x
        cy = canvas.canvas_center_y
        canvas.scale("all", cx, cy, factor, factor)
        canvas.configure(scrollregion=canvas.bbox("all"))
        center_objects_on_canvas(canvas)

    def center_objects_on_canvas(canvas):
        bbox = canvas.bbox("all")
        if not bbox:
            return
        obj_center_x = (bbox[0] + bbox[2]) / 2
        obj_center_y = (bbox[1] + bbox[3]) / 2
        offset_x = canvas.canvas_center_x - obj_center_x
        offset_y = canvas.canvas_center_y - obj_center_y
        canvas.move("all", offset_x, offset_y)

    def scale_values_abs(values, new_max):
        old_max = np.max(np.abs(values))
        if old_max == 0:
            return np.zeros_like(values)
        return (values / old_max) * new_max

    items = canvas.find_all()

    for item in items:
        item_type = canvas.type(item)  # Typ objektu (line, rectangle, oval, text, image, ...)
        coords = canvas.coords(item)  # Súradnice objektu
        options = canvas.itemconfig(item)  # Vlastnosti objektu

        if item_type == "line":
            # Skopírovanie vlastností čiary
            width = options["width"][-1]
            fill = options["fill"][-1]
            arrow = options["arrow"][-1]
            dash = options["dash"][-1]
            capstyle = options["capstyle"][-1]
            # Ak si niekde v pôvodnom kóde nastavoval aj arrowshape, prevezmeme ho
            arrowshape = options["arrowshape"][-1] if "arrowshape" in options else None

            graph_canvas_O.create_line(
                coords,
                fill=fill,
                width=width,
                arrow=arrow,
                dash=dash,
                capstyle=capstyle,
                arrowshape=arrowshape  # zachovanie tvaru šípky
            )

        elif item_type == "rectangle":
            fill = options["fill"][-1]
            outline = options["outline"][-1]
            graph_canvas_O.create_rectangle(coords, fill=fill, outline=outline)

        elif item_type == "oval":
            fill = options["fill"][-1]
            outline = options["outline"][-1]
            graph_canvas_O.create_oval(coords, fill=fill, outline=outline)

        elif item_type == "text":
            text_value = options["text"][-1]
            font_value = options["font"][-1]
            fill_value = options["fill"][-1]
            # Pre CustomTkinter vytvorený text s rotáciou:
            angle = options["angle"][-1] if "angle" in options else 0
            graph_canvas_O.create_text(
                coords,
                text=text_value,
                font=font_value,
                fill=fill_value,
                angle=angle  # Tento parameter zabezpečí rotáciu textu
            )
        elif item_type == "arc":
            fill = options["fill"][-1]
            outline = options["outline"][-1]
            width = options["width"][-1]
            style = options["style"][-1] if "style" in options else "arc"
            start = float(options["start"][-1]) if "start" in options else 0
            extent = float(options["extent"][-1]) if "extent" in options else 90

            graph_canvas_O.create_arc(
                coords,
                fill=fill,
                outline=outline,
                width=width,
                style=style,
                start=start,
                extent=extent
            )

    for canvas in [graph_canvas, graph_canvas_M, graph_canvas_N, graph_canvas_O]:
        setup_canvas_zoom(canvas)

    if T_all:
        T_all = scale_values_abs(T_all, 70)
        M_all = scale_values_abs(M_all, 70)
        N_all = scale_values_abs(N_all, 70)
    if T_all_ver:
        T_all_ver = scale_values_abs(T_all_ver, 70)
        M_all_ver = scale_values_abs(M_all_ver, 70)
        N_all_ver = scale_values_abs(N_all_ver, 70)

    hor_offset = 0
    ver_offset = 0
    # Nakreslenie čiar na plátno

    for k in range(len(lines_sorted)):
        graph_canvas.create_line(lines_sorted[k][0], lines_sorted[k][1], fill="black", width=4)
        stop = False

        if lines_sorted[k][2] == "horizontal":
            useky_x = 0  # inicializujeme počet prútov pre tento segment
            for rod in range(len(T_all)):  # Pre každý "prút"
                if stop:
                    break
                # Použijeme lokálny index = rod + hor_offset pre prístup k T_all a x_coords
                for i in range(len(T_all[rod + hor_offset]) - 1):  # Pre každý úsek v danom prúte
                    if T_all[rod + hor_offset][i] > 0:
                        color = "red"
                    elif T_all[rod + hor_offset][i] < 0:
                        color = "blue"
                    else:
                        color = "black"
                    x1 = float(x_coords[rod + hor_offset][i])
                    y1 = float(T_all[rod + hor_offset][i]) + lines_sorted[k][0][1]
                    x2 = float(x_coords[rod + hor_offset][i + 1])
                    y2 = float(T_all[rod + hor_offset][i + 1]) + lines_sorted[k][1][1]
                    if i == 0:
                        graph_canvas.create_line(x1, lines_sorted[k][0][1], x1,
                                                 float(T_all[rod + hor_offset][i]) + lines_sorted[k][0][1], fill=color,
                                                 width=2)
                    if i == len(T_all[rod + hor_offset]) - 2:
                        graph_canvas.create_line(x2, lines_sorted[k][0][1], x2,
                                                 float(T_all[rod + hor_offset][-1]) + lines_sorted[k][0][1], fill=color,
                                                 width=2)
                    if x2 >= lines_sorted[k][1][0]:
                        stop = True
                        break
                    if x2_old is not None:
                        graph_canvas.create_line(x2, y2, x2_old, y2_old, fill=color, width=2)
                        x2_old = None
                        y2_old = None
                    if line_counter == 15:
                        graph_canvas.create_line(x1, lines_sorted[k][0][1], x1,
                                                 float(T_all[rod + hor_offset][i]) + lines_sorted[k][0][1], fill=color,
                                                 width=2)
                        line_counter = 0
                    graph_canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
                    line_counter += 1
                if rod != len(T_all) - 1:
                    x2_old = x2
                    y2_old = y2
                useky_x += 1  # Po každom "prúte" zvýš počet
            # Po spracovaní všetkých prútov v tomto segmente posunieme hor_offset
            hor_offset = useky_x

        elif lines_sorted[k][2] == "vertical":
            useky_y = 0  # Inicializujeme počet prútov pre tento vertikálny segment
            for rod in range(len(T_all_ver)):  # Pre každý "prút"
                actual_index = rod + ver_offset
                # Kontrola, či máme dáta pre daný index
                if actual_index >= len(T_all_ver) or actual_index >= len(y_coords):
                    break

                stop = False
                for i in range(len(T_all_ver[actual_index]) - 1):  # Pre každý úsek v danom prúte
                    if T_all_ver[actual_index][i] > 0:
                        color = "red"
                    elif T_all_ver[actual_index][i] < 0:
                        color = "blue"
                    else:
                        color = "black"

                    y1 = float(y_coords[actual_index][i])  # y súradnice z y_coords
                    x1 = float(T_all_ver[actual_index][i]) + lines_sorted[k][0][
                        0]  # x súradnice posunuté podľa T_all_ver a segmentu
                    y2 = float(y_coords[actual_index][i + 1])
                    x2 = float(T_all_ver[actual_index][i + 1]) + lines_sorted[k][1][0]

                    if i == 0:
                        graph_canvas.create_line(lines_sorted[k][0][0], y1,
                                                 float(T_all_ver[actual_index][i]) + lines_sorted[k][0][0],
                                                 y1, fill=color, width=2)
                    if i == len(T_all_ver) - 2:
                        graph_canvas.create_line(lines_sorted[k][0][0], y2,
                                                 float(T_all_ver[actual_index][-1]) + lines_sorted[k][0][0],
                                                 y2, fill=color, width=2)

                    if y2 >= lines_sorted[k][1][1]:
                        stop = True
                        break

                    if x2_old is not None:
                        graph_canvas.create_line(x2, y2, x2_old, y2_old, fill=color, width=2)
                        x2_old = None
                        y2_old = None

                    if line_counter == 15:
                        graph_canvas.create_line(lines_sorted[k][0][0], y1,
                                                 float(T_all_ver[actual_index][i]) + lines_sorted[k][0][0],
                                                 y1, fill=color, width=2)
                        line_counter = 0

                    graph_canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
                    line_counter += 1

                # (Voliteľné) Kreslíme začiatkovú spojovaciu čiaru, ak potrebuješ – len pre prvý prút a prvý segment
                if rod == 0 and k == 0:
                    ix = rod + ver_offset
                    if ix >= len(y_coords):
                        ix = len(y_coords) - 1
                    graph_canvas.create_line(
                        float(y_coords[ix][0]),
                        lines_sorted[k][0][0],
                        float(y_coords[ix][0]),
                        float(T_all_ver[ix][0]) + lines_sorted[k][0][0],
                        fill=color, width=2
                    )
                if rod != len(T_all_ver) - 1:
                    x2_old = x2
                    y2_old = y2

                useky_y += 1  # Zvýšime počet prútov pre tento segment
            ver_offset = useky_y  # Aktualizujeme globálny offset pre vertikálne dáta až po spracovaní celého segmentu

        x1 = None
        y1 = None
        x2 = None
        y2 = None
        x2_old = None
        y2_old = None

    hor_offset = 0
    useky_x = 0
    ver_offset = 0
    useky_y = 0
    line_counter = 0
    x2_old = None
    y2_old = None

    for k in range(len(lines_sorted)):
        graph_canvas_M.create_line(lines_sorted[k][0], lines_sorted[k][1], fill="black", width=4)
        stop = False

        if lines_sorted[k][2] == "horizontal":
            local_useky_x = 0  # Lokálny počet prútov pre tento segment
            for rod in range(len(M_all)):  # Pre každý "prút"
                actual_index = rod + hor_offset
                if actual_index >= len(M_all) or actual_index >= len(x_coords):
                    break

                if stop:
                    #graph_canvas_M.create_line(x2, lines_sorted[k][0][1], x2, y1, fill=color, width=2)
                    break

                for i in range(len(M_all[actual_index]) - 1):  # Pre každý úsek v danom prúte
                    if M_all[actual_index][i] > 0:
                        color = "red"
                    elif M_all[actual_index][i] < 0:
                        color = "blue"
                    else:
                        color = "black"
                    x1 = float(x_coords[actual_index][i])
                    y1 = float(M_all[actual_index][i]) + lines_sorted[k][0][1]
                    x2 = float(x_coords[actual_index][i + 1])
                    y2 = float(M_all[actual_index][i + 1]) + lines_sorted[k][1][1]
                    if i == 0:
                        graph_canvas_M.create_line(x1, lines_sorted[k][0][1], x1,
                                                   float(M_all[actual_index][0]) + lines_sorted[k][0][1], fill=color,
                                                   width=2)
                    if x2 >= lines_sorted[k][1][0]:
                        stop = True
                        break
                    if x2_old is not None:
                        graph_canvas_M.create_line(x2, y2, x2_old, y2_old, fill=color, width=2)
                        x2_old = None
                        y2_old = None
                    if line_counter == 15:
                        graph_canvas_M.create_line(x1, lines_sorted[k][0][1], x1,
                                                   float(M_all[actual_index][i]) + lines_sorted[k][0][1], fill=color,
                                                   width=2)
                        line_counter = 0
                    graph_canvas_M.create_line(x1, y1, x2, y2, fill=color, width=2)
                    line_counter += 1

                if rod != len(M_all) - 1:
                    x2_old = x2
                    y2_old = y2
                local_useky_x += 1  # Zvýšime počet prútov pre tento segment
            hor_offset = local_useky_x  # Aktualizujeme globálny offset až po spracovaní celého horizontálneho segmentu

        elif lines_sorted[k][2] == "vertical":
            local_useky_y = 0  # Lokálny počet prútov pre vertikálny segment
            for rod in range(len(M_all_ver)):  # Pre každý "prút"
                actual_index = rod + ver_offset
                if actual_index >= len(M_all_ver) or actual_index >= len(y_coords):
                    break

                local_useky_y += 1
                if stop:
                    graph_canvas_M.create_line(y2, lines_sorted[k][1][1], y2, x1, fill=color, width=2)
                    break
                for i in range(len(M_all_ver[actual_index]) - 1):  # Pre každý úsek v danom prúte
                    if M_all_ver[actual_index][i] > 0:
                        color = "red"
                    elif M_all_ver[actual_index][i] < 0:
                        color = "blue"
                    else:
                        color = "black"
                    y1 = float(y_coords[actual_index][i])
                    x1 = float(M_all_ver[actual_index][i]) + lines_sorted[k][0][0]
                    y2 = float(y_coords[actual_index][i + 1])
                    x2 = float(M_all_ver[actual_index][i + 1]) + lines_sorted[k][1][0]
                    if i == 0:
                        graph_canvas_M.create_line(lines_sorted[k][0][0], y1,
                                                   float(M_all_ver[actual_index][i]) + lines_sorted[k][0][0], y1,
                                                   fill=color, width=2)
                    if i == len(M_all_ver) - 2:
                        graph_canvas_M.create_line(lines_sorted[k][0][0], y2,
                                                   float(M_all_ver[actual_index][-1]) + lines_sorted[k][0][0], y2,
                                                   fill=color, width=2)
                    if y2 >= lines_sorted[k][1][1]:
                        stop = True
                        break
                    if x2_old is not None:
                        graph_canvas_M.create_line(x2, y2, x2_old, y2_old, fill=color, width=2)
                        x2_old = None
                        y2_old = None
                    if line_counter == 15:
                        graph_canvas_M.create_line(lines_sorted[k][0][0], y1,
                                                   float(M_all_ver[actual_index][i]) + lines_sorted[k][0][0], y1,
                                                   fill=color, width=2)
                        line_counter = 0
                    graph_canvas_M.create_line(x1, y1, x2, y2, fill=color, width=2)
                    line_counter += 1
                # Voliteľne: kreslenie spojovacej čiary pre prvý prút v segmente (ak potrebuješ)
                if rod == 0 and k == 0:
                    if rod == 0 and k == 0:
                        ix = actual_index
                        if ix >= len(y_coords):
                            ix = len(y_coords) - 1

                        start_y = float(y_coords[ix][0])
                        base_x = lines_sorted[k][0][0]
                        M_x = float(M_all_ver[ix][0]) + base_x

                        graph_canvas_M.create_line(
                            base_x, start_y,
                            M_x, start_y,
                            fill=color,
                            width=2
                        )
                if rod != len(M_all_ver) - 1:
                    x2_old = x2
                    y2_old = y2
            ver_offset = local_useky_y  # Aktualizujeme globálny offset pre vertikálne dáta

    hor_offset = 0
    useky_x = 0
    ver_offset = 0
    useky_y = 0
    line_counter = 0
    x2_old = None
    y2_old = None

    for k in range(len(lines_sorted)):
        graph_canvas_N.create_line(lines_sorted[k][0],lines_sorted[k][1], fill="black", width=4)
        stop = False

        if lines_sorted[k][2] == "horizontal":
            for rod in range(len(N_all)):  # Pre každý "prút"
                useky_x += 1
                if stop:
                    graph_canvas_N.create_line(x2, lines_sorted[k][0][1], x2, y1,fill=color, width=2)
                    break
                for i in range(len(N_all[rod + hor_offset]) - 1):  # Pre každý usek v danom prúte
                    if N_all[rod + hor_offset][i]>0:
                        color = "red"
                    elif N_all[rod + hor_offset][i]<0:
                        color = "blue"
                    else:
                        color = "black"
                    x1 = float(x_coords[rod + hor_offset][i])
                    y1 = float(N_all[rod + hor_offset][i]) + lines_sorted[k][0][1]
                    x2 = float(x_coords[rod + hor_offset][i + 1])
                    y2 = float(N_all[rod + hor_offset][i + 1]) + lines_sorted[k][1][1]
                    if i == 0:
                        graph_canvas_N.create_line(x1, lines_sorted[k][0][1], x1,
                                                   float(N_all[rod + hor_offset][i]) + lines_sorted[k][0][1],
                                                   fill=color, width=2)
                    if i == len(N_all) - 2:
                        graph_canvas_N.create_line(x2, lines_sorted[k][0][1], x2,
                                                   float(N_all[rod + hor_offset][-1]) + lines_sorted[k][0][1],
                                                   fill=color, width=2)

                    if x2 >= lines_sorted[k][1][0]:
                        stop = True
                        hor_offset = useky_x
                        break
                    if x2_old is not None:
                        graph_canvas_N.create_line(x2, y2, x2_old, y2_old, fill=color, width=2)
                        x2_old = None
                        y2_old = None
                    if line_counter == 15:
                        graph_canvas_N.create_line(x1, lines_sorted[k][0][1], x1, float(N_all[rod + hor_offset][i]) + lines_sorted[k][0][1], fill=color, width=2)
                        line_counter = 0
                    graph_canvas_N.create_line(x1, y1, x2, y2, fill=color, width=2)
                    line_counter +=1
                if rod == 0 and k ==0:
                    print("s")
                    #graph_canvas_N.create_line(float(x_coords[rod + hor_offset][0]), lines_sorted[k][0][1], float(x_coords[rod + hor_offset][0]),float(N_all[rod + hor_offset][0]) + lines_sorted[k][0][1], fill=color, width=2)
                if rod != len(N_all)-1:
                    x2_old = x2
                    y2_old = y2

        elif lines_sorted[k][2] == "vertical":
            for rod in range(len(N_all_ver)):  # Pre každý "prút"
                useky_y+=1
                if stop:
                    graph_canvas_N.create_line(y2, lines_sorted[k][1][1], y2, x1,fill=color, width=2)
                    break
                for i in range(len(N_all_ver[rod + ver_offset]) - 1):  # Pre každý úsek v danom prúte
                    if N_all_ver[rod + ver_offset][i]>0:
                        color = "red"
                    elif N_all_ver[rod + ver_offset][i]<0:
                        color = "blue"
                    else:
                        color = "black"
                    y1 = float(y_coords[rod + ver_offset][i])  # Namiesto x_coords teraz y_coords
                    x1 = float(N_all_ver[rod + ver_offset][i]) + lines_sorted[k][0][0]  # Použiť správnu os
                    y2 = float(y_coords[rod + ver_offset][i + 1])
                    x2 = float(N_all_ver[rod + ver_offset][i + 1]) + lines_sorted[k][1][0]
                    if i == 0:
                        graph_canvas_N.create_line(lines_sorted[k][0][0], y1,
                                                   float(N_all_ver[rod + ver_offset][i]) + lines_sorted[k][0][0], y1,
                                                   fill=color, width=2)
                    if i == len(N_all_ver) - 2:
                        graph_canvas_N.create_line(lines_sorted[k][0][0], y2,
                                                   float(N_all_ver[rod + ver_offset][-1]) + lines_sorted[k][0][0], y2,
                                                   fill=color, width=2)
                    if y2 >= lines_sorted[k][1][1]:
                        stop = True
                        ver_offset = useky_y
                        break
                    if x2_old is not None:
                        graph_canvas_N.create_line(x2, y2, x2_old, y2_old, fill=color, width=2)
                        x2_old = None
                        y2_old = None
                    if line_counter == 15:
                        graph_canvas_N.create_line(lines_sorted[k][0][0], y1, float(N_all_ver[rod + ver_offset][i]) + lines_sorted[k][0][0],y1, fill=color, width=2)
                        line_counter = 0
                    graph_canvas_N.create_line(x1, y1, x2, y2, fill=color, width=2)
                    line_counter += 1
                if rod == 0 and k == 0:
                    print("s")
                    #graph_canvas_N.create_line(float(y_coords[rod + ver_offset][0]), lines_sorted[k][0][0], float(y_coords[rod + ver_offset][0]),float(N_all_ver[rod + ver_offset][0]) + lines_sorted[k][0][0], fill=color, width=2)
                if rod != len(N_all_ver) - 1:
                    x2_old = x2
                    y2_old = y2

    label_T = Label(window_graph, text="T", font=("Arial", 20, "bold"), bg="white")
    label_T.place(relx=0.75, rely=0.05)

    label_M = Label(window_graph, text="M", font=("Arial", 20, "bold"), bg="white")
    label_M.place(relx=0.25, rely=0.55)

    label_N = Label(window_graph, text="N", font=("Arial", 20, "bold"), bg="white")
    label_N.place(relx=0.75, rely=0.55)

    for segment in calc_points.get('horizontal', []) + calc_points.get('vertical', []):

        for i, support_coord in enumerate(segment['supports']):

            support_index = segment['supports_index'][i]

            if support_index not in support_image_dict:
                try:
                    image_path = f"image/sup{support_index}.jpg"
                    image = Image.open(image_path)
                    resized = image.resize((45, 45))
                    if support_index == 2:
                        angle = sup_angle  # pretože sup_angle je len jedno číslo
                        rotated = resized.rotate(angle, expand=True)
                        photo = ImageTk.PhotoImage(rotated, master=window_graph)
                    else:
                        photo = ImageTk.PhotoImage(resized, master=window_graph)
                    support_image_dict[support_index] = photo
                    support_images_refs.append(photo)  # ulož, aby nebol zmazaný
                except Exception as e:
                    print(f"Chyba pri načítaní obrázku pre support {support_index}: {e}")
                    continue

            sup_x, sup_y = support_coord
            sup_graph = graph_canvas_O.create_image(sup_x, sup_y, image=support_image_dict[support_index], anchor="center")
            graph_canvas_O.tag_lower(sup_graph)


    # Priradenie udalosti myšového kolieska k plátnu
    graph_canvas.bind("<MouseWheel>", on_mousewheel)
    graph_canvas.bind("<Configure>", on_configure)
    graph_canvas_M.bind("<MouseWheel>", on_mousewheel)
    graph_canvas_M.bind("<Configure>", on_configure)
    graph_canvas_N.bind("<MouseWheel>", on_mousewheel)
    graph_canvas_N.bind("<Configure>", on_configure)
    graph_canvas_O.bind("<MouseWheel>", on_mousewheel)
    graph_canvas_O.bind("<Configure>", on_configure)

    window.destroy()
    # Spustenie cyklu udalostí
    window_graph.mainloop()




#buttons in tool_frame
button1 = customtkinter.CTkButton(tool_frame1, image=support1, text="", command=sup1)
button1.pack(padx=5, pady=5, ipady=10)
button2 = customtkinter.CTkButton(tool_frame1, image=support2, text="", command=sup2)
button2.pack(padx=5, pady=5, ipady=10)
button3 = customtkinter.CTkButton(tool_frame1, image=support3, text="", command=sup3)
button3.pack(padx=5, pady=5, ipady=10)
button4 = customtkinter.CTkButton(tool_frame1, image=support4, text="", command=sup4)
button4.pack(padx=5, pady=5, ipady=10)
button5 = customtkinter.CTkButton(tool_frame1, image=support5, text="", command=sup5)
button5.pack(padx=5, pady=5, ipady=10)

button9 = customtkinter.CTkButton(tool_frame2, image=line, text="", command=enable_line_drawing)
button9.pack(padx=5, pady=5, ipady=10)
button10 = customtkinter.CTkButton(tool_frame2, image=arc_1, text="", command=arc1)
button10.pack(padx=5, pady=5, ipady=10)
button12 = customtkinter.CTkButton(tool_frame2, image=arc_2, text="", command=arc2)
button12.pack(padx=5, pady=5, ipady=10)
button13 = customtkinter.CTkButton(tool_frame2, image=arc_3, text="", command=arc3)
button13.pack(padx=5, pady=5, ipady=10)
button14 = customtkinter.CTkButton(tool_frame2, image=arc_4, text="", command=arc4)
button14.pack(padx=5, pady=5, ipady=10)

button12 = customtkinter.CTkButton(tool_frame3, image=force, text="", command=force1)
button12.pack(padx=5, pady=5, ipady=10)
button13 = customtkinter.CTkButton(tool_frame3, image=linear_force, text="", command=force2)
button13.pack(padx=5, pady=5, ipady=10)
button14 = customtkinter.CTkButton(tool_frame3, image=moment_image, text="", command=place_moment_window)
button14.pack(padx=5, pady=5, ipady=10)

#buttons in menu
button_menu1 = customtkinter.CTkButton(menu_frame, text="", image = calculate, width= 150, command = calc)
button_menu1.grid(row=0, column=0, padx = 5, pady = 5, ipady = 10)
button_menu2 = customtkinter.CTkButton(menu_frame, text="", image = save, command=save_canvas, width= 150)
button_menu2.grid(row=0, column=1, padx = 5, pady = 5, ipady = 10)
button_menu3 = customtkinter.CTkButton(menu_frame, text="",image = change_dimension, width= 150, command=change_dim_line)
button_menu3.grid(row=0, column=2, padx = 5, pady = 5, ipady = 10)
button_menu4 = customtkinter.CTkButton(menu_frame, text="podpory", command=Zmen2, width= 150)
button_menu4.grid(row=0, column=7, padx = 5, pady = 5, ipady = 10)
button_menu5 = customtkinter.CTkButton(menu_frame, text="", image = beam_image,command=Zmen1, width= 150)
button_menu5.grid(row=0, column=5, padx = 5, pady = 5, ipady = 10)
button_menu6 = customtkinter.CTkButton(menu_frame, text="sily a momenty", command=Zmen3, width= 150)
button_menu6.grid(row=0, column=6, padx = 5, pady = 5, ipady = 10)
button_menu7 = customtkinter.CTkButton(menu_frame, text="", image = select_image, command=bind_select, width= 150)
button_menu7.grid(row=0, column=3, padx = 5, pady = 5, ipady = 10)
button_menu8 = customtkinter.CTkButton(menu_frame, text="", image = move_image, width= 150)
button_menu8.grid(row=0, column=4, padx = 5, pady = 5, ipady = 10)

#AR buttons
button_AR1 = customtkinter.CTkButton(ar_frame, text="", image = undo_image,width= 10, height= 15, command=graph)
button_AR1.grid(row=0, column=0, padx = 5, pady = 5, ipady = 10)
button_AR2 = customtkinter.CTkButton(ar_frame, text="", image = redo_image,width= 10, height= 15, command=redo)
button_AR2.grid(row=0, column=1, padx = 5, pady = 5, ipady = 10)
button_AR3 = customtkinter.CTkButton(ar_frame, text="", image = delete_image,width= 10, height= 15, command=clear_canvas)
button_AR3.grid(row=0, column=2, padx = 5, pady = 5, ipady = 10)

#nacitanie platnaf
load_canvas()

window.bind("<Escape>", lambda event: deselect_line())
window.bind("<Control-s>", lambda event: save_canvas())
window.bind('c', lambda event: change_dim_line())
window.bind("<Control-z>", lambda event: undo())
window.bind("<Control-y>", lambda event: redo())
window.bind('l', lambda event: enable_line_drawing())


window.mainloop()
