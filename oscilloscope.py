from izi_pygame import *
from math import sin
from math import pi
from math import cos
from math import tan
from math import sqrt
import sys
import os
from random import randint

GRID_COLOR = (0, 20, 0)
AXES_COLOR = (0, 200, 0)
CHA_COLOR = (0, 255, 255)
CHB_COLOR = (255, 0, 0)
CHC_COLOR = (255, 255, 0)
FOCUS_COLOR = []

class Signal:

	def __init__(self, amplitude, frequence, phi, font, square_size, tension_ladder, color, ipos):
		self.fontInfo = font
		self.square_size = square_size
		self.tension_ladder = tension_ladder
		self.amplitude = amplitude
		self.frequence = frequence
		self.periode = 0.0
		self.phi = phi
		self.amplitude_info = Printstring(self.fontInfo, str(f"A {self.amplitude} V"), color, ipos, 10)
		self.periode_info = Printstring(self.fontInfo, str(f"T infini s"), color, ipos, 35)
		self.frequence_info = Printstring(self.fontInfo, str(f"f {float(self.frequence):.3} Hz"), color, ipos, 60)
		self.phi_info = Printstring(self.fontInfo, str(f"φ {self.phi}"), color, ipos, 85)
		self.v_t = 0
		FOCUS_COLOR.append(color)

