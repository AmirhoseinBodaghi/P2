def k_fold ():
    from sklearn.model_selection import KFold
    kf = KFold(n_splits = 10)
    x = list(range(0,1100))
    kf.get_n_splits(x)
    kf.get_n_splits(x)
    t = []
    train_text_index_for_experiments = [] #its like [[[train_indexes_1],[test_indexes_1]], ... , [[train_indexes_10],[test_indexes_10]]]
    for train_index, test_index in kf.split(x):
        t.append (train_index.tolist())
        t.append (test_index.tolist())
        train_text_index_for_experiments.append(t)
        t = []
    return train_text_index_for_experiments
#------------------------------------
def getting_data() :
    import os #for giving adress to where we want to save output files
    from openpyxl import load_workbook
    wb = load_workbook('E:\\Papers\\Paper_2\\Codes\\WithCrossFolding\\Total.xlsx')
    ws = wb.active
    name=[]
    number_of_posts = []
    number_of_followers = []
    number_of_followings = []
    number_of_likes_for_10th_ex_post = []
    number_of_likes_for_11th_ex_post = []
    number_of_likes_for_12th_ex_post = []
    number_of_self_picture_posts_form_9_previous_posts = []
    sex = []
    
    #getting data of each column of excel file into a list named by the name of corrospondant name of that column 
    for row in ws :
        name.append(row[0].value)
        number_of_posts.append(row[1].value)
        number_of_followers.append(row[2].value)
        number_of_followings.append(row[3].value)
        number_of_likes_for_10th_ex_post.append(row[4].value)
        number_of_likes_for_11th_ex_post.append(row[5].value)
        number_of_likes_for_12th_ex_post.append(row[6].value)
        number_of_self_picture_posts_form_9_previous_posts.append(row[7].value)
        sex.append(row[8].value)
#--------- deleting labels ----------
    del name [0]
    del number_of_posts [0]
    del number_of_followers [0]
    del number_of_followings [0]
    del number_of_likes_for_10th_ex_post [0]
    del number_of_likes_for_11th_ex_post [0]
    del number_of_likes_for_12th_ex_post [0]
    del number_of_self_picture_posts_form_9_previous_posts [0]
    del sex [0]

    #finding the number of users in dataset
    number_of_users_in_dataset = len (name) 
    print ("number_of_users_in_dataset = ", number_of_users_in_dataset)

    return name, number_of_posts, number_of_followers, number_of_followings, number_of_likes_for_10th_ex_post, number_of_likes_for_11th_ex_post, number_of_likes_for_12th_ex_post, number_of_self_picture_posts_form_9_previous_posts, sex, number_of_users_in_dataset 
