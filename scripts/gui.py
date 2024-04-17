import tkinter


class GuiCanvas:
    def __init__(self, inf_canv, image, width=1920, height=1080):
        self.infinite_canvas = inf_canv
        self.master = tkinter.Tk()
        # self.master.attributes("-fullscreen", True)

        self.label = tkinter.Label(self.master, bg='white', width=width, height=height)
        self.label.bind("<Motion>", self.move_mouse)
        self.label.bind("<MouseWheel>", self.scroll)
        self.label.bind("<Configure>", self.resize)

        self.image_for_canvas = image
        self.image = ''
        self.update_image()

    def resize(self, event):
        self.infinite_canvas.change_width_height(self.master.winfo_width(), self.master.winfo_height())
        self.infinite_canvas.stretch_image(self.master.winfo_width(), self.master.winfo_height())

    def move_mouse(self, event):
        # self.infinite_canvas.set_cam_pos(event.x, event.y)
        # self.update_image()
        # print(self.master.winfo_width(), self.master.winfo_height())
        pass

    def scroll(self, event):
        # self.infinite_canvas.set
        print(event.delta)
        event.delta = event.delta
        if event.delta <= -1000:  # CRUTCH
            event.delta = -800
        self.infinite_canvas.set_cam_zoom(self.infinite_canvas.cam_zoom * (1 + event.delta / 1000))
        self.infinite_canvas.set_cam_pos(event.x, event.y)
        self.update_image()

    def update_image(self):
        self.infinite_canvas.generate_image(self.image_for_canvas)
        self.image = self.infinite_canvas.get_tkinter_image()
        self.label.config(image=self.image)
        self.label.pack(fill=tkinter.BOTH, expand=1)
        self.master.update_idletasks()

    def main_loop(self):
        self.master.mainloop()
