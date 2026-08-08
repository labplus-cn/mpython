# The MIT License (MIT)

# Copyright (c) 2020, Tangliufeng for labplus Industries

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


class Service(object):
    """ 服务 """

    def __init__(self, uuid):
        self.uuid = uuid
        self.characteristics = []
        self.value_handle = None

    def __repr__(self):
        return "<{} {}{}>" .format(self.__class__.__name__, self.uuid, (': ' + str(self.characteristics).strip('[').strip(']')) if self.characteristics else '')

    def __setitem__(self, index, val):
        self.characteristics[index] = val

    def __getitem__(self, index):
        return self.characteristics[index]

    def __len__(self):
        return len(self.characteristics)

    def add_characteristics(self, *characteristics):
        """ 添加特征 """
        for characteristic in tuple(characteristics):
            self.characteristics.append(characteristic)
        return self

    @property
    def definition(self):
        if self.characteristics:
            return (self.uuid, tuple([char.definition for char in self.characteristics]))
        else:
            raise ValueError("A service must contain at least one characteristics")

    @property
    def handles(self):
        service_handles = ()
        for char in self.characteristics:
            service_handles += char.handles
        return service_handles

    @handles.setter
    def handles(self, value_handles):
        slice_start, slice_end = 0, 0
        for n, char in enumerate(self.characteristics):
            slice_end += len(char.handles)
            char.handles = value_handles[slice_start:slice_end]
            slice_start = slice_end

    # def clear(self):
    # 	self.characteristics = []
