from enum import Enum
import json
import numpy as _np


class Op(Enum):
    Add = 1
    Subtract = 2
    Multiply = 3
    Divide = 4
    Sine = 5
    Cosine = 6
    Tangent = 7
    Square_Root = 8
    Power = 9
    Exponent = 10
    Logarithm = 11
    Truncated_Modulo = 12
    Absolute = 13
    Sign = 14
    Minimum = 15
    Maximum = 16
    Ceil = 18
    Floor = 19
    Round = 20
    Less_Than = 21
    Greater_Than = 22


op = {
    Op.Add: lambda a, b: a + b,
    Op.Subtract: lambda a, b: a - b,
    Op.Multiply: lambda a, b: a * b,
    Op.Divide: lambda a, b: a / b,
    Op.Sine: lambda a, _: _np.sin(a),
    Op.Cosine: lambda a, _: _np.cos(a),
    Op.Tangent: lambda a, _: _np.tan(a),
    Op.Square_Root: lambda a, _: _np.sqrt(a),
    Op.Power: lambda a, b: a ** b,
    Op.Exponent: lambda a, _: _np.exp(a),
    Op.Logarithm: lambda a, b: _np.log(a) / _np.log(b),
    Op.Truncated_Modulo: lambda a, b: a % (_np.where(a < 0, -1, 1) * abs(b)),
    Op.Absolute: lambda a, _: _np.abs(a),
    Op.Sign: lambda a, _: _np.sign(a),
    Op.Minimum: lambda a, b: _np.minimum(a, b),
    Op.Maximum: lambda a, b: _np.maximum(a, b),
    Op.Ceil: lambda a, _: _np.ceil(a),
    Op.Floor: lambda a, _: _np.floor(a),
    Op.Round: lambda a, _: _np.round(a),
    Op.Less_Than: lambda a, b: (a < b).astype(_np.float32),
    Op.Greater_Than: lambda a, b: (a > b).astype(_np.float32),
}


class Node(object):
    __next_id = [1]

    def __init__(self, name=None):
        self.id = self.__next_id[0]
        self._name = name

        self.__next_id[0] += 1

    @property
    def name(self):
        if self._name is not None:
            return self._name
        else:
            return f'n{self.id:03}'

    def extension(self):
        return "node"

    def title(self):
        if self._name is not None:
            return self._name
        else:
            return f'{self.name}_{self.extension()}'.title()

    @name.setter
    def name(self, value):
        self._name = value

    def to_json(self):
        return None

    def __abs__(self):
        return MathFun(Op.Absolute, self, 0)

    def __neg__(self):
        return MathFun(Op.Multiply, self, -1)

    def __invert__(self):
        return 1 - self

    def __or__(self, other):
        return self.max(other)

    def __and__(self, other):
        return self.min(other)

    def __round__(self):
        return MathFun(Op.Round, self, 0)

    def __add__(self, other):
        return MathFun(Op.Add, self, other)

    def __radd__(self, other):
        return MathFun(Op.Add, other, self)

    def __sub__(self, other):
        return MathFun(Op.Subtract, self, other)

    def __rsub__(self, other):
        return MathFun(Op.Subtract, other, self)

    def __mul__(self, other):
        return MathFun(Op.Multiply, self, other)

    def __rmul__(self, other):
        return MathFun(Op.Multiply, other, self)

    def __truediv__(self, other):
        return MathFun(Op.Divide, self, other)

    def __rtruediv__(self, other):
        return MathFun(Op.Divide, other, self)

    def __pow__(self, other):
        return MathFun(Op.Power, self, other)

    def __rpow__(self, other):
        return MathFun(Op.Power, other, self)

    def __mod__(self, other):
        return MathFun(Op.Truncated_Modulo, self, other)

    def __rmod__(self, other):
        return MathFun(Op.Truncated_Modulo, other, self)

    def __lt__(self, other):
        return MathFun(Op.Less_Than, self, other)

    def __gt__(self, other):
        return MathFun(Op.Greater_Than, self, other)

    def __le__(self, other):
        return ~(self > other)

    def __ge__(self, other):
        return ~(self < other)

    def __eq__(self, other):
        return (self <= other) & (self >= other)

    def __ne__(self, other):
        return ~(self == other)

    def sin(self):
        return MathFun(Op.Sine, self, 0)

    def cos(self):
        return MathFun(Op.Cosine, self, 0)

    def tan(self):
        return MathFun(Op.Tangent, self, 0)

    def sqrt(self):
        return MathFun(Op.Square_Root, self, 0)

    def exp(self):
        return MathFun(Op.Exponent, self, 0)

    def log(self, other):
        return MathFun(Op.Logarithm, self, other)

    def abs(self):
        return MathFun(Op.Absolute, self, 0)

    def sign(self):
        return MathFun(Op.Sign, self, 0)

    def min(self, other):
        return MathFun(Op.Minimum, self, other)

    def max(self, other):
        return MathFun(Op.Maximum, self, other)

    def clamp(self):
        return self.max(0).min(1)

    def ceil(self):
        return MathFun(Op.Ceil, self, 0)

    def floor(self):
        return MathFun(Op.Floor, self, 0)

    def smoothstep(self):
        return (3 * self**2 - 2 * self**3).clamp()


