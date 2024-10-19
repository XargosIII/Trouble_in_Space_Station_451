import pyxel as px
import random

########################### Superclase Superguerrero ###########################

class Superguerrero: 
    def __init__(self, nombre, salud, salud_max, velocidad, ataque, defensa, resistencia, voluntad, descriptores, frases=None):
        self.nombre = nombre
        self.salud = salud
        self.salud_max = salud_max
        self.velocidad = velocidad
        self.ataque = ataque
        self.defensa = defensa
        self.resistencia = resistencia
        self.voluntad = voluntad
        self.esquiva = 0
        self.descriptores = descriptores
        self.defendiendose = False
        self.habilidades = [
            {"id":"atacar","nombre":"Atacar","tiempo_espera":0, "cooldown":0, "descripcion":f"{self.nombre} ataca."},
        ]
        # self.turnos_en_defensa = 0 # contador de los turnos que esta activa la defensa DEPRECATED
        self.condiciones=dict() # Diccionario para los bonos y efectos de las habilidades
                           # Lo siguiente es un ejemplo por defecto de todos las condiciones existentes
        """"veneno":{"turnos":0,"danyo":0}, 
        "velocidad":{"turnos":0,"bono":0},
        "ataque":{"turnos":0,"bono":0},
        "defensa":{"turnos":0,"bono":0},
        "resistencia":{"turnos":0,"bono":0},
        "voluntad":{"turnos":0,"bono":0},
        "esquiva":{"turnos":0,"bono":0}"""
    
        self.frases = frases or { # frases por defecto...por si se me olvida
            "inicio_combate": ["¡A la batalla!"],
            "recibir_danyo": ["¡Me estan machacando!"],
            "morir": ["¡Han aparecido por...la retaguardia..aghh!"],
            "ganar_pelea": ["¡Chupado!"],
            "evento_satisfactorio": ["¡Mision cumplida!"],
            "evento_fallido": ["¡Mision fallida, me retiro!"]
        }

    ########################### Metodos de informacion ###########################

    def sigue_vivo(self):
        """ Metodo que devuelve True si la salud del guerrero es mayor que 0, False si no """
        return self.salud > 0

    def mostrar_estadisticas(self):
        """ Metodo que imprime los atributos actuales del guerrero (¡ahora con __dict__ activo!)"""
        estadisticas = {k: v for k, v in self.__dict__.items() if not callable(v) and not k.startswith("__")} # Version 2.0 adaptada de un friki de internet. Asi hay que escribir menos
        print(estadisticas)
    
    def mostrar_descripcion(self):
        """ Metodo que devuelve la descripcion del guerrero, si es que tiene alguna """
        return f"{self.nombre} es un superviviente del tipo: {', '.join(self.descriptores)}."
    
    def mostrar_habilidades(self):
        """ Metodo que devuelve todas las habilidades de nuestro guerrero en un diccionario. Con el nombre de su metodo como key, 
        y un diccionario con el conteniendo del nombre de la habilidad, tiempo de espera y su descripcion, como claves y valor"""
        habilidades_a_mostrar = {}
        for habilidad in self.habilidades:
            descripcion = f"{habilidad['nombre']} - Cooldown: {habilidad['tiempo_espera']} - Descripción: {habilidad['descripcion']}"
            habilidades_a_mostrar[descripcion] = getattr(self, habilidad["id"])  # Asocia la descripción al método de esta clase
        return habilidades_a_mostrar
    
    def datos_blt_sprite(self):
        """ 
        Metodo que devuelve dicionario con los datos de la libreria pixel 
        para localizar el sprite del guerrero y pintarlo usando el metodo blt 
        """
    ########################### Metodos de Mecanicas ###########################
    
    def usar_habilidad(self, dicc_habilidad: dict, enemigos=None, aliados=None)->str:
        # print(dicc_habilidad)
        if dicc_habilidad and dicc_habilidad['cooldown'] == 0:
            # Bajamos el cooldown del resto de las habilidades
            for habilidad in self.habilidades:
                # Aplicamos la habilidad y actualizamos el cooldown
                if dicc_habilidad["nombre"] == habilidad["nombre"]:
                    mensaje = habilidad['accion'](self, enemigos, aliados) if enemigos or aliados else habilidad['accion'](self)
                    habilidad['cooldown'] = habilidad['tiempo_espera']
                habilidad['cooldown'] = max(0, habilidad['cooldown'] - 1)
              # Establecemos el cooldown
            return mensaje
        else:
            return False

    
    def defender(self, danyo)->str:
        """ Reduce el danyo recibido en función del atributo defensa """
        esquiva = random.randint(1,100) # Tirada de esquiva
        if self.esquiva > esquiva:
            print(f"{self.nombre} esquiva completamente el danyo.")
            mensaje = f"{self.nombre} esquiva completamente el danyo."
        else:
            danyo_recibido = max(0, danyo - self.defensa) # Forma super chula de quitarme un if else comprimido. Devuelve 0 si el otro parametro es menor que 0, con lo cual me quito los negativos
            self.salud -= danyo_recibido
            if danyo_recibido:
                if not self.sigue_vivo():
                        mensaje = f"{self.nombre} ha caido en batalla"
                        mensaje += "  " + random.choice(self.frases["morir"])
                        print(mensaje)
                else:
                    mensaje = f"{self.nombre} recibe {danyo_recibido} de danyo. Salud restante: {self.salud}."
                    print(mensaje)
            else:
                mensaje = f"La defensa de {self.nombre} niega todo el danyo recibido."
                print(mensaje)
        return mensaje
    
    # Esto habria que crearlo como una clase a parte, que se instancia en cada guerrero...
    # pero estoy cansado para pensarlo ahora
    def actualizar_condiciones(self, dicc_condicion: dict = None):
        """ Metodo que actualiza todas las condiciones existentes o añade una nueva, 
        dependiendo de si se le pasa un diccionario o no."""
        mensaje = ""
        if dicc_condicion: # Refactorizamos chorizo largo, ahora 2x bonico
            print(dicc_condicion)
            print(type(dicc_condicion))
            for k, v in dicc_condicion.items():
                print(k, v)
                if k != "veneno":
                    setattr(self, k, getattr(self, k) + v["bono"])  # Asi actualizamos solo la estadística relevante, fuera elifs
                self.condiciones[k] = v
                print(f"Soy {self.nombre} y mis condiciones son: {self.condiciones}")
                mensaje = ""
        else:
            dicc_temporal = self.condiciones.copy()
            for k, v in dicc_temporal.items():
                if v["turnos"] > 0:
                    v["turnos"] -= 1
                    if k == "veneno":
                        danyo_veneno = max(0, v["danyo"] - (self.resistencia / 2))
                        if danyo_veneno > 0:
                            self.salud -= danyo_veneno
                            if not self.sigue_vivo():
                                mensaje = f"{self.nombre} ha caido en batalla"
                                mensaje += "  " + random.choice(self.frases["morir"])
                                print(mensaje)
                            else:
                                mensaje = f"{self.nombre} recibe {danyo_veneno} de danyo por veneno."
                                print(mensaje)
                        else:
                            mensaje = f"{self.nombre} ha resistido el danyo del veneno"
                            print(mensaje)
                    if v["turnos"] == 0:
                        mensaje = f"{self.nombre} pierde {k}."
                        print(mensaje)
                        if k != "veneno":
                            setattr(self, k, getattr(self, k) - v["bono"])  # Igual que arriba, reseteamos solo la estadística relevante, fuera elifs
                        del self.condiciones[k]
                else:
                    mensaje = ""
        return mensaje
    
    def consultar_condiciones(self):
        """ Metodo que devuelve un diccionario con las condiciones que padece el guerrero """
        return self.condiciones
    
    def comentar(self, evento):
        """ Metodo que imprime una frase adecuada a la situación actual """
        if evento in self.frases and self.frases[evento]:
            frase = self.frases[evento][random.randint(0, len(self.frases[evento])-1)]
            print(f"{self.nombre}: {frase}")


    ########################### Metodos de Habilidades ###########################

    
    def atacar(self, objetivo, mensaje: str)->str:
        """ Metodo para realizar un ataque basico al objetivo """
        danyo = self.ataque
        print(f"\n{self.nombre} causa {danyo} de danyo.")
        mensaje += (f"\n{self.nombre} causa {danyo} de danyo.")
        mensaje += " " + objetivo.defender(danyo)
        return mensaje


