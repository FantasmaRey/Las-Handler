import numpy as np
import laspy as lp
import pptk
import tkinter as tk
from tkinter import filedialog
import pylas

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen

clrcheck = None
class MainMenu(Screen):

    def fileimport(self):
        global clrcheck
        clrcheck = 0
        root = tk.Tk()
        root.withdraw()
        # то что происходит в окне. открытие через проводник файл
        global input_path
        input_path = filedialog.askopenfilename()
        point_cloud = lp.read(input_path)
        # points = np.vstack((point_cloud.x, point_cloud.y, point_cloud.z)).transpose()
        # point_cloud = lp.file.File(input_path, mode="r")

        with pylas.open(input_path) as fh:
            print('Points from Header:', fh.header.point_count)
            global las
            las = fh.read()
            print(las)
        # # библиотека LasPy также дает структуру point_cloud переменной,
        # # и мы можем использовать простые методы для получения, например, полей X, Y, Z, Red, Blue и Green.
        self.label_wid.text = str(las)
        # # Выделение облака точек
        # selection = v.get('selected')

    def export(self):
        point_cloud = lp.read(input_path)
        points = np.vstack((point_cloud.x, point_cloud.y, point_cloud.z)).transpose()
        # сохранения .las файла в .txt  координаты
        if clrcheck == 0:
            np.savetxt('test.txt', points, fmt='%s')
        else:
            np.savetxt('test.txt', points_cleared, fmt='%s')


    def vizual(self):
        point_cloud = lp.read(input_path)
        points = np.vstack((point_cloud.x, point_cloud.y, point_cloud.z)).transpose()
        colors = np.vstack((point_cloud.red, point_cloud.green, point_cloud.blue)).transpose()
        v = pptk.viewer(points)
        #v.attributes(colors / 65535)
        v.set(point_size=0.001, bg_color=[0, 0, 0, 0], show_axis=1,
                show_grid=1)
        return v

    pass



class Clear(Screen):

    def clear(self):
        global clrcheck
        clrcheck = 1
        point_cloud = lp.read(input_path)
        # очистка по оси Z
        global points_cleared
        points = np.vstack((point_cloud.x, point_cloud.y, point_cloud.z)).transpose()
        points = np.delete(points, points[:, 2] > float(self.max_Z.text), 0)
        points = np.delete(points, points[:, 2] < float(self.min_Z.text), 0)
        # очистка по оси y
        points = np.delete(points, points[:, 1] < float(self.min_Y.text), 0)
        points = np.delete(points, points[:, 1] > float(self.max_Y.text), 0)
        points_cleared = points
        v = pptk.viewer(points)
        #v.attributes(colors / 65535)
        v.set(point_size=0.001, bg_color=[0, 0, 0, 0], show_axis=1, show_grid=1)
        return v

        print('cleared')
    pass

class Docs(Screen):

    pass

class my(App):
    def build(self):
        self.title = 'Las Handler'
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(Clear(name='clear'))
        sm.add_widget(Docs(name='docs'))
        return sm

if __name__ == '__main__':
    my().run()