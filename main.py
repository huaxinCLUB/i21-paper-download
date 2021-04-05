import requests
from lxml import etree
import os

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication,QMessageBox,QFileDialog


class Downloader():

    def __init__(self):
        #从文件中加载UI定义
        self.ui = QUiLoader().load("UI/main.ui")

        #给查询的按钮点击信号增加槽函数
        self.ui.checkButton.clicked.connect(self.checkButtonEvent)

        #给浏览按钮添加槽函数，选择下载路径
        self.ui.chooseDownloadPath.clicked.connect(self.downloadPath)
        #给下载按钮添加槽函数，根据用户输入的报纸期数和下载类型（PDF，word）进行下载
        self.ui.downloadButton.clicked.connect(self.action)


    #查询按钮的槽函数
    def checkButtonEvent(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",
            "Host": "paper.i21st.cn",
            "Referer": "https://paper.i21st.cn/index_21je2.html"
            }
        #获取年级的index，起始值为0
        grade = self.ui.grade.currentIndex()+1

        url = "https://paper.i21st.cn/index_21je{}.html".format(grade)
        #打印用户选择查询的年级及URL
        self.ui.logs.append("您正在查询的是{}，URL为：{}\n请等待***************".format(self.ui.grade.currentText,url))

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            self.ui.logs.append('正在获取响应码-------')
            #self.ui.logs.append 只能显示str类型格式
            self.ui.logs.append(str(response.status_code))  # 显示响应码
            # print(text)
            text = response.text
            html = etree.HTML(text)
            date = html.xpath("//div[@class='listPicDiv listPicDivM0']/text()")
            # print(date[0].strip())
            self.ui.logs.append("目前报纸最新为：{}。请填写需要下载的报纸期数！" .format(date[0].strip()))
        except:
            QMessageBox.critical(self.ui,'错误','查询错误，请联系作者\n点击{}，提交issue'.format("这里"))


    #浏览按钮的槽函数，点击浏览后弹窗选择下载路径，并在左侧文本框中显示下载路径
    def downloadPath(self):
        filePath = QFileDialog.getExistingDirectory(self.ui, "选择存储路径")
        self.ui.dlPath.setText(filePath)





    #下载按钮的槽函数
    def action(self):
        #判断下载路径是否为空
        if self.ui.dlPath.text() == "":
            QMessageBox.critical(self.ui,'错误','还没有选择下载路径呢，急什么！')
        else:
            #判断选择的路径是否存在，如无则创建
            try:
                if os.path.exists(self.ui.dlPath.text()):
                    self.ui.logs.append('下载目录已存在，正在执行下一步\n\n*************************************')
                else:
                    self.ui.logs.append("未发现下载目录，正在创建**************\n\n*************************************")
                    os.mkdir(self.ui.dlPath.text())
            except:
                #若文件未正常创建，则弹窗提示用户重新输入
                QMessageBox.critical(self.ui, '错误', '路径有误，请重新选择下载路径！')

        #输出下载目录为self.ui.dlPath.text()
        self.ui.logs.append("文件保存目录为：{}\n\n*************************************".format(self.ui.dlPath.text()))

        #判断下载期数是否为空
        if self.ui.startNum.text() == "":
            QMessageBox.critical(self.ui,'错误','请输入下载开始期数！')

        if self.ui.endNum.text() == "":
            QMessageBox.critical(self.ui, '错误', '请输入下载结束期数！')


        #判断下载期数是否输入的是数值，且后者大于前者
        startNum = eval(self.ui.startNum.text())
        endNum = eval(self.ui.endNum.text())
        if isinstance(startNum,int) and isinstance(endNum,int):
            pass
        else:
            QMessageBox.critical(self.ui, '错误', '报纸期数请输入正整数类型，不要瞎搞！')

        #判断结束期数是否大于等于起始期数
        if startNum > endNum:
            QMessageBox.critical(self.ui, '错误', '小可爱，貌似结束期数应该大于起始期数吧！')

        #输出下载报纸的年级（）和期数
        self.ui.logs.append("需要下载{}第 {} 期——第 {} 期报纸\n\n*************************************".format(self.ui.grade.currentText(),self.ui.startNum.text(),self.ui.endNum.text()))


        #确定需要下载报纸的期数，保存在列表nums里
        nums = list(range(startNum,endNum + 1))

        #判断是否要下载PDF格式的报纸
        if self.ui.pdfCheckBox.isChecked():
            for num in nums:
                pdf_url = "https://paper.i21st.cn/download/21je{}_{}.pdf".format(self.ui.grade.currentIndex()+1,num)
                # self.down_pdf(pdf_url)

        print(self.ui.pdfCheckBox.isChecked())
        print(endNum)
        print(list(range(startNum,endNum)))
        print(type(startNum))
        print(type(endNum))




        #self.down_pdf()

    #下载指定报纸的PDF版
    def down_pdf(self,url):
        #从文本框获取cookie
        # cookie = self.ui.cookie.toPlainText()
        # #获取需下载的报纸起始期数
        # startNum = self.ui.startNum.text()
        # #获取需下载报纸的结束期数
        # endNum = eval(self.ui.endNum.text())
        #
        # print(startNum)
        # print(type(startNum))
        # print(isinstance(startNum,int))

        # self.ui.logs.append(startNum)

        pass








app = QApplication([])
downloader = Downloader()
downloader.ui.show()
app.exec_()