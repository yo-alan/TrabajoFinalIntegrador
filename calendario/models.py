from random import random, randrange
from django.db import models


class Especialidad(models.Model):
	
	nombre = models.CharField(max_length=100, null=False)
	carga_horaria_semanal = models.IntegerField(default=0, null=False)
	max_horas_diaria = models.IntegerField(default=0, null=False)
	
	def __str__(self, ):
		return self.nombre.encode('utf-8')
	
	def __eq__(self, o):
		return self.nombre == o.nombre
	

class Espacio(models.Model):
	
	nombre = models.CharField(max_length=100, null=False, blank=False)
	#HARDCODED
	_dias_habiles = [1, 2, 3, 4, 5]
	_horas = []
	#~ _horas = [["18:15", "18:55"],
				#~ ["18:55", "19:35"],
				#~ ["19:45", "20:25"],
				#~ ["20:25", "21:05"],
				#~ ["21:05", "21:45"],
				#~ ["21:45", "22:25"],
				#~ ["22:25", "23:05"]]
	
	def __str__(self, ):
		return self.nombre.encode('utf-8')
	
	@property
	def horas(self, ):
		
		if not self._horas:
			self._horas = Hora.objects.filter(espacio=self).order_by('hora_desde')
		
		return self._horas

class Hora(models.Model):
	
	hora_desde = models.TimeField('desde', null=False)
	hora_hasta = models.TimeField('hasta', null=False)
	espacio = models.ForeignKey(Espacio)
	

class Persona(models.Model):
	
	nombre = models.CharField(max_length=100, null=False, blank=False)
	apellido = models.CharField(max_length=100, null=False, blank=False)
	cuil = models.CharField(max_length=11, unique=True, null=False, blank=False)

class Profesional(Persona):
	
	restricciones = []
	especialidad = models.ForeignKey(Especialidad)
	
	def __str__(self, ):
		return self.apellido.encode('utf-8') + ", " + self.nombre.encode('utf-8')
	
	def __eq__(self, o):
		return self.cuil == o.cuil

class Calendario(models.Model):
	
	espacio = models.ForeignKey(Espacio)
	horarios = []
	puntaje = models.IntegerField(default=0)
	
	def __str__(self, ):
		return str(self.espacio) + "(" + str(self.id) + ")"
	
	#Por cada franja horaria de uso se inserta una nueva lista de horarios vacia
	######################################################
	#~ for dia in dias:
		#~ horarios.append([])
	######################################################
	
	def agregar_horario(self, horario):
		"""
		Agrega un Horario a la lista de horarios del Calendario.
		"""
		
		for franja_horaria in self.horarios: #Por cada dia.
			#Si contiene un Horario con mismo dia_desde lo agrega a la lista
			if franja_horaria[0].hora_desde == horario.hora_desde:
				franja_horaria.append(horario)
				print franja_horaria
				raw_input()
				return
		
		#Sino crea una nueva lista con el Horario
		self.horarios.append([horario])
		#~ print self.horarios
	
	def cruce(self, madre, prob_mutacion=0.01):
		"""
		Cruza el individuo con otro madre.
		
		@Parametros:
		madre - individuo con quien realizar la cruza.
		prob_mutacion - probabilidad de mutacion para los hijos resultantes. Valor: 0.01.
		
		@Return:
		
		"""
		if not isinstance(madre, Calendario):
			raise Exception("El objeto no es de tipo Calendario.")
		
		if self == madre:
			raise Exception("Un Calendario no puede cruzarse consigo mismo.")
		
		
		
	
	def mutar(self, ):
		pass
	

class Horario(models.Model):
	
	hora_desde = models.TimeField('desde', null=False)
	hora_hasta = models.TimeField('hasta', null=False)
	dia_semana = models.IntegerField(default=0, null=False)
	calendario = models.ForeignKey(Calendario)
	profesional = models.ForeignKey(Profesional)
	
	def __str__(self, ):
		return str(self.profesional.especialidad)
	
	def __eq__(self, o):
		return self.hora_desde == o.hora_desde and\
				self.hora_hasta == o.hora_hasta and\
				self.dia_semana == o.dia_semana and\
				self.calendario == o.calendario
	
	def __ne__(self, o):
		return self.dia_semana != o.dia_semana and self.hora_desde != o.hora_desde
	
	def __lt__(self, o):
		if self.dia_semana == o.dia_semana:
			return self.hora_desde < o.hora_desde
		
		return self.dia_semana < o.dia_semana
	
	def __le__(self, o):
		if self.dia_semana == o.dia_semana:
			return self.hora_desde <= o.hora_desde
		
		return self.dia_semana <= o.dia_semana
	
	def __gt__(self, o):
		if self.dia_semana == o.dia_semana:
			return self.hora_desde > o.hora_desde
		
		return self.dia_semana > o.dia_semana
	
	def __ge__(self, o):
		if self.dia_semana == o.dia_semana:
			return self.hora_desde >= o.hora_desde
		
		return self.dia_semana >= o.dia_semana

