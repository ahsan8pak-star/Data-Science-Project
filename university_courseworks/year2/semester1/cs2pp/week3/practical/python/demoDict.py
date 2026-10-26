# Need to import random within this space to use it here.
import random

# ** packs any keyword arguments (supplied on execution) into a dictionary.
def dictConvert(**kwargs):
    """
    Process keyword arguments by applying key-specific transformations.

    This function iterates over the provided keyword arguments and performs
    transformations based on the key:

    - If the key is 'Ages', each numerical value in the corresponding list is
      incremented by a random float in the range [0, 1) and then rounded to three
      decimal places.
    - If the key is 'Grades', each string in the corresponding list is converted
      to uppercase.
    - For any other keys, the values are left unchanged.

    During processing, the function prints each key along with its transformed
    value. Finally, the modified dictionary is returned.

    Parameters
    ----------
    **kwargs : dict
        Arbitrary keyword arguments. Expected keys include:

        - 'Ages' : list of numbers
            A list where each number represents an age that will be adjusted with a
            random offset.
        - 'Grades' : list of str
            A list of grade strings that will be converted to uppercase.
        - Other keys with associated values are accepted but remain unmodified.

    Returns
    -------
    dict
        A dictionary containing the processed keyword arguments. The values for
        'Ages' and 'Grades' are transformed as described above, while other keys
        retain their original values.

    Examples
    --------
    >>> result = dictConvert(Ages=[20, 30], Grades=['a', 'b'], Name='Alice')
    key='Ages', val=[20.123, 30.456]   # Output will vary due to randomness.
    key='Grades', val=['A', 'B']
    key='Name', val='Alice'
    >>> print(result)
    {'Ages': [20.123, 30.456], 'Grades': ['A', 'B'], 'Name': 'Alice'}
    """

    for key, val in kwargs.items():
        match key:
            case 'Ages':
                val = [round(x + random.random(), 3) for x in val]
                kwargs['Ages'] = val
            case 'Grades':
                val = [x.upper() for x in val]
                kwargs['Grades'] = val
            case _:
                pass

        print(f'{key=}, {val=}')
    # Return the dictionary
    return kwargs