#------------------------------------
def finding_coeficient(name, number_of_posts, number_of_followers, number_of_followings, number_of_likes_for_10th_ex_post, number_of_likes_for_11th_ex_post, number_of_likes_for_12th_ex_post, number_of_self_picture_posts_form_9_previous_posts, sex, number_of_users_in_dataset, train_index) :
    # finding the relation of self post with  "following/follower" , "like/follower" and "sex"
    # notice we want to find best amount for cc , cx , cxx , cy , cyy , cq in the equation z = cc + cx*x + cxx*x + cy*y + cyy*y + cq*q (in which x , y , q are independent variables)
    import numpy as np
    name_train = []
    number_of_posts_train = []
    number_of_followers_train = []
    number_of_followings_train = []
    number_of_likes_for_10th_ex_post_train = []
    number_of_likes_for_11th_ex_post_train = []
    number_of_likes_for_12th_ex_post_train = []
    number_of_self_picture_posts_form_9_previous_posts_train = []
    sex_train = []
    
    for index in train_index :
        name_train.append (name [index])
        number_of_posts_train.append (number_of_posts [index])
        number_of_followers_train.append (number_of_followers [index])
        number_of_followings_train.append (number_of_followings [index])
        number_of_likes_for_10th_ex_post_train.append (number_of_likes_for_10th_ex_post [index])
        number_of_likes_for_11th_ex_post_train.append (number_of_likes_for_11th_ex_post [index])
        number_of_likes_for_12th_ex_post_train.append (number_of_likes_for_12th_ex_post [index])
        number_of_self_picture_posts_form_9_previous_posts_train.append (number_of_self_picture_posts_form_9_previous_posts  [index])
        sex_train.append (sex [index])

    
    i = 0
    sex_values = []
    for st in sex_train :
        if st == "m" :
            sex_values.append(10)
        elif st == "f" :
            sex_values.append(-10)
        i+=1

    number_of_users_in_dataset = len (sex_train)
        
    c = np.ones(number_of_users_in_dataset) #we make a list c=[1,1,1,...,1] (number_of_users_in_dataset -1 elements which is same size with x , y and q) for constant amount in the equation (ie: cc) 
    x = mean_like_to_follower_for_all_users
    y = ratio_of_followings_to_followers_for_all_users
    q = sex_values


    
    
    xx = [] #we want to get xx = x**2
    xxx = [] #we want to get xxx = x**3
    for x_element in x :
        element_power_2 = x_element**2
        xx.append(element_power_2)
        element_power_3 = x_element**3
        xxx.append(element_power_3)
        
    yy = [] #we want to get yy = y**2
    yyy = [] #we want to get yyy = y**3
    for y_element in y :
        element_power_2 = y_element**2
        yy.append(element_power_2)
        element_power_3 = y_element**3
        yyy.append(element_power_3)

    
    z = number_of_self_picture_posts_form_9_previous_posts
    A_3 = np.column_stack ((c,x,xx,xxx,y,yy,yyy,q)) # cubic equation
    A_2 = np.column_stack ((c,x,xx,y,yy,q)) # quadratic equation
    B = z
    result_3, _ , _ , _ = np.linalg.lstsq(A_3, B)
    result_2, _ , _ , _ = np.linalg.lstsq(A_2, B)
    cc_3 , cx_3 , cxx_3 , cxxx_3, cy_3 , cyy_3 , cyyy_3 , cq_3   = result_3
    cc_2 , cx_2 , cxx_2 , cy_2 , cyy_2 , cq_2   = result_2
    print ("-------------------------------------")
    print("cc_3 = ",cc_3 , "cx_3 = ",cx_3 , "cxx_3 = ",cxx_3 , "cxxx_3 = ",cxxx_3 , "cy_3 = ",cy_3 , "cyy_3 = ",cyy_3 , "cyyy_3 = ",cyyy_3 , "cq_3 = ",cq_3 )
    print ("-------------------------------------")
    print("cc_2 = ",cc_2 , "cx_2 = ",cx_2 , "cxx_2 = ",cxx_3  , "cy_2 = ",cy_2 , "cyy_2 = ",cyy_2  , "cq_2 = ",cq_2 )

    return cc_3 , cx_3 , cxx_3 , cxxx_3, cy_3 , cyy_3 , cyyy_3 , cq_3 , cc_2 , cx_2 , cxx_2 , cy_2 , cyy_2 , cq_2
