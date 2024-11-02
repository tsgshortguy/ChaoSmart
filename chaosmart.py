import sys
import os
import platform
import socket
import psutil
import ctypes
import winreg
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout,
    QLabel, QPushButton, QFileDialog, QListWidget, QHBoxLayout,
    QMessageBox, QLineEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QProgressBar, QGraphicsOpacityEffect
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PyQt5.QtGui import QIcon, QFont, QColor, QPixmap

# ==========================
# Function to Check Administrative Privileges
# ==========================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Re-run the program with admin privileges."""
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to elevate privileges:\n{e}")
    sys.exit()

if not is_admin():
    run_as_admin()

# ==========================
# Custom Stylesheet for ChaoSmart
# ==========================
CHAOSMART_STYLE = """
QMainWindow {
    background-color: #1e1e1e;
    color: #ffffff;
}

QTabWidget::pane {
    border-top: 2px solid #444;
}

QTabBar::tab {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #2d2d2d, stop:1 #1e1e1e);
    color: #ffffff;
    padding: 10px;
    margin: 2px;
    border-radius: 4px;
    min-width: 100px;
}

QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #0078d7, stop:1 #005a9e);
    font-weight: bold;
}

QPushButton {
    background-color: #0078d7;
    color: #ffffff;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    font-weight: bold;
    transition: background-color 0.3s;
}

QPushButton:hover {
    background-color: #3399ff;
}

QLabel {
    font-size: 14px;
}

QListWidget {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #555;
}

QTableWidget {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #555;
}

QHeaderView::section {
    background-color: #0078d7;
    color: #ffffff;
    padding: 4px;
    font-weight: bold;
}

QLineEdit {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #555;
    padding: 6px;
    border-radius: 4px;
}

QProgressBar {
    border: 1px solid #555;
    border-radius: 5px;
    text-align: center;
    color: #ffffff;
    background-color: #2d2d2d;
}

QProgressBar::chunk {
    background-color: #0078d7;
    width: 20px;
}

QMessageBox {
    background-color: #1e1e1e;
    color: #ffffff;
}
"""

# ==========================
# System Information Tab
# ==========================
class SystemInfoTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Fonts
        header_font = QFont()
        header_font.setPointSize(12)
        header_font.setBold(True)

        # Operating System
        self.os_label = QLabel()
        self.os_label.setFont(header_font)

        # CPU Usage
        self.cpu_label = QLabel()
        self.cpu_label.setFont(header_font)
        self.cpu_progress = QProgressBar()
        self.cpu_progress.setMaximum(100)
        self.cpu_progress.setValue(0)

        # Memory Usage
        self.memory_label = QLabel()
        self.memory_label.setFont(header_font)
        self.memory_progress = QProgressBar()
        self.memory_progress.setMaximum(100)
        self.memory_progress.setValue(0)

        # Disk Usage
        self.disk_label = QLabel()
        self.disk_label.setFont(header_font)
        self.disk_progress = QProgressBar()
        self.disk_progress.setMaximum(100)
        self.disk_progress.setValue(0)

        # Add Widgets to Layout
        layout.addWidget(self.os_label)
        layout.addWidget(QLabel("CPU Usage:"))
        layout.addWidget(self.cpu_progress)
        layout.addWidget(self.cpu_label)
        layout.addWidget(QLabel("Memory Usage:"))
        layout.addWidget(self.memory_progress)
        layout.addWidget(self.memory_label)
        layout.addWidget(QLabel("Disk Usage:"))
        layout.addWidget(self.disk_progress)
        layout.addWidget(self.disk_label)

        self.setLayout(layout)
        self.update_info()

        # Set up a timer to auto-update system info every 3 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(3000)  # 3000 ms = 3 seconds

    def update_info(self):
        os_info = f"Operating System: {platform.system()} {platform.release()}"
        cpu_usage = psutil.cpu_percent(interval=None)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        self.os_label.setText(os_info)

        self.cpu_progress.setValue(int(cpu_usage))
        self.cpu_label.setText(f"{cpu_usage}%")

        self.memory_progress.setValue(int(memory_usage))
        self.memory_label.setText(f"{memory_usage}%")

        self.disk_progress.setValue(int(disk_usage))
        self.disk_label.setText(f"{disk_usage}%")

