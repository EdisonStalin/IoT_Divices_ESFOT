class Device:
    def __init__(self, ip, fecha, banner,dominio, whois, dns, puerto):
        self.ipv4 = ip
        self.date = fecha
        self.banner = banner
        self.dominio = dominio
        self.whois = whois
        self.dns = dns
        self.puerto = puerto

    def toCollection(self):
        return{
            "Direccion": self.ipv4,
            "Fecha": self.date,
            "Banner": self.banner,
            "Dominio": self.dominio,
            "Whois": self.whois,
            "Dns": self.dns,
            "puerto": self.puerto
        }