import re
from os.path import getsize as get_file_size


# Класс Машина Тьюринга
class TM():
    # Конструктор класса с одним параметром - программой
    def __init__(self, program):
        self.program = program
        self.output_display = None

    # Запуск Машины Тьюринга
    def run(self, input_word):
        # Добавляем входное слово в список и преписываем в начало и в конец символ "пусто"
        word = list(input_word)
        word.append("^")
        word.insert(0, "^")
        print("Входное слово:", word)

        head_position = 1  # положение читающе-записывающей головки
        q_m = 1  # состояние машины

        # Счётчик тактов
        tact_counter = 0

        # Основной цикл программы
        while q_m != 0:  # машина работает, пока состояние машины не нулевое
            instruction_found = False  # Будет равна True, если инструкция будет найдена
            for instruction in self.program:
                s0, q0, s, q, w = instruction.get_instruction()
                # Если начальное состояние машины не совпадает с начальным состоянием инструкции,
                #  то берём следующую инструкцию
                if q0 != q_m:
                    continue
                # Если видимый символ машины не совпадает с начальным символом в инструкции,
                #  то берём следующую инструкцию
                if s0 != word[head_position]:
                    continue

                word[head_position] = s
                q_m = q
                head_position += w
                instruction_found = True

                # Проверяем, что по краям ленты стоят "пустые" символы
                if word[0] != '^':
                    word.insert(0, "^")
                    head_position += 1
                if word[len(word) - 1] != '^':
                    word.append('^')

                # Выведем действие на output_display
                if self.output_display is not None:
                    if w == 1:
                        way = 'R'
                    elif w == -1:
                        way = 'L'
                    else:
                        way = 'N'
                    tact_counter += 1

                    word_str = ""
                    result = re.findall(r'\d+', str(word))
                    for i in result:
                        word_str += i

                    self.output_display.addItem('{0:>20}{1:>30}{2:>30}{3:>35}{4:>35}{5:>35}             {6:<35}'
                                        .format(tact_counter, s0, 'q' + str(q0), s, 'q' + str(q), way, word_str))

                # Остановим поиск по списку инструкций - необходимая инструкция уже найдена
                break

            if  instruction_found is False:
                print("Ошибка! Инструкция не найдена!")
                return "Ошибка! Инструкция не найдена!"
        output_word = ""
        for i in word[1:-1]:
            output_word += i
        return output_word

    # Установить выходной дисплей
    def setOutputDisplay(self, outputDisplay):
        self.output_display = outputDisplay


# Класс Программа, который хранит инструкции для класса Машина Тьюринга
class Program:
    # Список инструкций
    instructions = []
    # Описание программы
    description = ""
    # Алфавит
    alphabet = ""
    # Количество состояний
    condition_length = 0

    # Установить инструкции
    # Проверяет, все ли элементы списка являются объектами класса Instruction
    # Если нет, то вызывается исключение TMExceptions
    def set_instructions(self, instructions):
        for i in instructions:
            if type(i) != Instruction:
                raise TMExceptions("Попытка записать в класс Program объект класса не Instruction")
        self.instructions = instructions

    # Установить алфавит и число состояний
    def set_alphabet_condition_length(self, alphabet, condition_length):
        self.alphabet = alphabet
        self.condition_length = condition_length

    # Установить описание программы
    def set_description(self, text):
        if type(text) == str:
            self.description = text
        else:
            raise TMExceptions("Попытка записать Program.description не тип str")

    # Получить количество инструкций
    def get_instructions_count(self):
        if self.instructions is not None:
            return len(self.instructions)
        else:
            return 0

    # Загрузить программу из файла
    def load_instructions(self, path):
        file_size = get_file_size(path)
        if file_size == 0:
            raise TMExceptions("Попытка открыть пустой файл!")
        # Откроем файл
        file = open(path)
        try:
            # Прочитаем строку - алфавит
            line = file.readline()
            self.alphabet = line.rstrip()
            # Прочитаем строку - количество состояний
            line = file.readline()
            self.condition_length = int(line.rstrip())
            # Прочитаем строку - количество инструкций
            line = file.readline()
            count = int(line.rstrip())
            # Прочитаем следующие count строк - count инструкций. Запишем их
            for i in range(count):
                line = file.readline()
                line = (line.rstrip()).split(' ')
                configuration = line[0] + ',' + line[1]
                action = line[2] + ',' + line[3] + ',' + line[4]
                self.instructions.append(Instruction(configuration, action))
            # Прочитаем описание программы
            line = file.readline()
            if line != '':
                self.description = line
            for i in self.instructions:
                print(i.get_instruction())
        except IndexError:
            raise TMExceptions("Program.load_instructions: ошибка чтения файла! Файл повреждён!")
        finally:
            # Закроем файл
            file.close()

    # Сохранить программу в файл
    def save_instructions(self, path):
        file = open(path, 'w')
        file.write(self.alphabet + '\n')
        file.write(str(self.condition_length) + '\n')
        file.write(str(self.get_instructions_count()) + '\n')
        for instruction in self.instructions:
            values = list(instruction.get_instruction())
            for i in values:
                file.write(str(i) + ' ')
            file.write('\n')
        if self.description is not None:
            file.write(self.description)
        file.close()