class Restriccion(models.Model):
	
	hora_desde = models.TimeField('desde', null=False, blank=False)
	hora_hasta = models.TimeField('hasta', null=False, blank=False)
	dia_semana = models.IntegerField(default=0, null=False, blank=False)
	
	def __eq__(self, o):
		pass
		#return self.hora_desde == o.hora_desde and self.hora_hasta == o.hora_hasta and self.

class Espacio_restriccion(Restriccion):
	
	espacio = models.ForeignKey(Espacio)

class Profesional_restriccion(Restriccion):
	
	profesional = models.ForeignKey(Profesional)

class Entorno(object):
	"""
	Clase que abarca el medio ambiente en el cual se desarrolla el algoritmo.
	
	@Atributos:
	.DIAS - constante con los dias de la semana. Valor: {0 : 'Domingo', 1 : 'Lunes', 2 : 'Martes', 3 : 'Miercoles', 4 : 'Jueves', 5 : 'Viernes', 6 : 'Sabado'}.
	.dias_habiles - lista con los dias a cubrir. Valor: {}.
	.horarios - diccionario con los horarios a cubrir. Valor: {}.
	.poblacion - lista de individuos. Valor: [].
	.profesionales - lista de profesionales a utilizar. Valor: [].
	.restricciones - lista de restricciones a utilizar. Valor: [].
	.generaciones - cantidad de generacion a generar. Valor: 0.
	.espacio - espacio para el cual se generan los individuos. Valor: None.
	"""
	
	DIAS = {0 : 'Domingo', 1 : 'Lunes', 2 : 'Martes', 3 : 'Miercoles', 4 : 'Jueves', 5 : 'Viernes', 6 : 'Sabado'}
	
	_poblacion = []
	_restricciones = []
	_profesionales = []
	_especialidades = []
	_generaciones = 0
	_espacio = None
	
	def __init__(self, generaciones=50, espacio=None):
		"""
		Inicializa los atributos del objeto.
		
		@Parametros:
		generaciones - cantidad de generaciones a generar. Valor: 50.
		espacio - El espacio para el cual se generaran los calendarios. Valor: None.
		
		@Return:
		None
		"""
		
		self.profesionales = Profesional.objects.all()[:6] #Asignamos todas las especialidades de la BBDD.
		
		for p in self.profesionales:
			
			self.restricciones += Profesional_restriccion.objects.filter(profesional=p)
			
			self.especialidades.append(p.especialidad)
		
		self.generaciones = generaciones
		self.espacio = espacio
		
		self.generar_poblacion_inicial()
	
	def generar_poblacion_inicial(self, ):
		"""
		Crea la poblacion inicial de individuos y los guarda en el atributo 'poblacion'.
		
		@Parametros:
		None
		
		@Return:
		None
		"""
		
		#Iteramos generando todas las combinaciones posibles de horarios.
		#Y los agregamos a un calendario.
		for dia in range(0, 7): #Cantidad de iteraciones por los dias.
			
			if dia not in self.espacio._dias_habiles:
				continue
			
			for hora in self.espacio.horas: #Cantidad de iteraciones por los horarios.
				
				for profesional in self.profesionales: #Iteracion por cada profesional(p).
					
					c = Calendario() #Se crea un Calendario.
					c.espacio = self.espacio #Se le asigna el espacio.
					c.save() #Y se guarda.
					
					self.poblacion.append(c) #A su vez el Calendario es agregado a la poblacion del Entorno.
					
					h = Horario() #Se crea un Horario.
					h.profesional = profesional #Se le asigna un Profesional.
					h.hora_desde = hora.hora_desde #Se le asigna una hora desde.
					h.hora_hasta = hora.hora_hasta #Se le asigna una hora hasta.
					h.dia_semana = dia #Se le asigna un dia de la semana.
					h.calendario = c #Se le asigna el calendario.
					#~ h.save() #Y se guarda.
					
					c.agregar_horario(h) #El Horario es agregado a la lista del Calendario.
					
					#~ print c.horarios
					#~ raw_input()
					
		"""
		#Rellenamos el Calendario generando Horarios aleatorios.
		for c in self.poblacion: #Por cada Calendario en la poblacion.
			
			for dia in range(0, 7): #Iteramos por la cantidad de dias.
				
				if dia not in self.espacio._dias_habiles:
					continue
				
				for hora in self.espacio.horas: #Tambien por la cantidad de horarios.
					
					h = Horario() #Se crea un Horario.
					h.profesional = self.profesionales[randrange(1, len(self.profesionales))] #Se le asigna un Profesional.
					h.hora_desde = hora.hora_desde #Se le asigna una hora desde.
					h.hora_hasta = hora.hora_hasta #Se le asigna una hora hasta.
					h.dia_semana = dia #Se le asigna un dia de la semana.
					h.calendario = c #Se le asigna el calendario.
					
					#Comprobamos que el Horario generado no exista en el Calendario.
					existe = False
					for franja_horaria in c.horarios:
						for hh in franja_horaria:
							if h == hh:
								existe = True
					
					#Si ya existe continuamos generando.
					if existe:
						print "Objeto eliminado."
						continue
					print "Objeto nuevo."
					#Sino lo guardamos.
					#~ h.save()
					
					#Y lo agregamos a la lista de horarios del Calendario
					c.agregar_horario(h)
		"""
	
	def evolucionar(self, ):
		print "FITNESS"
		self.fitness()
	
	def fitness(self, ):
		"""
		Asigna un puntaje a los calendarios.
		Utiliza las restricciones de los profesionales para
		determinar el valor de aptitud de los individuos.
		
		@Parametros:
		None
		
		@Return:
		None
		"""
		
		#Primera evaluacion: Que los horarios asignados cumplan las restricciones.
		
		for c in self.poblacion: #Por cada individuo en la poblacion.
			
			#Si el individuo ya fue evaluado seguimos con otro.
			if c.puntaje != 0:
				continue
			
			#Comparamos los horarios con las restricciones de
			#los profesionales. Cada superposicion vale un punto, mientras mas
			#alto sea el puntaje, menos apto es el individuo.
			
			#~ for r in self.restricciones: #Por cada restriccion.
				#~ 
				#~ for franja_horaria in c.horarios: #Por cada franja de horarios.
					#~ 
					#~ for h in franja_horaria: #Por cada por cada horario dentro de la franja.
						#~ 
						#~ for p in self.profesionales: #Por cada profesional.
							#~ 
							#~ if h.profesional != p: #Si no es el profesional del horario continuamos.
								#~ continue
							#~ 
							#~ if h.dia_semana != r.dia_semana: #Si no es el mismo dia de la semana del horario continuamos.
								#~ continue
							#~ 
							#~ if (h.desde >= r.desde and h.desde < r.hasta) or \
								#~ (h.hasta > r.desde and h.hasta <= r.hasta) or \
								#~ (h.desde <= r.desde and h.hasta >= r.hasta):
								#~ c.puntaje += 1
			
			
			#Segunda evaluacion: Que se cumplan las horas semanales y diarias de la especialidad.
			
			for e in self.especialidades: #Por cada especialidad
				
				horas_semanales = 0 #Contador de horas semanales.
				for franja_horaria in c.horarios: #Por cada franja de horarios.
					
					for h in franja_horaria: #Por cada horario en la franja horaria.
						
						#Si la especialidad del profesional es igual, contamos.
						if h.profesional.especialidad == e:
							
							horas_semanales += 1
					
				if horas_semanales != e.carga_horaria_semanal:
					c.puntaje += abs(e.carga_horaria_semanal - horas_semanales)
					
					#~ print horas_semanales
					#~ print c.puntaje
			
			for i in range(len(self.espacio._dias_habiles)):
				
				for j in self.espacio.horas:
					pass
				
			
	
	def seleccionar(self, ):
		pass
	
	@property
	def espacio(self, ):
		return self._espacio
	
	@espacio.setter
	def espacio(self, espacio):
		self._espacio = espacio
	
	@property
	def generaciones(self, ):
		return self._generaciones
	
	@generaciones.setter
	def generaciones(self, generaciones):
		self._generaciones = generaciones
	
	@property
	def poblacion(self, ):
		return self._poblacion
	
	@poblacion.setter
	def poblacion(self, poblacion):
		self._poblacion = poblacion
	
	@property
	def restricciones(self, ):
		return self._restricciones
	
	@restricciones.setter
	def restricciones(self, restricciones):
		self._restricciones = restricciones
	
	@property
	def dias(self, ):
		return self._dias
	
	@dias.setter
	def dias(self, dias):
		self._dias = dias
	
	@property
	def especialidades(self, ):
		return self._especialidades
	
	@especialidades.setter
	def especialidades(self, especialidades):
		self._especialidades = especialidades
	
