import math
import re
import sys
from PyQt6.QtCore import QSize,QTranslator
from PyQt6.QtWidgets import QApplication, QComboBox, QMainWindow, QDialog, QGridLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem

version = '2023.12.15.002'
class ExposureCalculator(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("LUX2EV   " + version)
        self.resize(QSize(320, 720))
        # 创建构件
        self.lux_label = QLabel("LUX")
        self.lux_edit = QLineEdit()
        self.iso_label = QLabel("ISO")
        iso_list = [50,64,100,125,160,200,250,320,400,500,640,800,1000,1250,1600,2000,2500,3200,4000,5000,6400,8000,10000,12500,16000,20000,25000,32000,4000,5000,6400,8000,10000,12800,16000,20000,25600,51200,102400]
        self.iso_select = QComboBox()
        self.iso_select.addItems([str(iso) for iso in iso_list])
        self.iso_select.setCurrentIndex(0)
        self.iso_label.setBuddy(self.iso_select)

        self.ev_label = QLabel("EV:")
        self.ev_value = QLabel()
        self.calculate_button = QPushButton("Calc")
        self.exposure_table = QTableWidget()
        self.exposure_table.setColumnCount(2)
        self.exposure_table.setHorizontalHeaderLabels(["F (Aperture)", "S (Shutter Speed)"])
        
        # 创建布局
        layout = QGridLayout()
        layout.addWidget(self.lux_label, 0, 0)
        layout.addWidget(self.lux_edit, 0, 1)
        layout.addWidget(self.iso_label, 1, 0)
        layout.addWidget(self.iso_label, 1, 0)
        layout.addWidget(self.iso_select, 1, 1)
        layout.addWidget(self.calculate_button, 2, 0)
        layout.addWidget(self.ev_label, 3, 0)
        layout.addWidget(self.ev_value, 3, 1)
        layout.addWidget(self.exposure_table, 4, 0, 1, 2)
        self.setLayout(layout)
        
        # 链接事件
        self.calculate_button.clicked.connect(self.calculate_ev)
        
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        print("Current window size:", self.size())
    
    def calculate_ev(self):
        try:
            lux = float(self.lux_edit.text())
            iso = float(self.iso_select.currentText())
            ev = 2+math.log2(lux /10)
            ev = round(ev * 10) / 10
            self.ev_value.setText(str(ev))
            self.populate_table(ev,iso)
        except ValueError:
            pass
    
    def populate_table(self, ev,iso):
        self.exposure_table.clearContents()
        aperture_list = [0.95, 1.2, 1.4, 1.7, 1.8, 2, 2.8, 3.5, 4, 4.5, 5.6, 6.3, 7.1, 8, 11, 16, 22, 32]
        aperture_count = len(aperture_list)
        self.exposure_table.setRowCount(aperture_count)
        for i in range(aperture_count):
            aperture = aperture_list[i]
            shutter_speed = self.calculate_shutter_speed(aperture, ev,iso)
            self.exposure_table.setItem(i, 0, QTableWidgetItem(str(aperture)))
            self.exposure_table.setItem(i, 1, QTableWidgetItem(shutter_speed))
        # self.exposure_table.setHorizontalHeaderLabels(["F (Aperture)", "S (Shutter Speed)"])
    
    def calculate_shutter_speed(self,aperture,ev,iso):
        shutter_speed = (aperture*aperture/math.pow(2,ev)*100/iso)
        if 1/8000 <= shutter_speed<=30:
            shutter_speed_list =[30, 25, 20, 15, 13, 10, 8, 6, 5 , 4, 3.2, 2.5 , 2, 1.6, 1.3, 1, 0.8, 0.6, 0.5, 0.4, 1/3, 1/4, 1/5, 1/6, 1/8, 1/10, 1/13, 1/15, 1/20, 1/25, 1/30, 1/40, 1/50, 1/60, 1/80, 1/100, 1/125, 1/160, 1/200, 1/250, 1/320, 1/400, 1/500, 1/640, 1/800, 1/1000, 1/1250, 1/1600, 1/2000, 1/2500, 1/3200, 1/4000, 1/5000, 1/6400, 1/8000]
            shutter_speed_str_list = ['30','25','20','15','13','10','8','6','5','4','3.2','2.5','2','1.6','1.3','1','0.8','0.6','0.5','0.4','1/3','1/4','1/5','1/6','1/8','1/10','1/13','1/15','1/20','1/25','1/30','1/40','1/50','1/60','1/80','1/100','1/125','1/160','1/200','1/250','1/320','1/400','1/500','1/640','1/800','1/1000','1/1250','1/1600','1/2000','1/2500','1/3200','1/4000','1/5000','1/6400','1/8000']
            closest_speed = min(shutter_speed_list, key=lambda x: abs(x - shutter_speed))
            closest_speed_index = shutter_speed_list.index(closest_speed)
            return str(shutter_speed_str_list[closest_speed_index])
        elif shutter_speed > 30:
            return str(int(shutter_speed))
        else:
            return ('Overexposure Warning')

    def nearest_power_of_two(self,num):
        power = math.ceil(math.log(num, 2))
        return int(math.pow(2, power))
        
# Run The Code
def main():

    app = QApplication(sys.argv)
    main_window = ExposureCalculator()
    main_window.show()
    app.exec()


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
