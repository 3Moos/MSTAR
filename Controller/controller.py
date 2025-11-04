import tkinter as tk
import time

#This code can/will be used to control the experiment via a pico board. This program will be run on a master computer, and send a start signal to children (three oxygen sensors) who will be listening for a start signal, and return an "echo" when the oxygen sensor is started. The master controller will record times and write it to a csv file.

#This has also been pushed to the github repository.

#Please forward to johnny, and see if he can set up the pico board if I am not available through the week.


class ControllerGUI:
    def __init__(self, master):
        self.timeStart = time.time()
        self.timeStop = None
        self.type = None
        self.master = master
        self.label = tk.Label(master, text="MSTAR Experiment Controller", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.start_button = tk.Button(master, text="Start Experiment", command=self.start_experiment)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(master, text="Stop Experiment", command=self.stop_experiment)
        self.stop_button.pack(pady=10)

    def sendStartSignal(self):
        print("Start signal: attempting send to hardware.")
        #SEND START SIGNAL CODE
        print("Start signal: sent.")

    def start_experiment(self):
        print("Experiment started.", time.time())
        sendStartSignal(self)

    def stop_experiment(self):
        self.timeStop = time.time()
        #truncate to 3 decimal places
        self.timeStop = float(f"{self.timeStop:.3f}")
        print("Experiment duration:", self.timeStop - self.timeStart, "seconds")
        print("Experiment stopped at time", self.timeStop)
       
    def listenForStartSignal(self):
        print("Listening for start signal from hardware...")
        #LISTEN FOR START SIGNAL CODE FROM PICO BOARD
        print("Start signal received from master controller")
        self.start_experiment()
       
    def listenForChildrenEcho(self):
        print("Listening for child echo...")
        #LISTEN FOR CHILD CONTROLLER SIGNALS IF WE HAVE I/O
        print("Child controller signal received.")
       
if __name__ == "__main__":
    root = tk.Tk()
    root.title("MSTAR Experiment Controller")

    tk.Label(root, text="Controller Experiment").pack()

    root.minsize(1280, 720)
    root.geometry("300x300+50+50")
   
    my_gui = ControllerGUI(root)
    root.mainloop()