########################### Subclases de Superguerrero supervivientes ###########################


class Conserje_espacial(Superguerrero):
    """ 
    Clase que crea un Conserje espacial del tipo Superguerrero
    Atributos:
    nombre = str
    """
    def __init__(self, nombre: str = "Conserje Espacial"):
        super().__init__(
            nombre = nombre,
            salud=70,
            salud_max=70,
            velocidad=8,
            ataque=5,
            defensa=3,
            resistencia=4,
            voluntad=6,
            descriptores=["ingeniero", "aliado", "curandero", "mago"]
        )
        self.habilidades = [
            {"id":"atacar","nombre": "Atacar", "tiempo_espera": 0,"cooldown":0, "descripcion": f"{self.nombre} atacara con su fregona.","tipo_objetivo": "enemigo","accion": lambda self, enemigos=None, aliados=None: self.atacar(enemigos, aliados)},
            {"id":"defenderse","nombre": "Defender", "tiempo_espera": 0,"cooldown":0, "descripcion": f"{self.nombre} doblara su defensa a {self.defensa*2} y aumentará su esquiva a {self.esquiva+30}.","tipo_objetivo": "propio","accion": lambda self: self.defenderse()},
            {"id":"saquear_maquina_expendedora","nombre": "Maquina expendedora", "tiempo_espera": 3,"cooldown":0, "descripcion": f"Restaura {self.ataque * 2} de salud a todos los aliados.","tipo_objetivo": "todos_aliados","accion": lambda self, enemigos=None, aliados=None: self.saquear_maquina_expendedora(enemigos, aliados)},
            {"id":"limpieza_a_fondo","nombre": "Limpieza a fondo", "tiempo_espera": 5,"cooldown":0, "descripcion": f"Limpia todos los efectos del aliado objetivo, eliminándolos completamente.","tipo_objetivo": "aliado","accion": lambda self, enemigos=None, aliados=None: self.limpieza_a_fondo(enemigos, aliados)},
            {"id":"explosion_quimica","nombre": "Explosion quimica", "tiempo_espera": 4,"cooldown":0, "descripcion": f"Lanza una mezcla de productos químicos a un enemigo, \ncausando ({self.ataque * 3}) de danyo y {self.ataque * 2} de danyo extra por veneno durante 2 turnos.","tipo_objetivo": "enemigo","accion": lambda self, enemigos=None, aliados=None: self.explosion_quimica(enemigos, aliados)}
        ]
        self.frases={
            "inicio_combate": ["¡Esto no estaba en mi contrato!", "¡Vamos a sacar la basura!","¿Quien necesita una limpieza?", "¡Pagareis por mi abrillantadora nuevecita!"],
            "recibir_danyo": ["¡Ay, eso no estaba en la lista de tareas!", "¡No me manches el uniforme!"],
            "morir": ["La suciedad...viene a por mi...", "Don limpio...te he fallado..."],
            "ganar_pelea": ["Una pelea limpia, como siempre.", "¡Yo no pienso limpiar este desastre!"],
            "evento_satisfactorio": ["¡Vaya, un 2x1 inesperado!", "Un buen dia para ser un conserje"],
            "evento_fallido": ["La hemos liado pero bien...", "No me enrole para esto."]
        }


    ########################### Metodos comunes ###########################

    
    def mostrar_descripcion(self):
        """ Metodo que devuelve la descripcion de nuestro guerrero """
        base_description = super().mostrar_descripcion()
        return base_description + "\n Un experto en mantener todo limpio y ordenado, pero también tiene conocimientos en la manipulación de sustancias químicas y el uso de objetos improvisados para curar a sus compañeros. Aunque su fuerza física es limitada, su positividad es contagiosa. ¿Donde he dejado mi mopa dorada?"
    
    
    def datos_blt_sprite(self):
        """ 
        Metodo que devuelve dicionario con los datos de la libreria pixel 
        para localizar el sprite del conserje y pintarlo usando el metodo blt 
        """
        datos_blt = {"u":32,"v":0,"img":0,"w":16,"h":16}
        return datos_blt

    
    ########################### Habilidades ###########################
    
    
    def atacar(self, enemigos: Superguerrero = [], aliados: Superguerrero = []):
        if enemigos:
            enemigo = enemigos[0]
        """ Ataque basico del friegasuelos """
        print(f"{self.nombre} ataca con una fregona a {enemigo.nombre}.")
        mensaje = f"{self.nombre} ataca con una fregona a {enemigo.nombre}."
        mensaje = super().atacar(enemigo, mensaje)
        return mensaje

    def defenderse(self) -> str:
        """ Defensa basica activa del limpiaventanas """
        self.defendiendose = True
        condiciones={ 
            "defensa":{"turnos":2,"bono":self.defensa}, # Duplica su defensa
            "esquiva":{"turnos":2,"bono":30} # 30% de probabilidad de esquivar ataque
        }
        print(f"{self.nombre} se defiende, aumentando la defensa y posibilidad de esquivar.")
        mensaje = f"{self.nombre} se defiende, aumentando la defensa y posibilidad de esquivar."
        self.actualizar_condiciones(condiciones)
        mensaje += "\n" + self.actualizar_condiciones()
        return mensaje 
    
    def saquear_maquina_expendedora(self, enemigos: Superguerrero = [], aliados: Superguerrero = []):
        """ Restaura una pequeña cantidad de salud a todos los aliados """
        mensaje = ""
        if aliados:
            for aliado in aliados:
                aliado.salud += self.ataque * 2
                print(f"{self.nombre} restaura 10 de salud a {aliado.nombre}. Salud actual de {aliado.nombre}: {aliado.salud}.")
                mensaje = f"{self.nombre} restaura 10 de salud a {aliado.nombre}. Salud actual de {aliado.nombre}: {aliado.salud}.\n"
            mensaje += self.actualizar_condiciones()
        return mensaje 
            

    def limpieza_a_fondo(self, enemigos: Superguerrero = [], aliados: Superguerrero = []):
        """ Elimina todos los efectos negativos de un aliado """
        mensaje = ""
        if aliados:
            aliado = aliados[0]        
            print(f"{self.nombre} limpia todos los efectos de {aliado.nombre}.")
            mensaje = f"{self.nombre} limpia todos los efectos de {aliado.nombre}."
            aliado.condiciones = dict()
            print(aliado.consultar_condiciones())
            mensaje += "\n" + self.actualizar_condiciones()
        return mensaje

    def explosion_quimica(self, enemigos: Superguerrero = [], aliados: list[Superguerrero] = []):
        """ Lanza una mezcla de productos químicos a un enemigo, causando (ataque * 3) de danyo y efectos secundarios """
        if enemigos:
            enemigo = enemigos[0]
        danyo = self.ataque * 3
        veneno = {"veneno":{"turnos":2,"danyo":self.ataque * 2}}
        print(f"{self.nombre} lanza una mezcla química a {enemigo.nombre}, causando {danyo} de danyo y envenenandolo")
        mensaje = f"{self.nombre} lanza una mezcla química a {enemigo.nombre}, causando {danyo} de danyo y envenenandolo"
        mensaje += "\n" + enemigo.defender(danyo)
        mensaje += "\n" + enemigo.actualizar_condiciones(veneno) # Le metemos la condicion de veneno por dos turnos con el danyo establecido, jeje
        mensaje += self.actualizar_condiciones()
        return mensaje     


