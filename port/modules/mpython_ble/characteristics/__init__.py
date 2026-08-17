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

from bluetooth import FLAG_NOTIFY, FLAG_READ, FLAG_WRITE


class Characteristic(object):

    def __init__(self, uuid, properties='-r'):
        self.uuid = uuid
        # properties(read,write,notify)
        self.properties = (True if 'r' in properties else False,
                           True if 'w' in properties else False, True if 'n' in properties else False)
        self.flags = (FLAG_READ if self.properties[0] else 0x00) | (
            FLAG_WRITE if self.properties[1] else 0x00) | (FLAG_NOTIFY if self.properties[2] else 0x00)
        self.descriptors = []
        self.value_handle = None

    def _properties(self, flags):
        self.flags = flags
        self.properties = (True if FLAG_READ & self.flags else False, True if FLAG_WRITE &
                           self.flags else False, True if FLAG_NOTIFY & self.flags else False)
        return self.properties

    def __repr__(self):
        properties_ = '-'
        if self.properties[0]:
            properties_ += 'r'
        if self.properties[1]:
            properties_ += 'w'
        if self.properties[2]:
            properties_ += 'n'
        return "<{} {}, '{}'{}>" .format(self.__class__.__name__, self.uuid, properties_, (': ' + str(self.descriptors).strip('[').strip(']')) if self.descriptors else '')

    def __setitem__(self, index, obj):
        self.descriptors[index] = obj

    def __getitem__(self, index):
        return self.descriptors[index]

    def __len__(self):
        return len(self.descriptors)

    def add_descriptors(self, *descriptors):
        for descriptor in tuple(descriptors):
            self.descriptors.append(descriptor)
        return self

    @property
    def definition(self):
        if self.descriptors:
            return (self.uuid, self.flags) + ([descriptor.definition for descriptor in self.descriptors],)
        else:
            return (self.uuid, self.flags)

    # def clear(self):
    # 	self.descriptors = []

    @property
    def handles(self):
        return tuple([self.value_handle] + [descr.value_handle for descr in self.descriptors])

    @handles.setter
    def handles(self, value_handles):
        self.value_handle = value_handles[0]
        for n, desc in enumerate(self.descriptors):
            desc.value_handle = value_handles[n + 1]
