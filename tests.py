from scripts import functions

def test_scroll_status_bar():
    assert functions.scroll_status_bar(3, 5) == '>>>..'
    assert functions.scroll_status_bar(1, 5) == '>....'
    assert functions.scroll_status_bar(4, 7) == '>>>>...'
    assert functions.scroll_status_bar(0, 3) == '...'
    assert functions.scroll_status_bar(1, 1) == '>'

def test_compare_for_unfollow():
    assert functions.compare_for_unfollow(['Kamil', 'Jakub', 'Szymon'], ['Jakub', 'Szymon']) == []
    assert functions.compare_for_unfollow([], ['Jakub', 'Szymon']) == ['Jakub', 'Szymon']
    assert functions.compare_for_unfollow(['Michał', 'Czesław'], ['Michał', 'Czesław']) == []

def test_compare_with_keep_following():
    assert functions.compare_with_keep_following(['Kamil', 'Jakub', 'Szymon'], ['Jakub', 'Szymon']) == ['Kamil']
    assert functions.compare_with_keep_following([], ['Jakub', 'Szymon']) == []
    assert functions.compare_with_keep_following(['Kamil', 'Jakub', 'Szymon'], ['Marcin', 'Michał']) == ['Kamil', 'Jakub', 'Szymon']

def test_count_people():
    assert functions.count_people([['Marcin', 'Michał', 'Marek'], ['Marek', 'Michał'], ['Marcin']]) == {'Marcin': 2, 'Michał': 2, 'Marek': 2}
    assert functions.count_people([['Marcin', 'Krystian', 'Marek'], ['Krystian', 'Michał'], ['Krystian']]) == {'Krystian': 3, 'Michał': 1, 'Marek': 1, 'Marcin': 1}
    assert functions.count_people([['Marcin'], ['Marcin'], ['Marcin']]) == {'Marcin': 3}

def test_flask():
    def try_flask():
        ### Flask is not installed ###
        try:
            from flask import Flask
            return True
        except:
            return False
    assert try_flask() == True

def test_selenium():
    def try_selenium():
        ### Selenium is not installed ####
        try:
            from selenium import webdriver
            return True
        except:
            return False
    assert try_selenium() == True

def test_webdriver():
    def check_chrome():
        try:
            ### Chromedriver is not installed ###
            import scripts.selenium_browser as selenium_browser
            selenium_browser.init()
            selenium_browser.get_browser()
            selenium_browser.close_browser()
            return True
        except:
            return False
    assert check_chrome() == True