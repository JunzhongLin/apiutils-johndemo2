class Calculator:
    """simple calculator class as a template.

    Args:
        a (int): a magic number.
        b (int): a magic number.

    """

    @staticmethod
    def add(a: int, b: int) -> int:
        """Add two magic numbers together.

        Example:
            >>> res = Calculator(1, 2).add()
            1 + 2 = 3

        Returns:
            int: sum of two magic numbers.
        """
        return a + b
