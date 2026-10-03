def bubble_sort(array: list[int]) -> None:
    n = len(array)

    for i in range(n - 1, -1, -1):
        sorted_flag = True

        for j in range(0, n - 1):

            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                sorted_flag = False

        if sorted_flag:
            break

