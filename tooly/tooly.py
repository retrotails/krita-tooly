# ~ krita-tooly
# ~ Copyright (C) 2020 retrotails

# ~ This program is free software: you can redistribute it and/or modify
# ~ it under the terms of the GNU General Public License as published by
# ~ the Free Software Foundation, specifically version 3 of the License.

# ~ This program is distributed in the hope that it will be useful,
# ~ but WITHOUT ANY WARRANTY; without even the implied warranty of
# ~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# ~ GNU General Public License for more details.

# ~ You should have received a copy of the GNU General Public License
# ~ along with this program.  If not, see <https://www.gnu.org/licenses/>.

button = {}
# see in krita source: krita/krita.action
# also https://scripting.krita.org/icon-library
# "toolAction": "tool_icon_name",
tools = {
	"KritaShape/KisToolBrush":           "krita_tool_freehand",
	"KritaSelected/KisToolColorSampler": "krita_tool_color_sampler",
	"KritaFill/KisToolFill":             "krita_tool_color_fill",
	"KritaTransform/KisToolMove":        "krita_tool_move",
	"KisToolTransform":                  "krita_tool_transform",
	"KisToolSelectRectangular":          "tool_rect_selection",
	"KisToolSelectPolygonal":            "tool_polygonal_selection",
	"KisToolSelectOutline":              "tool_outline_selection",
	"KisToolSelectContiguous":           "tool_contiguous_selection",
}

from PyQt5.QtWidgets import *
from krita import *

class tooly(DockWidget):

	def __init__(self):
		super().__init__()
		self.setWindowTitle("tooly")
		mainWidget = QWidget(self)
		self.setWidget(mainWidget)
		box = QFormLayout()
		box.setSpacing(0)
		mainWidget.setLayout(box)
		
		for tool in tools:
			button[tool] = QPushButton("", mainWidget)
			button[tool].clicked.connect(self.press(tool, button))
			button[tool].setFixedSize(QSize(48, 48))
			button[tool].setIcon(QtGui.QIcon(Application.icon(tools[tool])))
			mainWidget.layout().addWidget(button[tool])

	def press(self, tool, button):
		def thing(): # stupid python quirks
			ins = Krita.instance().action(tool)
			if ins is not None:
				button[tool].setStyleSheet("background-color: gray")
				if getattr(self, "button_last", None) is not None:
					if self.button_last !=  tool:
						button[self.button_last].setStyleSheet("")
				self.button_last = tool
				ins.trigger()
		return thing

	def canvasChanged(self, canvas):
		pass

dock = DockWidgetFactory("tooly", DockWidgetFactoryBase.DockLeft, tooly)
Krita.instance().addDockWidgetFactory(dock)
