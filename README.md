# Python_spam_filter
Spam filter using Naive Bayesian classifier 
# Training procedure:
1. Find the ratio of spam and ham emails to all emails.
2. Count how many times each word occurs in spam and ham.
3. Calculate the sum of the words in ham and spam
4. Find the ratio of each word to the number of words in spam and ham. These values
are used as probabilities to determine spam.
# Text processing:
For proper filtering, text needs to be split into words. The process in my spam filter
was as follows:
1. Remove all capital letters using the lower function.
2. Replace special symbols (e.g. '.', '?', '@'...) with an empty string
3. Count the words
The functions for these steps are in the module utils.py
# Datasets:
1. TRUTH_FILE is file with a name of mail and with a SPAM_TAG or HAM_TAG after it (for constants look utils.py)
2. Mails are text files that will be read
# How to use:
1. Create object MyFilter
2. Use method train(path), where path is location directory where is TRUTH_FILE located
3. Use method test(path), where path is location of directory where PREDICTION_FILE will be created
