class Dataset(list):
    def reset(self, d):
        if isinstance(d,list):
            self.clear()
            self.extend(d)
        else:
            raise TypeError('Only list of dicts allowed.')

    def __getattribute__(self, item):
        if item == 'rows':
            return self
        elif item == 'cols':
            return {var:[row[var] for row in self] for var in self.vars}
        elif item == 'vars':
            if len(self):
                return list(self[0].keys())
            return []

        return super().__getattribute__(item)

    def __setattr__(self, name, value):
        raise NameError("name '" + name + "' is not defined")
        #super().__setattr__(name, value)     
