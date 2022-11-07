import random
import sys,json,time,pygame,threading,base_gui,math
from math import floor
# load initial #
pygame.init()
root_window=pygame.display.set_mode((1024,576),pygame.RESIZABLE);screen=root_window.copy().convert_alpha();clock=pygame.time.Clock()
loading_font=pygame.font.Font('assets/ARLRDBD.TTF',20);loading_progress=0.0
# loading screen #
def loading_wait():
    loading_cnt=0;loading_bar_rect=lambda load_prg: (root_window.get_rect().centerx - 100, root_window.get_rect().centery+20, load_prg*200, 14)
    while globals()['loading_progress']!=1.0:new_ld_prg=globals()['loading_progress'];loading_cnt+=1;loading_cnt%=128;loading=loading_font.render('Loading'+'.'*(loading_cnt//32),True,(255,255,255));root_window.fill((0,0,0));screen.fill((0,0,0));pygame.draw.rect(screen,(255,255,255),loading_bar_rect(new_ld_prg));pygame.draw.rect(screen,(255,255,255),(root_window.get_rect().centerx-104,root_window.get_rect().centery+16,208,22),2);screen.blit(loading,(root_window.get_rect().centerx-loading.get_width()/2,root_window.get_rect().centery-loading.get_height()/2));root_window.blit(screen,(0,0));pygame.display.flip();pygame.display.update();clock.tick(60)
loading_thread = threading.Thread(target=loading_wait);loading_thread.daemon=True;loading_thread.start()
# load rest required #
with open("assets/config") as assets_raw: assets = json.loads(assets_raw.read());del assets['IMPORTANT NOTICE']
debug_mode=False
loading_progress=0.1
target_list=["First","Last","Near","Far","Strongest","Weakest","Random"]
def anim_need_money():
    def need_money_anim():
            orgx=gameplay.text_displayers[0].rect.x; x=0;clock_clock = pygame.time.Clock();gameplay.text_displayers[0].text_color=(255,0,0)
            def easeOutExpo(x):return 1 - pow(2, -10 * x)
            while x<1: gameplay.text_displayers[0].rect.x=orgx+easeOutExpo(x)*5; x+=0.1; clock_clock.tick(60)
            x=0
            while x<1: gameplay.text_displayers[0].rect.x=orgx+(easeOutExpo(x)*-10); x+=0.1; clock_clock.tick(60)
            x=0
            while x<1: gameplay.text_displayers[0].rect.x=orgx+(easeOutExpo(x)*5); x+=0.1; clock_clock.tick(60)
            gameplay.text_displayers[0].text_color=(0,0,0);gameplay.text_displayers[0].f_suf = [gameplay.text_displayers[0].font.render(gameplay.text_displayers[0].text, gameplay.text_displayers[0].antialias, gameplay.text_displayers[0].text_color)];gameplay.text_displayers[0].rect.x=orgx
    need_money_anim_thr=threading.Thread(target=need_money_anim); need_money_anim_thr.start()
def upgrade(data):
    turret, money = data
    if money >= turret.cost[2] and not isinstance(turret.level, str) and not turret.level >= 5:
        turret.level+=1;money-=turret.cost[2];turret.cost[2]=int(turret.cost[2]*1.5);turret.BULLETDAMAGE=int(turret.BULLETDAMAGE+(turret.BULLETDAMAGE*0.4));turret.cost[1]=int(turret.cost[1]*1.8)
        if turret.level == 3: turret.RANGE=int(turret.RANGE+(turret.RANGE*0.2))
        if turret.level == 4: turret.shoot_speed=round((turret.shoot_speed-(turret.shoot_speed*0.5))*1000)/1000
        if turret.level == 5: turret.level = "5 (MAX)"
        return True, int(money) #if buy success
    if money < turret.cost[2]:anim_need_money()
    return False, money # if not buy success
def sell(data):
    turret, money = data;gameplay.gameplay_items.remove(turret); gameplay.gameplay_area_data[turret.area] = None; gameplay.gameplay_area_data[turret.area+gameplay.direction_memory_adress] = 0;gameplay.slc.selecting=False;gameplay.gameplay_items.remove(gameplay.slc.info__);gameplay.slc.info__=None
    return True, turret.cost[1]+money
def change_mode(data):
    turret, null = data;turret.mode = (turret.mode + 1) % len(target_list)
    return None, null
class Info_Slide:
    def __init__(self,turret):
        self.image=pygame.Surface((round(root_window.get_width()/6),root_window.get_height()));self.image.fill((146,220,129))
        self.rect=self.image.get_rect(topleft=(root_window.get_width()-(round(root_window.get_width()/6)),0));self.target=turret
        self.bt_=[
            base_gui.TextButton(upgrade,"Upgrade - " + str(turret.cost[2]), "assets/ARLRDBD.TTF", 15, (self.rect.left,150), (round(root_window.get_width()/6),30), (0,0,0), text_alignment="center", background=(131, 222, 164)),
            base_gui.TextButton(sell,"Sell - " + str(turret.cost[1]), "assets/ARLRDBD.TTF", 15, (self.rect.left,180), (round(root_window.get_width()/6),30), (0,0,0), text_alignment="center", background=(163, 212, 181)),
            base_gui.TextButton(change_mode,"Target - " + target_list[turret.mode], "assets/ARLRDBD.TTF", 15, (self.rect.left,210), (round(root_window.get_width()/6),30), (0,0,0), text_alignment="center", background=(173, 222, 131)),]
        self.info_texts=[
            base_gui.TextFrame("Info:","assets/ARLRDBD.TTF", 15, (0,120), (round(root_window.get_width()/6),270), (0,0,0), text_alignment="center"),
            base_gui.TextFrame("Level: "+str(turret.level),"assets/ARLRDBD.TTF", 15, (0,120), (round(root_window.get_width()/6),30), (0,0,0), text_alignment="center", background=(47, 208, 187)),
            base_gui.TextFrame("Damage: "+str(turret.BULLETDAMAGE),"assets/ARLRDBD.TTF", 15, (0,120), (round(root_window.get_width()/6),320), (0,0,0), text_alignment="center"),
            base_gui.TextFrame("Attack spd: "+str(turret.shoot_speed)+" sec.","assets/ARLRDBD.TTF", 15, (0,120), (round(root_window.get_width()/6),360), (0,0,0), text_alignment="center"),
            base_gui.TextFrame("Range: "+str(turret.RANGE),"assets/ARLRDBD.TTF", 15, (0,120), (round(root_window.get_width()/6),400), (0,0,0), text_alignment="center"),
        ]
        self.TextFrame_functions_info=[lambda : "Level: " + str(self.target.level), lambda : "Damage:" + str(self.target.BULLETDAMAGE), lambda : "Attack spd: " + str(self.target.shoot_speed) + " sec", lambda : "Range: " + str(self.target.RANGE)]
        self.TextFrame_functions_bt=[lambda :"Upgrade - "+str(self.target.cost[2]),lambda :"Sell - "+str(self.target.cost[1]),lambda :"Target - "+target_list[self.target.mode]]
        self.update()#temporary 0
    def update(self):
        for textFrame_index in range(len(self.info_texts)-1):self.info_texts[textFrame_index+1].text=self.TextFrame_functions_info[textFrame_index](); self.info_texts[textFrame_index + 1].f_suf=[self.info_texts[textFrame_index + 1].font.render(self.info_texts[textFrame_index + 1].text, self.info_texts[textFrame_index + 1].antialias, self.info_texts[textFrame_index + 1].text_color)]
        for textFrame_index_bt in range(len(self.bt_)):self.bt_[textFrame_index_bt].text=self.TextFrame_functions_bt[textFrame_index_bt](); self.bt_[textFrame_index_bt].f_suf=[self.bt_[textFrame_index_bt].font.render(self.bt_[textFrame_index_bt].text, self.bt_[textFrame_index_bt].antialias, self.bt_[textFrame_index_bt].text_color)]
        self.image.fill((146,220,129));self.image.blit(self.target.org_img,(self.image.get_rect().centerx-self.target.org_img.get_rect().centerx,30))
        for index, bt in enumerate(self.bt_):this_bt_rect=(bt.rect.left-self.rect.left,bt.rect.top-self.rect.top);self.image.blit(bt.image, this_bt_rect);self.image.blit(bt.f_suf[0], (this_bt_rect[0] + getattr(bt.image.get_rect(), bt.ext_anchor)[0]-bt.f_suf[0].get_rect().centerx, this_bt_rect[1] + getattr(bt.image.get_rect(), bt.ext_anchor)[1]-bt.f_suf[0].get_rect().centery))
        for text in self.info_texts:self.image.blit(text.image, text.rect);self.image.blit(text.f_suf[0], (text.rect.left + getattr(text.image.get_rect(), text.ext_anchor)[0]-text.f_suf[0].get_rect().centerx, text.rect.top + getattr(text.image.get_rect(), text.ext_anchor)[1]-text.f_suf[0].get_rect().centery))
    def pressed(self, mouse_pos, money):
        otb = False
        for bt in self.bt_:
            bt.args=self.target, money;funct = bt.run_when_clicked(mouse_pos)
            if funct: self.update(); money = funct[1]; otb=True
        return money, otb
loading_progress=0.15
class Slc:
    def __init__(self,area_size,area_grid,parent):self.image=pygame.Surface((round(area_size[0]/area_grid[0]+1),round(area_size[1]/area_grid[1]+1)));self.image.set_alpha(50);self.rect=self.image.get_rect(center=(-100,-100));self.area_grid=area_grid;self.parent=parent;self.area_size=self.parent.rect.size;self.inner_img=None;self.cc_slot=None;self.at_area=False;self.placing=False;self.selecting=False;self.info__=None;self.turret_range=None
    def run__(self,mouse_pos,c_slot,c_dir):
        if self.info__ and self.selecting: self.info__.update()
        if self.parent.rect.right>=mouse_pos[0]>=self.parent.rect.left and self.parent.rect.bottom>=mouse_pos[1]>=self.parent.rect.top:
            rx,ry=floor(mouse_pos[0]/(self.area_size[0]/self.area_grid[0])),floor(mouse_pos[1]/(self.area_size[1]/self.area_grid[1]))
            if rx>=self.area_grid[0]:rx=self.area_grid[0]-1
            if ry>=self.area_grid[1]:rx=self.area_grid[1]-1
            self.rect.topleft=self.area_size[0]/self.area_grid[0]*rx,self.area_size[1]/self.area_grid[1]*ry
            if c_slot and(not self.cc_slot or self.cc_slot!=c_slot):self.cc_slot=c_slot;self.inner_img=self.cc_slot((0,0),0,0).image
            elif not c_slot:self.cc_slot=None;self.inner_img=None;self.image.fill((0,0,0))
            if self.inner_img:self.turret_range=self.cc_slot((0,0),0,0).RANGE;self.image.fill((0,0,0));self.inner_img=self.cc_slot((0,0),0,c_dir).image;self.image.blit(pygame.transform.scale(self.inner_img,self.rect.size), (0, 0))
            self.at_area=True;return
        self.at_area=False
    def select__(self,mouse_pos,area_gameplay_data,on_top_button):
        rx, ry = floor(mouse_pos[0] / (self.area_size[0] / self.area_grid[0])), floor(mouse_pos[1] / (self.area_size[1] / self.area_grid[1]))
        if rx>=self.area_grid[0]:rx=self.area_grid[0]-1
        if ry>=self.area_grid[1]:rx=self.area_grid[1]-1
        area_n = self.area_grid[0]*ry+rx;obj_ = area_gameplay_data[area_n]
        if obj_ and issubclass(type(obj_), Turret):
            if not self.selecting:self.selecting=True;self.info__=Info_Slide(obj_);gameplay.gameplay_items.append(self.info__)
            elif self.selecting and issubclass(type(obj_), Turret) and obj_ != self.info__.target:gameplay.gameplay_items.remove(self.info__);self.info__=Info_Slide(obj_);gameplay.gameplay_items.append(self.info__)
            else:self.selecting=False;gameplay.gameplay_items.remove(self.info__)
        elif self.selecting and self.info__ and not on_top_button: self.selecting=False;gameplay.gameplay_items.remove(self.info__)
    def place__(self,mouse_pos,obj,area_gameplay_data,direction,gameplay_items,money):
        rx,ry=floor(mouse_pos[0]/(self.area_size[0]/self.area_grid[0])),floor(mouse_pos[1]/(self.area_size[1]/self.area_grid[1]))
        if rx>=self.area_grid[0]:rx=self.area_grid[0]-1
        if ry>=self.area_grid[1]:rx=self.area_grid[1]-1
        area_n=self.area_grid[0]*ry+rx
        if obj and not area_gameplay_data[area_n]:
            obj_=obj(self.rect.topleft,area_n,direction)
            if not issubclass(type(obj_), Turret) or money >= obj_.cost[0]:
                area_gameplay_data[area_n]=obj_; area_gameplay_data[int(len(area_gameplay_data)/2)+area_n]=direction;gameplay_items.append(obj_)
                if not issubclass(type(obj_), Turret):obj_.image=pygame.transform.scale(obj_.image,self.rect.size)
                elif issubclass(type(obj_), Turret):obj_.rect.center=self.rect.center;money-=obj_.cost[0];
            else: anim_need_money()
        self.placing=False
        return area_gameplay_data,gameplay_items,None,money
loading_progress=0.2
class Road:
    def __init__(self,pos,area,direction):direction%=2;self.sprites=[pygame.image.load(assets['road'+str(i)])for i in range(2)];self.sprite_num=direction;self.image=self.sprites[self.sprite_num];self.rect=self.image.get_rect(topleft=pos);self.area=area
class Road_turn:
    def __init__(self,pos,area,direction):direction%=4;self.sprites=[pygame.image.load(assets['road_turn'+str(i)])for i in range(4)];self.sprite_num=direction;self.image=self.sprites[self.sprite_num];self.rect=self.image.get_rect(topleft=pos);self.area=area
class EndPoint:
    def __init__(self,pos,area,direction):self.image=pygame.image.load(assets['endpoint']);self.rect=self.image.get_rect(topleft=pos);self.area=area
class StartPoint:
    def __init__(self,pos,area,direction):self.image=pygame.image.load(assets['startpoint']);self.rect=self.image.get_rect(topleft=pos);self.area=area
loading_progress=0.3
def move_condition(direction,c_p_movement):
    if direction==0:
        if c_p_movement==(1,0):c_p_movement=0,-1
        elif c_p_movement==(0,1):c_p_movement=-1,0
    elif direction==1:
        if c_p_movement==(-1,0):c_p_movement=0,-1
        elif c_p_movement==(0,1):c_p_movement=1,0
    elif direction==2:
        if c_p_movement==(0,-1):c_p_movement=1,0
        elif c_p_movement==(-1,0):c_p_movement=0,1
    elif direction==3:
        if c_p_movement==(0,-1):c_p_movement=-1,0
        elif c_p_movement==(1,0):c_p_movement=0,1
    return c_p_movement
small_font=pygame.font.Font('assets/ARLRDBD.TTF',12)
class Enemy:
    def __init__(self, start_pos, turn_points, endpoint):
        self.sprites = [pygame.image.load(assets['normal' + str(i)]) for i in range(4)];self.sprite_num=0;self.image = self.sprites[self.sprite_num];self.rect = self.image.get_rect(center=start_pos);self.hp = 100;self.speed = 1;self.dead=False;self.death_income=25;self.at_end=False
        self.enemy_dir = 1, 0;self.speed_ext_wait = 0;self.turn_points=turn_points;self.endpoint=endpoint;self.flip=False;self.goingToTurnpoint=0;self.last_turn_point=False
    def move(self):
        if self.speed_ext_wait == 0: self.rect.center = (self.speed * self.enemy_dir[0] + self.rect.centerx, self.speed * self.enemy_dir[1] + self.rect.centery)
        self.speed_ext_wait += 1;self.speed_ext_wait %= 2
        for point in self.turn_points:
            if point.rect.right>=self.rect.centerx>=point.rect.left and point.rect.bottom>=self.rect.centery>=point.rect.top:
                turn=False
                if isinstance(point, Road_turn):
                    if self.enemy_dir==(1, 0) and self.rect.centerx>=point.rect.centerx:turn=True
                    elif self.enemy_dir==(0, 1) and self.rect.centery>=point.rect.centery:turn=True
                    elif self.enemy_dir==(-1, 0) and self.rect.centerx<=point.rect.centerx:turn=True
                    elif self.enemy_dir==(0, -1) and self.rect.centery<=point.rect.centery:turn=True
                    if turn:
                        self.enemy_dir = move_condition(point.sprite_num, self.enemy_dir)
                        if not self.last_turn_point: self.goingToTurnpoint += 1; self.last_turn_point = True
                    else:self.last_turn_point = False
                elif isinstance(point, EndPoint) and self.rect.centerx>=point.rect.centerx:self.dead=True; self.at_end=True
        self.animate_enemy()
        if self.endpoint[0] <= self.rect.centerx:self.dead=True
        if self.enemy_dir==(-1,0):self.flip=True
        else:self.flip=False
        if self.hp<=0: self.dead=True
    def animate_enemy(self):
        self.sprite_num += 1;self.sprite_num %= 16*len(self.sprites);self.image=self.sprites[self.sprite_num//16]
        if self.flip:self.image=pygame.transform.flip(self.image,True,False)
class Jello(Enemy):
    def __init__(self, startpoint, turn_points, endpoint):super().__init__(startpoint, turn_points, endpoint);self.sprites=[pygame.image.load(assets['jello'+str(i)])for i in range(4)];self.image=self.sprites[self.sprite_num];self.rect=self.image.get_rect(center=startpoint);self.speed=2;self.hp=45;self.death_income=25;self.at_end=False
class Heavy(Enemy):
    def __init__(self, startpoint, turn_points, endpoint):super().__init__(startpoint, turn_points, endpoint);self.sprites=[pygame.image.load(assets['heavy'+str(i)])for i in range(7)];self.image=self.sprites[self.sprite_num];self.rect=self.image.get_rect(center=startpoint);self.speed=1;self.hp=220;self.death_income=65;self.at_end=False
loading_progress = 0.4
def touching_range(point_a, point_b, radius_a, radius_b): return math.hypot(point_a[0]-point_b[0], point_a[1]-point_b[1]) <= (radius_a + radius_b)
class Bullet:
    def __init__(self,pos,angle,speed,dmg,target):self.image=pygame.transform.rotozoom(pygame.image.load(assets['bullet_n']),angle,1);self.rect=self.image.get_rect(center=pos);self.angle=angle;self.speed=speed;self.dmg=dmg;self.target=target;self.fixed_target_rect=pygame.Rect(*list(target.rect))
    def move(self):
        self.rect.center = (self.rect.centerx - math.cos(-self.angle * math.pi / 180) * self.speed,self.rect.centery - math.sin(-self.angle * math.pi / 180) * self.speed)
        if debug_mode is True: pygame.draw.circle(screen, (255,0,0),self.fixed_target_rect.center,15,1); pygame.draw.circle(screen, (0,255,0),self.rect.center,8,1)
        if touching_range(self.rect, self.fixed_target_rect, 8, 15): gameplay.gameplay_items.remove(self);self.target.hp-=self.dmg
loading_progress=0.5
class Turret:
    def __init__(self, pos, area, direction):self.image=pygame.image.load(assets['turret_n']);self.rect=self.image.get_rect(center=pos);self.BULLETDAMAGE=20;self.RANGE=170;self.mode=0;self.area=area;self.org_img=self.image;self.org_rect=self.rect;self.shoot_now=False;self.shoot_thr=None;self.shoot_speed=1;self.cost=[100,50,120];self.level=1
    def shoot(self, enemies, turn_points):
        target=None;highest_distance=None;highest_turn_point=None;highest_health=None;random_inRange_list=[]
        def shoot_wait():self.shoot_now=True;time.sleep(self.shoot_speed);self.shoot_thr=None;self.shoot_now=True
        for enemy in enemies:
            if touching_range(enemy.rect.center, self.rect.center, 8, self.RANGE):
                if self.mode==0:
                    if highest_turn_point is None or highest_turn_point<=enemy.goingToTurnpoint:
                        if highest_turn_point is None or highest_turn_point<enemy.goingToTurnpoint: highest_distance=None
                        highest_turn_point=enemy.goingToTurnpoint;dst=int(math.sqrt((enemy.rect.centerx - enemy.turn_points[enemy.goingToTurnpoint].rect.centerx) ** 2 + (enemy.rect.centery - enemy.turn_points[enemy.goingToTurnpoint].rect.centery) ** 2))
                        if highest_distance is None or highest_distance>=dst: highest_distance=dst; target=enemy
                elif self.mode==1:
                    if highest_turn_point is None or highest_turn_point>=enemy.goingToTurnpoint:
                        if highest_turn_point is None or highest_turn_point>enemy.goingToTurnpoint: highest_distance=None
                        highest_turn_point=enemy.goingToTurnpoint
                        dst=int(math.sqrt((enemy.rect.centerx - enemy.turn_points[enemy.goingToTurnpoint].rect.centerx) ** 2 + (enemy.rect.centery - enemy.turn_points[enemy.goingToTurnpoint].rect.centery) ** 2))
                        if highest_distance is None or highest_distance<=dst: highest_distance=dst; target=enemy
                elif self.mode == 2:
                    dst = int(math.sqrt((enemy.rect.centerx - self.rect.centerx) ** 2 + (enemy.rect.centery - self.rect.centery) ** 2))
                    if not highest_distance or dst<highest_distance:target=enemy;highest_distance=dst
                elif self.mode == 3:
                    dst = int(math.sqrt((enemy.rect.centerx - self.rect.centerx) ** 2 + (enemy.rect.centery - self.rect.centery) ** 2))
                    if not highest_distance or dst>highest_distance:target=enemy;highest_distance=dst
                elif self.mode == 4:
                    if highest_health is None or highest_health < enemy.hp: highest_health = enemy.hp; target = enemy
                elif self.mode == 5:
                    if highest_health is None or highest_health > enemy.hp: highest_health = enemy.hp; target = enemy
                elif self.mode == 6: random_inRange_list.append(enemy)
        if self.mode==6 and len(random_inRange_list) != 0:
            target=random_inRange_list[random.randint(0,len(random_inRange_list)-1)]
        if target:
            angle = math.floor(math.atan2(self.rect.centery - target.rect.centery, self.rect.centerx - target.rect.centerx) * (180 / math.pi))
            if not self.shoot_thr:self.shoot_thr=threading.Thread(target=shoot_wait);self.shoot_thr.start(); gameplay.gameplay_items.append(Bullet(self.rect.center,-angle,12,self.BULLETDAMAGE,target)); self.image = pygame.transform.rotozoom(self.org_img, -angle, 1);self.rect = self.image.get_rect(center=self.org_rect.center)
            if debug_mode:pygame.draw.rect(screen,(0,0,155),target.rect,1)
        if debug_mode:pygame.draw.circle(screen, (0,255,0), self.rect.center, self.RANGE, 1);pygame.draw.rect(screen,(155,0,0),self.rect,1)
class AutoRifle(Turret):
    def __init__(self, pos, area, direction):self.image=pygame.image.load(assets['turret_a']);self.rect=self.image.get_rect(center=pos);self.BULLETDAMAGE=5;self.RANGE=150;self.mode=0;self.area=area;self.org_img=self.image;self.org_rect=self.rect;self.shoot_now=False;self.shoot_thr=None;self.shoot_speed=0.15;self.cost=[120,45,150];self.level=1
loading_progress = 0.9
class debug_fps:
    def __init__(self):self.font=pygame.font.Font('assets/ARLRDBD.TTF',11);self.image=self.font.render("fps: "+str(floor(clock.get_fps())), True, (0,0,0));self.rect=self.image.get_rect()
    def update(self):self.image=self.font.render("fps: "+str(floor(clock.get_fps())),True,(0,0,0))
# temporary loading screen wait
loading_progress = 1.0  # load_checkpoint
def basic_render_sprites(sprites):
    if not sprites:return
    if isinstance(sprites,list):
        for sprite in sprites:
            if sprite:screen.blit(sprite.image,sprite.rect)
    elif isinstance(sprites,dict):
        for sprite in sprites:
            if sprites[sprite]:screen.blit(sprites[sprite].image,sprites[sprite].rect)
def advance_render_sprites(sprites):
    basic_render_sprites(sprites)
    for sprite in sprites:
        if not hasattr(sprite,'ext_mode'):return
        for ex_img in sprite.f_suf:screen.blit(ex_img, getattr(sprite.rect, sprite.ext_anchor))
def advance_render_sprites_text_exclusive(sprites):
    basic_render_sprites(sprites)
    for sprite in sprites:
        if not hasattr(sprite,'ext_mode'):return
        for ex_img in sprite.f_suf:screen.blit(ex_img, (sprite.rect.left + getattr(sprite.image.get_rect(), sprite.ext_anchor)[0]-sprite.f_suf[0].get_rect().centerx, sprite.rect.top + getattr(sprite.image.get_rect(), sprite.ext_anchor)[1]-sprite.f_suf[0].get_rect().centery))
def text_displayer_function(text_displayers):text_displayers[0].text="Money: "+str(gameplay.player_data['money']); text_displayers[0].f_suf=[text_displayers[0].font.render(text_displayers[0].text, text_displayers[0].antialias, text_displayers[0].text_color)]; advance_render_sprites_text_exclusive(text_displayers)
def gameplay(level):
    grid_info=level['grid_info'];ONLY_EXECUTABLE_CLASSES=['Road','Road_turn','EndPoint','StartPoint'];turn_points=[];s_e_larea=[None,None]
    Base_frames={'bg':None,'gameplay_area':base_gui.BasicFrame((0,0),root_window.get_size(),(156,240,139))};c_slot=None;grid_area=Base_frames['gameplay_area'].rect.size
    c_dir=0;gameplay.gameplay_area_data=gameplay_area_data=[None for i in range(grid_info[0]*grid_info[1])]+[0 for i in range(grid_info[0]*grid_info[1])];Base_frames['slc']=gameplay.slc=slc=Slc(grid_area,grid_info,Base_frames['gameplay_area'])
    gameplay.gameplay_items=gameplay_items=[];gameplay.enemies=enemies=[];startpoint=None;endpoint=None;debug_items=[debug_fps()]
    gameplay.player_data=player_data={'money':200}; wave_counter = 1; wavedisfunc = lambda wave_num: ("Wave "+str(wave_num), "assets/ARLRDBD.TTF", 14, (screen.get_width()/2-50,screen.get_height()-115), (100,15), (0,0,0))
    gameplay.text_displayers=text_displayers=[base_gui.TextFrame("Money: "+str(player_data['money']), "assets/ARLRDBD.TTF", 14, (screen.get_width()/2-50,screen.get_height()-95), (100,15), (0,0,0), text_alignment="center"), base_gui.TextFrame(*wavedisfunc(wave_counter), text_alignment="center")]
    gameplay.buttons_for_gameplay=buttons_for_gameplay=[base_gui.TextButton(lambda: print("HALLO WORLD!"), "Skip wave", "assets/ARLRDBD.TTF", 15, (screen.get_width()/2-50,screen.get_height()-140), (100,20), (0,0,0), text_alignment="center", background=(255,128,0))];
    def change_slot(obj):nonlocal c_slot;c_slot = obj; return obj
    slots_data = [Turret, AutoRifle, None, None, None, None, None, None];slot_img=pygame.image.load(assets['slot_frame']).convert_alpha()
    slots_bt=[base_gui.AdvancedImageButton(change_slot,slot_img,(-220+i*60,-25),slot_img.get_size(),(0,0,0),anchor='midbottom',function_args=v,f_surfaces=[pygame.transform.scale(v((0,0),0,0).image,slot_img.get_size())for ii in range(1)if v])for(i,v)in enumerate(slots_data)]
    slots_info_display=[base_gui.TextFrame("$"+str(v((0,0),0,0).cost[0] if v and hasattr(v((0,0),0,0), "cost") else "NA"), "assets/ARLRDBD.TTF", 14, (-220+i*60,-10), (100,15), (0,0,0), text_alignment="center", anchor="midbottom")for(i,v)in enumerate(slots_data)]
    ###################
    level_data = level['level']; gameplay.direction_memory_adress=direction_memory_adress = int(len(level_data) / 2); block_size = (round(grid_area[0] / grid_info[0] + 1), round(grid_area[1] / grid_info[1] + 1))
    for index in range(direction_memory_adress):
        value = level_data[index]
        if value and value in ONLY_EXECUTABLE_CLASSES:
            x_ = index % grid_info[0];y_ = index // grid_info[0];obj__ = eval(value)((grid_area[0] / grid_info[0] * x_, grid_area[1] / grid_info[1] * y_), index,level_data[direction_memory_adress + index]);obj__.image = pygame.transform.scale(obj__.image, block_size);gameplay_area_data[index] = obj__;gameplay_area_data[direction_memory_adress + index] = level_data[direction_memory_adress + index]; gameplay_items.append(obj__)
            if isinstance(obj__,StartPoint):startpoint=obj__.rect.midleft;s_e_larea[0]=[x_, y_]
            elif isinstance(obj__,EndPoint):endpoint=obj__.rect.center;s_e_larea[1]=[x_, y_]
    move_pointer = (1, 0);render_at_end = False;current_place = s_e_larea[0]
    while not render_at_end:
        current_place = [current_place[0] + move_pointer[0], current_place[1] + move_pointer[1]]; area_n = grid_info[0] * current_place[1] + current_place[0];is_road_turn = False; loc__ = gameplay_area_data[area_n]
        if isinstance(loc__, Road_turn): is_road_turn = True
        elif isinstance(loc__, EndPoint): is_road_turn = True
        if is_road_turn:rt_dir = gameplay_area_data[int(len(gameplay_area_data) / 2) + area_n]; move_pointer = move_condition(rt_dir, move_pointer); turn_points.append(loc__)
        if area_n > len(gameplay_area_data) / 2: break
    del level_data, direction_memory_adress, block_size
    level_enemies = level['enemies']
    def spawn_enemies():
        nonlocal wave_counter
        for enem_in_wave in level_enemies:
            for enemies_ in enem_in_wave:
                time.sleep(level['spawn_interval']);en_=None
                if enemies_ == 0:en_=Enemy(startpoint, turn_points, endpoint)
                if enemies_ == 1:en_=Jello(startpoint, turn_points, endpoint)
                if enemies_ == 2:en_=Heavy(startpoint, turn_points, endpoint)
                gameplay_items.append(en_);enemies.append(en_)
            time.sleep(level["wave_duration"])
            wave_counter+=1; text_displayers[1] = base_gui.TextFrame(*wavedisfunc(wave_counter), text_alignment="center")
    spawn_thread = threading.Thread(target=spawn_enemies);spawn_thread.daemon=True;spawn_thread.start()
    while 1:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:pygame.quit();sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                on_top_button = False
                for bt in slots_bt:
                    val=bt.run_when_clicked(mouse_pos)
                    if not on_top_button:
                        on_top_button=bt.get_if_clicked(mouse_pos)
                        if val:slc.placing=True
                if slc.info__ and slc.selecting and not on_top_button:
                    player_data['money'], on_top_button = slc.info__.pressed(mouse_pos, player_data['money'])
                if not on_top_button:
                    if slc.placing:gameplay_area_data,gameplay_items,c_slot,player_data['money']=slc.place__(mouse_pos, c_slot, gameplay_area_data, c_dir, gameplay_items, player_data['money']);slc.run__(mouse_pos, c_slot, c_dir)
                    else:slc.select__(mouse_pos, gameplay_area_data, on_top_button)
            elif event.type == pygame.MOUSEMOTION: slc.run__(mouse_pos, c_slot, c_dir)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:c_dir += 1;c_dir %= 4;slc.run__(mouse_pos, c_slot, c_dir)
                elif event.key == pygame.K_p:
                    list_copy = [v for v in gameplay_area_data];print(list_copy)
                    for index, obj in enumerate(list_copy):
                        if obj and not isinstance(obj, int):list_copy[index] = type(obj).__name__
                    json_copy = json.dumps(list_copy);print(json_copy)
                elif event.key==pygame.K_F3:
                    if globals()['debug_mode']: globals()['debug_mode']=False
                    else: globals()['debug_mode']=True
                elif event.key==pygame.K_y:enemy_=Jello(startpoint, turn_points, endpoint); gameplay_items.append(enemy_); enemies.append(enemy_)
                elif event.key==pygame.K_t:enemy_=Enemy(startpoint, turn_points, endpoint); gameplay_items.append(enemy_); enemies.append(enemy_)
                elif event.key==pygame.K_u:enemy_=Heavy(startpoint, turn_points, endpoint); gameplay_items.append(enemy_); enemies.append(enemy_)
                elif event.key==pygame.K_m:player_data['money'] += 250
        root_window.fill((0, 0, 0));screen.fill((255,255,255))
        basic_render_sprites(Base_frames);advance_render_sprites(slots_bt);basic_render_sprites(gameplay_items)
        if slc.info__ and slc.selecting: suff = pygame.Surface(screen.get_size(), pygame.SRCALPHA); pygame.draw.circle(suff, (47, 245, 238, 30), slc.info__.target.rect.center, slc.info__.target.RANGE); screen.blit(suff, (0,0))
        elif slc.inner_img: suff = pygame.Surface(screen.get_size(), pygame.SRCALPHA); pygame.draw.circle(suff, (47, 245, 238, 30), slc.rect.center, slc.turret_range); screen.blit(suff, (0,0))
        for enemy in enemies:
            enemy.move()
            if enemy.dead:
                enemies.remove(enemy);gameplay_items.remove(enemy)
                if not enemy.at_end: player_data['money']+=enemy.death_income
        for item in gameplay_items:
            if issubclass(type(item),Turret):item.shoot(enemies, turn_points)
            elif isinstance(item, Bullet):item.move()
        advance_render_sprites_text_exclusive(slots_info_display)
        text_displayer_function(text_displayers)
        advance_render_sprites_text_exclusive(buttons_for_gameplay)
        #####
        for item in debug_items:item.update();screen.blit(item.image,item.rect)
        ###
        root_window.blit(screen, (0, 0));pygame.display.flip();pygame.display.update();clock.tick(60)

### temporary
with open("assets/data/levels.dat", 'r') as level_dat: level_data = json.loads(level_dat.read());gameplay(level_data[0])


# # # Progress: # # #
#
# SLC: Placing, Selecting, Deleting Turrets
#       - info__
#       - Slots buttons (added during the third day of coding this project)
#       - Maths and science computation
#
# Enemy: Moving, Hp, losses  (Types: 3 [Normal, Jello, Heavy that looks like a rusted frog])
#       - move_condition() function
#       - types of enemies
#       - assignments and self attributes for turrets and other game mechanics
#
# Turrets: Aiming, Bullet tracing, Targeting   (Types: 2 [Turret, AutoRifle])
#       - Aims at selected enemy
#       - Bullet hitbox with enemy at fixed position (invisible unless using debug mode [F3] [added [11/3/22]])
#       - Range, Damage, Attack speed using threading
#       - Buy, sell, upgrade (added last 3 months [@11/4/22])
#       - Targets: First, Last, Near, Far, Strongest, Weakest, Random (fixed [11/3/22])
#
# Mechanics:
#       - Add lives system (NOT YET)
#       - Add wave system (NOT YET)
#       - gameplay() is the main gameplay function :))
#
# Map: Rendering, Spawning, Identifying turn points, Reading Data from "levels.dat"
#       - Identifying turn points used for enemies, functions same as move in enemies
#       - Reads data from levels.dat in json
#       - Spawns at spawn point road, for time being, for bug, 2 spawn point road will result using the latest spawn road in the data
#       - Enemy spawning at separate thread
#
# Assets: Reading and using Assets
#       - Reads from config and transforms to python data
#       - Used for classes like the map and the enemies and turrets
#
# Loading Screen: Loading screen and Loading bar
#       - Added Loading bar (11/3/22)
#       - Loading screen for loading classes while not hang up
#
# Animations: animation functions and others
#       - Used by text:Not enough money and Enemies
#       - functions and cycles used (revised at 11/4/22)
#
# Events:
#       - Captures Mouse and keyboard for game related functions
#       - Too lazy to put it to a function because of the struggles
#
# # # Overall Progress: 35% to completion # # #

# TODO: add lives and wave system, add main menu, add music, add more enemies and turrets, add inventory, add more assets, add rocks and trees in map,
#  add maps, add logic, change upgrade system mechanic (its just a small repeating code), cleanup and revise code in slc and gameplay,

