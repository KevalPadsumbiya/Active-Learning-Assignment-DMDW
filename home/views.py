from django.shortcuts import render
import math

def index(request):

    if(request.method == "GET" and request.GET.get('Algorithm')=='Apriori'):        
        return render(request,"home/index.html",{'algo':'Apriori'})

    if request.method == "POST":

        if request.POST.get('Apriori'):
            data = request.POST['textarea_data1']
            if len(data) == 0 :
                return render(request,"home/index.html",{'input':"Please enter data",'algo':'Apriori'})
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
                    elif(len(s)):
                        # print(s)
                        l.append([s])
                    # elif(len(s.split(' '))>1): 
                    #     l.append(s.split(' '))
                    s = ""
            s = s.strip()
            if(len(s.split(';'))>1):
                l.append(s.split(';'))
            elif(len(s.split(','))>1): 
                l.append(s.split(','))
            elif(len(s)):
                # print(s)
                l.append([s])
            # elif(len(s.split(' '))>1): 
            #     l.append(s.split(' '))
            print(len(l))
        
            vis=dict()

            for i in range(len(l)):
                m=dict()
                for item in l[i]:
                    if item not in m:
                        m[item] = 0
                    m[item] += 1
                if i not in vis:
                    vis[i]=dict()
                vis[i]=m
            # print(vis)

            if(request.POST['sup_count'] == ""):
                return render(request,"home/index.html",{'algo':'Apriori','input':data,'min_sup':'Please Enter valid support count'})
           

            min_sup = int(request.POST['sup_count'])
            support=list()
            last_itemset=list()
           
            mp=dict()
            ls = list()
            for row in l:
                for item in row:
                    if item not in mp:
                        mp[item]=0
                    mp[item]+=1
            
            temp = []
            print("L1 (itemset : support) : ")
            for it in mp:
                if mp[it]>=min_sup:
                    support.append([it,mp[it]])
                    last_itemset.append([it])
                    # print(it ," : ",mp[it])
                    temp.append([it,mp[it]])
            #print(last_itemset)
            ls.append(["L1",temp])
            # print(ls)
            cnt=2
            while len(last_itemset) > 0:
                temp=list()
                print(len(last_itemset))
                sorted_candidates = list()
                for i in range(0,len(last_itemset)-1):
                    for j in range(i+1,len(last_itemset)):
                        s=list()
                        if cnt==2:
                            s.append(last_itemset[i][0])
                            s.append(last_itemset[j][0])
                        else:
                            for el in last_itemset[i]:
                                s.append(el)
                            for el in last_itemset[j]:
                                if el not in s:
                                    s.append(el)
                        #print(s)
                            
                        if len(s)==len(last_itemset[i])+1:
                            v=list()
                            for el in s:
                                v.append(el)
                            fre=0
                            #print(v)
                            for k in range(len(l)):
                                f=1
                                for item in v:
                                    if item not in vis[k]:
                                        f=0
                                        break
                                if f==1:
                                    fre+=1
                            v.sort()
                            
                            if fre>=min_sup and v not in support:
                                temp.append(v)
                                if([v,fre] not in sorted_candidates):
                                    sorted_candidates.append([v,fre])
                                support.append([v,fre])
                            #print(temp)
                last_itemset=temp
                #print(last_itemset)
                if len(last_itemset):
                    # print()
                    print("L",cnt,"(itemset : support) :" )
                    #print(support)
                    ans=list()
                    # print(sorted_candidates)
                    if len(sorted_candidates):
                        l1 = [[', '.join(sorted_candidates[i][0]),sorted_candidates[i][1]] for i in range(len(sorted_candidates))]
                        # for i in range(len(sorted_candidates)):
                        #     print(','.join(sorted_candidates[0][0]))
                    ls.append(["L{}".format(cnt),l1])
                    cnt += 1
                    for v in last_itemset:
                        if v not in ans:
                            for el in v:
                                print(el,end=" ")
                            ans.append(v)
                            print()
            table = []
            for i in range(len(l)):
                table.append([i+1,','.join(l[i])])
            data1 = table
            data2 = []
            # print(table)
            if(len(l)>25):
                data1 = table[:25]
                data2 = table[25:]
            # print(ls)
            return render(request,"home/index.html",{'algo':'Apriori','input':data,'min_sup':min_sup,'table':table,'data1':data1,'data2':data2,'status':'ok','rem_rows':str(max(0,len(l)-25)),'result':ls})
        
        elif request.POST.get('ID3'):
            # print('11111')
            data = request.POST['textarea_data']
            # print(data)
            if len(data) == 0 :
                return render(request,"home/index.html",{'input':"Please enter data",'algo':'ID3'})
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
                data1 = l[1:]
                data2 = []
                if(len(l)>50):
                    data1 = l[1:25]
                    data2 = l[25:]
                # print(data1)
                return render(request,"home/index.html",{'result' : result,'input':data,'status':"ok",'algo':'ID3','data1':data1,'data2':data2,'classes':l[0],'rem_rows':str(max(0,len(l)-25))})
            except:
                return render(request,"home/index.html",{'input':"Please enter valid data",'algo':'ID3'})
    return render(request,"home/index.html",{'algo':'ID3'})