# ==========================
# Network Information Tab
# ==========================
class NetworkInfoTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Fonts
        header_font = QFont()
        header_font.setPointSize(12)
        header_font.setBold(True)

        # Hostname
        self.hostname_label = QLabel()
        self.hostname_label.setFont(header_font)

        # IP Address
        self.ip_label = QLabel()
        self.ip_label.setFont(header_font)

        # Add Widgets to Layout
        layout.addWidget(self.hostname_label)
        layout.addWidget(self.ip_label)

        self.setLayout(layout)
        self.update_info()

        # Set up a timer to auto-update network info every 3 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(3000)  # 3000 ms = 3 seconds

    def update_info(self):
        hostname = socket.gethostname()
        try:
            ip_address = socket.gethostbyname(hostname)
        except socket.error:
            ip_address = "Unable to retrieve IP"

        self.hostname_label.setText(f"Hostname: {hostname}")
        self.ip_label.setText(f"IP Address: {ip_address}")

# ==========================
# File Explorer Tab
# ==========================
class FileExplorerTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Fonts
        header_font = QFont()
        header_font.setPointSize(12)
        header_font.setBold(True)

        # Current Path
        self.path_label = QLabel("Current Path: ")
        self.path_label.setFont(header_font)

        # List Widget
        self.list_widget = QListWidget()
        self.list_widget.setFont(QFont("Arial", 12))
        self.list_widget.itemDoubleClicked.connect(self.open_item)

        # Open Directory Button
        self.open_button = QPushButton("Open Directory")
        self.open_button.setFixedWidth(150)
        self.open_button.clicked.connect(self.open_directory)

        # Add Widgets to Layout
        layout.addWidget(self.path_label)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.open_button)

        self.setLayout(layout)
        self.current_path = os.path.expanduser("~")
        self.load_directory()

    def open_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", self.current_path)
        if directory:
            self.current_path = directory
            self.load_directory()

    def load_directory(self):
        self.path_label.setText(f"Current Path: {self.current_path}")
        self.list_widget.clear()
        try:
            for item in os.listdir(self.current_path):
                self.list_widget.addItem(item)
        except PermissionError:
            QMessageBox.warning(self, "Permission Denied", f"Cannot access {self.current_path}")

    def open_item(self, item):
        path = os.path.join(self.current_path, item.text())
        if os.path.isdir(path):
            self.current_path = path
            self.load_directory()
        else:
            try:
                os.startfile(path)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Cannot open file:\n{e}")

