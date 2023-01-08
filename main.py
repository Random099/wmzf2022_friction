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
    def error_box_failure(error_box, message: str):
        error_box.set_text(message)
        error_box.set_color('red')
        error_box.set_bbox(dict(facecolor='none', edgecolor='red'))

    @staticmethod
    def error_box_success(error_box, message: str):
        error_box.set_text(message)
        error_box.set_color('black')
        error_box.set_bbox(dict(facecolor='none', edgecolor='none'))

    @staticmethod
    def s_round(number, base=5) -> float:
        return base * np.round(number / base)

    def create_textbox(self, element_name: str, title: str, initial_text: str, bottom=0.57, width=0.12, height=0.05, left=0.02): #Adds a text box object to the plot
        box_ax = plt.axes([left, bottom, width, height])
        box_ax.text(0, 1.1, title)
        self.elements[element_name] = wgs.TextBox(box_ax, '', initial=initial_text, textalignment='center')

    def create_radio(self, element_name: str, title: str, bottom=0.9, width=0.12, height=0.1, left=0.02, color='white', buttons=()): #Adds a radio button object to the plot
        radio_ax = plt.axes([left, bottom, width, height], facecolor=color)
        radio_ax.text(0, 1.1, title)
        self.elements[element_name] = wgs.RadioButtons(radio_ax, buttons)

    def create_button(self, element_name: str, button_text: str, bottom=0.9, width=0.12, height=0.05, left=0.02): #Adds a button object to the plot
        radio_ax = plt.axes([left, bottom, width, height])
        self.elements[element_name] = wgs.Button(radio_ax, button_text)

    def set_axis_x(self, new_x):
        self.x = new_x
        self.line.set_data([], [])
        self.line, = self.ax.plot(self.x, self.y, self.line_color)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def set_axis_y(self, new_y):
        self.y = new_y
        self.line.set_data([], [])
        self.line, = self.ax.plot(self.x, self.y, self.line_color)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def save_plot(self, file_name: str):
        try:
            print(os.listdir())
            if file_name+'.png' in os.listdir():
                raise OSError('File already exists.')
        except OSError as err:
            Plots.error_box_failure(self.error_box, str(err))
        except (Exception, ):
            Plots.error_box_failure(self.error_box, 'Failed to save plot.')
        else:
            self.fig.savefig(file_name)
            Plots.error_box_success(self.error_box, 'Plot successfully saved.')


