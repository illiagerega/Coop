from Util.MapController import Map
from CarController import CarDriver
import matplotlib.pyplot as plt

def main():
    plt.rcParams["figure.figsize"] = [5, 5]



#Короче я зробив якусь фігню з тим шоб воно тут показувало як машинки їдуть, без анімацій но показує (побачиш як),
# ще я наварганив повну діч шоб було декілька Полос, але поняв шо воно вообще не так маэ бути, але поки що, сойдет

# Крім того,
#Якогось фіга, коли я роблю більше спавпоінтів вилітає помилка, хз чого
#Вообщем.... как-то так

# А і ще, там в мапКонтроллері, коли ліній більше ніж одна я добавив якись костиль, я хз чи воно файно



    Map.init("test.txt")

    CarDriver.init()
    for node in CarDriver.cars_array[0].way:
        print(node)

    print()
    print()
    print("Simulation: ")
    print()
    print()


    colors = ['r*', 'b*', 'y*', 'g*']


    for i in range(50):


        for node in Map.nodes:
            plt.plot(node.apos[0], node.apos[1], marker=".", markersize=40)
        for road in Map.roads:
            # Тут багато тупого коду, якого вообще треба забрати звідси, но пофіг, пусть буде, вообщем
            cnt = 0
            for line in road.lines[road.start_node]:
                x_values = []
                y_values = []

                x1 = Map.nodes[line.start_node].apos[0]
                x2 = Map.nodes[line.end_node].apos[0]

                y1 = Map.nodes[line.start_node].apos[1]
                y2 = Map.nodes[line.end_node].apos[1]

                x_values.extend([x1, x2])
                y_values.extend([y1 , y2 ])
                plt.plot(x_values, y_values, "#7D3C98") # purple
                cnt += 1
            for line in road.lines[road.end_node]:
                x_values = []
                y_values = []
                x1 = Map.nodes[line.start_node].apos[0]
                x2 = Map.nodes[line.end_node].apos[0]

                y1 = Map.nodes[line.start_node].apos[1]
                y2 = Map.nodes[line.end_node].apos[1]

                print(x1, x2, y1 ,y2)
                #okay, i will just go through every possibility
                # не обращай вніманія, тут я грався і радувався життю
                x_res = -1
                distance_between_line = 0.03

                if x2 > x1 and y1 == y2:
                    x_res = 0
                    y_res = distance_between_line * 2
                elif x2 > x1 and y2 > y1:
                    x_res = -distance_between_line
                    y_res = distance_between_line
                elif x2 == x1 and y2 > y1:
                    x_res = -distance_between_line  * 2
                    y_res = 0
                elif x2 < x1 and y2 > y1:
                    x_res = -distance_between_line
                    y_res = -distance_between_line
                elif x2 < x1 and y2 == y1:
                    x_res = 0
                    y_res = -distance_between_line * 1
                elif x2 < x1 and y2 < y1:
                    x_res = distance_between_line
                    y_res  = -distance_between_line
                elif x1 == x2 and y2 < y1:
                    x_res = distance_between_line *2
                    y_res = 0
                elif x2 > x1 and y2 < y1:
                    x_res = distance_between_line
                    y_res = distance_between_line
                else:
                    raise Exception("something went wrong")

                x_values.extend([x1 + x_res*cnt, x2 + x_res*cnt])
                y_values.extend([y1 + y_res*cnt, y2 + y_res*cnt])
                plt.plot(x_values, y_values, "#2471A3") # blue
                cnt+=1
            print()
            print()

        color = 0
        for car in CarDriver.cars_array:
            #print(car.x)
            #print(car.getLines()[car.currentLine])
            #print(car.getCoordinates())
            plt.plot(car.getCoordinates()[0][0], car.getCoordinates()[0][1], colors[color])
            color = (color + 1) % 4



        CarDriver.comp()
        print()
        print()

        plt.show()
        plt.cla()



if __name__ == "__main__":
    main()
