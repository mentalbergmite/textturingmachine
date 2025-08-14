from dtm import *
import datetime


if __name__ == '__main__':
    ct = datetime.datetime.now()
    print(ct)
    print("dtm tape from module 3 video, returns yes")
    example = DTM('101000')#dtm tape from module 3 video, returns yes
    example_result = example.run()
    file_name = str(ct)+".txt"
    print("Yes" if example_result[0] else "No")
    print("Final state:",example_result[1]+'\n')
 
    print("returns NO from q1")
    example = DTM('0')#returns NO from q1
    example_result = example.run()
    file_name = str(ct)+".txt"
    print("Yes" if example_result[0] else "No")
    print("Final state:",example_result[1]+'\n')
 

    print("returns NO from q3")
    example = DTM('1')#returns NO from q3
    example_result = example.run()
    file_name = str(ct)+".txt"
    print("Yes" if example_result[0] else "No")
    print("Final state:",example_result[1]+'\n')


    print("dtm addition, expected result 10010")
    add = DTM('1101+101')#dtm addition, expected result 10010
    add_result = add.run()
    print(add_result[1])
    
    print("dtm addition error case: no number before +(should throw recursion exception)")
    add = DTM('+1101101')#dtm addition error case: no number before +(should throw recursion exception)
    add_result = add.run()
    print(add_result[1])

    print("dtm addition edge case: no number after +, assumes addition by 0")
    add = DTM('1101101+')#dtm addition edge case: no number after +, assumes addition by 0
    add_result = add.run()
    print(add_result[1])

    print("\ndtm addition error case: multiple + signs")
    add = DTM('1101++101')#dtm addition error case: multiple + signs
    add_result = add.run()
    print(add_result[1])
    
    print("dtm subtraction, expected result of 0110")
    sub = DTM('1101-111')#dtm subtraction, expected result of 0110
    sub_result = sub.run()
    print(sub_result[1])

    print("\ndtm subtraction error case: no number before -(should throw recursion exception)")
    sub = DTM('-1101111')#dtm subtraction error case: no number before -(should throw recursion exception)
    sub_result = sub.run()
    print(sub_result[1])

    print("dtm subtraction edge case: no number after -, assumes subtraction by 0")
    sub = DTM('1101111-')#dtm subtraction edge case: no number after -, assumes subtraction by 0
    sub_result = sub.run()
    print(sub_result[1])

    print("dtm subtraction error case:multiple - signs")
    sub = DTM('1101-11-1')#dtm subtraction error case:multiple - signs
    sub_result = sub.run()
    print(sub_result[1])

    user_input = ""
    while user_input != "exit":
        user_input = input("Enter a string or \"exit\" to exit: ").lower().strip()
        if user_input != "exit":
            user_dtm = DTM(user_input)
            user_result = user_dtm.run()
            print(user_result[1] if user_result[1] != "" else "Result output to file")
            del(user_dtm)