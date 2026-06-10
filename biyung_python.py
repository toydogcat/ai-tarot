    def biyung(self):
        sike = self.all_sike()
        relation = self.find_sike_relations()
        filter_list = self.find_sike_relations()[7]
        filter_list_four_ke = self.find_sike_relations()[7][2]
        filter_list_yy = self.find_sike_relations()[7][5]
        dayganzhi_yy = self.find_sike_relations()[8]
        hourganzhi_yy = self.gangzhi_yinyang(self.hourgangzhi[1])
        hourganzhi_yy0 = self.gangzhi_yinyang(self.hourgangzhi[0])

        if filter_list[0] == "試賊尅":
            findtrue =  "不適用，或試他法"
            return findtrue
        elif filter_list[0] == "試涉害":
            findtrue =  "不適用，或試他法"
            return findtrue
        elif filter_list[0] == "試賊尅涉害以外方法":
            findtrue =  "不適用，或試他法"
            return findtrue
        elif relation[0].count("下賊上") == 4:
            if self.Ganzhiwuxing(self.daygangzhi[1]) == self.Ganzhiwuxing(self.hourgangzhi[1]):
                findtrue = ["涉害", "絕嗣",  self.find_three_pass(self.all_sike()[0][0])]
                return findtrue
            else:
                findtrue =  "不適用，或試他法"
                return findtrue
        elif relation[0].count("下賊上") == 2 and relation[9] == '天地盤返吟':
            if dayganzhi_yy == "陽":
               if self.Ganzhiwuxing(self.daygangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[1]) or self.Ganzhiwuxing(self.daygangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[1]):
                   findtrue = ["返吟", "無依", [self.all_sike()[1][1], self.all_sike()[0][1],  self.all_sike()[1][1]]]
               if self.Ganzhiwuxing(self.daygangzhi[1]) == self.Ganzhiwuxing(self.hourgangzhi[1]):
                   if hourganzhi_yy =="陰":
                       findtrue = ["返吟", "元胎", [self.all_sike()[0][1], self.all_sike()[0][0],  self.all_sike()[0][1]]]
                   else:
                       findtrue = ["返吟", "元胎", [self.all_sike()[2][1], self.all_sike()[2][0],  self.all_sike()[2][1]]]
               if self.Ganzhiwuxing(self.daygangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[0]):
                   findtrue = ["返吟", "無依", [self.all_sike()[2][0], self.all_sike()[2][1],  self.all_sike()[2][0]]]
               else:
                   if hourganzhi_yy == "陰":
                       if self.Ganzhiwuxing(self.daygangzhi[1]) == self.Ganzhiwuxing(self.hourgangzhi[0]) and self.Ganzhiwuxing(self.daygangzhi[0]) != self.Ganzhiwuxing(self.hourgangzhi[1]):
                           findtrue = ["返吟", "元胎", [self.all_sike()[3][0],  self.all_sike()[2][0], self.all_sike()[3][0]]]
                       if self.Ganzhiwuxing(self.daygangzhi[1]) == self.Ganzhiwuxing(self.hourgangzhi[0]) and self.Ganzhiwuxing(self.daygangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[1]):
                           findtrue = ["返吟", "無依", [self.all_sike()[1][0],  self.all_sike()[1][1], self.all_sike()[1][0]]]
                       if self.Ganzhiwuxing(self.daygangzhi[1]) != self.Ganzhiwuxing(self.hourgangzhi[1]): 
                           if hourganzhi_yy0 == hourganzhi_yy:
                               findtrue = ["返吟", "元胎贅婿", [self.all_sike()[1][1], self.all_sike()[1][0],  self.all_sike()[1][1]]]
                           else:
                               findtrue = ["返吟", "元胎", [self.all_sike()[1][0],  self.all_sike()[1][1], self.all_sike()[1][0]]]
                       if self.Ganzhiwuxing(self.daygangzhi[1]) != self.Ganzhiwuxing(self.hourgangzhi[1]) and self.Ganzhiwuxing(self.daygangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[1]): 
                           findtrue = ["返吟", "元胎", [self.all_sike()[1][1], self.all_sike()[1][0], self.all_sike()[1][1]]]
                   else:
                       if len([char for char, count in Counter([self.Ganzhiwuxing(char) for item in sike for char in item]).items() if count == 2]) > 2:
                           if sike[0][0] ==self.daygangzhi[1]:
                               findtrue = ["返吟", "元胎勵德", [self.all_sike()[0][0],  self.all_sike()[1][0], self.all_sike()[0][0]]]
                           else:
                               findtrue = ["返吟", "元胎", [self.all_sike()[2][1],  self.all_sike()[2][0], self.all_sike()[2][1]]]
                       else:
                           if self.Ganzhiwuxing(self.hourgangzhi[1]) == self.Ganzhiwuxing(self.hourgangzhi[0]) and self.Ganzhiwuxing(self.hourgangzhi[1]) == self.Ganzhiwuxing(self.hourgangzhi[0]):
                               findtrue = ["返吟", "三交", [self.all_sike()[1][1],self.all_sike()[0][1],  self.all_sike()[1][1]]]
                           else:
                               findtrue = ["返吟", "無依", [self.all_sike()[0][1],self.all_sike()[1][1],  self.all_sike()[0][1]]]
            if dayganzhi_yy == "陰":
                if self.Ganzhiwuxing(self.daygangzhi[1]) == self.Ganzhiwuxing(self.hourgangzhi[1]):
                    findtrue = ["返吟", "元胎", [self.all_sike()[0][1],  self.all_sike()[1][1], self.all_sike()[0][1]]]
                else:
                    if hourganzhi_yy == "陰":
                        findtrue = ["返吟", "龍戰", [self.all_sike()[0][1], self.all_sike()[1][1],  self.all_sike()[0][1] ]]
                    else:
                        findtrue = ["返吟", "無依", [self.all_sike()[1][1],  self.all_sike()[0][1], self.all_sike()[1][1] ]]
            return findtrue
        elif relation[0].count("下賊上") == 3 and relation[9] == '天地盤返吟':
            if dayganzhi_yy == "陽":
                if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[1]) and self.Ganzhiwuxing(self.hourgangzhi[1]) != self.Ganzhiwuxing(self.daygangzhi[1]):
                    findtrue = ["返吟", "元胎", [ self.all_sike()[1][1], self.all_sike()[0][1] ,  self.all_sike()[1][1]]]
                if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[1]) and self.Ganzhiwuxing(self.hourgangzhi[1]) == self.Ganzhiwuxing(self.daygangzhi[1]):
                    findtrue = ["返吟", "高蓋", [ self.all_sike()[0][1], self.all_sike()[1][1] ,  self.all_sike()[0][1]]] 
                if self.Ganzhiwuxing(self.daygangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[1]):
                    findtrue = ["返吟", "三交", [self.all_sike()[1][1], self.all_sike()[0][1],self.all_sike()[1][1],  ]]
                else:
                    findtrue = ["返吟", "返吟", [ self.all_sike()[0][1], self.all_sike()[1][1] ,  self.all_sike()[0][1]]]
            else:
                findtrue = ["返吟", "返吟", [self.all_sike()[1][1],  self.all_sike()[0][1],self.all_sike()[1][1] ]]
            return findtrue    
        
        elif relation[0].count("下賊上") >= 2 and relation[9] == '天地盤沒有返吟':
            if filter_list_yy[0] == dayganzhi_yy:
                findtrue = ["比用", "比用", self.find_three_pass(self.all_sike()[1][0])]
            if self.daygangzhi == self.hourgangzhi:
                findtrue = ["比用", "知一斫輪", self.find_three_pass(self.all_sike()[2][0])]
            elif filter_list_yy[1] == dayganzhi_yy:
                if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[1]) and  self.Ganzhiwuxing(self.daygangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[1]) :
                    findtrue = ["比用", "知一斫輪四絕鑄印", self.find_three_pass(self.all_sike()[2][0])]
                else:    
                    findtrue = ["比用", "比用", self.find_three_pass(self.all_sike()[2][1])]
            else:
                try:
                    if relation[0].count("上尅下") == 0:
                        f = [self.Ganzhiwuxing(i[0]) for i in sike].index(self.Ganzhiwuxing(self.daygangzhi[0]))
                        if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[1]) and hourganzhi_yy == "陰":
                            findtrue = ["涉害", "極陰", self.find_three_pass(self.all_sike()[0][1])]
                        if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[1]) and hourganzhi_yy == "陽":
                            findtrue = ["涉害", "從革", self.find_three_pass(self.all_sike()[2][0])]
                        else:
                            findtrue = ["比用", "比用", self.find_three_pass(sike[f][0])]   
                    if relation[0].count("上尅下") == 1:
                        if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[0]):
                            findtrue = ["比用", "知一", self.find_three_pass(self.all_sike()[0][0])]    
                        if self.Ganzhiwuxing(self.hourgangzhi[1]) == self.Ganzhiwuxing(self.daygangzhi[1]):
                            findtrue = ["比用", "知一", self.find_three_pass(self.all_sike()[2][0])]    
                        else:
                            try:
                                if [char for char, count in Counter([self.Ganzhiwuxing(char) for item in sike for char in item]).items() if count > 3][0] == self.Ganzhiwuxing(self.hourgangzhi[1]):
                                    findtrue = ["比用", "知一", self.find_three_pass(self.all_sike()[0][0])]
                                else:
                                    f = [self.Ganzhiwuxing(i[0]) for i in sike].index(self.Ganzhiwuxing(self.hourgangzhi[1]))
                                    findtrue = ["涉害", "涉害", self.find_three_pass(sike[f][0])]   
                            except IndexError:
                                if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[1]):
                                    if dayganzhi_yy == "陰":
                                        findtrue = ["比用", "知一鑄印", self.find_three_pass(self.all_sike()[2][0])]
                                    else:
                                        findtrue = ["涉害", "度厄", self.find_three_pass(self.all_sike()[0][0])]
                                if self.Ganzhiwuxing(self.daygangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[1]):
                                    findtrue = ["比用", "知一鑄印", self.find_three_pass(self.all_sike()[2][0])]
                                if self.Ganzhiwuxing(self.daygangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[0]):
                                    findtrue = ["比用", "知一斫輪羅網", self.find_three_pass(self.all_sike()[2][0])]
                                if self.Ganzhiwuxing(self.daygangzhi[1]) == self.Ganzhiwuxing(self.hourgangzhi[0]):
                                    findtrue = ["涉害", "間傳", self.find_three_pass(self.all_sike()[1][0])]
                                else:
                                    findtrue = ["比用", "知一", self.find_three_pass(self.all_sike()[0][0])]
                                
                except ValueError:
                    try:
                        fa = self.find_duplicates(sike)[0]
                        if relation[0][self.all_sike().index(fa)] == "下賊上":
                            findtrue = ["賊克", "重審", self.find_three_pass(fa[0])]
                        if relation[0][self.all_sike().index(fa)] == "上尅下":
                            findtrue = ["賊克", "元首", self.find_three_pass(fa[0])]
                        if relation[0][self.all_sike().index(fa)] != "上尅下" and  relation[0][self.all_sike().index(fa)] != "下賊上":
                            findtrue = ["涉害", "涉害", self.find_three_pass(fa[1])] 
                    except IndexError:
                        if dayganzhi_yy == "陰":
                            if hourganzhi_yy == "陰":
                                if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[1]):
                                    findtrue = ["比用", "知一", self.find_three_pass(self.all_sike()[2][0])]
                                else:
                                    findtrue = ["比用", "知一", self.find_three_pass(self.all_sike()[3][0])]
                            else:
                                findtrue = ["比用", "知一", self.find_three_pass(self.all_sike()[0][0])]
                        if dayganzhi_yy == "陽":
                            if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[0]) and self.Ganzhiwuxing(self.hourgangzhi[1]) == self.Ganzhiwuxing(self.daygangzhi[1]):
                                findtrue = ["涉害", "涉害", self.find_three_pass(self.all_sike()[3][0])]
                            if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[0]):
                                findtrue = ["涉害", "涉害", self.find_three_pass(self.all_sike()[0][0])]
                            if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[1]):
                                findtrue = ["比用", "退茹", self.find_three_pass(self.all_sike()[2][0])]
                            else:
                                findtrue = ["比用", "知一", self.find_three_pass(self.all_sike()[1][1])]
                if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[0]):
                    if relation[0].count("上尅下") == 2 and relation[0].count("下賊上") == 2:
                        findtrue = ["比用", "知一三奇", self.find_three_pass(self.all_sike()[2][0])]
                    if relation[0].count("上尅下") == 0 and relation[0].count("下賊上") == 3:
                        if dayganzhi_yy == "陽":
                            findtrue = ["比用", "知一鑄印", self.find_three_pass(self.all_sike()[2][0])]
                        else:
                            findtrue = ["涉害", "龍戰", self.find_three_pass(self.all_sike()[1][0])]
                    if relation[0].count("上尅下") == 0 and relation[0].count("下賊上") == 2:
                        findtrue = ["涉害", "見機四絕", self.find_three_pass(self.all_sike()[2][0])]
                    if relation[0].count("上尅下") == 1 and relation[0].count("下賊上") == 2:
                        findtrue = ["比用", "退茹", self.find_three_pass(self.all_sike()[0][0])]
                    else:
                        if self.Ganzhiwuxing(self.daygangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[0]) and self.Ganzhiwuxing(self.hourgangzhi[0]) != self.Ganzhiwuxing(self.hourgangzhi[1]):
                            try:
                                if len([char for char, count in Counter([self.Ganzhiwuxing(char) for item in sike for char in item]).items() if count > 1]) > 2:
                                    findtrue = ["比用", "四絕鑄印", self.find_three_pass(self.all_sike()[0][0])]
                                else:
                                    findtrue = ["涉害", "間傳", self.find_three_pass(self.all_sike()[1][0])]
                            except IndexError:
                                findtrue = ["涉害", "間傳", self.find_three_pass(self.all_sike()[1][0])]
                        if self.Ganzhiwuxing(self.daygangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[0]) and self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[1]):
                            findtrue = ["比用", "知一度厄", self.find_three_pass(self.all_sike()[0][0])]
                        if self.daygangzhi[0] ==self.hourgangzhi[0]:
                            findtrue = ["涉害", "從革", self.find_three_pass(self.all_sike()[2][0])]
                        if self.Ganzhiwuxing(self.daygangzhi[0]) != self.Ganzhiwuxing(self.hourgangzhi[0]) and self.Ganzhiwuxing(self.hourgangzhi[0]) != self.Ganzhiwuxing(self.hourgangzhi[1]):
                            findtrue = ["涉害", "涉害", self.find_three_pass(self.all_sike()[0][0])]
                else:
                    try:
                        fa = self.find_duplicates(sike)[0]
                        if relation[0][self.all_sike().index(fa)] != "上尅下" and  relation[0][self.all_sike().index(fa)] != "下賊上" :
                            findtrue = ["涉害", "曲直", self.find_three_pass(self.all_sike()[0][0])] 
                        if self.Ganzhiwuxing(self.hourgangzhi[1]) == self.Ganzhiwuxing(self.daygangzhi[0]) and self.Ganzhiwuxing(self.hourgangzhi[1]) == self.Ganzhiwuxing(self.hourgangzhi[0]):
                            findtrue = ["比用", "知一進茹", self.find_three_pass(self.all_sike()[2][0])] 
                        if self.Ganzhiwuxing(self.hourgangzhi[1]) == self.Ganzhiwuxing(self.daygangzhi[0]) and self.Ganzhiwuxing(self.hourgangzhi[1]) != self.Ganzhiwuxing(self.hourgangzhi[0]):
                            findtrue = ["涉害", "間傳斬關贄婿狡童", self.find_three_pass(self.all_sike()[3][0])] 
                        else:
                            if dayganzhi_yy == "陰":
                                findtrue = ["比用", "知一不備亂首驀越", self.find_three_pass(self.all_sike()[0][0])]
                            else:
                                findtrue = ["比用", "知一1", self.find_three_pass(self.all_sike()[2][0])]
                    except IndexError:
                        if self.Ganzhiwuxing(self.hourgangzhi[1]) == self.Ganzhiwuxing(self.daygangzhi[0]):
                            findtrue = ["比用", "知一進茹", self.find_three_pass(self.all_sike()[0][0])]

                        if relation[0].count("上尅下") == 2 and relation[0].count("下賊上") == 2:
                            if self.Ganzhiwuxing(self.hourgangzhi[1]) == self.Ganzhiwuxing(self.daygangzhi[0]):
                                findtrue = ["比用", "知一", self.find_three_pass(self.all_sike()[2][0])]
                            else:
                                findtrue = ["比用", "知一四絕", self.find_three_pass(self.all_sike()[0][0])]
                        if relation[0].count("上尅下") == 1 and relation[0].count("下賊上") == 3:
                            if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[1]) and self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[1]) :
                                findtrue = ["涉害", "度厄", self.find_three_pass(self.all_sike()[3][0])]
                            else:
                                findtrue = ["比用", "知一鑄印", self.find_three_pass(self.all_sike()[0][0])]
                        if  relation[0].count("上尅下") == 0 and relation[0].count("下賊上") == 3:
                            if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[1]) and self.Ganzhiwuxing(self.hourgangzhi[1]) != self.Ganzhiwuxing(self.daygangzhi[0]) :
                                findtrue = ["涉害", "度厄四絕", self.find_three_pass(self.all_sike()[2][1])] 
                            if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[1]) and self.Ganzhiwuxing(self.hourgangzhi[1]) == self.Ganzhiwuxing(self.daygangzhi[0]) :
                                findtrue = ["涉害", "亂首", self.find_three_pass(self.all_sike()[1][0])] 
                            if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[1]):
                                findtrue = ["涉害", "龍戰泆女", self.find_three_pass(self.all_sike()[1][0])] 
                            else:
                                findtrue = ["比用", "知一不備", self.find_three_pass(self.all_sike()[0][0])]  
                        if  relation[0].count("上尅下") == 1 and relation[0].count("下賊上") == 2:
                            f = [char for char, count in Counter([char for item in sike for char in item]).items() if count > 1]
                            if len(f) > 2:
                                if dayganzhi_yy == "陽":
                                    if self.Ganzhiwuxing(self.daygangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[1]):
                                        findtrue = ["比用", "蕪淫", self.find_three_pass(self.all_sike()[2][0])]
                                    else:
                                        findtrue = ["比用", "四絕", self.find_three_pass(self.all_sike()[0][0])] 
                                else:
                                    findtrue = ["比用", "連茹", self.find_three_pass(self.all_sike()[2][0])]  
                            if len(f)== 2 and self.Ganzhiwuxing(f[0]) == self.Ganzhiwuxing(f[1]):
                                findtrue = ["比用", "乘軒", self.find_three_pass(self.all_sike()[0][0])]  
                            if len(f) <= 1:
                                findtrue = ["涉害", "間傳"+str(f), self.find_three_pass(self.all_sike()[1][0])]  
                        if relation[0].count("上尅下") == 0 and relation[0].count("下賊上") == 2:
                            if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[1]):
                                findtrue =  ["比用", "知一元胎", self.find_three_pass(self.all_sike()[2][0])]
                            if self.Ganzhiwuxing(self.hourgangzhi[1]) == self.Ganzhiwuxing(self.daygangzhi[1]):
                                findtrue =  ["比用", "知一斫輪", self.find_three_pass(self.all_sike()[0][0])]
                            if self.Ganzhiwuxing(self.hourgangzhi[1]) == self.Ganzhiwuxing(self.daygangzhi[1]) and self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[1]):
                                if dayganzhi_yy == "陽":
                                    findtrue =  ["比用", "進茹", self.find_three_pass(self.all_sike()[2][0])]   
                                else:
                                    findtrue =  ["比用", "曲直", self.find_three_pass(self.all_sike()[1][0])]   
                            else:
                                if self.Ganzhiwuxing(self.hourgangzhi[0]) =="火":
                                    if dayganzhi_yy == "陽":
                                        if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[1]):
                                            findtrue = ["比用", "龍戰", self.find_three_pass(self.all_sike()[2][0])]
                                        if self.Ganzhiwuxing(self.hourgangzhi[1]) == self.Ganzhiwuxing(self.daygangzhi[0]) and self.Ganzhiwuxing(self.hourgangzhi[0]) != self.Ganzhiwuxing(self.daygangzhi[1]):
                                            findtrue = ["涉害", "斬關間傳", self.find_three_pass(self.all_sike()[3][0])]
                                        if self.Ganzhiwuxing(self.hourgangzhi[1]) == self.Ganzhiwuxing(self.daygangzhi[0]) and self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[1]):
                                            if self.Ganzhiwuxing(self.hourgangzhi[0]) in [char for char, count in Counter([self.Ganzhiwuxing(char) for item in sike for char in item]).items() if count > 2]:
                                                findtrue = ["比用", "知一元胎", self.find_three_pass(self.all_sike()[2][0])]
                                            else:
                                                findtrue = ["涉害", "斬關登三天狡童", self.find_three_pass(self.all_sike()[3][0])]
                                        else:
                                            findtrue = ["賊尅", "重審不備", self.find_three_pass(self.all_sike()[0][0])]
                                    else:
                                        if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[1]):
                                            findtrue =  ["比用", "知一稼穡遊子", self.find_three_pass(self.all_sike()[3][0])]
                                        else:
                                            findtrue = ["比用", "知一不備四絕", self.find_three_pass(self.all_sike()[0][0])]
                                else:
                                    if self.Ganzhiwuxing(self.daygangzhi[1])==self.Ganzhiwuxing(self.hourgangzhi[0]):
                                        findtrue = ["涉害", "見機順茹", self.find_three_pass(self.all_sike()[0][1])]
                                    if self.Ganzhiwuxing(self.daygangzhi[0])==self.Ganzhiwuxing(self.hourgangzhi[1]) and self.Ganzhiwuxing(self.daygangzhi[1])=="火":
                                        findtrue = ["涉害", "炎上", self.find_three_pass(self.all_sike()[0][0])]
                                    if self.Ganzhiwuxing(self.hourgangzhi[0])==self.Ganzhiwuxing(self.hourgangzhi[1]):
                                        findtrue = ["比用", "知一狡童", self.find_three_pass(self.all_sike()[1][0])]
                                    else:
                                        if self.Ganzhiwuxing(self.daygangzhi[0])==self.Ganzhiwuxing(self.hourgangzhi[1]):
                                            findtrue = ["涉害", "從革", self.find_three_pass(self.all_sike()[1][0])]
                                        if self.Ganzhiwuxing(self.daygangzhi[1])==self.Ganzhiwuxing(self.hourgangzhi[1]):
                                            if self.Ganzhiwuxing(self.hourgangzhi[0]) in  [char for char, count in Counter([self.Ganzhiwuxing(char) for item in sike for char in item]).items() if count >= 3][0]:
                                                findtrue = ["涉害", "斬關登三天", self.find_three_pass(self.all_sike()[0][1])]
                                            if self.Ganzhiwuxing(self.hourgangzhi[1]) in  [char for char, count in Counter([self.Ganzhiwuxing(char) for item in sike for char in item]).items() if count >= 3]:
                                                findtrue = ["比用", "退茹三奇", self.find_three_pass(self.all_sike()[2][0])]
                                            
                                            else:
                                                if len(list(set([char for char, count in Counter([self.Ganzhiwuxing(char) for item in sike for char in item]).items()]))) == 5:
                                                    findtrue = ["比同", "知一曲直"+str(), self.find_three_pass(self.all_sike()[0][0])]
                                                else:
                                                    findtrue = ["涉害", "炎上狡童"+str(), self.find_three_pass(self.all_sike()[3][0])]
                                        else:
                                            if dayganzhi_yy == "陽":
                                                if hourganzhi_yy == "陽":
                                                    if [char for char, count in Counter([self.Ganzhiwuxing(char) for item in sike for char in item]).items() if count >= 2][0] ==  self.Ganzhiwuxing(self.hourgangzhi[0]):
                                                        if [char for char, count in Counter([self.Ganzhiwuxing(char) for item in sike for char in item]).items() if count >= 3][0] == self.Ganzhiwuxing(self.hourgangzhi[0]):
                                                            findtrue = ["涉害", "登三天間傳", self.find_three_pass(self.all_sike()[0][0])]
                                                        if [char for char, count in Counter([self.Ganzhiwuxing(char) for item in sike for char in item]).items() if count >= 3][0] == self.Ganzhiwuxing(self.daygangzhi[1]):
                                                            findtrue = ["涉害", "炎上斬關狡童", self.find_three_pass(self.all_sike()[3][0])]
                                                        
                                                        else:
                                                            findtrue = ["比用", "退茹", self.find_three_pass(self.all_sike()[2][0])]
                                                    else:
                                                        findtrue = ["比用", "退茹", self.find_three_pass(self.all_sike()[0][0])]
                                                else:
                                                    if [char for char, count in Counter([self.Ganzhiwuxing(char) for item in sike for char in item]).items() if count >= 3][0] ==  self.Ganzhiwuxing(self.daygangzhi[1]):
                                                        findtrue = ["涉害", "間傳涉三淵", self.find_three_pass(self.all_sike()[0][0])]
                                                    if [char for char, count in Counter([self.Ganzhiwuxing(char) for item in sike for char in item]).items() if count >= 3][0] ==  self.Ganzhiwuxing(self.daygangzhi[0]):
                                                        findtrue = ["賊尅", "重審炎上", self.find_three_pass(self.all_sike()[0][0])]
                                                    else:
                                                        findtrue = ["涉害", "間傳1", self.find_three_pass(self.all_sike()[0][0])]
                                            else:
                                                try:
                                                    if [char for char, count in Counter([self.Ganzhiwuxing(char) for item in sike for char in item]).items() if count > 3][0] ==  self.Ganzhiwuxing(self.daygangzhi[1]):
                                                        findtrue = ["涉害", "進茹斬關", self.find_three_pass(self.all_sike()[0][0])]
                                                    else:
                                                        findtrue = ["涉害", "間傳2", self.find_three_pass(self.all_sike()[3][0])]
                                                except IndexError:
                                                    findtrue = ["比用", "從革", self.find_three_pass(self.all_sike()[0][0])]
                                
                       # else:
                       #     findtrue = ["比用", "知一", self.find_three_pass(self.all_sike()[2][0])]
            return findtrue
        elif relation[0].count("上尅下") >= 2 and relation[0].count("下賊上") == 0 and relation[9] == '天地盤沒有返吟':
            if filter_list_yy[0] == dayganzhi_yy:
                if dayganzhi_yy == "陰":
                    if self.hourgangzhi[1] in [char for item in sike for char in item] or self.Ganzhiwuxing(self.daygangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[1]):
                        if self.Ganzhiwuxing(self.daygangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[1]) and self.Ganzhiwuxing(self.daygangzhi[1]) != self.Ganzhiwuxing(self.hourgangzhi[1]) :
                            findtrue = ["涉害", "度厄四絕", self.find_three_pass(self.all_sike()[2][0])]
                        if self.Ganzhiwuxing(self.daygangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[1]) and self.Ganzhiwuxing(self.daygangzhi[1]) == self.Ganzhiwuxing(self.hourgangzhi[1]) :
                            findtrue = ["比用", "知一從革", self.find_three_pass(self.all_sike()[1][0])]
                        else:   
                            findtrue = ["比用", "曲直", self.find_three_pass(self.all_sike()[0][0])]
                    else:
                        findtrue = ["比用", "知一", self.find_three_pass(self.all_sike()[0][1])]
                if dayganzhi_yy == "陽" or self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[1]):
                    findtrue = ["比用", "知一", self.find_three_pass(self.all_sike()[0][0])]
                if self.Ganzhiwuxing(self.hourgangzhi[0]) == self.Ganzhiwuxing(self.hourgangzhi[1]) and self.Ganzhiwuxing(self.daygangzhi[0]) == self.Ganzhiwuxing(self.daygangzhi[1]):
                    if hourganzhi_yy == "陽":
                        findtrue = ["比用", "知一從革", self.find_three_pass(self.all_sike()[1][0])]
                    else:
                        findtrue = ["比用", "元胎斬關", self.find_three_pass(self.all_sike()[0][0])]
            elif filter_list_yy[1] == dayganzhi_yy:
                f = [char for char, count in Counter([char for item in sike for char in item]).items() if count > 1]
                if len(f) == 1:
                    findtrue = ["比用", "知一", self.find_three_pass(f)]
                else:
                    try:
                        f1 = [self.Ganzhiwuxing(i) for i in f].index(self.Ganzhiwuxing(self.hourgangzhi[1]))
                        findtrue = ["比用", "知一", self.find_three_pass(f[f1])]
                    except ValueError:
                        findtrue = ["比用", "知一斬關", self.find_three_pass(self.all_sike()[3][0])]
            return findtrue



    def fiter_four_ke(self):
