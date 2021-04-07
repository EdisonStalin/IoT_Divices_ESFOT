class divice:
    def __init__(self, Nombre, Direccion, Puerto):
        self.Nombre = Nombre
        self.Direccion = Direccion
        self.Puerto = Puerto

    def toCollection(self):
        return{
            "Nombre": self.Nombre,
            "Direccion": self.Direccion,
            "Puerto": self.Puerto
        }