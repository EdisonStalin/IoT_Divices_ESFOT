class Device:
    def __init__(self, Nombre, Direccion, Puerto,status):
        self.Nombre = Nombre
        self.Direccion = Direccion
        self.Puerto = Puerto
        self.status = status

    def toCollection(self):
        return{
            "Nombre": self.Nombre,
            "Direccion": self.Direccion,
            "Puerto": self.Puerto,
            "Estado": self.status
        }