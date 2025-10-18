import math
from typing import List, Tuple

class CPolygon:
    def __init__(self, vertices):
        self.vertices = vertices
        if not self.is_convex():
            print("Not a convex polygon")
    def is_convex(self) -> bool:
        n = len(self.vertices)
        sign = None
        for i in range(n):
            a1 = self.vertices[i]
            o = self.vertices[(i + 1) % n]
            a2 = self.vertices[(i + 2) % n]
            cross = CPolygon.cp(a1, o, a2)
            if abs(cross) < 1e-10:
                continue
            if sign is None:
                sign = 1 if cross > 0 else -1
            else:
                cross_sign = 1 if cross > 0 else -1
                if cross_sign != sign:
                    return False
        return True
    @staticmethod
    def cp(a1, o, a2) -> float:
        return (a1[0] - o[0]) * (a2[1] - o[1]) - (a1[1] - o[1]) * (a2[0] - o[0])
    def perimeter(self) -> float:
        perimeter = 0.0
        n = len(self.vertices)
        for i in range(n):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % n]
            perimeter += math.sqrt((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2)
        return perimeter
    def area(self) -> float:
        n = len(self.vertices)
        area = 0.0
        for i in range(n):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % n]
            area += v1[0] * v2[1] - v2[0] * v1[1]
        return abs(area) / 2.0
    def triangulation(self) -> List[Tuple[float, float]]:
        if len(self.vertices) < 3:
            return []
        triangles = []
        first_vertex = self.vertices[0]
        for i in range(1, len(self.vertices) - 1):
            triangle = [first_vertex, self.vertices[i], self.vertices[i + 1]]
            triangles.append(triangle)
        return triangles
    def contain_point(self, point) -> bool:
        n = len(self.vertices)
        sign = None
        for i in range(n):
            a1 = self.vertices[i]
            a2 = self.vertices[(i + 1) % n]
            cross = CPolygon.cp(a1, a2, point)
            if abs(cross) < 1e-10:
                continue
            if sign is None:
                sign = 1 if cross > 0 else -1
            else:
                cross_sign = 1 if cross > 0 else -1
                if cross_sign != sign:
                    return False
        return True
    def contain_polygon(self, polygon) -> bool:
        for i in range(len(polygon.vertices)):
            if not self.contain_point(polygon.vertices[i]):
                return False
        return True

def is_polygon_convex(vertices: List[Tuple[float, float]]) -> bool:
    temp_polygon = CPolygon.__new__(CPolygon)
    temp_polygon.vertices = vertices
    return temp_polygon.is_convex()

def get_vertexes():
    str = input("Задайте вершины многоугольника в формате \"(1, 2), (3, 4), (5, 6)\"\n");
    vertexes = []
    x = 0
    y = 0
    partNum = 0 #0 - ждём '(', 1 - заполняем х, 2 - заполняем y.
    for c in str:
        if c == '(':
            x = 0
            y = 0
            partNum = 1
        elif c == ',' and partNum == 1:
            partNum = 2
        elif c == ')':
            vertexes.append((x, y))
            partNum = 0
        elif partNum == 1 and c != ' ':
            x *= 10
            x += int(c)
        elif partNum == 2 and c != ' ':
            y *= 10
            y += int(c)

    if len(vertexes) < 3:
        print("Ошибка: многоугольник должен иметь хотя бы 3 вершины")
        return None
    temp_polygon = CPolygon(vertexes)
    if temp_polygon.is_convex():
        return vertexes
    else:
        print("Ошибка: многоугольник не выпуклый! Пожалуйста, введите выпуклый многоугольник.")
        return None
    return vertexes



def line_intersection(startVert1, endVert1, startVert2, endVert2):
    x1, y1 = startVert1
    x2, y2 = endVert1
    x3, y3 = startVert2
    x4, y4 = endVert2

    determinant = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if abs(determinant) < 1e-10:
        return None

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / determinant
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / determinant

    if 0 <= t <= 1 and 0 <= u <= 1:
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        return (round(x, 10), round(y, 10))

    return None


def sort_points(points):
    if len(points) <= 2:
        return points

    center_x = sum(p[0] for p in points) / len(points)
    center_y = sum(p[1] for p in points) / len(points)

    def angle(point):
        return math.atan2(point[1] - center_y, point[0] - center_x)

    return sorted(points, key=angle)

def intersection(CPolygon1, CPolygon2):

    points_lying_inside = [] # Массив для точек внутри

    for i in range(0,len(CPolygon2.vertices)):
        if(CPolygon1.contain_point(CPolygon2.vertices[i])):
            points_lying_inside.append(CPolygon2.vertices[i])

    for j in range(0,len(CPolygon1.vertices)):
        if(CPolygon2.contain_point(CPolygon1.vertices[j])):
            points_lying_inside.append(CPolygon1.vertices[j])

    intersection_points = [] # Массив для точек пересечения

    for i in range(0,len(CPolygon1.vertices)):
        startVert1 = CPolygon1.vertices[i]
        endVert1 = CPolygon1.vertices[(i + 1) % len(CPolygon1.vertices)]

        for j in range(0,len(CPolygon2.vertices)):

            startVert2 = CPolygon2.vertices[j]
            endVert2 = CPolygon2.vertices[(j + 1) % len(CPolygon2.vertices)]
            # % len(CPolygon2.vertices) нужено чтобы последняя вершина корректно соединилась с первой
            point = line_intersection(startVert1, endVert1, startVert2, endVert2)
            if point is not None:
                intersection_points.append(point)


    all_points = points_lying_inside + intersection_points

    if not all_points:
        return []

    all_points = list(dict.fromkeys(all_points))
    all_points = sort_points(all_points)

    return all_points