# Класс Инcтрукция
class Instruction:
    # Конструктор класса
    def __init__(self, configuration, action):
        # Проверим кооректность configuration<current_value, current_condition>

        # configuration должна быть строкой
        if type(configuration) != str:
            # Вызываем исключение
            raise TMExceptions("Входной параметр configuration должен иметь тип str!")
        # Посчитаем количество запятых, их должно быть ровно 1, иначе ошибка
        comma_count = re.findall(r',', configuration)
        if len(comma_count) != 1:
            # Вызываем исключение
            raise TMExceptions("Входной параметр configuration должен иметь ровно одну запятую!")
        # Удалим все пробелы в строке
        configuration = re.sub(r' ', '', configuration)
        # Разделим строку на две переменных
        self.current_value, self.current_condition = configuration.split(",")
        # Проверим, коректно ли введено текущее значение ячейки: в переменной должен быть записан ровно 1 символ
        if len(self.current_value) != 1:
            # Вызываем исключение
            raise TMExceptions("current_condition может содержать только один символ 'q' и цифры,"
                               " либо только цифры!")
        # Проверим, коректно ли введено значение нового состояния
        search_letters_result = re.findall(r'\D', self.current_condition)
        # current_condition может содержать только один символ 'q' и цифры, либо только цифры
        if len(search_letters_result) > 1:
            # Вызываем исключение
            raise TMExceptions("current_condition может содержать только один символ 'q' и цифры,"
                               " либо только цифры!")
        # Символ один и не яв-я Q или q, то ошибка
        if len(search_letters_result) == 1 and self.current_condition[0] != 'q' and\
                self.current_condition[0] != "Q":
            # Вызываем исключение
            raise TMExceptions("current_condition может содержать только один символ 'q' и цифры,"
                               " либо только цифры!")
        # Ищем все цифры в current_condition
        search_numbers_result = re.findall(r'\d+', self.current_condition)
        # Если не найдено ни одной, то ошибка
        if len(search_numbers_result) == 0:
            # Вызываем исключение
            raise TMExceptions("current_condition должен содержать число - номер текущего состояния машины!")
        # В current_condition записываем лишь число - номер текущего состояния
        self.current_condition = int(search_numbers_result[0])


        # Проверим кооректность action<value, condition, position>

        # action должна быть строкой
        if type(action) != str:
            # Вызываем исключение
            raise TMExceptions("Входной параметр action должен иметь тип str!")
        # Посчитаем количество запятых, их должно быть ровно 2, иначе ошибка
        comma_count = re.findall(r',', action)
        if len(comma_count) != 2:
            # Вызываем исключение
            raise TMExceptions("action должен содержать ровно 2 запятые!")
        # Удалим все пробелы в строке
        action = re.sub(r' ', '', action)
        # Разделим строку на три переменных
        self.value, self.condition, self.position = action.split(",")
        # Проверим, коректно ли введено новое значение ячейки
        if len(self.value) != 0 and len(self.value) != 1:
            # Вызываем исключение
            raise TMExceptions("value должен содержать ровно 1 символ, либо быть вообще пустым!")
        # Если значение value пустое, значит оно равно current_value
        # self.value = self.current_value
        # Проверим, корректна ли новая позиция. Из множества доступных вариантов приведём к каноническому виду
        if self.position == "L" or self.position == "l" or self.position == '-1' or self.position == '-':
            self.position = -1
        elif self.position == "R" or self.position == "r" or self.position == '1' or self.position == '+':
            self.position = 1
        elif self.position == "N" or self.position == "n" or self.position == '0' or self.position == '':
            self.position = 0
        else:
            # Вызываем исключение
            raise TMExceptions("Направление смещения введено не корректно!")
        # Проверим, коректно ли введено значение нового состояния
        search_letters_result = re.findall(r'\D', self.condition)
        # Если больше 1 символа(не цифры), то ошибка
        if len(search_letters_result) > 1:
            # Вызываем исключение
            raise TMExceptions("Значение нового состояния машины может содержать только один символ 'q' и цифры,"
                               " либо только цифры!")
        # Символ один и не яв-я Q или q, то ошибка
        if len(search_letters_result) == 1 and self.condition[0] != 'q' and self.condition[0] != "Q":
            # Вызываем исключение
            raise TMExceptions("Значение нового состояния машины может содержать только один символ 'q' и цифры,"
                               " либо только цифры!")
        # Ищем все цифры в condition
        search_numbers_result = re.findall(r'\d+', self.condition)
        # Если записан лишь сивол 'q', то ошибка
        if len(search_letters_result) != 0 and len(search_numbers_result) == 0:
            # Вызываем исключение
            raise TMExceptions("Значение нового состояния машины может содержать только один символ 'q' и цифры,"
                               " либо только цифры!")
        # В новое состояние записываем только число
        if len(search_numbers_result) != 0:
            self.condition = int(search_numbers_result[0])
        # Если строка пустая, то старое состояние машины
        else:
            self.condition = self.current_condition

    # Получить инструкцию
    def get_instruction(self):
        return (self.current_value, self.current_condition, self.value, self.condition, self.position)


# Класс исключений для Машины Тьюринга
class TMExceptions(Exception):
    def __init__(self, error_message):
        self.error_message = error_message






# Тестирование модуля


if __name__ == '__main__':
    program1 = []
    program1.append(Instruction('0, 1', '1, 1, 1'))
    program1.append(Instruction('1, 1', '0, 1, 1'))
    program1.append(Instruction('^, 1', '^, 2, -1'))
    program1.append(Instruction('0, 2', '0, 2, -1'))
    program1.append(Instruction('1, 2', '1, 2, -1'))
    program1.append(Instruction('^, 2', '^, 0, 1'))

    program = Program()
    print(program.get_instructions_count())
    program.set_instructions(program1)
    program.set_alphabet_condition_length("01^", 2)
    program.set_description("Машина заменит все 1 на 0, а все 0 на 1")
    program.save_instructions("program1.tmprog")
    program.load_instructions("program1.tmprog")



    tm1 = TM(program1)
    tm1.set_input_word('1001')
    tm1.start()