#-----------------------------------------------    
def Error_computing_cubic_equation(name, number_of_posts, number_of_followers, number_of_followings, number_of_likes_for_10th_ex_post, number_of_likes_for_11th_ex_post, number_of_likes_for_12th_ex_post, number_of_self_picture_posts_form_9_previous_posts, sex, number_of_users_in_dataset, cc_3 , cx_3 , cxx_3 , cxxx_3, cy_3 , cyy_3 , cyyy_3 , cq_3, test_index) :
    name_test = []
    number_of_posts_test = []
    number_of_followers_test = []
    number_of_followings_test = []
    number_of_likes_for_10th_ex_post_test = []
    number_of_likes_for_11th_ex_post_test = []
    number_of_likes_for_12th_ex_post_test = []
    number_of_self_picture_posts_form_9_previous_posts_test = []
    sex_test = []
    
    for index in test_index :
        name_test.append (name [index])
        number_of_posts_test.append (number_of_posts [index])
        number_of_followers_test.append (number_of_followers [index])
        number_of_followings_test.append (number_of_followings [index])
        number_of_likes_for_10th_ex_post_test.append (number_of_likes_for_10th_ex_post [index])
        number_of_likes_for_11th_ex_post_test.append (number_of_likes_for_11th_ex_post [index])
        number_of_likes_for_12th_ex_post_test.append (number_of_likes_for_12th_ex_post [index])
        number_of_self_picture_posts_form_9_previous_posts_test.append (number_of_self_picture_posts_form_9_previous_posts  [index])
        sex_test.append (sex [index])

    #----
    i=0
    sex_values = []
    while i < 100 :
        if sex_test[i] == "m" :
            sex_values.append(+10)
        elif sex_test[i] == "f" :
            sex_values.append(-10)
        i+=1
    #----
    i=0
    ratio_of_followings_to_followers_for_all_users = []
    while i < 100 : 
        t = number_of_followings_test[i]/number_of_followers_test[i]
        ratio_of_followings_to_followers_for_all_users.append(t)   
        i+=1
    #----
    i=0
    mean_like_for_all_users = []
    while i < 100 :
        total_like = number_of_likes_for_10th_ex_post_test[i] + number_of_likes_for_11th_ex_post_test[i] + number_of_likes_for_12th_ex_post_test[i]
        mean_like = total_like/3
        mean_like_for_all_users.append (mean_like)
        i+=1
    #----
    i=0
    mean_like_to_follower_for_all_users = []
    while i < 100 :
        mean_like_to_follower = mean_like_for_all_users[i]/number_of_followers_test[i]
        mean_like_to_follower_for_all_users.append (mean_like_to_follower)
        i+=1

    #----------------------------
    x = mean_like_to_follower_for_all_users
    y = ratio_of_followings_to_followers_for_all_users
    z = sex_values

    
    xx = [] #we want to get xx = x**2
    xxx = [] #we want to get xxx = x**3
    for x_element in x :
        element_power_2 = x_element**2
        xx.append(element_power_2)
        element_power_3 = x_element**3
        xxx.append(element_power_3)
        
    yy = [] #we want to get yy = y**2
    yyy = [] #we want to get yyy = y**3
    for y_element in y :
        element_power_2 = y_element**2
        yy.append(element_power_2)
        element_power_3 = y_element**3
        yyy.append(element_power_3)
        
    i=0
    narcissism_total = []
    while i < 100 :
        narcissism = cc_3 + cx_3*x[i] + cxx_3*xx[i] + cxxx_3*xxx[i] + cy_3*y[i] + cyy_3*yy[i] + cyyy_3*yyy[i] + cq_3*z[i]
        narcissism_total.append(narcissism)
        i+=1
    #-----------------------------
    #finding error : notice we set two group : high narcissism [5,9] (ie narcissism < %50) , low narcissism [0,4] (ie narcissism < %50), and by the above equation we find if the user belong to the first group or second group , in the following we compute our error in test dataset which is 5 in 100 means our model (above equation with the amounts we get for its variables) in 95% of cases guess true
    i=0
##    error_total = []
    error = 0
    while i < 100 :
        if narcissism_total[i] >= 5 :
            if number_of_self_picture_posts_form_9_previous_posts [i] > 4.5 :
                error += 0
            elif number_of_self_picture_posts_form_9_previous_posts [i] < 4.5 :
                error += 1
        
        elif narcissism_total[i] <= 4 :
            if number_of_self_picture_posts_form_9_previous_posts [i] < 4.5 :
                error += 0
            elif number_of_self_picture_posts_form_9_previous_posts [i] > 4.5 :
                error += 1
