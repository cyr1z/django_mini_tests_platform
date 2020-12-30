### Write a mini-platform for passing / creating tests

1. registration / authorization of users

2. the possibility of authorization through the social network (any one to choose from, more is possible)

3. Add a personal account - add a profile photo, name, surname, date of birth, information about yourself

4. the user can create his own test (at least 5 questions, for each question 4 possible answers, one correct; test name, description, number of passes)

5. create a page with views of all tests, filter by passed, search by name, sort by date added.

6. page of detailed display of the test - n ame, description, number of passes, comments, button "pass the test"

    6.1 if the test is passed, show the test result (number of correct answers and result in%)

    6.2 passing the test can be on one page at once or each question separately.

7. tests can be annotated
   
8. create a fixture or migration that will add two tests
   
9. configure django admin panel to view users, display test results inline in the detailed display of the user.

back - python / django (versions to taste)

front - minimal, you can bootstrap / jquery
