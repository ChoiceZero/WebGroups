from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
import sys
import json
import webbrowser as wb
import requests
from bs4 import BeautifulSoup
from pytube import Playlist
from ctypes import byref, c_int, sizeof

class WebGroups(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WebGroups')
        self.resize(1300, 700)
        self.setWindowIcon(QIcon('Logo.png'))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.collections = {}

        try:
            with open('webs_data.json', 'r', encoding = 'utf-8') as file:
                self.collections = json.load(file)
        except FileNotFoundError:
            with open('webs_data.json', 'w', encoding = 'utf-8') as file:
                json.dump({}, file, ensure_ascii = False)
            with open('webs_data.json', 'r', encoding = 'utf-8') as file:
                self.collections = json.load(file)

        with open('Languages.json', 'r', encoding = 'utf-8') as file:
                self.LanguagePacks = json.load(file)

        with open('settings.json', 'r', encoding = 'utf-8') as file:
                self.settings = json.load(file)

        self.LanguagePack = self.LanguagePacks[self.settings['language']]

        self.tab_widget = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QScrollArea()
        

        self.tab_widget.addTab(self.tab1, "Web Tree")
        self.tab_widget.addTab(self.tab2, "Viewport")
        self.tab_widget.addTab(self.tab3, "Options")

        self.layout.addWidget(self.tab_widget)

        self.initTab1()
        self.initTab2()
        self.initTab3()

    def loadLanguage(self,element):
        return str(self.LanguagePack['tab1'][element])
    def loadLanguage2(self,element):
        return str(self.LanguagePack['tab2'][element])
    def loadLanguage3(self,element):
        return str(self.LanguagePack['tab3'][element])

    def initTab1(self):
        layout = QHBoxLayout(self.tab1)
        self.list_webs = QListWidget()
        self.list_webs_label = QLabel(self.loadLanguage('title'))
        self.list_webs_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.list_webs_label.setAlignment(Qt.AlignLeft)
        self.len_webs_label = QLabel(self.loadLanguage('title')+ ": 0")
        self.len_webs_label.setAlignment(Qt.AlignRight)
        self.bottom_label_1 = QLabel(self.loadLanguage3('about_text'))
        self.bottom_label_1.setStyleSheet("font-size: 12px; color: gray;")
        self.bottom_label_1.setAlignment(Qt.AlignRight)
        self.tools_label = QLabel(self.loadLanguage('options_label'))
        self.tools_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.button_web_add = QPushButton(self.loadLanguage('button_web_add'))
        self.button_YT_add = QPushButton(self.loadLanguage('button_YT_add'))
        self.button_YT_pl_add = QPushButton(self.loadLanguage('button_YT_pl_add'))
        self.button_web_del = QPushButton(self.loadLanguage('button_web_del'))
        self.field_search = QLineEdit('')
        self.field_search.setPlaceholderText(self.loadLanguage('field_search'))
        self.button_search = QPushButton(self.loadLanguage('button_search'))
        self.button_clear = QPushButton(self.loadLanguage('button_clear'))
        self.button_web_exec = QPushButton(self.loadLanguage('button_web_exec'))
        self.descText = QTextEdit()
        self.descBtn = QPushButton(self.loadLanguage('descBtn'))
        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.HLine)
        self.divider2 = QFrame()
        self.divider2.setFrameShape(QFrame.HLine)
        self.divider3 = QFrame()
        self.divider3.setFrameShape(QFrame.HLine)
        self.list_groups = QListWidget()
        self.list_groups_label = QLabel(self.loadLanguage('list_groups_label'))
        self.list_groups_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.button_add = QPushButton(self.loadLanguage('button_add'))
        self.button_del = QPushButton(self.loadLanguage('button_del'))
        self.button_editGroup = QPushButton(self.loadLanguage('button_editGroup'))
        self.button_editWebUrl = QPushButton(self.loadLanguage('button_editWebUrl'))

        col_1 = QVBoxLayout()
        row = QHBoxLayout()
        row.addWidget(self.list_webs_label)
        row.addWidget(self.len_webs_label)
        col_1.addLayout(row)
        col_1.addWidget(self.list_webs)

        col_2 = QVBoxLayout()
        col_2.addWidget(self.list_groups_label)
        col_2.addWidget(self.list_groups)

        row_1 = QHBoxLayout()
        row_1.addWidget(self.button_web_add)
        row_1.addWidget(self.button_web_del)
        row_1.addWidget(self.button_editWebUrl)

        row_3 = QHBoxLayout()
        row_3.addWidget(self.button_add)
        row_3.addWidget(self.button_del)
        row_3.addWidget(self.button_editGroup)

        row_4 = QHBoxLayout()
        row_4.addWidget(self.button_search)
        row_4.addWidget(self.button_clear)

        col_3 = QVBoxLayout()
        col_3.addWidget(self.tools_label)
        col_3.addWidget(self.divider)
        col_3.addLayout(row_3)   
        col_3.addLayout(row_1)
        col_3.addWidget(self.button_YT_add)
        col_3.addWidget(self.button_YT_pl_add)
        col_3.addWidget(self.divider2)
        col_3.addWidget(self.field_search)
        col_3.addLayout(row_4)
        col_3.addWidget(self.divider3)
        col_3.addWidget(self.button_web_exec)
        col_3.addStretch()

        col_3.addWidget(self.descText, stretch = 1)
        col_3.addWidget(self.descBtn)

        col_3.addWidget(self.bottom_label_1)

        layout.addLayout(col_2, stretch = 2)
        layout.addLayout(col_1, stretch = 3)
        layout.addLayout(col_3, stretch = 2)

        self.list_groups.itemClicked.connect(self.get_webs)
        self.list_webs.itemClicked.connect(self.get_desc)
        self.list_webs.itemClicked.connect(self.url_defaulting)
        self.button_web_add.clicked.connect(self.add_web)
        self.button_web_del.clicked.connect(self.del_web)
        self.button_web_exec.clicked.connect(self.run_web)
        self.button_add.clicked.connect(self.add_group)
        self.button_del.clicked.connect(self.del_group)
        self.button_YT_add.clicked.connect(self.add_YT_vid)
        self.button_YT_pl_add.clicked.connect(self.add_YT_pl)
        self.button_search.clicked.connect(self.search)
        self.button_clear.clicked.connect(self.clear)
        self.descBtn.clicked.connect(self.save_desc)
        self.button_editWebUrl.clicked.connect(self.edit_web)
        self.button_editGroup.clicked.connect(self.edit_group)
        self.list_groups.addItems(self.collections)

    def initTab2(self):

        self.url_text = QLineEdit()
        self.url_text.setText(self.settings['default-url'])

        self.webview = QWebEngineView()
        self.webview.load(QUrl(self.settings['default-url']))
        self.webview.urlChanged.connect(self.url_changed)

        back_button = QPushButton("<")
        back_button.clicked.connect(self.webview.back)
        forward_button = QPushButton(">")
        forward_button.clicked.connect(self.webview.forward)
        self.refresh_button = QPushButton(self.loadLanguage2('refresh_button'))
        self.refresh_button.clicked.connect(self.webview.reload)

        self.go_button = QPushButton(self.loadLanguage2('search'))
        self.go_button.clicked.connect(self.url_set)

        self.home_btn = QPushButton(self.loadLanguage2('home'))
        self.home_btn.clicked.connect(self.loadDefaultUrl)

        toplayout = QHBoxLayout()
        toplayout.addWidget(back_button)
        toplayout.addWidget(forward_button)
        toplayout.addWidget(self.home_btn)
        toplayout.addWidget(self.refresh_button)
        toplayout.addWidget(self.url_text)
        toplayout.addWidget(self.go_button)       

        layout = QVBoxLayout()
        layout.addLayout(toplayout)
        layout.addWidget(self.webview)

        self.tab2.setLayout(layout)

    def initTab3(self):  
        languages = ['English', 'Español', 'Français', 'Deutsch', 'Português', 'Italiano', 'Русский', 'Euskara']
        self.langbox = QComboBox()
        for language in languages:
            self.langbox.addItem(language)
        self.langbox.setCurrentText(languages[self.settings['language']])

        layout = QVBoxLayout()

        self.options_label = QLabel(self.loadLanguage3('options_label'))
        self.options_label.setAlignment(Qt.AlignLeft)
        self.options_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.HLine) 
        layout.addWidget(self.options_label)
        layout.addWidget(self.divider)

        # Language selection
        self.lang_group = QGroupBox(self.loadLanguage3('language_label'))
        self.lang_group.setAlignment(Qt.AlignLeft)
        self.lang_layout = QVBoxLayout()
        self.lang_layout.addWidget(self.langbox)
        self.lang_group.setLayout(self.lang_layout)
        layout.addWidget(self.lang_group)

        # About & Help
        self.verLabel = QLabel(str("WebGroups ver: "+ self.settings['version']))
        self.about_group = QGroupBox(self.loadLanguage3('about_label'))  
        self.about_group.setAlignment(Qt.AlignLeft)    
        self.about_layout = QVBoxLayout()
        self.about_layout.addWidget(self.verLabel)
        self.taglayout = QLabel(self.loadLanguage3('about_text'))
        self.about_layout.addWidget(self.taglayout)
        self.about_group.setLayout(self.about_layout)
        layout.addWidget(self.about_group)

        # Default URL (already present)
        self.url_group = QGroupBox(self.loadLanguage3('default_url_label'))
        self.url_layout = QHBoxLayout()
        self.url_edit = QLineEdit()
        self.url_edit.setText(self.settings['default-url'])
        self.url_apply = QPushButton(self.loadLanguage3('url_apply'))
        self.url_layout.addWidget(self.url_edit)
        self.url_layout.addWidget(self.url_apply)
        self.url_group.setLayout(self.url_layout)
        layout.addWidget(self.url_group)

        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)
        self.tab3.setWidget(container)
        self.tab3.setWidgetResizable(True)


        self.langbox.currentTextChanged.connect(self.changeLang)
        self.url_apply.clicked.connect(self.setDefaultUrl)
        self.url_edit.setText(self.settings['default-url'])

    def loadDefaultUrl(self):
        self.url_text.setText(self.settings['default-url'])
        self.webview.load(QUrl(self.settings['default-url']))
        self.webview.urlChanged.connect(self.url_changed)

    def setDefaultUrl(self):
        self.settings['default-url'] = self.url_edit.text()
        with open('settings.json', 'w', encoding = 'utf-8') as file:
            json.dump(self.settings, file, ensure_ascii = False)
        self.webview.load(QUrl(self.url_text.text()))
        self.webview.urlChanged.connect(self.url_changed)
    
    def setLang(self,id):
        self.settings['language'] = id
        with open('settings.json', 'w', encoding = 'utf-8') as file:
            json.dump(self.settings, file, ensure_ascii = False)
        self.LanguagePack = self.LanguagePacks[self.settings['language']]
        self.list_webs_label.setText(self.loadLanguage('title'))
        self.list_groups_label.setText(self.loadLanguage('list_groups_label'))
        self.bottom_label_1.setText(self.loadLanguage3('about_text'))
        self.tools_label.setText(self.loadLanguage('options_label'))
        self.button_web_add.setText(self.loadLanguage('button_web_add'))
        self.button_YT_add.setText(self.loadLanguage('button_YT_add'))
        self.button_YT_pl_add.setText(self.loadLanguage('button_YT_pl_add'))
        self.button_web_del.setText(self.loadLanguage('button_web_del'))
        self.field_search.setPlaceholderText(self.loadLanguage('field_search'))
        self.button_search.setText(self.loadLanguage('button_search'))
        self.button_clear.setText(self.loadLanguage('button_clear'))
        self.button_web_exec.setText(self.loadLanguage('button_web_exec'))
        self.descBtn.setText(self.loadLanguage('descBtn'))
        self.go_button.setText(self.loadLanguage2('search'))
        self.refresh_button.setText(self.loadLanguage2('refresh_button'))
        self.home_btn.setText(self.loadLanguage2('home'))
        self.url_group.setTitle(self.loadLanguage3('default_url_label'))
        self.url_apply.setText(self.loadLanguage3('url_apply'))
        self.button_add.setText(self.loadLanguage('button_add'))
        self.button_del.setText(self.loadLanguage('button_del'))
        self.button_editGroup.setText(self.loadLanguage('button_editGroup'))
        self.button_editWebUrl.setText(self.loadLanguage('button_editWebUrl'))
        self.options_label.setText(self.loadLanguage3('options_label'))
        self.lang_group.setTitle(self.loadLanguage3('language_label'))
        self.list_groups_label.setText(self.loadLanguage('list_groups_label'))
        #self.theme_group.setTitle(self.loadLanguage3('theme_label'))
        #self.font_group.setTitle(self.loadLanguage3('font_size_label'))
        #self.startup_group.setTitle(self.loadLanguage3('startup_label'))
        #self.restore_session_chk.setText(self.loadLanguage3('restore_session'))
        #self.backup_group.setTitle(self.loadLanguage3('backup_label'))
        #self.export_btn.setText(self.loadLanguage3('export_data'))
        #self.import_btn.setText(self.loadLanguage3('import_data'))
        #self.notif_group.setTitle(self.loadLanguage3('notifications_label'))
        #self.notif_chk.setText(self.loadLanguage3('enable_notifications'))
        #self.webview_group.setTitle(self.loadLanguage3('web_preview_label'))
        #self.js_chk.setText(self.loadLanguage3('enable_js'))
        #self.privacy_group.setTitle(self.loadLanguage3('privacy_label'))
        #self.clear_data_btn.setText(self.loadLanguage3('clear_data'))
        self.about_group.setTitle(self.loadLanguage3('about_label'))
        self.taglayout.setText(self.loadLanguage3('about_text'))
        self.verLabel.setText(str("WebGroups ver: "+ self.settings['version']))

        

    def setStyle(self):
        style = self.styling.currentText()
        app = QApplication.instance()
        
        if style == 'Default':
            # Use Windows 11/10 modern style
            app.setStyle("windowsvista")
            
            # Enable modern Windows features if available
            try:
                # Import Windows specific API
                from ctypes import windll
                windll.dwmapi.DwmSetWindowAttribute(
                    int(self.winId()), 
                    20,  # DWMWA_USE_IMMERSIVE_DARK_MODE
                    byref(c_int(1)), 
                    sizeof(c_int)
                )
            except:
                pass  # Fallback if modern Windows features aren't available
                
        else:
            app.setStyle(style)

    def changeLang(self):
        if self.langbox.currentText() == 'English':
            self.setLang(0)
        elif self.langbox.currentText() == 'Español':
            self.setLang(1)
        elif self.langbox.currentText() == 'Français':
            self.setLang(2)
        elif self.langbox.currentText() == 'Deutsch':
            self.setLang(3)
        elif self.langbox.currentText() == 'Português':
            self.setLang(4)
        elif self.langbox.currentText() == 'Italiano':
            self.setLang(5)
        elif self.langbox.currentText() == 'Русский':
            self.setLang(6)
        elif self.langbox.currentText() == 'Euskara':           
            self.setLang(7)

    def url_changed(self):
        self.url_text.setText(self.webview.url().toString())

    def url_set(self):
        self.webview.setUrl(QUrl(self.url_text.text()))

    def url_defaulting(self):
        if self.list_webs.selectedItems():
            self.url_text.setText(str(self.collections[self.list_groups.selectedItems()[0].text()][self.list_webs.selectedItems()[0].text()]['URL']))
            self.webview.setUrl(QUrl(str(self.collections[self.list_groups.selectedItems()[0].text()][self.list_webs.selectedItems()[0].text()]['URL'])))

    def search(self):
        if self.list_groups.selectedItems():
            key = self.list_groups.selectedItems()[0].text()
            key_val = list(self.collections[key].keys())
            self.list_webs.clear()
            for i in range(len(key_val)):
                val = key_val[i]
                check = val.lower()
                if self.field_search.text() in check:
                    self.list_webs.addItem(key_val[i]) 

    def clear(self):
        if self.list_groups.selectedItems():
            key = self.list_groups.selectedItems()[0].text()
            self.list_webs.clear()
            self.list_webs.addItems(self.collections[key])

    def add_YT_pl(self):
        if self.list_groups.selectedItems():
            pl_url, ok = QInputDialog.getText(self.tab1, 'Add web', 'URL')
            if ok and pl_url != '':
                key = self.list_groups.selectedItems()[0].text()
                yt_play = Playlist(pl_url)
                for i in yt_play.videos:
                    self.collections[key][i.title] = {'URL': i.watch_url}
                    self.list_webs.addItem(i.title) 
                    self.len_text = self.loadLanguage("title") + ": " + str(len(self.collections[key]))
                    self.len_webs_label.setText(self.len_text)
        with open('webs_data.json', 'w', encoding = 'utf-8') as file:
            json.dump(self.collections, file, ensure_ascii = False)

    def add_YT_vid(self):
        if self.list_groups.selectedItems():
            vid_url, ok = QInputDialog.getText(self.tab1, 'Add web', 'URL')
            if ok and vid_url != '':
                key = self.list_groups.selectedItems()[0].text()
                r = requests.get(vid_url)
                soup = BeautifulSoup(r.text)
                link = soup.find_all(name="title")[0]
                title = str(link)
                title = title.replace("<title>","")
                title = title.replace("</title>","")
                self.collections[key][title] = {'URL': vid_url}
                self.list_webs.addItem(title) 
                self.len_text = self.loadLanguage("title") + ": " + str(len(self.collections[key]))
                self.len_webs_label.setText(self.len_text)
        with open('webs_data.json', 'w', encoding = 'utf-8') as file:
            json.dump(self.collections, file, ensure_ascii = False)

    def add_group(self):
        group_name, ok = QInputDialog.getText(self.tab1, 'New group', 'Name')
        if ok and group_name != '':
            self.collections[group_name] = {}
            self.list_groups.addItem(group_name)
        with open('webs_data.json', 'w', encoding = 'utf-8') as file:
            json.dump(self.collections, file, ensure_ascii = False)

    def del_group(self):
        if self.list_groups.selectedItems():
            key = self.list_groups.selectedItems()[0].text()
            del self.collections[key]
            self.list_webs.clear()
            self.list_groups.clear()
            self.list_groups.addItems(self.collections)
            self.len_webs_label.setText(self.loadLanguage("title") + ": 0")
            with open('webs_data.json', 'w', encoding = 'utf-8') as file:
                json.dump(self.collections, file, sort_keys = True)

    def edit_group(self):
        if self.list_groups.selectedItems():
            group_name, ok = QInputDialog.getText(self.tab1, 'Edit group', 'Name')
            if ok and group_name != '':
                key = self.list_groups.selectedItems()[0].text()
                self.collections[group_name] = self.collections[key]
                del self.collections[key]
                self.list_webs.clear()
                self.list_groups.clear()
                self.list_groups.addItems(self.collections)
        with open('webs_data.json', 'w', encoding = 'utf-8') as file:
            json.dump(self.collections, file, ensure_ascii = False)

    def add_web(self):
        if self.list_groups.selectedItems():
            web_name, ok = QInputDialog.getText(self.tab1, 'Add web', 'Name')
            web_url, ok = QInputDialog.getText(self.tab1, 'Add web', 'URL')
            if ok and web_name != '' and web_url != '':
                key = self.list_groups.selectedItems()[0].text()
                self.collections[key][web_name] = {'URL': web_url, 'Description': ''}
                self.list_webs.addItem(web_name) 
                self.len_text = self.loadLanguage("title") + ": " + str(len(self.collections[key]))
                self.len_webs_label.setText(self.len_text)
        with open('webs_data.json', 'w', encoding = 'utf-8') as file:
            json.dump(self.collections, file, ensure_ascii = False)

    def edit_web(self):
        if self.list_groups.selectedItems():
            web_url, ok = QInputDialog.getText(self.tab1, 'Edit web', 'URL')
            if ok and web_url != '':
                key = self.list_groups.selectedItems()[0].text()
                key2 = self.list_webs.selectedItems()[0].text()
                self.collections[key][key2]['URL'] = web_url
        with open('webs_data.json', 'w', encoding = 'utf-8') as file:
            json.dump(self.collections, file, ensure_ascii = False)

    def del_web(self):
        if self.list_webs.selectedItems():
            key = self.list_groups.selectedItems()[0].text()
            key2 = self.list_webs.selectedItems()[0].text()
            del self.collections[key][key2]
            self.list_webs.clear()
            self.list_groups.clear()
            self.list_webs.addItems(self.collections[key])
            self.list_groups.addItems(self.collections)
            self.len_text = self.loadLanguage("title") + ": " + str(len(self.collections[key]))
            self.len_webs_label.setText(self.len_text)
            with open('webs_data.json', 'w', encoding = 'utf-8') as file:
                json.dump(self.collections, file, ensure_ascii = False)

    def get_desc(self):
        if self.list_webs.selectedItems():
            key = self.list_groups.selectedItems()[0].text()
            key1 = self.list_webs.selectedItems()[0].text()
            if 'Description' not in self.collections[key][key1]:
                self.collections[key][key1]['Description'] = ''
            desc = self.collections[key][key1]['Description']
            self.descText.setText(desc)

    def save_desc(self):
        if self.list_groups.selectedItems():
            key = self.list_groups.selectedItems()[0].text()
            key1 = self.list_webs.selectedItems()[0].text()
            desc = self.descText.toPlainText()
            self.collections[key][key1]['Description'] = desc
            with open('webs_data.json', 'w', encoding = 'utf-8') as file:
                json.dump(self.collections, file, ensure_ascii = False)

    def run_web(self):
        if self.list_webs.selectedItems():
            key = self.list_groups.selectedItems()[0].text()
            key2 = self.list_webs.selectedItems()[0].text()
            wb.open(self.collections[key][key2]['URL'])

    def get_webs(self):
        if self.list_groups.selectedItems():
            key = self.list_groups.selectedItems()[0].text()             
            with open('webs_data.json', 'r', encoding = 'utf-8') as file:
                self.collections = json.load(file)
            self.list_webs.clear()
            self.list_webs.addItems(self.collections[key])
            self.len_text = self.loadLanguage("title") + ": " + str(len(self.collections[key]))
            self.len_webs_label.setText(self.len_text)

    def apply_theme(self):
        theme = self.theme_combo.currentText()
        app = QApplication.instance()
        if theme == "Dark":
            dark_palette = QPalette()
            dark_palette.setColor(QPalette.Window, QColor(35, 38, 41))
            dark_palette.setColor(QPalette.WindowText, Qt.white)
            dark_palette.setColor(QPalette.Base, QColor(49, 54, 59))
            dark_palette.setColor(QPalette.AlternateBase, QColor(35, 38, 41))
            dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
            dark_palette.setColor(QPalette.ToolTipText, Qt.white)
            dark_palette.setColor(QPalette.Text, Qt.white)
            dark_palette.setColor(QPalette.Button, QColor(49, 54, 59))
            dark_palette.setColor(QPalette.ButtonText, Qt.white)
            dark_palette.setColor(QPalette.BrightText, Qt.red)
            dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(dark_palette)
        else:
            app.setPalette(app.style().standardPalette())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tabWidgetApp = WebGroups()
    tabWidgetApp.show()
    sys.exit(app.exec())