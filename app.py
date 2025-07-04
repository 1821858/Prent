from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from plyer import filechooser
import os
import sys
from ArgParse import create_parser
from Main import render

class EffectApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.file_path = None

        # File chooser trigger
        self.choose_button = Button(text="📁 Choose File", size_hint=(1, 0.1))
        self.choose_button.bind(on_press=self.open_file_chooser)
        self.add_widget(self.choose_button)

        # Label to show selected file
        self.file_label = Label(text="No file selected", size_hint=(1, 0.1))
        self.add_widget(self.file_label)

        # Effect spinner
        self.effect_spinner = Spinner(
            text='Choose Effect',
            values=('polygonize', 'cartoon', 'sketch', 'reduce', 'red_view'),
            size_hint=(1, 0.1)
        )
        self.add_widget(self.effect_spinner)

        # Apply button
        self.apply_button = Button(text="Apply Effect", size_hint=(1, 0.1))
        self.apply_button.bind(on_press=self.apply_effect)
        self.add_widget(self.apply_button)

        # Status label
        self.status_label = Label(text="Ready", size_hint=(1, 0.1))
        self.add_widget(self.status_label)

    def open_file_chooser(self, instance):
        filechooser.open_file(on_selection=self.file_selected)

    def file_selected(self, selection):
        if selection:
            self.file_path = selection[0]
            self.file_label.text = f"Selected: {os.path.basename(self.file_path)}"
        else:
            self.file_label.text = "No file selected"

    def apply_effect(self, instance):
        import sys
        from ArgParse import create_parser
        from Main import render

        if not self.file_path:
            self.status_label.text = "No file selected"
            return

        effect = self.effect_spinner.text
        if effect not in self.effect_spinner.values:
            self.status_label.text = "Please choose an effect"
            return

        self.status_label.text = "Processing..."

        try:
            original_argv = sys.argv
            sys.argv = [
                "Main.py",
                self.file_path,
                effect,
                "--num_colors", "8",
                "--num_polygons", "100"
            ]

            parser = create_parser()
            args = parser.parse_args()
            sys.argv = original_argv

            render(args)
            self.status_label.text = "Processing complete"
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"

class MyApp(App):
    def build(self):
        return EffectApp()

if __name__ == '__main__':
    MyApp().run()