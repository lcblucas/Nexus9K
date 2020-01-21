import classes_nexus9k

usuario = "admin"
senha = "Admin_1234!"
ip = "sbx-nxos-mgmt.cisco.com"
url_equipamento = 'https://' + ip + '/ins/'
vrf = "management"
comando = "show ip arp vrf " + vrf + ""

u = classes_nexus9k.Usuario(usuario, senha)
f = classes_nexus9k.Equipamento(comando, url_equipamento, u)
f.pegar_hostname()
f.aplicar_comando()
f.sh_ip_arp_vrf()