########################### Subclases de Superguerrero enemigos ###########################


class Larva_shekamorfa(Superguerrero):
    def __init__(self, nombre: str = "Larva Shekamorfa"):
        salud = px.rndi(20, 35)
        super().__init__(
            nombre=nombre,
            salud=salud,
            salud_max=salud,
            velocidad=px.rndi(5, 15),
            ataque=10,
            defensa=px.rndi(0, 2),
            resistencia=5,
            voluntad=3,
            descriptores=["enemigo", "infectador"],
            frases={
                "inicio_combate": ["¡Kriii!"],
                "morir": ["¡Grugrugru!"],
                "eliminar_superviviente": ["¡Krinfectado!"]
            }
        )
        self.habilidades = [
            {"id": "atacar","nombre": "Atacar", "tiempo_espera":0, "cooldown":0, "descripcion": f"{self.nombre} salta hacia un enemigo y le golpea con sus garras.","tipo_objetivo": "enemigo","accion": lambda self, enemigos=None, aliados=None: self.atacar(enemigos)},
            {"id": "salto_infectante","nombre": "Salto Infectante", "tiempo_espera":0, "cooldown":0, "descripcion": f"{self.nombre} salta hacia un enemigo y lo infecta, causando danyo a lo largo del tiempo.","tipo_objetivo": "enemigo","accion": lambda self, enemigos=None, aliados=None: self.salto_infectante(enemigos)}
        ]

    ########################### Metodos de información ###########################

    def mostrar_descripcion(self):
        """ Método que devuelve la descripción de la Larva Shekamorfa """
        return f"{self.nombre} es una larva infectadora que busca dañar y debilitar a los supervivientes."
    
    def datos_blt_sprite(self):
        """                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
        Metodo que devuelve dicionario con los datos de la libreria pixel 
        para localizar el sprite de la larva y pintarlo usando el metodo blt 
        """
        if self.sigue_vivo():
            datos_blt = {"u":0,"v":0,"img":0,"w":16,"h":16,"rotate":0}
        else:
            datos_blt = {"u":16,"v":0,"img":0,"w":16,"h":16,"rotate":180}
        return datos_blt

    ########################### Métodos de habilidades ###########################

    def atacar(self, enemigos: list[Superguerrero] = [], aliados: list[Superguerrero] = [])->str:
        """ Método para realizar un ataque básico a un objetivo """
        px.play(1,1) # Reproducimos el sonido de los ataques de las garritas
        enemigo = enemigos[0] # Seleccionamos siempre el enemigo 0 ya que es de un solo objetivo
        
        print(f"{self.nombre} ataca con sus pequeñas garras.")
        mensaje = f"{self.nombre} ataca con sus pequeñas garras."
        mensaje = super().atacar(enemigo, mensaje)
        return mensaje

    def salto_infectante(self, enemigos: list[Superguerrero] = [], aliados: list[Superguerrero] = []):
        """ Salta hacia un enemigo y lo infecta, causando danyo a lo largo del tiempo. """
        px.play(1,0) # Reproducimos el sonido del saltito
        enemigo = enemigos[0] # Seleccionamos siempre el enemigo 0 ya que es de un solo objetivo        
        veneno = {"veneno":{"turnos":3,"danyo":self.ataque}}
        print(f"{self.nombre} salta hacia {enemigo.nombre} y lo infecta durante {veneno["veneno"]["turnos"]} turnos.")
        mensaje = f"{self.nombre} salta hacia {enemigo.nombre} y lo infecta durante {veneno["veneno"]["turnos"]} turnos."
        enemigo.actualizar_condiciones(veneno)
        mensaje += "\n" + self.actualizar_condiciones()
        return mensaje 