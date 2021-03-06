"""
# Board
G: grass
L: Land
"""
BOARD = """\
GLGGG
GLLLG
GGGLG
GGLLG
GGLGG
"""

VERTICES = [
    (0, 30),
    (30, 30),
    (30, 70),
    (70, 70),
    (70, 50),
    (100, 50)]

TOWERS = [
    (10, 10),           (10, 50), (10, 70), (10, 90),
    (30, 10),                               (30, 90),
    (50, 10), (50, 30), (50, 50),           (50, 90),
    (70, 10), (70, 30),                     (70, 90),
    (90, 10), (90, 30),           (90, 70), (90, 90)]


class Field:

    WIDHT = 100
    HEIGHT = 100
    SECTION  = 20

    def __init__(self):
        self.board = self._load_map(BOARD)
        self.path = self._generate_path_list(VERTICES)
        self.towers = TOWERS

    def _load_map(self, map_string):
        matrix = []
        list_of_lines = map_string.split("\n")
        for line in list_of_lines:
            matrix.append(list(line))
        return matrix

    def _generate_path_list(self, vertices):
        path = []
        for start, stop in zip(vertices, vertices[1:]):
            path.extend(self._generate_segment_list(start, stop))
        path.append(vertices[-1])
        return path

    def _generate_segment_list(self, start, stop):
        result = []
        if start[0] == stop[0]:
            for i in range(start[1], stop[1]):
                result.append((start[0], i))
        else:
            for i in range(start[0], stop[0]):
                result.append((i, start[1]))
        return result

    def move(self, monsters):
        """
        params: monsters must be an iterable
        return: an iterable of monster outside of map
        """
        monsters_outside = []
        for monster in monsters:
            current_position = monster.position
            current_index = self.path.index(current_position)
            next_index = current_index + monster.step_length
            try:
                next_position = self.path[next_index]
                monster.position = next_position
            except IndexError:
                monster.position = (101, 51)  # go outside
                monsters_outside.append(monster)
        return monsters_outside

    def get_tower_locations(self):
        """
        returns an iterable of tower locations as tuble (x, y)
        """
        return self.towers

    def get_monster_entrance(self):
        """
        returns a monster entrance as a tuble (x, y)
        """
        return self.path[0]

    def get_board(self):
        """
        returns a matrix:
            - G means grass
            - L means land
        """
        return self.board
