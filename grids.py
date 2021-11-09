import numpy as np


class Grid2D(object):
    """"""
    '''
    
             x
       |-----------> X axis
       |
     y |
       |
       |
       ˅ Y axis

    '''

    # noinspection PyMethodParameters
    @classmethod
    def _dims(_, x, y):
        return (
            (y + 1, x),
            (y, x + 1)
        )

    @classmethod
    def new(cls, *dimensions):
        d = cls._dims(*dimensions)

        return cls(dimensions, map(np.zeros, d))

    def __init__(self, dimensions, data):
        self._dimensions = dimensions
        self.pX, self.pY = data

        # pX : Horizontal lines, parallel to X axis
        # pY : Vertical lines, parallel to Y axis

    @property
    def x(self):
        x, *_ = self._dimensions
        return x

    @property
    def y(self):
        _, y, *_ = self._dimensions
        return y

    def is_set(self, x, y):
        return self.pX[y, x] \
           and self.pY[y, x] \
           and self.pX[y + 1, x] \
           and self.pY[y, x + 1]

    @staticmethod
    def _set(array, dims, value):
        array[(*reversed(dims),)] = value

    # noinspection PyPep8Naming
    def set_pX(self, *dims):
        self._set(self.pX, dims, 1)

    # noinspection PyPep8Naming
    def unset_pX(self, *dims):
        self._set(self.pX, dims, 0)

    # noinspection PyPep8Naming
    def set_pY(self, *dims):
        self._set(self.pY, dims, 1)

    # noinspection PyPep8Naming
    def unset_pY(self, *dims):
        self._set(self.pY, dims, 0)

    def __repr__(self):
        return "Grid2D(\npX = \\\n" + repr(self.pX) + ",\npY = \\\n" + repr(self.pY) + "\n)"


class Grid3D(Grid2D):
    """"""
    '''

             |-----------> X axis
            /|     x
         y / | z
          /  |
    Y axis   |
             ˅ Z axis

    '''

    # noinspection PyMethodOverriding
    @classmethod
    def _dims(cls, x, y, z):
        # noinspection PyPep8Naming
        pX, pY = super()._dims(x, y)

        return (
            (z + 1, *pX),
            (z + 1, *pY),
            (z, y + 1, x + 1)
        )

    def __init__(self, dimensions, data):
        *data, self.pZ = data

        # pZ : Lines parallel to the Z axis

        super().__init__(dimensions, data)

    @property
    def z(self):
        _, _, z, *_ = self._dimensions
        return z

    # noinspection PyMethodOverriding
    def is_set(self, x, y, z):
        return self.XY_slice(z).is_set(x, y) \
           and self.XY_slice(z + 1).is_set(x, y) \
           and self.pZ[z, y, x] \
           and self.pZ[z, y, x] \
           and self.pZ[z, y, x] \
           and self.pZ[z, y, x]

    # noinspection PyPep8Naming
    def set_pZ(self, *dims):
        self._set(self.pZ, dims, 1)

    # noinspection PyPep8Naming
    def unset_pZ(self, *dims):
        self._set(self.pZ, dims, 0)

    # noinspection PyPep8Naming
    def XY_slice(self, n):
        return Grid2D(
            (self.x, self.y),
            (
                self.pX[n, :, :],
                self.pY[n, :, :]
            )
        )

    # noinspection PyPep8Naming
    def XZ_slice(self, n):
        return Grid2D(
            (self.x, self.z),
            (
                self.pX[:, n, :],
                self.pZ[:, n, :]
            )
        )

    # noinspection PyPep8Naming
    def YZ_slice(self, n):
        return Grid2D(
            (self.y, self.z),
            (
                self.pY[:, :, n],
                self.pZ[:, :, n]
            )
        )

    def __repr__(self):
        return "Grid3D(\npX = \\\n" + repr(self.pX) + ",\npY = \\\n" + repr(self.pY) + ",\npZ = \\\n" + repr(
            self.pZ) + "\n)"

    # noinspection PyPep8Naming
    @staticmethod
    def related_from_3D(x, y, z):
        # (n, (x, y)), (n, (x, y))
        return (z, (x, y)), (x, (y, z))  # indices in XY(n), YZ(n)

    # noinspection PyPep8Naming
    @staticmethod
    def related_from_2D_XY(n, x, y):
        # (x, y, z), (n, (x, y))
        return (x, y, n), (x, (y, n))  # indices in 3D, YZ(n)

    # noinspection PyPep8Naming
    @staticmethod
    def related_from_2D_YZ(n, y, z):
        # (x, y, z), (n, (x, y))
        return (n, y, z), (z, (n, y))  # indices in 3D, XY(n)


class Grid4D(Grid3D):
    """"""
    '''

    (4th dimension)
    W axis <~~~~~~~~|-----------> X axis
               w   /|     x
                y / | z
                 /  |
           Y axis   |
                    ˅ Z axis

    '''

    # noinspection PyMethodOverriding,PyMethodParameters
    @classmethod
    def _dims(_, x, y, z, w):
        # noinspection PyPep8Naming
        pX, pY, pZ = super()._dims(x, y, z)

        return (
            (w + 1, *pX),
            (w + 1, *pY),
            (w + 1, *pZ),
            (w, z + 1, y + 1, x + 1)
        )

    def __init__(self, dimensions, data):
        *data, self.pW = data

        # pW : Lines parallel to the W axis

        super().__init__(dimensions, data)

    @property
    def w(self):
        _, _, _, w, *_ = self._dimensions
        return w

    # noinspection PyMethodOverriding
    def is_set(self, x, y, z, w):
        pass  # TODO

    # noinspection PyPep8Naming
    def set_pW(self, *dims):
        self._set(self.pW, dims, 1)

    # noinspection PyPep8Naming
    def unset_pW(self, *dims):
        self._set(self.pW, dims, 0)

    def XY_slice(self, n):
        raise NotImplementedError

    def YZ_slice(self, n):
        raise NotImplementedError

    # noinspection PyPep8Naming
    def XYZ_slice(self, n):
        return Grid3D(
            (self.x, self.y, self.z),
            (
                self.pX[n, :, :, :],
                self.pY[n, :, :, :],
                self.pZ[n, :, :, :]
            )
        )

    # noinspection PyPep8Naming
    def YZW_slice(self, n):
        return Grid3D(
            (self.y, self.z, self.w),
            (
                self.pY[:, :, :, n],
                self.pZ[:, :, :, n],
                self.pW[:, :, :, n]
            )
        )

    def __repr__(self):
        return object.__repr__(self)

    # noinspection PyPep8Naming
    @staticmethod
    def related_from_4D(x, y, z, w):
        # (n, (x, y, z)), (n, (x, y, z))
        return (w, (x, y, z)), (x, (y, z, w))  # indices in XYZ(n), YZW(n)

    # noinspection PyPep8Naming
    @staticmethod
    def related_from_3D_XYZ(n, x, y, z):
        # (x, y, z, w), (n, (x, y, z))
        return (x, y, z, n), (x, (y, z, n))  # indices in 4D, YZW(n)

    # noinspection PyPep8Naming
    @staticmethod
    def related_from_3D_YZW(n, y, z, w):
        # (x, y, z, w), (n, (x, y, z))
        return (n, y, z, w), (w, (n, y, z))  # indices in 4D, XYZ(n)


def main():
    g = Grid4D.new(1, 1, 1, 1)

    print(g.XYZ_slice(0).XY_slice(0))


if __name__ == "__main__":
    main()
