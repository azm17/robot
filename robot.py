# -*- coding: utf-8 -*-
"""    
注意:
   オブジェクトの描画はareaからしなければならない
   plt.figure()で初期化されるため

"""
import matplotlib.pyplot as plt

# オブジェクト
class MyObject():
    def __init__(self, x, y):
        self.x1 = x
        self.y1 = y
# エリア
class Area(MyObject):
    def __init__(self, x, y, width, height):# エリア設定
        super(Area, self).__init__(x, y)
        self.x2 = x + width
        self.y2 = y + height
        
    def draw(self):# 描画
        plt.figure(figsize=(5, 5))
        width = 0.9
        x = [self.x1 - width, 
             self.x1 - width, 
             self.x2 + width, 
             self.x2 + width, 
             self.x1 - width]
        
        y = [self.y1 - width, 
             self.y2 + width, 
             self.y2 + width, 
             self.y1 - width, 
             self.y1 - width]

        plt.plot(x, y, color='#1f77b4')
        margin_width = 5
        plt.ylim(self.x1 - margin_width, 
                 self.x2 + margin_width)
        plt.xlim(self.y1 - margin_width, 
                 self.y2 + margin_width)
# 障害物
class Obstacle(MyObject):
    def __init__(self, x, y, width, height):# エリア設定
        super(Obstacle, self).__init__(x, y)
        self.x2 = x + width
        self.y2 = y + height
    
    def draw(self):# 描画
        width = 0.9
        x = [self.x1 - width, 
             self.x1 - width, 
             self.x2 + width, 
             self.x2 + width, 
             self.x1 - width]
        
        y = [self.y1 - width, 
             self.y2 + width, 
             self.y2 + width, 
             self.y1 - width, 
             self.y1 - width]

        plt.plot(x, y, color='#FF0000')
# エージェント
class Agent(MyObject):
    def __init__(self, x, y):# 初期設定
        super(Agent, self).__init__(x, y)
    
    def getAgent(self):# 座標を取得
        return (self.x1, self.y1)
    
    def area_collision(self, area):# エリアの衝突判定
        # エリアの範囲に出たら，エリア内の戻す
        if self.x1 <= area.x1:
            self.x1 = area.x1
        if self.y1 <= area.y1:
            self.y1 = area.y1
        if self.x1 >= area.x2:
            self.x1 = area.x2
        if self.y1 >= area.y2:
            self.y1 = area.y2
    
    def obstacle_collision(self, obstacle, x, y):# 障害物との衝突判定
        if self.x1 >= obstacle.x1 \
            and self.x1 <= obstacle.x2 \
            and self.y1 >= obstacle.y1 \
            and self.y1 <= obstacle.y2:# 障害物に侵入した時
            self.x1 = x
            self.y1 = y
    
    def goal_collision(self, obstacle):# 障害物との衝突判定
        if self.x1 >= obstacle.x1 \
            and self.x1 <= obstacle.x2 \
            and self.y1 >= obstacle.y1 \
            and self.y1 <= obstacle.y2:# 障害物に侵入した時
            return True
        return False
        
    def draw(self):# 描画
        plt.plot(self.x1, 
                 self.y1,
                 marker='.', 
                 markersize = 20, 
                 color='#1f77b4')
    
    def up(self):# 上へ移動
        self.y1 += 1
    def down(self):# 下へ移動
        self.y1 -= 1
    def right(self):# 右へ移動
        self.x1 += 1
    def left(self):# 左へ移動
        self.x1 -= 1

class Goal(MyObject):
    def __init__(self, x, y, width, height):# エリア設定
        super(Goal, self).__init__(x, y)
        self.x2 = x + width
        self.y2 = y + height
    
    def draw(self):# 描画
        width = 0.9
        x = [self.x1 - width, 
             self.x1 - width, 
             self.x2 + width, 
             self.x2 + width, 
             self.x1 - width]
        
        y = [self.y1 - width, 
             self.y2 + width, 
             self.y2 + width, 
             self.y1 - width, 
             self.y1 - width]

        plt.plot(x, y, color='#008000')
# mainの関数
def run(move):
    fig_interval = 1
    fig_draw = False
    
    area = Area(0, 0, 30, 30)# Area 生成
    agent = Agent(2, 28)# agent 生成
    goal = Goal(28, 28, 2, 2)
    obstacle1 = Obstacle(15, 5, 2, 5)# 障害物1 生成
    obstacle2 = Obstacle(5, 15, 5, 3)# 障害物2 生成
    
    bstacle_list = [obstacle1, obstacle2]# 障害物リスト
    object_list = [area, agent, goal] + bstacle_list# オブジェクトリスト
    #　描画
    if fig_draw:
        for oject in object_list:
                oject.draw()
    # メインの計算
    for t in range(len(move)):
        x_before = agent.x1#移動前のx座標
        y_before = agent.y1#移動前のy座標
        # --移動--
        if move[t] == 'UP':
            agent.up()
        if move[t] == 'DOWN':
            agent.down()
        if move[t] == 'RIGHT':
            agent.right()
        if move[t] == 'LEFT':
            agent.left()
        # --衝突判定--
        agent.area_collision(area)# エリア
        for bstacle in bstacle_list:# 障害物
            agent.obstacle_collision(bstacle, x_before, y_before)
        # --ゴール判定--
        if agent.goal_collision(goal): return agent.getAgent()# ゴール(計算の終了)
        #　--描画--
        if fig_draw:
            if t % fig_interval ==0:
                for oject in object_list:
                    oject.draw()
    # 計算の終了
    return agent.getAgent()

if __name__ == "__main__":
    move_list = []
    for i in range(30):
         move_list.append('RIGHT')

    print(run(move_list))