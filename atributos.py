class Device:
    def __init__(self, ip,res, fecha, banner,dominio, whois, dns, puerto):
        self.ipv4 = ip
        self.res = res,
        self.date = fecha
        self.banner = banner
        self.dominio = dominio
        self.whois = whois
        self.dns = dns
        self.puerto = puerto

    def toCollection(self):
        return{
            "Direccion": self.ipv4,
            "Locatizacion":self.res,
            "Fecha": self.date,
            "Banner": self.banner,
            "Dominio": self.dominio,
            "Whois": self.whois,
            "Dns": self.dns,
            "puerto": self.puerto
        }