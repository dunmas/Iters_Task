class FlatIterator:

    def __init__(self, list_of_list):
        self.raw_list = list_of_list

    def __iter__(self):
        self.iterator = iter(self.raw_list)
        try:
            self.entity = next(self.iterator)
        except StopIteration:
            self.entity = None

        self.flag = bool(self.entity)
        self.last_flag = False
        self.iter_stack = [self.iterator]
        return self

    def __next__(self):
        while self.flag:
            if isinstance(self.entity, list):
                if not self.entity:
                    self.iterator = self.iter_stack[-1]
                    try:
                        self.entity = next(self.iterator)
                    except StopIteration:
                        self.iter_stack.pop()
                        if len(self.iter_stack) == 1:
                            if self.entity:
                                return self.entity
                            else:
                                raise StopIteration
                else:
                    self.iterator = iter(self.entity)
                    self.entity = next(self.iterator)
                    self.iter_stack.append(self.iterator)
            else:
                try:
                    ret_val = self.entity
                    self.entity = next(self.iterator)
                    if self.last_flag:
                        self.last_flag = False

                    return ret_val
                except StopIteration:
                    if not self.last_flag:
                        self.last_flag = True
                        return self.entity

                    self.iter_stack.pop()
                    self.iterator = self.iter_stack[-1]
                    try:
                        self.entity = next(self.iterator)
                        self.last_flag = False
                    except StopIteration:
                        self.last_flag = True

                        if len(self.iter_stack) == 1:
                            raise StopIteration
        else:
            raise StopIteration


def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


def test_3():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


if __name__ == '__main__':
    test_1()
    test_3()
