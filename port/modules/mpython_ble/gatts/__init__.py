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


class Profile(object):

    def __init__(self):
        self.services = []

    def __repr__(self):
        return "<{}{}>" .format(self.__class__.__name__, (': ' + str(self.services).strip('[').strip(']')) if self.services else '')

    def __add__(self, others):
        new_profile = Profile()
        for service in (self.services + others.services if others is not None else self.services):
            new_profile.add_services(service)
        return new_profile

    def __setitem__(self, index, val):
        self.services[index] = val

    def __getitem__(self, index):
        return self.services[index]

    def __len__(self):
        return len(self.services)

    def add_services(self, *services):
        for service in tuple(services):
            self.services.append(service)

    @property
    def definition(self):
        return tuple([service.definition for service in self.services])

    @property
    def services_uuid(self):
        return [service.uuid for service in self.services]

    @property
    def handles(self):
        return tuple([service.handles for service in self.services])

    @handles.setter
    def handles(self, value_handles):
        for n, server in enumerate(self.services):
            server.handles = value_handles[n]

    # def clear(self):
    #     self.services = []
