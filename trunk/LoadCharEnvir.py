from direct.actor import Actor
from panda3d.core import GeoMipTerrain
import random

class loadCharEnvir():
	#Carrega o terreno
	def loadEnvir(self):
		terrain = GeoMipTerrain("terreno")
		terrain.setHeightfield("terreno/preto.png")
		terrain.setColorMap("terreno/tile_far.jpg")
		terrain.getRoot().setScale(5,5,50)
		terrain.getRoot().reparentTo(render)
		terrain.generate()


	#Permite que o objeto seja clicavel com o botao esquerdo
	def makeClickable(self,newObj): 
		newObj.setTag("clickable","1")

	def setMale(self, newObj):
		newObj.setTag("femaleOrMale", "1")

	def setFemale(self, newObj):
		newObj.setTag("femaleOrMale", "0")


	#Carrega um lagarto na cena, dada uma posicao
	def loadLizard(self, x, y, z):
		lizard = Actor.Actor("lagarto/model.bam", {"walk": "lagarto/walk.bam"})
		texture = loader.loadTexture("lagarto/texture.jpg")
		lizard.reparentTo(render)
		lizard.setScale(0.05)
		lizard.setPos(x,y,z)
		self.makeClickable(lizard)
		randomNumber = random.randint(0, 2)
		if (randomNumber == 1):
			self.setMale(lizard)
			lizard.setColor(0,0,1,1)
		else:
			self.setFemale(lizard)
			lizard.setColor(1,0,0,1)
		return(lizard)


