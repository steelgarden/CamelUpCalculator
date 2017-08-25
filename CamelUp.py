import numpy

#camel=(pos,D2,D3)
#board=((camel1, ..., camel5),((spot,+-1),...)), back camel first, 2nd tuple is oases/mirages

def moveCamel(c,dest):
    spot,D2,D3=c
    return (dest,D2,D3)

def useDie(c,n):
    assert 2<=n<=3
    spot,D2,D3=c
    if n==2:
        assert D2==True
        D2=False
    elif n==3:
        assert D3==True
        D3=False
    return (spot,D2,D3)

def CalcLegProbs(board, probs={}):
    #probs is a dict mapping boards to win probabilities, in the same order as the camels (loser first). Can be filled in if already partly known.
    if board in probs:
        return probs[board]
    dice=[]
    prevSpot=10**6
    camels,boosts=board
    for indRaw,(spot,D2,D3) in enumerate(reversed(camels)):
        ind=len(camels)-1-indRaw
        if prevSpot>spot:
            prevSpot=spot
            topInd=ind+1
        if D3:
            dice.append((3,ind,topInd))
        if D2:
            dice.append((2,ind,topInd))
    ret=numpy.array([0.0]*len(camels))
    
    if not dice:
        ret[-1]+=1
        return ret

    bd={}
    for spot,delta in boosts:
        bd[spot]=delta
    
    for (n,ind,topInd) in dice:
        for roll in range(1,n+1):
            slip=False
            target=camels[ind][0]+roll
            if target in bd:
                target+=bd[target]
                if bd[target]==-1:
                    slip=True
            camelArray=list(camels)
            permute=list(range(len(camels)))
            stack=camelArray[ind:topInd]
            stack[0]=useDie(stack[0],n)
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
            subProbs=CalcLegProbs(newBoard,probs)/(len(dice)*n)
            permutedProbs=numpy.array([0.0]*len(subProbs))
            for i in range(len(permutedProbs)):
                permutedProbs[permute[i]]=subProbs[i]
            ret+=permutedProbs
    probs[board]=ret
    return ret

boosts=()
camels=((1,False,True),(1,False,True),(1,False,True),(1,False,True),(1,False,True))
board=(camels,boosts)
print(CalcLegProbs(board))

            
            

            
