import matplotlib.pyplot as plt
import matplotlib.widgets as wgs
import numpy as np
import math


class Plots:
    def __init__(self, x, y, plot_title: str, x_label: str, y_label: str): #Default plot
        self.x = x
        self.y = y
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot(self.x, self.y)
        self.fig.set_size_inches(13.5, 7)
        self.fig.subplots_adjust(left=0.225)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.set_title(plot_title)
        self.ax.set_xticks(self.x)
        self.ax.grid()
        self.error_box = self.fig.text(0.025, 0.025, '', fontsize=11) #Object displaying feedback message
        print(type(self.error_box))
        self.elements = {} #Dict holding references to the elements on the plot

    def createTextbox(self, element_name: str, title: str, initial_text: str, bottom=0.57, width=0.12, height=0.05, left=0.02): #Adds a text box object to the plot
        box_ax = plt.axes([left, bottom, width, height])
        box_ax.text(0, 1.1, title)
        self.elements[element_name] = wgs.TextBox(box_ax, '', initial=initial_text, textalignment='center')

    def createRadio(self, element_name: str, title: str, bottom=0.9, width=0.12, height=0.1, left=0.02, color='white', buttons=()): #Adds a radio button object to the plot
        radio_ax = plt.axes([left, bottom, width, height], facecolor=color)
        radio_ax.text(0, 1.1, title)
        self.elements[element_name] = wgs.RadioButtons(radio_ax, buttons)

    def setY(self, factor: float): #For testing purposes
        try:
            self.line.set_ydata(self.y * float(factor))
        except:
            Plots.errorBoxFailure(self.error_box, 'Input has to be float')
        else:
            Plots.errorBoxSuccess(self.error_box, 'Data updated')
            self.fig.canvas.draw()

    def setAxisY(self, new_y):
        self.y = new_y
        self.line.set_data([], [])
        self.line, = self.ax.plot(self.x, self.y)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    @staticmethod
    def errorBoxFailure(error_box, message: str):
        error_box.set_text(message)
        error_box.set_color('red')
        error_box.set_bbox(dict(facecolor='none', edgecolor='red'))

    @staticmethod
    def errorBoxSuccess(error_box, message: str):
        error_box.set_text(message)
        error_box.set_color('black')
        error_box.set_bbox(dict(facecolor='none', edgecolor='none'))


class Friction(Plots):
    def __init__(self, x, angle: float, coefficient: float, plot_title='Friction', x_label='time[s]', y_label='V(t)[m/s]'): #Default friction plot
        y = Friction.calculateVelocity(Friction.inclinedPlaneAcceleration(angle, coefficient), x)
        Plots.__init__(self, x, y, plot_title, x_label, y_label)
        self.angle = angle
        self.coefficient = coefficient

    @staticmethod
    def inclinedPlaneAcceleration(angle: float, coefficient: float) -> float:
        g = float(9.8067)
        return (g * math.sin(np.radians(angle))) - (coefficient * g * math.cos(np.radians(angle)))

    @staticmethod
    def calculateVelocity(acceleration: float, time: float) -> float:
        return acceleration * time #XD

    def setAngle(self, new_angle: float): #Updates angle of the inclined plane
        try:
            if not(new_angle.isnumeric()):
                raise TypeError('Angle must be a numeric value 0-90')
            elif float(new_angle) < 0 or float(new_angle) > 90:
                raise Warning('Angle not in range(0-90)')
        except TypeError as err:
            Friction.errorBoxFailure(self.error_box, err)
        except Warning as err:
            Friction.errorBoxFailure(self.error_box, err)
        else:
            self.angle = float(new_angle)
            self.setAxisY(Friction.calculateVelocity(Friction.inclinedPlaneAcceleration(self.angle, self.coefficient),
                                          self.x))
            Friction.errorBoxSuccess(self.error_box, 'Data updated')
        assert type(self.angle) == float

    def setFrictionCoefficient(self, new_friction_coefficient: float): #Updates friction coefficient
        try:
            if not(new_friction_coefficient.isnumeric()):
                raise TypeError('Friction coefficient must be a numeric value')
        except TypeError as err:
            Friction.errorBoxFailure(self.error_box, err)
        else:
            self.coefficient = float(new_friction_coefficient)
            self.setAxisY(Friction.calculateVelocity(Friction.inclinedPlaneAcceleration(self.angle, self.coefficient),
                                          self.x))
            Friction.errorBoxSuccess(self.error_box, 'Data updated')

if __name__ == '__main__':
    time_axis = np.arange(0, 21)
    friction_plot = Friction(time_axis, float(30), float(0.5))

    friction_plot.createTextbox('acceleration_input', 'Set Y: ', '0', 0.55)
    friction_plot.createTextbox('incline_angle', 'Angle[degrees]: ', '30', 0.45)
    friction_plot.createRadio('surface_radio', 'Surface type: ', 0.8, buttons=('Concrete', 'Wood'))
    friction_plot.createRadio('condition_radio', 'Surface condition: ', 0.65, buttons=('Dry', 'Wet'))

    #friction_plot.elements['acceleration_input'].on_submit(friction_plot.setY)
    friction_plot.elements['incline_angle'].on_submit(friction_plot.setAngle)

    plt.show()