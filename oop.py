class Animal:

    def __init__(self, name, action):
        self.name = name
        self.action = action

    def cat(self, arr):
        for a in arr:
            print(a)

    def cow(self):
        print(self.name)


kitchn = Animal("cat", "cow")
kitchn.cow()
