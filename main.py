import types


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


def flat_generator(list_of_lists):
    iterator = iter(list_of_lists)
    try:
        entity = next(iterator)
    except StopIteration:
        entity = None

    flag = bool(entity)
    last_flag = False
    iter_stack = [iterator]

    while flag:
        if isinstance(entity, list):
            if not entity:
                iterator = iter_stack[-1]
                try:
                    entity = next(iterator)
                except StopIteration:
                    iter_stack.pop()
                    if len(iter_stack) == 1:
                        if entity:
                            yield entity
                        else:
                            return
            else:
                iterator = iter(entity)
                entity = next(iterator)
                iter_stack.append(iterator)
        else:
            try:
                ret_val = entity
                entity = next(iterator)
                if last_flag:
                    last_flag = False

                yield ret_val
            except StopIteration:
                if not last_flag:
                    yield entity

                iter_stack.pop()
                iterator = iter_stack[-1]
                try:
                    entity = next(iterator)
                    last_flag = False
                except StopIteration:
                    last_flag = True

                    if len(iter_stack) == 1:
                        return
    else:
        return


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


def test_2():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


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


def test_4():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    assert isinstance(flat_generator(list_of_lists_2), types.GeneratorType)


if __name__ == '__main__':
    test_1()
    test_3()
    test_2()
    test_4()
