class Intersector(object):

    def __init__(self, relation):
        self.relation = relation

    def intersect(self, a, b):
        a_classes = self.get_equivalence_classes(a)
        b_classes = self.get_equivalence_classes(b)
        return self.intersect_classes(a_classes, b_classes)

    def get_equivalence_classes(self, elements):
        eq_classes = []
        for element in elements:
            match = False
            for eq_class in eq_classes:
                if self.relation(element, eq_class[0]):
                    eq_class.append(element)
                    match = True
                    break

            if not match:
                eq_classes.append([element])
        return eq_classes

    def intersect_classes(self, a, b):

        def search_in_B(g):
            for h in b:
                if self.relation(g[0], h[0]):
                    return h

        result = []
        for g in a:
            h = search_in_B(g)
            if h is not None:
                result.append(g + h)
        return result