class Friction(Plots):
    g = float(9.8067)
    surface_types = ['concrete', 'asphalt', 'basalt slab', 'dirt road']
    surface_conditions = ['dry', 'wet']
    coefficient_values = [0.7, 0.9, 0.45, 0.75, 0.4, 0.65, 0.35, 0.55]

    def __init__(self, x, angle: float, coefficient: float, plot_title='Friction', x_label='time[s]', y_label='Velocity(t)[m/s]'): #Default friction plot
        self.plot_type = 1
        self.angle = angle
        self.coefficient = coefficient
        y = self.get_acceleration() * x
        Plots.__init__(self, x, y, plot_title, x_label, y_label, line_color='green')
        self.coefficient_choice = ['', '']

    @staticmethod
    def get_coefficient_dict() -> dict:
        coefficient_list = [s_condition + ' ' + s_type for s_condition in Friction.surface_conditions for s_type in Friction.surface_types]
        return dict(zip(coefficient_list, Friction.coefficient_values))

    def get_acceleration(self) -> float:
        return (Friction.g * math.sin(np.radians(self.angle))) - \
               (self.coefficient * Friction.g * math.cos(np.radians(self.angle)))

    def set_plot_type(self, new_plot_type: str):
        plot_type_dict = {'Velocity(t)[m/s]': 1, 'Distance(t)[m]': 2}
        self.plot_type = plot_type_dict[new_plot_type]
        self.ax.set_ylabel(new_plot_type)
        if self.plot_type == 1:
            self.set_axis_y(self.get_acceleration() * self.x)
        elif self.plot_type == 2:
            self.set_axis_y(self.get_acceleration() * self.x ** 2)

    def set_axis_y(self, new_y):
        self.y = new_y
        self.line.set_data([], [])
        self.line, = self.ax.plot(np.arange(0, len(self.y[self.y >= 0])), self.y[self.y >= 0], self.line_color)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def set_time(self, new_time):
        self.x = np.arange(0, float(new_time) + 1)
        self.ax.set_xticks(self.x)
        if self.plot_type == 1:
            self.set_axis_y(self.get_acceleration() * self.x)
        elif self.plot_type == 2:
            self.set_axis_y(self.get_acceleration() * self.x ** 2)

    def set_angle(self, new_angle: float): #Updates angle of the inclined plane
        try:
            if float(new_angle) < 0 or float(new_angle) > 90:
                raise Warning('Angle not in range (0-90).')
            self.angle = float(new_angle)
            Friction.error_box_success(self.error_box, 'Data updated.')
            if self.plot_type == 1:
                self.set_axis_y(self.get_acceleration() * self.x)
            elif self.plot_type == 2:
                self.set_axis_y(self.get_acceleration() * self.x ** 2)
        except ValueError:
            Friction.error_box_failure(self.error_box, 'Angle has to be a float value in range 0-90')
        except Warning as err:
            Friction.error_box_failure(self.error_box, str(err))
        assert type(self.angle) == float

    def set_friction_coefficient(self, new_coefficient: float): #Updates friction coefficient
        try:
            if float(new_coefficient) < 0:
                raise Warning('Coefficient cannot be negative.')
            self.coefficient = float(new_coefficient)
            Friction.error_box_success(self.error_box, 'Data updated.')
            if self.plot_type == 1:
                self.set_axis_y(self.get_acceleration() * self.x)
            elif self.plot_type == 2:
                self.set_axis_y(self.get_acceleration() * self.x ** 2)
        except ValueError:
            Friction.error_box_failure(self.error_box, 'Coefficient has to be a non-negative float value')
        assert type(self.coefficient) == float

    def r_set_coefficient(self, label: str): #Handles setting friction coefficient by radio buttons
        if label.lower() in Friction.surface_types:
            self.coefficient_choice[1] = label.lower()
        if label.lower() in Friction.surface_conditions:
            self.coefficient_choice[0] = label.lower()
        if self.coefficient_choice[0] != '' and self.coefficient_choice[1] != '':
            self.coefficient = float(Friction.get_coefficient_dict()[' '.join(self.coefficient_choice)])
            if self.plot_type == 1:
                self.set_axis_y(self.get_acceleration() * self.x)
            elif self.plot_type == 2:
                self.set_axis_y(self.get_acceleration() * self.x**2)
            Friction.error_box_success(self.error_box, 'Data updated')


if __name__ == '__main__':
    time_axis = np.arange(0, 21)
    friction_plot = Friction(time_axis, float(30), float(0.5))

    #Text boxes
    friction_plot.create_textbox('t_duration', 'Duration[s]: ', '20', 0.45)
    friction_plot.create_textbox('t_incline_angle', 'Angle[degrees]: ', '30', 0.35)
    friction_plot.create_textbox('t_friction_coefficient', 'Coefficient: ', '0.5', 0.25)
    friction_plot.create_textbox('t_save_button', 'Save Plot:', 'File name', 0.15)
    #Radio buttons
    friction_plot.create_radio('r_plot_type', 'Plot type: ', 0.85, buttons=('Velocity(t)[m/s]', 'Distance(t)[m]'))
    friction_plot.create_radio('r_surface_radio', 'Surface type: ', 0.7, buttons=('Concrete', 'Asphalt', 'Basalt slab', 'Dirt road'))
    friction_plot.create_radio('r_condition_radio', 'Surface condition: ', 0.55, buttons=('Dry', 'Wet'))
    #Buttons

    #Text boxes' functions
    friction_plot.elements['t_duration'].on_submit(friction_plot.set_time)
    friction_plot.elements['t_incline_angle'].on_submit(friction_plot.set_angle)
    friction_plot.elements['t_save_button'].on_submit(friction_plot.save_plot)
    friction_plot.elements['t_friction_coefficient'].on_submit(friction_plot.set_friction_coefficient)
    #Radio buttons' functions
    friction_plot.elements['r_plot_type'].on_clicked(friction_plot.set_plot_type)
    friction_plot.elements['r_surface_radio'].on_clicked(friction_plot.r_set_coefficient)
    friction_plot.elements['r_condition_radio'].on_clicked(friction_plot.r_set_coefficient)

    #Buttons' functions

    plt.show()