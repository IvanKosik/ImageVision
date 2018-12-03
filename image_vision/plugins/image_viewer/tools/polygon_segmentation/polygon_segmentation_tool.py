from plugins.image_viewer.tools.image_viewer_tool import ImageViewerTool
import settings

from PyQt5.QtCore import Qt, QEvent
from skimage.draw import line, polygon
import pandas as pd
import os


class PolygonSegmentationTool(ImageViewerTool):
    def __init__(self, viewer, parent=None):
        super().__init__(viewer, parent)

        self.points = []

    def on_before_viewer_image_changed(self):
        super().on_before_viewer_image_changed()

        if len(self.points) == 4:
            self.save_points_to_csv()
        else:
            print('NUMBER OF POINTS', len(self.points), '!= 4')

    def on_viewer_image_changed(self):
        super().on_viewer_image_changed()

        self.points.clear()

    def save_points_to_csv(self):
        csv_path = os.path.join(self.viewer.view_path, 'corners.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
        else:
            df = pd.DataFrame(columns=['File', 'x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4'])
            # df.loc[0] = ['image1', 10, 12, 22, 23, 31, 32, 44, 45]  # test

        file_name = os.path.basename(self.viewer.image_path)

        points_coords = [self.points[0][0], self.points[0][1], self.points[1][0], self.points[1][1],
                         self.points[2][0], self.points[2][1], self.points[3][0], self.points[3][1]]

        image_data_rows = df['File'] == file_name
        if image_data_rows.any():
            # replace old data with new one
            df.loc[image_data_rows, ['x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4']] = points_coords
        else:
            # add points data to the end
            df.loc[df.shape[0]] = [file_name] + points_coords

        df.to_csv(csv_path, index=False)

    def eventFilter(self, watched_obj, e):
        if e.type() == QEvent.MouseButtonPress:
            self.on_mouse_pressed(e)
            return True
        else:
            return super().eventFilter(watched_obj, e)

    def on_mouse_pressed(self, e):
        if not (self.viewer.has_image() and self.viewer.is_over_image(e.pos())):
            return

        image_coords = self.viewer.pos_to_image_coords(e.pos())

        if e.buttons() == Qt.LeftButton:
            self.add_point(image_coords[0], image_coords[1])
        elif e.buttons() == Qt.RightButton:
            self.remove_last_point()

    def add_point(self, row, col):
        self.viewer.mask().data[row, col] = settings.MASK_COLOR
        self.points.append((row, col))

        # self.draw_line(settings.TOOL_FOREGROUND)
        self.draw_polygon()

        self.viewer.update_scaled_combined_image()

    def remove_last_point(self):
        if len(self.points) < 1:
            return

        # self.draw_line(settings.TOOL_NO_COLOR)  # remove line

        last_point = self.points[-1]
        self.viewer.mask().data[last_point[0], last_point[1]] = settings.NO_MASK_COLOR

        del self.points[-1]

        self.draw_polygon()

        self.viewer.update_scaled_combined_image()

    def draw_line(self, color):
        if len(self.points) < 2:
            return

        penult_point = self.points[-2]
        last_point = self.points[-1]

        rr, cc = line(penult_point[0], penult_point[1], last_point[0], last_point[1])
        self.tool_mask.data[rr, cc] = color

    def draw_polygon(self):
        # Erase old polygon
        self.tool_mask.data.fill(0)

        if not len(self.points):
            return

        r_coords = []
        c_coords = []
        for p in self.points:
            r_coords.append(p[0])
            c_coords.append(p[1])

        rr, cc = polygon(r_coords, c_coords, shape=self.tool_mask.data.shape)
        self.tool_mask.data[rr, cc] = settings.TOOL_FOREGROUND
