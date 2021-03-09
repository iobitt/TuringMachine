from Ui_MainWindow import Ui_MainWindow

from PyQt5.QtWidgets import QMainWindow, QWidget, QErrorMessage, QTableWidgetItem, QListWidget, QListWidgetItem,\
    QFileDialog, QMessageBox

from PyQt5.QtGui import QIcon

from PyQt5 import QtTest

from TM_v2 import TM, Instruction, Program, TMExceptions

from time import sleep


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        # Инициализация
        QMainWindow.__init__(self)
        self.setupUi(self)
        # Установим значок программы
        self.setWindowIcon(QIcon("TM.png"))
        # Установим заголовок программы
        self.setWindowTitle("Turing Machine")
        # Создадим объект класса программа
        self.program = Program()
        # Настройка tabWidget
        self.tabWidget.setTabText(0, "Запуск машины")
        self.tabWidget.setTabText(1, "Настройка машины")
        # pushButton
        self.pushButton.clicked.connect(self.create_table)
        # tableWidget
        # Событие возникающее при изменении ячейки
        # self.tableWidget.cellChanged.connect(self.cell_changed)
        # action
        self.action.triggered.connect(self.open_save_file_dialog)
        # action_2
        self.action_2.triggered.connect(self.load_program)
        # pushButton_3
        self.pushButton_3.clicked.connect(self.write_instructions)
        # pushButton_2
        self.pushButton_2.clicked.connect(self.run_machine)  # запуск машины
        # pushButton_4
        self.pushButton_4.clicked.connect(self.clear_console)  # отчистка консоли

    # Создаёт таблицу
    def create_table(self):
        if len(self.lineEdit.text()) == 0 or len(self.lineEdit_2.text()) == 0:
            error_message = QErrorMessage()
            error_message.setWindowTitle("Ошибка!")
            error_message.showMessage("Все поля должны быть заполнены!")
            error_message.exec()
        else:
            # Установим и подпишем строки
            try:
                row_count = int(self.lineEdit_2.text())
                self.tableWidget.setRowCount(row_count)
                self.tableWidget.setVerticalHeaderLabels(["q" + str(x + 1) for x in range(row_count)])
                # Установим и подпишем столбцы
                alphabet = list(self.remove_duplicate_characters(self.lineEdit.text()))
                # alphabet.append("^")
                column_count = len(alphabet)
                self.tableWidget.setColumnCount(column_count)
                self.tableWidget.setHorizontalHeaderLabels([alphabet[x] for x in range(column_count)])
            except ValueError:
                error_message = QErrorMessage()
                error_message.setWindowTitle("Ошибка!")
                error_message.showMessage("В поле число состояний должно быть целое число!")
                error_message.exec()

    # Срабатывает при изменении ячейки в таблице
    # def cell_changed(self, row, column):
    #     try:
    #         print("Ячейка изменена!")
    #         print("Строка", row)
    #         print("Столбец", column)
    #         cell_value = self.tableWidget.cellWidget(row, column).text()
    #         configuration = self.tableWidget.horizontalHeaderItem(column).text() + "," + str(row)
    #         print("Инструкция", configuration, cell_value)
    #         self.program.instructions[row + 1][column] = Instruction(configuration, cell_value)
    #         self.print_instructions()
    #     except TMExceptions as TMExc:
    #         print("Сработало исключение TMExceptions")
    #         error_message = QErrorMessage()
    #         error_message.setWindowTitle("Ошибка!")
    #         error_message.showMessage(TMExc.error_message)
    #         error_message.exec()
    #         self.tableWidget.setItem(row, column, QTableWidgetItem(",,"))
    #     except IndexError:
    #         print("Сработало исключение IndexError")

    def print_instructions(self):
        for i in range(len(self.program.instructions)):
            for j in range(len(self.program.instructions[i])):
                if self.program.instructions[i][j] == "":
                    print("%15s" % "Null", end=" ")
                elif type(self.program.instructions[i][j]) == Instruction:
                    print("%15s" % (str(self.program.instructions[i][j].value) + ',' +
                               str(self.program.instructions[i][j].condition) + ',' +
                               str(self.program.instructions[i][j].position)), end=" ")
                else:
                    print("%15s" % self.program.instructions[i][j], end=" ")
            print("\n")

    def open_save_file_dialog(self):
        save_file_dialog = QFileDialog(self)
        file_path = save_file_dialog.getSaveFileName(self, "Сохранить программу Машины Тьюринга", "",
                                                    "Turing Machine Program (*.tmprog);;All Files (*)")
        file_path = file_path[0]
        if file_path == "":
            return
        self.program.save_instructions(file_path)

    def load_program(self):
        try:
            open_file_dialog = QFileDialog(self)
            file_path = open_file_dialog.getOpenFileName(self, "Загрузить программу Машины Тьюринга", "",
                                                         "Turing Machine Program (*.tmprog);;All Files (*)")
            file_path = file_path[0]
            # Если путь пустой, то выходим из функции
            if file_path == "":
                return
            self.program.load_instructions(file_path)
            #
            self.lineEdit.setText(self.program.alphabet)
            self.lineEdit_2.setText(str(self.program.condition_length))
            # Загрузим описание программы
            self.textEdit.clear()
            self.textEdit.insertPlainText(self.program.description)
            # Запишем данные в listWidget
            row_count = self.program.condition_length
            self.tableWidget.setRowCount(row_count)
            self.tableWidget.setVerticalHeaderLabels(["q" + str(x + 1) for x in range(row_count)])
            # Установим и подпишем столбцы
            alphabet = list(self.program.alphabet)
            # alphabet.append("^")
            column_count = len(alphabet)
            self.tableWidget.setColumnCount(column_count)
            self.tableWidget.setHorizontalHeaderLabels([alphabet[x] for x in range(column_count)])

            for instruction in self.program.instructions:
                s0, q0, s, q, w = instruction.get_instruction()
                row = q0
                column = alphabet.index(s0)
                if w == 1:
                    way = 'R'
                elif w == -1:
                    way = 'L'
                else:
                    way = 'N'
                action = str(s) + "," + str(q) + "," + way
                self.tableWidget.setItem(row - 1, column, QTableWidgetItem(action))
        except TMExceptions as TMExc:
            error_message = QMessageBox()
            error_message.setWindowIcon(QIcon("TM.png"))
            error_message.setWindowTitle("Ошибка!")
            error_message.setIcon(QMessageBox.Warning)
            error_message.setText(TMExc.error_message)
            error_message.exec()

    # Удаляет повторяющиеся символы в строке
    def remove_duplicate_characters(self, string):
        new_string = ""
        for i in string:
            try:
                new_string.index(i)
            except ValueError:
                new_string += i
        return new_string

    # Запись инструкций из таблицы в объект Program
    def write_instructions(self):
        instructions = []
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                action = self.tableWidget.item(i, j)
                print(action)
                if action is not None and action.text() != "":
                    action = action.text()
                    configuration = self.tableWidget.horizontalHeaderItem(j).text() + "," + str(i + 1)
                    instructions.append(Instruction(configuration, action))
        self.program = Program()
        self.program.set_instructions(instructions)
        description = self.textEdit.toPlainText()
        if description != "":
            self.program.set_description(description)
        for i in self.program.instructions:
            print(i.get_instruction())
        condition_length = int(self.lineEdit_2.text())
        alphabet = self.remove_duplicate_characters(self.lineEdit.text())
        self.program.set_alphabet_condition_length(alphabet, condition_length)

    # Запуск машины
    def run_machine(self):
        # Если входное слово равно пустой строке, то ошибка
        input_word = self.lineEdit_3.text()
        if input_word == "":
            error_message = QMessageBox()
            error_message.setWindowIcon(QIcon("TM.png"))
            error_message.setWindowTitle("Ошибка!")
            error_message.setIcon(QMessageBox.Warning)
            error_message.setText("Для продолжения необходимо ввести входное слово!")
            error_message.exec()
            return

        self.listWidget.addItem("\nЗапуск машины:")
        self.listWidget.addItem("Входное слово:   " + input_word)
        tm = TM(self.program.instructions)  # Инициализируем машину программой
        tm.setOutputDisplay(self.listWidget)  # Передаём ссылку на listWidget для отображения работы машины
        self.listWidget.addItem('{0:<20}{1:<20}{2:<20}{3:<20}{4:<20}{5:<20}{6:<20}'
                                .format("№ такта", "Старый символ", 'Старое состояние', "Новый символ",
                                        'Новое состояние', "Направление", "Лента"))
        self.listWidget.addItem("Выходное слово:   " + tm.run(input_word))  # Запускаем машину

    # Отчитска консоли
    def clear_console(self):
        self.listWidget.clear()





