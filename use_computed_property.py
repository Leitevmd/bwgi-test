from bwgi_test import computed_property

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


def main():
    c = Circle()
    print(f"Initial diameter: {c.diameter}, calls = {c.calls}")
    print(f"Second access (cached): {c.diameter}, calls = {c.calls}")

    c.radius = 10  # Invalidate cache
    print(f"After radius change: {c.diameter}, calls = {c.calls}")

    c.diameter = 20  # Use setter
    print(f"After setting diameter to 20: radius = {c.radius}, diameter = {c.diameter}")

    del c.diameter  # Use deleter
    print(f"After deleting diameter: radius = {c.radius}, diameter = {c.diameter}")

if __name__ == "__main__":
    main()