##        error = narcissism_total[i] - number_of_self_picture_posts_form_9_previous_posts [i]
##        error_total.append(error)
        i+=1
##    error_sum = 0
##    for e in error_total :
##        error_sum += abs(e)
##    mean_error = error_sum/100
    print("error_3 :", error)


    i=0
    error_total = []
    while i  < 100 :
        error_exact = narcissism_total[i] - number_of_self_picture_posts_form_9_previous_posts [i]
        error_total.append(error_exact)
        i+=1
    error_sum = 0
    for e in error_total :
        error_sum += abs(e)
    mean_error_exact = error_sum/100
    print("mean_error_exact_3 :",mean_error_exact)    
#-----------------------------------------------    
def Error_computing_quadratic_equation(name, number_of_posts, number_of_followers, number_of_followings, number_of_likes_for_10th_ex_post, number_of_likes_for_11th_ex_post, number_of_likes_for_12th_ex_post, number_of_self_picture_posts_form_9_previous_posts, sex, number_of_users_in_dataset, cc_2 , cx_2 , cxx_2 , cy_2 , cyy_2 , cq_2, test_index) :

    name_test = []
    number_of_posts_test = []
    number_of_followers_test = []
    number_of_followings_test = []
    number_of_likes_for_10th_ex_post_test = []
    number_of_likes_for_11th_ex_post_test = []
    number_of_likes_for_12th_ex_post_test = []
    number_of_self_picture_posts_form_9_previous_posts_test = []
    sex_test = []
    
    for index in test_index :
        name_test.append (name [index])
        number_of_posts_test.append (number_of_posts [index])
        number_of_followers_test.append (number_of_followers [index])
        number_of_followings_test.append (number_of_followings [index])
        number_of_likes_for_10th_ex_post_test.append (number_of_likes_for_10th_ex_post [index])
        number_of_likes_for_11th_ex_post_test.append (number_of_likes_for_11th_ex_post [index])
        number_of_likes_for_12th_ex_post_test.append (number_of_likes_for_12th_ex_post [index])
        number_of_self_picture_posts_form_9_previous_posts_test.append (number_of_self_picture_posts_form_9_previous_posts  [index])
        sex_test.append (sex [index])
    
    #----
    i=0
    sex_values = []
    while i < 100 :
        if sex_test[i] == "m" :
            sex_values.append(+10)
        elif sex_test[i] == "f" :
            sex_values.append(-10)
        i+=1
    #----
    i=0
    ratio_of_followings_to_followers_for_all_users = []
    while i < 100 : 
        t = number_of_followings_test[i]/number_of_followers_test[i]
        ratio_of_followings_to_followers_for_all_users.append(t)   
        i+=1
    #----
    i=0
    mean_like_for_all_users = []
    while i < 100 :
        total_like = number_of_likes_for_10th_ex_post_test[i] + number_of_likes_for_11th_ex_post_test[i] + number_of_likes_for_12th_ex_post_test[i]
        mean_like = total_like/3
        mean_like_for_all_users.append (mean_like)
        i+=1
    #----
    i=0
    mean_like_to_follower_for_all_users = []
    while i < 100 :
        mean_like_to_follower = mean_like_for_all_users_test[i]/number_of_followers_test[i]
        mean_like_to_follower_for_all_users.append (mean_like_to_follower)
        i+=1

    #----------------------------
    x = mean_like_to_follower_for_all_users
    y = ratio_of_followings_to_followers_for_all_users
    z = sex_values

    
    xx = [] #we want to get xx = x**2
    for x_element in x :
        element_power_2 = x_element**2
        xx.append(element_power_2)

        
    yy = [] #we want to get yy = y**2
    for y_element in y :
        element_power_2 = y_element**2
        yy.append(element_power_2)

        
    i=0
    narcissism_total = []
    while i < 100 :
        narcissism = cc_2 + cx_2*x[i] + cxx_2*xx[i] +  cy_2*y[i] + cyy_2*yy[i]  + cq_2*z[i]
        narcissism_total.append(narcissism)
        i+=1
    #-----------------------------
    #finding error : notice we set two group : high narcissism [5,9] (ie narcissism < %50) , low narcissism [0,4] (ie narcissism < %50), and by the above equation we find if the user belong to the first group or second group , in the following we compute our error in test dataset which is 5 in 100 means our model (above equation with the amounts we get for its variables) in 95% of cases guess true
    i=0
