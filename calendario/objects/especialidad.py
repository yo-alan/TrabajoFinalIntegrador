# -*- coding: utf-8 -*-
from django.db import models

def purificador(nombre):
	
	nombre_copia = nombre
	
	nombre = ""
	
	for n in nombre_copia.split(' '):
		
		if not n.isalpha():
			raise
		
		nombre = nombre + " " + n.capitalize()	
	
	if nombre.startswith(' '):
		nombre = nombre[1:]
	
	return nombre

class Especialidad(models.Model):
	
	nombre = models.CharField(max_length=100, null=False)
	carga_horaria_semanal = models.IntegerField(default=0, null=False)
	max_horas_diaria = models.IntegerField(default=0, null=False)
	
	def __str__(self, ):
		return unicode(self.nombre).encode('utf-8')
	
	def __eq__(self, o):
		return self.nombre == o.nombre	
	
	def setnombre(self, nombre):
		
		if nombre == "":
			raise Exception("El nombre no puede estar vacío.")
		
		try:
			nombre = purificador(nombre)
		except:
			raise Exception("El nombre posee caracteres no permitidos.")
		
		self.nombre = nombre
	
	def setcarga_horaria_semanal(self, carga_horaria_semanal):
		
		if carga_horaria_semanal == "" or int(carga_horaria_semanal) == 0:
			raise Exception("La carga horaria semanal no puede ser 0.")
		
		self.carga_horaria_semanal = carga_horaria_semanal
	
	def setmax_horas_diaria(self, max_horas_diaria):
		
		if max_horas_diaria == "" or int(max_horas_diaria) == 0:
			raise Exception("La horas diarias máxima no puede ser 0.")
		
		self.max_horas_diaria = max_horas_diaria
	