class Device:
    def __init__(self, ip, fecha, hora, banner,dominio, whois, dns):
        self.ipv4 = ip
        self.date = fecha
        self.hour = hora
        self.banner = banner
        self.dominio = dominio
        self.whois = whois
        self.dns = dns

    def toCollection(self):
        return{
            "ipv4": self.ipv4,
            "Fecha": self.date,
            "Hora": self.hour,
            "Banner": self.banner,
            "Dominio": self.dominio,
            "Whois": self.whois,
            "Dns": self.dns
        }