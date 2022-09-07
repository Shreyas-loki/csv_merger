import itertools
import json


# function definitions
def generate_testCase_for_testCaseList(testcase, content_list, parameter_list):

    output_testcases_list = []
    action_list = []

    input_testcase_id = testcase.get("testcase_id")
    # print(input_testcase_id)
    input_seq_list = testcase.get("seq")

    # logic to get the all actions of a testcase in a list
    for index in range(len(input_seq_list)):
        action = input_seq_list[index].get("action")
        action_list.append(action)
        
    # logic to add set_param at the end of the list
    index_set_param = action_list.index("set_param")
    get_set_param = action_list.pop(index_set_param)
    action_list.append(get_set_param)
    # print(action_list, '\n')
    
    # logic to get "from" values from parameter_list for action
    temp_action_from_dict = dict()

    for action_item in range(len(action_list)):
        if action_list[action_item] != "set_param":
            from_parameter_list = parameter_list[action_item].get("from")
            temp_action_from_dict[action_list[action_item]] = from_parameter_list
            # print(from_parameter_list, '\n')
    # print(temp_action_from_dict, '\n')

    l = []
    for i in temp_action_from_dict.values():
        l.append(i)
    # print(l)

    permuted_action_from_list = list(itertools.product(*l))
    # print(permuted_action_from_list, '\n')
    # use "for" loop for getting in testcase's permutations
    # then in the inner for loop have the contents_list loop
    '''
    The below for loop is the main permutation loop to generate testcase
    for a single testcase id
    '''
    count = 1

    for item in permuted_action_from_list:      
        get_actions = item

        temp_action_dict = dict()
        for i in range(len(get_actions)):
            temp_action_dict[i] = get_actions[i]
        # print(temp_action_dict)

        final_lis = []
        for x in range(len(temp_action_dict)):
            get_action = action_list[x]
            get_from = temp_action_dict.get(x)

            temp_list = []
            temp_dict = dict()
            temp_dict["action"] = get_action
            temp_dict["parameters"] = {
                "from" : get_from
            }
            temp_list.append(temp_dict)
            final_lis.append(temp_list)
            # print(temp_list)
        # print(final_lis)

        for content in content_list:
            output_single_testcase_seqList = []
            content_dict = dict()
            device, path, file = content.get("device"), content.get("path"), content.get("file")
            content_dict["action"] = "set_param"
            content_dict["parameters"] = {
                "device": device,
                "path": path,
                "file": file
            }
            # print(content_dict)
            # print('count:', count)

            output_single_testcase_dict = dict()

            content_count = 1
            for a in range(len(final_lis)):
                output_single_testcase_seqList.append(final_lis[a][0])
                if content_count <= 1:
                    output_single_testcase_seqList.append(content_dict)
                    content_count += 1


            # print(output_single_testcase_seqList)
            output_single_testcase_dict["id"] = input_testcase_id + "_" + str("%03d" % count)
            output_single_testcase_dict["desc"] = ""
            output_single_testcase_dict["seq"] = output_single_testcase_seqList

            count += 1
            # print(output_single_testcase_dict)
            output_testcases_list.append(output_single_testcase_dict)
            # "for" loop ends


        print()
    print(output_testcases_list)  

    return output_testcases_list



# main code run from here
if __name__ == '__main__':

    # input_file = input("Enter the input JSON file path: ")

    print('\n')
    with open("input.json", 'r') as file:
        inputJSONData = json.load(file)

    testcase_list = []
    content_list = []
    parameter_list = []

    for item in inputJSONData.keys():
        if item == "testCase_list":
            testcase_list = inputJSONData[item]
            # print(testcase_list, '\n')

        elif item == "content_list":
            content_list = inputJSONData[item]
            # print(content_list, '\n')

        elif item == "parameter_list":
            parameter_list = inputJSONData[item]
            # print(parameter_list, '\n')


    outputJSONData = []
    loop_count = 1

    json_sheet_name = True
    final_testcases_list = []
    outputJSONSheet = dict()
    for i in range(len(testcase_list)):

        if json_sheet_name:
            outputJSONSheet["name"] = inputJSONData["sheet"]["name"]
            outputJSONSheet["desc"] = ""
            json_sheet_name = False
       
        testcases_list = generate_testCase_for_testCaseList(testcase_list[i], content_list, parameter_list)
        final_testcases_list.extend(testcases_list)
        loop_count += 1
        
    outputJSONSheet["cases"] = final_testcases_list
    outputJSONData.append(outputJSONSheet)

    finalJSONOutputData = dict()
    finalJSONOutputData["id"] = "JSON_grouping"
    finalJSONOutputData["name"] = "New_output_grouping_for_SMA"
    finalJSONOutputData["desc"] = "" 
    finalJSONOutputData["sheet"] = outputJSONData 


    with open('final_output.json', 'w') as file:
        json.dump(finalJSONOutputData, file, indent=4)
        print('\n\n', "Output generated successfully")

    print('\n')