class U(Node):
    def __init__(self, name=None, n=512):
        Node.__init__(self, name)

        self.data = _np.outer(
            _np.full(n, 1.0),
            _np.arange(0.5 / n, 1.0, 1.0 / n)
        )

    def extension(self):
        return "u"


class V(Node):
    def __init__(self, name=None, n=512):
        Node.__init__(self, name)

        self.data = _np.outer(
            _np.flip(_np.arange(0.5 / n, 1.0, 1.0 / n)),
            _np.full(n, 1.0)
        )

    def extension(self):
        return "v"


class Input(Node):
    def __init__(self, val, name=None):
        Node.__init__(self, name)

        self.input = val
        self.data = val.data if isinstance(val, Node) else val

    def extension(self):
        return "input"

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": "Input",
            "value": 1.0 if isinstance(self.input, Node) else self.input
        }


class MathFun(Node):
    def __init__(self, opcode, val1, val2, name=None):
        Node.__init__(self, name)

        v1 = val1.data if isinstance(val1, Node) else val1
        v2 = val2.data if isinstance(val2, Node) else val2

        self.opcode = opcode
        self.inputs = (val1, val2)
        self.data = op[opcode](v1, v2)

        if _np.isscalar(self.data):
            if not _np.isfinite(self.data):
                self.data = 0.0
        else:
            self.data[~_np.isfinite(self.data)] = 0.0

    def extension(self):
        return f'{self.opcode}'.replace('Op.', '')

    def to_json(self):
        inputs = [
            ["node", v.id] if isinstance(v, Node) else ["value", v]
            for v in self.inputs
        ]

        return {
            "id": self.id,
            "name": self.name,
            "type": "Math",
            "op": self.opcode.name,
            "inputs": inputs
        }


def trace_network(outputs):
    from collections import deque

    dq = deque(outputs)
    nodes = []
    seen = set()

    while len(dq):
        node = dq.popleft()
        if node.id in seen:
            continue

        nodes.append(node)
        seen.add(node.id)

        if hasattr(node, 'inputs'):
            for input in node.inputs:
                if isinstance(input, Node):
                    dq.append(input)

    return nodes


def network_as_json(outputs):
    nodes = [node.to_json() for node in trace_network(outputs)]
    outputs = [node.id for node in outputs]

    return json.dumps({"nodes": nodes, "outputs": outputs}, indent=2)


if __name__ == "__main__":
    from PIL import Image

    u = Input(U(), "u")
    v = Input(V(), "v")
    a = ((u - 0.5)**2 + (v - 0.5)**2).sqrt() < 0.5

    out = a
    out.name = "mask"

    print(network_as_json([out]))

    Image.fromarray(out.data * 256).show()
