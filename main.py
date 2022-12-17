import matplotlib.pyplot as plt
import matplotlib.widgets as wgs
import numpy as np
import math
import os


class Plots:
    def __init__(self, x, y, plot_title: str, x_label: str, y_label: str, line_color: str): #Default plot
        self.x = x
        self.y = y
        self.line_color = line_color
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot(self.x, self.y, self.line_color)
        self.fig.set_size_inches(13.5, 7)
        self.fig.subplots_adjust(left=0.225)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.set_title(plot_title)
        self.ax.set_xticks(self.x)
        self.ax.grid()
        self.error_box = self.fig.text(0.025, 0.025, '', fontsize=11) #Object displaying feedback message
        self.elements = {} #Dict holding references to the elements on the plot

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

    @staticmethod
    def s_round(number, base=5) -> float:
        return base * np.round(number / base)

    def createTextbox(self, element_name: str, title: str, initial_text: str, bottom=0.57, width=0.12, height=0.05, left=0.02): #Adds a text box object to the plot
        box_ax = plt.axes([left, bottom, width, height])
        box_ax.text(0, 1.1, title)
        self.elements[element_name] = wgs.TextBox(box_ax, '', initial=initial_text, textalignment='center')

    def createRadio(self, element_name: str, title: str, bottom=0.9, width=0.12, height=0.1, left=0.02, color='white', buttons=()): #Adds a radio button object to the plot
        radio_ax = plt.axes([left, bottom, width, height], facecolor=color)
        radio_ax.text(0, 1.1, title)
        self.elements[element_name] = wgs.RadioButtons(radio_ax, buttons)

    def createButton(self, element_name: str, button_text: str, bottom=0.9, width=0.12, height=0.05, left=0.02): #Adds a button object to the plot
        radio_ax = plt.axes([left, bottom, width, height])
        self.elements[element_name] = wgs.Button(radio_ax, button_text)

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
        self.line, = self.ax.plot(self.x, self.y, self.line_color)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def savePlot(self, file_name: str):
        try:
            print(os.listdir())
            if file_name+'.png' in os.listdir():
                raise OSError('File already exists.')
        except OSError as err:
            Plots.errorBoxFailure(self.error_box, str(err))
        except (Exception, ):
            Plots.errorBoxFailure(self.error_box, 'Failed to save plot.')
        else:
            self.fig.savefig(file_name)
            Plots.errorBoxSuccess(self.error_box, 'Plot successfully saved.')


class Friction(Plots):
    g = float(9.8067)
    surface_types = ('concrete', 'asphalt', 'basalt slab', 'dirt road')
    surface_conditions = ('dry', 'wet')
    coefficient_values = [0.7, 0.9, 0.45, 0.75, 0.4, 0.65, 0.35, 0.55]

    def __init__(self, x, angle: float, coefficient: float, plot_title='Friction', x_label='time[s]', y_label='V(t)[m/s]'): #Default friction plot
        y = Friction.calculateVelocity(Friction.inclinedPlaneAcceleration(angle, coefficient), x)
        Plots.__init__(self, x, y, plot_title, x_label, y_label, line_color='green')
        self.angle = angle
        self.coefficient = coefficient
        self.coefficient_choice = ['', '']

    @staticmethod
    def getCoefficientDict() -> dict:
        coefficient_list = [s_condition + ' ' + s_type for s_condition in Friction.surface_conditions for s_type in Friction.surface_types]
        return dict(zip(coefficient_list, Friction.coefficient_values))

    @staticmethod
    def inclinedPlaneAcceleration(angle: float, coefficient: float) -> float:
        return (Friction.g * math.sin(np.radians(angle))) - (coefficient * Friction.g * math.cos(np.radians(angle)))

    @staticmethod
    def calculateVelocity(acceleration: float, time: float) -> float:
        return acceleration * time #XD

    def setAngle(self, new_angle: float): #Updates angle of the inclined plane
        try:
            if float(new_angle) < 0 or float(new_angle) > 90:
                raise Warning('Angle not in range (0-90).')
            self.angle = float(new_angle)
            Friction.errorBoxSuccess(self.error_box, 'Data updated.')
            self.setAxisY(Friction.calculateVelocity(Friction.inclinedPlaneAcceleration(self.angle, self.coefficient),
                                          self.x))
        except ValueError:
            Friction.errorBoxFailure(self.error_box, 'Angle has to be a float value in range 0-90')
        except Warning as err:
            Friction.errorBoxFailure(self.error_box, str(err))
        assert type(self.angle) == float

    def setFrictionCoefficient(self, new_coefficient: float): #Updates friction coefficient
        try:
            if float(new_coefficient) < 0:
                raise Warning('Coefficient must be bigger than 0.')
            self.coefficient = float(new_coefficient)
            Friction.errorBoxSuccess(self.error_box, 'Data updated.')
            self.setAxisY(Friction.calculateVelocity(Friction.inclinedPlaneAcceleration(self.angle, self.coefficient),
                                          self.x))
        except ValueError:
            Friction.errorBoxFailure(self.error_box, 'Coefficient has to be a float value bigger than 0')
        assert type(self.coefficient) == float

    def r_setCoefficient(self, label: str):
        if label in Friction.surface_types:
            self.coefficient_choice[1] = label
        if label in Friction.surface_conditions:
            self.coefficient_choice[0] = label
        if self.coefficient_choice[0] != '' and self.coefficient_choice[1] != '':
            self.coefficient = float(Friction.getCoefficientDict()[' '.join(self.coefficient_choice)])
            self.setAxisY(Friction.calculateVelocity(Friction.inclinedPlaneAcceleration(self.angle, self.coefficient),
                                                     self.x))
            Friction.errorBoxSuccess(self.error_box, 'Data updated')


if __name__ == '__main__':
    time_axis = np.arange(0, 21)
    friction_plot = Friction(time_axis, float(30), float(0.5))

    #Text boxes
    friction_plot.createTextbox('t_acceleration_input', 'Set Y: ', '0', 0.55)
    friction_plot.createTextbox('t_incline_angle', 'Angle[degrees]: ', '30', 0.45)
    friction_plot.createTextbox('t_friction_coefficient', 'Coefficient: ', '0.5', 0.35)
    friction_plot.createTextbox('t_save_button', 'Save Plot:', 'File name', 0.25)
    #Radio buttons
    friction_plot.createRadio('r_surface_radio', 'Surface type: ', 0.8, buttons=('concrete', 'asphalt', 'basalt slab', 'dirt road'))
    friction_plot.createRadio('r_condition_radio', 'Surface condition: ', 0.65, buttons=('dry', 'wet'))
    #Buttons

    #Text boxes' functions
    friction_plot.elements['t_incline_angle'].on_submit(friction_plot.setAngle)
    friction_plot.elements['t_save_button'].on_submit(friction_plot.savePlot)
    friction_plot.elements['t_friction_coefficient'].on_submit(friction_plot.setFrictionCoefficient)
    #Radio buttons' functions
    friction_plot.elements['r_surface_radio'].on_clicked(friction_plot.r_setCoefficient)
    friction_plot.elements['r_condition_radio'].on_clicked(friction_plot.r_setCoefficient)

    #Buttons' functions

    plt.show()