##    error_total = []
    error = 0
    while i < 100 :
        if narcissism_total[i] >= 5 :
            if number_of_self_picture_posts_form_9_previous_posts_test [i] > 4.5 :
                error += 0
            elif number_of_self_picture_posts_form_9_previous_posts_test [i] < 4.5 :
                error += 1
        
        elif narcissism_total[i] <= 4 :
            if number_of_self_picture_posts_form_9_previous_posts_test [i] < 4.5 :
                error += 0
            elif number_of_self_picture_posts_form_9_previous_posts_test [i] > 4.5 :
                error += 1
##        error = narcissism_total[i] - number_of_self_picture_posts_form_9_previous_posts [i]
##        error_total.append(error)
        i+=1
##    error_sum = 0
##    for e in error_total :
##        error_sum += abs(e)
##    mean_error = error_sum/100
    print("error_2 :", error)


    i=0
    error_total = []
    while i  < 100 :
        error_exact = narcissism_total [i] - number_of_self_picture_posts_form_9_previous_posts_test [i]
        error_total.append(error_exact)
        i+=1
    error_sum = 0
    for e in error_total :
        error_sum += abs(e)
    mean_error_exact = error_sum/100
    print("mean_error_exact_2 :",mean_error_exact)

#---------------------------------------
def main():
    train_text_index_for_experiments = k_fold ()  #10 sets for train and test gives us (from the 1100 index (number of whole users in both train and test)
    name, number_of_posts, number_of_followers, number_of_followings, number_of_likes_for_10th_ex_post, number_of_likes_for_11th_ex_post, number_of_likes_for_12th_ex_post, number_of_self_picture_posts_form_9_previous_posts, sex, number_of_users_in_dataset = getting_data()
    for kf in train_text_index_for_experiments :
        cc_3 , cx_3 , cxx_3 , cxxx_3, cy_3 , cyy_3 , cyyy_3 , cq_3 , cc_2 , cx_2 , cxx_2 , cy_2 , cyy_2 , cq_2 = finding_coeficient(name, number_of_posts, number_of_followers, number_of_followings, number_of_likes_for_10th_ex_post, number_of_likes_for_11th_ex_post, number_of_likes_for_12th_ex_post, number_of_self_picture_posts_form_9_previous_posts, sex, number_of_users_in_dataset, kf[0])
        Error_computing_cubic_equation(name, number_of_posts, number_of_followers, number_of_followings, number_of_likes_for_10th_ex_post, number_of_likes_for_11th_ex_post, number_of_likes_for_12th_ex_post, number_of_self_picture_posts_form_9_previous_posts, sex, number_of_users_in_dataset, cc_3 , cx_3 , cxx_3 , cxxx_3, cy_3 , cyy_3 , cyyy_3 , cq_3, kf[1])
        Error_computing_quadratic_equation(name, number_of_posts, number_of_followers, number_of_followings, number_of_likes_for_10th_ex_post, number_of_likes_for_11th_ex_post, number_of_likes_for_12th_ex_post, number_of_self_picture_posts_form_9_previous_posts, sex, number_of_users_in_dataset , cc_2 , cx_2 , cxx_2 , cy_2 , cyy_2 , cq_2, kf[1])

#---------------------------------------
main()
input("\n press enter key to exit.")