# ==========================
# Process Manager Tab
# ==========================
class ProcessManagerTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Table Widget
        self.process_table = QTableWidget()
        self.process_table.setColumnCount(3)
        self.process_table.setHorizontalHeaderLabels(["PID", "Name", "CPU Usage (%)"])
        self.process_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.process_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.process_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.process_table.setFont(QFont("Arial", 12))

        # Apply styles to the table
        self.process_table.setStyleSheet("""
            QTableWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
            }
            QHeaderView::section {
                background-color: #0078d7;
                color: #ffffff;
                padding: 4px;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #1e90ff;
                color: #ffffff;
            }
        """)

        # Buttons
        self.refresh_button = QPushButton("Refresh Processes")
        self.kill_button = QPushButton("Kill Selected Process")

        # Button Animations
        self.add_hover_animation(self.refresh_button)
        self.add_hover_animation(self.kill_button)

        self.refresh_button.clicked.connect(self.load_processes)
        self.kill_button.clicked.connect(self.kill_process)

        # Button Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.kill_button)
        button_layout.addStretch()

        # Add Widgets to Layout
        layout.addWidget(self.process_table)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.load_processes()

    def add_hover_animation(self, button):
        """Add a simple hover animation to buttons."""
        effect = QGraphicsOpacityEffect()
        button.setGraphicsEffect(effect)
        self.anim = QPropertyAnimation(effect, b"opacity")
        self.anim.setDuration(300)
        button.enterEvent = lambda event: self.start_animation(1.0)
        button.leaveEvent = lambda event: self.start_animation(0.7)

    def start_animation(self, end_value):
        self.anim.stop()
        self.anim.setStartValue(self.anim.startValue() if self.anim.startValue() else 0.7)
        self.anim.setEndValue(end_value)
        self.anim.start()

    def load_processes(self):
        self.process_table.setRowCount(0)
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                cpu = proc.info['cpu_percent']
                row_position = self.process_table.rowCount()
                self.process_table.insertRow(row_position)
                self.process_table.setItem(row_position, 0, QTableWidgetItem(str(pid)))
                self.process_table.setItem(row_position, 1, QTableWidgetItem(name))
                self.process_table.setItem(row_position, 2, QTableWidgetItem(str(cpu)))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    def kill_process(self):
        selected_items = self.process_table.selectedItems()
        if selected_items:
            pid = int(selected_items[0].text())
            reply = QMessageBox.question(
                self, 'Confirm Kill',
                f"Are you sure you want to kill process PID {pid}?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                try:
                    proc = psutil.Process(pid)
                    proc.terminate()
                    proc.wait(timeout=3)
                    QMessageBox.information(self, "Success", f"Process PID {pid} terminated.")
                    self.load_processes()
                except psutil.NoSuchProcess:
                    QMessageBox.warning(self, "Error", "Process does not exist.")
                except psutil.AccessDenied:
                    QMessageBox.warning(self, "Error", "Access Denied.")
                except psutil.TimeoutExpired:
                    QMessageBox.warning(self, "Error", "Could not terminate process.")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a process to kill.")

# ==========================
# Registry Editor Tab
# ==========================
class RegistryEditorTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Fonts
        header_font = QFont()
        header_font.setPointSize(12)
        header_font.setBold(True)

        # Registry Key Input
        self.key_label = QLabel("Registry Key:")
        self.key_label.setFont(header_font)
        self.key_input = QLineEdit("HKEY_CURRENT_USER\\Software")
        self.key_input.setFont(QFont("Arial", 12))

        # Load Button
        self.load_button = QPushButton("Load Key")
        self.load_button.setFixedWidth(100)
        self.load_button.clicked.connect(self.load_registry_key)

        # Value List
        self.value_list = QListWidget()
        self.value_list.setFont(QFont("Arial", 12))

        # Add Widgets to Layout
        layout.addWidget(self.key_label)
        layout.addWidget(self.key_input)
        layout.addWidget(self.load_button)
        layout.addWidget(self.value_list)

        self.setLayout(layout)

    def load_registry_key(self):
        key_path = self.key_input.text()
        root_key, sub_key = self.parse_registry_path(key_path)
        try:
            registry_key = winreg.OpenKey(root_key, sub_key, 0, winreg.KEY_READ)
            self.value_list.clear()
            index = 0
            while True:
                try:
                    value = winreg.EnumValue(registry_key, index)
                    self.value_list.addItem(f"{value[0]}: {value[1]}")
                    index += 1
                except OSError:
                    break
            winreg.CloseKey(registry_key)
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "Registry key not found.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load registry key:\n{e}")

    def parse_registry_path(self, path):
        hive_map = {
            "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
            "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
            "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
            "HKEY_USERS": winreg.HKEY_USERS,
            "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG
        }
        parts = path.split("\\", 1)
        hive = parts[0]
        sub_key = parts[1] if len(parts) > 1 else ""
        return hive_map.get(hive.upper(), winreg.HKEY_CURRENT_USER), sub_key

