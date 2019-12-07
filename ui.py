from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QAction, QApplication, QCheckBox, QComboBox,
		QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
		QMessageBox, QMenu, QPushButton, QSpinBox, QStyle, QSystemTrayIcon,
		QTextEdit, QVBoxLayout, QInputDialog)
from PyQt5.QtCore import (QThread, QTimer, QFile, QSettings)

from PyQt5 import QtCore, QtGui, QtWidgets
from utils import common, net_op
from core.profile_reader import KProfile
#from core.computer_score import KScore
from ui import resources_rc
from ui.login import Ui_Login
from ui.settings import Ui_Settings
from ui.about import Ui_About
from ui.startup import KStartup
import urllib.parse, json
from multiprocessing import Pipe
import start

wsettings = None
wabout = None

ti = None
main_proc = None

parent_end = None
child_end = None

def start_python_main():
	global main_proc
	global parent_end
	global child_end

	parent_end, child_end = Pipe()

	main_proc = common.fork_process(start.python_main, (child_end,))
	main_proc.daemon = True
	main_proc.start()

def terminate_main():
	global main_proc
	global parent_end
	global child_end

	if main_proc:
		main_proc.terminate()

	if parent_end and child_end:
		parent_end.close()
		child_end.close()

		parent_end = None
		child_end = None

class TrayIcon(QSystemTrayIcon):
	def __init__(self, parent = None):
		super(TrayIcon, self).__init__(parent)

		self.checkout_loggon = False

		# UI
		self.createActions()
		self.createTrayIcon()

		self.set_icon()

		self.setToolTip("")

	def set_icon(self):
		icon_png = ":icons/icon.png"

		# Draw system tray icon
		pixmap = QtGui.QPixmap(QtGui.QPixmap(icon_png))

		self.setIcon(QtGui.QIcon(pixmap))
		# End drawing system tray icon

		# Menu actions
	def createActions(self):
		self.inprotected = QAction("&Marsnake正在保护您的设备", self)
		self.inprotected.setDisabled(True)
		self.setting = QAction("&设置", self, triggered = self.trigger_setting)
		self.quit_proc = QAction("&退出", self, triggered = self.trigger_exit)

		self.help_checkupdate = QAction("&检查更新", self, triggered = self.trigger_help_checkupdate)
		self.help_feedback = QAction("&问题反馈", self, triggered = self.trigger_help_feedback)
		self.help_about = QAction("&关于", self, triggered = self.trigger_help_about)

		# UI functions
	def createTrayIcon(self):
		self.main_menu = QMenu()
		self.help_menu = QMenu()
		self.loggon_menu = QMenu()
		self.status_menu = QMenu()

		self.help_menu.setTitle("帮助")
		#self.help_menu.addAction(self.help_checkupdate)
		#self.help_menu.addAction(self.help_feedback)
		self.help_menu.addAction(self.help_about)

		self.loggon_menu.addAction(self.logout)

		self.main_menu.addAction(self.inprotected)
		self.main_menu.addMenu(self.loggon_menu)
		self.main_menu.addAction(self.tologin)

		self.main_menu.addSeparator()
		self.main_menu.addAction(self.setting)
		self.main_menu.addAction(self.goto_online)
		self.main_menu.addMenu(self.help_menu)
		self.main_menu.addAction(self.quit_proc)

		self.setContextMenu(self.main_menu)
		self.activated.connect(self.trayIconActivated)

	def trigger_help_checkupdate(self):
		self.showMessage("测试", "检查更新")

	def trigger_help_feedback(self):
		self.showMessage("测试", "问题反馈")

	def trigger_help_about(self):
		global wabout

		wabout.show()
		wabout.activateWindow()

	def trigger_setting(self):
		global wsettings

		wsettings.show()
		wsettings.activateWindow()

	def trigger_exit(self):
		terminate_main()
		QApplication.instance().quit()

	def trayIconActivated(self, reason):
		if self.checkout_loggon:
			self.inprotected.setText("&Marsnake正在保护您的设备")
			self.inprotected.setVisible(True)
			self.loggon_menu.menuAction().setVisible(True)
			self.status_menu.menuAction().setVisible(True)
			self.tologin.setVisible(False)
		else:
			self.inprotected.setVisible(False)
			self.loggon_menu.menuAction().setVisible(False)
			self.status_menu.menuAction().setVisible(False)
			self.tologin.setVisible(True)

class Settings(QDialog):
	def __init__(self):
		super(Settings, self).__init__()

		self.ui = Ui_Settings()
		self.ui.setupUi(self)

		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.trigger_btn_ok_clicked)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.trigger_btn_cancel_clicked)

		self.setWindowFlags(QtCore.Qt.Window)

	def showEvent(self, event):
		self.ui.show()

	def closeEvent(self, event):
		event.ignore()
		self.hide()

	def trigger_btn_ok_clicked(self):
		remote_support_code = self.ui.remote_support_code.text()

		if remote_support_code:
			startup = self.ui.auto_startup.isChecked()

			if startup:
				if not KStartup().query_auto_run():
					KStartup().enable_auto_run()
			else:
				if KStartup().query_auto_run():
					KStartup().disable_auto_run()

			KProfile().write_settings(self.ui.auto_vul_repair_interval.currentData(),
											self.ui.auto_cleaner_interval.currentData(),
											self.ui.virus_scan_interval.currentData(),
											self.ui.allow_terminal.isChecked(),
											self.ui.allow_vnc.isChecked(),
											self.ui.remote_support_code.text())

			self.accept()
		else:
			QMessageBox.information(self, "设置", "连接码不能为空", QMessageBox.Yes)

	def trigger_btn_cancel_clicked(self):
		self.reject()

class About(QDialog):
	def __init__(self):
		super(About, self).__init__()

		self.ui = Ui_About()
		self.ui.setupUi(self)

		self.setWindowFlags(QtCore.Qt.Window)

	def closeEvent(self, event):
		event.ignore()
		self.hide()

	def trigger_btn_ok_clicked(self):
		self.accept()

class MyWindow(QWidget):
	def __init__(self, parent = None):
		super(MyWindow, self).__init__(parent)
		global ti

		ti = TrayIcon(self)
		ti.show()

		self.timer = QTimer(self)
		self.timer.timeout.connect(self.status_check)
		self.timer.setInterval(1000 * 10)
		self.timer.start()

		self.status_check()

	def status_check(self):
		pass

def signal_term_handler(signal, frame):
	global ti

	ti.trigger_exit()

def ui_main():
	import sys
	global wsettings, wabout

	app = QApplication(sys.argv)
	systemtray_timeout = 0

	# Check if DE supports system tray
	while not QSystemTrayIcon.isSystemTrayAvailable():
		systemtray_timeout += 1
		time.sleep (20)
		if systemtray_timeout == 5:
			QMessageBox.critical(None, "Mail notifier",
					"I couldn't detect any system tray on this system.")
			sys.exit(1)

	QApplication.setQuitOnLastWindowClosed(False)

	import signal
	signal.signal(signal.SIGTERM, signal_term_handler)

	wabout = About()
	wsettings = Settings()
	window = MyWindow()

	sys.exit(app.exec_())

if __name__ == '__main__':
	ui_main()