import random

if __name__ == "__main__":
    a = (0, 15, 100) # point, distance, health
    b = (1, 3, 90)
    c = (0, 2, 210)
    d = (1, 17, 150)
    lst = [a,b,c,d]
    lst2 = [(i * i, i / (i+1), i + i * i - i) for i in range(20)]

    highpt = None; highdist = None; highhealth = None ;enemyTarget = None

    for i in range(200):
        random_guy = random.randint(0, len(lst2)-1);
        print(random_guy, lst2[random_guy])


# First or Last (interchange greater and lesser sign if last)
#for enemy in lst:
    #if highpt is None or highpt<=enemy[0]:
        #if highpt is None or highpt<enemy[0]: highdist = None
        #highpt=enemy[0]
        #if highdist is None or highdist>=enemy[1]:
            #highdist = enemy[1]
            #enemyTarget = enemy

# Strongest and weakest (interchange greater and lesser sign if weakest)
#for enemy in lst:
    #if highhealth is None or highhealth < enemy[2]:
        #highhealth = enemy[2]
        #enemyTarget = enemy