# ==========================
# Startup Manager Tab
# ==========================
class StartupManagerTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Fonts
        header_font = QFont()
        header_font.setPointSize(12)
        header_font.setBold(True)

        # Startup List
        self.startup_list = QListWidget()
        self.startup_list.setFont(QFont("Arial", 12))

        # Buttons
        self.refresh_button = QPushButton("Refresh Startup Items")
        self.enable_button = QPushButton("Enable Selected")
        self.disable_button = QPushButton("Disable Selected")

        # Button Animations
        self.add_hover_animation(self.refresh_button)
        self.add_hover_animation(self.enable_button)
        self.add_hover_animation(self.disable_button)

        # Connect Buttons
        self.refresh_button.clicked.connect(self.load_startup_items)
        self.enable_button.clicked.connect(self.enable_item)
        self.disable_button.clicked.connect(self.disable_item)

        # Button Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.enable_button)
        button_layout.addWidget(self.disable_button)
        button_layout.addStretch()

        # Add Widgets to Layout
        layout.addWidget(self.startup_list)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.load_startup_items()

    def add_hover_animation(self, button):
        """Add a simple hover animation to buttons."""
        effect = QGraphicsOpacityEffect()
        button.setGraphicsEffect(effect)
        self.anim = QPropertyAnimation(effect, b"opacity")
        self.anim.setDuration(300)
        button.enterEvent = lambda event: self.start_animation(1.0)
        button.leaveEvent = lambda event: self.start_animation(0.7)

    def start_animation(self, end_value):
        self.anim.stop()
        self.anim.setStartValue(self.anim.startValue() if self.anim.startValue() else 0.7)
        self.anim.setEndValue(end_value)
        self.anim.start()

    def load_startup_items(self):
        self.startup_list.clear()
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ)
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(registry_key, i)
                    self.startup_list.addItem(f"{name}: {value}")
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(registry_key)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load startup items:\n{e}")

    def enable_item(self):
        selected = self.startup_list.currentItem()
        if selected:
            name, path = selected.text().split(": ", 1)
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            try:
                winreg.SetValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE), name, 0, winreg.REG_SZ, path)
                QMessageBox.information(self, "Success", f"Enabled startup item: {name}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to enable startup item:\n{e}")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a startup item to enable.")

    def disable_item(self):
        selected = self.startup_list.currentItem()
        if selected:
            name, _ = selected.text().split(": ", 1)
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            try:
                winreg.DeleteValue(winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE), name)
                QMessageBox.information(self, "Success", f"Disabled startup item: {name}")
                self.load_startup_items()
            except FileNotFoundError:
                QMessageBox.warning(self, "Error", "Startup item not found.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to disable startup item:\n{e}")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a startup item to disable.")

# ==========================
# Main Application Window
# ==========================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChaoSmart - PC Utility Tool")
        self.setWindowIcon(QIcon())  # Optionally, set a custom icon here
        self.setGeometry(100, 100, 1000, 800)

        # Apply the custom stylesheet
        self.setStyleSheet(CHAOSMART_STYLE)

        # Initialize Tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Initialize Each Tab
        self.system_info_tab = SystemInfoTab()
        self.network_info_tab = NetworkInfoTab()
        self.file_explorer_tab = FileExplorerTab()
        self.process_manager_tab = ProcessManagerTab()
        self.registry_editor_tab = RegistryEditorTab()
        self.startup_manager_tab = StartupManagerTab()

        # Add Tabs with Icons
        self.tabs.addTab(self.system_info_tab, QIcon('system_info.png'), "System Info")
        self.tabs.addTab(self.network_info_tab, QIcon('network_info.png'), "Network Info")
        self.tabs.addTab(self.file_explorer_tab, QIcon('file_explorer.png'), "File Explorer")
        self.tabs.addTab(self.process_manager_tab, QIcon('process_manager.png'), "Process Manager")
        self.tabs.addTab(self.registry_editor_tab, QIcon('registry_editor.png'), "Registry Editor")
        self.tabs.addTab(self.startup_manager_tab, QIcon('startup_manager.png'), "Startup Manager")

        # Refresh Button with Animation
        self.refresh_button = QPushButton("Refresh All")
        self.refresh_button.setFixedWidth(150)
        self.refresh_button.clicked.connect(self.refresh_all)

        # Add Animation to Refresh Button
        self.add_button_animation(self.refresh_button)

        # Refresh Button Layout
        refresh_layout = QHBoxLayout()
        refresh_layout.addStretch()
        refresh_layout.addWidget(self.refresh_button)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.addLayout(refresh_layout)

        # Container Widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Add Fade-in Animation for the Entire Window
        self.fade_in()

    def add_button_animation(self, button):
        """Add a hover animation to buttons."""
        effect = QGraphicsOpacityEffect()
        button.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(300)
        button.enterEvent = lambda event: self.start_animation(animation, 1.0)
        button.leaveEvent = lambda event: self.start_animation(animation, 0.7)

    def start_animation(self, animation, end_value):
        animation.stop()
        animation.setStartValue(animation.startValue())
        animation.setEndValue(end_value)
        animation.start()

    def fade_in(self):
        """Fade in the window when it starts."""
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(1000)  # 1 second
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def refresh_all(self):
        self.system_info_tab.update_info()
        self.network_info_tab.update_info()
        self.file_explorer_tab.load_directory()
        self.process_manager_tab.load_processes()
        self.registry_editor_tab.load_registry_key()
        self.startup_manager_tab.load_startup_items()
        # Removed QMessageBox to eliminate "Refreshed" message

# ==========================
# Entry Point
# ==========================
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
