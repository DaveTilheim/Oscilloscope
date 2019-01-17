from oscilloscope import *
from threading import Thread

fini = False
temps = pygame.time.Clock()

window = Window(wwidth=1400, wheight=800, wtitle="Oscilloscope")
oscillo = Oscilloscope(window)
#thread
thread_command_line_oscillo_config = Thread(target=lambda:stream_oscillo(oscillo))
thread_command_line_oscillo_config.start()

info = True
get_time = pygame.time.get_ticks
signal = 0
delete_signal = [False, False, False]
stop = False

while not fini:
	signal = int(oscillo.get_term_focus(signal))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			fini = True
			print("enter 'end' to stop the programm\n> ")
		elif event.type == KEYUP:
			if event.key == K_q:
				fini = True
				print("enter 'end' to stop the programm\n> ")
		
		elif event.type == KEYDOWN:
			if event.key == K_RIGHT:
				oscillo.signaux[signal].frequence += 0.1
				oscillo.signaux[signal].frequence_info << f"f {float(oscillo.signaux[signal].frequence):.3} Hz"
				if oscillo.signaux[signal].frequence:
					oscillo.signaux[signal].periode = 1/oscillo.signaux[signal].frequence
					oscillo.signaux[signal].periode_info << f"T {oscillo.signaux[signal].periode:.3} s"
				else:
					oscillo.signaux[signal].periode = 0
					oscillo.signaux[signal].periode_info << "T infini"
			elif event.key == K_LEFT:
				oscillo.signaux[signal].frequence -= 0.1
				oscillo.signaux[signal].frequence_info << f"f {float(oscillo.signaux[signal].frequence):.3} Hz"
				if oscillo.signaux[signal].frequence:
					oscillo.signaux[signal].periode = 1/oscillo.signaux[signal].frequence
					oscillo.signaux[signal].periode_info << f"T {oscillo.signaux[signal].periode:.3} s"
				else:
					oscillo.signaux[signal].periode = 0
					oscillo.signaux[signal].periode_info << "T infini"
			
			elif event.key == K_UP:
				oscillo.signaux[signal].amplitude += 1
				oscillo.signaux[signal].amplitude_info << f"A {oscillo.signaux[signal].amplitude} V"
			elif event.key == K_DOWN:
				oscillo.signaux[signal].amplitude -= 1
				oscillo.signaux[signal].amplitude_info << f"A {oscillo.signaux[signal].amplitude} V"
			
			elif event.key == K_p:
				oscillo.signaux[signal].phi += 1
				oscillo.signaux[signal].phi_info << f"φ {oscillo.signaux[signal].phi}"
			elif event.key == K_m:
				oscillo.signaux[signal].phi -= 1
				oscillo.signaux[signal].phi_info << f"φ {oscillo.signaux[signal].phi}"
			
			elif event.key == K_s:
				oscillo.type_signal[signal] = "sin"
			elif event.key == K_c:
				oscillo.type_signal[signal] = "cos"
			elif event.key == K_r:
				oscillo.type_signal[signal] = "rec"
			elif event.key == K_t:
				oscillo.type_signal[signal] = "tan"
			
			elif event.key == K_TAB:
				signal += 1
				if signal == len(oscillo.signaux):
					signal = 0
				oscillo.focus_signal_info.x = 10+signal*110
				oscillo.focus_signal = -1
			
			elif event.key == K_o:
				oscillo.tension_ladder += 1
				if oscillo.tension_ladder == 0:
					oscillo.tension_ladder += 1
			elif event.key == K_l:
				oscillo.tension_ladder -= 1
				if oscillo.tension_ladder == 0:
					oscillo.tension_ladder -= 1
			
			elif event.key == K_i:
				info = not info
			
			elif event.key == K_d:
				delete_signal[signal] = not delete_signal[signal]
			
			elif event.key == K_k:
				oscillo.focus += 1
			elif event.key == K_j:
				oscillo.focus -= 1
			
			elif event.key == K_y:
				oscillo.time_ladder += 1
				oscillo.time_ladder_info << f"1 square -> {oscillo.tension_ladder*oscillo.time_ladder/100} s"
			elif event.key == K_h:
				oscillo.time_ladder -= 1
				oscillo.time_ladder_info << f"1 square -> {oscillo.tension_ladder*oscillo.time_ladder/100} s"

			elif event.key == K_RETURN:
				stop = not stop

	if not stop:
		window.fill((0, 100, 0))
		oscillo.print_signal(delete_signal)
		oscillo.print_grid()
		oscillo.print_info(info)
		oscillo.print_graduation()

	temps.tick(60)
	pygame.display.flip()
thread_command_line_oscillo_config.join()
print("exit success")

