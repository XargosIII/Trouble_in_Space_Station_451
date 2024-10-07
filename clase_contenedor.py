import pyxel as px

class Contenedor:
    """ Clase para pintar un marco donde queramos y algunos metodos para añadir elementos o texto """
    def __init__(self, x, y, ancho, alto, titulo=""):
        # "Coordenadas" donde empezamos a pintar el marco
        self.x = x
        self.y = y
        # Dimensiones del marco que queramos pintar
        self.ancho = ancho
        self.alto = alto
        # por si queremos ponerle titulo al marco, es opcional
        self.titulo = titulo
        # Lista de elementos para mostrar dentro del contenedor
        self.elementos = []
        # Una lista exclusiva para texto
        self.mensajes = []

    def añadir_elemento(self, elemento):
        """ Metodo que agrega elementos a la lista de elementos del objeto """
        # Añadir elementos como texto, imágenes, etc.
        self.elementos.append(elemento)
        
    def eliminar_elementos(self):
        """ Metodo para limpiar la lista de elementos """
        self.elementos = []
        
    def agregar_mensaje(self, mensaje):
        """ Metodo que agrega mensajes a la lista de mensajes del objeto """
        if mensaje != "" and type(mensaje) == str:
            for mensajito in mensaje.split("\n"):
                if mensajito == "":
                    continue
                self.mensajes.append(mensajito)
                # Mensajito de prueba
                # print(f"Mensaje agregado: {mensajito}")
    
    def limpiar_mensajes(self):
        """ otoxplicativo """
        self.mensajes = []

    def pintar_marco(self):
        """ Metodo para hacer lentejas """
        # Dibujamos el marco al estilo del final fantasy añejo
        
                # Pintamos las esquinas del recuadro usando las piezas del blt que representan las "esquinas"
        px.blt(u=0, v=16, img=0, w=8, h=8, x=self.x, y=self.y)
        px.blt(u=8, v=16, img=0, w=8, h=8, x=self.x + self.ancho - 8, y=self.y)
        px.blt(u=0, v=24, img=0, w=8, h=8, x=self.x, y=self.y + self.alto - 8)
        px.blt(u=8, v=24, img=0, w=8, h=8, x=self.x + self.ancho - 8, y=self.y + self.alto - 8)

        # Esto pinta las paredes del recuadro por toda la pantalla usando las piezas guardadas en el blt
        # Cada cuadrito de w=8 y h=8 en imagenes de pyxel son 8 pixeles en pantalla, asi que calculamos
        for x in range(int(self.ancho / 8)):
            for y in range(int(self.alto / 8)):
                # Pintamos el borde superior
                if y == 0 and not x == 0 and not x == int(self.ancho / 8) - 1:
                    px.blt(u=16, v=16, img=0, w=8, h=8, x=self.x + (x * 8), y=self.y + (y * 8))
                # Pintamos el borde inferior
                if y == int(self.alto / 8) - 1 and not x == 0 and not x == int(self.ancho / 8) - 1:
                    px.blt(u=16, v=24, img=0, w=8, h=8, x=self.x + (x * 8), y=self.y + (y * 8))
                # Pintamos el lateral izquierdo
                if x == 0 and not y == 0 and not y == int(self.alto / 8) - 1:
                    px.blt(u=24, v=16, img=0, w=8, h=8, x=self.x + (x * 8), y=self.y + (y * 8))
                # Pintamos el lateral derecho
                if x == int(self.ancho / 8) - 1 and not y == 0 and not y == int(self.alto / 8) - 1:
                    px.blt(u=24, v=24, img=0, w=8, h=8, x=self.x + (x * 8), y=self.y + (y * 8))
        
        px.rect(self.x+8, self.y+8, self.ancho-16, self.alto-16, col=0)
        
        """ Old version
        px.rectb(self.x, self.y, self.ancho, self.alto, 7)  # Rectángulo exterior
        px.rectb(self.x + 1, self.y + 1, self.ancho - 2, self.alto - 2, 0)  # Borde interior
        """
        # Si hay un título, mostrarlo en el marco superior
        if self.titulo:
            px.text(self.x + 4, self.y - 6, self.titulo, 7)

    def mostrar(self, seleccionado: int = -1):
        """ Metodo principal, pinta el marco y luego le añade los elementos y mensajes que tengamos guardados en el objeto """
        # Pintar el marco y todos los elementos contenidos
        self.pintar_marco()
        
        for i, elemento in enumerate(self.elementos):
            color = px.COLOR_LIGHT_BLUE if i == seleccionado else px.COLOR_WHITE
            if i == seleccionado:
                px.blt(self.x + 4, (self.y + 10) + (i * 10), 0, 40, 24, 8, 8) # Flecha indicadora
            # flecha = "-> " if i == seleccionado else ""
            # px.text(self.x + 4, (self.y + 10) + (i * 10), flecha, color)  # Flecha wapa indicadora
            px.text(self.x + 14, (self.y + 10) + (i * 10), str(elemento), color)
        
        if self.mensajes:
            for i, mensaje in enumerate(self.mensajes):
                px.text(self.x + 14, (self.y+10) + (i * 10), mensaje, px.COLOR_WHITE) # Mostramos mensajes de guerreros

    def actualizar(self):
        """ Ni recuerdo para que narices lo iba a usar..."""
        # Actualizar elementos del contenedor, si es necesario
        for elemento in self.elementos:
            elemento.actualizar()
