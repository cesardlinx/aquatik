Aquatik
=======

Aplicación para medición de parámetros del agua y control de dron aquático mediante
Raspberry Pi.

Mediciones:
-----------

Para la obtención de las mediciones la Raspberry Pi debe estar conectada serialmente
a un Arduino, el mismo que se encarga de la tansmisión de los valores via serial hacia la
Raspberry Pi.

Los parámetros que se miden son:

- Temperatura
- pH
- Conductividad Eléctrica
- Oxígeno Disuelto

El formato de string de como los valores son transmitidos hacia la Raspberry es el siguiente

`:<temperatura>:<ph>:<conductividad eléctrica>:<oxígeno disuelto>:`

Hardware:
---------

La Raspberry Pi se encuentra a cargo de los servomotores que mueven al dron por el agua,
y una pequeña bomba encargada de succionar el agua para tomar la muestra. Los motores
y la bomba se encuentran conectados a la Raspberry Pi en los siguientes pines del GPIO:

| Elemento   | Pines   |
| ---------- | :-----: |
| Bomba      | 21, 23  |
| Motor Izq  | 29, 31  |
| Motor Der  | 33, 35  |

Configuración de GPS
--------------------

La aplicación obtiene las lecturas de GPS del sensor mediante el daemon GPSD, por
lo que la configuración e instalación del mismo es la siguiente:

``` {.sourceCode .bash}
# apt-get install gpsd-clients gpsd -y
# systemctl stop gpsd.socket
# systemctl disable gpsd.socket
```
Posteriormente es necesario además hacer los siguientes cambios:

1. Modificar en el archivo /lib/systemd/system/gpsd.socket la línea que
dice `ListenStream=127.0.0.1:2947` por `ListenStream=0.0.0.0:2947`

2. Añadir en el archivo /etc/default/gpsd el valor en DEVICES del puerto serial
`DEVICES="/dev/ttyAMA0"`

3. Si hay problemas con los permisos del puerto, es necesario enmascarar el
servicio con el siguiente comando:

``` {.sourceCode .bash}
# systemctl mask serial-getty@ttyAMA0.service
```



