def create_test_file(filename, total_people, total_partners):
    with open(filename, 'w') as w:
        total_partners_people = total_partners * 2
        num_included = 0
        while num_included < total_people:
            if num_included < total_partners_people - 1:
                string = str(num_included) + '\t' + str(num_included + 1) + '\n'
                num_included += 2
            else:
                string = str(num_included) + '\n'
                num_included += 1
            w.write(string)

create_test_file('omar.txt', 20000, 5000)
