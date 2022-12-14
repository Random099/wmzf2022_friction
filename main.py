import matplotlib.pyplot as plt
import matplotlib.widgets as wgs
import numpy as np
import math


class Plots:
    def __init__(self, x, y, plot_title, x_label, y_label): #Default plot
        self.x = x
        self.y = y
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(13.5, 7)
        self.fig.subplots_adjust(left=0.225)
        self.line, = plt.plot(self.x, self.y)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.set_title(plot_title)
        self.ax.set_xticks(x)
        self.ax.grid()
        self.error_box = self.fig.text(0.025, 0.025, '', fontsize=11) #Object displaying feedback messages
        self.elements = {} #Dict holding references to the elements on the plot

    def createTextbox(self, element_name, title, initial_text, bottom=0.57, width=0.12, height=0.05, left=0.02): #Adds a text box object to the plot
        box_ax = plt.axes([left, bottom, width, height])
        label = box_ax.text(0, 1.1, title)
        self.elements[element_name] = wgs.TextBox(box_ax, '', initial=initial_text, textalignment='center')

    def createRadio(self, element_name, title, bottom=0.9, width=0.12, height=0.1, left=0.02, color='white', **kwargs): #Adds a radio button object to the plot
        radio_ax = plt.axes([left, bottom, width, height], facecolor=color)
        label = radio_ax.text(0, 1.1, title)
        self.elements[element_name] = wgs.RadioButtons(radio_ax, kwargs['buttons'])

    def setY(self, factor): #For testing purposes
        try:
            self.line.set_ydata(self.y * float(factor))
        except:
            Plots.errorBoxFailure(self.error_box, 'Input has to be float')
        else:
            Plots.errorBoxSuccess(self.error_box, 'Data updated')
            self.fig.canvas.draw()

    def setAxisY(self, new_y):
        self.line.set_ydata(new_y)
        self.fig.canvas.draw()

    @staticmethod
    def errorBoxFailure(error_box, message):
        error_box.set_text(message)
        error_box.set_color('red')
        error_box.set_bbox(dict(facecolor='none', edgecolor='red'))

    @staticmethod
    def errorBoxSuccess(error_box, message):
        error_box.set_text(message)
        error_box.set_color('black')
        error_box.set_bbox(dict(facecolor='none', edgecolor='none'))


class Friction(Plots):
    def __init__(self, x, angle, coefficient, plot_title='Friction', x_label='time[s]', y_label='V(t)[m/s]'): #Default friction plot
        y = Friction.calculateVelocity(Friction.inclinedPlaneAcceleration(angle, coefficient), x)
        Plots.__init__(self, x, y, plot_title, x_label, y_label)
        self.angle = angle
        self.coefficient = coefficient

    @staticmethod
    def inclinedPlaneAcceleration(angle, coefficient):
        g = float(9.8067)
        return (g * math.sin(angle)) - (coefficient * g * math.cos(angle))

    @staticmethod
    def calculateVelocity(acceleration, time):
        return acceleration * time

    def setAngle(self, new_angle): #Updates angle of the inclined plane
        try:
            self.angle = float(new_angle)
        except:
            Friction.errorBoxFailure(self.error_box, 'Input has to be float')
        else:
            Friction.errorBoxSuccess(self.error_box, 'Data updated')
            self.setAxisY(Friction.calculateVelocity(Friction.inclinedPlaneAcceleration(self.angle, self.coefficient),
                                          self.x))

    def setFrictionCoefficient(self, new_friction_coefficient): #Updates friction coefficient
        try:
            self.coefficient = float(new_friction_coefficient)
        except:
            Friction.errorBoxFailure(self.error_box, 'Input has to be float')
        else:
            Friction.errorBoxSuccess(self.error_box, 'Data updated')
            self.setAxisY(Friction.calculateVelocity(Friction.inclinedPlaneAcceleration(self.angle, self.coefficient),
                                          self.x))

if __name__ == '__main__':
    time = np.arange(0, 21)
    friction_plot = Friction(time, 30, 0.1)

    friction_plot.createTextbox('acceleration_input', 'Set Y: ', '0', 0.55)
    friction_plot.createTextbox('incline_angle', 'Angle[degrees]: ', '0', 0.45)
    friction_plot.createRadio('surface_radio', 'Surface type: ', 0.8, buttons=('Concrete', 'Wood'))
    friction_plot.createRadio('condition_radio', 'Surface condition: ', 0.65, buttons=('Dry', 'Wet'))

    friction_plot.elements['acceleration_input'].on_submit(friction_plot.setY)
    friction_plot.elements['incline_angle'].on_submit(friction_plot.setAngle)

    plt.show()