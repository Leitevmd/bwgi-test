import unittest
from bwgi_test import computed_property


class Vector:
    def __init__(self, x, y, z, color=None):
        self.x, self.y, self.z = x, y, z
        self.color = color
        self.calls = 0

    @computed_property('x', 'y', 'z')
    def magnitude(self):
        self.calls += 1
        from math import sqrt
        return round(sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2), 2)


class Circle:
    def __init__(self, radius=1):
        self.radius = radius
        self.calls = 0

    @computed_property('radius', 'area')
    def diameter(self):
        """Circle diameter from radius"""
        self.calls += 1
        return self.radius * 2

    @diameter.setter
    def diameter(self, value):
        self.radius = value / 2

    @diameter.deleter
    def diameter(self):
        self.radius = 0


class TestComputedProperty(unittest.TestCase):
    def test_vector_magnitude_cache(self):
        v = Vector(3, 4, 0)
        self.assertEqual(v.magnitude, 5.0)
        self.assertEqual(v.calls, 1)
        v.color = 'red'
        self.assertEqual(v.magnitude, 5.0)
        self.assertEqual(v.calls, 1)  # Still cached
        v.y = 0
        self.assertEqual(v.magnitude, 3.0)
        self.assertEqual(v.calls, 2)  # Recomputed

    def test_missing_attribute(self):
        c = Circle()
        self.assertEqual(c.diameter, 2)
        self.assertEqual(c.calls, 1)

    def test_setter_and_deleter(self):
        c = Circle()
        c.diameter = 10
        self.assertEqual(c.radius, 5)
        del c.diameter
        self.assertEqual(c.radius, 0)

    def test_docstring_preservation(self):
        doc = Circle.diameter.__doc__
        self.assertTrue("Circle diameter from radius" in (doc or ""))

    def test_unrelated_attribute_change_does_not_invalidate(self):
        v = Vector(1, 2, 2)
        self.assertEqual(v.magnitude, 3.0)
        v.color = 'blue'
        self.assertEqual(v.magnitude, 3.0)
        self.assertEqual(v.calls, 1)  # Still cached

    def test_missing_dependency_appears_later(self):
        class Dynamic:
            def __init__(self):
                self.calls = 0

            @computed_property('x', 'y')
            def total(self):
                self.calls += 1
                return getattr(self, 'x', 0) + getattr(self, 'y', 0)

        d = Dynamic()
        self.assertEqual(d.total, 0)
        d.x = 3
        d.y = 7
        self.assertEqual(d.total, 10)

    def test_mutable_dependency_change_does_not_invalidate(self):
        class Holder:
            def __init__(self):
                self.data = [1, 2, 3]
                self.calls = 0

            @computed_property('data')
            def total(self):
                self.calls += 1
                return sum(self.data)

        h = Holder()
        self.assertEqual(h.total, 6)
        h.data.append(4)
        self.assertEqual(h.total, 6)  # Still cached
        self.assertEqual(h.calls, 1)  # Confirms it was not recomputed

    def test_computed_property_is_cached_per_instance(self):
        v1 = Vector(1, 0, 0)
        v2 = Vector(0, 3, 4)
        self.assertEqual(v1.magnitude, 1.0)
        self.assertEqual(v2.magnitude, 5.0)
        self.assertEqual(v1.calls, 1)
        self.assertEqual(v2.calls, 1)
        v1.x = 0
        self.assertEqual(v1.magnitude, 0.0)
        self.assertEqual(v1.calls, 2)
        self.assertEqual(v2.magnitude, 5.0)
        self.assertEqual(v2.calls, 1)

    def test_mutable_object_mutation_not_tracked(self):
        """
        WARNING: This test demonstrates a known limitation.

        It uses a side effect (`calls` counter) to detect whether the cached
        function is re-executed after in-place mutation of a dependency.

        EXPECTED BEHAVIOR:
        - Cached result remains after mutation (should not re-execute).
        - This confirms that in-place changes to mutable objects do not invalidate cache.
        """
        class Box:
            def __init__(self):
                self.items = [1, 2]
                self.calls = 0

            @computed_property('items')
            def count(self):
                self.calls += 1
                return len(self.items)

        b = Box()
        result1 = b.count
        self.assertEqual(result1, 2)
        self.assertEqual(b.calls, 1)  # Computed once

        b.items.append(3)  # In-place mutation
        result2 = b.count
        self.assertEqual(result2, 2)  # Cached result
        self.assertEqual(b.calls, 1)  # ✅ Not recomputed — confirms limitation


if __name__ == "__main__":
    unittest.main()
