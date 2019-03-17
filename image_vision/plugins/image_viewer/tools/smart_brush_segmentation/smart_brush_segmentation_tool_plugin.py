from plugins.image_viewer.tools.image_viewer_tool_plugin import ImageViewerToolPlugin
from plugins.image_viewer.image_viewer_plugin import ImageViewerPlugin
from plugins.window.main import MainWindowPlugin

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDockWidget, QWidget, QFormLayout, QCheckBox, QGroupBox, QRadioButton, QVBoxLayout


class SmartBrushSegmentationToolPlugin(ImageViewerToolPlugin):
    def __init__(self, image_viewer_plugin: ImageViewerPlugin, main_window_plugin: MainWindowPlugin):
        super().__init__(image_viewer_plugin, main_window_plugin,
                         'plugins.image_viewer.tools.smart_brush_segmentation.smart_brush_segmentation_tool',
                         'SmartBrushSegmentationTool', 'Smart Brush', Qt.CTRL + Qt.Key_1)

        self.tool_settings_widget = None

    def activate_tool(self):
        super().activate_tool()

        if not self.tool_settings_widget:
            settings_dock_widget = QDockWidget('Tool Settings')
            self.tool_settings_widget = self.create_tool_settings_widget()
            settings_dock_widget.setWidget(self.tool_settings_widget)

            self.main_window.addDockWidget(Qt.LeftDockWidgetArea, settings_dock_widget)

    def create_tool_settings_widget(self):
        layout = QVBoxLayout()
        layout.addWidget(self.create_cluster_type_group_box())

        form_layout = QFormLayout()
        connected_component_check_box = QCheckBox()
        connected_component_check_box.toggled.connect(self.on_connected_component_check_box_toggled)
        connected_component_check_box.setChecked(True)
        form_layout.addRow('Connected Component', connected_component_check_box)

        layout.addLayout(form_layout)

        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def create_cluster_type_group_box(self):
        central_cluster_radio_button = QRadioButton('Central')
        central_cluster_radio_button.toggled.connect(self.on_central_cluster_radio_button_toggled)
        central_cluster_radio_button.setChecked(True)
        light_cluster_radio_button = QRadioButton('Light')
        light_cluster_radio_button.toggled.connect(self.on_light_cluster_radio_button_toggled)
        dark_cluster_radio_button = QRadioButton('Dark')
        dark_cluster_radio_button.toggled.connect(self.on_dark_cluster_radio_button_toggled)

        layout = QVBoxLayout()
        layout.addWidget(central_cluster_radio_button)
        layout.addWidget(light_cluster_radio_button)
        layout.addWidget(dark_cluster_radio_button)

        cluster_type_group_box = QGroupBox('Cluster Type')
        cluster_type_group_box.setLayout(layout)
        return cluster_type_group_box

    def on_connected_component_check_box_toggled(self, checked: bool):
        self.tool.paint_connected_component = checked

    def on_central_cluster_radio_button_toggled(self, checked: bool):
        self.tool.paint_central_pixel_cluster = checked

    def on_light_cluster_radio_button_toggled(self, checked: bool):
        self.tool.paint_dark_cluster = not checked

    def on_dark_cluster_radio_button_toggled(self, checked: bool):
        self.tool.paint_dark_cluster = checked
