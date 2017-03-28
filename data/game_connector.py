from .states import level1
from .components import Agent
import pygame as pg
import datetime
keybinding = {
    'action':pg.K_s,
    'jump':pg.K_a,
    'left':pg.K_LEFT,
    'right':pg.K_RIGHT,
    'down':pg.K_DOWN
}

class GameConnector(object):
	def __init__(self,level):
		self.level = level
		self.agent = Agent.Agent()
		self.enemys = 0
		self.jumping = False
		self.jumpCounter = 0
		self.hazardsLogged = False
		

	def getEnemyPos(self):
		for enemy in self.level.enemies_group:
			if(enemy.rect.x != 0):
				if(enemy.rect.x - self.level.mario.rect.x < -20):
					self.level.enemies_group.remove(enemy)
				else:
					self.enemys = enemy.rect.x
					break
	def getPipePos(self):
		self.agent.pipe_list = self.level.pipe_list

	def getHolePos(self):
		for groundBit in self.level.ground_list:
			if((groundBit.rect.x + groundBit.width) != 0):
				self.agent.hole_list.append(groundBit.rect.x + groundBit.width)


	def getStepPos(self):
		self.agent.step_list = self.level.step_list

	def executeInput(self,tools):
		if self.level.started:
			self.getEnemyPos()
			if self.hazardsLogged == False:
				self.getPipePos()
				self.getHolePos()	
				self.getStepPos()
				self.hazardsLogged = True
			action = self.agent.nextMove(self.level.mario.rect.x,self.enemys)
			current = datetime.datetime.now().second
			if self.jumping:
				if self.jumpCounter >= 25:
					print("Im not jumping")
					self.jumping = False
					l = list(tools.keys)
					l[keybinding["jump"]] = 0
					tools.keys = tuple(l)
					return
				else:
					self.jumpCounter +=1
					return
			if action == "jump":
				if not self.jumping:
					self.jumping = True
					self.jumpCounter = 0
			l = list(tools.keys)
			l[keybinding[action]] = 1
			tools.keys = tuple(l)
