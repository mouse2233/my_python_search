import sys  # библиотека для работы с файлами

myIpList = []  # массив ip адресов


# главная функция чтения
def readMyFile(name, version):
    myIpList.clear()  # массив ip адресов
    if version == "4":
        # попытка открыть файл
        try:
            f = open(name + '.txt', 'r')
            # если открыли читаем пока не кончился
            while True:
                line = f.readline()

                # Далее идут различного вида проверки
                # Вариантов реагирования на ошибку в написании 2:
                # 1 - выкинуть ValueError
                # 2 - пропустить битую строку
                # выбран вариант 1

                if not line:  # файл закончился?
                    if len(myIpList) == 0:
                        raise ValueError("файл пустой")
                    f.close()
                    break
                temp = line.rstrip().split(".")
                if len(temp) == 4:  # точно 4 блока в IP?
                    # Все цифры?
                    if temp[0].isdigit() and temp[1].isdigit() and temp[2].isdigit() and temp[3].isdigit():
                        # Интервал от 0 до 255?
                        if 0 <= int(temp[0]) < 256 and 0 <= int(temp[1]) < 256 and 0 <= int(temp[2]) < 256 \
                                and 0 <= int(temp[3]) < 256:
                            myIpList.append(temp)
                        else:
                            f.close()
                            raise ValueError("не все блоки попадают в границы")
                    else:
                        f.close()
                        raise ValueError("не все блоки являются цифрами")
                else:
                    f.close()
                    raise ValueError("неправильное к-во блоков в IP")

        except OSError:
            raise ValueError("файл " + name + " не найден")
    elif version == 6:
        print("не сегодня друзья, не сегодня")
    else:
        print("Версия не распознана, передайте 4 для IPV4 6 для IPV6")


def convertNumber(num):
    temp = str(bin(num))[2:]
    # на выходе можем получить число не подходящее под формат ####_#### (не октет)
    while len(temp) < 8:
        # исправляем несправедливость если она присутствует
        temp = "0" + temp
    return temp


def byteToStr(num):
    num = int(num, 2)
    return num


def findType(my_min, ny_max, level):
    # согласен, можно запихнуть это в int и доставать расчетом но и так сойдет...
    name_pref = ["31", "30", "29", "28", "27", "26", "25", "24", "23", "22", "21", "20", "19", "18", "17", "16", "15",
                 "14", "13", "12", "11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1", "0"]
    my_min = convertNumber(my_min)
    ny_max = convertNumber(ny_max)

    # АХТУНГ, пример!
    # Берем 2 числа и ведем поиск отличий (160 и 166)
    # 1 0 1 0 0 0 1 1
    # 1 0 1 0 0 1 1 0
    # _ _ _ _ _ * * * <-отличия чисел
    # 1 1 1 1 1 0 0 0 <- первый  IP 160

    # собрать постфикс
    deep = 0  # определяем базовый IP
    my_pref = ""
    for my_i in range(len(my_min)):
        if my_min[my_i] != ny_max[my_i]:
            my_pref = name_pref[7 - my_i + level]
            deep = my_i
            break
    # собрать число и вернуть его
    num = ""
    for my_j in range(deep):
        num += my_min[my_j]
    for my_j in range(8 - deep):
        num += "0"
    return byteToStr(num), my_pref


def main(p1, p2):
    readMyFile(p1, p2)
    m_stat = [[255, 0], [255, 0], [255, 0], [255, 0]]  # массив с максимальным и минимальным числом
    for i in range(len(myIpList)):
        # проверка на максимум в 1 октете
        for j in range(4):
            if int(myIpList[i][j]) < m_stat[j][0]:
                m_stat[j][0] = int(myIpList[i][j])
            # проверка на минимум в 1 октете
            if int(myIpList[i][j]) > m_stat[j][1]:
                m_stat[j][1] = int(myIpList[i][j])
    # проверка на отличающиеся IP в 1 и т.д. октете
    # + фактический ответ формируется тут
    if m_stat[0][0] != m_stat[0][1]:  # для 1 октата
        mint, pref = findType(m_stat[0][0], m_stat[0][1], 24)
        print(str(mint) + ".0.0.0/" + str(pref))
        return str(mint) + ".0.0.0/" + str(pref)
    elif m_stat[1][0] != m_stat[1][1]:  # для 2 октата
        mint, pref = findType(m_stat[1][0], m_stat[1][1], 16)
        print(str(m_stat[0][0]) + "." + str(mint) + "." + ".0.0/" + str(pref))
        return str(m_stat[0][0]) + "." + str(mint) + "." + ".0.0/" + str(pref)
    elif m_stat[2][0] != m_stat[2][1]:  # для 3 октата
        mint, pref = findType(m_stat[2][0], m_stat[2][1], 8)
        print(str(m_stat[0][0]) + "." + str(m_stat[1][0]) + "." + str(mint) + ".0/" + str(pref))
        return str(m_stat[0][0]) + "." + str(m_stat[1][0]) + "." + str(mint) + ".0/" + str(pref)
    elif m_stat[3][0] != m_stat[3][1]:  # для 4 октата
        mint, pref = findType(m_stat[3][0], m_stat[3][1], 0)
        print(str(m_stat[0][0]) + "." + str(m_stat[1][0]) + "." + str(m_stat[2][0]) + "." + str(mint) + "/" + str(pref))
        return str(m_stat[0][0]) + "." + str(m_stat[1][0]) + "." + str(m_stat[2][0]) + "." + str(mint) + "/" + str(pref)
        # для исключения октата
    elif m_stat[0][0] == m_stat[0][1] and m_stat[1][0] == m_stat[1][1] and m_stat[2][0] == m_stat[2][1] \
            and m_stat[3][0] == m_stat[3][1]:
        print(str(m_stat[0][0]) + "." + str(m_stat[1][0]) + "." + str(m_stat[2][0]) + "." + str(m_stat[3][0]) + "/32")
        return str(m_stat[0][0]) + "." + str(m_stat[1][0]) + "." + str(m_stat[2][0]) + "." + str(m_stat[3][0]) + "/32"


if __name__ == '__main__':
    # Идея приложения максимально простая, найти максимальный и минимальный IP указанный в текстовом файле
    # найденные IP разобрать и подобрать подсеть так, чтобы все влезли

    # согласен, byte для октета хватило бы, интами мне удобнее

    answer = ""  # для сборки ответа
    # точно получили 2 аргумента?
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        # main("D:\\ipv4", "4")
        raise ValueError("Неверные параметры запуска")