def show_menu():
    print("\n" + "="*50)
    print("="*50)
    print("1. Ввести новые многоугольники")
    print("2. Показать информацию о многоугольниках")
    print("3. Проверить точку внутри многоугольника")
    print("4. Проверить многоугольник внутри многоугольника")
    print("5. Найти пересечение многоугольников")
    print("6. Триангуляция многоугольника")
    print("7. Выход")
    print("="*50)


def main():
    poly1 = None
    poly2 = None

    while True:
        show_menu()
        choice = input("Выберите действие (1-7): ").strip()

        if choice == '1':
            print("\n--- Ввод первого многоугольника ---")
            vertices1 = get_vertexes()
            if vertices1:
                poly1 = CPolygon(vertices1)
                print(f"Первый многоугольник: {poly1.vertices}")

            print("\n--- Ввод второго многоугольника ---")
            vertices2 = get_vertexes()
            if vertices2:
                poly2 = CPolygon(vertices2)
                print(f"Второй многоугольник: {poly2.vertices}")

        elif choice == '2':
            if not poly1 or not poly2:
                print("Сначала введите многоугольники! Или если ввели невыпуклый, то повторите ввод")
                continue

            print(f"\n=== ПЕРВЫЙ МНОГОУГОЛЬНИК ===")
            print(f"Вершины: {poly1.vertices}")
            print(f"Периметр: {poly1.perimeter():.2f}")
            print(f"Площадь: {poly1.area():.2f}")
            print(f"Выпуклый: {is_polygon_convex(poly1.vertices)}")

            print(f"\n=== ВТОРОЙ МНОГОУГОЛЬНИК ===")
            print(f"Вершины: {poly2.vertices}")
            print(f"Периметр: {poly2.perimeter():.2f}")
            print(f"Площадь: {poly2.area():.2f}")
            print(f"Выпуклый: {is_polygon_convex(poly2.vertices)}")

        elif choice == '3':
            if not poly1:
                print("Сначала введите многоугольники! Или если ввели невыпуклый, то повторите ввод")
                continue

            try:
                point_input = input("Введите координаты точки - 2 числа через пробел - пример: 1 4 x y: ").strip()
                x, y = map(float, point_input.split())
                test_point = (x, y)
                result = poly1.contain_point(test_point)
                print(f"Точка {test_point} внутри первого многоугольника: {result}")
            except ValueError:
                print("Ошибка ввода координат!")

        elif choice == '4':
            if not poly1 or not poly2:
                print("Сначала введите оба многоугольника!")
                continue

            result = poly1.contain_polygon(poly2)
            print(f"Второй многоугольник внутри первого: {result}")

        elif choice == '5':
            if not poly1 or not poly2:
                print("Сначала введите оба многоугольника!")
                continue

            intersection_result = intersection(poly1, poly2)
            print(f"Пересечение многоугольников: {intersection_result}")

        elif choice == '6':
            if not poly1:
                print("Сначала введите многоугольники! Или если ввели невыпуклый, то повторите ввод")
                continue

            triangles = poly1.triangulation()
            print(f"Триангуляция первого многоугольника:")
            print(f"Количество треугольников: {len(triangles)}")
            for i, triangle in enumerate(triangles, 1):
                print(f"  Треугольник {i}: {triangle}")

        elif choice == '7':
            print("Выход из программы...")
            break

        else:
            print("Неверный выбор! Попробуйте снова.")

if __name__ == "__main__":
    print("|| Лабораторная 3, работа с многоугольниками ||")
    main()


    #convex_vertices = [(0, 0), (4, 0), (4, 3), (0, 3)]
    # print("Первый многоугольник:")
    # poly1 = CPolygon(get_vertexes())
    # print("Второй многоугольник:")
    # poly2 = CPolygon(get_vertexes())
    # print(f"Многоугольник: {poly1.vertices}")
    # print(f"Периметр: {poly1.perimeter()}")
    # print(f"Площадь: {poly1.area()}")
    # print(f"Выпуклый: {is_polygon_convex(poly1.vertices)}")
    # test_point = (2, 3)
    # print(f"Точка {test_point} внутри: {poly1.contain_point(test_point)}")
    # triangles = poly1.triangulation()
    # print(f"Количество треугольников: {len(triangles)}")
    #
    # print(intersection(poly1, poly2))
    # poly2 = CPolygon([(1, 1), (2, 2), (3, 1)])
    # print(f"Многоугольник {poly2.vertices} внутри: {poly1.contain_polygon(poly2)}")


