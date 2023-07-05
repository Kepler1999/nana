# -*- coding: utf-8 -*-
"""
Created on Fri Mar 09 09:57:34 2018

@author: admin
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 16:38:38 2018

@author: admin
"""

import copy
# import copy
import itertools
import json
import os
import random
import sys
import time

# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

# stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
# # reload(sys)
# # sys.setdefaultencoding('utf-8')
# sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponse
#
# from LogUtil import loger


from flask import Flask

app = Flask('test')


@app.route("/test/")
def main():
    def range_correct(A):
        out = (max(A) - min(A)) * max(A) * 0.1
        return out

    def myrange(A):
        out = max(A) - min(A)
        return out

    # 函数json_decode_c：Class数据转换函数
    # 输入参数：传入数据中的Class部分
    # 输出结果：object格式Class数据

    def json_decode_c(json_c):
        CC = []
        for i in range(len(json_c)):
            C = ['1', 0, '4+5']
            C[0] = str(json_c[i]['Course'])
            C[1] = int(json_c[i]['Admin_Class'])
            C[2] = str(json_c[i]['Group_ID'])
            CC.append(C)
        CCC = np.array(CC)
        C2 = CCC.astype('object')
        C2[0:, 1] = map(int, CCC[0:, 1])
        return C2

    # 函数json_decode_s：Student数据转换函数
    # 输入参数：传入数据中的Student部分
    # 输出结果：object格式Student数据

    def json_decode_s(json_s):
        SS = []
        for i in range(len(json_s)):
            S = []
            S.append(json_s[i]['ID'])
            S.append(json_s[i]['Gender'])
            S.append(json_s[i]['Admin_Class'])
            S = S + json_s[i]['Mode']
            SS.append(S)
        S2 = np.array(SS)
        S3 = S2.astype('object')
        S3[0:, 1] = map(str, S3[0:, 1])
        S3[0:, 0] = map(str, S3[0:, 0])
        for i in range(2, S2.shape[1]):
            S3[0:, i] = map(int, S3[0:, i])
        return S3

    #    处理学生成绩部分函数
    #    输入参数：json_s
    #    输出结果：放入成绩

    def json_decode_score(json_s):
        if len(json_s[0]['Score']) == 0:
            return {'code': False}
        SS = []
        for i in range(len(json_s)):
            S = []
            S = S + json_s[i]['Score']
            SS.append(S)
        S2 = np.array(SS)
        S3 = S2.astype('object')
        return {'code': True, 'result': S3}

    #    函数student_advance_list：根据解析出的提前放置学生的名单，提取出学生ID的list
    #    输入参数：提前放置学生详细信息
    #    输出结果：提前放置学生ID列表
    def student_advance_list_fun(student_advance):
        if len(student_advance) == 0:
            return False
        else:
            student_advance_list = student_advance.keys()
            return student_advance_list

    # 函数conflict：计算某两门课是否冲突
    # 输入参数：classa:a课程的课组信息；classb：b课程的课组信息
    # 输出结果：若为1则两门课存在时间冲突，否则不存在冲突

    def conflict(classa, classb):
        a = classa
        b = classb
        flag = 0
        for i in b:
            if i in a:
                flag = 1
        return flag

    # 函数get_conflict_matrix：计算所有课程的冲突矩阵
    # 输入参数：number_class：教学班数量；C：课程信息数据
    # 输出结果：number_class x number_class的冲突矩阵，1为冲突，否则不冲突

    def get_conflict_matrix(number_class, C):
        conflict_matrix = np.eye(number_class)
        for i in range(0, number_class):
            for j in range(0, number_class):
                classa = C[i].tolist()[2].split('+')
                classb = C[j].tolist()[2].split('+')
                if classa.count('') != 0:
                    classa.remove('')
                if classb.count('') != 0:
                    classb.remove('')
                if classa and classb:
                    conflict_matrix[i, j] = conflict(classa, classb)
                else:
                    conflict_matrix[i, j] = 1
                if (i == j):
                    conflict_matrix[i, j] = 0
        return conflict_matrix

    # 函数get_class_index：计算给定课程所开设教学班的Index
    # 输入参数：temp_class：Class信息；temp_dict：课程名称字典
    # 输出结果：课程开设教学班的字典

    def get_class_index(temp_class, temp_dict):
        Out = {}
        for x in temp_dict:
            Out[temp_dict[x]] = list(
                temp_class['Index'][temp_class['Course'] == temp_dict[x]].values)
        return Out

    # 函数get_alternative_options：计算备选方案函数
    # 输入参数：Mode：选课模式；conflict_matrix：冲突矩阵
    # 输出结果：每一种模式的备选方案

    def get_alternative_options(Mode, conflict_matrix):
        alternative_options = {}
        # for i in xrange(len(Mode)):
        for i in range(len(Mode)):
            class_number = get_class_number(Mode[i])
            cut_len = int(len(class_number) / 2)
            class_number1 = class_number[0:cut_len]
            class_number2 = class_number[cut_len:len(class_number)]
            hc1 = []
            hc2 = []
            hc = []
            all_options1 = itertools.product(*class_number1)
            all_options2 = itertools.product(*class_number2)
            for j in all_options1:
                all_options_index = list(j)
                if ((conflict_matrix[all_options_index,][0:, all_options_index]).sum() == 0):
                    hc1.append(all_options_index)
            for j in all_options2:
                all_options_index = list(j)
                if ((conflict_matrix[all_options_index,][0:, all_options_index]).sum() == 0):
                    hc2.append(all_options_index)
            len_hc1 = len(hc1)
            len_hc2 = len(hc2)
            index_hc1 = random.sample(range(len_hc1), len_hc1)
            index_hc2 = random.sample(range(len_hc2), len_hc2)
            if len(hc1) and len(hc2):
                for j in index_hc1:
                    for k in index_hc2:
                        all_options_index = hc1[j] + hc2[k]
                        if ((conflict_matrix[all_options_index,][0:, all_options_index]).sum() == 0):
                            hc.append(all_options_index)
            alternative_options[i] = hc
        return alternative_options

    #     函数get_class_infor:给出每个教学班对应着哪些学生，并判断教学班人数是否为空
    #    输入参数：学生选课方式
    #    输出结果：教学班的具体构成
    def get_class_infor(student_selection):
        infor = {}
        student_1 = {}
        bad_id = []
        student_numbers = []
        for i in range(number_class):
            infor[i] = []
        for i in range(len(student_information)):
            student_1 = student_information[i]
            student_id_1 = student_1[0]
            Kind = Mode.index(mode[i])
            if student_selection[i][0] == -1:
                continue
            else:
                selected_course = alternative_options[Kind][student_selection[i][0]]
                for j in range(len(selected_course)):
                    infor[selected_course[j]].append(student_id_1)
        for key in infor:
            s_numbers = len(infor[key])
            if s_numbers == 0:
                bad_id.append(key)
            student_numbers.append(s_numbers)
        return {'infor': infor, 'bad_id': bad_id, 'student_numbers': student_numbers}

    # 函数get_population：生成一个种群的函数
    # 输入参数：population_name，随机数，不影响结果
    # 输出结果：'E_M'：各个教学班的学生数；'Load'：学生选课方式

    def get_population(population_name):
        student_number_course = np.zeros((number_class, 1))
        student_selection = np.zeros((number_student, 1))
        student_selection.dtype = int
        index_student = random.sample(range(number_student), number_student)
        for ii in range(number_student):
            i = index_student[ii]
            kind = Mode.index(mode[i])

            l1 = student.iloc[[i]].values[0]
            sstudentID = l1[0]
            # print sstudentID
            wrong_mode_student_id = []
            # alternative_options=get_alternative_options(Mode,conflict_matrix)
            # 后面有定义Hcc=getHC(Mode,C_M)，那么此处的HC就是对用模式下的符合冲突矩阵要求的所有教学班的排列组合
            mode_i_alternative_options = alternative_options[kind]
            if mode_i_alternative_options:
                mode_i_alternative_options_2 = []
                if student_advance:
                    if sstudentID in student_advance_list:
                        advance_class = student_advance[sstudentID]
                        len1 = len(advance_class)
                        for n in range(len(mode_i_alternative_options)):  # 遍历每一种备选方案
                            k = 0
                            for key in advance_class.iterkeys():  # 遍历每一门课
                                temp_advance_class = advance_class[key]
                                if len(list(
                                        set(temp_advance_class).intersection(set(mode_i_alternative_options[n])))) == 0:
                                    break
                                k = k + 1
                                if k == len1:
                                    mode_i_alternative_options_2.append(
                                        mode_i_alternative_options[n])
                    else:
                        mode_i_alternative_options_2 = mode_i_alternative_options
                else:
                    mode_i_alternative_options_2 = mode_i_alternative_options

                E_M2 = np.repeat(student_number_course, len(mode_i_alternative_options)).reshape(
                    (number_class, len(mode_i_alternative_options)))
                for j in range(len(mode_i_alternative_options)):
                    if mode_i_alternative_options[j] in mode_i_alternative_options_2:
                        E_M2[mode_i_alternative_options[j], j] += 1
                people = []
                for k in range(len(mode_i_alternative_options)):
                    PC = []
                    for y in range(len(temp_dict)):
                        PC.append(E_M2[class_index[temp_dict[y]], k])
                    if mode_i_alternative_options[k] in mode_i_alternative_options_2:
                        # temp_people = map(range_correct, PC)
                        #
                        temp_people = []
                        for x in PC:
                            temp_people.append(range_correct(x))
                        #
                        people.append(sum(temp_people) * max(temp_people) * 0.1)
                    else:
                        people.append(20000)
                min_people = min(people)
                Times = people.count(min_people)
                if Times != 1:
                    times = random.sample(range(Times), 1)[0]
                    while times >= 2:
                        times = times - 1
                        people[people.index(min_people)] = 10000
                index_min = people.index(min_people)
                ID = mode_i_alternative_options[index_min]
                student_selection[i, 0] = index_min
                student_number_course[ID] += 1
            else:
                student_selection[i, 0] = -1
                wrong_mode_student_id.append(sstudentID)
        print('get one popu')
        bad_id = get_class_infor(student_selection)['bad_id']
        return {'E_M': student_number_course, 'Load': student_selection, 'bad_id': bad_id,
                'wrong_mode_student_id': wrong_mode_student_id}

    # 函数range_population：计算所有课程的极差和及各个课程的极差
    # 输入参数：E_M：各个教学班的学生数
    # 输出结果：int(sum_out[0])：极差之和；individual_out：各个课程的极差

    def range_population(E_M):
        sum_out = 0
        individual_out = []
        for i in range(len(temp_dict)):
            cur2 = myrange(E_M[class_index[temp_dict[i]]])
            sum_out = sum_out + cur2
            individual_out.append(cur2[0])
        return int(sum_out[0]), individual_out

    # 函数initial_population：生成初始种群
    # 输入参数：best_range：极差设置；iteration_times：迭代次数
    # 输出结果：初始种群

    def initial_population(best_range, iteration_times):
        count = 0
        start = time.time()
        population = get_population(random.randint(0, 100))
        print(range_population(population['E_M'])[1])
        if population['wrong_mode_student_id'] or population['bad_id']:
            return population
        else:
            end = time.time()
            temp_time = end - start
            all_time = round((temp_time * iteration_times) / 60, 2)
            # loger('Initialization needs about ' + str(all_time) + ' minutes')
            Grade1 = range_population(population['E_M'])
            sum_range1 = Grade1[0]
            individual_range1 = Grade1[1]
            # grade_min=sum_range1
            if max(individual_range1) <= best_range:
                return population
            while count <= iteration_times:
                count += 1
                population2 = get_population(random.randint(0, 10))
                Grade2 = range_population(population2['E_M'])
                sum_range2 = Grade2[0]
                individual_range2 = Grade2[1]
                if max(individual_range2) <= best_range:
                    population = population2
                    break
                if sum_range2 < sum_range1:
                    population = population2
                    sum_range1 = sum_range2
                #                mylogger('Initialization is normal')
                print(max(individual_range2))
        return population

    # 函数get_evaluation_matrix：给出男生人数、各个行政班人数
    # 输入参数：学生选课方式
    # 输出结果：评价矩阵

    def get_evaluation_matrix(student_selection):
        evaluation_matrix = np.zeros((number_class, number_admin + 1))
        for i in range(len(student_information)):
            Kind = Mode.index(mode[i])
            if len(alternative_options[Kind]) > 0:
                Row = alternative_options[Kind][student_selection[i][0]]
                if student_information[i, 1] == 'M':
                    evaluation_matrix[Row, 0] += 1
                student_i_admin = student_information[i, 2]
                evaluation_matrix[Row, student_i_admin] += 1
        return evaluation_matrix

    # 函数purity：计算教学班人员构成纯度
    # 输入参数：某一门课某教学班行政班人员构成
    # 输出结果：该教学班行政班指标得分

    def purity(slice):
        sum_slice = slice.sum()
        if sum_slice == 0:
            slice_grade = 0.0
        if sum_slice != 0:
            proportion = slice / sum_slice
            slice_grade = sum([i * i for i in proportion])
        return slice_grade

    #    函数get_average_grade：给出每个教学班的平均成绩,学生的总成绩
    #    输入参数：学生选课方式
    #    输出结果：平均成绩
    def get_average_grade(student_selection, student_grade):
        infor = get_class_infor(student_selection)['infor']
        all_average_grades = {}
        for i in range(len(temp_dict)):
            average_grades = []
            course = temp_dict[i]
            courses = class_index[course]
            for j in range(len(courses)):
                sum_grade = 0
                courses_this = courses[j]
                all_students = infor[courses_this]
                for k in range(len(all_students)):
                    s = (
                        student_grade.loc[student_grade.ID == all_students[k]])
                    sum_grade += int(s.loc[0:, course])
                average_grade = sum_grade / len(infor[courses[j]])
                average_grades.append(average_grade)
            all_average_grades[course] = average_grades
        return all_average_grades

    # 函数calculate_points：评分函数
    # 输入参数：student_seclection:学生选课方式；number_student_class：各个教学班学生人数；
    # 输入参数：flag_gender：是否男女比例均衡;flag_admin：是否行政班均衡
    # 输出结果：种群得分

    def calculate_points(student_selection, number_student_class, student_grade, flag_gender=1, flag_admin=1):
        evaluation_matrix_2 = get_evaluation_matrix(student_selection)
        if student_grade_code:
            all_average_grades = {}
            all_average_grades = get_average_grade(
                student_selection, student_grade)
        grades = 0
        total_student = number_student_class.sum()
        for k in range(len(temp_dict)):
            row = class_index[temp_dict[k]]
            if len(row) > 0:
                NN = len(row)
                Cur = evaluation_matrix_2[row]
                full = number_student_class[row]
                full = full.reshape((1, NN))
                ZongRenShu = full.sum()
                NanShengShu = Cur[0:, 0].sum()
                ZuiJiaBiLi = NanShengShu / ZongRenShu
                P1 = abs(Cur[0:, 0] / full - ZuiJiaBiLi).sum()
                P2 = np.apply_along_axis(purity, 0, Cur[0:, 1:]).sum()
                WP = ZongRenShu / total_student

                if student_grade_code == False:
                    grades = grades + flag_gender * P1 * WP - flag_admin * P2 * WP * 0.2
                else:
                    list1 = all_average_grades[temp_dict[k]]
                    std1 = np.std(list1)
                    mean1 = np.mean(list1)
                    if mean1 <= 0:
                        P3 = 0
                    if mean1 > 0:
                        P3 = 10 * std1 / mean1
                    grades = grades + flag_gender * P1 * WP - flag_admin * P2 * WP * 0.2 + P3 * WP
        return grades

    # 函数mute：交叉进化函数
    # 输入参数：student_seclection:学生选课方式；number_student_class：各个教学班学生人数
    # 输入参数：max_iteration：最大迭代次数；flag_gender：是否男女比例均衡;flag_admin：是否行政班均衡
    # 返回最终学生选课结果

    def mute(student_selection, number_student_class, max_iteration, flag_gender, flag_admin, student_grade):
        points_now = calculate_points(
            student_selection, number_student_class, student_grade, flag_gender, flag_admin)
        mute_times = 0
        while mute_times <= max_iteration:
            mute_times += 1
            start = time.time()
            student_selection_2 = copy.deepcopy(student_selection)
            kind = random.sample(range(len(pool)), 1)
            while len(pool[kind[0]]) == 1:
                kind = random.sample(pool_scheme, 1)
            kind = kind[0]
            if student_advance:
                student_advance_index = []
                for i in range(len(student_advance_list)):
                    student_advance_id = student_advance_list[i]
                    student_advance_index1 = student.loc[student.ID ==
                                                         student_advance_id].index.values[0]
                    student_advance_index.append(student_advance_index1)
                pool2 = list(set(pool[kind]).difference(
                    set(student_advance_index)))
                Index = random.sample(pool2, 2)
            else:
                Index = random.sample(pool[kind], 2)

            student_selection_2[Index[0]] = student_selection[Index[1]]
            student_selection_2[Index[1]] = student_selection[Index[0]]
            points_next = calculate_points(
                student_selection_2, number_student_class, student_grade, flag_gender, flag_admin)
            if points_next < points_now:
                student_selection = student_selection_2
                points_now = points_next
                print('Lucky')
            if mute_times == 1:
                end = time.time()
                temp_time = end - start
                all_time = round((temp_time * max_iteration) / 60, 2)
                # loger('Evolution needs about ' + str(all_time) + ' minutes')
        return student_selection

    # 函数population_evaluation：分学生结果评价函数
    # 输入参数：student_seclection:学生选课方式；number_student_class：各个教学班学生人数
    # 输出结果：某门课的极差、各个教学班人数、与最佳性别比例的差值、各个教学班主要包括哪个行政班学生

    def population_evaluation(student_selection, number_student_class):
        evaluation_matrix_2 = get_evaluation_matrix(student_selection)
        out = {}
        for k in range(len(temp_dict)):
            temp_out = {}
            row = class_index[temp_dict[k]]
            current_evaluation_matrix = evaluation_matrix_2[row]
            full = number_student_class[row]
            NN = len(row)
            temp_out['0.Subject'] = (temp_dict[k])
            temp_out['1.Pole'] = int(max(full) - min(full))
            full = full.reshape((1, NN))
            temp_out['2.Full'] = full.tolist()
            ZongRenShu = full.sum()
            NanShengShu = current_evaluation_matrix[0:, 0].sum()
            ZuiJiaBiLi = NanShengShu / ZongRenShu
            P1 = (current_evaluation_matrix[0:, 0] / full - ZuiJiaBiLi)
            temp_out['3.Gender'] = P1.tolist()
            P2 = np.apply_along_axis(max, 1, current_evaluation_matrix[0:, 1:])
            temp_out['4.Center'] = P2.tolist()
            # Out.append(out)
            out[temp_dict[k]] = temp_out
        return out

    # 函数student_encode_json：学生选课数据转换为json格式函数
    # 输入参数：mode：学生选课情况；student_selection:学生选课方式；
    # 输出参数：字典形式的分学生结果

    def student_encode_json(mode, student_selection):
        schedule = {}
        for i in range(number_student):
            kind = Mode.index(mode[i])
            alternative_options_i = alternative_options[kind]
            if alternative_options_i:
                student_selection_i = student_selection[i][0]
                student_selection_i_now = alternative_options_i[student_selection_i]
                AAA = []
                for j in range(len(student_selection_i_now)):
                    AAA.append(
                        temp_class[temp_class['Index'] == student_selection_i_now[j]].iloc[:, 3].values[0])
                    schedule[student['ID'][i]] = AAA
        return schedule

    # jsonD = json.loads(request.body)
    #
    path = r"D:\Repo\Piake\1121.json"
    # jsonD = json.loads(path)
    with open(path, encoding="utf-8") as f:
        jsonD = json.load(f)
    #
    total_keys = jsonD.keys()
    if 'Initialization_times' in total_keys:
        population_iteration_times = jsonD['Initialization_times']
    else:
        population_iteration_times = 15
    if 'Evolution_times' in total_keys:
        mute_iteration_times = jsonD['Evolution_times']
    else:
        mute_iteration_times = 300
    rigidIndex = jsonD['rigidIndex']
    task_id = str(jsonD['taskId'])
    start_time = time.strftime('%Y_%m_%d_%H_%M_%S',
                               time.localtime(time.time()))
    # loger('/outcome: task ' +
    #       task_id + ' , start_time: ' + start_time)
    # max_renshu=rigidIndex[0]['MaxRenshu']
    max_range = rigidIndex[1]['Pole']
    soft_index = jsonD['softIndex']
    # population_value=soft_index[0]['PopuValue']
    gender_value = soft_index[1]['GenderValue']
    admin_value = soft_index[2]['AdminValue']
    C = json_decode_c(jsonD['Class'])
    number_class = C.shape[0]
    ClassID = []
    for i in range(number_class):
        ClassID.append(str(jsonD['Class'][i]['ClassID']))
    S = json_decode_s(jsonD['Student'])
    temp_class = pd.DataFrame(C)
    temp_class.columns = ['Course', 'Admin_Class', 'Group_ID']
    temp_class["ClassID"] = ClassID
    student = pd.DataFrame(S)
    number_subject = S.shape[1] - 3
    colName = ['ID', 'Gender', 'Admin_Class']
    for i in range(number_subject):
        colName.append(str(i + 1))
    student.columns = colName

    student_grade_fun = json_decode_score(jsonD['Student'])
    student_grade_code = student_grade_fun['code']
    if student_grade_code:
        student_grade = student_grade_fun['result']
        student_grade = pd.DataFrame(student_grade)
        colName2 = []
        for i in range(number_subject):
            colName2.append(str(i + 1))
        student_grade.columns = colName2
        student_grade['ID'] = student['ID']

    number_student = S.shape[0]
    temp_class["Index"] = np.arange(number_class)
    number_subject = len(temp_class['Course'].unique())
    temp_dict = {}
    for i in range(number_subject):
        temp_dict[i] = str(i + 1)
    number_admin = len(student['Admin_Class'].unique())
    student_information = S[0:, 0:3]
    # loger('Checking data...')
    match_wrong_code = 200
    match_wrong_class = []
    temp_match_name = map(str, range(1, number_subject + 1))
    for i in range(len(C)):
        match_slice = C[i].tolist()
        if (match_slice[0] in temp_match_name) == False:
            match_wrong_code = -1
            match_wrong_class.append(match_slice)
    if match_wrong_code == -1:
        warning_code_options = {'HcCode': -1,
                                'Unmatched Class': match_wrong_class,
                                'taskId': task_id}
        end_time = time.strftime('%Y_%m_%d_%H_%M_%S',
                                 time.localtime(time.time()))
        # if not os.path.exists('result'):
        #     os.makedirs('result')
        # file_name = 'result/outcome-' + \
        #             task_id + '-' + start_time + '__' + end_time + '.json'
        # with open(file_name, "w") as f:
        #     json.dump(warning_code_options, f)
        #     # loger('/outcome: task ' + task_id + ' ,result file is ok! start_time: ' +
        #     #       start_time + ';end_time:' + end_time)
        #     # loger('/outcome: ' + file_name)
        # # return HttpResponse(json.dumps(warning_code_options), content_type='application/json')
        # return json.dumps(warning_code_options)
    # loger('Computing alternative options...')
    mode = S[0:, 3:].tolist()
    Mode = []
    for i in range(len(mode)):
        if Mode.count(mode[i]) == 0:
            Mode.append(mode[i])

    # 函数mode_pool：每一种模式下都有哪些学生
    # 输入参数：Mode：学生选课种类；mode：学生选课情况
    # 输出结果：每一种模式下都有哪些学生

    def mode_pool(Mode, mode):
        temp_pool = {}
        for i in range(len(Mode)):
            Cur = []
            for k in range(len(mode)):
                if Mode.index(mode[k]) == i:
                    Cur.append(k)
            temp_pool[i] = Cur
        return temp_pool

    # 函数pool_scheme_function：扩展方式pool
    # 输入参数：Pool：每一种选课模式下有哪些学生
    # 输出结果：pool_scheme：学生选课模式构成如【1,1,1,2,2,3,3,3,3】

    def pool_scheme_function(Pool):
        pool_scheme = []
        for i in range(len(Pool)):
            pool_scheme = pool_scheme + [i] * len(Pool[i])
        return pool_scheme

    # 函数get_class_number：某种模式下，每一门课都有哪些教学班
    # 输入参数：mode_one：某种选课模式
    # 输出结果：out：该模式下各门课包括的教学班

    def get_class_number(mode_one):
        out = []
        for i in range(len(mode_one)):
            if (mode_one[i] == 1):
                out.append(
                    (temp_class[temp_class['Course'] == temp_dict[i]]['Index']).values.tolist())
        return (out)

    pool = mode_pool(Mode, mode)
    pool_scheme = pool_scheme_function(pool)
    conflict_matrix = get_conflict_matrix(number_class, C)
    class_index = get_class_index(temp_class, temp_dict)

    total_keys = jsonD.keys()
    if 'Advance_Student' in total_keys:
        student_advance = jsonD['Advance_Student']
    else:
        student_advance = {}

    def find_index(one_class):
        return np.where(temp_class['ClassID'] == str(one_class))[0][0]

    student_advance_list = student_advance_list_fun(student_advance)
    for i in range(len(student_advance)):
        temp_i_student_ac = student_advance[student_advance_list[i]]
        temp_ac_key = temp_i_student_ac.keys()
        for j in range(len(temp_i_student_ac)):
            temp_i_student_ac[temp_ac_key[j]] = map(
                find_index, temp_i_student_ac[temp_ac_key[j]])
        student_advance[student_advance_list[i]] = temp_i_student_ac

    alternative_options = get_alternative_options(Mode, conflict_matrix)

    warning_code = 200
    wrong_alternative_options = []
    for i in range(len(alternative_options)):
        if alternative_options[i] == []:
            warning_code = -1
            wrong_alternative_options.append(Mode[i])
    warning_code_options = {'HcCode': warning_code,
                            'WrongHc': wrong_alternative_options}
    '''
    if warning_code==-1:
        return HttpResponse(json.dumps(warning_code_options),content_type='application/json')
    '''
    # loger('Initializing population...')
    if wrong_alternative_options:
        population_iteration_times = 0
    first_population = initial_population(
        best_range=max_range, iteration_times=population_iteration_times)

    if wrong_alternative_options or first_population['bad_id']:
        final_population = first_population['Load']
        # loger('return initial population')
    else:
        # loger('Evolving')
        student_grade['ID'] = map(str, student_grade['ID'])
        if gender_value == False and admin_value == False:
            final_population = mute(student_selection=first_population['Load'], number_student_class=first_population[
                'E_M'], max_iteration=1, flag_gender=0, flag_admin=0, student_grade=student_grade)
        if gender_value and admin_value:
            final_population = mute(student_selection=first_population['Load'],
                                    number_student_class=first_population['E_M'],
                                    max_iteration=mute_iteration_times, flag_gender=1, flag_admin=1,
                                    student_grade=student_grade)
        if gender_value and admin_value == False:
            final_population = mute(student_selection=first_population['Load'],
                                    number_student_class=first_population['E_M'],
                                    max_iteration=mute_iteration_times, flag_gender=1, flag_admin=0,
                                    student_grade=student_grade)
        if gender_value == False and admin_value:
            final_population = mute(student_selection=first_population['Load'],
                                    number_student_class=first_population['E_M'],
                                    max_iteration=mute_iteration_times, flag_gender=0, flag_admin=1,
                                    student_grade=student_grade)
        # final_evaluation_matrix=population_evaluation(student_selection=final_population,number_student_class=first_population['E_M'])

    final_student_selection = student_encode_json(mode, final_population)
    infor_return = get_class_infor(final_population)['student_numbers']
    student_numbers_for_class = list(zip(
        temp_class.loc[:, 'ClassID'].values.tolist(), infor_return))
    bad_index = first_population['bad_id']
    bad_ids = []
    pole_grade = range_population(first_population['E_M'])[1]
    #
    out_come ={}
    print(warning_code)
    #
    if bad_index:
        bad_ids = temp_class.loc[bad_index, 'ClassID'].values.tolist()
    if warning_code == 200:
        warning_code_options = {'HcCode': 200, 'WrongHc': 'Nothing'}
        #
        out_come['pole'] = pole_grade
        out_come['HccCode'] = warning_code_options
        out_come['Schedule'] = final_student_selection
        out_come['Bad_id'] = bad_ids
        out_come['Student_numbers_for_class'] = student_numbers_for_class
        #
        # out_come = {'pole': pole_grade, 'HccCode': warning_code_options, 'Schedule': final_student_selection,
        #             'Bad_id': bad_ids, 'Student_numbers_for_class': student_numbers_for_class}
    if warning_code == -1:
        out_come['HcCode'] = -1
        out_come['WrongHc'] = wrong_alternative_options
        out_come['Schedule'] = final_student_selection
        out_come['Bad_id'] = bad_ids
        out_come['Student_numbers_for_class'] = student_numbers_for_class
        out_come['taskId'] = task_id


        # out_come = {'HcCode': -1, 'WrongHc': wrong_alternative_options, 'Schedule': final_student_selection,
        #             'Bad_id': bad_ids, 'Student_numbers_for_class': student_numbers_for_class, 'taskId': task_id}
    end_time = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
    # if not os.path.exists('result'):
    #     os.makedirs('result')
    # file_name = 'result/outcome-' + \
    #             task_id + '-' + start_time + '__' + end_time + '.json'
    # with open(file_name, "w", encoding="utf-8") as f:
    #     json.dump(out_come, f)
        # loger('/outcome: task ' + task_id + ' ,result file is ok! start_time: ' +
        #       start_time + ';end_time:' + end_time)
        # loger('/outcome: ' + file_name)
    # return HttpResponse(json.dumps(out_come), content_type='application/json')
    # return json.dumps(out_come)
    return json.dumps(out_come)

if __name__ == '__main__':
    app.run(debug=True)
