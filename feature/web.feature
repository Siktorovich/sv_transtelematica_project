Feature: Searching and filtering on the Yandex Market                                       
    Мне нужно выполнить тестовое задание от СЦ Транстелематика,
    В качестве кандидата на вакансию "Автотестировщик",
    Я хочу стать релевантным кандидатом и пройти на следующую ступень собеседования.

    Scenario: Smartphone searching by specified parameters
        Given full screen browser
        And Yandex Market page
        And Smartphone section
        When I push the All filters button
        And I set the search parameter to 20,000 rub. and a screen diagonal of 3 inches
        And choose at least 5 any manufacturers
        And I click the "Show" button
        And I remember the last phone on the first page
        And choose the sort by rating
        And find the phone that was remembered
        Then I print out a rating of the phone