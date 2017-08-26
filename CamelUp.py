import numpy

#camel=(pos,D2,D3)
#board=((camel1, ..., camel5),((spot,+-1),...)), back camel first, 2nd tuple is oases/mirages

numpy.set_printoptions(precision=4,suppress=True)

def moveCamel(c,dest):
    spot,D2,D3=c
    return (dest,D2,D3)

def setDie(c,n,val):
    assert 2<=n<=3
    spot,D2,D3=c
    if n==2:
        assert D2!=val
        D2=val
    elif n==3:
        assert D3!=val
        D3=val
    return (spot,D2,D3)

calls=0
#finish=-1 means leg probs
def CalcProbs(board, finish, isLeg, probs={}):
    global calls
    #probs is a dict mapping boards to win probabilities, in the same order as the camels (loser first). Can be filled in if already partly known.
    if board in probs:
        return probs[board]
    calls+=1
    dice=[]
    prevSpot=10**6
    camels,boosts=board
    for indRaw,(spot,D2,D3) in enumerate(reversed(camels)):
        ind=len(camels)-1-indRaw
        assert prevSpot>=spot
        if prevSpot>spot:
            prevSpot=spot
            topInd=ind+1
        if D3:
            dice.append((3,ind,topInd))
        if D2:
            dice.append((2,ind,topInd))
    ret=numpy.array([[0.0]*len(camels)]*len(camels))
    if camels[-1][0]>=finish or (isLeg and not dice):
        for i in range(len(camels)):
            ret[i,i]=1
        return ret

    if not dice:
        camels=tuple(setDie(c,3,True) for c in camels)
        return CalcProbs((camels,()), finish, isLeg, probs)
    
    bd={}
    for spot,delta in boosts:
        bd[spot]=delta
    
    for (n,ind,topInd) in dice:
        for roll in range(1,n+1):
            slip=False
            target=camels[ind][0]+roll
            if target in bd:
                delta=bd[target]
                target+=delta
                if delta==-1:
                    slip=True
            camelArray=list(camels)
            permute=list(range(len(camels)))
            stack=camelArray[ind:topInd]
            stack[0]=setDie(stack[0],n,False)
            for i in range(len(stack)):
                stack[i]=moveCamel(stack[i],target)
            camelArray[ind:topInd]=[]
            subPermute=permute[ind:topInd]
            permute[ind:topInd]=[]
            destInd=0
            for i,(s,d3,d2) in enumerate(camelArray):
                if s<target or (s==target and not slip):
                    destInd=i+1
            camelArray[destInd:destInd]=stack
            permute[destInd:destInd]=subPermute
            newCamels=tuple(camelArray)
            newBoard=(newCamels,boosts)
            subProbs=CalcProbs(newBoard,finish,isLeg,probs)/(len(dice)*n)
            invPerm=numpy.argsort(permute)
            permutedProbs=subProbs[:,invPerm]
            ret+=permutedProbs
    probs[board]=ret
    #print(camels,ret)
    return ret

boosts=((10,-1)),
boosts=()
camels=((1,False,True),(1,False,True),(1,False,True),(1,False,True),(1,False,True))
board=(camels,boosts)
print(CalcProbs(board, 17, False))
print(calls)
            
            

            
