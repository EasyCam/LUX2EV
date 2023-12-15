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


    # 计算电子伏特ev
    def calculate_ev(self):
        try:
            # 获取输入的 lux 值
            lux = float(self.lux_edit.text())
            # 获取下拉框中的 iso 值
            iso = float(self.iso_select.currentText())
            # 计算 ev 值
            ev = 2+math.log2(lux /10)
            # 保留两位小数
            ev = round(ev * 10) / 10
            # 将计算结果更新到文本框中
            self.ev_value.setText(str(ev))
            # 调用 populate_table 函数，传入 ev 和 iso 值，计算出曝光组合
            self.populate_table(ev,iso)
        except ValueError:
            pass

    # 计算曝光组合
    # 定义一个函数，用于将参数ev和iso传入，并清空表格，然后创建一个列表aperture_list，用于存放光圈值，计算出列表长度，然后将表格行数设置为列表长度，然后遍历列表，计算出光圈值， shutter_speed，最后将计算出的结果分别放入表格中
    def populate_table(self, ev,iso):
        # 清空表格
        self.exposure_table.clearContents()
        # 创建一个列表，用于存放光圈值
        aperture_list = [0.95, 1.2, 1.4, 1.7, 1.8, 2, 2.8, 3.5, 4, 4.5, 5.6, 6.3, 7.1, 8, 11, 16, 22, 32]
        # 计算列表长度
        aperture_count = len(aperture_list)
        # 将表格行数设置为列表长度
        self.exposure_table.setRowCount(aperture_count)
        # 遍历列表
        for i in range(aperture_count):
            # 获取当前循环中的光圈值
            aperture = aperture_list[i]
            # 计算出快门速度
            shutter_speed = self.calculate_shutter_speed(aperture, ev,iso)
            # 将计算出的结果放入表格中
            self.exposure_table.setItem(i, 0, QTableWidgetItem(str(aperture)))
            self.exposure_table.setItem(i, 1, QTableWidgetItem(shutter_speed))


    # 计算快门速度
    def calculate_shutter_speed(self,aperture,ev,iso):
        # 计算快门速度
        shutter_speed = (aperture*aperture/math.pow(2,ev)*100/iso)
        # 如果快门速度在1/8000到30之间，则从shutter_speed_list中取出最接近shutter_speed的值，并返回其字符串表示
        if 1/8000 <= shutter_speed<=30:
            shutter_speed_list =[30, 25, 20, 15, 13, 10, 8, 6, 5 , 4, 3.2, 2.5 , 2, 1.6, 1.3, 1, 0.8, 0.6, 0.5, 0.4, 1/3, 1/4, 1/5, 1/6, 1/8, 1/10, 1/13, 1/15, 1/20, 1/25, 1/30, 1/40, 1/50, 1/60, 1/80, 1/100, 1/125, 1/160, 1/200, 1/250, 1/320, 1/400, 1/500, 1/640, 1/800, 1/1000, 1/1250, 1/1600, 1/2000, 1/2500, 1/3200, 1/4000, 1/5000, 1/6400, 1/8000]
            shutter_speed_str_list = ['30','25','20','15','13','10','8','6','5','4','3.2','2.5','2','1.6','1.3','1','0.8','0.6','0.5','0.4','1/3','1/4','1/5','1/6','1/8','1/10','1/13','1/15','1/20','1/25','1/30','1/40','1/50','1/60','1/80','1/100','1/125','1/160','1/200','1/250','1/320','1/400','1/500','1/640','1/800','1/1000','1/1250','1/1600','1/2000','1/2500','1/3200','1/4000','1/5000','1/6400','1/8000']
            closest_speed = min(shutter_speed_list, key=lambda x: abs(x - shutter_speed))
            closest_speed_index = shutter_speed_list.index(closest_speed)
            return str(shutter_speed_str_list[closest_speed_index])
        # 如果快门速度大于30，则返回其整数表示
        elif shutter_speed > 30:
            return str(int(shutter_speed))
        # 如果快门速度小于1/8000，则返回“Overexposure Warning”
        else:
            return ('Overexposure Warning')

    def nearest_power_of_two(self,num):
        '''
        返回最近的2的幂
        '''
        power = math.ceil(math.log(num, 2))
        return int(math.pow(2, power))


# 定义主函数
def main():
    # 创建QApplication实例
    app = QApplication(sys.argv)
    # 创建ExposureCalculator实例
    main_window = ExposureCalculator()
    # 显示窗口
    main_window.show()
    # 执行应用
    app.exec()


# 判断当前文件是否被作为脚本运行
if __name__ == '__main__':
    # 将sys.argv[0]中的'-script.pyw'或'.exe'替换为空字符
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    # 退出应用
    sys.exit(main())
