from direct.showbase.ShowBase import ShowBase
from direct.actor import Actor
from panda3d.core import CollisionRay,CollisionHandlerFloor, CollisionNode,GeomNode,CollisionTraverser, CollisionHandlerQueue, CollisionSphere, BitMask32, Vec3,Vec4,Point3
from FollowCam import FollowCam
from MoveCam import MoveCam
from LoadCharEnvir import loadCharEnvir
from direct.task import Task
from direct.interval.IntervalGlobal import Parallel, Sequence, Func
from math import *
import random
import sys

class App(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		base.disableMouse()

		#Carrega o terreno
		self.terrain = loadCharEnvir().loadEnvir()


		#Declaracao de variaveis
		self.isMoving = False
		self.getClick = 0			#Quantos objetos foram clicados
		self.clickedObj = None
		self.terrainSize = 1024
		self.numLizards = 5
		self.numMaleLizards = 0
		self.numFemaleLizards = 0
		#self.contChamGetMed = 0		#Contador para saber se atualiza o ponto medio


		#Carrega os lagartos iniciais
		self.lizards = []
		for i in range(self.numLizards):
			randNum = random.randint(10,20)
			randNum2 = random.randint(10,20)
			lizard = loadCharEnvir().loadLizard(100 + (randNum+randNum2)*i,150 + (randNum+randNum2)*i,3)
			lizard.setTag("ID",str(i))
			self.lizards.append(lizard)
			if (lizard.getTag("femaleOrMale") == "1"):
				self.numMaleLizards = self.numMaleLizards + 1
			else:
				self.numFemaleLizards = self.numFemaleLizards + 1



		#Calcula o ponto medio dos lagartos, tanto femeas quantos machos
		self.getMedianGenderPoints()
		#taskMgr.add(self.getCloserToMedian, "Aproxima os lagartos do ponto medio dos generos")



 

		#Adiciona as tasks e as funcoes de teclado e mouse
		self.taskMgr.add(self.updateTask, "update")
		self.keyboardSetup()


		#CAMERAS:
		#Faz a camera seguir o lagarto
		#self.followcam = FollowCam(self.camera, self.lizards[0])

		#Faz a camera visualizar como um deus
		self.MoveCam = MoveCam(self.camera)


		#Ativa as colisoes
		self.setupMouseCollision()


	#Funcao que ajusta o angulo
	def clampAngle(self, angle):
		while angle < -180:
			angle = angle + 360
		while angle > 180:
			angle = angle -360

		return angle


	#Atribui um valor especifico para uma chave
	def keyboardSetup(self):
		self.keyMap = {"left":0, "right":0, "forward":0, "backward":0}
		self.accept("escape", sys.exit)
		self.accept("arrow_left", self.setKey, ["left", 1])
		self.accept("arrow_left-up", self.setKey, ["left", 0])
		self.accept("arrow_right", self.setKey, ["right", 1])
		self.accept("arrow_right-up", self.setKey, ["right", 0])
		self.accept("arrow_up", self.setKey, ["forward", 1])
		self.accept("arrow_up-up", self.setKey, ["forward", 0])
		self.accept("arrow_down", self.setKey, ["backward", 1])
		self.accept("arrow_down-up", self.setKey, ["backward", 0])
		self.accept("mouse1", self.leftMouseCommands)	#Pode ser adicionado um drag aqui
		self.accept("mouse3", self.rightMouseCommands)


	#Funcao que calcula o ponto medio da densidade de lagartos de cada genero
	def getMedianGenderPoints(self):
			self.medianMalePoint = (0,0,0)
			self.medianFemalePoint = (0,0,0)

			#Calculo do somatorio dos pontos para cada genero
			for i in range(self.numLizards):
				if (self.lizards[i].getTag("femaleOrMale") == "1"):
					self.medianMalePoint = self.lizards[i].getPos() + self.medianMalePoint
				else:
					self.medianFemalePoint = self.lizards[i].getPos() + self.medianFemalePoint

			#Calculo do ponto medio de cada genero
			if (self.numMaleLizards != 0):
				self.medianMalePoint = (self.medianMalePoint[0]/self.numMaleLizards, self.medianMalePoint[1]/self.numMaleLizards, self.medianMalePoint[2]/self.numMaleLizards)
			if (self.numFemaleLizards != 0):
				self.medianFemalePoint = (self.medianFemalePoint[0]/self.numFemaleLizards, self.medianFemalePoint[1]/self.numFemaleLizards, self.medianFemalePoint[2]/self.numFemaleLizards)



#=====================================================================================
	#NAO ESTA PRONTA // NAO FUNCIONA
	#Funcao que faz com que os lagartos, dependendo do genero, aproximem-se
#=====================================================================================

	"""
	def getCloserToMedian(self, task):

		maleMedianPoint = render.attachNewNode("male median point")
		maleMedianPoint.setPos(self.medianMalePoint)
		femaleMedianPoint = render.attachNewNode("female median point")
		femaleMedianPoint.setPos(self.medianFemalePoint)

		for i in range(self.numLizards):
			#Se for macho, procura for femeas
			if (self.lizards[i].getTag("femaleOrMale") == 1):
				lizardAuxPoint = render.attachNewNode("ponto auxiliar para obter heading")
				lizardAuxPoint.setPos(self.lizards[i].getPos())
				lizardAuxPoint.lookAt(femaleMedianPoint)
				self.lizards[i].setH(self.clampAngle(lizardAuxPoint.getH() + 180))
				self.lizards[i].setPos(self.lizards[i], self.lizards[i].getRelativeVector(femaleMedianPoint, Vec3(0.1,-0.1,0)))	
				print self.lizards[i].getRelativeVector(femaleMedianPoint, Vec3(0.1,-0.1,0))
				
				#Respeitando os limites do terreno
				if (self.lizards[i].getX() < 0):
					self.lizards[i].setX(0)
				elif (self.lizards[i].getX() > self.terrainSize):
					self.lizards[i].setX(self.terrainSize)
				if (self.lizards[i].getY() < 0):
					self.lizards[i].setY(0)
				elif (self.lizards[i].getY() > self.terrainSize):
					self.lizards[i].setY(self.terrainSize)
	
			#Se for femea, procura por machos
			else:
				self.lizards[i].lookAt(maleMedianPoint)
				self.lizards[i].setPos(self.lizards[i], self.lizards[i].getRelativeVector(maleMedianPoint, Vec3(0.1,-0.1,0)))
				
				#Respeitando os limites do terreno
				if (self.lizards[i].getX() < 0):
					self.lizards[i].setX(0)
				elif (self.lizards[i].getX() > self.terrainSize):
					self.lizards[i].setX(self.terrainSize)
				if (self.lizards[i].getY() < 0):
					self.lizards[i].setY(0)
				elif (self.lizards[i].getY() > self.terrainSize):
					self.lizards[i].setY(self.terrainSize)

			#Faz uma atualizacao pra saber se deve atualizar o ponto medio
			self.contChamGetMed = self.contChamGetMed + 1
			if (self.contChamGetMed == 1000):
				self.contChamGetMed = 0
				self.getMedianGenderPoints()

		return task.cont"""
				

#=====================================================================================
#A ATRIBUICAO DO BOTAO DIREITO SERA COMPLETAMENTE REFEITA, E ESTA SERVE APENAS PARA ILUSTRAR A IDEIA
#ESTA ATRIBUICAO ESTA ERRADA
#=====================================================================================
	def rightMouseCommands(self):
		if self.mouseWatcherNode.hasMouse():
			mpos = base.mouseWatcherNode.getMouse()
			if (self.clickedObj != None):
				self.moveCharacter(mpos.getX(), mpos.getY())


	#FUNCAO PROVISORIA:
	#FALTA AJUSTAR - COMO FAZER PARA OPERAR AS ENTRADAS SEPARADAMENTE?
	def moveCharacter(self, posX, posY):
		self.mClickRay.setFromLens(self.camNode, posX, posY)
		self.mClicker.traverse(self.render)
		if (self.mCollisionQue.getNumEntries() > 0):
			self.mCollisionQue.sortEntries()
			entry = self.mCollisionQue.getEntry(0)

			self.target = render.attachNewNode("target point")
			self.target.setPos(2*self.clickedObj.getX() - entry.getSurfacePoint(render).getX(), 2*self.clickedObj.getY() - entry.getSurfacePoint(render).getY(), entry.getSurfacePoint(render).getZ())
			self.finalPosY = self.target.getY()
			self.finalPosX = self.target.getX()

			finalHeading = render.attachNewNode("final heading")
			finalHeading.setPos(self.clickedObj.getPos())
			finalHeading.lookAt(self.target.getPos())
			self.Heading = finalHeading.getH()
			self.Heading = self.clampAngle(self.Heading)

			if (self.Heading-self.clickedObj.getH() > 150):
				turnTime = 4
			else:
				if (self.Heading-self.clickedObj.getH() > 100):
					turnTime = 3
				else:
					if (self.Heading-self.clickedObj.getH() > 50):
						turnTime = 2
					else:
						if (self.Heading-self.clickedObj.getH() < -50):
							turnTime = 2
						else:
							if (self.Heading-self.clickedObj.getH() < -100):
								turnTime = 3
							else:
								if (self.Heading-self.clickedObj.getH() < -150):
									turnTime = 4
								else:
									turnTime = 1
			self.deltaSX = self.target.getX()-self.clickedObj.getX()
			self.deltaSY = self.target.getY()-self.clickedObj.getY()
			self.deltaS = sqrt((self.target.getY()-self.clickedObj.getY())*(self.target.getY()-self.clickedObj.getY()) + (self.target.getX()-self.clickedObj.getX())*(self.target.getX()-self.clickedObj.getX()))
			t = self.deltaS/3
			changeHeading = self.clickedObj.hprInterval(turnTime, (self.Heading,0,0), (self.clickedObj.getH(),0,0))
			changePos = self.clickedObj.posInterval(t, self.target.getPos(), self.clickedObj.getPos())
			self.clickedObj.loop("walk", restart = 0)
			self.counter = 0
			moveInterv = Sequence(changeHeading, Func(self.stopAnimation))
			moveInterv.start()
			
	def stopAnimation(self):
		taskMgr.add(self.movingCharacter, "moving character")

	def movingCharacter(self,task):
		if self.counter < 130:
			self.clickedObj.setX(self.clickedObj.getX() - self.deltaSX/130)
			self.clickedObj.setY(self.clickedObj.getY() - self.deltaSY/130)
			self.counter = self.counter + 1
			return task.cont
		else:
			self.clickedObj.stop()
			taskMgr.remove("moving character")	


#=====================================================================================
#=====================================================================================
#=====================================================================================


	#Atribui valor a uma chave
	def setKey(self, key, value):
		self.keyMap[key] = value



	#Atualiza o game
	def updateTask(self, task):
		self.updateLizard()
		return Task.cont



	#Funcao do botao esquerdo do mouse
	def leftMouseCommands(self):
		if self.mouseWatcherNode.hasMouse():
			mpos = base.mouseWatcherNode.getMouse()

			self.mClickRay.setFromLens(self.camNode, mpos.getX(), mpos.getY())

			self.mClicker.traverse(self.render)

			if (self.mCollisionQue.getNumEntries() > 0):
				self.mCollisionQue.sortEntries()
				entry = self.mCollisionQue.getEntry(0)
				clickedObject = entry.getIntoNodePath()

				clickedObject = clickedObject.findNetTag("clickable")
				if not clickedObject.isEmpty():
					pos = entry.getSurfacePoint(self.render)
					self.getClick = 1
					clickedObjectId = clickedObject.findNetTag("ID")
					self.clickedObjId = clickedObjectId
					#Procura o lagarto clicado
					for i in range(self.numLizards):
						if (self.lizards[i].getTag("ID") == self.clickedObjId.getTag("ID")):
							self.clickedObj = self.lizards[i]
					return
				else:
					#Zera se nao houverem objetos clicaveis proximos
					self.getClick = 0




	#Define a colisao do mouse com objetos no terreno
	def setupMouseCollision(self):

		self.mClicker = CollisionTraverser()          
		self.mCollisionQue    = CollisionHandlerQueue()

		self.mClickRay = CollisionRay()
		self.mClickRay.setOrigin(self.camera.getPos(self.render))
		self.mClickRay.setDirection(render.getRelativeVector(camera, Vec3(0,1,0)))

		self.mClickNode = CollisionNode('clickRay')
		self.mClickNode.addSolid(self.mClickRay)

		self.mClickNP = self.camera.attachNewNode(self.mClickNode)

		self.mClickNode.setFromCollideMask(GeomNode.getDefaultCollideMask())

		self.mClicker.addCollider(self.mClickNP, self.mCollisionQue)



	#Atualiza o personagem se algum botao foi pressionado
	#POSTERIORMENTE SERA RETIRADA - ESTA AQUI APENAS PARA DEBUG/EXEMPLIFICACAO
	def updateLizard(self):
		speedFactor = 3

		if (self.getClick != 0):

			#Se o personagem esta se mexendo, rode a animacao
			#BUG - Se o jogador estiver pressionando o botao de andar enquanto muda de personagem, trava a animacao
			if (self.keyMap["forward"]!=0) or (self.keyMap["left"]!=0) or (self.keyMap["right"]!=0) or (self.keyMap["backward"]!=0): 
				if self.isMoving is False: 
					self.clickedObj.loop("walk", restart = 0) 
					self.isMoving = True 
			else: 
				if self.isMoving: 
					self.clickedObj.stop() 
					self.isMoving = False 

			#if (self.clicked != None):
			if (self.keyMap["left"]!=0):
				self.clickedObj.setH(self.clickedObj.getH()+1)
			elif (self.keyMap["right"]!=0):
				self.clickedObj.setH(self.clickedObj.getH()-1)
			if (self.keyMap["forward"]!=0):
				self.clickedObj.setY(self.clickedObj, -speedFactor)
			elif (self.keyMap["backward"]!=0):
				self.clickedObj.setY(self.clickedObj, speedFactor)

			#Respeitando os limites do terreno
			if (self.clickedObj.getX() < 0):
				self.clickedObj.setX(0)
			elif (self.clickedObj.getX() > self.terrainSize):
				self.clickedObj.setX(self.terrainSize)
			if (self.clickedObj.getY() < 0):
				self.clickedObj.setY(0)
			elif (self.clickedObj.getY() > self.terrainSize):
				self.clickedObj.setY(self.terrainSize)


		
app = App()
app.run()
