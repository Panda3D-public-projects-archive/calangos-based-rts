from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec3
import sys

class MoveCam(DirectObject):
	def __init__(self,camera):
		self.camera = camera
		self.camera.setP(-45)
		self.camera.setZ(200)
		#Centro do mapa (tribo)
		self.center = Vec3(200,200,200)
		self.keyboardSetupCam()
		taskMgr.add(self.updateCamera, "updateCamera")


	#Funcao que atribui valores de input
	def keyboardSetupCam(self):
		self.keyMap = {"camLeft":0, "camRight":0, "camFront":0, "camBack":0, "wheel-in":0, "wheel-out":0}
		self.accept("a", self.setKey, ["camLeft", 1])
		self.accept("a-up", self.setKey, ["camLeft", 0])
		self.accept("d", self.setKey, ["camRight", 1])
		self.accept("d-up", self.setKey, ["camRight", 0])
		self.accept("w", self.setKey, ["camFront", 1])
		self.accept("w-up", self.setKey, ["camFront", 0])
		self.accept("s", self.setKey, ["camBack", 1])
		self.accept("s-up", self.setKey, ["camBack", 0])
		self.accept("space", self.returnToCenter)
		self.accept("wheel_up", self.setKey, ["wheel-in",1])
		self.accept("wheel_down", self.setKey, ["wheel-out",1])


	#Funcao que da valor a chave
	def setKey(self, key, value):
		self.keyMap[key] = value


	#Funcao que retorna a camera ao centro do mapa (tribo) // Pode ser feita por uma transicao lenta caso pedido
	def returnToCenter(self):
		self.camera.setPos(self.center)

	def getX(self):
		return self.camera.getX()

	def getY(self):
		return self.camera.getY()

	def getPos(self, render):
		return self.camera.getPos()


	def updateCamera(self,task):
		#Atencao: se mudar o angulo da camera, tem que recalcular os valores
		cameraSpeed = 5

		#Zoom da camera
		if (self.keyMap["wheel-in"]!=0): 
			if (self.camera.getZ() > 130):
				self.camera.setY(self.camera, cameraSpeed)

			self.keyMap["wheel-in"] = 0 
		elif (self.keyMap["wheel-out"]!=0): 
			if (self.camera.getZ() < 200): 
				self.camera.setY(self.camera, -cameraSpeed)

			self.keyMap["wheel-out"] = 0 

		#Movimentacao da camera pelo teclado
		if (self.keyMap["camFront"]!=0):
			self.camera.setY(self.camera, cameraSpeed)
			self.camera.setZ(self.camera, cameraSpeed)
		elif (self.keyMap["camBack"]!=0):
			self.camera.setY(self.camera, -cameraSpeed)
			self.camera.setZ(self.camera, -cameraSpeed)
		if (self.keyMap["camLeft"]!=0):
			self.camera.setX(self.camera, -cameraSpeed)
		elif (self.keyMap["camRight"]!=0):
			self.camera.setX(self.camera, cameraSpeed)


		#Movimentacao da camera pelo mouse
		if base.mouseWatcherNode.hasMouse():
			mpos = base.mouseWatcherNode.getMouse()
			if mpos.getX() > 0.8:
				self.camera.setX(self.camera, mpos.getX()*2)
			if mpos.getX() < -0.8:
				self.camera.setX(self.camera, mpos.getX()*2)
			if mpos.getY() > 0.8:
				self.camera.setY(self.camera, mpos.getY()*2)
				self.camera.setZ(self.camera, mpos.getY()*2)
			if mpos.getY() < -0.8:
				self.camera.setY(self.camera, mpos.getY()*2)
				self.camera.setZ(self.camera, mpos.getY()*2)

		return task.cont


	def getX(self):
		return self.camera.getX()

	def getY(self):
		return self.camera.getY()


