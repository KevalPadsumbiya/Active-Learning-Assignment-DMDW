from django.shortcuts import render
import math

def index(request):
    if request.method == "POST":

        data = request.POST['textarea_data']
        
        if len(data) ==0 :
            return render(request,"home/index.html",{'input':"Please enter data"})
        try :

            l = []
            s = ""
            vars = []

            for ch in data:
                if ch != "\n":
                    s += ch
                else:
                    s = s.strip()
                    if(len(s.split(';'))>1):
                        l.append(s.split(';'))
                    elif(len(s.split(','))>1): 
                        l.append(s.split(','))
                    elif(len(s.split(' '))>1): 
                        l.append(s.split(' '))
                    s = ""
            s = s.strip()
            if(len(s.split(';'))>1):
                l.append(s.split(';'))
            elif(len(s.split(','))>1): 
                l.append(s.split(','))
            elif(len(s.split(' '))>1): 
                l.append(s.split(' '))
            # print(l,len(l))

            # entropy of class attribute
            #   -P         |   P   |     -P         |   P   |
            # ------- log2 |-------| + ------- log2 |-------|
            #  P + N       | P + N |    P + N       | P + N |
            
            fre = dict()
            for i in range(1,len(l)):
                # print(l[i])
                if l[i][-1] not in fre:
                    fre[l[i][-1]] = 1
                else:
                    fre[l[i][-1]] += 1

            class_attr = [(k, v) for k, v in fre.items()]
            for tuple in class_attr:
                vars.append(tuple[0])

            main_class_ent = 0  
            main_denom = class_attr[0][1]
            if len(class_attr) == 2 : 
                main_denom += class_attr[1][1]
            for tuple in class_attr:
                main_class_ent = main_class_ent + (-tuple[1]/main_denom)*math.log2(tuple[1]/main_denom)
            # print(main_class_ent)

            gain = dict()
            result = []

            for i in range(len(l[0])-1):
                fre = dict()
                temp = []
                yes = []
                no = []
                for j in range(1,len(l)):
                    if l[j][i] not in fre:
                        fre[l[j][i]]  = dict()
                        if l[j][-1] not in fre[l[j][i]]:
                            fre[l[j][i]][l[j][-1]] = 1
                        else:
                            fre[l[j][i]][l[j][-1]] += 1 
                    else:
                        if l[j][-1] not in fre[l[j][i]]:
                            fre[l[j][i]][l[j][-1]] = 1
                        else:
                            fre[l[j][i]][l[j][-1]] += 1
                
                yes.append(vars[0])
                no.append(vars[1])

                for key,value in fre.items():
                    temp.append(key)
                    if vars[0] in value.keys() :
                        yes.append(value[vars[0]])
                    else:
                        yes.append(0)
                    if vars[1] in value.keys() :
                        no.append(value[vars[1]])            
                    else:
                        no.append(0)

                info_gain = dict()
                ent_of_attr = 0

                for (key,value)in fre.items():
                    class_attr = [(k, v) for k, v in value.items()]
                    class_ent = 0
                    denom = class_attr[0][1]  
                    if len(class_attr) == 2:
                        denom += class_attr[1][1]
                    for tuple in class_attr:
                        class_ent = class_ent + (-tuple[1]/denom)*math.log2(tuple[1]/denom)
                    info_gain[key] = class_ent
                    
                    # entropy of attribute  E(pi+ni)/(main_denom)*(info_gain[i]) , (pi+ni) = denom
                    ent_of_attr = ent_of_attr + (denom/main_denom)*class_ent
                
                # gain = entropy_of_class - entro_of_attribute

                gain[l[0][i]] = main_class_ent - ent_of_attr
                result.append([l[0][-1],l[0][i],temp,yes,no,ent_of_attr,gain[l[0][i]]])        
                # print(fre)
                # print(info_gain)
            # print(result)
            # print(gain)
            # print(vars)
            return render(request,"home/index.html",{'result' : result,'input':data,'status':"ok"})

        except:
            return render(request,"home/index.html",{'input':"Please enter valid data"})

    return render(request,"home/index.html")
