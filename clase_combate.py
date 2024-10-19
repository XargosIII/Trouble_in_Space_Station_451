import pyxel as px
import random
import clase_contenedor as ct
import clase_Superguerrero as ch

px.init(480, 320, display_scale=3)

px.load("assets\space_station.pyxres")


# Constantes para la pantalla y el tamaño de los sprites
ANCHO_PANTALLA = 480
ALTO_PANTALLA = 320
TAMANO_SPRITE = 16

class FaseCombate: 
    def __init__(self, aliados: list[ch.Superguerrero], enemigos: list[ch.Superguerrero]):
        # Inicializador de enemigos y aliados
        self.aliados = aliados
        self.enemigos = enemigos
        self.turno_actual = 0
        
        # Banderas (FLAGS FOR EVERYONE) para la selección de habilidades, objetivos y turno
        self.seleccionando_habilidad = False
        self.habilidad_seleccionada = None
        self.objetivo_seleccionado = None
        self.nuevo_turno = False
        self.opcion_seleccionada = 0  # Inicialización de la opción seleccionada para evitar el error
        self.enemigo_seleccionado = None
        self.aliado_seleccionado = None
        self.fase_incial = True
        self.fase_final = False
        

        # Se crean los contenedores importantes que se usaran para organizar visualmente el combate
        self.contenedor_inicio_batalla = ct.Contenedor(0, 0, 480, 320, "Inicio de la Batalla")
        self.contendor_fin_batalla = ct.Contenedor(0, 0, 480, 320, "Fin de la Batalla")
        self.contenedor_aliados = ct.Contenedor(180, 10, 136, 144, "Aliados")
        self.contenedor_enemigos = ct.Contenedor(10, 10, 136, 144, "Enemigos")
        self.contenedor_habilidades = ct.Contenedor(10, 163, 104, 72, "Habilidades")
        self.contenedor_habilidades_descripcion = ct.Contenedor(122, 163, 352, 72, "Descripcion")
        self.contenedor_chat = ct.Contenedor(10, 246, 464, 72, "Chat")
 
            
        # Agregamos los elementos de los contenedores iniciales y finales 
        self.contenedor_inicio_batalla.añadir_elemento("\n\n¡Prepárate para la batalla!")
        self.contenedor_inicio_batalla.añadir_elemento("\n\nPresiona ESPACIO para comenzar")

        self.contendor_fin_batalla.añadir_elemento("\n\n¡Fin del juego!")
        self.contendor_fin_batalla.añadir_elemento("\n\n¿Quieres jugar de nuevo? (S/N)")
            
        # Inicializar el diccionario de habilidades a mostrar mas adelante
        self.habilidades_dict = None
        
        # Establecemos el turno del primer personaje
        self.turnos = sorted(aliados + enemigos, key=lambda x: x.velocidad, reverse=True)
        self.establecer_personaje_y_turno_actual(self.turnos[self.turno_actual])
        
        
    def gestionar_turno(self):
        """ Metodo para que los enemigos actuen automaticamente y activemos el control por el jugador """
        if self.personaje_actual in self.enemigos:
            # En el turno del enemigo, seleccionamos aleatoriamente la habilidad y el objetivo
            habilidad = random.choice(self.personaje_actual.habilidades) # Para que el enemigo pueda elegirlas aleatoriamente, sacamos de la lista
            print(habilidad)
            objetivo = random.choice(self.aliados)
            mensaje = self.personaje_actual.usar_habilidad(dicc_habilidad = habilidad, enemigos= [objetivo])  # Metodo para saber a que objetivo debe afectar la habilidad
            print(mensaje)
            self.contenedor_chat.agregar_mensaje(mensaje)
            self.verificar_estado()
            # Añadimos mensaje para terminar turno
            self.contenedor_chat.agregar_mensaje("Pulsa la barra espaciadora para continuar.")
            # Flag para esperar en ejecuciones hasta que se cumpla el turno
            self.nuevo_turno = True
        else:
            # En el turno del guerrero mostramos habilidades para que seleccione el jugador
            self.mostrar_habilidades(self.personaje_actual)
            
        
    def siguiente_turno(self, personaje_extra_turno: ch.Superguerrero = None):
        """ Metodo para pasar al siguiente guerrero en el turno """
        # Establecemos el guerrero que tiene el turno actual
        self.establecer_personaje_y_turno_actual(personaje_extra_turno)
        # Damos paso a quien le toque el turno que haga sus cosas
        self.gestionar_turno()
    
    
    def establecer_personaje_y_turno_actual(self, personaje_extra_turno: ch.Superguerrero = None):
        """ Metodo para establecer quien tiene el turno """
        if not personaje_extra_turno:
            # Encontramos al proximo guerrero vivo en la lista de turnos
            num_personajes = len(self.turnos)
            for _ in range(num_personajes):
                # Vamos recorriendo la lista si hasta encontrarlo
                self.turno_actual = (self.turno_actual + 1) % num_personajes
                # Comprobamos si sigue vivo, y si es asi, le damos el turno
                if self.turnos[self.turno_actual].sigue_vivo():
                    self.personaje_actual = self.turnos[self.turno_actual]
                    break
        else:
            # El pasado como atributo se convierte en el personaje_actual(que tiene el turno)
            self.personaje_actual = personaje_extra_turno
        
        # Agregamos el mensaje de a quien le toca en el chat
        if self.personaje_actual in self.enemigos:
            print(f"Turno de enemigo: {self.personaje_actual.nombre}")
            mensaje = f"Turno de enemigo: {self.personaje_actual.nombre}"
        else:
            print(f"Turno de superviviente: {self.personaje_actual.nombre}")
            mensaje = f"Turno de superviviente: {self.personaje_actual.nombre}"
        self.contenedor_chat.agregar_mensaje(mensaje)
        
        
    def mostrar_habilidades(self, personaje: ch.Superguerrero):
        """ Metodo para mostrar todas las habilidades del personaje actual """
        # Indicamos que la opcion seleccionada es la primera habilidad
        self.opcion_seleccionada = 0
        self.habilidades_dict = personaje.mostrar_habilidades()  # Obtén el diccionario de habilidades
        print(f"Habilidades mostradas: {self.habilidades_dict}") 
        # Asi rellenamos el contenedor de hablidades con los nombres de las habilidades
        self.contenedor_habilidades.elementos = [descripcion.split(" - ")[0] for descripcion in list(self.habilidades_dict.keys()) ] # Muestra solo el nombre de las descripciones
        # Rellenamos el contenedor de descripcion de habilidades con la descripcion de la primera habilidad
        self.contenedor_habilidades_descripcion.elementos = [descripcion.split(" - ") for descripcion in list(self.habilidades_dict.keys())][self.opcion_seleccionada] # Muestra el resto
        
        # Esperamos la selección del usuario self.contenedor_habilidades_descripcion.elementos = [descripcion.split(" - ")[1:] for descripcion in list(self.habilidades_dict.keys())][0]
        self.seleccionando_habilidad = True
        print(f"Mostramos habilidades y seleccionando_habilidad: {self.seleccionando_habilidad}")
        

    def ejecutar_seleccion_habilidad(self, personaje: ch.Superguerrero):

        if self.seleccionando_habilidad:
            
            # Número total de habilidades
            num_habilidades = len(self.contenedor_habilidades.elementos)

            # Navegar por las habilidades con teclas de dirección
            if px.btnp(px.KEY_DOWN):
                print(f"Pulsamos abajo")
                self.opcion_seleccionada = (self.opcion_seleccionada + 1) % num_habilidades
            elif px.btnp(px.KEY_UP):
                print(f"Pulsamos arriba")
                self.opcion_seleccionada = (self.opcion_seleccionada - 1) % num_habilidades
                
            self.contenedor_habilidades_descripcion.eliminar_elementos()
            self.contenedor_habilidades_descripcion.elementos = [descripcion.split(" - ") for descripcion in list(self.habilidades_dict.keys())][self.opcion_seleccionada] # Cambiamos la descripcion
            
            # Seleccionar habilidad con Enter
            if px.btnp(px.KEY_RETURN):
                print(f"Pulsamos intro")
                # Adquirimos el diccionario entero para la habilidad seleccionada
                self.habilidad_seleccionada = list(personaje.habilidades)[self.opcion_seleccionada]
                print(self.habilidad_seleccionada)
                self.seleccionando_habilidad = False
                self.objetivo_seleccionado = None
                
                # Por si es un caso de habilidad a uno mismo o grupal
                if self.habilidad_seleccionada['tipo_objetivo'] in ["propio","todos_aliados","todos_enemigos"]:
                    if self.habilidad_seleccionada['tipo_objetivo'] in ["propio"]:
                        mensaje = personaje.usar_habilidad(self.habilidad_seleccionada)
                    else:
                        mensaje = personaje.usar_habilidad(self.habilidad_seleccionada,enemigos=self.enemigos, aliados=self.aliados)
                    if mensaje:
                        self.contenedor_chat.agregar_mensaje(mensaje)
                        self.verificar_estado()
                        self.habilidad_seleccionada = None
                        self.contenedor_chat.agregar_mensaje("Pulsa la barra espaciadora para continuar.")
                        self.nuevo_turno = True
                    else: 
                        mensaje = f"La habilidad {self.habilidad_seleccionada['nombre']} está en tiempo de espera."
                    # Empezamos la seleccion de objetivo para el resto de casos
                else:
                    if self.habilidad_seleccionada['tipo_objetivo'] == "aliado":
                        self.aliado_seleccionado = 0
                        print(f"Aliado seleccionado: {self.aliado_seleccionado}")
                    else:
                        self.enemigo_seleccionado = 0
                        print(f"Enemigo seleccionado: {self.enemigo_seleccionado}")
                    self.seleccionando_objetivo = True
    

    def seleccionar_objetivo(self, personaje):

        if self.habilidad_seleccionada:
            # Número de objetivos disponibles
            num_objetivos = len(self.aliados) if self.habilidad_seleccionada['tipo_objetivo'] == "aliado" else len(self.enemigos)
            
            # Navegar por los enemigos con teclas de dirección
            if px.btnp(px.KEY_DOWN):
                if self.habilidad_seleccionada['tipo_objetivo'] == "aliado":
                    self.aliado_seleccionado = (self.aliado_seleccionado + 1) % num_objetivos
                    print(f"Aliado seleccionado: {self.aliado_seleccionado}")
                else:
                    self.enemigo_seleccionado = (self.enemigo_seleccionado + 1) % num_objetivos
                    print(f"Enemigo seleccionado: {self.enemigo_seleccionado}")

            elif px.btnp(px.KEY_UP):
                if self.habilidad_seleccionada['tipo_objetivo'] == "aliado":
                    self.aliado_seleccionado = (self.aliado_seleccionado - 1) % num_objetivos
                    print(f"Aliado seleccionado: {self.aliado_seleccionado}")
                else:
                    self.enemigo_seleccionado = (self.enemigo_seleccionado - 1) % num_objetivos
                    print(f"Enemigo seleccionado: {self.enemigo_seleccionado}")
            
            # Confirmar selección del objetivo con Enter
            if px.btnp(px.KEY_RETURN):
                # Adquirimos el diccionario entero para la habilidad seleccionada
                habilidad = self.habilidad_seleccionada
                print(habilidad)
                # Ejecuta la habilidad seleccionada y guardamos el mensaje
                if self.habilidad_seleccionada['tipo_objetivo'] == "aliado":
                    self.objetivo_seleccionado = self.aliados[self.aliado_seleccionado]
                    mensaje = personaje.usar_habilidad(habilidad, enemigos = self.enemigos, aliados=[self.objetivo_seleccionado])
                else:
                    self.objetivo_seleccionado = self.enemigos[self.enemigo_seleccionado]
                    mensaje = personaje.usar_habilidad(habilidad, enemigos = [self.objetivo_seleccionado], aliados=self.aliados)
                self.contenedor_chat.agregar_mensaje(mensaje)
                self.verificar_estado()  # Comprobamos si esta habilidad nos ha llevado a la victoria
                # Deseleccionamos habilidad y enemigo
                self.habilidad_seleccionada, self.enemigo_seleccionado, self.aliado_seleccionado = None, None, None
                # Añadimos mensaje para terminar turno
                self.contenedor_chat.agregar_mensaje("Pulsa la barra espaciadora para continuar.")
                # Flag para esperar en ejecuciones hasta que se cumpla el turno
                self.nuevo_turno = True
                
                            


    def verificar_estado(self):
        """ 
        Metodo que comprueba si algun bando ha ganado y elimina los muertos
        la condicion es que todos los guerreros de un bando esten a 0 de salud 
        """
        if all(not enemigo.sigue_vivo() for enemigo in self.enemigos):
            print("¡Los supervivientes ganan!")
            mensaje = "¡Los supervivientes ganan!"
            self.contenedor_chat.agregar_mensaje(mensaje)
            self.fase_final = True
        elif all(not aliado.sigue_vivo() for aliado in self.aliados):
            print("¡Los enemigos ganan!")
            mensaje = "¡Los enemigos ganan!"
            self.contenedor_chat.agregar_mensaje(mensaje)
            self.fase_final = True

        
    def dibujar_escenario(self):
        """ Metodo para dibujar del motor pyxel """
        # Limpiamos la pantalla cada frame
        px.cls(0)
        
        # Si estamos en la pantalla de preparacion 
        if self.fase_incial:
            self.contenedor_inicio_batalla.mostrar()
        # Si estamos en la pantalla de derrota/victoria
        elif self.fase_final:
            self.contendor_fin_batalla.mostrar()
        else:
            # Pintamos un fondo interesante
            px.blt(0,0,1,0,0,256,256,scale=2)
            px.blt(256,0,1,0,0,-256,256,scale=2)
            
            # Deberia de pintar todos los guerreros con estos dos metodos...pero leches
            self.contenedor_aliados.mostrar()
            self.contenedor_enemigos.mostrar()
                        
            # Muestra las habilidades disponibles actuales y resalta la seleccionada
            # Actualiza la interfaz después de cambiar la selección o finalizar la misma
            self.contenedor_habilidades.mostrar(self.opcion_seleccionada)
            self.contenedor_habilidades_descripcion.mostrar()
            
            # Dibujar el Log de acciones y consecuencias
            self.contenedor_chat.mostrar()
            
            
            # Esto no es dibujar aliados en su contenedor, pero vale
            for i, aliado in enumerate(self.aliados):
                if i < 3:
                    x = self.contenedor_aliados.x + 31
                    y = self.contenedor_aliados.y + 18 + (i * 44)
                else:
                    x = self.contenedor_aliados.x + 85
                    y = self.contenedor_aliados.y + 30 + (i-3) * 50
                datos_blt = aliado.datos_blt_sprite()
                px.blt(x, y, datos_blt["img"], datos_blt["u"], datos_blt["v"], datos_blt["w"], datos_blt["h"], 0,scale=2)
                # Barra de vida bonita :3
                ancho_barra = 4  # Ajusta el ancho de la barra de vida
                alto_barra = int((aliado.salud / aliado.salud_max) * 32)  # Calcula la altura de la barra verde
                px.rect(x+20, y-8, ancho_barra, 32, px.COLOR_RED)  # Dibuja la barra roja de fondo
                px.rect(x+20, y-8 + (32 - alto_barra), ancho_barra, alto_barra, col=11)  # Dibuja la barra verde encima
                if i == self.aliado_seleccionado or (aliado == self.personaje_actual and self.habilidad_seleccionada == None):
                    px.blt(x - 10, y + 7, 0, 40, 24, 8, 8) # Flecha indicadora
                if len(aliado.condiciones)>0:
                    for i,k in enumerate(aliado.condiciones.keys()):
                        if k == "veneno":
                            px.blt(x+26,y-8+(i*9),0,32,16,8,8)
                        if k == "defensa":
                            px.blt(x+26,y-8+(i*9),0,40,16,8,8)
                        if k == "esquiva":
                            px.blt(x+26,y-8+(i*9),0,32,24,8,8)
            
            
            # Esto no es dibujar enemigos en su contenedor, pero vale
            for i, enemigo in enumerate(self.enemigos):
                x = self.contenedor_enemigos.x + 20
                y = self.contenedor_enemigos.y + 6 + i * 25
                datos_blt = enemigo.datos_blt_sprite()
                px.blt(x, y, datos_blt["img"], datos_blt["u"], datos_blt["v"], datos_blt["w"], datos_blt["h"], 0, rotate=datos_blt["rotate"])
                # px.text(x + 20, y + 4, f"{enemigo.nombre} HP: {enemigo.salud}", px.COLOR_WHITE)
                # Si sigue vivo le pintamos todo lo que haga falta
                if enemigo.sigue_vivo():
                    px.text(x, y+20, f"HP: {enemigo.salud}", px.COLOR_GREEN)
                    # Si es nuestro objetivo, lo marcamos con una flecha roja, si no, no hay flecha
                    if i == self.enemigo_seleccionado or enemigo == self.personaje_actual:
                        px.blt(x - 10, y + 9, 0, 40, 24, 8, 8)
                    # Si es nuestro objetivo, aparecera su nombre en azul, a la derecha de el
                    nombre_enemigo = f"{enemigo.nombre}" if i == self.enemigo_seleccionado else ""
                    px.text(x + 25, y+9, nombre_enemigo, px.COLOR_RED)  # Nombre del enemigo 
                    if len(enemigo.condiciones)>0:
                        for i,k in enumerate(enemigo.condiciones.keys()):
                            if k == "veneno":
                                px.blt(x+30+(i*9),y+18,0,32,16,8,8)
                            elif k == "defensa":
                                px.blt(x+30+(i*9),y+18,0,40,16,8,8)
                            elif k == "esquiva":
                                px.blt(x+30+(i*9),y+18,0,32,24,8,8)       
                # Si no calaverita
                else:
                    # Vida en rojo
                    px.text(x, y+20, f"HP: {enemigo.salud}", px.COLOR_RED)
                    # Icono de calavera
                    px.blt(x+30,y+10,0,0,32,8,8)
                

    def actualizar(self):
        """ Metodo que se llama constantemente en el motor pyxel """
        self.dibujar_escenario()
        if self.fase_incial:
            if px.btnp(px.KEY_SPACE):
                self.fase_incial = False
        elif self.fase_final:
            if px.btnp(px.KEY_S):
                self.fase_final = False
                self.aliados = lista_aliados
                self.enemigos = lista_enemigos
                self.turno_actual = 0
                self.turnos = sorted(self.aliados + self.enemigos, key=lambda x: x.velocidad, reverse=True)
                self.fase_incial = True
            if px.btnp(px.KEY_N):
                px.quit()    
        else:       
            # Boton para salir
            if px.btnp(px.KEY_Q) or px.btnp(px.KEY_ESCAPE):
                px.quit()
            
            if not self.nuevo_turno and self.turno_actual == 0:
                # Ponemos en marcha el primer turno
                self.gestionar_turno()
                self.nuevo_turno = True
                
            
            # Boton para confirmar pasar turno
            if self.nuevo_turno:
                if px.btnp(px.KEY_SPACE):
                    self.nuevo_turno = False
                    self.contenedor_chat.limpiar_mensajes()
                    self.siguiente_turno()
            else:
                # Si el personaje es un aliado y ha seleccionado habilidad o esta seleccionando objetivo 
                if self.personaje_actual in self.aliados:
                    if self.seleccionando_habilidad:
                        self.ejecutar_seleccion_habilidad(self.personaje_actual)
                    else:
                        self.seleccionar_objetivo(self.personaje_actual)
    
    def ejecutar_fase(self):
        """ Metodo para arrancar el motor Pyxel y empezar la fase Combate"""
        # Inicializa el bucle principal de px
        px.run(self.actualizar, self.dibujar_escenario)


############################# Pruebas ###################################

lista_aliados = []
for i in range(5):
    lista_aliados.append(ch.Conserje_espacial(f"Conserje_{i+1}"))
    
lista_enemigos = []
for i in range(5):
    lista_enemigos.append(ch.Larva_shekamorfa(nombre = f"Larva_{i+1}"))

combate = FaseCombate(lista_aliados,lista_enemigos) 
combate.ejecutar_fase()