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

# https://github.com/C-Radius/Krita-Settings/
def find_tool_box():
	qwindow = Krita.instance().activeWindow().qwindow()
	for qobj in qwindow.findChildren(QWidget):
		if qobj.metaObject().className() == "KoToolBox":
			return qobj
def getCurrentTool():
	tool_box = find_tool_box()
	for qobj in tool_box.findChildren(QToolButton):
		if qobj.metaObject().className() == "KoToolBoxButton":
			if qobj.isChecked():
				return qobj.objectName()



class tooly(DockWidget):

	def __init__(self):
		super().__init__()
		self.setWindowTitle("tooly")
		mainWidget = QWidget(self)
		self.setWidget(mainWidget)
		box = QFormLayout()
		box.setSpacing(0)
		mainWidget.setLayout(box)
		
		self.button = {}
		for tool in tools:
			self.button[tool] = QPushButton("", mainWidget)
			self.button[tool].clicked.connect(self.press(tool))
			self.button[tool].setFixedSize(QSize(48, 48))
			self.button[tool].setIcon(QtGui.QIcon(Application.icon(tools[tool])))
			mainWidget.layout().addWidget(self.button[tool])
		# run self.setup after the window is initialized,
		#  cause right now the toolbox doesn't even exist
		Krita.instance().notifier().windowCreated.connect(self.setup)
	
	def setup(self):
		tool_box = find_tool_box()
		for qobj in tool_box.findChildren(QToolButton):
			if qobj.metaObject().className() == "KoToolBoxButton":
				qobj.toggled.connect(self.tool_toggled)
	
	def tool_toggled(self,true):
		if true:
			new_tool = getCurrentTool()
			# un-highlight now-deselected tool
			if getattr(self, "button_last", None) is not None:
				if self.button_last != new_tool:
					self.button[self.button_last].setStyleSheet("")
			# highlight selected tool
			if new_tool in tools:
				self.button[new_tool].setStyleSheet("background-color: gray")
				self.button_last = new_tool
			else:
				self.button_last = None
	
	def press(self, tool):
		def thing(): # stupid python quirks
			ins = Krita.instance().action(tool)
			if ins is not None:
				ins.trigger()
		return thing

	def canvasChanged(self, canvas):
		pass

dock = DockWidgetFactory("tooly", DockWidgetFactoryBase.DockLeft, tooly)
Krita.instance().addDockWidgetFactory(dock)