class Oscilloscope:

	command = str()
	def __init__(self, window, square_size=50):
		self.fontInfo = Fontstring(window=window.get_canva(), size=30)
		self.fontGraduation = Fontstring(window=window.get_canva(), size=20)
		self.window = window
		self.square_size = square_size
		self.x_axe = Printstring(self.fontInfo, "t(s)", AXES_COLOR, window.wwidth-40, window.wheight//2-30)
		self.y_axe = Printstring(self.fontInfo, "U(V)", AXES_COLOR, window.wwidth//2+20, 10)
		self.time_ladder = 1
		self.tension_ladder = 5
		self.graduation_info = Printstring(self.fontGraduation, str('1'), AXES_COLOR, 0, 0)
		self.focus = 8 #largeur du signal
		self.signaux = [
		Signal(0, 0, 0, self.fontInfo, square_size, self.tension_ladder, CHA_COLOR, 10), 
		Signal(0, 0, 10, self.fontInfo, square_size, self.tension_ladder, CHB_COLOR, 120),
		Signal(0, 0, -10, self.fontInfo, square_size, self.tension_ladder, CHC_COLOR, 230)
		]
		self.focus_signal_info = Printstring(self.fontInfo, "F", AXES_COLOR, 10, 120)
		self.focus_signal = 0
		self.time_ladder_info = Printstring(self.fontInfo, f"1 square -> {self.time_ladder/self.tension_ladder/4}", AXES_COLOR, 10, 145)
		self.type_signal = ["sin", "cos", "tan"]
		self.tmp = 1
	def print_signal(self, delete=[False, False, False]):
		time = pygame.time.get_ticks()
		for i in range(0, self.window.wwidth, 1):
			
			j = 0
			for s in self.signaux:
				if delete[j]:
					j+=1
					continue
				if self.type_signal[j] == "sin":
					s.v_t = s.amplitude*self.square_size/self.tension_ladder*sin(2*pi*s.frequence*time/1000)-(s.phi*self.square_size/self.tension_ladder)
				elif self.type_signal[j] == "cos":
					s.v_t = s.amplitude*self.square_size/self.tension_ladder*cos(2*pi*s.frequence*time/1000)-(s.phi*self.square_size/self.tension_ladder)
				elif self.type_signal[j] == "tan":
					s.v_t = s.amplitude*self.square_size/self.tension_ladder*tan(2*pi*s.frequence*time/1000)-(s.phi*self.square_size/self.tension_ladder)
				elif self.type_signal[j] == "rec":
					s.v_t = s.square_size/self.tension_ladder*s.amplitude
					if s.periode and not int(time/1000/s.periode % 2) == 0:
						s.v_t = -s.v_t
					s.v_t += -(s.phi*self.square_size/self.tension_ladder)
				j+=1
			
			j = 0
			for s in self.signaux:
				if delete[j]:
					j+=1
					continue
				pygame.draw.line(self.window.get_canva(), FOCUS_COLOR[j], 
					(i,(self.window.wheight//2-self.focus+s.v_t)), (i, self.window.wheight//2+self.focus+s.v_t), 1)
				j+=1

			time+=self.time_ladder


	def print_info(self, info=True):
		if info:
			for s in self.signaux:
				s.amplitude_info.write()
				s.frequence_info.write()
				s.periode_info.write()
				s.phi_info.write()
			self.focus_signal_info.write()
			self.time_ladder_info.write()

	def print_graduation(self, graduation=True):
		if graduation:
			ncase = self.window.wheight//2//self.square_size+1
			for i in range(0, self.window.wheight, self.square_size):
				self.graduation_info.x = self.window.wwidth//2+3
				self.graduation_info.y = i
				ncase -= 1
				self.graduation_info << str(ncase*self.tension_ladder)
				self.graduation_info.write()
			ncase = -self.window.wwidth//2//self.square_size-1


	def print_grid(self, grid=True):
		if grid:
			for i in range(0, self.window.wheight, self.square_size):
				pygame.draw.line(self.window.get_canva(), GRID_COLOR, (0,i), (self.window.wwidth, i), 1)
			for i in range(0, self.window.wwidth, self.square_size):
				pygame.draw.line(self.window.get_canva(), GRID_COLOR, (i,0), (i, self.window.wheight), 1)
			pygame.draw.line(self.window.get_canva(), AXES_COLOR, 
				(self.window.wwidth//2,0), (self.window.wwidth//2, self.window.wheight), 1)
			pygame.draw.line(self.window.get_canva(), AXES_COLOR, 
				(0,self.window.wheight//2), (self.window.wwidth, self.window.wheight//2), 1)
			self.x_axe.write()
			self.y_axe.write()

	def get_term_focus(self, s):
		if self.focus_signal == -1:
			return s
		return self.focus_signal

def print_info(oscilloscope, error):
	os.system("clear")
	print(f"[info] > {error}")
	print("\n[enter a command]\n\n")
	print("focus         -> size of signal")
	print("time          -> div/time")
	print("U             -> div/tension\n")
	print("s <id signal> -> focus a signal")
	print("f             -> frequence of the focus signal")
	print("T             -> periode of the focus signal")
	print("A             -> amplitude of the focus signal")
	print("phi           -> phi of the focus signal")
	print("sin           -> curent signal become a sin")
	print("cos           -> curent signal become a cos")
	print("tan           -> curent signal become a tan")
	print("rec           -> curent signal become a rec")
	if oscilloscope.focus_signal != -1:	
		print(f"\ncurrent signal -> s{int((oscilloscope.focus_signal_info.x-10)//110)}\n")
	else:
		print(f"\ncurrent signal -> None\n")

def stream_oscillo(oscilloscope):

	error = str("no info")
	list_idsignaux = list()
	for i in range(0, len(oscilloscope.signaux), 1):
		list_idsignaux.append(str(i))
	while oscilloscope.command != "end":
		print_info(oscilloscope, error)
		oscilloscope.command = input("> ")
		if oscilloscope.command == 'end':
			continue
		oscilloscope.command = oscilloscope.command.split(' ')
		if oscilloscope.command[0] in  ["sin", "cos", "tan", "rec"]:
			oscilloscope.type_signal[oscilloscope.focus_signal] = oscilloscope.command[0]
			continue
		elif len(oscilloscope.command) != 2:
			error = "command must have an idcmd and a value"
			continue
		try:
			oscilloscope.command[1] = float(oscilloscope.command[1])
		except:
			error = "the value of the focus must be an integer"
			continue
		if "focus" == oscilloscope.command[0]:
			oscilloscope.focus = oscilloscope.command[1]

		elif "time" == oscilloscope.command[0]:
			oscilloscope.time_ladder = oscilloscope.command[1]
			oscilloscope.time_ladder_info << f"1 square -> {oscilloscope.tension_ladder*oscilloscope.time_ladder/100} s"

		elif "U" == oscilloscope.command[0]:
			if oscilloscope.command[1] == 0:
				error = "div/tension must be different of 0"
				continue
			oscilloscope.tension_ladder = oscilloscope.command[1]

		elif "s" == oscilloscope.command[0]:
			if oscilloscope.command[1] in range(0, len(oscilloscope.signaux), 1):
				oscilloscope.focus_signal_info.x = 10+oscilloscope.command[1]*110#sfocus
				oscilloscope.focus_signal = int(oscilloscope.command[1])
			else:
				error = f"the signal number {int(oscilloscope.command[1])} not exists"
				continue
		elif oscilloscope.focus_signal == -1:
			error = "select a signal"
			continue

		elif "f" == oscilloscope.command[0]:
			oscilloscope.signaux[oscilloscope.focus_signal].frequence = oscilloscope.command[1]
			oscilloscope.signaux[oscilloscope.focus_signal].frequence_info << f"f {float(oscilloscope.signaux[oscilloscope.focus_signal].frequence):.3} Hz"
			if oscilloscope.command[1]:
				oscilloscope.signaux[oscilloscope.focus_signal].periode = 1/oscilloscope.signaux[oscilloscope.focus_signal].frequence
				oscilloscope.signaux[oscilloscope.focus_signal].periode_info << f"T {oscilloscope.signaux[oscilloscope.focus_signal].periode:.3} s"
			else:
				oscilloscope.signaux[oscilloscope.focus_signal].periode = 0
				oscilloscope.signaux[oscilloscope.focus_signal].periode_info << "T infini"

		elif "T" == oscilloscope.command[0]:
			oscilloscope.signaux[oscilloscope.focus_signal].periode = oscilloscope.command[1]
			oscilloscope.signaux[oscilloscope.focus_signal].periode_info << f"f {float(oscilloscope.signaux[oscilloscope.focus_signal].periode):.3} s"
			if oscilloscope.command[1]:
				oscilloscope.signaux[oscilloscope.focus_signal].frequence = 1/oscilloscope.signaux[oscilloscope.focus_signal].periode
				oscilloscope.signaux[oscilloscope.focus_signal].frequence_info << f"f {oscilloscope.signaux[oscilloscope.focus_signal].frequence:.3} Hz"
			else:
				oscilloscope.signaux[oscilloscope.focus_signal].frequence = 0
				oscilloscope.signaux[oscilloscope.focus_signal].periode_info << "f 0 Hz"

		elif "A" == oscilloscope.command[0]:
			oscilloscope.signaux[oscilloscope.focus_signal].amplitude = oscilloscope.command[1]
			oscilloscope.signaux[oscilloscope.focus_signal].amplitude_info << f"A {oscilloscope.signaux[oscilloscope.focus_signal].amplitude} V"

		elif "phi" == oscilloscope.command[0]:
			oscilloscope.signaux[oscilloscope.focus_signal].phi = oscilloscope.command[1]
			oscilloscope.signaux[oscilloscope.focus_signal].phi_info << f"φ {oscilloscope.signaux[oscilloscope.focus_signal].phi}"
		
		error = "no info"


	print("press 'Q' or click on the cross from the pygame window to quit the programm")




