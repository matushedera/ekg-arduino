import serial
import time
import keyboard
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# change the parameters as needed
FRAMES = 3 # number of frames to be rocorded
WINDOW = 200 # number of datapoints in one frame

# removes plot decorations
def setupAxis(ax):
	ax.spines['left'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.axes.get_yaxis().set_visible(False)
	ax.set_xticklabels([])


if __name__ == '__main__':

	ys = [ 512 ] * WINDOW # intialise with centered line
	fig, ax = plt.subplots()
	ln, = ax.plot(ys, 'r-', animated=True)

	setupAxis(ax)

	plt.ylim(0, 1024) # device data range is <0, 1024>
	plt.show(block=False)
	plt.pause(0.1)

	bg = fig.canvas.copy_from_bbox(fig.bbox)
	ax.draw_artist(ln)
	fig.canvas.blit(fig.bbox)


	#NOTE device is system dependent
	ser = serial.Serial('/dev/ttyACM0', 9600)

	data = 0
	counter = 0
	frame = 0
	ys_new = [] # accumulates ys before saving each record

	while True:

		counter = ( counter + 1 ) % WINDOW

		if keyboard.is_pressed('q'):
			break

		if keyboard.is_pressed('r'):
			frame = FRAMES

		if frame>0 and counter%WINDOW == 0:
			frame -= 1
			ys_new.extend(ys)

			if frame == 0:
				fig_new, ax_new = plt.subplots()
				ax_new.plot(ys_new, 'r-')
				setupAxis(ax_new)

				# interpolate to reduce noise
				spline = make_interp_spline([_ for _ in range(WINDOW*FRAMES)], ys_new, k=3)
				ys_new = spline([_ for _ in range(WINDOW*FRAMES)])

				fig_new.savefig('frame.pdf', dpi=300)
				ys_new = []

		# read data from serial device
		data = ser.readline()
		ln, = ax.plot(ys, 'r-', animated=True)
		try:
			data = data.decode().strip()
			if data == '!': # signal is corrupted
				data = 512
				ln, = ax.plot(ys, 'b-', animated=True)
			data = int(data)
		except:
			data = 512

		fig.canvas.restore_region(bg)

		ys.append(data)
		ys = ys[-WINDOW:] # only take the last window of data
		ln.set_ydata(ys)
		ax.draw_artist(ln)
		fig.canvas.blit(fig.bbox)
		fig.canvas.flush_events()
